"""
This script processes large volumes of messy product descriptions and extracts structured fields including:
- Manufacturer (brand)
- Model / branch
- Production year
- Product type



Output:
Structured dataset with extracted metadata fields for downstream analysis or reporting.
"""

import pandas as pd
from openai import OpenAI
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# API Key
client = OpenAI(api_key="AAC")

# logging
logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

# load data
df = pd.read_excel("data.xlsx")

BATCH_SIZE = 10
MAX_WORKERS = 5 


def clean_batch(texts, start_index):
    batch_input = "\n".join([str(t) for t in texts])

    prompt = f"""Clean each line to: Manufacturer Model Year

Rules:
1. Keep ONLY:
   - manufacturer
   - vehicle model
   - year

2. Remove everything else (Rears, Driver, Rubber, Binding, Cabrio, random suffix, etc.)

3. Year normalization:
   - Extract the most valid year pattern from the text
   - Accept formats like:
     yyyy-yyyy
     yyyy
     yyyy> or >yyyy
     -yyyy
     yyyy-
     yy- and many others
   - Convert to:
     yyyy-yyyy -> yy-yy
     yyyy -> yy-
     yyyy> or >yyyy -> yy-
     -yyyy -> -yy
     yy- -> yy-
     yy-yy -> yy-yy
     yy - yy -> yy-yy
     yy-yyabc -> yy-yy

4. IMPORTANT:
   - If year contains extra characters (e.g. "05-12abcd", "2015xyz"), REMOVE the extra part
   - Only keep clean numeric year format

5. Output must strictly be:
   Manufacturer Model YY-YY / YY- / -YY

6. If no valid year is found:
   return Manufacturer Model only

Return exactly one line per input line, same order.

Input:
{batch_input}
"""

    for attempt in range(3):
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
                temperature=0
            )

            raw = response.output_text.strip()

            result = [line.strip() for line in raw.split("\n") if line.strip()]

            if len(result) != len(texts):
                logging.error(f"Mismatch batch {start_index} | in={len(texts)} out={len(result)}")
                raise ValueError("Length mismatch")

            return result

        except Exception as e:
            logging.error(f"Batch {start_index} Attempt {attempt} | Error: {str(e)}")
            time.sleep(2 * (attempt + 1))

    return ["ERROR"] * len(texts)


results = [None] * len(df)

def process_batch(i):
    batch = df["Desc"].iloc[i:i+BATCH_SIZE].fillna("").tolist()
    cleaned = clean_batch(batch, i)
    return i, cleaned


print("Starting...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = []

    for i in range(0, len(df), BATCH_SIZE):
        futures.append(executor.submit(process_batch, i))

    completed = 0

    for future in as_completed(futures):
        start_idx, cleaned_batch = future.result()

        for j, val in enumerate(cleaned_batch):
            if start_idx + j < len(results):
                results[start_idx + j] = val

        completed += len(cleaned_batch)
        print(f"Processed {completed} / {len(df)}")


results = [r if r is not None else "ERROR" for r in results]

df["Cleaned"] = results
df.to_excel("cleaned_output.xlsx", index=False)

print("Done.")
