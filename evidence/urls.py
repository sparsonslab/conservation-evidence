from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('index.html', TemplateView.as_view(template_name='evidence/index.html'), name='index'),
]
