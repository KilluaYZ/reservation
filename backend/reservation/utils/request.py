import requests
import json

def post_with_auth(url: str, authorization: str, data: dict={})  ->  dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization":  authorization
    }
    return requests.post(url, data=json.dumps(data), headers=headers).json()

def post(url: str, data: dict) -> dict:
    headers = {
        "Content-Type": "application/json",
    }
    return requests.post(url, data=json.dumps(data), headers=headers).json()

def get_with_auth(url: str, authorization: str, param: dict={}) -> dict:
    headers = {
        "Authorization": authorization
    }
    return requests.get(url, params=param, headers=headers).json()

def get(url: str, param: dict={}) -> dict:
    return requests.get(url, params=param).json()
