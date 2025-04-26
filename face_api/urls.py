from django.urls import path
from .views import (
    RegisterFaceAPIView,
    RecognizeFaceAPIView,
    UpdatePersonAPIView,
    UpdateFaceAPIView,
    RecognitionLogListAPIView
)

app_name = 'face_api'

urlpatterns = [
    # ثبت چهره جدید
    path('register/', RegisterFaceAPIView.as_view(), name='register_face'),

    # تشخیص چهره
    path('recognize/', RecognizeFaceAPIView.as_view(), name='recognize_face'),

    # به‌روزرسانی اطلاعات شخصی
    path('update-person/<str:national_id>/', UpdatePersonAPIView.as_view(), name='update_person'),

    # به‌روزرسانی تصویر چهره
    path('update-face/<str:national_id>/', UpdateFaceAPIView.as_view(), name='update_face'),

    # دریافت لاگ‌های تشخیص
    path('logs/', RecognitionLogListAPIView.as_view(), name='all_logs'),
    path('logs/<str:national_id>/', RecognitionLogListAPIView.as_view(), name='person_logs'),
]
