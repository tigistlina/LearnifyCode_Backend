import base64

# Path to your Firebase credentials JSON file
input_file_path = 'firebase_credentials/learnifycode_firebase_credentials.json'
output_file_path = 'credentials_base64.txt'

# Read the JSON file and encode it
with open(input_file_path, 'rb') as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')

# Write the base64 encoded string to a file
with open(output_file_path, 'w') as file:
    file.write(encoded_string)

print(f'Base64 encoded string saved to {output_file_path}')
