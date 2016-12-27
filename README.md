# html_wrapper

html_wrapper implements a small subset of the BeautifulSoup API that I use. It's anywhere from 10x-100x faster than bs4.


## Installation
`pip3 install html_wrapper`


## Example
Faster to instantiate and parse HTML. Suits my needs.

```
In [1]: import bs4

In [2]: import html_wrapper

In [3]: %timeit html_wrapper.HtmlWrapper("<html><body><p>hi</p></body></html>").text
10000 loops, best of 3: 20.4 µs per loop

In [4]: %timeit bs4.BeautifulSoup("<html><body><p>hi</p></body></html>", "lxml").text
1000 loops, best of 3: 232 µs per loop

```


## License
See `LICENSE`
