from django import forms


class RegistrationForm(forms.Form):
    main_fname = forms.CharField(label='Main applicant first name', max_length=30)
    main_lname = forms.CharField(label='Main applicant last name', max_length=50)

    partner_fname = forms.CharField(label='Partner applicant first name', max_length=30)
    partner_lname = forms.CharField(label='Partner applicant last name', max_length=50)

