from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('processreg', views.register),
    path('processlogin', views.login),
    path('thoughts', views.show_thoughts_page),
    path('logout', views.logout),
    path('createnewthought', views.process_new_thought),
    path('thought/<int:thought_id>/remove', views.delete),
    path('thoughts/<int:thought_id>', views.details_page),
    path('thought/<int:thought_id>/liked', views.process_like),
    path('thought/<int:thought_id>/unliked', views.process_unlike),
    # path('wishes',views.dashboard_page),
    # path('wishes/new', views.new_wish_page),
    # path('createnewwish', views.process_new_wish),
    # path('logout', views.logout),
    # path('wishes/edit/<int:wish_id>', views.edit_wish_page),
    # path('wishes/<int:wish_id>/update', views.process_wish_update),
    # path('wishes/<int:wish_id>/remove', views.process_delete),
    # path('grantwish/<int:wish_id>', views.grant_wish),
    # path('process_like_granted_wish/<int:wish_id>', views.process_like_granted_wish),
    # path('wishes/stats', views.show_stats_page),
]