# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

import markdown
import yaml
import collections
import os.path

Page = collections.namedtuple('Person', 'path filename content title shorttitle author date categories tags series heading series_weight')

def convert_markdown(base, path, name):
    markdown_path = os.path.join(base, path, name)
    with open(markdown_path) as infile:
        ym = ''
        md = ''
        for s in infile:
            if s.startswith('---'):
                break;
        for s in infile:
            if s.startswith('---'):
                break;
            else:
                ym += s
        for s in infile:
            md += s

    info = yaml.load(ym, yaml.SafeLoader)
    html = markdown.markdown(md, extensions=['codehilite', 'fenced_code'])
    title = info.get('title', '')
    series = '' if not info.get('series') else info.get('series')[0]

#    if name=='index.md':
#        path = os.path.split(path)[0]

    page = Page(path=path,
                      filename=os.path.splitext(name)[0],
                      content=html,
                      title=title,
                      shorttitle=info.get('shorttitle', title),
                      author=info.get('author', ''),
                      date=info.get('date', ''),
                      categories=info.get('categories', []),
                      tags=info.get('tags', []),
                      series=series,
                      heading=info.get('heading', ''),
                      series_weight=int(info.get('series_weight', '0')))
    return page

def convert_all(base):
    pages = []
    for subdir, dirs, files in os.walk(base):
        for filename in files:
            filepath = os.path.join(base, subdir, filename)
            path = subdir[len(base)+1:]
            print(filename, subdir, base, path)
            if filepath.endswith(".md"):
                pages.append(convert_markdown(base, path, filename))
    return pages


