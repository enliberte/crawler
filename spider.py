from urllib.parse import urlparse
import requests
from urllib.request import urljoin
from collections import deque
import re
from datetime import datetime


class Spider:
    """Кроулер"""

    def __init__(self, start_url, log_file):
        self.start_url = start_url
        self.host = urlparse(self.start_url)[1]
        self.visited = set()
        self.queue = deque()
        self.queue.append(self.start_url)
        self.log_file = open(log_file, 'a')

    def __del__(self):
        self.log_file.close()

    @staticmethod
    def download_page(url):
        try:
            return requests.get(url).text
        except:
            return 'error in the url'

    def extract_links(self, page):
        link_regex = re.compile('<a[^>]+href=["\'](/wiki/.*?)["\']', re.IGNORECASE)
        links = link_regex.findall(page)
        return [urljoin(self.start_url, link) for link in links]

    def get_links(self, page_url):
        page = self.download_page(page_url)
        links = self.extract_links(page)
        return [link for link in links if urlparse(link)[1] == self.host]

    def start(self):
        while self.queue:
            url = self.queue.popleft()
            if url not in self.visited:
                self.visited.add(url)
                links = self.get_links(url)
                self.log_file.write('%s. (%s) %s\n' % (len(self.visited), datetime.today(), url))
                for link in links:
                    self.queue.appendleft(link)

if __name__ == '__main__':
    index_page = 'https://ru.wikipedia.org/wiki/Заглавная страница'
    wiki_spider = Spider(index_page, 'log.txt')
    wiki_spider.start()
