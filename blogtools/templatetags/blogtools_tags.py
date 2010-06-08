from django import template

from template_utils.templatetags.generic_content import GenericContentNode, ContextUpdatingNode


register = template.Library()


@register.filter
def concat(value,arg):
    #TODO: Maybe should be move to some generic library?
    return "%s%s" % (value, arg)


@register.filter
def integer_to_month_name(value):
    #TODO: Maybe should be move to some generic library?
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return month_names[value-1]







#TODO: Maybe use a metaclass to avoid to repeat all that boilerplate code in the ``__init__`` and ``render`` methods.





class EntryTemplateTagsBase(object):
    publication_date_field = 'pub_date'
    entry_queryset = None
    template_root_path = None
    #TODO: template_tag_name_prefix
    
    def register(self, given_register):
        this = self # Trickery so we can access this object in lower level objects and avoid conflicts with other self's.
    
    
    
        class ArchiveMonthList(ContextUpdatingNode):
            
            def __init__(self, queryset, varname):
                if queryset != None:
                    self.queryset = template.Variable(queryset)
                else:
                    self.queryset = None
                self.varname = varname
                
            def get_content(self, context):
                if self.queryset != None:
                    queryset = self.queryset.resolve(context)
                else:
                    queryset = this.entry_queryset
                return { self.varname: queryset.dates(this.publication_date_field, 'month', order='DESC') }
        
        def get_archive_month_list(parser, token):
            """
            Retrieves the list of months when entries were posted.
            If ``queryset`` is not given, it uses the default queryset provided in the class declaration.
            
            Syntax::
            
                {% get_archive_month_list [queryset] as [varname] %}
                {% get_archive_month_list as [varname] %}
            
            Example::
            
                {% get_archive_month_list entry_list as month_list %}
                {% get_archive_month_list as month_list %}
            
            """
            
            bits = token.contents.split()
            if len(bits) not in [3, 4]:
                raise template.TemplateSyntaxError("'%s' tag takes either two or three arguments" % bits[0])
            if len(bits) == 4:
                if bits[2] != 'as':
                    raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
                return ArchiveMonthList(bits[1], bits[3])
            else: # len(bits) == 3:
                if bits[1] != 'as':
                    raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
                return ArchiveMonthList(None, bits[2])
        get_archive_month_list = given_register.tag(get_archive_month_list)
            
            
            
            




        class LatestNode(ContextUpdatingNode):
            def __init__(self, queryset, num, varname):
                if queryset != None:
                    self.queryset = template.Variable(queryset)
                else:
                    self.queryset = None
                self.num = num
                self.varname = varname

            def get_content(self, context):
                if self.queryset != None:
                    queryset = self.queryset.resolve(context)
                else:
                    queryset = this.entry_queryset
                if self.num == 1:
                    result = queryset.order_by("-" + this.publication_date_field)[0]
                else:
                    result = list(queryset.order_by("-" + this.publication_date_field)[:self.num])
                return { self.varname: result }
        
                
        def get_latest_entries(parser, token):
            """
            Retrieves the latest ``num`` entries and stores them in a
            specified context variable. If ``queryset`` is not given, it uses the
            default queryset provided in the class declaration.
            
            Syntax::
            
                {% get_latest_entries [queryset] [num] as [varname] %}
                {% get_latest_entries [num] as [varname] %}
            
            Examples::
            
                {% get_latest_entries entry_list 5 as featured_entries %}
                {% get_latest_entries 5 as featured_entries %}
            
            """
            bits = token.contents.split()
            if len(bits) not in [4, 5]:
                raise template.TemplateSyntaxError("'%s' tag takes either three or four arguments" % bits[0])
            if len(bits) == 5:
                if bits[3] != 'as':
                    raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
                return LatestNode(bits[1], bits[2], bits[4])
            else: # len(bits) == 4:
                if bits[2] != 'as':
                    raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
                return LatestNode(None, bits[1], bits[3])
        get_latest_entries = given_register.tag(get_latest_entries)











        
        
        class GetEntryQueryset(ContextUpdatingNode):
            
            def __init__(self, varname):
                self.varname = varname
                
            def get_content(self, context):
                return { self.varname: this.entry_queryset }    
        
        def get_entry_queryset(parser, token):
            """
            Retrieves the queryset provided in the class declaration.
            
            Syntax::
            
                {% get_entry_queryset as [varname] %}
            
            Example::
            
                {% get_entry_queryset as queryset %}
            
            """
            bits = token.contents.split()
            if len(bits) != 3:
                raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
            if bits[1] != 'as':
                raise template.TemplateSyntaxError("first argument to '%s' tag must be 'as'" % bits[0])
            return GetEntryQueryset(bits[2])
        get_entry_queryset = given_register.tag(get_entry_queryset)
        
        
        

        
    
        class FeaturedNode(ContextUpdatingNode):
            def __init__(self, queryset, num, varname):
                if queryset != None:
                    self.queryset = template.Variable(queryset)
                else:
                    self.queryset = None
                self.num = num
                self.varname = varname

            def get_content(self, context):
                if self.queryset != None:
                    queryset = self.queryset.resolve(context)
                else:
                    queryset = this.entry_queryset
                if self.num == 1:
                    result = queryset.filter(is_featured__exact=True)[0]
                else:
                    result = list(queryset.filter(is_featured__exact=True)[:self.num])
                return { self.varname: result }
        
                
        def get_featured_entries(parser, token):
            """
            Retrieves the latest ``num`` featured entries and stores them in a
            specified context variable. If ``queryset`` is not given, it uses the
            default queryset provided in the class declaration.
            
            Syntax::
            
                {% get_featured_entries [queryset] [num] as [varname] %}
                {% get_featured_entries [num] as [varname] %}
            
            Examples::
            
                {% get_featured_entries entry_list 5 as featured_entries %}
                {% get_featured_entries 5 as featured_entries %}
            
            """
            bits = token.contents.split()
            if len(bits) not in [4, 5]:
                raise template.TemplateSyntaxError("'%s' tag takes either three or four arguments" % bits[0])
            if len(bits) == 5:
                if bits[3] != 'as':
                    raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
                return FeaturedNode(bits[1], bits[2], bits[4])
            else: # len(bits) == 4:
                if bits[2] != 'as':
                    raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
                return FeaturedNode(None, bits[1], bits[3])
        get_featured_entries = given_register.tag(get_featured_entries)
    
    
