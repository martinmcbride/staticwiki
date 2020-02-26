# Author:  Martin McBride
# Created: 2020-02-15
# Copyright (c) 2020, Martin McBride
# License: MIT

import os
import os.path
from pathlib import Path
import pystache
from create_tag_pages import create_tag_link, create_tag_linkname
from create_category_pages import create_category_link, create_category_linkname

def create_url(base, page):
    directory = os.path.join(base, page.path)
    html_name = 'index.html'
    html_path = os.path.join(directory, html_name)
    return directory, html_path


def create_link(page):
    return '/' + page.path + '/'


def create_toc(page, pages):
    if not page.series:
        return ''

    contents = []
    for p in pages:
        if p.series == page.series:
            html_path = create_link(p)
            contents.append((p.shorttitle, p.series_weight, html_path, p.heading))

    contents.sort(key=lambda x: x[1])

    out = '<section class="sidebar-module"><h4>' + page.series + '</h4><ol class="list-unstyled">'
    for shorttitle, series_weight, path, heading in contents:
        if heading:
            out += '<li><a href="' + path + '">' + shorttitle + '</a></li>'
        else:
            out += '<li><a href="' + path + '"> - ' + shorttitle + '</a></li>'
    out += '</ol></section>'
    return out


def write_html(template, base, page, pages):

    author = ''
    if page.author or page.date:
        author = '<br>' + ', '.join((page.author, str(page.date)))

    tags = ''
    if page.tags:
        tags = '<br>Tags'
        for tag in page.tags:
            link = create_tag_link(create_tag_linkname(tag))
            tags += ' <a href="' + link + '"><span class="badge badge-secondary">' + tag + '</span></a>'

    categories = ''
    if page.categories:
        categories = '<br>Categories'
        for category in page.categories:
            link = create_category_link(create_category_linkname(category))
            categories += ' <a href="' + link + '"><span class="badge badge-secondary">' + category + '</span></a>'

    toc = create_toc(page, pages)

    # Substitute page values
    params = dict(title=page.title, content=page.content, author=author, toc=toc, tags=tags, categories = categories)
    html = pystache.render(template, params)

    directory, html_path = create_url(base, page)
    os.makedirs(directory, exist_ok=True)
    with open(html_path, 'w') as outfile:
        outfile.write(html)
