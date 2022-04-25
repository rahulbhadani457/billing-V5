from django.conf.urls import url
from django.urls import path, re_path
from . import views


app_name = 'adminrep'

urlpatterns = [

    path('NewCustForm/',views.NewCustForm,name='NewCustForm'),
    path('payment/',views.payment,name='payment'),
    #path('delete/<int:pk>/',views.printDeleteView.as_view(),name='delete'),
    path('Invsearch/',views.Invsearch,name='Invsearch'),
    url(r'^Invsearch/(?P<Inv>\w+)/(?P<q>\w+)/$',views.Invsearch,name='Invsearch'),
    #re_path(r'^Invsearch\.+$',views.Invsearch,name='Invsearch'),
    path('paymentupdate/',views.paymentupdate,name='paymentupdate'),
    path('GST1/',views.GST1,name='GST1'),
    path('gst1Input/',views.gst1Input,name='gst1Input'),
    path('cancelInv/',views.cancelInv,name='cancelInv'),
    path('autocomplete_cust_search/',views.autocomplete_cust_search,name='autocomplete_cust_search'),
    path('oldCustForm/',views.oldCustForm,name='oldCustForm'),
    path('updateCustEntry/<int:pk>/',views.updateCustEntry.as_view(),name='updateCustEntry'),
    path('CustEntryView/',views.CustEntryView.as_view(),name='CustEntryView'),
    path('<int:pk>/',views.custDetailView.as_view(),name='detail'),
    


]
