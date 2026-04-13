import subprocess

def get_ai_response(message):
    """Get intelligent response using Ollama"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", message],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8"
        )
        
        response = result.stdout.strip()
        
        if not response:
            return "I didn't get a response. Make sure Ollama is running."
        
        return response
        
    except FileNotFoundError:
        return "Ollama is not installed. Download from ollama.ai"
    except subprocess.TimeoutExpired:
        return "I'm thinking too long. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"