import requests
from urllib.parse import urlparse, urlunparse, urljoin


class Page:
    def __init__(self, origin_url, url, cached_status=None):
        """
        Конструктор страницы
        :param origin_url: url страницы, где обнаружена ссылка
        :param url: url
        """
        self.origin_url = origin_url
        self.host = '%s://%s' % (urlparse(url)[0], urlparse(url)[1])
        self.url = url
        self.cached_status = cached_status
        if self.cached_status:
            self.response = None
        else:
            self.response = self.get_response()

    def __str__(self):
        return '%s : %s : %s' % (self.origin_url, self.url, self.status_code)

    def get_response(self):
        try:
            return requests.get(self.url)
        except:
            return None

    @property
    def status_code(self):
        if self.cached_status:
            return self.cached_status
        else:
            if self.response:
                return self.response.status_code
            else:
                return 'INVALID URL'

    @property
    def text(self):
        return self.response.text if self.response else None
