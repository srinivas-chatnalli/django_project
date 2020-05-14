from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from .models import BookInstance

"""
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter the date between now and 4 weeks(default 3weeks)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_("Invalid Date - Date past renewal"))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid Date - Date more than 4 weeks"))

        return data
"""
class RenewBookForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_("Invalid Date - Date past renewal"))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid Date - Date more than 4 weeks"))

        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New_Renewal_date')}
        help_text = {'due_back', _('Enter the date between now and 4 weeks')}
