import socket
import requests

async def iplookup(target):
    try:
        try:
            socket.inet_aton(target)
            ip = target
        except socket.error:
            ip = socket.gethostbyname(target)
        
        response = requests.get(f"https://ipinfo.io/{ip}")
        data = response.json()

        return [ip, data.get("hostname"), data.get("org"), data.get("company"), data.get("country"), data.get("city")]
        
    except (socket.error, requests.exceptions.RequestException) as err:
        return False