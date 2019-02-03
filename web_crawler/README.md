# Web crawler
The function `site_map(url)` takes a site URL as an argument and creates a mapping
of that domain as a Python dictionary.
The mapping contain all the accessible pages within that domain. Every entry consist of:
* key: URL
* value: dictionary with:

  * site title (HTML `<title>` tag)
  * links - set of all target URLs within the domain on the page but without anchor links

App uses requests, re, urllib3 libraries.
