from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def user_signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken ❌")
            return redirect("/signup/")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created ✅")
        return redirect("/login/")

    return render(request, "home/signup.html")


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful ✅")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, "home/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out ✅")
    return redirect("/login/")



def home_page(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    search = request.GET.get("search")
    if search:
        students_list = Student.objects.filter(name__icontains=search)
    else:
        students_list = Student.objects.all()

    paginator = Paginator(students_list, 5)  # 5 records per page
    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render(request, "home/index.html", {"students": students})




def add_student(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully ✅")
            return redirect("/")
    else:
        form = StudentForm()

    return render(request, "home/add.html", {"form": form})


def edit_student(request, id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    student = Student.objects.get(id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated ✅")
            return redirect("/")
    else:
        form = StudentForm(instance=student)

    return render(request, "home/edit.html", {"form": form})


def delete_student(request, id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, "Record deleted ❌")
    return redirect("/")
