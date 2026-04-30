import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from llm_cleaner import clean_batch
from validation import validate
from retry import retry

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(BASE_DIR, "data.xlsx")
output_file = os.path.join(BASE_DIR, "output.xlsx")
error_log_file = os.path.join(BASE_DIR, "error_log.txt")


BATCH_SIZE = 20      
SMALL_BATCH = 10    
MAX_RETRY = 1
MAX_WORKERS = 2     



df = pd.read_excel(input_file)

if "Desc" not in df.columns:
    raise ValueError("No Desc column")

df = df[df["Desc"].notna()].copy()
df["Desc"] = df["Desc"].astype(str).str.strip()
df = df[df["Desc"] != ""]

rows = df["Desc"].tolist()
total = len(rows)

print(f"Starting processing {total} rows...")
print(f"Batch={BATCH_SIZE}, Fallback={SMALL_BATCH}, Workers={MAX_WORKERS}\n")



def process_batch(batch, batch_number):
    print(f"\n Starting Batch {batch_number}...")

    local_results = []
    local_errors = []

    try:
        print(f" Batch {batch_number} calling LLM...")
        cleaned_list = clean_batch(batch)
        print(f" Batch {batch_number} LLM returned")

  
        if len(cleaned_list) == len(batch):
            for raw, cleaned in zip(batch, cleaned_list):
                val = validate(cleaned)

                attempt = 0
                while not val["is_valid"] and attempt < MAX_RETRY:
                    cleaned = retry(raw, cleaned, val["issues"])
                    val = validate(cleaned)
                    attempt += 1

                local_results.append({
                    "original": raw,
                    "cleaned": cleaned,
                    "is_valid": val["is_valid"],
                    "validation_issues": ", ".join(val["issues"]),
                    "retry_count": attempt
                })

   
        else:
            print(f" Batch {batch_number} mismatch → fallback to {SMALL_BATCH}")

            for i in range(0, len(batch), SMALL_BATCH):
                sub_batch = batch[i:i + SMALL_BATCH]
                print(f" Sub-batch size: {len(sub_batch)}")

                try:
                    sub_cleaned = clean_batch(sub_batch)
                    if len(sub_cleaned) == len(sub_batch):
                        for raw, cleaned in zip(sub_batch, sub_cleaned):
                            val = validate(cleaned)

                            attempt = 0
                            while not val["is_valid"] and attempt < MAX_RETRY:
                                cleaned = retry(raw, cleaned, val["issues"])
                                val = validate(cleaned)
                                attempt += 1

                            local_results.append({
                                "original": raw,
                                "cleaned": cleaned,
                                "is_valid": val["is_valid"],
                                "validation_issues": ", ".join(val["issues"]),
                                "retry_count": attempt
                            })

                    else:
                        print(f" Sub-batch mismatch → mark as error")

                        for raw in sub_batch:
                            local_results.append({
                                "original": raw,
                                "cleaned": "",
                                "is_valid": False,
                                "validation_issues": "SUB_BATCH_ERROR",
                                "retry_count": 0
                            })

                        local_errors.append(
                            f"Sub-batch mismatch | Batch {batch_number} | size={len(sub_batch)}"
                        )

                except Exception as e:
                    print(f" Sub-batch crashed")

                    for raw in sub_batch:
                        local_results.append({
                            "original": raw,
                            "cleaned": "",
                            "is_valid": False,
                            "validation_issues": "SUB_BATCH_EXCEPTION",
                            "retry_count": 0
                        })

                    local_errors.append(
                        f"Sub-batch exception | Batch {batch_number} | Error: {str(e)}"
                    )

        print(f" Batch {batch_number} done")

    except Exception as e:
        print(f" Batch {batch_number} crashed")

        local_errors.append(f"Batch {batch_number} error: {str(e)}")

        for raw in batch:
            local_results.append({
                "original": raw,
                "cleaned": "",
                "is_valid": False,
                "validation_issues": "BATCH_ERROR",
                "retry_count": 0})

    return local_results, local_errors


results = []
errors = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = []

    for start_idx in range(0, total, BATCH_SIZE):
        batch = rows[start_idx:start_idx + BATCH_SIZE]
        batch_number = start_idx // BATCH_SIZE + 1
        futures.append(
            executor.submit(process_batch, batch, batch_number)
        )

    for future in as_completed(futures):
        res, err = future.result()
        results.extend(res)
        errors.extend(err)

output_df = pd.DataFrame(results)
output_df.to_excel(output_file, index=False)


if errors:
    with open(error_log_file, "w", encoding="utf-8") as f:
        for err in errors:
            f.write(err + "\n")

    print(f"\nErrors logged to: {error_log_file}")
else:
    print("\nNo system errors.")


valid_count = sum(1 for r in results if r["is_valid"])
valid_rate = round(valid_count / len(results) * 100, 2) if results else 0


print(f"Done, output saved to: {output_file}")
