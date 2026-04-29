### LLM Data Cleaning & Structuring Pipeline

---

## Use Cases

### 1. Unstructured → Semi-Structured 

Input:
- Messy product descriptions (free text, inconsistent format)

Output:
- Stock Code:
  - Typically found within brackets ()
  - However, bracket content may sometimes contain additional descriptions rather than valid codes
  - Code formats are inconsistent (alphanumeric, variable patterns), so extraction requires validation rather than simple parsing
- Short Description (≤ 40 chars)

Characteristics:
- Information may be missing or implicit
- Requires interpretation and summarisation

Approach:
- Use LLM to extract and standardise fields
- Apply strict output format control

---

### 2. Semi-Structured → Structured (LLM-first approach)

Input:
- Long and highly inconsistent descriptions containing mixed information:
  - Manufacturer (brand)
  - Sub-brand / model
  - Production year
  - Product details (e.g. bag type and components in the bag)

Output:
- Manufacturer
- Model / Branch
- Year
- Product Type

Characteristics:
- Information exists but is:
  - Unordered (no fixed position)
  - Inconsistent in format
  - Often merged together (e.g. year embedded within model names)
- Patterns are not reliable enough for rule-based extraction

👉 Approach:
- Use LLM directly for extraction and structuring
- Apply strict prompt constraints to enforce output format
- Avoid rule-based parsing due to:
  - Unstable patterns
  - High maintenance cost
  - Low accuracy across edge cases
