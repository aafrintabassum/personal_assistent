import subprocess
from voice import speak, listen
from memory import remember, recall
from tasks import open_notepad, open_browser

print("Bruno AI Started (type exit to stop)")


while True:

    user = input("You: ")

    if user.lower() == "exit":
        break


    if "remember" in user:

        parts = user.replace("remember", "").split(" is ")
        key = parts[0].strip()
        value = parts[1].strip()

        remember(key, value)

        reply = "I will remember that"


    elif "what is my" in user:

        key = user.replace("what is my", "").strip()
        reply = recall(key)


    elif "open notepad" in user.lower():

        open_notepad()
        reply = "Opening Notepad"


    elif "open browser" in user.lower():

        open_browser()
        reply = "Opening Browser"


    else:

        result = subprocess.run(
            ["ollama", "run", "llama3", user],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        reply = result.stdout


    print("Bruno:", reply)
    speak(reply)
