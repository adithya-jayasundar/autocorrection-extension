import requests

url = "https://norvig.com/big.txt"
response = requests.get(url)

with open("big.txt", "w", encoding="utf-8") as f:
    f.write(response.text)
