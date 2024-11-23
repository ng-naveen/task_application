from django.urls import path
from task_web_application import views

urlpatterns = [
    path('', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('task/add/', views.CreateTaskView.as_view(), name='task-add'),
    path('task/all/', views.ListTaskView.as_view(), name='task-list'),
    path('task/details/<int:id>/', views.DetailTaskView.as_view(), name='task-details'),
    path('task/update/<int:id>/', views.UpdateView.as_view(), name='task-update'),
    path('task/remove/<int:id>/', views.DeleteTaskView.as_view(), name='task-delete'),
    path('signout/', views.SignOutView.as_view(), name='signout'),
]
