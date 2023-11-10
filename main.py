import tkinter as tk
from tkinter import scrolledtext
from googleapiclient.discovery import build


def fetch_comments(video_id):
    """
    This function focuses on using relevance to get the top 15 comments of a
    video ID provided by the user.
    :param video_id:
    :return:comments
    """
    api_key = "" # Enter your own API key here to make this work!
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


def scrape_comments():
    video_id = video_id_entry.get()
    comments = fetch_comments(video_id)
    comments_text.delete('1.0', tk.END)
    for comment in comments:
        comments_text.insert(tk.END, comment + "\n\n\n -----")


# Making the GUI here
root = tk.Tk()
root.title("WatchWorthy?")

tk.Label(root, text="Enter YouTube Video ID:").pack()
video_id_entry = tk.Entry(root)
video_id_entry.pack()

scrape_button = tk.Button(root, text="Checking Comments", command=scrape_comments)
scrape_button.pack()

comments_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100,
                                          height=100)
comments_text.pack()

root.mainloop()
