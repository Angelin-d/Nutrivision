from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('',views.main),
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('add_healthtips/',views.add_healthtips),
    path('add_healthtips_post/',views.add_healthtips_post),
    path('edit_healthtips/<id>',views.edit_healthtips),
    path('delete_dataset/<id>',views.delete_dataset),
    path('viewdataset/',views.viewdataset),
    path('edit_healthtips_post/',views.edit_healthtips_post),
    path('view_healthtip/',views.view_healthtip),
    path('view_feedback/',views.view_feedback),
    path('view_user/',views.view_user),
    path('adminhome/',views.adminhome),
    path('delete_tips/<id>',views.delete_tips),
    path('logout/',views.logout),
    path('viewpersonaldetails/<id>',views.viewpersonaldetails),



    # path('registration/',views.registration),
    path('userhome/',views.userhome),
    path('user_re/',views.user_re),
    path('user_reg_post/',views.user_reg_post),
    path('edit_details/',views.edit_details),
    path('add_personaldetails/',views.add_personaldetails),
    path('edit_details/<id>',views.edit_details),
    path('edit_details_post/',views.edit_details_post),
    path('add_personaldetails_post/',views.add_personaldetails_post),
    path('send_feedback/',views.send_feedback),
    path('send_feedback_post/',views.send_feedback_post),
    path('view_healthtips/',views.view_healthtips),
    path('view_personaldetails/',views.view_personaldetails),
    path('delete_personaldetails/<id>',views.delete_personaldetails),


path('chatbot/', views.chatbot_response, name='chatbot'),
    path('chat_ui/', views.chat_ui, name='chat_ui'),
    path('predict_nail/', views.predict_nail),
    path('predict_nail_post/', views.predict_nail_post),
    path('predict_eye/', views.predict_eye),
    path('predict_eye_post/', views.predict_eye_post),
    path('view_history/', views.view_history),


    path('profile/', views.profile),




]
