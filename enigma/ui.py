import tkinter as tk
import json
import threading
import time

class ChatBotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatBot")
        
        self.message_frame = tk.Frame(self.master, bg="black")
        self.message_frame.pack(expand=True, fill=tk.BOTH)

        self.chat_display = tk.Text(self.message_frame, wrap="word", state=tk.DISABLED, bg="black", fg="white")
        self.chat_display.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.message_frame, command=self.chat_display.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=self.scrollbar.set)

        self.entry_frame = tk.Frame(self.master, bg="black")
        self.entry_frame.pack(expand=True, fill=tk.X)

        self.cmd_label = tk.Label(self.entry_frame, text="cmd:", bg="purple", fg="white")
        self.cmd_label.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        self.user_input = tk.Entry(self.entry_frame, bg="black", fg="white")
        self.user_input.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg="black", fg="yellow")
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        self.history_file = "history.json"

        # Load initial chat history
        self.load_chat_history()

        # Start a thread to check for updates in the chat history file
        self.check_history_thread = threading.Thread(target=self.check_chat_history)
        self.check_history_thread.daemon = True
        self.check_history_thread.start()

    def load_chat_history(self):
        try:
            with open(self.history_file, 'r') as file:
                self.chat_history = json.load(file)
                self.chat_history.reverse()  # Reverse the order of messages
                self.update_chat_display()
        except FileNotFoundError:
            self.chat_history = []

    def update_chat_display(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        for message in self.chat_history:
            for key, value in message.items():
                if "Enigma" in key:
                    color = "green"
                elif "User" in key:
                    color = "red"
                else:
                    color = "white"  # Default color for other messages
                self.chat_display.insert(tk.END, f"{key}: ", ("color",))
                self.chat_display.insert(tk.END, f"{value}\n", (color,))
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if user_message:
            self.chat_history.append({"User said": user_message})
            self.user_input.delete(0, tk.END)
            self.update_chat_display()

    def check_chat_history(self):
        while True:
            time.sleep(1)  # Check every 1 second for updates
            try:
                with open(self.history_file, 'r') as file:
                    new_chat_history = json.load(file)
                    if new_chat_history != self.chat_history:
                        self.chat_history = new_chat_history
                        self.chat_history.reverse()  # Reverse the order of messages
                        self.update_chat_display()
            except FileNotFoundError:
                pass

def main():
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
