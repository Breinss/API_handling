
import requests
import json
import argparse
import openpyxl
import datetime
from auth import load_tokens
from cli import parse_arguments
from config import baseURL, auth, plussymbol, get_command_url, get_api_key

header = [
	"contact id", "phone number", "first name", "last name", "address", "postal code",
	"city", "is finalized(*)", "contact updated at", "phone number updated at",
	"phone number last call date", "last call result name", "last call campaign name",
	"last call agent name"
]
lines_appended = 0
args = parse_arguments()
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
tokens = load_tokens('auth.csv')



def clean_json(data):
	if isinstance(data, dict):
		return {k: clean_json(v) for k, v in data.items() if v not in [None, [], {}, ""]}
	elif isinstance(data, list):
		return [clean_json(item) for item in data if item not in [None, [], {}, ""]]
	else:
		return data

def make_request(command, **kwargs):
	url_command = get_command_url(command, **kwargs)
	if url_command:
		authURL = baseURL + tokens.get(kwargs.get('api_key'))
		full_url = authURL + url_command
		if command == "message":
			pass
		else:
			response = requests.get(full_url)

		if response.status_code == 200:
			try:
				if command == "findphone":
					json_data = json.loads(response.text)
					formatted_response = json.dumps(json_data, indent=4)
					contact_ids = json_data["contact_ids"]
					lines_appended = len(contact_ids) + 1
					print(f"{lines_appended} lines appended to contacts.txt")
					for id in contact_ids:
						contact_request = requests.get(authURL + f"&mod=contact&cmd=get&contact_id={id}")
						contact_json = clean_json(json.loads(contact_request.text))
						with open(f"contacts_{kwargs.get('phone_number')}_{timestamp}.txt", "a") as file:
							file.write(json.dumps(contact_json, indent=4))
							file.write("\n")
						if len(contact_ids) < 15:
							print(json.dumps(contact_json, indent=4))
				else:
					json_data = json.loads(response.text)
					formatted_response = json.dumps(json_data, indent=4)
					print("Formatted Response Data:", formatted_response)
			except json.JSONDecodeError:
				lines = response.text.splitlines()
				lines_list = []

				if command == "exportlist":
					workbook = openpyxl.Workbook()
					sheet = workbook.active
					sheet.append(header)
					for line in lines:
						columns = line.split(';')
						columns = [col.strip().strip('"') for col in columns]
						lines_list.append(columns)
						sheet.append(columns)
					workbook.save(f"contact_list_{kwargs.get('contact_list')}.xlsx")
		else:
			print("Error:", response.status_code, response.text)

args = parse_arguments()
kwargs = vars(args)
command = kwargs.pop("command")
make_request(command, **kwargs)
