import os
import random
import PyPDF2
from fpdf import FPDF
import re
import pdfplumber
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from config.supabase import supabase
from django.http import HttpResponse
from .forms import ExamPaperUploadForm
from .models import UploadedExamPaper
from django.http import FileResponse


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

def paper_builder(request):
    return render(request, "auth/paper_builder.html")

def paper_builder(request):
    if request.method == "POST":
        form = ExamPaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves the file to media/temp/
            messages.success(request, "PDF uploaded successfully! Now generating exam paper...")
            return redirect("generate_exam_paper")
    else:
        form = ExamPaperUploadForm()

    return render(request, "auth/paper_builder.html", {"form": form})

def generate_exam_paper(request):
    if request.method == "POST" and request.FILES.getlist("pdf_files"):
        uploaded_files = request.FILES.getlist("pdf_files")

        extracted_questions = []
        for file in uploaded_files:
            file_path = os.path.join("media/uploads", file.name)
            with open(file_path, "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            extracted_questions.extend(extract_questions_from_pdf(file_path))
            os.remove(file_path)  # Delete temporary file after extraction

        if not extracted_questions:
            return render(request, "paper_builder.html", {"error": "No valid questions found in PDFs."})

        new_pdf_path = create_custom_exam_paper(extracted_questions)

        return FileResponse(open(new_pdf_path, "rb"), as_attachment=True, filename="custom_exam.pdf")

    return render(request, "auth/paper_builder.html")

""" def generate_exam_paper(request):
    temp_files = UploadedExamPaper.objects.all()  # Get all uploaded PDFs

    if not temp_files:
        messages.error(request, "No uploaded PDFs found. Please upload first.")
        return redirect("paper_builder")

    selected_questions = extract_questions_from_pdfs(temp_files)
    
    # Generate new PDF and get file path
    new_pdf_path = create_custom_exam_paper(selected_questions)

    # Cleanup: Delete the uploaded PDFs
    for temp_file in temp_files:
        os.remove(temp_file.file.path)  # Delete from file system
        temp_file.delete()  # Remove from database

    return render(request, "auth/generated_paper.html", {"new_pdf_path": new_pdf_path}) """

def extract_questions_from_pdf(pdf_path):
    """
    Extracts individual questions from a GCSE/A-Level exam paper PDF
    by identifying question numbers and total marks using the format:
    "Total for Question X is Y marks".
    """
    questions = []
    current_question = []
    in_question = False

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue  # Skip blank pages

            lines = text.split("\n")

            for line in lines:
                # Detect question start (e.g., "1.", "2.", "Q3")
                if re.match(r"^\d+\.", line.strip()):  # Matches "1.", "2.", etc.
                    if current_question:  # Save the previous question
                        questions.append("\n".join(current_question))
                        current_question = []

                    in_question = True  # Start collecting new question
                    current_question.append(line.strip())

                # Detect question end using "Total for Question X is Y marks"
                elif re.search(r"Total for Question \d+ is \d+ marks", line.strip(), re.IGNORECASE):
                    current_question.append(line.strip())  # Include marks statement in the question
                    questions.append("\n".join(current_question))
                    current_question = []
                    in_question = False  # End of question

                elif in_question:
                    current_question.append(line.strip())  # Add to current question

    return questions

""" def extract_questions_from_pdfs(pdf_files):
    
    # Extracts questions from all uploaded PDFs and returns a random selection.
    
    all_questions = []

    for pdf in pdf_files:
        with open(pdf.file.path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_questions.append(text)

    return random.sample(all_questions, min(10, len(all_questions)))  # Pick 10 random questions """

def create_custom_exam_paper(questions, output_path="media/custom_exam.pdf"):
    """
    Creates a new exam PDF by selecting random questions from extracted ones.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Custom Exam Paper", ln=True, align="C")
    pdf.ln(10)

    selected_questions = random.sample(questions, min(len(questions), 5))  # Select 5 random questions

    for i, question in enumerate(selected_questions, start=1):
        pdf.multi_cell(0, 10, f"Question {i}:\n{question}")
        pdf.ln(5)  # Space between questions

    pdf.output(output_path)
    return output_path

""" def create_custom_exam_paper(questions):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Use a font that supports UTF-8 (like Arial Unicode or DejaVu)
    pdf.add_font("Arial", "", "/Library/Fonts/Arial Unicode.ttf", uni=True)  # Adjust font path if needed
    pdf.set_font("Arial", size=12)

    for i, question in enumerate(questions, 1):
        pdf.cell(200, 10, f"Question {i}:", ln=True, align="L")
        pdf.multi_cell(0, 10, question.encode("latin-1", "ignore").decode("latin-1"))  # Encode safely
        pdf.ln(5)

    output_path = os.path.join(settings.MEDIA_ROOT, "generated_exam.pdf")
    pdf.output(output_path, "F")

    return output_path """

def download_exam_paper(request):
    pdf_path = os.path.join(settings.MEDIA_ROOT, "generated_exam.pdf")

    # Ensure the file exists before serving
    if not os.path.exists(pdf_path):
        messages.error(request, "The exam paper could not be found.")
        return redirect("paper_builder")

    # Serve the file as a response
    response = FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="custom_exam_paper.pdf"'
    return response