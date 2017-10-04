from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from django.contrib.auth.models import User, Group 
from .models import Booking, Invoices, Driver, Vehicle, MyUser
from import_export.admin import ImportExportModelAdmin
from import_export import resources, widgets
# Register your models here.

class InvoicesInLine(admin.TabularInline):
	model = Invoices
class RiderInLine(admin.TabularInline):
	model=Booking

class DriverAdmin(admin.ModelAdmin):
	inlines = [RiderInLine]

class VehicleAdmin(admin.ModelAdmin):
	inlines = [RiderInLine]



class RoleResource(resources.ModelResource):

    class Meta:
        model = MyUser
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'last_name', 'first_name', 'middle_name','email_id','department','approver_id','budget_center')

    def import_obj(self, obj, data, dry_run):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = generate_username(first_name, last_name)
        for field in self.get_fields():
            if isinstance(field.widget, widgets.ManyToManyWidget):
                continue
            if field.column_name == 'email':
                data.update({'email': email})
            print(obj)

            self.import_field(field, obj, data)

class RoleAdmin(ImportExportModelAdmin):  
    resource_class = RoleResource   





class BookingAdmin(admin.ModelAdmin):
	list_display = ('user','approval_status','pickup_date','vehicle_type','booking_type','transport','driver')
	list_filter = ('user','approval_status',('pickup_date',DateRangeFilter),'vehicle_type','booking_type','transport','driver')
	inlines = [InvoicesInLine]



admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Invoices)
admin.site.register(MyUser,RoleAdmin)


admin.site.unregister(Group)