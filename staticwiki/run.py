# Author:  Martin McBride
# Created: 2020-02-14
# Copyright (c) 2020, Martin McBride
# License: MIT

from create_pages import convert_all
from create_tag_pages import create_all_tags
from create_recent_page import create_recent_page, create_index_page
from create_category_pages import create_all_categories
from write_html import write_html
import shutil, os
from pathlib import Path

BASE = '/nas/martin/websites/pythoninformer/site'
OUT = '/nas/martin/websites/pythoninformer/site/public'

def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst): # This one line does the trick
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                shutil.copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)


try:
    shutil.rmtree(OUT, ignore_errors=False, onerror=None)
except:
    pass

Path(OUT).mkdir(parents=True, exist_ok=True)
copytree(os.path.join(BASE, 'static'), OUT)

with open('index.tpl') as infile:
    template = ''.join(infile)

pages = convert_all(os.path.join(BASE, 'content'))
tagpages = create_all_tags(pages)
categorypages = create_all_categories(pages)
recentpages = create_recent_page(pages)
allpages = create_index_page(pages)

for s in [pages, tagpages, categorypages, recentpages, allpages]:
    for page in s:
        write_html(template, OUT, page, pages)


