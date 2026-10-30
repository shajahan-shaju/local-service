
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workers, Booking, Notification
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import WorkerProfile
from functools import wraps
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout

# HOME PAGE
def home(request):
    return render(request, "home.html")


# WORKS PAGE
def works(request):
    return render(request, "works.html")


# WORKERS PAGE
def workers(request):
    worker_list = Workers.objects.all()

    return render(request, "workers.html", {
        "workers": worker_list
    })


# SIGNUP PAGE

def singup(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "signup":
            from django.contrib.auth.models import User

            full_name = request.POST.get("full_name", "").strip()
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            password = request.POST.get("password", "")
            confirm_password = request.POST.get("confirm_password", "")

            if not all([full_name, username, email, phone, password, confirm_password]):
                return render(request, "singup.html", {
                    "error": "All fields are required",
                    "active_form": "signup"
                })

            if password != confirm_password:
                return render(request, "singup.html", {
                    "error": "Passwords do not match",
                    "active_form": "signup"
                })

            if User.objects.filter(username=username).exists():
                return render(request, "singup.html", {
                    "error": "Username already exists",
                    "active_form": "signup"
                })

            if User.objects.filter(email=email).exists():
                return render(request, "singup.html", {
                    "error": "Email already registered",
                    "active_form": "signup"
                })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name
            )

            messages.success(request, "Account created! Please log in.")
            return redirect("singup")

        elif action == "login":
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                auth_login(request, user)
                return redirect("booking")

            return render(request, "singup.html", {
                "error": "Invalid username or password",
                "active_form": "login"
            })

    return render(request, "singup.html", {
        "active_form": "login"
    })



# BOOKING PAGE
@login_required(login_url="login")
def booking(request):
    if request.method == "POST":
        work_name = request.POST.get("work_name")
        customer_mobile = request.POST.get("customer_mobile")
        work_details = request.POST.get("work_details")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")

        if not work_name:
            return render(request, "booking.html", {
                "error": "Please select a work type."
            })

        Booking.objects.create(
            customer=request.user,
            work_name=work_name,
            customer_mobile=customer_mobile,
            work_details=work_details,
            booking_date=booking_date,
            booking_time=booking_time,
        )

        messages.success(
            request,
            "Booking successful! Your service request has been submitted."
        )

        return redirect("booking")

    return render(request, "booking.html")


# LOGIN PAGE

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("booking")

        return render(request, "singup.html", {
            "error": "Invalid username or password",
            "active_form": "login"
        })

    return redirect("singup")

# WORKER-ONLY ACCESS

def worker_required(view_func):
    @wraps(view_func)
    @login_required(login_url="worker_login")
    def wrapper(request, *args, **kwargs):
        if not WorkerProfile.objects.filter(
            user=request.user
        ).exists():
            messages.error(
                request,
                "Worker account required to access this page."
            )
            return redirect("worker_login")

        return view_func(request, *args, **kwargs)

    return wrapper
# WORKER REGISTRATION

def worker_register(request):
    if request.user.is_authenticated:
        if WorkerProfile.objects.filter(user=request.user).exists():
            return redirect("worker_dashboard")
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        role = request.POST.get("role", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([
            name, username, email, phone, role,
            password, confirm_password
        ]):
            return render(request, "worker_register.html", {
                "error": "All fields are required."
            })

        if password != confirm_password:
            return render(request, "worker_register.html", {
                "error": "Passwords do not match."
            })

        if len(password) < 8:
            return render(request, "worker_register.html", {
                "error": "Password must contain at least 8 characters."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "worker_register.html", {
                "error": "Username already exists."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "worker_register.html", {
                "error": "Email already registered."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        WorkerProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            role=role
        )

        messages.success(
            request,
            "Worker account created! Please log in."
        )
        return redirect("worker_login")

    return render(request, "worker_register.html")
# WORKER LOGIN

def worker_login(request):
    if request.user.is_authenticated:
        if WorkerProfile.objects.filter(user=request.user).exists():
            return redirect("worker_dashboard")
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and WorkerProfile.objects.filter(
            user=user
        ).exists():
            auth_login(request, user)
            return redirect("worker_dashboard")

        return render(request, "worker_login.html", {
            "error": "Invalid worker username or password."
        })

    return render(request, "worker_login.html")
# WORKER DASHBOARD
@worker_required
def worker_dashboard(request):
    bookings = Booking.objects.all().order_by("-id")

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(request, "worker_dashboard.html", {
        "bookings": bookings,
        "notifications": notifications[:10],
        "unread_count": unread_count,
    })


# UPDATE BOOKING STATUS
@worker_required
def update_booking_status(request, booking_id):
    if request.method != "POST":
        return redirect("worker_dashboard")

    booking_obj = get_object_or_404(
        Booking,
        id=booking_id
    )

    action = request.POST.get("action")

    status_map = {
        "accept": "Accepted",
        "reject": "Rejected",
        "complete": "Completed",
    }

    if action not in status_map:
        messages.error(request, "Invalid booking action.")
        return redirect("worker_dashboard")

    new_status = status_map[action]

    booking_obj.status = new_status
    booking_obj.save(update_fields=["status"])

    Notification.objects.create(
        recipient=booking_obj.customer,
        message=(
            f"Your {booking_obj.work_name} booking "
            f"has been {new_status.lower()}."
        )
    )

    messages.success(
        request,
        f"Booking status updated to {new_status}."
    )

    return redirect("worker_dashboard")


# CUSTOMER DASHBOARD

@login_required(login_url="login")
def customer_dashboard(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).order_by("-id")

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(request, "customer_dashboard.html", {
        "bookings": bookings,
        "notifications": notifications,
        "unread_count": unread_count,
    })
@login_required(login_url="login")
def mark_notifications_read(request):
    if request.method == "POST":
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

    return redirect("customer_dashboard")

def logout_view(request):
    logout(request)
    return redirect("home")
def customer_logout(request):
    auth_logout(request)
    return redirect("home")