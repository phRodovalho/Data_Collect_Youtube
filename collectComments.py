# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import time
import googleapiclient.discovery
parent_dir = "C:\\Users\\PHELIPE\\Desktop\\UFU\\TCC\\Captura\\Comments"


def processResponse(response, path):

    for i, item in enumerate(response['items']):
        # print(item)
        if 'snippet' in item:
            snippet_item = item['snippet']
            if 'topLevelComment' in snippet_item:
                topLevelComment_snippet_item = snippet_item['topLevelComment']
                if 'snippet' in topLevelComment_snippet_item:
                    commentItem = topLevelComment_snippet_item['snippet']
                    try:
                        userId = str(
                            commentItem["authorChannelId"].get("value"))
                        # userId = str(
                        #    commentItem["authorDisplayName"])
                    except Exception as error:
                        print(error)
                        userId = "UserNotIdentify"

                    pathFileuserId = str(path) + "\\" + userId + ".json"
                    # just print original text
                    # here we have to save every relevant info we will need, considering replies to comments
                    # if file exits, 1 user have 2 or more comments
                    if os.path.exists(pathFileuserId) == True:
                        try:
                            with open(pathFileuserId, "a", encoding="utf-8") as f:
                                json.dump(commentItem, f, indent=4)
                        except OSError as error:
                            print(error)
                    else:
                        try:
                            with open(pathFileuserId, "w", encoding="utf-8") as f:
                                json.dump(commentItem, f, indent=4)
                        except OSError as error:
                            print(error)

    if 'nextPageToken' in response:
        return True, response['nextPageToken']

    return False, ''


def createPathDir(idVideo):
    directory = ("videoId."+idVideo)
    path = os.path.join(parent_dir, directory)
    try:
        os.mkdir(path)
        return path
    except OSError as error:
        print(error)
        return path


def getComments(youtube, idVideo):
    next = True
    nextPageToken = ""
    path = createPathDir(idVideo)
    count = 0
    while(next):
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=idVideo,
            pageToken=nextPageToken
        )
        response = request.execute()
        next, nextPageToken = processResponse(response, path)
        if count == 300:  # MAX COMMENTS 6.000, 300x20
            return False
        else:
            count += 1


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCx4LTP04AmYfO67ArGE47HWfVtg27SYZA"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    # https://www.youtube.com/watch?v=AQiY5jNI-gk&ab_channel=DiaEst%C3%BAdio
    # https://www.youtube.com/watch?v=yjki-9Pthh0&ab_channel=Beyonc%C3%A9VEVO
    # https://www.youtube.com/watch?v=DjGA0zUSu7o&ab_channel=PopRecords
    # https://www.youtube.com/watch?v=M9ZYS_Lt-tw&ab_channel=ChrisMarrin
    # https://www.youtube.com/watch?v=wzOhK0e4TfU&ab_channel=FelipeNeto
    getComments(youtube, 'wzOhK0e4TfU')


if __name__ == "__main__":
    main()
