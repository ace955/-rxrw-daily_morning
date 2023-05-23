from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]

ruixin_date = os.environ['RUIXIN_DATE']
zaocha_data = os.environ['ZAOCHA_DATE']

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_tea_day_count():
  next = datetime.strptime(str(date.today().year) + "-" + ruixin_date, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days+1

def get_zaocha_day_count():
  next = datetime.strptime(str(date.today().year) + "-" + zaocha_data, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days+1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days+1

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

word = get_words()
color = get_random_color()
# data = {"ruixin_date":{"value":get_tea_day_count()},"zaocha_data":{"value":get_zaocha_day_count()},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":word, "color":color}}
# res = wm.send_template(user_id, template_id, data)
data2 = {"ruixin_date":{"value":get_tea_day_count()},"zaocha_data":{"value":get_zaocha_day_count()},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":word, "color":color}}
res2 = wm.send_template(user_id2, template_id, data2)
print(res)

print(res2)
