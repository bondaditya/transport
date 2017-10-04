from django import forms
from .models import Booking 
from django.contrib.auth.models import User, Group
from django.contrib.admin.widgets import AdminDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking 
		fields = ['commuter_name','budget_head','vehicle_type','booking_type','pickup_address','pickup_date','pickup_time','am_pm','commuter_contact','approving_authority','approving_authority_email','remarks']
		widgets = {
		# 	'pickup_time':forms.TimeInput(format='%I:%M %p'),
		 	'pickup_date': DateInput(),
		 }


		#pickup_time = forms.TimeField(widget=TimeInput(format='%I:%M %p'))


class BookingUpdateForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['approval_status']



class SignupForm(forms.Form):
    

    def signup(self, request, user):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')
        if "@ashoka.edu.in" not in data:
            raise forms.ValidationError("Must be an ashoka id")

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


