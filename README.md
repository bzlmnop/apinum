# APINum Library

## Overview
APINum is a Python library designed for extracting well numbers, such as API (American Petroleum Institute) numbers, now known as US Well Numbers, from strings. It validates well numbers against predefined codes and supports different digit formats for API numbers/US Well Numbers.

## Installation
Install APINum directly using pip:

    pip install apinum

## Features
- Extract well numbers from strings.
- Validate well numbers against a list of predefined codes.
- Support for 10, 12, and 14-digit API number formats.
- Provides formatted and unformatted well number outputs.

## Usage
To use APINum, import and initialize the `APINumber` class with a string containing a well number. The class parses and extracts the API number from the string.

```python
from apinum import APINumber

# Example string containing an API number
input_string = "Your string containing API number"
api_number = APINumber(input_string)

# Access extracted API number and other details
print(api_number.extracted_number)
print(api_number.formatted_14_digit)
```

### Available Attributes
`APINumber` provides the following attributes to access the extracted number details:
- `extracted_number`: The raw extracted API number.
- `formatted_14_digit`: Formatted 14-digit API number.
- `formatted_12_digit`: Formatted 12-digit API number.
- `formatted_10_digit`: Formatted 10-digit API number.
- `unformatted_14_digit`: Unformatted 14-digit API number.
- `unformatted_12_digit`: Unformatted 12-digit API number.
- `unformatted_10_digit`: Unformatted 10-digit API number.

## Error Handling
`APINumber` raises exceptions for invalid inputs or if no API number is found:
- `TypeError`: Input is not a valid string.
- `ValueError`: No API number found in the input string.

## Configuration
The library uses JSON files for valid API codes and mappings. Ensure these files are correctly set up in your working directory.

## Contribution
Contributions are welcome. Follow standard practices for contributing to Python packages, such as forking the repository, making changes, and submitting a pull request.

## License
Include the license here to inform users of their rights when using and modifying the APINum library.
