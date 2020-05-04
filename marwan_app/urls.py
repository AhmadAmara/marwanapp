from django.urls import path
from marwan_app import views

urlpatterns = [
  path('', views.home, name='home'),
  path('login/', views.login, name='login'),
  path('signout/', views.signout, name='signout'),
  path('signup/', views.signup, name='signup'),
  path('order/',  views.order, name='order'),
  path('bookTimes/',  views.bookTimes, name='bookTimes'),
  path('book/<time_id>',  views.book, name='book'),
  path('cancel_booked/<booked_id>',  views.cancel_booked, name='cancel_booked'),
  path('controlPanel/', views.control_panel, name="controlPanel"),
  path('adminTemplates/today_orders',  views.today_orders, name='today_orders'),
  path('adminTemplates/tomorrow_orders',  views.tomorrow_orders, name='tomorrow_orders'),


]
