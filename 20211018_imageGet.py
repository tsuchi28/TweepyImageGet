# https://note.com/mitsuru_h_cc/n/n6a4e0b2134a8

import os
import sys
import tweepy
from time import sleep
import urllib.error
import urllib.request
import tauth
from tweepy.error import TweepError

api = tauth.api

def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

key_account = input('Enter account name:')
search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items()

# フォルダがなかったら作成
os.makedirs(f'img/{key_account}', exist_ok=True)
print("((((mkdir))))") #debug

try:
    for result in search_results:
        # RTだったらDLしない
        if("RT @" in result.text[0:4]):
            pass
        else:
            try:
                img_url = result.extended_entities['media'][0]['media_url']
                dst_path = f'img/{key_account}/{key_account}_{result.id}.png'
                download_file(img_url,dst_path)
                sleep(0.3)
            except:
                pass
# 存在しないユーザIDを指定したとき、
except TweepError as e:
    # フォルダの中身が空だったらフォルダ削除
    try:
        os.rmdir(f"img/{key_account}/")
        print("((((rmdir))))") #debug
        print(os.listdir(f"img/")) #debug
    except OSError as e:
        pass
    # プログラム終了
    print("((((exit))))") #debug
    sys.exit()