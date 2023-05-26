from django import forms
from .models import City


class CityFormSelect(forms.Form):
    select_city = forms.ChoiceField(
        choices=[(c.uuid, c.name) for c in City.objects.all()],
        widget=forms.Select(attrs={'class': 'filter-select'}),
        label=''
    )

