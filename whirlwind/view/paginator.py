from whirlwind.core.log import Log
from math import ceil


class Paginator(object):

    def __init__(self, collection, page_number=1, limit=20, total=-1):
        self.collection = collection
        self.page_number = int(page_number)
        self.limit = int(limit)
        self.total = int(total)

    @property
    def page(self):
        start = (self.page_number - 1) * self.limit
        end = start + self.limit
        try:
            return self.collection[start:end]
        except Exception as detail:
            Log.warning(detail)
            return []

    @property
    def current_page(self):
        return self.page_number

    @property
    def page_count(self):
        if self.total != -1:
            pages = int(ceil((0.0 + self.total) / self.limit))
            return pages
        else:
            return None

    @property
    def has_previous(self):
        return True if (self.page_number > 1) else False

    @property
    def has_next(self):
        return True if (self.current_page < self.page_count) else False

    @property
    def previous_page(self):
        if self.has_previous:
            return self.page_number - 1

    @property
    def next_page(self):
        if self.has_next:
            return self.page_number + 1

    def previous_page_link(self, request):
        return self.__build_url(self.previous_page, request.full_url())

    def next_page_link(self, request):
        return self.__build_url(self.next_page, request.full_url())

    def __build_url(self, page_num, url):
        import re

        #check if there is a query string
        if url.find('?') != -1:
            if re.search(r'page=\d', url) != None:
                page_str = "page=%d" % page_num
                return re.sub(r'page=\d+', page_str, url)
            else:
                return "%s&page=%d" % (url, page_num)

        else:
            return "%s?page=%d" % (url, page_num)
