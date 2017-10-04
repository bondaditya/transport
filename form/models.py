from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser




Vehicle_Choices = (('x','x'),('y','y'))
active_choices = (('x','x'),('y','y'))
night_choices = (('Yes','Yes'),('No','No'))
AmPm_Choices = (('am','am'),('am','am'))
Booking_Choices = (('x','x'),('y','y'))
Approval_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
assigned_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
driver_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
Time_Choices = 	(('0','1:00'),('1','2:00'),('2','3:00'),('3','4:00'),('4','5:00'),('5','6:00'),('6','7:00'),('7','8:00'),('8','9:00'),('9','10:00'),('10','11:00'),('11','12:00'))

class MyUser(AbstractUser):
	middle_name = models.CharField(max_length=120, null=True, blank=True)
	phone_number = models.CharField(max_length=15)
	department = models.CharField(max_length=120, null=True,blank=True)
	approver_id = models.CharField(max_length=120,null=True,blank=True)
	budget_center = models.CharField(max_length=120,null=True,blank=True)

	


class Driver(models.Model):
	driver_name = models.CharField(max_length=120,default='Ram')
	driver_contact = models.IntegerField()
	remarks = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.driver_name

class Vehicle(models.Model):
	vehicle_model_name = models.CharField(max_length=120,default='Maruti')
	registration_number = models.CharField(max_length=120,default='HR-XYZ-78')
	remarks = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.car_model_name


class Transport(models.Model):
	code = models.CharField(max_length=120)
	name = models.CharField(max_length=120)
	contact_person = models.CharField(max_length=120)
	contact_number = models.CharField(max_length=120)
	remarks = models.TextField()
	status = models.CharField(max_length=120,  choices=active_choices)



class Booking(models.Model):

	user = models.ForeignKey(MyUser)
	driver = models.ForeignKey(Driver, default=1, null=True, blank=True)
	vehicle = models.ForeignKey(Vehicle,default=1,null=True, blank=True)
	transport = models.ForeignKey(Transport, default=1,null=True,blank=True)
	commuter_name = models.CharField(max_length=120, null=False)
	#head_email = models.EmailField(max_length=254,null=False)
	budget_head = models.CharField(max_length=120, null=False)
	vehicle_type = models.CharField(max_length=120,  choices=Vehicle_Choices,default='Car')
	booking_type = models.CharField(max_length=120, choices=Booking_Choices,default='Unapproved')
	pickup_address = models.TextField(null=False)
	pickup_time = models.CharField(max_length=120,choices=Time_Choices,default='0')
	am_pm = models.CharField(max_length=120,  choices=AmPm_Choices,default='Car')
	pickup_date = models.DateField(null=False)
	commuter_contact = models.IntegerField()
	approving_authority = models.CharField(max_length=120, null=False)
	approving_authority_email = models.EmailField(max_length=254,null=False)
	approval_status = models.CharField(max_length=120, choices=Approval_Choices,default='Unapproved')
	remarks = models.TextField()
	note_admin = models.TextField()
	# assigned_to = models.CharField(max_length=120, choices=assigned_Choices,default='XYZ')
	# driver_name = models.CharField(max_length=120, choices=driver_Choices,default='XYZ')
	# driver_contact = models.IntegerField(null=True, blank=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("thanks", kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


from .utils import unique_slug_generator

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug = unique_slug_generator(instance)



pre_save.connect(pre_save_post_receiver, sender=Booking)




class Invoices(models.Model):
	booking = models.OneToOneField(Booking)
	tarrif = models.IntegerField()
	total_km = models.IntegerField()
	night_option = models.CharField(max_length=120, choices = night_choices, default='No')
	night_charges = models.IntegerField()
	toll_cost = models.IntegerField()
	total = models.IntegerField()

	def save(self, *args, **kwargs):
		if self.booking.approval_status=="approved":
			if self.night_option == "Yes":
				self.total = self.tarrif*self.total_km+self.night_charges+self.toll_cost
			else:
				self.total= self.tarrif*self.total_km+self.toll_cost
		super(Invoices,self).save(*args, **kwargs)



	def __str__(self):
		return self.booking.name

	@property
	def total_cost(self):
		if self.booking.approval_status=="approved":
			if self.night_option == "Yes":
				return self.tarrif*self.total_km+self.night_charges+self.toll_cost
			else:
				return self.tarrif*self.total_km+self.toll_cost
		else:
			return 0



