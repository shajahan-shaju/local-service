from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("works/", views.works, name="works"),
    path("workers/", views.workers, name="workers"),
    path('singup/',views.singup,name='singup'),
    path('booking/',views.booking,name='booking'),
    path('login/', views.login_view, name='login'),
    path('worker_dashboard/',views.worker_dashboard,name='worker_dashboard'),
    path(
    "worker/booking/<int:booking_id>/status/",
    views.update_booking_status,
    name="update_booking_status",
),
path(
    "worker-register/",
    views.worker_register,
    name="worker_register",
),

# WORKER LOGIN
path(
    "worker-login/",
    views.worker_login,
    name="worker_login",
),
path(
    "customer_dashboard/",
    views.customer_dashboard,
    name="customer_dashboard",
),
path(
    "mark-notifications-read/",
    views.mark_notifications_read,
    name="mark_notifications_read"
),
path("logout/", views.logout_view, name="logout"),
path("customer-logout/", views.customer_logout, name="customer_logout"),

]