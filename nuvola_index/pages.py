import markdown
import markdown.inlinepatterns
import markdown.util


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
