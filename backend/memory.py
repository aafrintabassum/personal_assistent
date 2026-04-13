import json
import os

MEMORY_FILE = "memory.json"

# Only name and birthday
ALLOWED_KEYS = ["name", "birthday"]

def load_memory():
    """Load memory from file"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_memory(memory_store):
    """Save memory to file"""
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory_store, f)
    except:
        pass

# Load existing memory
memory_store = load_memory()

def remember(key, value):
    """Remember only name and birthday"""
    key = key.lower().strip()
    
    # Check if it's allowed
    if key not in ALLOWED_KEYS:
        return f"I can only remember your name or birthday. Say: remember my name is John"
    
    memory_store[key] = value
    save_memory(memory_store)
    return f"I'll remember that your {key} is {value}"

def recall(key):
    """Recall something"""
    key = key.lower().strip()
    
    if key not in ALLOWED_KEYS:
        return "I can only remember name and birthday."
    
    value = memory_store.get(key)
    if value:
        return f"Your {key} is {value}"
    else:
        return f"I don't know your {key}. Say: remember my {key} is [value]"

def get_memory():
    """Get all memory"""
    if memory_store:
        items = [f"{k}: {v}" for k, v in memory_store.items()]
        return "I remember:\n" + "\n".join(items)
    return "I don't remember your name or birthday yet."

# Auto-load on startup
print("Loaded memory:", memory_store)