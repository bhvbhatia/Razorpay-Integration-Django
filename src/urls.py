from django.urls import path,include
from .views import home, success, donate, aboutus, event, blog, contact

urlpatterns = [
    path('',home,name="home"),
    path('aboutus',aboutus,name='aboutus'),
    path('event',event,name='event'),
    path('blog',blog,name='blog'),
    path('contact',contact,name='contact'),
    path('donate',donate,name='donate'),
    path('success',success,name='success')
]
