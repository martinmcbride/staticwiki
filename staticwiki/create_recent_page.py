# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import Page
import os.path

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ]

def get_month_year(date):
    month = int(date[5:7]) - 1
    return month_names[month] + ' ' + date[0:4]


def create_recent_page(pages):
    title = 'Recent articles'

    entries = []
    for page in pages:
        entries.append((page.title, '/' + os.path.join(page.path), str(page.date)))
    entries.sort(key=lambda x: x[2], reverse=True)

    content = ''
    month = '0000-00'
    first = True
    if entries:
        for t, p, d in entries[:30]:
            new = month[:7]!=d[:7]
            if new:
                month = d[:8]
                if not first:
                    content += '</ol>'
                first = False
                content += '<h3>' + get_month_year(month) + '</h3>'
                content += '<ol class="list-unstyled">'
            content += '<li><a href="' + p + '">' + t + '</a></li>'
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

def create_index_page(pages):
    title = 'All articles'

    entries = []
    for page in pages:
        entries.append((page.title, '/' + os.path.join(page.path)))
    entries.sort(key=lambda x: x[0])

    content = ''
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for initial in alphabet:
        initial_entries = [e for e in entries if e[0][0].upper()==initial]
        if initial_entries:
            content += '<p><h3>' + initial + '</h3>'
            content += '<ol class="list-unstyled">'
            for t, p in initial_entries:
                content += '<li><a href="' + p + '">' + t + '</a></li>'
            content += '</ol>'

    initial_entries = [e for e in entries if e[0][0].upper() not in alphabet]
    if initial_entries:
        content += '<p><h3>Other</h3>'
        content += '<ol class="list-unstyled">'
        for t, p in initial_entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    recentpage = Page(path='all',
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

