from django.shortcuts import render, redirect
from django.contrib import messages
from config.supabase import supabase
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the homepage!")

def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Signup failed: {str(e)}")
    
    return render(request, "auth/signup.html")

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            request.session["user"] = response.user.id
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, f"Login failed: {str(e)}")

    return render(request, "auth/login.html")
