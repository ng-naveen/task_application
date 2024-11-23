from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('task', views.TaskViewSetView, basename='task')
router.register('task', views.TaskModelViewSetView, basename='task')
router.register('user', views.UserView, basename='user')

urlpatterns = [
    # path('tasks/', views.TaskView.as_view()),
    # path('task/<int:id>/', views.TaskDetailView.as_view()),
    path('', include(router.urls))
]
