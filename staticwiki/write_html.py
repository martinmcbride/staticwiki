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


def create_link(path):
    return '/' + path + '/'


def create_toc(page, pages):
    if not page.series:
        return '', '', ''

    contents = []
    for p in pages:
        if p.series == page.series:
            contents.append((p.shorttitle, p.series_weight, p.path, p.heading))

    contents.sort(key=lambda x: x[1])
    current_page_index = -1

    out = '<section class="sidebar-module"><h4>' + page.series + '</h4><ol class="list-unstyled">'
    for i, p in enumerate(contents):
        shorttitle, series_weight, path, heading = p
        html_path = create_link(path)
        if page.path!=path:
            if heading:
                out += '<li><a href="' + html_path + '">' + shorttitle + '</a></li>'
            else:
                out += '<li><a href="' + html_path + '"> - ' + shorttitle + '</a></li>'
        else:
            current_page_index = i
            if heading:
                out += '<li>' + shorttitle + '</li>'
            else:
                out += '<li> - ' + shorttitle + '</li>'
    out += '</ol></section>'

    prev = ''
    next = ''
    if current_page_index > 0:
        prev = '<a href="' + create_link(contents[current_page_index-1][2]) + '"><button type="button" class="btn btn-primary">Previous</button></a>'
    if 0 <= current_page_index < (len(contents) - 1):
        next = '<a href="' + create_link(contents[current_page_index + 1][2]) + '"><button type="button" class="btn btn-primary float-right">Next</button></a>'
    return out, prev, next

def create_prev_next(prev, next):
    if not prev and not next:
        return ''
    return prev + '' + next

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

    toc, prev, next = create_toc(page, pages)

    prevnext = create_prev_next(prev, next)

    # Substitute page values
    params = dict(title=page.title, content=page.content, author=author, toc=toc, tags=tags, categories=categories, prevnext=prevnext)
    html = pystache.render(template, params)

    directory, html_path = create_url(base, page)
    os.makedirs(directory, exist_ok=True)
    with open(html_path, 'w') as outfile:
        outfile.write(html)
