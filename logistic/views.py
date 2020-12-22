from django.shortcuts import render, redirect


def Welcome(request):
    return render(request, 'logistic/draft.html')
