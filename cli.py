import argparse
from config import arguments


def parse_arguments():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="API Command Runner")

    parser.add_argument("command", choices=arguments, help="The command to execute")
    parser.add_argument(
        "--api_key",
        type=str,
        default=0,
        help="ClientID of the client, key will be parsed by script",
    )
    parser.add_argument(
        "--phone_number",
        type=str,
        default=0,
        help="Phonenumber: format 31612345678 the plussign will be added by the script",
    )
    parser.add_argument(
        "--contact_list", type=str, default=0, help="The contact list ID"
    )
    parser.add_argument(
        "--message",
        type=str,
        default=0,
        help="The message you want to send to the agent",
    )
    parser.add_argument(
        "--agent_name", type=str, default=0, help="The agent name, roughly"
    )
    parser.add_argument("--contact_id", type=str, default=0, help="The contact ID")
    parser.add_argument("--list", type=str, default=0, help="Contact list name")

    return parser.parse_args()
