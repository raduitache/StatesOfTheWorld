import re

import bs4
from tools.hlp import beautiful_strip, strip_citations


def parse_capital_text(item: bs4.Tag) -> str:
    """Parses the particular item in which a capital name is, extracts and returns it.
    It takes up the text up to the first br tag, since from that point forward the text represents coordinates of the
    cities.
    From the resulting string, remove the citations, which are between square brackets. Since they are all one after
    the other and they are the only things within square brackets, we can just remove everything between an open and
    a closed bracket.
    """
    capital = ''
    for elem in item.find_all():
        if elem.name == 'br':
            break
        capital += elem.text
    capital = strip_citations(capital)
    return capital


def parse_languages_text(item: bs4.Tag) -> list[str]:

    # For the incredible cases of Pakistan and the countries with languages split by commas:
    languages = re.split(',|\u2022', beautiful_strip(item.text))
    if len(languages) > 1:
        languages = [beautiful_strip(language) for language in languages if beautiful_strip(language) != '']
        # Amazing case for Luxembourg:

        return ['Luxembourgish' if language.find('Luxembourgish') != -1 else language for language in languages]

    languages = []
    language = ''
    found_one = False
    for elem in item.descendants:
        if elem.name == 'br' or elem.name == 'small':
            language = beautiful_strip(language)
            found_one = True
            if language != '':
                languages.append(language)
            language = ''
        else:
            if isinstance(elem, bs4.NavigableString):
                language += elem
    language = beautiful_strip(language)
    if language != '':
        languages.append(language)

    return languages