# Python Pandas

Start with the following line of code:

```python
import pandas as pd
```

## Creating Data

There are two core objects in pandas: the **DataFrame** and the **Series**.

### DataFrame

A **DataFrame** is a table.  
It contains an array of individual entries, each of which has a certain **value**.  
Each entry corresponds to a **row (record)** and a **column**.

**Example:**

```python
import pandas as pd

data = {
    'Product': ['A', 'B', 'C'],
    'Sales': 
}

df = pd.DataFrame(data)
df
```

Output:

| Product | Sales |
|----------|-------|
| A        | 30    |
| B        | 40    |
| C        | 50    |

---

### Series

A Series is a one-dimensional labeled array in pandas.  
It is similar to a list because it stores a sequence of values, but unlike a list, each value has an index label.  
It is also a bit like a dictionary because values are accessed using labels, but unlike a dictionary, a Series keeps the data in a fixed order and supports vectorized operations.

### Compare: List, Dictionary, and Series

- **List**: an ordered collection of values.
- **Dictionary**: a collection of key-value pairs.
- **Series**: an ordered collection of values with labels (index).


## Example

```python
import pandas as pd

# List
scores_list = [30,35,40]
print(scores_list)

# Dictionary
scores_dict = {
    '2015 Sales': 30,
    '2016 Sales': 35,
    '2017 Sales': 40
}
print(scores_dict)

# Series
scores_series = pd.Series(
    ,
    index=['2015 Sales', '2016 Sales', '2017 Sales'],
    name='Product A'
)
print(scores_series)
```

## Output

```text
[15,30,35]
```

```text
{'2015 Sales': 30, '2016 Sales': 35, '2017 Sales': 40}
```

```text
2015 Sales    30
2016 Sales    35
2017 Sales    40
Name: Product A, dtype: int64
```

### Key Idea
A Series is **not** a list and **not** a dictionary.  
It is a pandas object that combines the ordered nature of a list with the labeled access style of a dictionary.


## Reading Data Files

Pandas file reading functions:
- CSV files      -> pd.read_csv()
- Excel files    -> pd.read_excel()
- JSON files     -> pd.read_json()
- HTML tables    -> pd.read_html()
- SQL data       -> pd.read_sql()
- Parquet files  -> pd.read_parquet()
- Pickle files   -> pd.read_pickle()
- HDF5 files     -> pd.read_hdf()

```python
data = pd.read_csv("../data.csv")
```
