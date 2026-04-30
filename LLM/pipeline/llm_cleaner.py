from openai import OpenAI
import json
import os

client = OpenAI(api_key="123")


def clean_text(text):
    prompt = f"""
    Extract ONLY the brand and product type.

    Rules:
    - Keep ONLY: Brand + Product type
    - Remove numbers, colors, extra details
    - Do NOT guess
    - If unclear, return original
    - Keep output short (2-4 words max)

    Return ONLY the result text.

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        timeout=20   
    )

    return response.choices[0].message.content.strip()


def clean_batch(text_list):
    prompt = f"""
    Extract ONLY the brand and product type.

    Rules:
    - Keep ONLY: Brand + Product type
    - Remove numbers, colors, extra details
    - Do NOT guess
    - If unclear, return original

    VERY IMPORTANT:
    - Return ONLY a JSON array
    - No explanation
    - No markdown
    - No ```json block

    Format:
    ["result1","result2","result3"]

    Input:
    {text_list}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        timeout=20
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        cleaned = json.loads(content)
    except Exception as e:
        raise ValueError(f"Invalid JSON from LLM:\n{content}")

    return cleaned
