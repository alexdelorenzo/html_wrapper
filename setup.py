from setuptools import setup


setup(name="html_wrapper",
      version="0.2.2",
      description="HTML parser with an lxml backend. Implements a subset of BeautifulSoup API and is an order of magnitude faster",
      url="https://github.com/thismachinechills/html_wrapper",
      author="thismachinechills (Alex)",
      license="AGPL 3.0",
      packages=['html_wrapper'],
      zip_safe=True,
      install_requires=["lxml"],
      keywords="html parser wrapper beautifulsoup bs4 lxml xml html fast xpath".split(),
      )
