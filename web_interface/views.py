from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """صفحه اصلی"""
    template_name = 'web_interface/home.html'


class RegisterView(TemplateView):
    """صفحه ثبت‌نام چهره"""
    template_name = 'web_interface/register.html'


class RecognizeView(TemplateView):
    """صفحه تشخیص چهره"""
    template_name = 'web_interface/recognize.html'


class UpdateView(TemplateView):
    """صفحه بروزرسانی اطلاعات شخصی"""
    template_name = 'web_interface/update.html'


class UpdateFaceView(TemplateView):
    """صفحه بروزرسانی تصویر چهره"""
    template_name = 'web_interface/update_face.html'