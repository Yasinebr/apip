from django.db import models
import numpy as np
import json


class Person(models.Model):
    """مدل ذخیره‌سازی اطلاعات شخصی کاربر"""
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_id = models.CharField(max_length=10, unique=True, db_index=True, verbose_name="کد ملی")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class FaceEncoding(models.Model):
    """مدل ذخیره‌سازی اطلاعات embedding چهره"""
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='face_encoding', verbose_name="شخص")
    encoding_data = models.TextField(verbose_name="داده encoding")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "کدگذاری چهره"
        verbose_name_plural = "کدگذاری‌های چهره"

    def set_encoding(self, encoding_array):
        """ذخیره آرایه numpy به صورت JSON"""
        self.encoding_data = json.dumps(encoding_array.tolist())

    def get_encoding(self):
        """تبدیل داده‌های JSON به آرایه numpy"""
        return np.array(json.loads(self.encoding_data))

    def __str__(self):
        return f"Face encoding for {self.person}"


class RecognitionLog(models.Model):
    """مدل ذخیره‌سازی لاگ تشخیص‌های موفق"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='recognition_logs', verbose_name="شخص")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان تشخیص")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="مکان")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="آدرس IP")

    class Meta:
        verbose_name = "لاگ تشخیص"
        verbose_name_plural = "لاگ‌های تشخیص"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.person} recognized at {self.timestamp}"
