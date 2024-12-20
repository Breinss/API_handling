plussymbol = "%2B"
# ea45913a5dee0adc0b07c83212948bd0
# 994 API KEY
auth = "empty"
header = [
    "contact id",
    "phone number",
    "first name",
    "last name",
    "address",
    "postal code",
    "city",
    "is finalized(*)",
    "contact updated at",
    "phone number updated at",
    "phone number last call date",
    "last call result name",
    "last call campaign name",
    "last call agent name",
]


baseURL = "https://api.leaddesk.com/?auth="
arguments = [
    "findphone",
    "exportlist",
    "sendmessage",
    "agents",
    "findcontact",
    "findagent",
    "findlist",
    "widget",
    "findandexport",
]

commands = {
    "findphone": lambda **kwargs: f"&mod=contact&cmd=find&phone=%2B{kwargs.get('phone_number')}",
    "exportlist": lambda **kwargs: f"&mod=calling_list&cmd=export&id={kwargs.get('contact_list')}",
    "sendmessage": lambda **kwargs: f"&mod=messaging&cmd=send_agent&id={kwargs.get('agent_id')}&message={kwargs.get('message')}&mode=append",
    "findcontact": lambda **kwargs: f"&mod=contact&cmd=get&contact_id={kwargs.get('contact_id')}",
    "findagent": lambda **kwargs: f"&mod=agent&cmd=find&username=*",
    "findlist": lambda **kwargs: f"&mod=calling_list&cmd=list",
    "widget": lambda **kwargs: f"&mod=widget&cmd=list",
    "findandexport": lambda **kwargs: f"&mod=calling_list&cmd=list",
}


def get_api_key(**kwargs):
    return kwargs.get("api_key")


def get_command_url(command, **kwargs):
    command_func = commands.get(command)
    if command_func:
        return command_func(**kwargs)
    return None
