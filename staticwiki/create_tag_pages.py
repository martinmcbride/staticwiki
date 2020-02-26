# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import Page
import os

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
            entries.append((page.title, '/' + page.path + '/'))
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    tagpage = Page(path=os.path.join('tags', name),
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
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for initial in alphabet:
        initial_entries = [e for e in entries if e[0][0].upper()==initial]
        if initial_entries:
            content += '<p><h3>' + initial + '</h3>'
            for t, p in initial_entries:
                content += '<a href="' + p + '"><span class="badge badge-secondary">' + t + '</span></a> '

    initial_entries = [e for e in entries if e[0][0].upper() not in alphabet]
    if initial_entries:
        content += '<p><h3>Other</h3>'
        for t, p in initial_entries:
            content += '<a href="' + p + '"><span class="badge badge-secondary">' + t + '</span></a> '

    tagpage = Page(path='tags/tags',
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

