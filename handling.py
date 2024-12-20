import requests
import json
import argparse
import openpyxl
import datetime
from auth import load_tokens
from cli import parse_arguments
from config import baseURL, auth, plussymbol, get_command_url, get_api_key, header


class APIClient:
    def __init__(self, base_url=None, api_key=None):
        self.response = None
        lines_appended = 0
        args = parse_arguments()
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.base_url = base_url
        self.api_key = api_key
        self.authURL = ""

    def clean_json(self, data):
        if isinstance(data, dict):
            return {
                k: self.clean_json(v)
                for k, v in data.items()
                if v not in [None, [], {}, ""]
            }
        elif isinstance(data, list):
            return [
                self.clean_json(item) for item in data if item not in [None, [], {}, ""]
            ]
        else:
            return data

    def make_request(self, command, api_key, tokens, url_command):
        if url_command:
            if isinstance(tokens.get(api_key), str):
                self.authURL = baseURL + tokens.get(api_key)
                full_url = self.authURL + url_command
                response = requests.get(full_url)
                if response.status_code == requests.codes.ok:
                    return response
                else:
                    print(response.raise_for_status())
                    return
            else:
                print("Invalid ClientID: " + kwargs.get("api_key"))
                return

    def findphone(self, response, phone_number):
        json_data = json.loads(response.text)
        formatted_response = json.dumps(json_data, indent=4)
        contact_ids = json_data["contact_ids"]
        lines_appended = len(contact_ids) + 1
        print(f"{lines_appended} lines appended to contacts.txt")
        for id in contact_ids:
            contact_request = requests.get(
                self.authURL + f"&mod=contact&cmd=get&contact_id={id}"
            )
            contact_json = self.clean_json(json.loads(contact_request.text))
            with open(
                f"contacts_{phone_number}_{self.timestamp}.txt",
                "a",
            ) as file:
                file.write(json.dumps(contact_json, indent=4))
                file.write("\n")
            if len(contact_ids) < 15:
                print(json.dumps(contact_json, indent=4))
                continue

    def exportlist(self, lines, contact_list):
        lines_list = []
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(header)
        for line in lines:
            columns = line.split(";")
            columns = [col.strip().strip('"') for col in columns]
            lines_list.append(columns)
            sheet.append(columns)
        workbook.save(f"contact_list_{contact_list}.xlsx")
        return

    def exportlists(self, list_id):
        list_json = requests.get(
            self.authURL + f"&mod=calling_list&cmd=export&id={list_id}"
        )
        lines = list_json.text.splitlines()
        self.exportlist(lines, list_id)
        return

    def findlist(self, response, name="", silent=False):
        json_data = json.loads(response.text)
        if not name:
            formatted_response = json.dumps(json_data, indent=4)
            print(formatted_response)
        else:
            data = [item for item in json_data if name.lower() in item["name"].lower()]
            filtered_data = json.dumps(data, indent=4)
            return data
            if not silent:
                print(filtered_data)
                return
            return
        return

    def yes_no_question(self, prompt):
        while True:
            answer = input(f"{prompt} (yes/no): ").strip().lower()
            if answer in ["yes", "y"]:
                return True
            elif answer in ["no", "n"]:
                return False
            else:
                print("Please answer with 'yes', 'y', 'no', or 'n'.")

    def findandexport(self, response, name):
        if name != 0:
            return
        return
