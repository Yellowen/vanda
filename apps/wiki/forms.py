from django.forms import newforms

class SearchForm(forms.Form):
    text = forms.CharField(label="Enter search term")
