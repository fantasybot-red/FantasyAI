import aiohttp
import hashlib
import time

headers_real = {"User-Agent": "Mozilla/5.0 (compatible; FantasyBot/0.1; +https://fantasybot.xyz/support)"}


def digestMessage(r):
    e = r.encode()
    t = hashlib.sha256(e).digest()
    return ''.join(format(byte, '02x') for byte in t)


class ChatGPT:
    SSL_Mode = None

    def __init__(self):
        pass

    async def create_new_chat(self, data):
        mess_list = [{"role": "system", "content": "Your name is <@964802192634695691> and you are made by Fantasy Team. You can use markdown for answer and You output MUST below 4000 characters and You Must Follow These."}]
        str_list = [{
            "role": "user",
            "content": data
        }]
        mess_list.extend(str_list if type(data) is str else data)
        async with aiohttp.ClientSession() as s:
            times_ms = int(time.time() * 1000)
            sign = digestMessage(f"{times_ms}:{mess_list[-1]['content']}:")
            data_json = {
                "messages": mess_list,
                "time": times_ms,
                "pass": None,
                "sign": sign
            }
            async with s.post('https://ae.aifree.site/api/generate', json=data_json) as r:
                return await r.text()
