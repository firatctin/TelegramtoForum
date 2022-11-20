import configparser
import json
import asyncio
from datetime import date, datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
def getting_messages():
    #İlk olarak config.ini adlı dosyadan telegram api bilgilerimizi alıyoruz
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_id = config['Telegram']['api_id'].strip("\n")
    api_hash = config['Telegram']['api_hash'].strip("\n")

    #Kullanılabilirlik açısından api_hash'imizi string'e dönüştürüyoruz

    api_hash = str(api_hash)

    phone = config['Telegram']['phone'].strip("\n")
    username = config['Telegram']['username'].strip("\n")

    #Tarih açısından kaydetmek için class oluşturuyoruz:
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()

            if isinstance(o, bytes):
                return list(o)

            return json.JSONEncoder.default(self, o)


    #Şimdi client ögemizi oluşturup giriş bilgilerimizi içine gönderiyoruz:
    client = TelegramClient(username, api_id, api_hash)
    all_messages = []
    async def main (phone):
        await client.start()
        print('Client başlatıldı!')


        #Giriş yapmak isteyen kişinin izinli olduğundan emin oluyoruz değilse sms onayını input alıyoruz:
        if not client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        offset_id = 0
        limit = 100
        
        total_messages = 0
        total_count_limit = 100
        with open('grup_adi.txt', 'r', encoding='UTF-8') as file:
            link = file.read()
            link = link.strip()
            my_channel = await client.get_entity(link)
        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = await client(GetHistoryRequest(
                peer= link,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break  
           
        
    with client:
        client.loop.run_until_complete(main(phone))
    return all_messages