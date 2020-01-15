from django.urls import path
from django.conf.urls import url

from . import views
  
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tipo_lancamento_insert/', views.TipoLancamentoView.as_view(), name='tipo_lancamento_insert'),
    path('tipo_lancamento_list/', views.tipo_lancamento_list, name='tipo_lancamento_list'),
    path('tipo_lancamento_det/<int:pk>/', views.tipo_lancamento_detail, name='tipo_lancamento_det'),
    url(r'lancamentoquery', views.LancamentoQueryViewSet.as_view()),
    url(r'saldoquery', views.SaldoQueryViewSet.as_view())
]