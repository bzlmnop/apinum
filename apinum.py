# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:06:10 2021

@author: bzaitz

'apinum' is a program built for manipulating Well/API Numbers
    - apinum needs an dictionary of known State and County codes
        - ex. {'30':['015','025']}
        - if properly configured this will be read from file:
            "api_state_county_num.json"
    - apinum can extract 10-14 digit api numbers from a string or an las file
    - apinum can generate APINumber objects that make it simpler to manipulate
      a known API number
 
"""
#import pandas as pd
#import math
import json
from os import getcwd


def generate_api_dict(json_path):
    with open(json_path,'r') as infile:
        return json.loads(infile.read())


cwd = getcwd()

json_path = cwd + "\\inputs\\api_state_county_num.json"

json_path = "C:\\PythonScripts\\geolopy\\inputs\\api_state_county_num.json"

api_dict = generate_api_dict(json_path)


def count_substrings(string,substring):
    string_size = len(string)
    substring_size = len(substring)
    count = 0
    for i in range(0,string_size-substring_size+1):
        if string[i:i+substring_size] == substring:
            count+=1
    return count


def contains_only_digits(input_str):
    count = 0
    for character in input_str:
        if character.isdigit():
            count = count + 1
            if count == len(input_str):
                return True
    return False


def get_string_after_instance_of_substring(input_str,split_value,instance=0):
    input_list = input_str.split(split_value)
    input_list = input_list[instance+1:]
    #print(input_list)
    new_str = ''
    count = 0
    for value in input_list:
        count = count + 1
        #print(count)
        if count == 1:
            new_str = new_str + value
            #print(new_str)
        elif count < len(input_list):
            if input_str.startswith(split_value):
                #print('startswith')
                new_str = new_str + value
                #print(new_str)
            else:
                #print('not startswith')
                new_str = new_str + split_value + value
                #print(new_str)
        elif count == len(input_list):
            #print('last value')
            if input_str.endswith(split_value):
                new_str = new_str + split_value
            else:
                new_str = new_str + split_value + value
            #print(new_str)
    return new_str

def chunk_string(
        input_str,
        chunk_size=2,
        return_position=True
        ):
    for count,character in enumerate(input_str):
        start_pos = count
        stop_pos = start_pos + chunk_size
        if stop_pos <= len(input_str)-1:
            if return_position:
                yield input_str[start_pos:stop_pos],start_pos,stop_pos
            else:
                yield input_str[start_pos:stop_pos]

def strip_api_delimeters(
        input_str,
        delimeters=[' ','_','-']
        ):
    return input_str.strip(' ').strip('-').strip('_')

def api_from_string(
        input_str,
        api_dict=api_dict,
        strip_delimeters=True,
        return_length=14,
        state_codes=[]):
    # Check if there were any state codes input to cull the api dictionary by.
    if state_codes != []:
        new_api_dict = {}
        for state_code in state_codes:
            state_code = str(state_code)
            if state_code in api_dict.keys():
                new_api_dict[state_code] = api_dict[state_code]
        api_dict = new_api_dict
    # Create a list to store all api numbers found in the input string in.
    api_number_list = []
    # Loop through the input string in state code sized chunks, 2 characters.
    for state_chunk,start_pos,stop_pos in chunk_string(input_str,chunk_size=2):
        # Test if chunk is a state code.
        if state_chunk in api_dict.keys():
            state_code = state_chunk
            # Get the remaining string after the found state code.
            str_after_state_code = input_str[stop_pos:]
            if strip_delimeters:
                str_after_state_code = strip_api_delimeters(str_after_state_code)
            # Get the next three characters, a county code sized chunk.
            county_chunk = str_after_state_code[:3]
            # Test if the chunk is a county code for a county in the state.
            # corresponding to the found state code.
            if county_chunk in api_dict[state_code]:
                county_code = county_chunk
                # Get the string following the county code.
                str_after_county_code = str_after_state_code[3:]
                if strip_delimeters:
                    str_after_county_code = strip_api_delimeters(str_after_county_code)
                # Test if the remainder of the string after the found county 
                # code is long enough to contain a 5 digit well code
                if len(str_after_county_code) >= 5:
                    # Get the next five characters, a well code sized chunk.
                    well_chunk = str_after_county_code[:5]
                    # Test if the well chunk contains only digits.
                    if contains_only_digits(well_chunk):
                        well_code = well_chunk
                        # Generate the 10 digit api number.
                        api_10_digit = state_code + county_code + well_code
                        # Get the remaining string following the well code.
                        str_after_well_code = str_after_county_code[5:]
                        if strip_delimeters:
                            str_after_well_code = strip_api_delimeters(str_after_well_code)
                        # Test if the length of the remaining string after the well code
                        # is long enough to contain a 2 digit suffix code.
                        if len(str_after_well_code) >= 2:
                            # Test if the length of the remaining string is equal to the
                            # length of a wellbore code.
                            if len(str_after_well_code) == 2:
                                # If it is set the wellbore chunk equal to the remaining string.
                                wellbore_chunk = str_after_well_code
                            else:
                                # Get the next two characters, a wellbore code sized chunk.
                                wellbore_chunk = str_after_well_code[:2]
                            # Test if the wellbore chunk contains only digits.
                            if contains_only_digits(wellbore_chunk):
                                wellbore_code = wellbore_chunk
                                # Generate the 12 digit api number.
                                api_12_digit = api_10_digit + wellbore_code
                                # Get the remaining string following the wellbore code.
                                str_after_wellbore_code = str_after_well_code[2:]
                                if strip_delimeters:
                                    str_after_wellbore_code = strip_api_delimeters(str_after_wellbore_code)
                                # Test if the length of the remaining string after the 
                                # wellbore code is long enough to contain a 2 digit completion code.
                                if len(str_after_wellbore_code) >= 2:
                                    # Test if the remaining string is the same length as a completion code.
                                    if len(str_after_wellbore_code) == 2:
                                        # If it is set the completion chunk equal to the remaingin string.
                                        completion_chunk = str_after_wellbore_code
                                    else:
                                        # Get the next two characters, a completion code sized chunk.
                                        completion_chunk = str_after_wellbore_code[:2]
                                    # Test if the completion chunk contains only digits.
                                    if contains_only_digits(completion_chunk):
                                        completion_code = completion_chunk
                                        # Generate the 14 digit api number
                                        api_14_digit = api_12_digit + completion_code
                                        # Add the found 14 digit api number to the list
                                        # of found api numbers.
                                        api_number_list.append(api_14_digit)
                                    else:
                                        # If the suffix chunk does not contain only digits
                                        # append the found 12 digit api number to the list
                                        # of found api numbers.
                                        api_number_list.append(api_12_digit)
                                else:
                                    # If the length of the string after the found wellbore
                                    # code is not long enough to contain a completion code
                                    # append the found 12 digit api number to the list
                                    # of found api numbers.
                                    api_number_list.append(api_12_digit)
                            else:
                                # If the wellbore chunk does not contain only digits
                                # append the found 10 digit api number to the list of
                                # found api numbers.
                                api_number_list.append(api_10_digit)
                        else:
                            # If the length of the string after the found well code
                            # is not long enough to contain a wellbore code then
                            # append the found 10 digit api number to the list of
                            # found api numbers.
                            api_number_list.append(api_10_digit)
    # Test if the list of APIs extracted from the input string is not empty
    if len(api_number_list) > 0:
        #print('not empty')
        # Test if there is only one api in the list
        if len(api_number_list) == 1:
            #print('only on api found')
            # If there is only one, normalize it to the desired length and 
            # return it
            return normalize_unformatted_api_length(api_number_list[0],return_length=return_length)
        # Test if there is more than one api in the list
        elif len(api_number_list) > 1:
            #print('more than one api found')
            # Test if list of extracted API numbers is homogenous
            if len(set(api_number_list)) == 1:
                #print('list is homo')
                # If the list is homogenous, normalize the api to the
                # desired length and return it
                return normalize_unformatted_api_length(api_number_list[0],return_length=return_length)
            # If the list of extracted APIs is heterogenous
            else:
                # Test if the 14 digit APIs in the list are the same
                if len(set([api_number for api_number in api_number_list if len(api_number) == 14])) == 1:
                    #print('all 14 dig same')
                    # Return 14 digit api, normalized to desired length
                    return normalize_unformatted_api_length([api_number for api_number in api_number_list if len(api_number) == 14][0],return_length=return_length)
                # Test if the 12 digit APIs in the list are the same
                elif len(set([api_number for api_number in api_number_list if len(api_number) == 12])) == 1:
                    # Return 12 digit api, normalized to desired length
                    return normalize_unformatted_api_length([api_number for api_number in api_number_list if len(api_number) == 12][0],return_length=return_length)
                # Test if the first 10 digits are shared between all 
                # API numbers in list (i.e. State, County, and Well Codes are same)
                elif len(set([api_number[0:10] for api_number in api_number_list])) == 1:
                    # Return 10 digit api, normalized to desired length
                    return normalize_unformatted_api_length(api_number_list[0][0:10],return_length=return_length)
    else:
        return None
                        

def api_from_string_old(input_str,
                    api_dict=api_dict,
                    strip_delimiters=True,
                    strip_whitespaces=True,
                    return_length=14,
                    state_codes=[]):
    # Check if there were any state codes input to cull the api dictionary by.
    if state_codes != []:
        new_api_dict = {}
        for state_code in state_codes:
            state_code = str(state_code)
            if state_code in api_dict.keys():
                new_api_dict[state_code] = api_dict[state_code]
        api_dict = new_api_dict
        #print(api_dict)
    # Loop through the dictionary of API state and county codes
    for state_code,county_code_list in api_dict.items():
        # Create an empty list to store any APIs found in the string
        api_number_list = []
        # Test for any instances of the current stat code in the input string
        if str(state_code) in input_str:
            #print('found state code')
            #print(state_code)
            # Get the number of instances of the current state code in the input string
            state_code_instances = count_substrings(input_str,str(state_code))
            #print('state code instances')
            #print(state_code_instances)
            attempt_count = 0
            while attempt_count != state_code_instances:
                attempt_count = attempt_count + 1
                #print('attempt count')
                #print(attempt_count)
                #print('split string')
                #print(input_str.split(str(state_code)))
                if len(input_str.split(str(state_code))) >= attempt_count + 1:
                    # Get the remaining string after the current instance of 
                    # the current state code
                    string_after_state_code = get_string_after_instance_of_substring(
                            input_str,
                            str(state_code),
                            instance=attempt_count-1)
                    if string_after_state_code != None:
                        #print('string after state code is not None')
                        if len(string_after_state_code) >= 8:
                            #print('string after state code longer than 8 char')
                            #print('string after state code')
                            #print(string_after_state_code)
                            if strip_delimiters:
                                string_after_state_code = string_after_state_code.strip('-').strip('_')
                            if strip_whitespaces:
                                string_after_state_code = string_after_state_code.strip(' ')
                            #print('string after state code (delimiters removed)')
                            #print(string_after_state_code)
                            # Start looping through the known county codes for the current state code
                    for county_code in county_code_list:
                        #print(county_code)
                        # Test if the remaining string after the state code starts with the current county code
                        if string_after_state_code.startswith(str(county_code)):
                            #print('string after state code startswith county code')
                            # Get the remaining string after the current county code
                            string_after_county_code = string_after_state_code.lstrip(str(county_code))
                            #print('string after county code')
                            #print(string_after_county_code)
                            if strip_delimiters:
                                string_after_county_code = string_after_county_code.strip('-').strip('_')
                            if strip_whitespaces:
                                string_after_county_code = string_after_county_code.strip(' ')
                            #print('string after county code (delimiters removed)')
                            #print(string_after_county_code)
                            # Test that the remaining string is long enough to contain a well code
                            if len(string_after_county_code) >= 5:
                                #print('string after county code longer than 5 char')
                                # Get the next 5 characters after the current county code
                                api_5digit_well_number = string_after_county_code[0:5]
                                #print(api_5digit_well_number)
                            else:
                                continue
                            # Test if the extracted well code contains only digits
                            if contains_only_digits(api_5digit_well_number):
                                #print('api well code contains only digits')
                                # Build the extraced 10 digit api number
                                api_10digit = state_code + county_code + api_5digit_well_number
                                #print('10 digit api')
                                #print(api_10digit)
                                if string_after_county_code.startswith(api_5digit_well_number):
                                    string_after_well_code = string_after_county_code[len(api_5digit_well_number):]
                                #string_after_well_code = string_after_county_code.lstrip(str(api_5digit_well_number))
                                #print('string after well code')
                                #print(string_after_well_code)
                                if string_after_well_code != None:
                                    #print('string after well code not none')
                                    if len(string_after_well_code) >= 2:
                                        #print('string after well code longer than 2 char')
                                        if strip_delimiters:
                                            string_after_well_code = string_after_well_code.strip('-').strip('_')
                                        if strip_whitespaces:
                                            string_after_well_code = string_after_well_code.strip(' ')
                                        #print('string after well code (delimiters removed)')
                                        #print(string_after_well_code)
                                        # Test if the remaining string is long enough to contain a suffix/completion code
                                        if len(string_after_well_code) >= 4:
                                            #print('4 digit suffix')
                                            # Get the next 4 characters after the well code
                                            api_suffix = string_after_well_code[0:4]
                                            #print(api_suffix)
                                            # Test if the extracted suffix/completion code contains only digits
                                            if contains_only_digits(api_suffix):
                                                #print('suffix contains only digits')
                                                # Add the 14 digit API to the list of APIs found in the input string
                                                api_14digit = api_10digit + api_suffix
                                                #print('14 digit api')
                                                #print(api_14digit)
                                                api_number_list.append(api_14digit)
                                            else:
                                                api_number_list.append(api_10digit)
                                        elif len(string_after_well_code) <= 2:
                                            #print('2 digit suffix')
                                            # Get the next 2 characters after the well code
                                            api_suffix = string_after_well_code[0:2]
                                            #print(api_suffix)
                                            # Test if the extracted suffix/completion code contains only digits
                                            if contains_only_digits(api_suffix):
                                                #print('suffix contains only digits')
                                                # Add the 12 digit API to the list of APIs found in the input string
                                                api_12digit = api_10digit + api_suffix
                                                api_number_list.append(api_12digit)
                                            else:
                                                # Otherwise add the 10 digit API to the list of APIs found in the input string
                                                api_number_list.append(api_10digit)
                                        else:
                                            # If the string after the well code is not long enough add the 10 digit to the list
                                            api_number_list.append(api_10digit)
                                    else:
                                        # If string after well code length is less than 2
                                        api_number_list.append(api_10digit)
                                else:
                                    # If string after well code is None
                                    api_number_list.append(api_10digit)
                        else:
                            #print('string after state code shorter than 8 char')
                            continue
                    else:
                        #print('string after state code is None')
                        continue
                else:
                    #print('too many attempts')
                    continue
        # Test if the list of APIs extracted from the input string is not empty
        if len(api_number_list) > 0:
            #print('api list not empty')
            #print(api_number_list)
            # Test if there is only one api in the list
            if len(api_number_list) == 1:
                #print('only one api found')
                # If there is only one, normalize it to the desired length and 
                # return it
                return normalize_unformatted_api_length(api_number_list[0],return_length=return_length)
            # Test if there is more than one api in the list
            elif len(api_number_list) > 1:
                # Test if list of extracted API numbers is homogenous
                if len(set(api_number_list)) == 1:
                    # If the list is homogenous, normalize the api to the
                    # desired length and return it
                    return normalize_unformatted_api_length(api_number_list[0],return_length=return_length)
                # If the list of extracted APIs is heterogenous
                else:
                    # Test if all API numbers in the list are of equal length
                    if len(set([len(api_number) for api_number in api_number_list])) == 1:
                        # Test if the first 10 digits are shared between all 
                        # API numbers in list (i.e. State, County, and Well 
                        # Codes are same)
                        if len(set([api_number[0:11] for api_number in api_number_list])) == 1:
                            # Test if the 14 digit APIs in the list are the same
                            if len(set([api_number for api_number in api_number_list if len(api_number) == 14])) == 1:
                                # Return 14 digit api, normalized to desired length
                                return normalize_unformatted_api_length([api_number for api_number in api_number_list if len(api_number) == 14][0],return_length=return_length)
                            # Return 10 digit api, normalized to desired length
                            return normalize_unformatted_api_length(api_number_list[0][0:11],return_length=return_length)
    # Return None if API number not found or returned hetergenous list of found APIs
    # i.e. found APIs from different states, counties, and wells
    return None




def normalize_unformatted_api_length(input_str,return_length=14,missing_number='0'):
    # Test if the input contains only digits, if it does not, raise
    # an exception.
    if not contains_only_digits(input_str):
        raise ValueError("Input contains non-numerical character.")
    
    #print('normalizing length')
    #print(input_str)
    if len(input_str) == 10:
        #print('input api is 10 digit')
        if return_length == 10:
            return input_str
        if return_length == 12:
            return (input_str
                    + missing_number
                    + missing_number)
        if return_length == 14:
            #print('returning 14 digit api')
            return (input_str
                    + missing_number
                    + missing_number
                    + missing_number
                    + missing_number)
    elif len(input_str) == 12:
        if return_length == 10:
            return input_str[0:11]
        if return_length == 12:
            return input_str
        if return_length == 14:
            return (input_str
                    + missing_number
                    + missing_number)
    elif len(input_str) == 14:
        if return_length == 10:
            return input_str[0:11]
        if return_length == 12:
            return input_str[0:13] 
        if return_length == 14:
            return input_str


def api_from_las(las_path,
                 las,
                 api_dict=api_dict,
                 return_length=14):
    # Try to get from 'Well' section of LASIO object
    well = las.well
    #well_mnemonics = [item.mnemonic.upper() for item in well]
    api = None
    if len(well) > 0:
        if 'API' in well:
            #print('API in well section')
            api = well['API'].value
            #print(api)
            api = api_from_string(api)
            #print(api)
            if api != None:
                if len(api) >= 10:
                    return normalize_unformatted_api_length(api,return_length)
                else:
                    api = None
            else:
                api = None
        if 'api' in well:
            #print('api in well section')
            api = well['api'].value
            api = api_from_string(api)
            if api != None:
                if len(api) >= 10:
                    return normalize_unformatted_api_length(api,return_length)
                else:
                    api = None
            else:
                api = None
        if 'Api' in well:
            #print('Api in well section')
            api = well['Api'].value
            #print(api)
            api = api_from_string(api)
            #print(api)
            if api != None:
                if len(api) >= 10:
                    return normalize_unformatted_api_length(api,return_length)
                else:
                    api = None
            else:
                api = None
        if 'UWI' in well:
            #print('UWI in well section')
            api = well['UWI'].value
            #print(api)
            api = api_from_string(api)
            #print(api)
            if api != None:
                if len(api) >= 10:
                    return normalize_unformatted_api_length(api,return_length)
                else:
                    api = None
            else:
                api = None
        api = None
    if api == None:
        #print(las_path)
        # Try to get from las file name
        #print('No API found in las')
        api = api_from_string(las_path,api_dict)
        if api != None:
            #print(normalize_unformatted_api_length(api,return_length))
            return normalize_unformatted_api_length(api,return_length)
        return None


def format_api_string(input_str,
                      return_length=14,
                      missing_number='0',
                      delimiter='-'):
    # Test if the input contains any formatting characters and if it
    # does, raise an exception.
    if '-' in input_str or \
       '_' in input_str or \
       ' ' in input_str:
        raise ValueError("Only unformatted API Numbers are allowed,"\
                          "input contains a '-','_', or ' '.")
    
    # Test if the input is long enough to contain state, county, and well codes
    # and if it does not, raise an exception.
    if len(input_str) < 10:
        raise ValueError("Input must be at least 10 characters long.")
    
    # Test if the input contains only digits, if it does not, raise
    # an exception.
    if not contains_only_digits(input_str):
        raise ValueError("Input contains non-numerical character.")
    
    # Test if the return length is 10, 12, or 14.
    if return_length != 10 and \
       return_length != 12 and \
       return_length != 14:
        raise ValueError("Return length must be 10, 12, or 14.")
    
    # Test if the missing number contains only digits, if it does not, raise
    # an exception.
    if not contains_only_digits(missing_number):
        raise ValueError("Missing number input is a non-numerical character.")
    
    # Extract the first two digits, the state code, to a variable.
    state_code = input_str[0:2]
    
    # Extract the third through fifth digits, the county code, to a variable.
    county_code = input_str[2:5]
    
    # Test if the input is 10 digits long, if it is set the sixth through the 
    # last character, the well code, to a variable named well code.
    if len(input_str) == 10:
        well_code = input_str[5:]
    # Otherwise, set the sixth through the tenth character, the well code,
    # equal to a variable named well code.
    else:
        well_code = input_str[5:10]
    
    # Create the 10 digit API number by combining the state, county, and well
    # codes with delimiters between each and set it equal to a variable.
    api_10digit_formatted = (state_code
                             + delimiter
                             + county_code
                             + delimiter
                             + well_code)
    #print(api_10digit_formatted)
    
    # Test what the return length and input length are and do the appropriate
    # string concatenation and return the formatted output.
    if return_length == 10:
        if len(input_str) >= 10:
            formatted_api = api_10digit_formatted
            return api_10digit_formatted
    elif return_length == 12:
        if len(input_str) == 10:
            formatted_api = (api_10digit_formatted
                             + delimiter 
                             + missing_number 
                             + missing_number)
            return formatted_api
        elif len(input_str) == 11:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10]
                             + missing_number)
            return formatted_api
        elif len(input_str) == 12:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10:])
            return formatted_api
        elif len(input_str) >= 13:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10:12])
            return formatted_api
    elif return_length == 14:
        if len(input_str) == 10:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + missing_number
                             + missing_number
                             + missing_number
                             + missing_number)
            return formatted_api
        elif len(input_str) == 11:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10]
                             + missing_number
                             + missing_number
                             + missing_number)
            return formatted_api
        elif len(input_str) == 12:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10:]
                             + missing_number
                             + missing_number)
            return formatted_api
        elif len(input_str) == 13:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10:]
                             + missing_number)
            return formatted_api
        elif len(input_str) == 14:
            formatted_api = (api_10digit_formatted
                             + delimiter
                             + input_str[10:])
            return formatted_api


def unformat_api_string(input_str,
                        return_length=14,
                        missing_number='0',
                        delimiter='-'):
    # Test if the string contains the defined delimiter, if it does not, raise
    # an exception.
    if delimiter not in input_str:
        raise ValueError("Delimiter '%s' not found in input." % (delimiter,))
    
    # Test if the input is long enough to contain state, county, and well codes
    # and if it does not, raise an exception.
    if len(input_str) < 12:
        raise ValueError("Input must be at least 12 characters long.")
    
    # Test if the return length is 10, 12, or 14.
    if return_length != 10 and \
       return_length != 12 and \
       return_length != 14:
        raise ValueError("Return length must be 10, 12, or 14.")
    
    # Test if the missing number contains only digits, if it does not, raise
    # an exception.
    if not contains_only_digits(missing_number):
        raise ValueError("Missing number input is a non-numerical character.")
    
    # Split the api into state, well, county and suffix codes by splitting at 
    # the delimiter.
    split_api = input_str.split(delimiter)
    
    # If there are at least 3 parts (state, county and well codes) to the split
    # input string.
    if len(split_api) >= 3:
        state_code = split_api[0]
        county_code = split_api[1]
        well_code = split_api[2]
        # If there is a suffix present in the input, create the unformatted api
        # by combining state, county, well, and suffix codes.
        if len(split_api) == 4:
            suffix_code = split_api[3]
            unformatted_api = (state_code
                               + county_code
                               + well_code
                               + suffix_code)
            print(unformatted_api)
        # If there is no suffix code in input, create the unformatted api by
        # combining state, county and well codes
        elif len(split_api) == 3:
            unformatted_api = (state_code
                               + county_code
                               + well_code)
            print(unformatted_api)
    
    # Test if the unformatted api contains only digits, if it does not,
    # raise an exception.
    if not contains_only_digits(unformatted_api):
        raise ValueError("Input contains non-numerical character.")
    
    # Normalize the unformatted api to the desired length.
    unformatted_api = normalize_unformatted_api_length(
                                                unformatted_api,
                                                return_length=return_length,
                                                missing_number=missing_number
                                                )
    return unformatted_api


class APINumber():
    """
    Description:
        An API number (or US well number) is a minimum 10-digit number that is 
    used to identify an oil and gas well using the two digit and three digit 
    numbers that correspond to the state and county respectively where the oil 
    and gas well was drilled and a 5-digit number unique to each well that is
    typically assigned by a well permitting agency. Also, an API Number may 
    include a 2 to 4-digit suffix made up of a 2-digit wellbore number (typically 
    '00' for first wellbore) and a 2-digit completion number (typically '00' 
    for initial completion). This object assumes a string representation of an
    API number that does not include a wellbore or completion number is 
    referencing the first wellbore drilled and initial completion and will 
    therefore store a wellbore number and completion number of '00'.
    
        This object stores the formatted (with hyphens) version, unformatted
    version, and can return the individual parts of the API Number by name.
    
    Comparison:
        If a string representation of an API number is compared to an APINumber
    object it can be either formatted or unformatted and can be different 
    lengths; this is because the program assumes a wellbore and completion code.
    
    """
    def __init__(self,input_str,length=14,missing_number='0',delimiter='-'):
        # If input type is an APINumber object clone the object.
        if type(input_str) == APINumber:
            self.unformatted = input_str.unformatted
            self.formatted = input_str.formatted
            self.state_code = input_str.state_code
            self.county_code = input_str.county_code
            self.well_code = input_str.well_code
            self.suffix_code = input_str.well_code
            self.wellbore_code = input_str.wellbore_code
            self.comp_code = input_str.comp_code
        # If input type is a string use api_from_string function to verify it 
        # is an api.
        elif type(input_str) == str:
            self.unformatted = api_from_string(input_str,return_length=length)
        # If an unformatted API number has been created, create formatted API 
        # and extract state, county, well, and suffix codes.
        if self.unformatted != None:
            self.formatted = format_api_string(self.unformatted,
                                               return_length=length,
                                               missing_number=missing_number,
                                               delimiter=delimiter)
            self.state_code = self.formatted.split(delimiter)[0]
            self.county_code = self.formatted.split(delimiter)[1]
            self.well_code = self.formatted.split(delimiter)[2]
            self.suffix_code = self.formatted.split(delimiter)[3]
            self.wellbore_code = self.suffix_code[0:2]
            self.comp_code = self.suffix_code[2:]
        else:
            self.formatted = None
            self.state_code = None
            self.county_code = None
            self.well_code = None
            self.suffix_code = None
            self.wellbore_code = None
            self.comp_code = None
    
    # Use the unformatted version as the text representation of the object.
    def __repr__(self):
        return str(self.unformatted)
    
    # Define how to compare APINumber objects and string representations of API
    # numbers.
    def __eq__(self, other): 
        # If the other object is not an APINumber object...
        if not isinstance(other, APINumber):
            try:
                # and if the other object is a string...
                if type(other) == str:
                    # ...attempt to convert it to an APINumber object and 
                    # return True if they are equal.
                    other = APINumber(other)
                    return self.unformatted == other.unformatted
            except:
                # If the other object is not an APINumber object or string that
                # can be converted to an APINumber object don't attempt to 
                # compare the unrelated types.
                return NotImplemented
        if other != None:
            # Test if the APINumber objects are equal and return True if they are.
            return self.unformatted == other.unformatted
        else:
            return False

        
            








