import tkinter as tk
from tkinter import scrolledtext
from urllib.parse import urlparse, parse_qs
import analysis


def extract_video_id(url):
    """
    extracting ID from the URL
    :param url:
    :return:
    """
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    return None


def calculate_average_sentiment(sentiments):
    """
    calculating the consensus
    :param sentiments:
    :return:
    """

    total_polarity = 0
    total_subjectivity = 0
    for _, polarity, subjectivity in sentiments:
        total_polarity += polarity
        total_subjectivity += subjectivity
    avg_polarity = total_polarity / len(sentiments)
    avg_subjectivity = total_subjectivity / len(sentiments)
    return avg_polarity, avg_subjectivity


def analyze_comments():
    """
    Main function that prints out everything and directly uses the YT API
    :return:
    """
    url = video_id_entry.get()
    video_id = extract_video_id(url)
    comments = analysis.fetch_comments("", video_id) # Your API KEY goes in the ""
    likes = analysis.fetch_video_likes("", video_id)
    sentiments = analysis.analyze_sentiment(comments)

    avg_polarity, avg_subjectivity = calculate_average_sentiment(sentiments)
    general_sentiment = f"Average Polarity: {avg_polarity:.2f}," \
                        f" Average Subjectivity: {avg_subjectivity:.2f}\n"

    comments_text.delete('1.0', tk.END)
    comments_text.insert(tk.END, f"Video Likes: {likes}\n")
    comments_text.insert(tk.END, f"General Sentiment:\n{general_sentiment}\n")

    for comment, polarity, subjectivity in sentiments:
        sentiment_text = f"Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}"
        comments_text.insert(tk.END, f"Comment: {comment}\n{sentiment_text}\n\n")


# GUI Begins Here
root = tk.Tk()
root.title("Watch Worthy?")

tk.Label(root, text="Enter YouTube Video URL:").pack()
video_id_entry = tk.Entry(root)
video_id_entry.pack()

analyze_button = tk.Button(root, text="Analyze Comments", command=analyze_comments)
analyze_button.pack()

comments_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
comments_text.pack()
root.mainloop()
