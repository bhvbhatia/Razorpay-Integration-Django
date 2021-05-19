from django.shortcuts import render
import razorpay
from.models import coffee
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
def home(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'about_us.html')
def event(request):
    return render(request,'events.html')
def blog(request):
    return render(request,'blog.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        send_mail("Contact Form",message,settings.EMAIL_HOST_USER,
                 ['reciepentemailaddress'], )
    return render(request,'contact_us.html')





def donate(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = int(request.POST.get("amount"))*100
        client = razorpay.Client(auth = ("yourapikeyrazorpay", "privatekeyrazorpay"))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        print(payment)
        coff = coffee(name=name, amount=amount, email=email, payment_id = payment['id'])
        coff.save()
        return render(request , "donate.html" , {'payment' : payment})

    return render(request,'donate.html')


@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        print(a)
        order_id = ""
        for key , val in a.items():

            if key == 'razorpay_order_id':
                order_id = val
                break
        user = coffee.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()


        msg_plain = render_to_string('email.txt')
        msg_html = render_to_string('email.html')

        send_mail("Your donation has been received", msg_plain, settings.EMAIL_HOST_USER,
                 [user.email], html_message = msg_html)



        return render(request,'success.html')
