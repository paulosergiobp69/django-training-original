from django.shortcuts import render, get_object_or_404
from django import views
from django.http import JsonResponse
from .serializers import TipoLancamentoSerializer, LancamentoSerializer, ReceitaSerializer
from rest_framework import generics, viewsets
from rest_framework.views import APIView, Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
from django.shortcuts import render
#from django.http import HttpResponse
from lancamento.external_apis import TestRequest
from lancamento.models import TipoLancamento, Lancamento, Receita
from .raw_sql_queries import get_lancamentos
from .raw_sql_queries import get_saldo

def tipo_lancamento_list(request):
    MAX_OBJECTS = 20
    tipos_lancamento = TipoLancamento.objects.all()[:MAX_OBJECTS]
    data = {"results": list(tipos_lancamento.values("id", "descricao"))}

    return JsonResponse(data)

def tipo_lancamento_detail(request, pk):
    tipo_lancamento = get_object_or_404(TipoLancamento, pk=pk)
    data = {"results": {
        "id": tipo_lancamento.id,
        "descricao": tipo_lancamento.descricao
    }}

    return JsonResponse(data)

class IndexView(views.View):

    def get(self, request):
        request_api = TestRequest()
        exchange_dict = request_api.get_rates()
        result = []
        for row in exchange_dict['rates']:
            result.append(row +' : '+ str(exchange_dict['rates'][row]))
        title = 'Exchange Rates'
        lancamento = TipoLancamento.objects.all()
        #return HttpResponse("<h1>%s</h1>" % result)
    
        return render(request, 'index.html', {'title': title, 'rates': result, 'tipolancamento': lancamento})

class TipoLancamentoView(views.View):

    def get(self, request):
        return render(request, 'manutencao_tipo_lancamento.html')

    def post(self, request):
        descricao = request.POST.get('descricao')
        TipoLancamento.objects.create(descricao=descricao)

        return self.get(request)

class TipoLancamentoAPI(viewsets.ModelViewSet):
    queryset = TipoLancamento.objects.all().order_by('id')
    serializer_class = TipoLancamentoSerializer

class LancamentoAPI(viewsets.ModelViewSet):
    queryset = Lancamento.objects.all().order_by('-id')
    serializer_class = LancamentoSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('descricao', 'valor', 'created_by__username')
       
    def destroy(self, request, *args, **kwargs):
         lancamento = Lancamento.objects.get(pk=self.kwargs["pk"])
         if not request.user == lancamento.created_by:
             raise PermissionDenied("Voce não tem permissão para apagar esse lancamento.")
         return super().destroy(request, *args, **kwargs)

@permission_classes((permissions.AllowAny,))
class ReceitaAPI(viewsets.ModelViewSet):
    queryset = Receita.objects.all().order_by('-id')
    serializer_class = ReceitaSerializer
       
    def destroy(self, request, *args, **kwargs):
         receita = Receita.objects.get(pk=self.kwargs["pk"])
         if not request.user == receita.created_by:
             raise PermissionDenied("Voce não tem permissão para apagar essa receita.")
         return super().destroy(request, *args, **kwargs)

class LancamentoQueryViewSet(APIView):

    def get(self, request):
        user = self.request.query_params.get('user', None)

        result = get_lancamentos(user=user)
        # print(result)
        return Response(result, content_type="application/json", status=status.HTTP_200_OK)

class SaldoQueryViewSet(APIView):

    def get(self, request):
        user = self.request.query_params.get('user', None)

        result = get_saldo(user=user)
        # print(result)
        return Response(result, content_type="application/json", status=status.HTTP_200_OK)
