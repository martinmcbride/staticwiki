# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import Page

def create_tag_linkname(tag):
    return 'tag-' + tag.replace(' ', '-')

def create_tag_link(linkname):
    return '/tags/' + linkname + '/'

def create_tag_page(tag, pages):
    title = 'Articles tagged with ' + tag
    name = create_tag_linkname(tag)

    entries = []
    for page in pages:
        if tag in page.tags:
            entries.append((page.title, '/' + page.path + '/' + page.filename + '/'))
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    tagpage = Page(path='tags',
                      filename=name,
                      content=content,
                      title=title,
                      shorttitle=title,
                      author='',
                      date='',
                      categories=[],
                      tags=[],
                      series='',
                      heading='',
                      series_weight=0)
    return tagpage

def create_alltag_page(pages):
    title = 'All tags'
    name = 'tags'

    entry_set = set()
    for page in pages:
        for tag in page.tags:
            entry_set.add((tag, create_tag_link(create_tag_linkname(tag))))

    entries = list(entry_set)
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    tagpage = Page(path='tags',
                      filename=name,
                      content=content,
                      title=title,
                      shorttitle=title,
                      author='',
                      date='',
                      categories=[],
                      tags=[],
                      series='',
                      heading='',
                      series_weight=0)
    return tagpage

def create_all_tags(pages):
    tags = set()
    for page in pages:
        if page.tags:
            for tag in page.tags:
                tags.add(tag)

    tagpages = []
    for tag in tags:
        tagpages.append(create_tag_page(tag, pages))

    alltags = create_alltag_page(pages)
    tagpages.append(alltags)

    return tagpages

