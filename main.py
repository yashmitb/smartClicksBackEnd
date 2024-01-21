import whisper
from transformers import pipeline
import math
from dotenv import load_dotenv
import json


# Transcript to sumamry
def returnTranscript(mp3file, model):
    model = whisper.load_model(model)
    result = model.transcribe(mp3file)
    result = result["text"]
    resultSegemnts = math.floor(len(result) / 1000)
    resultList = []
    for i in range(1, resultSegemnts):
        resultList.append(result[: i * 1000].strip())
    return resultList


def returnSummary(summaryType, transcript):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    lent = []
    if summaryType == "short":
        lent = [50, 100]
    if summaryType == "long":
        lent = [100, 200]
    summaryParas = []
    for i in range(0, len(transcript)):
        summary = summarizer(transcript[i], max_length=lent[1], min_length=lent[0])
        summaryParas.append(summary)
    big_summary = ""
    for i in range(0, len(summaryParas)):
        print(i)
        big_summary = big_summary + summaryParas[i][0]["summary_text"]
    return big_summary


transcript = returnTranscript("howToGrammer.mp3", "base")
summary = returnSummary("long", transcript)
# summary = """The typical approach is to write the larger multi-digit number on top. And then you would write the smaller single digit number below that. And since it's in the ones place to 7, you would put it in the those place columns. So for example, if I'm taking those two ones and I'm multiplying it times 7, well, that's going to be 14 ones. Well, there's no digit for 14. I can only put 14. So right below that two, then you'd write the multiplication symbol. All right, I'm just going to take each of these places and multiply it by the 7.The typical approach is to write the larger multi-digit number on top. And then you would write the smaller single digit number below that. And the way you think about it is, all right, I'm just going to take each of these places and multiply it by the 7. So for example, if I'm taking those two ones and I'm multiplying it times 7, well, that's going to be 14 ones. But then you move over to the 10s place. You say, hey, what's 9, 10s, time 7? Well, 9 times 7 is 63. And so you can stick that right over there.Think about how we might multiply 592 times 7. The typical approach is you would write the larger multi-digit number on top. The smaller single digit number would be below that. And the way you think about it is, all right, I%27m just going to take each of these places and multiply it by the 7. It%27s the same as saying, hey, 9 times 7 is 63 plus 1 is 64, right? The 4 and carry the 6. But hopefully you understand what we mean by carrying."""
print("\nSummary: ")
print(summary)
print("\n")
import requests, json


url = (
    "https://worker-solitary-bush-d345.yashmitb07.workers.dev/summarize"
    + 'what concept is this tryign to teach in 5 words  " '
    + summary
    + ' " '
)

response = requests.get(url)
concept = json.loads(response.text)
concept = concept[0]["response"]["response"]

if len(concept) <= 10:
    url1 = (
        'https://worker-solitary-bush-d345.yashmitb07.workers.dev/generate 2 MCQ question based on this concept"'
        + summary
        + ' " '
    )
else:
    url1 = (
        'https://worker-solitary-bush-d345.yashmitb07.workers.dev/generate 2 MCQ question based on this concept"'
        + concept
        + ' " '
    )


response1 = requests.get(url1)
question = json.loads(response1.text)
question = question[0]["response"]["response"]
print(question)
