from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save 
from django.utils import timezone
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string





#Transport_Choices = (('Ashoka University','Ashoka University'),('Vikrant Holidays','Vikrant Holidays'),('W G Tours & Travels','W G Tours & Travels'))
#Budget_Head_Choices = (('Admin','Admin'),('Career Development','Career Development'),('CFE','CFE'),('CMGGA','CMGGA'),('Colloquium Creative Writing','Colloquium Creative Writing'),('Colloquium','Colloquium'),('CSBC','CSBC'),('CSGS','CSGS'),('CSIP','CSIP'),('Finance','Finance'),('Fund Raising','Fund Raising'),('GCWL','GCWL'),('HR','HR'),('IT','IT'),('Library','Library'),('Marketing YIF','Marketing YIF'),('Media','Media'),('OAA','OAA'),('OOR','OOR'),('OSL','OSL'),('OUP','OUP'),('Operations','Operations'),('Performing Arts','Performing Arts'),('Pro VC Office','Pro VC Office'),('Projects','Projects'),('Research Budget(Madhavi Maganti)','Research Budget(Madhavi Maganti)'),('Research Budget(Tusli Sriniwasan)','Research Budget(Tusli Sriniwasan)'),('Rsearch Budget(Dario Darji)','Rsearch Budget(Dario Darji)'),('Science','Science'),('SERI','SERI'),('Sports','Sports'),('Summer Semester','Summer Semester'),('TCPD','TCPD'),('VC Office','VC Office'),('YIF','YIF'),('YIF Alumni','YIF Alumni'))
active_choices = (('active','active'),('inactive','inactive'))
night_choices = (('Yes','Yes'),('No','No'))
AmPm_Choices = (('am','am'),('pm','pm'))
Booking_Choices = (('One way journey','One way journey'),('Return journey','Return journey'),('Airport transfer','Airport transfer'),('Railway Station Transfer','Railway Station Transfer'))
Approval_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
#assigned_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
driver_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
Time_Choices = 	(('1:00','1:00'),('2:00','2:00'),('3:00','3:00'),('4:00','4:00'),('5:00','5:00'),('6:00','6:00'),('7:00','7:00'),('8:00','8:00'),('9:00','9:00'),('10:00','10:00'),('11:00','11:00'),('12:00','12:00'))

# class MyUser(AbstractUser):
# 	middle_name = models.CharField(max_length=120, null=True, blank=True)
# 	phone_number = models.CharField(max_length=15)
# 	department = models.CharField(max_length=120, null=True,blank=True)
# 	approver_id = models.CharField(max_length=120,null=True,blank=True)
# 	budget_center = models.CharField(max_length=120,null=True,blank=True)

	


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
		return self.vehicle_model_name


class Transporter(models.Model):
	code = models.CharField(max_length=120)
	name = models.CharField(max_length=120)
	contact_person = models.CharField(max_length=120)
	contact_number = models.CharField(max_length=120)
	contact_email = models.EmailField()
	remarks = models.TextField()
	status = models.CharField(max_length=120,  choices=active_choices)

	def __str__(self):
		return self.name

# class Budget_Head(models.Model):
# 	code = models.CharField(max_length=120)
# 	name = models.CharField(max_length=120)
# 	contact_person = models.CharField(max_length=120)
# 	contact_number = models.CharField(max_length=120)
# 	remarks = models.TextField()
# 	status = models.CharField(max_length=120,  choices=active_choices)

# 	def __str__(self):
# 		return self.name 

class Budget_Head(models.Model):
	center_name = models.CharField(max_length=120)
	reporting_authority1 = models.CharField(max_length=120)
	reporting_authority2 = models.CharField(max_length=120, null=True, blank=True)
	reporting_authority_email1 = models.EmailField(max_length=120)
	reporting_authority_email2 = models.EmailField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.center_name+ " "+ "(%s)"%self.reporting_authority_email1  + " / " + "(%s)"%self.reporting_authority_email2

class Booking( models.Model):

	user = models.ForeignKey(User)
	driver = models.ForeignKey(Driver, default=1, null=True, blank=True)
	vehicle = models.ForeignKey(Vehicle,default=1,null=True, blank=True)
	transporter = models.ForeignKey(Transporter, default=1,null=True,blank=True)
	commuter_name = models.CharField(max_length=120, null=False)
	#head_email = models.EmailField(max_length=254,null=False)
	budget_head_approval_authority = models.ForeignKey(Budget_Head,default=1,null=True,blank=True)
	#vehicle_type = models.CharField(max_length=120,  choices=Vehicle_Choices,default='Car')
	booking_type = models.CharField(max_length=120, choices=Booking_Choices,default='Unapproved')
	pickup_address = models.TextField(null=False)
	pickup_time = models.CharField(max_length=120,choices=Time_Choices,default='0')
	am_pm = models.CharField(max_length=120,  choices=AmPm_Choices,default='Car')
	pickup_date = models.DateField(null=False)
	commuter_contact = models.IntegerField()
	# approving_authority = models.CharField(max_length=120, null=False)
	# approving_authority_email = models.EmailField(max_length=254,null=False)
	approval_status = models.CharField(max_length=120, choices=Approval_Choices,default='unapproved')
	remarks = models.TextField()
	note_admin = models.TextField()
	# assigned_to = models.CharField(max_length=120, choices=assigned_Choices,default='XYZ')
	# driver_name = models.CharField(max_length=120, choices=driver_Choices,default='XYZ')
	# driver_contact = models.IntegerField(null=True, blank=True)
	slug = models.SlugField(unique=True)

	
	def get_absolute_url(self):
		return reverse("thanks", kwargs={"slug": self.slug})

	def __str__(self):
		return self.commuter_name

		

	def create_slug(instance, new_slug=None):
	    slug = slugify(instance.commuter_name)
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


@receiver(pre_save, sender=Booking, dispatch_uid='active')
def active(sender, instance, **kwargs):
    if instance.approval_status == "approved":
        subject = 'Request Update'
        mesagge = '%s your account is now active' %(instance.slug)
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email,'transport.app@ashoka.edu.in']
        contact_message = "http://127.0.0.1:8000/booking/"+"%s" %(instance.slug)
        msg_html = render_to_string('form/email_update.html', {'booking': Booking.objects.get(slug=instance.slug)})
        send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, html_message=msg_html)
        # print (instance.slug)
        # messages.success(request, "Successfully Updated")

		# def save(self):
		# if self.slug:
		# 	booking = Booking.objects.get(slug=self.slug)
		# 	email1 = settings.EMAIL_HOST_USER
		# 	from_email = settings.EMAIL_HOST_USER
		# 	to_email = [from_email,email1,'transport.app@ashoka.edu.in'] 
		# 	subject = "localhost:8000/booking/%s" %(instance.slug) 
		# 	contact_message = "http://127.0.0.1:8000/booking/"+"%s" %(self.slug)
		# 	msg_html = render_to_string('form/email_assigned.html', {'booking': Booking.objects.get(slug=instance.slug)})
		# 	send_mail(subject, 
		# 		contact_message, 
		# 		from_email, 
		# 		to_email, html_message=msg_html)

	
	




class Invoices(models.Model):
	booking = models.OneToOneField(Booking)
	tarrif = models.IntegerField()
	total_km = models.IntegerField()
	night_option = models.CharField(max_length=120, choices = night_choices, default='No')
	night_charges = models.IntegerField()
	toll_cost = models.IntegerField()
	total = models.IntegerField()

	def save(self, *args, **kwargs):
		if self.night_option == "Yes":
			self.total = self.tarrif*self.total_km+self.night_charges+self.toll_cost
		else:
			self.total = self.tarrif*self.total_km+self.toll_cost
		super(Invoices,self).save(*args, **kwargs)
		print (self.total)



	def __str__(self):
		return self.booking.commuter_name +" "+self.booking.user.username

	@property
	def total_cost(self):
		if self.booking.approval_status=="approved":
			if self.night_option == "Yes":
				return self.tarrif*self.total_km+self.night_charges+self.toll_cost
			else:
				return self.tarrif*self.total_km+self.toll_cost
		else:
			return 0



