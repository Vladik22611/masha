from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Аутентификация пользователя
            user = authenticate(username=username, password=password)
            if user is not None:
                # Логиним пользователя
                login(request, user=user)
                return redirect("index")  # Направляем на главную страницу или другую э
            else:
                form.add_error(None, "Неверный логин или пароль.")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("index")  # Замените на нужный URL или имя представления
