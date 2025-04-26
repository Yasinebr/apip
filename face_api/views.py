from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Person, FaceEncoding, RecognitionLog
from .serializers import (
    PersonSerializer, RegisterFaceSerializer, RecognizeFaceSerializer,
    UpdatePersonSerializer, UpdateFaceSerializer, RecognitionLogSerializer
)
from .face_utils import base64_to_image, extract_face_encoding, find_matching_person


class RegisterFaceAPIView(APIView):
    """API برای ثبت چهره جدید"""

    def post(self, request):
        serializer = RegisterFaceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # بررسی آیا کاربری با این کد ملی از قبل وجود دارد
        national_id = serializer.validated_data['national_id']
        if Person.objects.filter(national_id=national_id).exists():
            return Response(
                {"error": "کاربری با این کد ملی قبلاً ثبت شده است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # تبدیل تصویر base64 به تصویر PIL
        image_data = serializer.validated_data['image']
        try:
            image = base64_to_image(image_data)
        except Exception as e:
            return Response(
                {"error": f"خطا در پردازش تصویر: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # استخراج embedding چهره
        face_encoding = extract_face_encoding(image)
        if face_encoding is None:
            return Response(
                {"error": "هیچ چهره‌ای در تصویر تشخیص داده نشد."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ایجاد کاربر و ذخیره embedding چهره
        with transaction.atomic():
            # ایجاد شخص جدید
            person = Person.objects.create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                national_id=national_id
            )

            # ایجاد embedding چهره
            face_encoding_obj = FaceEncoding(person=person)
            face_encoding_obj.set_encoding(face_encoding)
            face_encoding_obj.save()

        return Response({
            "success": True,
            "message": "ثبت‌نام با موفقیت انجام شد.",
            "person": PersonSerializer(person).data
        }, status=status.HTTP_201_CREATED)


class RecognizeFaceAPIView(APIView):
    """API برای تشخیص چهره"""

    def post(self, request):
        serializer = RecognizeFaceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # تبدیل تصویر base64 به تصویر PIL
        image_data = serializer.validated_data['image']
        try:
            image = base64_to_image(image_data)
        except Exception as e:
            return Response(
                {"error": f"خطا در پردازش تصویر: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # استخراج embedding چهره
        face_encoding = extract_face_encoding(image)
        if face_encoding is None:
            return Response(
                {"error": "هیچ چهره‌ای در تصویر تشخیص داده نشد."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # دریافت تمام embedding های موجود
        face_encodings = list(FaceEncoding.objects.all())  # تبدیل به لیست
        known_encodings = [face_enc.get_encoding() for face_enc in face_encodings]

        # یافتن تطابق
        match_index = find_matching_person(face_encoding, known_encodings)

        if match_index is not None:
            # تشخیص موفق
            matched_face_encoding = face_encodings[match_index]  # حالا می‌توانیم اندیس‌دهی کنیم
            person = matched_face_encoding.person

            # ثبت لاگ تشخیص
            RecognitionLog.objects.create(
                person=person,
                ip_address=request.META.get('REMOTE_ADDR')
                # مکان را می‌توان از درخواست یا از سرویس‌های geolocation دریافت کرد
            )

            return Response({
                "success": True,
                "message": f"سلام {person.first_name}",
                "person": PersonSerializer(person).data
            })
        else:
            # عدم تشخیص
            return Response({
                "success": False,
                "message": "کاربر شناسایی نشد."
            })



class UpdatePersonAPIView(APIView):
    """API برای به‌روزرسانی اطلاعات شخصی"""

    def put(self, request, national_id):
        person = get_object_or_404(Person, national_id=national_id)
        serializer = UpdatePersonSerializer(person, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "اطلاعات با موفقیت به‌روزرسانی شد.",
                "person": PersonSerializer(person).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonAPIView(APIView):
    """API برای به‌روزرسانی اطلاعات شخصی"""

    def get(self, request, national_id):
        """دریافت اطلاعات شخص با کد ملی"""
        person = get_object_or_404(Person, national_id=national_id)
        return Response(PersonSerializer(person).data)

    def put(self, request, national_id):
        """به‌روزرسانی اطلاعات شخصی"""
        person = get_object_or_404(Person, national_id=national_id)
        serializer = UpdatePersonSerializer(person, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "اطلاعات با موفقیت به‌روزرسانی شد.",
                "person": PersonSerializer(person).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateFaceAPIView(APIView):
    """API برای به‌روزرسانی تصویر چهره"""

    def put(self, request, national_id):
        person = get_object_or_404(Person, national_id=national_id)
        serializer = UpdateFaceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # تبدیل تصویر base64 به تصویر PIL
        image_data = serializer.validated_data['image']
        try:
            image = base64_to_image(image_data)
        except Exception as e:
            return Response(
                {"error": f"خطا در پردازش تصویر: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # استخراج embedding چهره
        face_encoding = extract_face_encoding(image)
        if face_encoding is None:
            return Response(
                {"error": "هیچ چهره‌ای در تصویر تشخیص داده نشد."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # به‌روزرسانی یا ایجاد embedding چهره
        try:
            face_encoding_obj = person.face_encoding
        except FaceEncoding.DoesNotExist:
            face_encoding_obj = FaceEncoding(person=person)

        face_encoding_obj.set_encoding(face_encoding)
        face_encoding_obj.save()

        return Response({
            "success": True,
            "message": "تصویر چهره با موفقیت به‌روزرسانی شد."
        })


class RecognitionLogListAPIView(APIView):
    """API برای دریافت لیست لاگ‌های تشخیص"""

    def get(self, request, national_id=None):
        if national_id:
            # دریافت لاگ‌های یک شخص خاص
            person = get_object_or_404(Person, national_id=national_id)
            logs = RecognitionLog.objects.filter(person=person)
        else:
            # دریافت همه لاگ‌ها
            logs = RecognitionLog.objects.all()

        serializer = RecognitionLogSerializer(logs, many=True)
        return Response(serializer.data)
