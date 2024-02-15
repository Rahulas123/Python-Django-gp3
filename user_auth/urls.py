
from django.contrib import admin
from django.urls import path,include
from accounts.views import login_view,signup, patient_dashboard, doctor_dashboard,create_blog_post, view_blog_posts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
     path('login/', login_view, name='login'),
    path('', signup, name='signup'),
    path('patient/', patient_dashboard, name='patient_dashboard'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
     path('create_blog_post/', create_blog_post, name='create_blog_post'),
    path('view_blog_posts/', view_blog_posts, name='view_blog_posts'),
    # path('accounts/', include('django.contrib.auth.urls')),
]
