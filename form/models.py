from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.auth.models import User



Vehicle_Choices = (('x','x'),('y','y'))
AmPm_Choices = (('am','am'),('am','am'))
Booking_Choices = (('x','x'),('y','y'))
Approval_Choices = (('approved','approved'),('unapproved','unapproved'),('rejected','rejected'))
Time_Choices = 	(('0','1:00'),('1','2:00'),('2','3:00'),('3','4:00'),('4','5:00'),('5','6:00'),('6','7:00'),('7','8:00'),('8','9:00'),('9','10:00'),('10','11:00'),('11','12:00'))

class Booking(models.Model):

	user = models.ForeignKey(User)
	name = models.CharField(max_length=120, null=False)
	name_email = models.EmailField(max_length=254,null=False)
	head_name = models.CharField(max_length=120, null=False)
	vehicle_type = models.CharField(max_length=120,  choices=Vehicle_Choices,default='Car')
	booking_type = models.CharField(max_length=120, choices=Booking_Choices,default='Free')
	pickup_address = models.TextField(null=False)
	pickup_time = models.CharField(max_length=120,choices=Time_Choices,default='0')
	am_pm = models.CharField(max_length=120,  choices=AmPm_Choices,default='Car')
	pickup_date = models.DateField(null=False)
	contact = models.IntegerField()
	approval_name = models.CharField(max_length=120, null=False)
	approval_email = models.EmailField(max_length=254,null=False)
	approval_status = models.CharField(max_length=120, choices=Approval_Choices,default='Free')
	note_user = models.TextField()
	note_admin = models.TextField()
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




