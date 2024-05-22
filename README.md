# GDPR Obfuscator

The purpose of this project is to create a general-purpose tool to process data being ingested to AWS and intercept personally identifiable information (PII). All information stored by the company data projects should be for bulk data analysis only. Consequently, there is a requirement under GDPR to ensure that all data containing information that can be used to identify an individual should be anonymised.

## High-level desired outcome

- This project is an obfuscation tool that can be integrated as a library module into a Python codebase.
- The obfuscator will be supplied with the S3 location of a file containing sensitive information, and the names of the fields to obfuscated. It will create a new file or byte stream object containing an exact copy of the input file but with the sensitive data replaced with obfuscated strings.
- The calling procedure will handle saving the output to its destination.
- The obfuscator will be designed to be deployed within the AWS account.

### Assumptions and Prerequisites

1. Data is stored in CSV, JSON, or parquet format in S3.
2. Fields containing GDPR-sensitive data are known and will be supplied in advance.
3. Data records will be supplied with a primary key.

### Minimum viable product

The obfuscator will be able to process CSV data. It will be invoked upon receiving a JSON string containing:

- the S3 location of the required CSV file for obfuscation
- the names of the fields that are required to be obfuscated

This JSON string is expected in the format:

```json
{
	"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
	"pii_fields": ["name", "email_address"]
}
```

The input CSV is expected in the format:

```csv
student_id,name,course,cohort,graduation_date,email_address
...
1234,'John Smith','Software','2024-03-31','j.smith@email.com'
...
```

The output will be a bytestream representation of a file like this:

```csv
student_id,name,course,cohort,graduation_date,email_address
...
1234,'***','Software','2024-03-31','***'
...
```

The output format will provide content compatible with the boto3 [S3 Put Object](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object.html).

Invocation is through AWS EventBridge. The actual invocation mechanism is outside the scope of this project.

### Possible extensions

The MVP could be extended to allow for other file formats, primarily JSON and Parquet. The output file formats should be the same as the input formats.

## Non-functional requirements

- The tool will be written in Python, be fully documented, be unit tested, PEP-8 compliant, and tested for security vulnerabilities.
- No credentials are to be recorded in the code.
- The complete size of the module should not exceed the memory limits for Python Lambda dependencies

- The tool should be able to handle files of up to 1MB with a runtime of less than 1 minute
