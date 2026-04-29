"""
This script processes large volumes of messy product descriptions and extracts:
- Product code, where available
- Short product description

Logic:
- If the description contains content inside brackets (), extract it as the product code.
- If the whole description looks like a standalone code, use it as the product code.
- Generate a clear, human-readable short description with a maximum length of 40 characters.

Output:
The original dataset with two additional fields:
- Code
- Short_Desc
"""

import pandas as pd
from openai import OpenAI
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

client = OpenAI(api_key="ABC")

logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

df = pd.read_excel("data.xlsx")

# Number of rows processed per API call 
BATCH_SIZE = 10
# Number of parallel threads (controls how many API requests run concurrently)
MAX_WORKERS = 5

def process_batch(texts, start_index):
    batch_input = "\n".join([str(t) for t in texts])

    prompt = f"""
For each line, extract TWO things:

1. Code:
- If there is content inside brackets (), extract it
- If no brackets:
    - If the whole line looks like a code (letters + numbers, no spaces, e.g. 19040538PF), use the whole line as Code
- Otherwise return empty

2. Short Description:
- If the line is just a code, return the same code
- Otherwise summarise what the product is (e.g. Custom Mat, Rubber Mat, Carpet Mat)
- Max 40 characters
- Clear and human readable

Return format (STRICT):
Code | Short Description

One line per input, same order.

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
            lines = [line.strip() for line in raw.split("\n") if line.strip()]

            results = []

            for line in lines:
                if "|" in line:
                    code, desc = line.split("|", 1)
                    results.append((code.strip(), desc.strip()[:40]))
                else:
                    results.append(("", line.strip()[:40]))
            # Validate output length to ensure alignment with input to prevents row misalignment where results shift and map to wrong records. 
            # If mismatch occurs, trigger retry instead of silently accepting incorrect mapping  
            if len(results) != len(texts):
                raise ValueError("Length mismatch")

            return results

        except Exception as e:
            logging.error(f"Batch {start_index} Attempt {attempt} Error: {str(e)}")
            time.sleep(2 * (attempt + 1))
    # If all retry attempts fail, return placeholder values
    return [("ERROR", "ERROR")] * len(texts)


codes = [None] * len(df)
descs = [None] * len(df)


def run_batch(i):
    batch = df["Desc"].iloc[i:i+BATCH_SIZE].fillna("").tolist()
    result = process_batch(batch, i)
    return i, result


print("Starting...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = []

    for i in range(0, len(df), BATCH_SIZE):
        futures.append(executor.submit(run_batch, i))

    completed = 0
  
    # Collect results as each task completes (order is NOT guaranteed)
    for future in as_completed(futures):
        start_idx, batch_result = future.result()
      
        # Map batch results back to the correct global positions
        for j, (code, desc) in enumerate(batch_result):
            idx = start_idx + j
            if idx < len(df):
                codes[idx] = code
                descs[idx] = desc

        completed += len(batch_result)
        print(f"Processed {completed} / {len(df)}")
      

df["Code"] = [c if c else "" for c in codes]
df["Short_Desc"] = [d if d else "" for d in descs]

df.to_excel("final_output.xlsx", index=False)

print("Done.")
