from apiclient.discovery import build
from datetime import datetime
import os
import re
import json

powerful_api_key = os.environ.get("POWERFUL_API_KEY")
powerful_channelId = "UCzQUP1qoWDoEbmsQxvdjxgQ"

def getVideos(api_key=powerful_api_key, channelId=powerful_channelId):
    videosResponse = []
    nextPageToken = ""
    videos = []

    youtube = build("youtube", "v3", developerKey=api_key)

    playlistResponse = youtube.channels().list(
        id=channelId,
        part="contentDetails"
    ).execute()

    playlistId = playlistResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    while nextPageToken is not None:
        thisPageResponse = youtube.playlistItems().list(
            playlistId=playlistId,
            part="snippet",
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        videosResponse += thisPageResponse["items"]
        nextPageToken = thisPageResponse.get("nextPageToken")

    for video in videosResponse:
        title = video["snippet"]["title"]
        videoId = video["snippet"]["resourceId"]["videoId"]
        URL = "https://www.youtube.com/watch?v=" + videoId
        fullDate = datetime.strptime(video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S.000Z").strftime("%Y-%m-%d %H:%M:%S")
        description = video["snippet"]["description"]
        thumbnail = video["snippet"]["thumbnails"]["high"]["url"]
        number = 0

        if title[:22].lower() == "joe rogan experience #":
            category = "Interview"
            number = int(re.findall("\d+", title)[0] if bool(re.search(r"\d", title)) else 0)

        elif title[:41].lower() == "joe rogan experience - fight companion - ":
            category = "Fight Companion"

        elif title[:14].lower() == "jre mma show #":
            category = "MMA Show"
            number = int(re.findall("\d+", title)[0] if bool(re.search(r"\d", title)) else 0)

        elif title[-11:].lower() == " - jre toon" or title[-12:].lower() == " - jre toons":
            category = "JRE Toons"

        elif title[:27].lower() == "joe rogan experience vlog #":
            category = "Vlog"
            number = int(re.findall("\d+", title)[0] if bool(re.search(r"\d", title)) else 0)

        elif title[:19].lower() == "best of the week - ":
            category = "Best of the Week"

        elif title[:32].lower() == "joe rogan questions everything #":
            category = "Joe Questions Everything"
            number = int(re.findall("\d+", title)[0] if bool(re.search(r"\d", title)) else 0)

        elif title[-15:].lower() == " year in review":
            category = "Year in Review"

        elif "(from" in title.lower():
            category = "Clip"
            number = int(re.findall("\d+", title)[0] if bool(re.search(r"\d", title)) else 0)

        else:
            category = "Other"

        videos.append({
            "title": title,
            "category": category,
            "number": number,
            "url": URL,
            "publishedAt": fullDate,
            "description": description,
            "thumbnail": thumbnail,
        })

    return videos

def saveToStatic(videos, path):
    with open(path, "w") as file:
        json.dump(videos, file)

def readFromStatic(path):
    with open(path) as file:
        return json.load(file)

def getFilteredVideos(videos, guest="", category="", sort="publishedAt", order="descending"):
    return sorted(
        [video for video in videos if guest.lower() in video["title"].lower() and (video["category"] == category or category == "all")],
        key=lambda i: i[sort],
        reverse=False if order == "ascending" else True
    )
