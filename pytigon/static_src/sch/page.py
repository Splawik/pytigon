class Page:
    def __init__(self, id, page):
        self.id = id
        self.page = page

    def set_href(self, href):
        self.page.attr('_href', href)

    def get_href(self):
        return self.page.attr('_href')


