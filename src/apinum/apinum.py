# apinum.py

import os
import re
import json
# # import lasfile
# from os import path
dir_path = os.path.dirname(os.path.realpath(__file__))
valid_codes_path = os.path.join(dir_path, 'well_numbers.json')

codes_to_names_path = os.path.join(
    dir_path, "well_number_to_state_county.json"
)


def load_json(json_path):
    with open(json_path, 'r') as infile:
        return json.loads(infile.read())


codes_to_names = load_json(codes_to_names_path)


def well_number_from_string(string: str,
                            json_path: str = valid_codes_path):
    """Extracts well numbers from a string based on valid codes in a JSON file.

    Args:
        string (str): A string that may contain well numbers.
        json_path (str, optional): The path to the JSON file containing
        valid well codes. Defaults to "valid_codes.json".

    Returns:
        Optional[str]: The extracted well number as a string if one is
        found, otherwise None.
    """
    # Load the valid codes from the JSON file
    valid_codes = load_json(json_path)

    # Find all 10 to 14 digit strings in the input string
    matches = re.findall(r'(?=(\d{10,14}))', re.sub(r'[^\d]', '', string))

    well_numbers = []
    for match in matches:
        # If the string is 11 digits long, remove the last digit
        if len(match) == 11:
            match = match[:10]
        # If the string is 13 digits long, remove the last digits
        if len(match) == 13:
            match = match[:12]
        # If the string is 10, 12, or 14 digits long and the first two
        # digits are in the valid state codes
        if (
            len(match) in [10, 12, 14] and
            match[:2] in valid_codes.keys()
        ):
            # If the string is 14 digits long and the third through
            # fifth digits are in the valid codes
            if len(match) == 14 and match[2:5] in valid_codes[match[:2]]:
                well_numbers.append(match)
            # If the string is 12 digits long and the third through
            # fifth digits are in the valid codes
            elif len(match) == 12 and match[2:5] in valid_codes[match[:2]]:
                well_numbers.append(match + "00")
            # If the string is 10 digits long and the first two and
            # third through fifth digits are in the valid codes
            elif (
                len(match) == 10 and
                match[:2] in valid_codes.keys() and
                match[2:5] in valid_codes[match[:2]]
            ):
                well_numbers.append(match + "0000")

    # If any well numbers were found, return the most commonly occurring one
    if well_numbers:
        return max(well_numbers, key=well_numbers.count)
    else:
        return None


# def well_number_from_las(las_path: str, extract_from_path: bool = False):
#     """
#     Extracts the longest API or UWI well number from a LAS file.

#     Args:
#         las_path (str): The path to the LAS file.
#         extract_from_path (bool): If True, attempts to extract the well
#             number from the file path if no well number is found in the
#             LAS file. Defaults to False.

#     Returns:
#         str or None: The longest well number found in the LAS file, or
#             extracted from the file path if extract_from_path is True
#             and no well number is found in the LAS file. Returns None if
#             no well number is found.

#     """
#     # Read the LAS file and get the well section
#     well = lasfile.LASFile(file_path=las_path).well

#     # Extract well numbers from the well section
#     well_numbers = []
#     for key in well.keys():
#         if re.search(r"(?i)api|uwi", key):
#             well_numbers.append(
#                 well_number_from_string(
#                     well[key].value
#                 )
#             )

#     # Remove None values and return the longest well number
#     well_numbers = [x for x in well_numbers if x is not None]
#     if well_numbers:
#         longest_well_number = max(well_numbers, key=well_numbers.count)
#         return longest_well_number

#     # Attempt to extract well number from file path if requested
#     elif extract_from_path:
#         well_number = well_number_from_string(las_path)
#         if well_number:
#             return well_number

#     # If no well number is found, return None
#     return None

# Correct path for well_number_to_state_county.json
well_number_to_state_county_path = os.path.join(
    dir_path, "well_number_to_state_county.json"
)

# Load the JSON file using the defined function
well_number_to_state_county = load_json(well_number_to_state_county_path)


# Create a class for storing well numbers, parameters inlude, state code,
# county code, well number, wellbore code, and completion code.
class APINumber():
    """A class for storing API numbers. It accepts a string, a file_path
    to a LAS file, or a LASFile object as input. The class will attempt
    to extract the longest API number from the input.

    Args:
    -----
        input (str, LASFile): A string, a file_path to a LAS file, or a
            LASFile object.

    Attributes:
    -----------
        state_code (str): The two digit state code.
        county_code (str): The three digit county code.
        well_number (str): The five to seven digit well number.
        wellbore_code (str): The two digit wellbore code.
        completion_code (str): The two digit completion code.
        formatted_14_digit (str): The 14 digit API number formatted.
        formatted_12_digit (str): The 12 digit API number formatted.
        formatted_10_digit (str): The 10 digit API number formatted.
        unformatted_14_digit (str): The 14 digit API number unformatted.
        unformatted_12_digit (str): The 12 digit API number unformatted.
        unformatted_10_digit (str): The 10 digit API number unformatted.
        extracted_number (str): The longest API number extracted from
            the input.

    Raises:
    -------
        TypeError: If the input is not a string, a valid .las file path,
            or an LASFile object.
    """
    def __init__(self, input):
        # if isinstance(input, str):
        #     # If the input is a string attempt to extract an API number
        #     # from it
        #     str_extracted_number = well_number_from_string(input)
        #     # If no API number is found, test if the input is a valid
        #     # .las file path and attempt to extract the API number from
        #     # the file
        #     if path.isfile(input) and input.endswith(".las"):
        #         las_extracted_number = well_number_from_las(input)
        #         # If the first 10 digits of the API number extracted
        #         # from the file match the first 10 digits of the API
        #         # number extracted from the string, use the API number
        #         # extracted from the file
        #         if (
        #             str_extracted_number is not None and
        #             las_extracted_number is not None and
        #             str_extracted_number[:10] == las_extracted_number[:10]
        #         ):
        #             self.extracted_number = las_extracted_number
        # elif isinstance(input, lasfile.LASFile):
        #     self.extracted_number = well_number_from_las(input)
        # else:
        #     raise TypeError("Input must be a string, a valid .las file "
        #                     "path, or an LASFile object.")
        if isinstance(input, str):
            # If the input is a string attempt to extract an API number
            # from it
            self.extracted_number = well_number_from_string(input)
        else:
            raise TypeError("Input must be a string")
        # Generate the formatted and unformatted API numbers
        if self.extracted_number is not None:
            self.state_code = self.extracted_number[:2]
            
            self.county_code = self.extracted_number[2:5]
            if self.state_code in well_number_to_state_county.keys():
                self.state_name = well_number_to_state_county[self.state_code][0]
                if self.county_code in well_number_to_state_county[self.state_code][1].keys():
                    self.county_name = well_number_to_state_county[self.state_code][1][self.county_code]
            self.well_number = self.extracted_number[5:10]
            self.wellbore_code = self.extracted_number[10:12]
            self.completion_code = self.extracted_number[12:14]
            self.formatted_14_digit = (
                self.state_code + "-" +
                self.county_code + "-" +
                self.well_number + "-" +
                self.wellbore_code + "-" +
                self.completion_code
            )
            self.formatted_12_digit = (
                self.state_code + "-" +
                self.county_code + "-" +
                self.well_number + "-" +
                self.wellbore_code
            )
            self.formatted_10_digit = (
                self.state_code + "-" +
                self.county_code + "-" +
                self.well_number
            )
            self.unformatted_14_digit = (
                self.state_code +
                self.county_code +
                self.well_number +
                self.wellbore_code +
                self.completion_code
            )
            self.unformatted_12_digit = (
                self.state_code +
                self.county_code +
                self.well_number +
                self.wellbore_code
            )
            self.unformatted_10_digit = (
                self.state_code +
                self.county_code +
                self.well_number
            )
            return
        else:
            raise ValueError("No API number found in input string.")
