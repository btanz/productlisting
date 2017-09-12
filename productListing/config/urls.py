"""productListing URL Configuration

The `urlpatterns` list routes URLs to views. More information:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/

"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('products.urls')),
]