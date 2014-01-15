# coding: utf-8


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request, *args, **kwargs):
    return render(request, "app/dashboard.html", kwargs)
