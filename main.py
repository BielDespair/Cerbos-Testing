from jwt import ExpiredSignatureError, InvalidSignatureError
from pydantic import BaseModel
from cerbos import CerbosClient
from authentication import JWTHandler
from fastapi import FastAPI, HTTPException, Request
import uvicorn

app = FastAPI()

cerbos = CerbosClient()
jwt = JWTHandler()

class LoginRequest(BaseModel):
    username: str
    password: str

def prepare_cerbos_request(token: dict, action: str, resource_kind: str, resource_id: str)  -> dict:
    principal = {
        "id":token["sub"],
        "roles": token["roles"],
        "attr":{}
    }
    resources = [
        {
            "actions":["open"],
            "resource": {
                "kind": "cookie_jar",
                "id": "cookie_jar1",
                "attr": {"grounded":False}
            }
        }
    ]

    return {

    }

def extract_token(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401)
    
    token = auth_header.split(" ")[1]
    try:
        decoded_token = jwt.decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid signature")

    return decoded_token

@app.post("/auth")
def authenticate(data: LoginRequest):
    if (not ((data.username == "mom" or data.username == "dad" or data.username == "child") and data.password == "1234")):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    #Ele buscaria no banco / keycloack a role do usuário. No momento, fica hardcoded.
    roles = []
    roles.append(data.username)

    token = jwt.generate_token(data.username, roles)
    return {"acess_token": token, "token_type": "bearer"}


@app.get("/cookie-jar")
def get_cookie(request: Request) -> dict:
    token = extract_token(request)
    principal = {
        "id":token["sub"],
        "roles": token["roles"],
        "attr":{"grounded":False}
    }
    resources = [
        {
            "actions":["open"],
            "resource": {
                "kind": "cookie_jar",
                "id": "cookie_jar1",
                "attr": {}
            }
        }
    ]

    return cerbos.check(principal, resources)

@app.patch("/cookie-jar")
def refill_cookie_jar(request: Request) -> dict:
    token = extract_token(request)

    principal = {
        "id":token["sub"],
        "roles": token["roles"],
        "attr":{}
    }
    resources = [
        {
            "actions":["refill"],
            "resource": {
                "kind": "cookie_jar",
                "id": "cookie_jar1",
                "attr": {}
            }
        }
    ]
    return cerbos.check(principal, resources)

@app.get("/biscuit-jar")
def get_biscuit(request: Request) -> dict:
    token = extract_token(request)

    principal = {
        "id":token["sub"],
        "roles": token["roles"],
        "attr":{}
    }
    resources = [
        {
            "actions":["open"],
            "resource": {
                "kind": "biscuit_jar",
                "id": "biscuit_jar1",
                "attr": {}
            }
        }
    ]
    return cerbos.check(principal, resources)

@app.patch("/biscuit-jar")
def refill_biscuit_jar(request: Request) -> dict:
    token = extract_token(request)

    principal = {
        "id":token["sub"],
        "roles": token["roles"],
        "attr":{}
    }
    resources = [
        {
            "actions":["refill"],
            "resource": {
                "kind": "biscuit_jar",
                "id": "biscuit_jar1",
                "attr": {}
            }
        }
    ]
    return cerbos.check(principal, resources)

'''
Admin: Create, Read, Update, Delete
User: Create, Read, Update, Delete
'''


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)