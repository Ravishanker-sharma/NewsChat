# 🗞️NewsChat

This project is a simple AI-powered desktop application that delivers the latest news summaries in conversational Hindi with speech output.

It uses **real-time web scraping**, **Gemini Pro (Google Generative AI)**, and **text-to-speech** in Hindi to provide an interactive experience for users who want news updates in simple Hinglish.

---

## 🧠 Features

- 🔍 Fetches news based on user's query using Yahoo search engine results.
- 🧹 Scrapes content from the top links using a general-purpose smart scraper.
- 🤖 Uses Google Gemini 2.0 Flash to:
  - Summarize the news article in English.
  - Translate it into **simplified, conversational Hindi**.
- 🔊 Plays the translated news using Hindi text-to-speech.
- 🖥️ Built with a modern GUI using `customtkinter`.

---

## 🛠️ Requirements

Install the required packages using:

```bash
pip install -r requirements.txt
requirements.txt
nginx
Copy
Edit
beautifulsoup4
requests
gtts
pygame
pydub
customtkinter
langchain
langchain-google-genai
```
⚠️ ffmpeg must be installed for pydub to work with audio.


## Working
RCB IPL 2025 news
And the assistant will:

Scrape latest articles

Summarize in English

Translate to Hindi

Speak the summary out loud

📁 Project Structure
```
├── NewsChat.py              # Main application (GUI + logic)
├── hinditexttospeach.py     # Hindi text-to-speech module
├── genralscraper.py         # Web scraper (uses Yahoo search)
├── yahoosearchengine.py     # Yahoo search result parser
🔗 For detailed explanation of the yahoosearchengine.py and genralscraper.py, refer to the Scraper Repo
```
📌 Notes
Make sure you have a valid Google Gemini API key to use in NewsChat.py.

Use headphones or speakers to hear the audio output.

Hindi output is optimized for natural speech, not formal writing.

💡 Example
```
You: "Punjab Kings IPL news 2025"
AI: (Summarizes in English and then translates)
Hindi (Spoken): "Punjab Kings ne kal ka match jeet liya. Unke player ne last over mein 3 chhakka maara!"
```
🧑‍💻 Author
Made with ❤️ by Ravishanker Sharma
Feel free to fork or star ⭐ if you find it useful!








