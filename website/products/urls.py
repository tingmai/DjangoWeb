from . import views
from django.urls import path


urlpatterns=[
    path('backend/', views.index),
    path('backend/create', views.create),
    path('backend/edit/<int:id>', views.edit),
    path('backend/update/<int:id>', views.update),
    path('backend/delete/<int:id>', views.delete),
    path('frontend/', views.search),
    path('frontend/checkout/', views.checkout),
    path('frontend/add-to-cart/<int:id>', views.add),
    path('frontend/removeall/', views.removeall),
    path('frontend/remove/<int:id>', views.remove_me),
    #path('frontend/search', views.search),
]