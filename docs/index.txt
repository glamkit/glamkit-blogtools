Blogtools
=========

A tool for quickly creating customised blog apps.

.. rubric:: This is part of the GLAMkit Project. For more information, please visit http://glamkit.org.


Most blogs are very similar - they are usually a regular flow of entries published over time. But each blog may also have subtle differences that make them unique or special. For example, you may want to attach multiple authors to a given blog entry, or no specific author at all; you may want to attach a thumbnail image to every blog entry; or you may want to have multiple blogs on your website... and so on.

There are many blog apps available in the Django ecosystem. However, all of them are written in a "traditional" way (i.e. a bunch of models, views, templates, etc.) which makes them difficult to extend or trim down to fit your specific needs, unless you are willing to modify and maintain that code yourself.

Blogtools takes a totally different approach: instead of being just another blog app, it is a mini-framework that lets you create your own blog apps. You can use blogtools to create several blog apps for several websites, and each of these apps can easily be tweaked to fit any specifications.

Blogtools is already fully functional so feel free to jump right in. More documentation, including step-by-step tutorials, will also be posted here soon to get you started.

Settings:
=========

MARKUP_FILTER = ('typogridown', {})  # Or "markdown", "typygmentdown", etc.
