from googleapiclient.discovery import build
from textblob import TextBlob
import nltk


def fetch_comments(api_key, video_id):
    """
    Using the YT API to scrape comments
    :param api_key:
    :param video_id:
    :return:
    """
    resource = build('youtube', 'v3', developerKey=api_key)
    request = resource.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=15,
        order="relevance"
    )
    response = request.execute()
    comments = []
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
    return comments


def analyze_sentiment(comments):
    """
    Here we take the comments and put it together with the polarity and
    "subjectivity"
    :param comments:
    :return: sentiments
    """
    sentiments = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiment = blob.sentiment
        sentiments.append((comment, sentiment.polarity, sentiment.subjectivity))
    return sentiments


def fetch_video_likes(api_key, video_id):
    resource = build('youtube', 'v3', developerKey=api_key)
    request = resource.videos().list(
        part="statistics",
        id=video_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        return int(response['items'][0]['statistics']['likeCount'])
    return 0
