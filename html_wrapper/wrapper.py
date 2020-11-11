from typing import Union, Dict, AnyStr, Any, Optional, \
    Iterable, Tuple
from functools import lru_cache
from abc import ABC

from lxml.html import HtmlElement, fromstring, tostring
from lxml.etree import XPath


BS4_TYPES = "Tag", "BeautifulSoup"
NO_ATTRS: Dict[str, str] = {}
NO_TEXT = ''


Attrs = Union[str, Dict]


class BeautifulSoupMethods(ABC):
    """
    This is the subset of the BS4 API that is implemented
    """

    def __init__(self, html):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __getitem__(self, item):
        pass

    def __getattr__(self, item):
        pass

    @property
    def text(self) -> str:
        pass

    @property
    def string(self) -> str:
        pass

    def name(self) -> str:
        pass

    def find(self, tag: str, attrs: Attrs = NO_ATTRS, *, _class: str = None, **kwargs) -> Optional['HtmlWrapper']:
        pass

    def find_all(self, tag: str, attrs: Attrs = NO_ATTRS, *, _class: str = None, gen=False, **kwargs) -> 'Wrappers':
        pass


class HtmlWrapper(BeautifulSoupMethods):
    """
    An lxml adapter over a subset of the BeautifulSoup API
    """

    __slots__ = ['html']

    def __init__(self, html):
        if isinstance(html, (str, bytes)):
            self.html = fromstring(html)

        elif isinstance(html, HtmlWrapper):
            self.html = html.html

        elif isinstance(html, HtmlElement):
            self.html = html

        elif isinstance(html, BS4_TYPES):
            self.html = fromstring(str(html))

        else:
            name = str(type(html))
            msg = f"Object of type {name} not compatible with HtmlWrapper"

            raise TypeError(msg)

    def __repr__(self):
        return f'HtmlWrapper: {repr(self.html)}'

    def __str__(self):
        return self.html.text

    def __getitem__(self, item):
        items = self.html.attrib[item]

        if item == 'class':
            items = items.split(' ')

        return items

    def __getattr__(self, item):
        val = self.find(item)

        if val is None:
            if hasattr(self.html, item):
                return getattr(self.html, item)

            else:
                return None

        else:
            return val

    @property
    def text(self) -> str:
        text = self.html.text_content()

        return text if text else NO_TEXT

    @property
    def string(self) -> str:
        return tostring(self.html)

    def name(self) -> str:
        return self.html.tag

    def find(self, tag: str, attrs: Attrs = NO_ATTRS, *, _class: str = None, **kwargs) -> Optional['HtmlWrapper']:
        return find(self.html, tag, attrs, _class=_class, **kwargs)

    def find_all(self, tag: str, attrs: Attrs = NO_ATTRS, *, _class: str = None, gen=False, **kwargs) -> 'Wrappers':
        return find_all(self.html, tag, attrs, _class=_class, gen=gen, **kwargs)


Wrappers = Union[Tuple[HtmlWrapper, ...], Iterable[HtmlWrapper]]


def find(
    html: HtmlElement,
    tag: str,
    attrs: Attrs = NO_ATTRS,
    _class: str = None,
    **kwargs
) -> Optional[HtmlWrapper]:
    if isinstance(attrs, str):
        _class = attrs
        attrs = NO_ATTRS

    elif isinstance(attrs, dict):
        kwargs.update(attrs)

    results = find_all(html, tag, attrs, _class, gen=True, **kwargs)

    return next(results) if results else None


def find_all(
    html: HtmlElement,
    tag: str,
    attrs: Attrs = NO_ATTRS,
    _class: str = None,
    gen: bool = False,
    **kwargs
) -> Wrappers:
    if isinstance(attrs, str):
        _class = attrs
        attrs = NO_ATTRS

    elif isinstance(attrs, dict):
        kwargs.update(attrs)

    xpath = get_xpath(tag, _class, **kwargs)
    elems = xpath(html)

    if not elems:
        return tuple()

    wrapper_map = map(HtmlWrapper, elems)  # returns an iterator

    return wrapper_map if gen else tuple(wrapper_map)


def get_xpath_str(tag: str, _class: str = None, **kwargs) -> str:
    tag_xp = f'.//{tag}'

    if _class:
        kwargs['class'] = _class

    for attr, val in kwargs.items():
        tag_xp += '['
        attr_xp = f'@{attr}'

        if isinstance(val, bool):
            if val:
                tag_xp += attr_xp

            else:
                tag_xp += f'not({attr_xp})'

        elif isinstance(val, (set, list, tuple)):
            for item in val:
                val_xp = f'"{item}", '

            val_xp = val_xp[:-2] if val else ''
            tag_xp += f'contains({attr_xp}, {val_xp})'

        elif isinstance(val, str):
            tag_xp += f'contains({attr_xp}, "{val}")'

        else:
            tag_xp += "{attr_xp}={val}'"

        tag_xp += ']'

    return tag_xp


@lru_cache(maxsize=None)
def get_xpath(tag: str, _class: str = None, **kwargs) -> XPath:
    xpath_str = get_xpath_str(tag, _class, **kwargs)

    return XPath(xpath_str)
