import webbrowser

def google_search(query: str) -> str:
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for {query}."

def open_website(website: str) -> str:
    # If user just says "YouTube", add correct URL
    if "youtube" in website.lower():
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    elif "." not in website:
        website = f"https://www.{website}.com"
    webbrowser.open(website)
    return f"Opening {website}."
