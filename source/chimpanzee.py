from apiclient.discovery import build
import os
import re

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
        # nextPageToken = thisPageResponse.get("nextPageToken")
        nextPageToken = None

    for video in videosResponse:
        position = int(video["snippet"]["position"]) + 1
        title = video["snippet"]["title"]
        number = int(re.findall("\d+", title)[0] if bool(re.search(r"\d", title)) else 0)
        videoId = video["snippet"]["resourceId"]["videoId"]
        URL = "https://www.youtube.com/watch?v=" + videoId
        fullDate = video["snippet"]["publishedAt"]
        description = video["snippet"]["description"]
        thumbnail = video["snippet"]["thumbnails"]["high"]["url"]

        statisticsResponse = youtube.videos().list(
            id=videoId,
            part="statistics"
        ).execute()

        statistics = statisticsResponse["items"]

        for statistic in statistics:
            views = statistic["statistics"]["viewCount"]

        videoData = {
            "Position": position,
            "Title": title,
            "Number": number,
            "URL": URL,
            "Date": fullDate,
            "Description": description,
            "Thumbnail": thumbnail,
            "Views": views
        }

        if title[:22] == "Joe Rogan Experience #":
            videoData["Category"] = "Interview"

        elif title[:41] == "Joe Rogan Experience - Fight Companion - ":
            videoData["Category"] = "Fight Companion"

        elif title[:14] == "JRE MMA Show #":
            videoData["Category"] = "MMA Show"

        elif title[-11:] == " - JRE Toon" or title[-12:] == " - JRE Toons":
            videoData["Category"] = "Toon"

        elif title[:27] == "Joe Rogan Experience Vlog #":
            videoData["Category"] = "Vlog"

        elif title[:19] == "Best of the Week - ":
            videoData["Category"] = "Best of the Week"

        elif title[:32] == "Joe Rogan Questions Everything #":
            videoData["Category"] = "Joe Questions Everything"

        elif title[-15:] == " Year in Review":
            videoData["Category"] = "Year Review"

        elif "(from" in title:
            videoData["Category"] = "Clip"

        else:
            videoData["Category"] = "Other"

        videos.append(videoData)

    return videos

def getFilteredVideos(videos, guest="", category="", sort="Date", order="ascending"):
    return sorted(
        [video for video in videos if guest in video["Title"] and (video["Category"] == category or category == "All")],
        key=lambda i: i[sort],
        reverse=False if order == "ascending" else True
    )
