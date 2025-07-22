from src.crack.utils.http_response import HttpResponse
import time
import logging

logger = logging.getLogger(__name__)

def get_characters(page_id: str):
    resource_url = get_resource_url(page_id)

    if resource_url is None:
        return

    url = "https://contents-api.wrtn.ai/character/" + resource_url

    try:
        response = HttpResponse(url).get()
    except Exception as e:
        print(f"Error getting characters: {e}")
        return None

    if response is None:
        return

    characters = response.get("data", {}).get("characters", [])

    next_cursor = response.get("data", {}).get("nextCursor")
    
    while next_cursor:
        # time.sleep(0.5)
        
        next_page_url = url + "&cursor=" + response.get("data", {}).get("nextCursor") + "&limit=30"
        response = HttpResponse(next_page_url).get()
        
        if response is None:
            return None

        next_characters = response.get("data", {}).get("characters", [])
        characters.extend(next_characters)

        next_cursor = response.get("data", {}).get("nextCursor")
    
    logger.info(f"Page ID: {page_id} success to crawl {len(characters)} characters")
    return characters

def get_resource_url(page_id: str):
    url = "https://contents-api.wrtn.ai/crack-bff/pages/" + page_id + "/web"
    
    response = HttpResponse(url).get()

    if response is None:
        return 

    sections = response.get("data", {}).get("sections", [])
    resource_url = sections[len(sections) - 1].get("defaultSort", {}).get("resourceUrl")
    
    return resource_url 