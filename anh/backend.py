import json
from datetime import datetime
import paho.mqtt.client as paho
from youtube_search import YoutubeSearch
from GoogleNews import GoogleNews
import requests

temp = ""
hum = ""
topicTem = '/iot/group7/temp'
topicHum = '/iot/group7/hum'
topicAsk = '/iot/group7/ask'
topicAnswer = '/iot/group7/answer'


def onYoutube(key, Max_results=2):
    contents = ""
    try:
        with requests.get('https://youtube.com', timeout=5) as response:
            response.raise_for_status()
            results = YoutubeSearch(key, max_results=Max_results).to_dict()
            for article in results:
                content = ""
                url = "https://www.youtube.com" + article['url_suffix']
                image = str(article['thumbnails'][0])
                title = str(article['title'])
                content = content + f"<td>{title}</td>" + f'<td><a href="{url}" target="_blank"><img src="{image}"></a></td>'
                content = "<tr>" + content + "</tr>"
                contents = contents + content

            # print(results)
            # print(results[0]['thumbnails'][0])
            # print(results[0]['title'])
            # print(results[0]['url_suffix'])
            contents = "<table>" + contents + "</table>"
            # print(contents)
    except requests.exceptions.Timeout:
        print("YouTube request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Request to YouTube failed: {e}")
    return contents


def onNewsGoogle(key, Lang='vi', Period='7d', Encode='utf-8'):
    contents = ""
    try:
        googlenews = GoogleNews()

        googlenews.set_lang(Lang)
        googlenews.set_period(Period)
        googlenews.set_encode(Encode)

        googlenews.search(key)

        results = googlenews.result()

        limit = 3
        for article in results:
            if limit == 0:
                break
            content = ""
            title = str(article['title'])
            link = str(article['link']).split('&ved')[0]
            content = content + f"<td>{title}</td>" + f'<td><a href="{link}" target="_blank">read news</a></td>'
            content = "<tr>" + content + "</tr>"
            # print("Title:", title)
            # print("Link:", link)
            # print()
            contents = contents + content
            limit -= 1

        googlenews.clear()
        contents = "<table>" + contents + "</table>"
        # print(contents)
    except requests.exceptions.Timeout:
        print("YouTube request timed out.")
    return contents


def Answer(ask):
    newspaper = onNewsGoogle(ask)
    video = onYoutube(ask)

    return json.dumps({"newspaper": newspaper, "video": video})


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    global temp, hum
    data = str(msg.payload.decode("UTF-8"))
    print(msg.topic + " " + str(msg.qos) + " " + data)

    if msg.topic == topicTem:
        temp = data
    if msg.topic == topicHum:
        hum = data

    if temp != "" and hum != "":
        print(temp, hum)
        with open("data.txt", "a+", encoding="UTF-8") as file:
            file.write(temp + "; " + hum + "; " + str(datetime.now()) + "\n")
        temp, hum = "", ""
    if msg.topic == topicAsk:
        ask = data
        client.publish(topicAnswer, Answer(ask), qos=0)


client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('broker.mqttdashboard.com', 1883)
client.subscribe('/iot/group7/#', qos=1)

try:
    client.loop_forever()
except Exception as e:
    print(e)
    client.disconnect()
