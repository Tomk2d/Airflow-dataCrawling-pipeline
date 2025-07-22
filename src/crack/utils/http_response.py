import requests
from typing import Optional
import logging

class HttpResponse:
    def __init__(self, url: str, headers: Optional[dict] = None):
        self.url = url
        self.headers = headers if headers is not None else {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.logger = logging.getLogger(__name__)

    def get(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[HttpResponse Error] : {e} \n")
            return None 