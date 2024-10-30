# urls.py

from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, simple_logout, admin_view, about
from django.contrib.auth import views as auth_views

# Define URL patterns for the inventory app
urlpatterns = [
    # Path for the index view (homepage)
    path('', Index.as_view(), name='index'),
    # Path for the dashboard view
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    # Path for adding a new inventory item
    path('add-item/', AddItem.as_view(), name='add-item'),
    # Path for editing an existing inventory item using its primary key
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    # Path for deleting an existing inventory item using its primary key
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    # Path for user signup view
    path('signup/', SignUpView.as_view(), name='signup'),
    # Path for user login view
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    # Path for user logout view
    path('simple_logout/', simple_logout, name='simple_logout'),
    # Path for admin view
    path('admin-view/', admin_view, name='admin-view'),
    # Path for the about screen
    path('about/', about, name='about'),

]
