from django.urls import path
from demonstrationsite import views

urlpatterns = [
    path('', views.index_site, name='index_site'),
    path('index/', views.index_site, name='index_site'),
    path('login/', views.login_user, name='login_site'),
    path('logout/', views.logout_user, name='logout_site'),
    path('registrieren/', views.register_user, name='registration_site'),
    path('account/', views.account_data_change, name='account_site'),
    path('account/choose_image/', views.choose_image, name='choose_image_site'),
    path('kontakt/', views.contact, name='contact_site'),
    path('skills/', views.Skill_List_View.as_view(), name='skill_list_site'),
    path('skills/<slug:slug>/', views.Skill_Detail_View.as_view(), name='skill_detail_site')
]