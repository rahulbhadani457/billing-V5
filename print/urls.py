from django.urls import path
from . import views


app_name = 'print'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('printview/',views.printview.as_view(),name='printview'),
    path('post_print_Form/',views.post_print_Form,name='post_print_Form'),
    path('update_print_Form/<int:pk>',views.update_print_Form,name='update_print_Form'), 
    path('get_print_Form/', views.get_print_Form,name='get_print_Form'),
    path('viewprint/',views.viewprint,name='viewprint'),
    path('delete/<int:pk>/',views.printDeleteView.as_view(),name='delete'),
    path('InvoicePrint/',views.InvoicePrint,name='InvoicePrint'),
    path('quick_print_Form/',views.quick_print_Form,name='quick_print_Form'),
    path('autocomplete/', views.autocomplete,name='autocomplete'),
    path('testPrint/', views.testPrint,name='testPrint'),
    
    
]
