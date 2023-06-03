
import json
import os
import random
import src.apinum.apinum as apinum

# Load /src/apinum/well_numbers.json into a dictionary
parent_dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
known_numbers_path = os.path.join(
    parent_dir_path, "src", "apinum", "well_numbers.json"
)

with open(known_numbers_path, "r") as f:
    known_numbers = json.load(f)


# Define a function to create a list of strings to test the
# well_number_from_string function. With, test strings containing
# formatted and non formatted API numbers that are 10, 12, and 14 digits
# long, preceded and followed by many different characters including
# special characters. All api numbers should be generated from the known
# api numbers in the known_numbers dictionary above.
def test_well_number_from_string(iterations=1000, known_numbers=known_numbers):
    for i in range(iterations):
        # Get a random state and county code from known numbers
        state_code = random.choice(list(known_numbers.keys()))
        county_code = random.choice(known_numbers[state_code])
        # Get a random 5 digit well number from 00000 to 99999
        well_number = str(random.randint(0, 99999)).zfill(5)
        # Get a random 2 digit wellbore code from 00 to 99
        wellbore_code = str(random.randint(0, 99)).zfill(2)
        # Get a random 2 digit completion code from 00 to 99
        completion_code = str(random.randint(0, 99)).zfill(2)
        # Create one third of 10, 12, and 14 digit API numbers with half
        # each of the three groups being formatted API numbers, half
        # unformatted API numbers, with the formatted API numbers using
        # a delimiter from hyphen, underscore, period, and space
        delimiters = ['-', '_', '.', ' ']
        if i % 3 == 0:
            # Create a formatted 10 digit API number
            if i % 2 == 0:
                delimiter = random.choice(delimiters)
                api_number = (
                    f"{state_code}"
                    f"{delimiter}"
                    f"{county_code}"
                    f"{delimiter}"
                    f"{well_number}"
                )
            # Create an unformatted 10 digit API number
            else:
                api_number = (
                    f"{state_code}"
                    f"{county_code}"
                    f"{well_number}"
                )
        elif i % 3 == 1:
            # Create a formatted 12 digit API number
            if i % 2 == 0:
                delimiter = random.choice(delimiters)
                api_number = (
                    f"{state_code}"
                    f"{delimiter}"
                    f"{county_code}"
                    f"{delimiter}"
                    f"{well_number}"
                    f"{delimiter}"
                    f"{wellbore_code}"
                )
            # Create an unformatted 12 digit API number
            else:
                api_number = (
                    f"{state_code}"
                    f"{county_code}"
                    f"{well_number}"
                    f"{wellbore_code}"
                )
        else:
            # Create a formatted 14 digit API number
            if i % 2 == 0:
                delimiter = random.choice(delimiters)
                api_number = (
                    f"{state_code}"
                    f"{delimiter}"
                    f"{county_code}"
                    f"{delimiter}"
                    f"{well_number}"
                    f"{delimiter}"
                    f"{wellbore_code}"
                    f"{delimiter}"
                    f"{completion_code}"
                )
            # Create an unformatted 14 digit API number
            else:
                api_number = (
                    f"{state_code}"
                    f"{county_code}"
                    f"{well_number}"
                    f"{wellbore_code}"
                    f"{completion_code}"
                )
        # Generate two random strings about 50 characters long to
        # precede and follow the API number
        pre_string = "".join(random.choices(
            list(
                "abcdefghijklmnopqrstuvwxyz"
                "0123456789"
                "~!@#$%^&*()_+`-=[]{}|;':\",./<>?"
            ),
            k=50))
        post_string = "".join(random.choices(
            list(
                "abcdefghijklmnopqrstuvwxyz"
                "0123456789"
                "~!@#$%^&*()_+`-=[]{}|;':\",./<>?"
            ),
            k=50))
        # Create a test string with the API number in the middle
        test_string = f"{pre_string}{api_number}{post_string}"

        assert apinum.APINumber(test_string)
