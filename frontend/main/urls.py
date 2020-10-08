from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='main/index.html'), name='home'),
    path('pricing', TemplateView.as_view(template_name='main/pricing.html'), name='pricing'),
    path('privacy', TemplateView.as_view(template_name='main/privacy.html'), name='privacy'),
    path('tos', TemplateView.as_view(template_name='main/tos.html'), name='tos'),
    path('statping', TemplateView.as_view(template_name='main/statping.html'), name='statping'),
]
