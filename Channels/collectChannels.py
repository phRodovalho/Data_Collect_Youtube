# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import googleapiclient.discovery


def processChannelListResponse(response):
    '''
    https://developers.google.com/youtube/v3/docs/channels#resource
    '''
    channelinfo = {}
    for i, item in enumerate(response['items']):

        channel_id = ''
        channel_defaultLanguage = ''
        channel_country = ''
        channel_title = ''
        channel_description = ''
        channel_publishedAt = ''
        channel_viewCount = ''
        channel_subscriberCount = ''
        channel_videoCount = ''
        channel_topicIds = []
        channel_topicCategories = []
        channel_madeForKids = False
        channel_selfDeclaredMadeForKids = False

        channel_item = item
        channel_id = channel_item['id']
        if 'defaultLanguage' in channel_item:
            channel_defaultLanguage = channel_item['defaultLanguage']
        if 'country' in channel_item:
            channel_country = channel_item['country']
        if 'snippet' in channel_item:
            snippet = channel_item['snippet']
            channel_title = snippet['title']
            channel_description = snippet['description']
            channel_publishedAt = snippet['publishedAt']
        if 'statistics' in channel_item:
            statistics = channel_item['statistics']
            channel_viewCount = statistics['viewCount']
            channel_subscriberCount = statistics['subscriberCount']
            channel_videoCount = statistics['videoCount']
        if 'topicDetails' in channel_item:
            topicDetails = channel_item['topicDetails']
            channel_topicIds = topicDetails['topicIds']
            channel_topicCategories = topicDetails['topicCategories']
        if 'status' in channel_item:
            status = channel_item['status']
            channel_madeForKids = status['madeForKids']
            channel_selfDeclaredMadeForKids = status['selfDeclaredMadeForKids']

        print('Id:', channel_id)
        print('Default language:', channel_defaultLanguage)
        print('Country:', channel_country)
        print('Title:', channel_title)
        print('Description:', channel_description)
        print('PublishedAt:', channel_publishedAt)
        print('ViewCount:', channel_viewCount)
        print('SubscriberCount:', channel_subscriberCount)
        print('VideoCount:', channel_videoCount)
        print('TopicIds:', channel_topicIds)
        print('TopicCategories:', channel_topicCategories)
        print('Made for kids:', channel_madeForKids)
        print('Self declared for kids:', channel_selfDeclaredMadeForKids)

        channelinfo[i] = {
            'Id': channel_id,
            'Default language': channel_defaultLanguage,
            'Country': channel_country,
            'Title': channel_title,
            'Description': channel_description,
            'PublishedAt': channel_publishedAt,
            'ViewCount': channel_viewCount,
            'SubscriberCount': channel_subscriberCount,
            'VideoCount': channel_videoCount,
            'TopicIds': channel_topicIds,
            'TopicCategories': channel_topicCategories,
            'Made for kids': channel_madeForKids,
            'Self declared for kids': channel_selfDeclaredMadeForKids
        }

    exportjson(channelinfo)


def exportjson(channelinfo):
    channelj = json.dumps(channelinfo, indent=4)
    with open("channels.json", "w") as outfile:
        outfile.write(channelj)


def processChannelSubscriptionListResponse(response):
    '''
    https://developers.google.com/youtube/v3/docs/subscriptions
    '''

    for i, item in enumerate(response['items']):

        subscription_id = ''
        subscription_publishedAt = ''
        subscription_channelTitle = ''
        subscription_title = ''
        subscription_description = ''
        subscription_kind = ''
        subscription_channelId = ''

        print('==================================================')
        print('[subscription item]')
        subscription = item
        subscription_id = subscription['id']
        if 'snippet' in subscription:
            snippet = subscription['snippet']
            subscription_publishedAt = snippet['publishedAt']
            if 'channelTitle' in snippet:
                subscription_channelTitle = snippet['channelTitle']
            subscription_title = snippet['title']
            subscription_description = snippet['description']
            subscription_kind = snippet['resourceId']['kind']
            subscription_channelId = snippet['resourceId']['channelId']

        print('Subscription id:', subscription_id)
        print('Subscription published at:', subscription_publishedAt)
        print('Subscription channel title:', subscription_channelTitle)
        print('Subscription title:', subscription_title)
        print('Subscription description:', subscription_description)
        print('Subscription kind:', subscription_kind)
        print('Subscription channel id:', subscription_channelId)

    if 'nextPageToken' in response:
        return True, response['nextPageToken']

    return False, ''


def getChannelSubscriptionInfo(youtube, idChannel):
    next = True
    nextPageToken = ""
    while(next):
        request = youtube.subscriptions().list(
            part="contentDetails,id,snippet,subscriberSnippet",
            channelId=idChannel,
            pageToken=nextPageToken
        )
        response = request.execute()

        next, nextPageToken = processChannelSubscriptionListResponse(
            response)  # SubscriptionListResponse


def getChannelInfo(youtube, idChannel):
    next = True
    nextPageToken = ""

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics,topicDetails",
        id=idChannel
    )
    response = request.execute()

    processChannelListResponse(response)  # channelListResponse


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCx4LTP04AmYfO67ArGE47HWfVtg27SYZA"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    # https://www.youtube.com/channel/UCH8H3nWKV8hyqO7zQFPHpiw
    getChannelInfo(youtube, 'UCH8H3nWKV8hyqO7zQFPHpiw')
    getChannelSubscriptionInfo(youtube, 'UCAXJUODD9beu3EfwoOHhHUA')


if __name__ == "__main__":
    main()
