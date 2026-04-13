import requests

def get_weather(city=None):
    try:
        if city:
            url = f"https://wttr.in/{city}?format=j1"
        else:
            url = "https://wttr.in/?format=j1"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp_c = current['temp_C'][0]
            temp_f = current['temp_F'][0]
            condition = current['weatherDesc'][0]['value']
            humidity = current['humidity'][0]
            location = data['nearest_area'][0]['areaName'][0]['value']
            
            return f"Weather in {location}: {temp_c}°C ({temp_f}°F), {condition}. Humidity: {humidity}%"
        
        return "Couldn't fetch weather."
        
    except Exception as e:
        return f"Weather error: {str(e)}"