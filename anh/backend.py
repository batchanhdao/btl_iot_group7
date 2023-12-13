import json
from datetime import datetime
import paho.mqtt.client as paho
from youtube_search import YoutubeSearch
from GoogleNews import GoogleNews

temp = ""
hum = ""
topicTem = '/iot/group7/temp'
topicHum = '/iot/group7/hum'
topicAsk = '/iot/group7/ask'
topicAnswer = '/iot/group7/answer'

def onYoutube(key, Max_results=2):
    results = YoutubeSearch(key, max_results=Max_results).to_dict()
    contents = ""
    for article in results:
        content = ""
        url = 'https://www.youtube.com' + article['url_suffix']
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
    return contents

def onNewsGoogle(key, Lang='vi', Period='7d', Encode='utf-8'):
    contents = ""
    # Create a GoogleNews object
    googlenews = GoogleNews()

    googlenews.set_lang(Lang)
    googlenews.set_period(Period)
    googlenews.set_encode(Encode)
    # Perform a search 
    googlenews.search(key)
    # Get news articles
    results = googlenews.result()

    limit = 3
    # Print the titles and links of the first few articles
    for article in results:
        if limit==0:
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
        limit-=1

    # Clear the results (optional)
    googlenews.clear()  
    contents = "<table>" + contents + "</table>"
    # print(contents)
    return contents


def Answer(ask):
    newspaper = onNewsGoogle(ask) 
    video = onYoutube(ask)
    # url, image, title = onYoutube(ask)
    
    return json.dumps({"newspaper": newspaper, "video": video})


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    global temp, hum
    data = str(msg.payload.decode("UTF-8"))
    print(msg.topic+" "+str(msg.qos)+" "+data)   
    
    if  msg.topic == topicTem:
        temp = data
    if  msg.topic == topicHum:
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

client.loop_forever()
client.disconnect()

