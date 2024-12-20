import requests
import json
import argparse
import openpyxl
import datetime
from auth import load_tokens
from cli import parse_arguments
from config import baseURL, auth, plussymbol, get_command_url, get_api_key, header
from handling import APIClient

lines_appended = 0
args = parse_arguments()
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
tokens = load_tokens("auth.csv")
client = APIClient()


def main():
    args = parse_arguments()
    kwargs = vars(args)
    command = kwargs.pop("command")
    url_command = get_command_url(command, **kwargs)
    response = client.make_request(command, kwargs.get("api_key"), tokens, url_command)
    calls(command, response, **kwargs)
    return


def calls(command, response, **kwargs):
    if command == "findphone":
        client.findphone(response, kwargs.get("phone_number"))
        return
    if command == "exportlist":
        lines = response.text.splitlines()
        client.exportlist(lines, kwargs.get("contact_list"))
        return
    if command == "findlist":
        client.findlist(response, kwargs.get("list"), True)
        return
    if command == "widget":
        json_data = json.loads(response.text)
        print(json.dumps(json_data, indent=4))
        return
    if command == "findandexport":
        list = client.findlist(response, kwargs.get("list"), True)
        if client.yes_no_question(
            f"You are about to download {len(list)} items. Do you want to proceed?"
        ):
            print("You chose yes!")
            for data in list:
                print(data)  # Debug: Print each item in the list
                client.exportlists(data["id"])  # Export the list
        else:
            print("You chose no!")
            return  # Exit if the user chooses not to proceed


def make_request(command, **kwargs):
    url_command = get_command_url(command, **kwargs)
    if url_command:
        if isinstance(tokens.get(kwargs.get("api_key")), str):
            authURL = baseURL + tokens.get(kwargs.get("api_key"))
            full_url = authURL + url_command
        else:
            print("Invalid ClientID: " + kwargs.get("api_key"))
            return
        if command == "message":
            pass
        else:
            response = requests.get(full_url)


if __name__ == "__main__":
    main()  # Calls the main function
