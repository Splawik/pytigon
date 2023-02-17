import httpx

#Assign to access_token, token_type the result of the script operation: 2_rest_get_access_token.sh
key = {
    "access_token": "zmL9nWTrVTrRphrfOnj3irbwRBMqiz",
    "token_type": "Bearer",
}

endpoint = "http://127.0.0.1:8000/api/tables_adv_demo/hello"

headers = {"Authorization": "%s %s" % (key["token_type"], key["access_token"])}
print(httpx.get(endpoint, headers=headers).json())
