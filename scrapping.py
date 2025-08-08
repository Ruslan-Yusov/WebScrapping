from dataclasses import dataclass
from typing import List
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from logger import logger


@dataclass
class ScrappingConfig:
    keyword: List[str]
    site: str


class Scraper:
    def __init__(self, config: ScrappingConfig):
        self.config = config
        options = ChromiumOptions()
        options.add_argument('--headless')
        self.browser = Chrome(
            service=Service(executable_path=ChromeDriverManager().install()),
            options=options
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.browser:
            self.browser.quit()

    def _get_articles_list(self) -> List[str]:
        try:
            self.browser.get(self.config.site)
            articles = self.browser.find_elements(by=By.CSS_SELECTOR, value='article.tm-articles-list__item')
            return [
                article.find_element(by=By.CSS_SELECTOR, value='a.tm-title__link').get_attribute('href')
                for article in articles
            ]
        except NoSuchElementException:
            return []
    @logger(path='get_title')
    def get_title(self) -> List[dict]:
        title_list = []
        for article in self._get_articles_list():
            try:
                self.browser.get(article)
                title = self.browser.find_element(by=By.TAG_NAME, value='h1').text
                
                if self._contains_keyword(title) or self._get_text():
                    title_list.append({
                        'data': self.browser.find_element(
                            by=By.CSS_SELECTOR, 
                            value='div.tm-article-reading-time'
                        ).text,
                        'title': title,
                        'link': article
                    })
            except NoSuchElementException:
                continue
        return title_list

    def _contains_keyword(self, text: str) -> bool:
        return any(keyword in text for keyword in self.config.keyword)

    def _get_text(self) -> bool:
        try:
            paragraphs = self.browser.find_elements(by=By.TAG_NAME, value='p')
            return any(
                any(keyword in p.text for keyword in self.config.keyword)
                for p in paragraphs
            )
        except NoSuchElementException:
            return False
