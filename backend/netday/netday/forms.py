from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(
        required=True,
        error_messages={'required': 'The name field is required'},
    )
    surname = forms.CharField(
        required=True,
        error_messages={'required': 'The last name field is required'}
    )
    email = forms.EmailField()
    phone_number = forms.CharField()
    country = forms.CharField()
    university = forms.CharField()
    major = forms.CharField(
        required=True,
        error_messages={'required': 'The major field is mandatory'}
    )
    course = forms.IntegerField()

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if course is not None and not str(course).isdigit():
            raise forms.ValidationError('The course field must be a number')
        return course
