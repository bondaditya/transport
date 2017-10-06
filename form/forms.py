from django import forms
from .models import Booking 
from django.contrib.auth.models import User, Group
from django.contrib.admin import widgets

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['commuter_name','budget_head_approval_authority','vehicle','booking_type','pickup_address','pickup_date','pickup_time','am_pm','commuter_contact','remarks']
        widgets = {
        #   'pickup_time':forms.TimeInput(format='%I:%M %p'),
            'pickup_date': DateInput(),

            'delivery_time': forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
         }

    
    # def __init__(self,*args,**kwargs):
    #     super(BookingForm,self).__init__(*args,**kwargs)
    #     self.fields['pickup_time'].widget = widgets.AdminTimeWidget()
    #     self.fields['pickup_date'].widget = widgets.AdminDateWidget(format='%H:%M')
        




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


