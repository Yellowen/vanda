from django.forms import newforms

class SearchForm(forms.Form):
    text = forms.CharField(label="Enter search term")
    search_content = forms.BooleanField(label="Search content", required=False)
