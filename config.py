
plussymbol = '%2B'
#ea45913a5dee0adc0b07c83212948bd0
#994 API KEY
auth = 'empty'



baseURL = 'https://api.leaddesk.com/?auth='
arguments = ['findphone', 'exportlist', 'sendmessage', 'agents', 'findcontact', 'findagent']

commands = {
    "findphone": lambda **kwargs: f"&mod=contact&cmd=find&phone=%2B{kwargs.get('phone_number')}",
    "exportlist": lambda **kwargs: f"&mod=calling_list&cmd=export&id={kwargs.get('contact_list')}",
    "sendmessage": lambda **kwargs: f"&mod=messaging&cmd=send_agent&id={kwargs.get('agent_id')}&message={kwargs.get('message')}&mode=append",
    "findcontact": lambda **kwargs: f"&mod=contact&cmd=get&contact_id={kwargs.get('contact_id')}",
    "findagent": lambda **kwargs: f"&mod=agent&cmd=find&username=*",
}


def get_api_key(**kwargs):
        return kwargs.get('api_key')

def get_command_url(command, **kwargs):
    command_func = commands.get(command)
    if command_func:
        return command_func(**kwargs)
    return None