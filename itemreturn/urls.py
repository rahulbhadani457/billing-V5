from django.urls import path
from . import views

app_name = 'itemreturn'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('returnindex/',views.returnindex.as_view(),name='returnindex'),
    path('CreatereturnEntry/',views.CreatereturnEntry.as_view(),name='CreatereturnEntry'),
    #path('<int:pk>/',views.gstDetailView.as_view(),name='detail'),
    #path('update/<int:pk>/',views.updateSaleEntry.as_view(),name='update'),
    #path('delete/<int:pk>/',views.billDeleteView.as_view(),name='delete'),
    
]
