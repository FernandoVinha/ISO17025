from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import Contacts, Companies

class ContactsTestCase(TestCase):

    def setUp(self):
        # Configurar dados de exemplo
        self.company = Companies.objects.create(name="Empresa Teste", email="empresa@teste.com", phone="123456789")
        self.contact = Contacts.objects.create(
            name="Contato Teste",
            email="contato@teste.com",
            phone="987654321",
            position="Gerente",
            company=self.company
        )
        # Criar um usuário de teste
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        # Adicionar permissões necessárias ao usuário
        permissions = Permission.objects.filter(content_type__app_label='accounts')
        self.user.user_permissions.add(*permissions)

        # Fazer login
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_contacts_list_view(self):
        """
        Testa se a lista de contatos é renderizada corretamente.
        """
        response = self.client.get(reverse('contacts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contato Teste")
        self.assertTemplateUsed(response, 'accounts/contacts_list.html')

    def test_search_contacts(self):
        """
        Testa a funcionalidade de busca de contatos.
        """
        response = self.client.get(reverse('contacts_list'), {'search': 'Contato'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contato Teste")

        # Teste de busca sem resultados
        response_no_result = self.client.get(reverse('contacts_list'), {'search': 'Inexistente'})
        self.assertEqual(response_no_result.status_code, 200)
        self.assertNotContains(response_no_result, "Contato Teste")
        self.assertContains(response_no_result, "Nenhum contato encontrado.")

    def test_create_contact(self):
        """
        Testa a criação de um novo contato via view.
        """
        response = self.client.post(reverse('contacts_create'), {
            'name': 'Novo Contato',
            'email': 'novo@contato.com',
            'phone': '1122334455',
            'position': 'Analista',
            'company': self.company.id
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após a criação
        self.assertTrue(Contacts.objects.filter(name='Novo Contato').exists())

    def test_contact_card_click(self):
        """
        Testa se o clique no card de contato redireciona corretamente para a edição.
        """
        contact_edit_url = reverse('contacts_edit', args=[self.contact.id])
        response = self.client.get(contact_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contato Teste")
