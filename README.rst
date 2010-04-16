=================
Glamkit-blogtools
=================

A tool for quickly creating customised blog apps. It is part of the `GLAMkit project <http://glamkit.org/>`_. For more information, see the `documentation <http://docs.glamkit.org/blogtools/>`_.

The approach
============

Most blogs are very similar - they usually are a regular flow of entries published over time. But each blog may also have subtle differences that make them unique or special. For example, you may want to attach multiple authors to a given blog entry, or no specific author at all; you may want to attach a thumbnail image to every blog entry; or you may want to have multiple blogs on your website; and so on.

There are many blog apps available in the Django ecosystem. However, all of them are written in a "traditional" way (i.e. a bunch of models, views, templates, etc.) which makes them difficult to extend or trim down to fit your specific needs, unless you are willing to modify and maintain that code yourself.

Blogtools takes a totally different approach in that instead of being just another blog app, it is in fact a mini-framework that lets you create your own blog apps. So, you can use blogtools to create several blog apps for several websites, and each of these apps can easily be tweaked to fit any specifications.

Blogtools is already fully functional so feel free to jump right in. More documentation, including step-by-step tutorials, will also be posted here soon to get you started.

View a full list of `GLAMkit components <http://docs.glamkit.org/components/>`_.

Dependencies:
=============

* django apps:
    - django.contrib.admin
    - django-template-utils
    - django-tagging (optional)
    - typogrify (optional)
    
* python libraries:
    - BeautifulSoup (optional)
    - markdown (optional)
    
