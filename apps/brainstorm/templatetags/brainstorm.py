from django import template , forms
from django.utils.translation import ugettext as _
from django.template import Template , Context
from apps.brainstorm.models import *
from django.template.loader import get_template
from dina.core.dev import dassert

register = template.Library()


# {% brainstorm "section" %} defination. --------------------------------------------------------

def do_brainstorm (parser, token):
    sections = (
        'view',
        'form',
        )
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, section_title = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (section_title[0] == section_title[-1] and section_title[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    if section_title[1:-1] in sections:
        return brainstorm_node(section_title[1:-1])
    else:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    




class storm_form (forms.Form):

    def __init__(self, *args, **kwargs):
        super(storm_form, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(i.id, i.name) for i in category.objects.all()]

    email = forms.EmailField (label = _("Email") , help_text = _("We will contact you via this email address"))
    category = forms.ChoiceField (label = _("Category"))
    storm = forms.CharField (max_length =100 , label = _("Title"))
    description = forms.CharField (widget=forms.Textarea , label = _("Description"))



class category_form (forms.Form):


    title= forms.CharField (label = _("title"))

    
    
class brainstorm_node(template.Node):
    def __init__(self, section):
        self.section = section
        self.form =[ storm_form () , category_form ()]
        
        

    def render(self, context):
        
        if self.section == 'view':
            cate = category.objects.filter (published = True).order_by ('title')
            obj = list ()
            
            for i in cate:
                dic = dict ()
                dic['title'] = i.title
                storms = storm.objects.filter (category = i)
                dic['storms'] = storms
                obj.append (dic)
            t = get_template ('view.html')
            return t.render (Context ({"cats" : obj }))
        if self.section == 'form':
            t = get_template ("form.html")
            return t.render (Context ( {"form" : self.form[0] , "catform" : self.form[1] }))
                
        
            
# -------------------------------------------------------------------------------------------------
register.tag ('brainstorm' , do_brainstorm)
