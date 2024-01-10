from django.http.request import HttpRequest
from django.shortcuts import render
from django.urls import Resolver404


def csrf_exception(request: HttpRequest,
                   reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request: HttpRequest,
                   exception: Resolver404):
    return render(request, 'pages/404.html', status=404)


def server_error(request: HttpRequest):
    return render(request, 'pages/500.html', status=500)
