from cerbos import CerbosClient
from authentication import JWTHandler
from fastapi import FastAPI

app = FastAPI()



'''
Admin: Create, Read, Update, Delete
User: Create, Read, Update, Delete
'''

cerbos = CerbosClient()
jwt = JWTHandler()

principal = {
    "id":"son1",
    "roles":["mom"]
}

resources = [
    {
        "actions": ["open","steal", "refill"],
        "resource": {
            "kind": "cookie_jar",
            "id": "cookiejar1",
            "attr": {}
        }
    }
]

payload = principal

token = jwt.generate(payload)

print(token)

print("--------------------------------------------------")
print(jwt.extract_claims(token))


#print(cerbos.check(principal, resources))

