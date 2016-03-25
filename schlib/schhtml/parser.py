from lxml import etree

class Parser:
    def __init__(self):
        self._tree = None
        self._cur_elem = None

    def get_starttag_text(self):
        if self._cur_elem:
            ret = ""
            for key, value in self._cur_elem.items():
                if value:
                    ret = ret + "%s=\"%s\" " % (key, value)
                else:
                    ret = ret + key + " "
            return "<%s %s>" % (self._cur_elem.tag, ret[0:-1])
        return ""

    def handle_starttag(self, tag, attrib):
        pass

    def handle_data(self, txt):
        pass

    def handle_endtag(self, tag):
        pass

    def _crawl_tree(self, tree):
        self._cur_elem = tree
        if type(tree.tag) is str:
            self.handle_starttag(tree.tag.lower(), tree.attrib)
            if tree.text:
                self.handle_data(tree.text)
            for node in tree:
                self._crawl_tree(node)
            self.handle_endtag(tree.tag)
        if tree.tail:
            self.handle_data(tree.tail)

    def init(self, html_txt):
        self._tree = etree.HTML(html_txt)

    def feed(self, html_txt):
        self.init(html_txt)
        self._crawl_tree(self._tree)

    def close(self):
        self._tree = None


def tostring(elem):
    return etree.tostring(elem,encoding='unicode', method="html", pretty_print=True)


def content_tostring(elem):
    tab = []
    if elem.text:
        tab.append(elem.text)
    for pos in elem:
        tab.append(tostring(pos))
    if elem.tail:
        tab.append(elem.tail)
    return "".join(tab)
