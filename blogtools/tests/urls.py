from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^blog/', include('blogtools.tests.blug.urls')),
     url(r'^comments/', include('django.contrib.comments.urls')),
)
