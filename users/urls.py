from django.urls import path
from .views import  ProfileEditView, my_functional_view, confirm_needed, login_view, profile



urlpatterns = [
      path('signup/', my_functional_view, name='signup'),
      path('login/', login_view, name='login'),
      path('confirm_needed/<int:id>', confirm_needed, name='confirm_needed'),
      path('edit/<str:username>/', ProfileEditView.as_view(), name=''),
      path('profile/<str:username>/', profile, name='user_detail'),

]