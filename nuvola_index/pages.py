from io import BytesIO

import markdown
import markdown.inlinepatterns
import markdown.util
from markdown.util import etree


class SpanWithClassPattern(markdown.inlinepatterns.Pattern):
    PATTERN = r'\{\.\s+([-a-zA-Z_ ]+)\}'

    def handleMatch(self, m):
        elm = markdown.util.etree.Element('span')
        elm.attrib['class'] = m.group(2)
        return elm


class MarkdownPage:
    def __init__(self, path: str):
        self.path = path
        self.markdown = markdown.Markdown(
                extensions=[
                    'meta',
                    'sane_lists',
                    'footnotes(PLACE_MARKER=$FOOTNOTES$)',
                    'fenced_code',
                    'codehilite',
                    'def_list',
                    'attr_list',
                    'abbr',
                    'admonition',
                    'nuvola_index.md_bootstrap',
                ],
                lazy_ol=False)
        self.markdown.inlinePatterns.add('spanclass', SpanWithClassPattern(SpanWithClassPattern.PATTERN), '_end')
        self.body = None
        self.metadata = None
        self.references = None

    def process(self):
        with open(self.path) as fh:
            data = fh.read()
        md = self.markdown
        self.body = md.convert(data)
        self.metadata = m = {}
        try:
            for key, val in md.Meta.items():
                m[key] = " ".join(val)
        except AttributeError:
            pass
        self.references = md.references


class HtmlPage:
    def __init__(self, path: str):
        self.path = path
        self.body = None
        self.metadata = None

    def process(self):
        self.metadata = meta = {}
        with open(self.path) as fh:
            data = fh.read()

        tree = etree.fromstring(data)
        assert tree.tag == 'html'
        head = tree.find('head')
        if head:
            title = head.find('title')
            if title is not None:
                meta['title'] = title.text
            for elm in head.iter('meta'):
                meta[elm.attrib['name']] = elm.attrib['content']
        body: etree.Element = tree.find('body')
        assert body
        tree.remove(body)
        tree = etree.ElementTree(body)
        buffer = BytesIO()
        tree.write(buffer, encoding='utf-8', xml_declaration=False)
        self.body = buffer.getvalue().decode('utf-8')


