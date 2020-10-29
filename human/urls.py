from django.urls import path
from .views import *

urlpatterns = [
    path('qualification/<pas>', status_qual, name='status_qual'),
    path('investor/create/', download_passport),
    path('investor/rules/<pas>', rule_accept),
    path('investor/file_pass/<pas>', download_file_passport),
    path('investor/qualification/file/<pas>', download_file_qualification),
    path('investor/qualification/<pas>', qualification_permission),
]
