# GDPR Obfuscator

- [Installation](#installation)
- [Basic usage](#basic-usage)
- [Advanced usage](#advanced-usage)
- [Writing obfuscated data](#writing-obfuscated-data)

A general-purpose tool to process data being ingested to AWS and intercept and obfuscate Personally Identifiable Information (PII). It returns a string of data in the same format, ready to be written to a file.

Currently suported file types are `CSV`, `JSON`, `Parquet` and `XML`.

## Installation

To install `obfuscator`, run:

```bash
pip install git+https://github.com/CJohnston079/gdpr-obfuscator.git
```

## Basic usage

Use `obfuscator.Obfuscator()` to create and initialize an Obfuscator, which will obfuscate any fields identified as PII in the `event` argument.

```python
from obfuscator import Obfuscator

obfuscator = Obfuscator()

event = {
    "file_to_obfuscate": "s3://gdpr-obfuscator-24-06-20/sample_csv.csv",
    "pii_fields": ["name", "contact"],
}

data = obfuscator.obfuscate(event)
```

This will obfuscate the `name` and `contact` fields in the targeted data, as shown below:

| id  | name          | contact                   | cohort     | course               |
| --- | ------------- | ------------------------- | ---------- | -------------------- |
| 1   | Claire Burton | c.burton639@hotmail.co.uk | 2024-05-31 | software development |
| 2   | June Mistry   | j.mistry354@outlook.com   | 2024-03-31 | java development     |
| 3   | Hilary Welch  | hilary244@hotmail.co.uk   | 2024-01-26 | java development     |

| id  | name   | contact | cohort     | course               |
| --- | ------ | ------- | ---------- | -------------------- |
| 1   | \*\*\* | \*\*\*  | 2024-05-31 | software development |
| 2   | \*\*\* | \*\*\*  | 2024-03-31 | java development     |
| 3   | \*\*\* | \*\*\*  | 2024-01-26 | java development     |

For more information on what is considered Personally Identifiable Information, visit https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/what-is-personal-information-a-guide/

## Advanced usage

By default, `obfuscator` tokenises targeted PII fields. However, there are othre obfuscation methods available.

### Tokenisation

This is the default setting for `Obfuscator`. The default token is a triple asterisk (`***`), however, this can be changed by initializing `Obfuscator` with a custom token.

To use a custom token, you can pass the `options` parameter with your desired token value. For example, to use the tilde (`~`) as the token:

```python
Obfuscator(options={"token": "~"})
```

This would return:

| id  | name | contact | cohort     | course               |
| --- | ---- | ------- | ---------- | -------------------- |
| 1   | ~    | ~       | 2024-05-31 | software development |
| 2   | ~    | ~       | 2024-03-31 | java development     |
| 3   | ~    | ~       | 2024-01-26 | java development     |

### Masking

Masking is the process of obscuring a field by replacing all characters with a single token. It is commonly used for sensitive information such as credit card numbers and passwords.

To use the `mask` method, initialise `Obfuscator` with `"mask"` as the `method` argument:

```python
obfuscator = Obfuscator(method="mask")
```

This will obfuscate the data as show below:

| id  | name          | contact                   | cohort     | course               |
| --- | ------------- | ------------------------- | ---------- | -------------------- |
| 1   | Claire Burton | c.burton639@hotmail.co.uk | 2024-05-31 | software development |
| 2   | June Mistry   | j.mistry354@outlook.com   | 2024-03-31 | java development     |
| 3   | Hilary Welch  | hilary244@hotmail.co.uk   | 2024-01-26 | java development     |

| id  | name                       | contact                                            | cohort     | course               |
| --- | -------------------------- | -------------------------------------------------- | ---------- | -------------------- |
| 1   | \*\*\*\*\*\*\*\*\*\*\*\*\* | \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* | 2024-05-31 | software development |
| 2   | \*\*\*\*\*\*\*\*\*\*\*     | \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*     | 2024-03-31 | java development     |
| 3   | \*\*\*\*\*\*\*\*\*\*\*\*   | \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*     | 2024-01-26 | java development     |

Custom tokens may used in conjunction with the `mask` method.

```python
obfuscator = Obfuscator(method="mask", options={"token": "~"})
```

| id  | name          | contact                   | cohort     | course               |
| --- | ------------- | ------------------------- | ---------- | -------------------- |
| 1   | ~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~~~~ | 2024-05-31 | software development |
| 2   | ~~~~~~~~~~~   | ~~~~~~~~~~~~~~~~~~~~~~~   | 2024-03-31 | java development     |
| 3   | ~~~~~~~~~~~~  | ~~~~~~~~~~~~~~~~~~~~~~~   | 2024-01-26 | java development     |

### Anonymisation

Anonymisation, or pseudonymisation, replaces PII fields with randomly generated data that is no longer attributable to the specific data subject.

To use the `anonymise` method, initialise `Obfuscator` with `"anonymise"` as the `method` argument:

```python
obfuscator = Obfuscator(method="anonymise")
```

This will obfuscate the data as shown below:

| id  | name          | contact                   | cohort     | course               |
| --- | ------------- | ------------------------- | ---------- | -------------------- |
| 1   | Claire Burton | c.burton639@hotmail.co.uk | 2024-05-31 | software development |
| 2   | June Mistry   | j.mistry354@outlook.com   | 2024-03-31 | java development     |
| 3   | Hilary Welch  | hilary244@hotmail.co.uk   | 2024-01-26 | java development     |

| id  | name            | contact                | cohort     | course               |
| --- | --------------- | ---------------------- | ---------- | -------------------- |
| 1   | Ian McCarthy    | ian460@hotmail.com     | 2024-05-31 | software development |
| 2   | Kate Stephenson | kate259@outlook.com    | 2024-03-31 | java development     |
| 3   | Leigh Jones     | l.jones459@yahoo.co.uk | 2024-01-26 | java development     |

The second table might look similar, however, all the PII fields have been replaced with randomly generated data, obscuring the original data subjects.

When anonymising data, `Obfuscator` will attempt to generate meaningful replacements for each PII field. If it is unable to generate a meaningful replacement, `Obfuscator` will tokenise the field instead. Not that a custom token can still be assigned when `method` is set to `"anonymise"`, as shown below:

```python
obfuscator = Obfuscator(method="anonymise", options={"token": "~"})
```

For further information about obfuscation methods and how to implement them, see: https://www.gov.uk/government/publications/joined-up-data-in-government-the-future-of-data-linking-methods/linking-with-anonymised-data-how-not-to-make-a-hash-of-it

## Writing obfuscated data

`Obfuscator` returns a string ready to be written to a file of the same format as the input file. Instructions on how to write each file type with the obfuscated data are below.

### CSV

```python
import csv

csv_data = obfuscator.obfuscate(csv_data_event)

with open("obfuscated_csv_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(csv.reader(csv_data.splitlines()))
```

### JSON

```python
import json

json_data = obfuscator.obfuscate(json_data_event)

with open("obfuscatedJsonData.json", "w") as file:
    json.dump(json.loads(json_data), file, indent=2)

```

### Parquet

```python
import json

parquet_data = obfuscator.obfuscate(parquet_data_event)

with open("obfuscated_pq_data.parquet", "wb") as file:
    file.write(parquet_data)
```

### XML

```python
import xml.etree.ElementTree as ET

xml_data = obfuscator.obfuscate(xml_data_event)

root = ET.fromstring(xml_data)
tree = ET.ElementTree(root)

tree.write("obfuscated-xml.xml", encoding="utf-8")
```
