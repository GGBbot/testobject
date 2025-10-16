# 封装发送 HTTP 请求的方法
import requests
import yaml
from core.variable_manager import VariableManager

def get_base_url():
    with open("config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["base_url"]

def send_request(method, url, **kwargs):
    base_url = get_base_url()
    headers = kwargs.get("headers", {})

    # 自动带 token
    token = VariableManager.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    kwargs["headers"] = headers
    response = requests.request(method, base_url + url, **kwargs)
    return response
