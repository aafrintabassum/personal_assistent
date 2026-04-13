import requests

def get_news():
    try:
        url = "https://feeds.bbci.co.uk/news/rss.xml"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            news = []
            for item in items[:5]:
                title = item.find('title').text
                title = title.replace(' - BBC News', '')
                news.append(f"• {title}")
            
            return "\n".join(news)
        
        return "Couldn't fetch news."
        
    except Exception as e:
        return f"News error: {str(e)}"