import os
from datetime import datetime

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django import template
from django.template.loaders import app_directories
from django.template import TemplateSyntaxError
from django.test.utils import ContextList
from django.core.management import call_command
from django.db.models.loading import load_app

from blogtools.tests.blug.models import BlugEntry


class TemplateTagTestCase(TestCase):
    #TODO: Maybe it'd be good to move this class to some generic library.
    
    def renderTemplate(self, tstr, **context):
        t = template.Template(tstr)
        c = template.Context(context)
        return (t.render(c), ContextList(c))

class OverrideSettingsTestCase(TestCase):
    #TODO: Maybe this class could be taken to a generic library.
    
    def setUp(self):
        if hasattr(self, 'settings_override'):
            for (key, value) in self.settings_override.items():
                if hasattr(settings, key):
                    setattr(self, '_old_%s' % key, getattr(settings, key)) # Back up the setting
                setattr(settings, key, value) # Override the setting

        # since django's r11862 templatags_modules and app_template_dirs are cached
        # the cache is not emptied between tests
        # clear out the cache of modules to load templatetags from so it gets refreshed
        template.templatetags_modules = []
        
        # clear out the cache of app_directories to load templates from so it gets refreshed
        app_directories.app_template_dirs = []
        # reload the module to refresh the cache
        reload(app_directories)
            
        

    def tearDown(self):
        # Restore settings
        if hasattr(self, 'settings_override'):
            for (key, value) in self.settings_override.items():
                if hasattr(self, '_old_%s' % key):
                    setattr(settings, key, getattr(self, '_old_%s' % key))



class BlugTestsBase(OverrideSettingsTestCase):
    urls = 'blogtools.tests.urls'
    
    settings_override = {
        'BLOG_NAME': 'Not another Wordpress blog',
        'INSTALLED_APPS': list(settings.INSTALLED_APPS) + ['blogtools.tests.blug'],
        'TEMPLATE_DIRS': (os.path.join(os.path.dirname(__file__), 'templates'),),
    }
    
    def setUp(self):
        super(BlugTestsBase, self).setUp()
        
        # Install test app -----------------------------------------------------

        load_app('blogtools.tests.blug')
        call_command('flush', verbosity=0, interactive=False)
        call_command('syncdb', verbosity=0, interactive=False)
        
        # Create test data -----------------------------------------------------
        
        # Users
        self.jon = User.objects.create_superuser('jon', 'jon@example.com', 'testpw')
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'testpw')
        
        # Entries
        self.entry_cool = BlugEntry.objects.create(author=self.jon, status=1, excerpt='I won\'t spoil the content of this post', title="Supa cool title",
                                          body="Today I did something really cool!",
                                          slug="supa-cool-title",
                                          pub_date='2009-12-04',
                                          is_featured=True)
        self.entry_cool.tags = 'cool stuff'
        self.entry_cool.save()
        self.entry_hype = BlugEntry.objects.create(author=self.jon, status=1, title="Another blog post",
                                          body="I can't help but be the coolest guy wherever I go. Oh yeah, I'm so cool.",
                                          slug="another-blog-post",
                                          pub_date='2009-06-05',
                                          is_featured=True)
        self.entry_hype.tags = 'cool hype'
        self.entry_hype.save()
        self.entry_unpublished1 = BlugEntry.objects.create(author=self.jon, title="Can't publish this yet",
                                          body="This post isn't cool enough, so I won't publish it",
                                          slug="cant-publish-yet",
                                          pub_date='2009-06-05')
        self.entry_unpublished2 = BlugEntry.objects.create(author=self.jon, title="Can't publish this one either",
                                          body="This post is just crap. Don't publish it!",
                                          slug="cant-publish-either",
                                          pub_date='2008-09-15')
        self.entry_boring = BlugEntry.objects.create(author=self.jon, status=1, title="My life is boring",
                                          body="Please, subscribe to my blog and be my friend. Yawn.",
                                          slug="my-life-boring",
                                          pub_date='2008-10-14',
                                          is_featured=True)
        self.entry_initial = BlugEntry.objects.create(author=self.jon, status=1, title="Welcome to our blog",
                                          body="This is our new blog, and it's made with Django!",
                                          slug="welcome-our-blog",
                                          pub_date='2007-02-22')



class BlugViewTests(BlugTestsBase):
    
    def test_archive_index(self):
        response = self.client.get('/blog/')
        self.assertEquals(response.status_code, 200)
        entries = response.context['entry_list']
        self.assertEquals(list(entries), [self.entry_cool, self.entry_hype, self.entry_boring, self.entry_initial])
        
    def test_search(self):
        response = self.client.get('/blog/search/')
        self.assertEquals(response.status_code, 200)
        
        # Empty searches
        response = self.client.get('/blog/search/', {'q': ''})
        self.assertEquals(response.status_code, 200)
        entries = response.context['found_entries']
        self.assertTrue(entries is None)
        
        # Correct search
        response = self.client.get('/blog/search/', {'q': 'boring'})
        entries = response.context['found_entries']
        self.assertEquals(list(entries), [self.entry_boring])
        
        # Search again
        response = self.client.get('/blog/search/', {'q': 'cool'})
        entries = response.context['found_entries']
        self.assertEquals(list(entries), [self.entry_cool, self.entry_hype])
        
        # Another search
        response = self.client.get('/blog/search/', { 'q': '"really cool"'})
        entries = response.context['found_entries']
        self.assertEquals(list(entries), [self.entry_cool])
    
    def test_archives(self):
        #TODO: test content returned in pages
        
        # Wrong day
        response = self.client.get('/blog/2009/12/03/')
        self.assertEquals(response.status_code, 404)
        
        # Wrong month
        response = self.client.get('/blog/2009/11/')
        self.assertEquals(response.status_code, 404)
        
        # Wrong year
        response = self.client.get('/blog/2005/')
        self.assertEquals(response.status_code, 404)
        
        # Correct day
        response = self.client.get('/blog/2009/12/04/')
        self.assertEquals(response.status_code, 200)
        
        # Correct month
        response = self.client.get('/blog/2009/12/')
        self.assertEquals(response.status_code, 200)
        
        # Correct year
        response = self.client.get('/blog/2009/')
        self.assertEquals(response.status_code, 200)
        
    def test_entry(self):
        #TODO: test content returned in pages
        
        # Wrong date
        response = self.client.get('/blog/2009/11/04/supa-cool-title/')
        self.assertEquals(response.status_code, 404)
        
        # Wrong slug
        response = self.client.get('/blog/2009/12/04/supa-lame-title/')
        self.assertEquals(response.status_code, 404)
        
        # Correct URL
        response = self.client.get('/blog/2009/12/04/supa-cool-title/')
        self.assertEquals(response.status_code, 200)
        entry = response.context['entry']
        self.assertEquals(entry, self.entry_cool)
        
    def test_tagged_entries(self):
        response = self.client.get('/blog/tags/nonexisting/')
        self.assertEquals(response.status_code, 404)
        
        response = self.client.get('/blog/tags/cool/')
        self.assertEquals(response.status_code, 200)
        entries = response.context['entry_list']
        self.assertEquals(entries.count(), 2)
        self.assertTrue(self.entry_cool in entries)
        self.assertTrue(self.entry_hype in entries)
    
        response = self.client.get('/blog/tags/hype/')
        self.assertEquals(response.status_code, 200)
        entries = response.context['entry_list']
        self.assertEquals(entries.count(), 1)
        self.assertTrue(self.entry_hype in entries)
    
    def test_preview_entry(self):
        self.client.login(username='bob', password='testpw') # Bob is *not* a super user
        response = self.client.get('/blog/entry_preview/%s/' % self.entry_cool.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('entry' not in response.context)
        
        self.client.login(username='jon', password='testpw') # Jon *is* a super user
        response = self.client.get('/blog/entry_preview/%s/' % self.entry_cool.id)
        self.assertEquals(response.status_code, 200)
        entry = response.context['entry']
        self.assertEquals(entry, self.entry_cool)
        
        response = self.client.get('/blog/entry_previe/%s/' % 999)
        self.assertEquals(response.status_code, 404)



class BlugTemplateTagsTests(BlugTestsBase, TemplateTagTestCase):

    def test_archive_month_list(self):
        # Wrong syntax ---------------------------------
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_archive_month_list %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_archive_month_list as %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_archive_month_list blah blah %}"))
        
        # With queryset as parameter --------------------
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_archive_month_list nonexisting_queryset as blah %}"))
        
        output, context = self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_archive_month_list entries as month_list %}{% for month in month_list %}{{ month|date:'F Y' }}-{% endfor %}")
        self.assertEquals(output, "December 2009-June 2009-October 2008-February 2007-")
        
        # Without queryset as parameter -----------------
        output, context = self.renderTemplate("{% load blug_tags %}{% get_archive_month_list as month_list %}{% for month in month_list %}{{ month|date:'F Y' }}-{% endfor %}")
        self.assertEquals(output, "December 2009-June 2009-October 2008-February 2007-")
        
    def test_featured_entries(self):
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_featured_entries %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_featured_entries 2 %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_featured_entries 2 as %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_featured_entries 3 blah featuredentries %}"))
        
        # With queryset as parameter --------------------
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_featured_entries entries %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_featured_entries entries 2 %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_featured_entries entries 2 as %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_featured_entries entries 3 blah featuredentries %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_featured_entries nonexisting_queryset 2 as featuredentries %}"))
        
        output, context = self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_featured_entries entries 2 as featuredentries %}")
        self.assertEquals(output, "")
        self.assertEquals(context['featuredentries'], [self.entry_cool, self.entry_hype])

        # Without queryset as parameter -----------------
        output, context = self.renderTemplate("{% load blug_tags %}{% get_featured_entries 2 as featuredentries %}")
        self.assertEquals(output, "")
        self.assertEquals(context['featuredentries'], [self.entry_cool, self.entry_hype])
        
        
    def test_latest_entries(self):
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_latest_entries %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_latest_entries 3 %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_latest_entries 3 as %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_latest_entries 3 blah latestentries %}"))
        
        # With queryset as parameter --------------------
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_latest_entries entries %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_latest_entries entries 3 %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_latest_entries entries 3 as %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_latest_entries entries 3 blah latestentries %}"))
        self.assertRaises(TemplateSyntaxError, lambda: self.renderTemplate("{% load blug_tags %}{% get_latest_entries nonexisting_queryset 3 as latestentries %}"))
        
        output, context = self.renderTemplate("{% load blug_tags %}{% get_entry_queryset as entries %}{% get_latest_entries entries 3 as latestentries %}")
        self.assertEquals(output, "")
        self.assertEquals(context['latestentries'], [self.entry_cool, self.entry_hype, self.entry_boring])

        # Without queryset as parameter -----------------
        output, context = self.renderTemplate("{% load blug_tags %}{% get_latest_entries 3 as latestentries %}")
        self.assertEquals(output, "")
        self.assertEquals(context['latestentries'], [self.entry_cool, self.entry_hype, self.entry_boring])
        
class MiscTests(BlugTestsBase):
    
    def test_absolute_url(self):
        entry = BlugEntry.objects.get(slug='supa-cool-title')
        self.assertEquals(entry.get_absolute_url(), '/blog/2009/12/04/supa-cool-title/')
        
    def test_feeds(self):
        response = self.client.get('/blog/feeds/latest-typo/')
        self.assertEquals(response.status_code, 404)
        
        response = self.client.get('/blog/feeds/latest/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content.count('<item>'), 4)
        self.assertTrue(self.entry_cool.title in response.content)
        self.assertTrue(self.entry_hype.title in response.content)
        self.assertTrue(self.entry_boring.title in response.content)
        self.assertTrue(self.entry_initial.title in response.content)
        
        response = self.client.get('/blog/feeds/tags/')
        self.assertEquals(response.status_code, 404)
        
        response = self.client.get('/blog/feeds/tags/nonexisting/')
        self.assertEquals(response.status_code, 404)
        
        response = self.client.get('/blog/feeds/tags/cool/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content.count('<item>'), 2)
        self.assertTrue(self.entry_cool.title in response.content)
        self.assertTrue(self.entry_hype.title in response.content)
