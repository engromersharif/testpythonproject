from django import forms
from pandasdemo.models import Ethanol
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy
from crispy_forms.layout import Submit


class EthanolForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Ethanol
        fields = ['Year', 'Month', 'Product', 'Date', 'REGION', 'COUNTRY',
                  'EXPORTER', 'IMPORTER', 'QTYMT', 'StorageType', 'MTonPrice', 'VALUEUSD']
