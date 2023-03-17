import requests

def get_random_string(length):
    url = f"https://www.random.org/strings/?num=1&len={length}&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new"
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip()
