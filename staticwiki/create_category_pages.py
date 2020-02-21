# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import Page

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
            entries.append((page.title, '/' + page.path + '/' + page.filename + '/'))
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    categorypage = Page(path='categories',
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
    return categorypage

def create_allcategory_page(pages):
    title = 'All categories'
    name = 'categories'

    entry_set = set()
    for page in pages:
        for category in page.categories:
            entry_set.add((category, create_category_link(create_category_linkname(category))))

    entries = list(entry_set)
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    categorypage = Page(path='categories',
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

