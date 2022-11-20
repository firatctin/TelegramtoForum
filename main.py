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
import Telebot
import time
import csv


starting_time = datetime.now()
starting_time = starting_time.timestamp()
try:
    ending_time = int(input("Dakika cinsinden programın kaç dakika çalışacağını giriniz:"))
except:
    print("Hatalı giriş yaptınız lütfen bir tamsayı giriniz!:")
    ending_time = int(input("Dakika cinsinden programın kaç dakika çalışacağını giriniz:"))

ending_time = starting_time + 60*ending_time
headers = ["id","content"]
with open('contents.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
while datetime.now().timestamp() < ending_time:
    
    json_obj = Telebot.getting_messages()
    
    cleared_data= []
    indexcounter = 0
    ids = []
    zipped = []
    for i in json_obj:
        try:
            ids.append(i["id"])
        
            cleared_data.append(i["message"])
        except:
            continue
    zipped = list(zip(ids,cleared_data))
    with open('contents.csv', 'r', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        for i in csvreader:
            print(i)
    for i in zipped:
        if i[0] in csvreader:
            
    with open('contents.csv', 'a', encoding='utf-8') as file:
        csvwriter = csv.writer(csvfile)(file)
        
            

    print(zipped)
    time.sleep(20)

    
        

    
    time.sleep(5)