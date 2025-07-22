from src.crack.utils.http_response import HttpResponse

def get_collections():
    response = HttpResponse("https://contents-api.wrtn.ai/crack-bff/genre-navigations/web").get()
    
    if response is None:
        return None
    
    collections = response.get("data", {}).get("genreNavigations", [])

    return collections 