import httpx
import os
from dotenv import load_dotenv


def get_salesforce_token() -> list[str]:
    url = "https://login.salesforce.com/services/oauth2/token"  
    data = {
       "grant_type":"password",
       "client_id":os.getenv("CLIENT_ID"),
       "client_secret":os.getenv("CLIENT_SECRET"),
       "username":os.getenv("USERNAME"), 
       "password":os.getenv("PASSWORD") 
    } 

    headers = { 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    r = httpx.post(url, data=data, headers=headers)
    token = r.json()["access_token"]
    instance_url = r.json()["instance_url"]
    return [token, instance_url]