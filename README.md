# html_wrapper

`html_wrapper` implements a small subset of the `BeautifulSoup4` API. It can be anywhere from 10x-100x faster than `bs4` for some use cases.


## Installation
`python3 -m pip install html_wrapper`


## Example
It's faster to instantiate and parse HTML. Suits my needs.

```
In [1]: from html_wrapper import HtmlWrapper

In [2]: from bs4 import BeautifulSoup

In [3]: from requests import get

In [4]: html = get("https://en.wikipedia.org/wiki/HTML").content

In [5]: %timeit HtmlWrapper(html).text
23.4 ms ± 563 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

In [6]: %timeit BeautifulSoup(html).text
190 ms ± 29.3 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```


## License
See `LICENSE`
