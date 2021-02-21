from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('quality/', views.quality, name = 'quality'),

    #WORKER
    path('workers/', views.workers, name = 'workers'),
    path('worker_individual/<str:pk_test>/', views.worker_individual, name = 'worker_individual'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('change_presence/<str:pk_test>/', views.change_presence, name = 'change_presence'),
    path('worker_absent/', views.worker_absent, name = 'worker_absent'),

    #TASK
    path('production/', views.production, name = 'production'),
    path('product_individual/<str:pk_test>/', views.product_individual, name = 'product_individual'),
    path('change_status/<str:pk_test>/', views.change_status, name = 'change_status'),
    path('add_task/', views.add_task, name='add_task'),

    #HUMAN MACHINE INTERFACE
    path('login/', views.login, name='login'),
    path('HMImachine1/<str:pk_test>/', views.HMImachine1, name = 'HMImachine1'),
    path('HMI_notauth/', views.HMI_notauth, name = 'HMI_notauth'),
    path('HMI_exception/', views.HMI_exception, name = 'HMI_exception'),

    #DISPLAY PAGES
    path('displaypage/', views.displaypage, name = 'displaypage'),
]
