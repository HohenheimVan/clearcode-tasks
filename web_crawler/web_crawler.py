import re
import requests
from urllib3.util import parse_url
from pprint import pprint
from urllib.parse import urljoin


def generate_links(url, all_links):
    """
    Generate all internal links
    :param url: base url
    :param all_links: all links from <a href> tags
    :return: internal links
    """

    internal_links = []
    parsed_url = parse_url(url)
    host = parsed_url.host

    for link in all_links:
        parsed_link = parse_url(link)

        # check if link is external
        if parsed_link.host != host and parsed_link.host is not None:
            continue
        else:
            validated_link = urljoin(url, link)
            internal_links.append(validated_link)
    return internal_links


def generate_dictionary(url, dictionary):
    """
    Generate dictionary with url, title and internal links
    :param url: base url
    :param dictionary: dictionary to store new data
    :return: updated dictionary
    """

    # connect to url and get html as a string
    connect = requests.get(url)
    html = connect.text
    all_links = re.findall('<a href="(.*?)"', html)  # get all links from <a href> tags
    title = re.findall('<title>(.*?)<', html)  # get title from <title> tag
    internal_links = generate_links(url, all_links)
    single_url_dict = {url: {'title': title[0], 'links': set(internal_links)}}

    # update main dictionary with single_url_dict items
    dictionary.update(single_url_dict)

    for link in internal_links:
        # check if link is a key in dict
        try:
            dictionary[link]
        except KeyError:
            generate_dictionary(link, dictionary)
    return dictionary


def site_map(url):
    """
    Print site map as dictionary
    :param url: base url
    :return: None
    """
    empty_dict = {}
    dictionary = generate_dictionary(url, empty_dict)
    pprint(dictionary)
    return dictionary


if __name__ == '__main__':
    site_map('http://0.0.0.0:8000/')
