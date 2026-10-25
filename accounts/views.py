from django.shortcuts import redirect, render

from .forms import UserRegistrationForm

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = "OWNER"
            user.save()

            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(
    request,
    "registration/register.html",
    {"form": form},
)
