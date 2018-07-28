import re
import textwrap
from html import escape

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from markdown.util import etree, STX, ETX


RE = re.compile(r'(^|\n)(<bootstrap>.*?</bootstrap>\s*?)(\n|$)', re.DOTALL)
PLACEHOLDER = STX + "bs4stsh:%s" + ETX
PLACEHOLDER_RE = re.compile(PLACEHOLDER % r'([0-9]+)')


def dedent(text, unindent=None):
    if '\n' in text:
        return textwrap.dedent(unindent + text if unindent else text)
    return text


class Stash(list):
    def store(self, data):
        index = len(self)
        self.append(data)
        return PLACEHOLDER % index

    def reset(self):
        self.clear()


class BootstrapExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.parser.blockprocessors.add('bootstrap', BootstrapProcessor(md), '_begin')
        md.preprocessors.add('bootstrap', BootstrapPreprocessor(md), '<html_block')


class BootstrapPreprocessor(Preprocessor):
    def run(self, lines):
        try:
            stash = self.markdown.bootstrap_stash
            stash.reset()
        except AttributeError:
            stash = Stash()
            self.markdown.bootstrap_stash = stash

        def replace(m):
            return (m.group(1) or '') + stash.store(m.group(2)) + (m.group(3) or '')

        text = "\n".join(lines)
        text = RE.sub(replace, text)
        return text.split("\n")


class BootstrapProcessor(BlockProcessor):
    def __init__(self, md):
        super().__init__(md.parser)
        self.md = md

    def test(self, parent, block):
        return PLACEHOLDER_RE.search(block)

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = PLACEHOLDER_RE.search(block)
        if m:
            index = int(m.group(1))
            block = self.md.bootstrap_stash[index]
            try:
                tree = etree.fromstring(block)

            except etree.ParseError as e:
                pre = etree.SubElement(parent, 'pre')
                pre.text = f'{e}\n{escape(block)}'
            else:
                self._parse(parent, tree)
        else:
            self.parser.parseChunk(sibling, block)

    def _parse(self, parent: etree.Element, tree: etree.Element):
        for child in tree:
            parse = getattr(self, f'_parse_{child.tag}')
            parse(parent, child)

    def _parse_accordion(self, parent: etree.Element, accordion: etree.Element):
        attrib = accordion.attrib
        if 'class' in attrib:
            attrib['class'] = 'accordion ' + attrib['class']
        id_accordion = attrib['id']
        div = etree.SubElement(parent, 'div', attrib)
        for n, entry in enumerate(accordion):
            show = entry.get('show', 'default')
            visible = {
                'true': True,
                'false': False,
                'default': n == 0,
            }[show]
            id_header = f'{id_accordion}-h{n}'
            id_body = f'{id_accordion}-b{n}'
            assert entry.tag == 'entry'
            header = None
            body = None
            for child in entry:
                if child.tag == 'header':
                    header = child
                elif child.tag == 'body':
                    body = child
                else:
                    raise ValueError(child)
            assert header is not None and body is not None, (header, body)
            entry_class = entry.get('class')
            card = etree.SubElement(div, 'div', {'class': 'card ' + entry_class if entry_class else 'card'})
            header_class = header.get('class')
            card_header = etree.SubElement(card, 'div', {
                'class': 'card-header py-1 ' + (f' {header_class}' if header_class else ''),
                'id': id_header,
            })
            h5 = etree.SubElement(card_header, 'h5', {'class': 'my-0'})
            button = etree.SubElement(h5, 'button', {
                'class': 'btn btn-link font-weight-bold my-0',
                'type': 'button',
                'data-toggle': 'collapse',
                'data-target': '#' + id_body,
                'aria-expanded': 'true' if visible else 'false',
                'aria-controls': id_body,
            })
            dummy = etree.Element('div')
            self.parser.parseChunk(dummy, dedent(header.text, '  '))
            p = dummy[0]
            assert p.tag == 'p', p
            button.text = p.text
            button.tail = p.tail
            children = list(p)
            for child in children:
                p.remove(child)
                button.append(child)
            collapse = etree.SubElement(card, 'div', {
                'class': 'collapse show' if visible else 'collapse',
                'id': id_body,
                'aria-labelledby': id_header,
                'data-parent': '#' + id_accordion,
            })
            card_body = etree.SubElement(collapse, 'div', {'class': 'card-body'})
            self.parser.parseChunk(card_body, dedent(body.text, '  '))


# noinspection PyPep8Naming
def makeExtension(**kwargs):
    return BootstrapExtension(**kwargs)
