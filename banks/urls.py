from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home),
    path('banks/', views.banks),
    re_path('bank/(?P<ifsc_code>\w+)/$', views.bank_branch_detail),
    path('banks/<int:bank_id>/', views.bank_branches),
]
