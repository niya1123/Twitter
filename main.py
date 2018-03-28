#! user/bin/env python3
# -*- coding: utf-8 -*-

from settings import CK, CS, AT, ATS
from requests_oauthlib import OAuth1Session
from io import StringIO
import json, time, calendar, subprocess


def Client_Key():
    """
    TwitterはOAuth認証を行なっているのでそのためのもの.
    """
    return OAuth1Session(
        client_key = CK,
        client_secret = CS,
        resource_owner_key = AT,
        resource_owner_secret = ATS
    )


def Response(client, **filter_data):
    """
    引数にclient(Client_Keyで返ってくるもの)と**filter_data(Twitterの検索するときのフィルター複数設定可)
    """
    return client.post(
        URL,
        data = filter_data,
        stream = True
    )


def YmdHMS(created_at):
    """
    tweetの投稿日時を定めるもの.Twitterから返ってくるjsonのcreated_atは日本基準ではないので,それを日本基準にするため.
    """
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y年%m月%d日%H時%M分%S秒", time_local)

def PrintTweet(r):
    """
    本格的なtweet内容の表示
    """
    try:
        for line in r.iter_lines():
            
                tweet = json.loads(line.decode('utf-8'))
                    
                """
                Created_at:投稿時間
                User:ユーザのIDを格納するもの
                Name:ユーザの名前を格納するもの
                Text:Twitterの投稿の本文の内容
                python2からpython3に移行する際には.encodeはいらないことに注意.すべてstr型に変更されている.
                """
                Created_at = YmdHMS(tweet["created_at"])
                User = (tweet["user"]["screen_name"])
                Name = (tweet["user"]["name"])
                Text = (tweet["text"])
            
                if 'retweeted_status' not in tweet:
                    print(Created_at)
                    print("ID: @",end="")
                    print(User)
                    print("ユーザ名: ",end="")
                    print(Name)
                    print("ツイート本文")
                    print(Text)
                    print("=="*40)
                    time.sleep(0.5)
                    if "extended_entities" in tweet:
                        for i in range(len(tweet["extended_entities"]["media"])):
                            media = tweet["extended_entities"]["media"][i]["media_url_https"]
                            print("画像のID: ",end="")
                            print(media)
                            cmd = "curl -s " + media + ":small" + "| imgcat"
                            subprocess.call(cmd, shell = True)
                            print("=="*40)
                            time.sleep(1) 
                    else:
                        pass             
                else:
                    pass   

                """
                もし画像内容が投稿されてる際にはこの文を実行して画像を表示する.
                その際subprocessをimportしておきコマンドラインでimgcatを実行しコマンドプロント場で画像を表示する.
                しかし,デフォルトのterminalではコマンドは実行できるが,表示はされないので,iTerm2などのそのほかのterminaを使った方が良い.
                """

    except (ValueError or json.decoder.JSONDecodeError) or AttributeError:    
        print("Tweet待機しています")
        time.sleep(10)
        PrintTweet(r)
    
if __name__ == "__main__":
    client = Client_Key()
    word = input("検索したいワードを入力してください: ")
    # word += " OR @absgdifewfu"
    # print(word)
    URL = "https://stream.twitter.com/1.1/statuses/filter.json"
    r = Response(
        client,
        track = word
    )
    PrintTweet(r)
        
