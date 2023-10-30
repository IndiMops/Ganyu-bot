import json

input_file_path = 'locale\\uk.json'

with open(input_file_path, 'r', encoding = 'utf-8') as file:
    json_data = file.read()

data = json.loads(json_data)
sorted_data = json.dumps(data, indent = 4, ensure_ascii = False, sort_keys = True)

output_file_path = 'locale.json'

with open(output_file_path, 'w', encoding = 'utf-8') as output_file:
    output_file.write(sorted_data)

print('The sorted JSON is saved to a file: {0}'.format(output_file_path))
