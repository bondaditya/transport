try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import FormView
from .models import Booking 
from .forms import BookingForm, BookingUpdateForm 
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, DetailView 
from django.core.mail import send_mail
# from django.template import Context
# from django.template.loader import get_template
from django.template.loader import render_to_string



@login_required
def BookingFormView(request):
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	raise Http404
		
	form = BookingForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form_email1 = form.cleaned_data.get("approving_authority_email")
		#form_email2 = form.cleaned_data.get("approval_email")
		form_name = form.cleaned_data.get("commuter_name")
		form_vehicle_type = form.cleaned_data.get("vehicle_type")
		subject = "localhost:8000/booking/%s" %(instance.slug)  
		from_email = settings.EMAIL_HOST_USER 
		to_email = [form_email1, from_email,'guptaadityaiitb@gmail.com',]
		contact_message = "http://127.0.0.1:8000/booking/"+"%s" %(instance.slug)
		msg_html = render_to_string('form/email_request.html', {'booking': Booking.objects.get(slug=instance.slug)})

		# some_html_message =  """
		# 			<!DOCTYPE html>
		# 	<html lang="en">
		# 	<head>
		# 	    <meta charset="UTF-8">
		# 	    <title>title</title>
		# 	</head>
		# 	<body>
		# 	    <p>"https://yoursite.com/thanks/%s":%(instance.id)</p>Click</a>
		# 	</body>
		# 	</html>
		
		# """
		
		
		
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, html_message=msg_html)
		print (instance.slug)
		messages.success(request, "Successfully Created")
		return redirect('thanks', slug=instance.slug)
	else:
		form = BookingForm
	context = {
		"form": form,
	}
	return render(request, "form.html", context)


@login_required
def BookingDetailView(request, slug=None):
	instance = get_object_or_404(Booking, slug=slug)
	# if instance.publish > timezone.now().date() or instance.draft:
	# 	if not request.user.is_staff or not request.user.is_superuser:
	# 		raise Http404
	share_string = quote_plus(instance.commuter_name)
	print (instance.approval_status)
	context = {
		"title": instance.commuter_name,
		"instance": instance,
		"share_string": share_string,
		"booking": Booking.objects.get(slug=instance.slug)
	}
	return render(request, "form/booking_detail.html", context)	






# def BookingFormView(request):
# 	if request.method == "POST":
# 		form = BookingForm(request.POST)
# 		if form.is_valid():
# 			post = form.save(commit=False)
# 			post.author = request.user
# 			form_email = form.cleaned_data.get("email")
# 			form_message = form.cleaned_data.get("message")
# 			form_full_name = form.cleaned_data.get("full_name")
# 			subject = 'Testing'
# 			from_email = 'aditya.gupta@ashoka.edu.in'
# 			to_email = [form_email, 'guptaadityaiitb@gmail.com']
# 			contact_message = "%s: %s via %s"%( 
# 				form_full_name, 
# 				form_message, 
# 				form_email)
# 		some_html_message = """
# 					<!DOCTYPE html>
# 			<html lang="en">
# 			<head>
# 			    <meta charset="UTF-8">
# 			    <title>title</title>
# 			</head>
# 			<body>
# 			    <a href="https://yoursite.com{% url 'b' pk %}">Click</a>Click</a>
# 			</body>
# 			</html>
		
# 		"""
# 		send_mail(subject, 
# 				contact_message, 
# 				from_email, 
# 				to_email, 
# 				html_message=some_html_message,
# 				fail_silently=True)
# 		post.save()
# 		return redirect('thanks')
# 	else:
# 		form = BookingForm
# 	return render(request,'form.html',{'form':form})



@login_required
def Thanks(request):
	return render(request,'thanks.html')


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BookingUpdateForm
    model = Booking

    
    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        slug = self.kwargs.get("slug")
        # form_email1 = self.object.head_email
        form_email2 = self.object.approving_authority_email
        form_name = self.object.commuter_name
        form_vehicle_type = form.cleaned_data.get("vehicle_type")
        subject = "localhost:8000/detail/%s" %(slug)  
        from_email = 'gupta.aditya.iitb@gmail.com' 
        to_email = [from_email,'guptaadityaiitb@gmail.com']
        contact_message = "http://127.0.0.1:8000/detail/"+"%s" %(slug)
        send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				
				fail_silently=True)
        print (slug)
        #messages.success(self, "Successfully Created")
        return redirect('thanks', slug=slug)
      

    def get_context_data(self, slug=None, **kwargs):
    	slug = self.kwargs.get("slug")
    	print (slug)
    	context = super(BookingUpdateView, self).get_context_data(**kwargs)
    	context['booking'] = Booking.objects.get(slug=self.object.slug)
    	return context 

    


@login_required
def BookingListView(request):
	today = timezone.now().date()
	queryset_list = Booking.objects.filter(user=request.user)
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Booking.objects.all()
	query = request.GET.get("q")
	if query:
		querylist = queryset_list.filter(
						Q(head_name__icontains=query)|
						Q(name__icontains=query)|
						Q(approval_name__icontains=query) |
						Q(approval_status__icontains=query)
						).distinct()
								
	paginator = Paginator(queryset_list, 10)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)



			
	context = {
	'booking':Booking.objects.filter(user=request.user),
	"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request,'form/booking_list.html',context)
