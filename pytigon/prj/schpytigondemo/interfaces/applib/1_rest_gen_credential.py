import base64

# register application: http://127.0.0.1:8000/o/applications/
# Client type: confidential, Authorization Grant Type: lient-credentials
# Rewrite the parameters client_id, secret to the lines below
client_id = "rchd90b0H9IeW3IWNS4izxAa5Ai9IFsmryKNxSkl"
secret = "6Pp20cCwfZU3qaiXJuXeQ6MGiSXPLkBe8AHvJeej0U2ZPYZUw0DysJHQhffHkZgAC9TxeOos7xxhHl4s57RWX5QH7xr9bhJsJBuJtAPPB3oRXkiVlGHp4RdlJUueXZiP"

credential = "{0}:{1}".format(client_id, secret)
b64_credential = base64.b64encode(credential.encode("utf-8"))

print(b64_credential.decode("utf-8"))
