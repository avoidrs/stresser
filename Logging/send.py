from JsonParser.parser import *

import requests

async def sendAdmins(message):
    for admin in Config().Admins:
        requests.get(f'https://api.telegram.org/bot{Config().NotifyToken}/sendMessage?chat_id={admin}&text={message}&disable_web_page_preview=True&parse_mode=HTML')