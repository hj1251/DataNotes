import pandas as pd
from openai import OpenAI
import json
import time

client = OpenAI(api_key="AAAAA")

df = pd.read_excel("Desc.xlsx") 


def check_description(desc):
    prompt = f"""
You are a strict data quality checker.

Check if the product description is valid.

Rules:
- Must contain manufacturer (brand like Tesla, BMW, Audi)
- Must contain product type (Mat, Rubber Mat, Carpet Mat, Pack, etc.)
- Should be concise (not overly long, no unnecessary extra words)

Description:
{desc}

Return JSON ONLY:
{{
  "is_valid": true/false,
  "issues": ["list of problems"],
  "suggestion": "short corrected version OR null"
}}
"""

    for attempt in range(3):
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
                temperature=0
            )

            raw = response.output_text.strip()

         
            start = raw.find("{")
            end = raw.rfind("}") + 1
            raw_json = raw[start:end]

            result = json.loads(raw_json)

            return {
                "is_valid": result.get("is_valid", False),
                "issues": result.get("issues", ["UNKNOWN_ERROR"]),
                "suggestion": result.get("suggestion", None)
            }

        except Exception as e:
            time.sleep(2 * (attempt + 1))

    return {
        "is_valid": False,
        "issues": ["MODEL_ERROR"],
        "suggestion": None
    }


print("Starting validation...")

results = []

for i, row in df.iterrows():
    desc = str(row.get("Desc", ""))

    result = check_description(desc)
    results.append(result)

    if i % 10 == 0:
        print(f"Processed {i}/{len(df)}")


df["is_valid"] = [r["is_valid"] for r in results]
df["issues"] = [", ".join(r["issues"]) for r in results]
df["suggestion"] = [r["suggestion"] for r in results]


df.to_excel("validated_output.xlsx", index=False)


df[df["is_valid"] == False].to_excel("needs_review.xlsx", index=False)

print("Done.")
