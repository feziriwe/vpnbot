import requests
import urllib3
from config import OUTLINE_API_URL, OUTLINE_API_KEY

# Отключаем предупреждения о небезопасном SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_key():
    url = f"{OUTLINE_API_URL}/access-keys"
    headers = {"Authorization": f"Bearer {OUTLINE_API_KEY}"}
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 201:
        return response.json()["accessUrl"], response.json()["id"]
    else:
        raise Exception("Не удалось создать ключ")

def delete_key(key_id):
    url = f"{OUTLINE_API_URL}/access-keys/{key_id}"
    headers = {"Authorization": f"Bearer {OUTLINE_API_KEY}"}
    requests.delete(url, headers=headers, verify=False)
