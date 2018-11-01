from collections import deque
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs
from page import Page


class Spider:
    """Паук"""

    def __init__(self, start_url):
        self.start_page = Page('-', start_url)
        self.current_page = None
        self.visited = {}
        self.pages = []
        self.queue = deque()
        self.queue.append(self.start_page)

    def create_page(self, url):
        if url in self.visited:
            page = Page(self.current_page.url, url, self.visited[url])
        else:
            page = Page(self.current_page.url, url)
        return page

    def get_abs_url(self, url):
        return url if url.startswith('http') else urljoin(self.start_page.host, url)

    def extract_links(self):
        soup = bs(self.current_page.text, 'html.parser')
        links = soup.find_all('a', href=True)
        return [self.get_abs_url(link.attrs['href']) for link in links]

    def get_data(self):
        """Формирует список страниц, помещает внутренние страницы в очередь"""

        if self.current_page.text:
            urls = self.extract_links()
            for url in urls:
                page = self.create_page(url)
                print(page)  # тест
                self.pages.append(page)
                if page.host == self.start_page.host:
                    self.queue.appendleft(page)

    def move(self):
        while self.queue:
            self.current_page = self.queue.popleft()
            if self.current_page.url not in self.visited:
                self.visited[self.current_page.url] = self.current_page.status_code
                self.get_data()

    def start(self):
        self.move()

if __name__ == '__main__':
    start_time = time.time()
    index = 'https://www.raiffeisen.ru/'
    raiff_spider = Spider(index)
    raiff_spider.start()
    print('Execution time: %s seconds' % int(time.time() - start_time))