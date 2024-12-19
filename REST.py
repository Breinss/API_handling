import requests

BASE_URL = "https://restapi-nor.leaddesk.com/stable"

res_token = requests.post(
    "{}{}".format(BASE_URL, "/oauth/access-token"),
    json={
        "grant_type":"leaddesk_client_id",
        "client_id": "O4P2aSV8R4mZOPtVdi2OZZkqs3a5v0YqPEPAgAq5",  # <your-client-id>
        "client_secret": "yK1c6RUoGelC9XNTIOw5f713XLZbaZPTEjPe1epX",  # <your-client-secret>
        "leaddesk_client_id": 994 # <your-leadDesk-client-id>
    }

)
res_token.raise_for_status()
access_token = res_token.json()["access_token"]

response = requests.request(
    "GET",
    "{}{}".format(BASE_URL, "/users"),
    headers={
        "Authorization": "Bearer {}".format(access_token)
    },
    params={
        "per_page": 5,
        "page": 1
    }
)

result = {
    "code": response.status_code,
    "data": response.json()
}

if result.get("code") >= 200 and result.get("code") <= 299:
    print("Hello world, we have {} users in LeadDesk.\n".format(result["data"]["_meta"]["count"]))
else:
    print("Fail to get users data.\n")
    print(result)
