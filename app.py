import streamlit as st
from transformers import pipeline
import google.generativeai as genai
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import func
import news_scraper
import requests
from bs4 import BeautifulSoup
import json

#

# S E T U P

#

# TODO: deploy  

fin_data = ""
pipe = pipeline(
    "text-classification",
    model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
)
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=API_KEY)
fig = plt.figure(figsize=(4, 4))


st.title("Stock Analysis and Prediction")


#  FIN INDICATOR CHARTS AND MODELS
stock_name = st.text_input(label="enter the ticker name")
# news_scraper
history = yf.download(stock_name, start="2023-01-01")
stck = yf.Ticker(stock_name)

dict = stck.info
# st.write(dict)
df = pd.DataFrame.from_dict(dict, orient="index")
df = df.reset_index()
df_str = df.to_string()
st.write(df_str)
keywords = [stock_name, "finance", "news news news"]
news_scraper.perform_search(keywords)

with open("results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

text_descriptions = ""
for frame in data:

    text_descriptions += "Title: " + frame["Title"]
    text_descriptions += "  " + (frame["Description"])

st.write(text_descriptions)
# SENTIMENT TRACKER
# TODO : CONNECT THE SCRAPER TO THE SENTIMENT PIPELINE
output_sentiment = pipe(text_descriptions)
st.write(output_sentiment)

prompt = f"You are a financial analyst, given relevant data provide only the pros and cons of the stock provide a buy reccomendation on a scale of 1 to 10. This is the financial data {df_str} . Consider the following news : {text_descriptions}, also here is a sentiment score of the recent news{output_sentiment}."


# GEMINI API RESPONSE CODE
response = model.generate_content(prompt)
st.write(response.text)


# st.line_chart(history["Close"])
fig1 = func.plot_column(history, "Close")
st.pyplot(fig1)
st.write("% Change")
fig2 = func.plot_column(history, "Volume")
st.line_chart(history["Close"].pct_change())
st.pyplot(fig2)

