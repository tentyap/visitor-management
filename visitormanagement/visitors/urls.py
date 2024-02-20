from . import views
from django.urls import path


urlpatterns = [
    path("",views.base, name ="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('visitor/checkout/<int:pk>',views.checkout,name="checkout"),
    path('importdata/', views.import_data_to_db,name='importdata'),
    path('exportdata/',views.export_data_to_excel, name='exportdata'),

    path('qr/', views.qr, name='qr'),

    path("visitor/",views.visitor, name='visitor'),
    path('new/', views.visitor_create_view, name='visitor_create'),
    path('visitor/details/<int:id>',views.details, name="details"),
    path('visitor/delete/<int:id>',views.delete,name='delete'),
    path('visitor/update/<int:id>',views.update,name='update'),
    
    path('purpose/',views.purpose,name='purpose'),
    path('purpose/delete/<int:id>',views.delete_purpose,name='delete_purpose'),
    path('purpose/update/<int:id>',views.edit_purpose,name='edit_purpose'),

]