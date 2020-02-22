# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import Page
import os.path

def create_recent_linkname():
    return 'recent'

def create_recent_link(linkname):
    return '/recent/'

def create_recent_page(pages):
    title = 'Recent articles'
    name = create_recent_linkname()

    entries = []
    for page in pages:
        entries.append((page.title, '/' + os.path.join(page.path), str(page.date)))
    entries.sort(key=lambda x: x[2], reverse=True)

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p, d in entries[:30]:
            content += '<li><a href="' + p + '">' + d + ' ' + t + '</a></li>'
        content += '</ol>'

    recentpage = Page(path='recent',
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
    return [recentpage]

