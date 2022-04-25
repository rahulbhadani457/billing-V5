from django.urls import path
from . import views

app_name = 'GST2A'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('GST2Aindex/',views.GST2Aindex.as_view(),name='GST2Aindex'),
    path('CreateGST2A/',views.CreateGST2A.as_view(),name='CreateGST2A'),
    path('UpdateGSTR2A/<int:pk>/',views.UpdateGSTR2A.as_view(),name='UpdateGSTR2A'),
    path('GSTR2AList/',views.GSTR2AList.as_view(),name='GSTR2AList'),
    path('GSTR2ADeleteView/<int:pk>/',views.GSTR2ADeleteView.as_view(),name='GSTR2ADeleteView'),
    path('search/',views.search,name='search'),
    path('gst2Input/',views.gst2Input,name='gst2Input'),
    path('GSTR2AFilling/',views.GSTR2AFilling,name='GSTR2AFilling'),
    path('autocomplete/',views.autocomplete,name='autocomplete'),
    path('autocomplete_gst_no/',views.autocomplete_gst_no,name='autocomplete_gst_no'),
    path('autocomplete_Supplier/',views.autocomplete_Supplier,name='autocomplete_Supplier'),
    path('DetailGSTR2A/<int:pk>/',views.DetailGSTR2A.as_view(),name='DetailGSTR2A'),
    
    
]
