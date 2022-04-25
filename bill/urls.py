from django.urls import path
from . import views

app_name = 'bill'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('admin/',views.AdminView.as_view(),name='admin'),
    path('report/',views.ReportView.as_view(),name='report'),
    #path('print/',views.printView.as_view(),name='print'),
    path('admin_gst_list/',views.gstAdminListView.as_view(),name='admin_gst_list'),
    path('admin_nogst_list/',views.nogstAdminListView.as_view(),name='admin_nogst_list'),
    path('gst_list/',views.gstListView.as_view(),name='gst_list'),
    path('nogst_list/',views.nogstListView.as_view(),name='nogst_list'),
    path('create/',views.CreateSaleEntry.as_view(),name='create'),
    path('<int:pk>/',views.gstDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',views.updateSaleEntry.as_view(),name='update'),
    path('delete/<int:pk>/',views.billDeleteView.as_view(),name='delete'),
    path('view/',views.viewSales.as_view(),name='viewSales'),
    path('search/',views.search,name='search'),
    path('search-form/', views.search_form,name='search-form'),
    path('Estimate/', views.Estimate,name='Estimate'),
    path('Invoice/', views.Invoice,name='Invoice'),
    path('stock/', views.stock.as_view(),name='stock'),
    path('stateOfSupply/',views.stateOfSupply,name='stateOfSupply'),
    path('autocomplete/', views.autocomplete,name='autocomplete'),
    path('autocomplete_Catogory/', views.autocomplete_Catogory,name='autocomplete_Catogory'),
]
