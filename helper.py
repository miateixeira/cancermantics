# Similar to update() method for dicts, but adds values
# instead of assigning the highest value to the key
def sum_update(dict1, dict2):
    output = {}
    for key in dict1:
        if key not in dict2:
            output[key] = dict1[key]
        else:
            output[key] = dict1[key] + dict2[key]
    for key in dict2:
        if key not in dict1:
            output[key] = dict2[key]
    return output
