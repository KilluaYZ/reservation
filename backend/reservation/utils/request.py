import requests
import json

def request_to_string(url, headers, method: str, data={}, param={}):
    return f"""request请求参数如下:
url: {url}
headers: {headers}
method: {method}
data: {data}
param: {param}
    """


def post_with_auth(url: str, authorization: str, data: dict={})  ->  dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    try:
        return requests.post(url, data=json.dumps(data), headers=headers).json()
    except Exception as e:
        raise Exception(f"请求失败！{request_to_string(url, headers, method='POST', data=data)}\n错误信息:{e}")

def post(url: str, data: dict) -> dict:
    headers = {
        "Content-Type": "application/json",
    }
    try:
        return requests.post(url, data=json.dumps(data), headers=headers).json()
    except Exception as e:
        raise Exception(f"请求失败！{request_to_string(url, headers, method='POST', data=data)}\n错误信息:{e}")

def get_with_auth(url: str, authorization: str, param: dict={}) -> dict:
    headers = {
        "Authorization": authorization
    }
    try:
        return requests.get(url, params=param, headers=headers).json()
    except Exception as e:
        raise Exception(f"请求失败！{request_to_string(url, headers, method='GET', param=param)}\n错误信息:{e}")

def get(url: str, param: dict={}) -> dict:
    try:
        return requests.get(url, params=param).json()
    except Exception as e:
        raise Exception(f"请求失败！{request_to_string(url, {}, method='GET', param=param)}\n错误信息:{e}")
