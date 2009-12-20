from django import forms
from django.utils.translation import ugettext as _
from apps.brainstorm.models import *
from django.template import Template , Context

class comment_form (forms.Form):
    
    email = forms.EmailField (label = _("Email"))
    storm = forms.CharField (widget=forms.HiddenInput)
    description = forms.CharField (widget=forms.Textarea , label = _("Comment"))

    def as_complete_table (self , action = "" , method="POST" , bname = _("submit")):
        a = super(comment_form , self).as_table()
        b = "<table><form action ='%s' method='%s'>" % (action , method )
        c = "<tr><td></td><td><p align='center'><input type='submit' value='%s'></p></td></tr></form></table>" % (bname)
        return Template (b + a + c).render (Context ())


class storm_form (forms.Form):

    def __init__(self, *args, **kwargs):
        super(storm_form, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(i.id, i.title) for i in category.objects.all()]

    email = forms.EmailField (label = _("Email") , help_text = _("We will contact you via this email address"))
    category = forms.ChoiceField (label = _("Category"))
    storm = forms.CharField (max_length =100 , label = _("Title"))
    description = forms.CharField (widget=forms.Textarea , label = _("Description"))



class category_form (forms.Form):


    title= forms.CharField (label = _("title"))
    
        
