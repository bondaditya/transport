from django.contrib import admin
from django.contrib.auth.models import User, Group 
from .models import Booking
# Register your models here.

class BookingAdmin(admin.ModelAdmin):
	list_display = ('user','approval_status')
	list_filter = ('user','approval_status')


admin.site.register(Booking, BookingAdmin)

admin.site.unregister(Group)