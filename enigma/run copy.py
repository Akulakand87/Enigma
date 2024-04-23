import threading
import subprocess

def start_assistant():
    subprocess.run(["python", "./control/assistant.py"])

def start_recognition():
    subprocess.run(["python", "./recog/recognition.py"])

def start_ui():
    subprocess.run(["python", "ui.py"])

def main():
    assistant_thread = threading.Thread(target=start_assistant)
    recognition_thread = threading.Thread(target=start_recognition)
    ui_thread = threading.Thread(target=start_ui)

    # Start all threads
    assistant_thread.start()
    recognition_thread.start()
    ui_thread.start()

    # Wait for all threads to complete
    assistant_thread.join()
    recognition_thread.join()
    ui_thread.join()

if __name__ == "__main__":
    main()