from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from django.views.decorators.cache import cache_page, cache_control

urlpatterns = [
    path('lessons/<int:year>/<int:month>/<int:day>', views.LessonYMDView.as_view(), name='LessonYMDView'),
    path('lessons/<int:id>', views.LessonIdView.as_view(), name='LessonIdView'),
    path('groups', views.GroupView.as_view(), name='GroupView'),
    path('groups/<int:id>', views.GroupIdView.as_view(), name='GroupIdView'),
    path('subjects', views.SubjectView.as_view(), name='Subjects'),
    path('subjects/<int:id>', views.SubjectIdView.as_view(), name='SubjectId'),
]