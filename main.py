from pprint import pprint
from time import sleep
from typing import List

from scrapping import ScrappingConfig, Scraper

KEYWORDS: List[str] = ['дизайн', 'фото', 'web', 'python']
HABR_URL: str = 'https://habr.com/ru/articles/'

def main() -> None:
    config = ScrappingConfig(KEYWORDS, HABR_URL)
    
    with Scraper(config) as scraper:
        results = scraper.get_title()
        pprint(results)
        sleep(10)

if __name__ == '__main__':
    main()