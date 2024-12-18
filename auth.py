import csv

def load_tokens(filename):
    tokens = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            client_id = row['ClientID']
            auth_token = row['AuthToken']
            tokens[client_id] = auth_token
    return tokens
