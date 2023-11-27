def sort_by_difviewcount(data):
    # Zip the lists into a list of tuples
    zipped_data = zip(data['channel'], data['difviewcount'], data['difsubscribercount'], data['diftotalvideo'])

    # Sort the list of tuples based on the difviewcount (index 1)
    sorted_data = sorted(zipped_data, key=lambda x: x[2] if isinstance(x[2], (int, float)) else float('-inf'), reverse=True)

    # Unzip the sorted data
    sorted_channel, sorted_difviewcount, sorted_difsubscribercount, sorted_diftotalvideo = zip(*sorted_data)

    # Create a new dictionary with the sorted data
    sorted_dict = {
        'channel': list(sorted_channel),
        'difviewcount': list(sorted_difviewcount),
        'difsubscribercount': list(sorted_difsubscribercount),
        'diftotalvideo': list(sorted_diftotalvideo),
    }

    return sorted_dict

# Example usage
data = {
    'channel': ['CSSGOSS', 'GadgetIn','Pricebook'],
    'difviewcount': [5050, 6000,1000],
    'difsubscribercount': [5000, 0, 6000],
    'diftotalvideo': [0, 0, 1]
}

sorted_data = sort_by_difviewcount(data)
print(sorted_data)
