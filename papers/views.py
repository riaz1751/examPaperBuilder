from django.shortcuts import render, redirect
from django.contrib import messages
from config.supabase import supabase
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})

            # Log the response for debugging
            print(f"Supabase response: {response}")

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
            # request.session["user"] = response.user.id
            request.session["access_token"] = response.session.access_token
            return redirect("dashboard")
        except Exception as e:
            messages.error(request, f"Login failed: {str(e)}")

    return render(request, "auth/login.html")

def dashboard(request):
    # Check if the user is logged in by checking the session
    # user_id = request.session.get("user")
    session_token = request.session.get("access_token")
    if not session_token:
        # If no user is logged in, redirect to the login page
        messages.error(request, "You need to log in first.")
        return redirect("login")
    
    # Fetch user data from Supabase (optional, for personalization)
    # user = supabase.auth.api.get_user(user_id)

    try:
        user_response = supabase.auth.get_user(session_token)
        user = user_response.user
    
        return render(request, "auth/dashboard.html", {"user": user})
    except Exception as e:
        messages.error(request, f"Error retrieving user: {str(e)}")
        return redirect("login")

def logout(request):
    try:
        # Log the user out by removing their session data
        del request.session["access_token"]
        messages.success(request, "You have logged out successfully.")
    except KeyError:
        pass  # In case there is no session data
    return redirect("login")  # Redirect to the login page after logging out

