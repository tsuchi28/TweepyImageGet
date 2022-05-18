# 2021/10/25 URLを指定してツイートID抽出、そしてstatusを取得、そこから動画を保存するプログラムを作りたい→完成
# 参考：https://teratail.com/questions/329739
# 　　　https://qiita.com/Jameson/items/184a065d96b50f9c5750

import tweepy
import tauth
import re
import sys
import urllib.request
import urllib.error

api = tauth.api

folder_path = "./douga/"

# URLからIDを抽出
url = input("URlを入力：")

id = re.search('[0-9]{19,20}', url).group()
if id == None:
    print("URLが有効ではありません。")
    sys.exit() # 強制終了

# IDからstatus取得
status = api.get_status(id, tweet_mode='extended', include_entities=True)
# print(status.text)

def download_file(url, file_name):
   urllib.request.urlretrieve(url, folder_path + file_name)

# 動画抽出
if hasattr(status, 'extended_entities'): # statusがextended_entities属性を持っているか判定
    ex_media = status.extended_entities['media']
    if 'video_info' in ex_media[0]:
        ex_media_video_variants = ex_media[0]['video_info']['variants']
        media_name = '%s.mp4' % (id)
        if 'animated_gif' == ex_media[0]['type']:
            #GIFファイル
            gif_url = ex_media_video_variants[0]['url']
            download_file(gif_url, media_name)
        else:
            #動画ファイル
            bitrate_array = []
            for movie in ex_media_video_variants:
                bitrate_array.append(movie.get('bitrate',0))
            max_index = bitrate_array.index(max(bitrate_array))
            movie_url = ex_media_video_variants[max_index]['url']
            download_file(movie_url, media_name)
else:
    print("extended_entitiesがないよ。")