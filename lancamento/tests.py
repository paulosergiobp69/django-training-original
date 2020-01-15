from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from .models import TipoLancamento, Lancamento

# Create your tests here.
class TestLancamento(APITestCase):

    def setUp(self):
        self.url = '/lancamentoviewapi/'
        self.user = self.setup_user('test')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.user2 = self.setup_user('test2')
        self.token2 = Token.objects.create(user=self.user2)
        self.token2.save()
        self.lancamento = self.setup_lancamento(self.user2,'Nissei',150.00,'Farmácia')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @staticmethod
    def setup_user(username):
        User = get_user_model()
        return User.objects.create_user(
            username,
            email=username+'@test.com',
            password='test'
        )

    @staticmethod
    def setup_lancamento(user, descricao, valor, tipolancamento):
        tipolancamento = TipoLancamento.objects.create(descricao=tipolancamento)
        return Lancamento.objects.create(descricao=descricao,
                                         valor=valor,
                                         tipolancamento=tipolancamento,
                                         created_by=user)

    def test_list(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)        

    def test_destroy(self):
        response = self.client.delete(self.url+str(self.lancamento.id)+'/', format='json')
        self.assertEqual(response.status_code, 403)        
