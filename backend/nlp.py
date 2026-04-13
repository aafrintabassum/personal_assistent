import subprocess

def ask_bruno(user_input):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", user_input],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        response = result.stdout.strip()

        if response == "":
            return "Sorry, I didn't understand."

        return response

    except Exception as e:
        return "Error: " + str(e)
