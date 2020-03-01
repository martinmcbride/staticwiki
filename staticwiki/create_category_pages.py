# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import Page
import os

def create_category_linkname(category):
    return 'category-' + category.replace(' ', '-')

def create_category_link(linkname):
    return '/categories/' + linkname + '/'

def create_category_page(category, pages):
    title = 'Articles categorised with ' + category
    name = create_category_linkname(category)

    entries = []
    for page in pages:
        if category in page.categories:
            entries.append((page.title, '/' + page.path + '/'))
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    categorypage = Page(path=os.path.join('categories', name),
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
    return categorypage

def create_allcategory_page(pages):

    entry_set = set()
    for page in pages:
        for category in page.categories:
            entry_set.add((category, create_category_link(create_category_linkname(category))))

    entries = list(entry_set)
    entries.sort(key=lambda x: x[0])
    title = 'All categories (' + str(len(entries)) + ')'

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

    categorypage = Page(path='categories/categories',
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
    return categorypage

def create_all_categories(pages):
    categories = set()
    for page in pages:
        if page.categories:
            for category in page.categories:
                categories.add(category)

    categorypages = []
    for category in categories:
        categorypages.append(create_category_page(category, pages))

    allcategories = create_allcategory_page(pages)
    categorypages.append(allcategories)

    return categorypages

