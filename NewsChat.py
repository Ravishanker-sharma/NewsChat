import customtkinter as ctk
import threading
from genralscraper import get_data
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from hinditexttospeach import speak_summary_streaming , stop_playback

# Optional: if you're using pyttsx3 or similar, make sure stop() works
def stop_sound():
    print("Voice stopped.")
    # Add your voice-stopping logic here, like engine.stop() if using pyttsx3
    stop_playback()

speak_thread = None  # Global thread reference

def run_chat_ui():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    class ChatApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("AI News Assistant")
            self.geometry("600x600")

            self.chat_frame = ctk.CTkFrame(self)
            self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

            self.chat_history = ctk.CTkTextbox(self.chat_frame, wrap="word", font=("Helvetica", 14))
            self.chat_history.pack(padx=10, pady=10, fill="both", expand=True)
            self.chat_history.configure(state="disabled")

            self.bottom_frame = ctk.CTkFrame(self)
            self.bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

            self.entry = ctk.CTkEntry(self.bottom_frame, width=350, height=40, font=("Helvetica", 14))
            self.entry.pack(side="left", padx=(0, 10), pady=10)
            self.entry.bind("<Return>", self.send_message)

            self.send_btn = ctk.CTkButton(self.bottom_frame, text="Send", command=self.send_message)
            self.send_btn.pack(side="left", padx=(0, 10))

            self.stop_btn = ctk.CTkButton(self.bottom_frame, text="Stop Sound", fg_color="red", command=stop_sound)
            self.stop_btn.pack(side="left")

        def send_message(self, event=None):
            user_input = self.entry.get().strip()
            if user_input:
                self.append_chat("You", user_input)
                self.entry.delete(0, "end")
                threading.Thread(target=self.handle_agent, args=(user_input,)).start()

        def handle_agent(self, ask):
            global speak_thread
            try:

                tools = []

                instructions = """You are helpful news assistant who provides the real fact based news on the basis of the content you are given using web scraping.
                Summarize the news and tell the user on the basis of content you have been provided.
                Provide the latest news on the basis of Date. Today date [3 june 2025].
                """

                instructions2 = """
                You will receive a English summary. Your task is to translate it into simple, conversational Hindi, like how normal people speak in real life. Avoid using formal or pure Hindi words. Use simple and common Hindi vocabulary, and include basic English terms like "app", "video", "tool", "update", etc., if they feel natural.

                Only output the translated Hindi sentence.
                Do not use * or something else keep the output simple looking.
                """

                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    api_key="YOUR_API_KEY",
                    temperature=0.5
                )

                agent = initialize_agent(
                    llm=llm,
                    tools=tools,
                    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                    agent_kwargs={"system_message": instructions},
                    verbose=False
                )

                hindi = initialize_agent(
                    llm=llm,
                    tools=tools,
                    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                    agent_kwargs={"system_message": instructions2},
                    verbose=False
                )

                content = get_data(ask)
                data = f"What user asked: {ask}\nDATA: {content}"
                output = agent.invoke(data)
                summary = output["output"]

                self.append_chat("Agent", summary)

                translation = hindi.invoke(f"Convert this into simplified Hinglish : {summary}")["output"]
                translation = str(translation).replace("*","")
                self.append_chat("Agent (Hindi)", translation)

                # Run speak in a thread so it doesn't block UI
                speak_thread = threading.Thread(target=speak_summary_streaming, args=(translation,1.3))
                speak_thread.start()

            except Exception as e:
                self.append_chat("Agent", f"Error: {str(e)}")

        def append_chat(self, sender, message):
            self.chat_history.configure(state="normal")

            tag = "user_tag" if sender == "You" else "agent_tag"

            # Insert tagged sender name
            self.chat_history.insert("end", f"{sender}: ", tag)
            self.chat_history.insert("end", f"{message}\n\n")

            # Only color styling (no font allowed!)
            self.chat_history.tag_config("user_tag", foreground="#1e88e5")
            self.chat_history.tag_config("agent_tag", foreground="#43a047")

            self.chat_history.configure(state="disabled")
            self.chat_history.yview("end")

    app = ChatApp()
    app.mainloop()

if __name__ == "__main__":
    run_chat_ui()
