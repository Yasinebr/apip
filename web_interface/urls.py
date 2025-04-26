from django.urls import path
from .views import HomeView, RegisterView, RecognizeView, UpdateView, UpdateFaceView

app_name = 'web_interface'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recognize/', RecognizeView.as_view(), name='recognize'),
    path('update/', UpdateView.as_view(), name='update'),
    path('update-face/', UpdateFaceView.as_view(), name='update_face'),
]