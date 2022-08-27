from django.urls import path
from .import views


urlpatterns = [

    path('', views.home, name="home"),
    path('analysis1/', views.analysis1, name="analysis1"),
    path('menu/',views.ethanolmenu,name="ethanolmenu"),
    path('analysis2/', views.analysis2, name="analysis2"),
    path('analysis3/',views.analysis3, name="analysis3"),
    path('analysis4/',views.analysis4, name="analysis4"),
    path('analysis5/',views.analysis5, name="analysis5"),
    path('analysis6/',views.analysis6, name="analysis6"),
    path('analysis7/',views.analysis7, name="analysis7"),
    path('analysis8/',views.analysis8, name="analysis8"),
    path('analysis9/',views.analysis9, name="analysis9"),
    path('analysis10/',views.analysis10, name="analysis10"),
    path('analysis11/',views.analysis11, name="analysis11"),
    path('analysis12/',views.analysis12, name="analysis12"),
    path('analysis13/',views.analysis13, name="analysis13"),
    path('analysis14/',views.analysis14, name="analysis14"),
    path('analysis15/',views.analysis15, name="analysis15"),
    path('analysis16/',views.analysis16, name="analysis16"),
    path('analysis17/',views.analysis17, name="analysis17"),
    path('analysis18/',views.analysis18, name="analysis18"),
    path('analysis19/',views.analysis19, name="analysis19"),
    path('ethanol/<pk>/update/', views.EthanolView.as_view(), name="update_ethanol"),
    path('ethanollist_yearwise/<int:year>/',views.ethanolList_yearwise, name="ethanolList_yearwise"),
    path('ethanollist/',views.ethanolList, name="ethanollist"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    
    ]
