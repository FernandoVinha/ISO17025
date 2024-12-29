# nonconformity/models.py

from django.db import models
from django.apps import apps
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _

def get_installed_apps():
    # Função para obter uma lista de apps instalados
    installed_apps = [(app.label, app.verbose_name) for app in apps.get_app_configs()]
    # Adiciona uma opção vazia no início da lista para permitir "Nenhum App selecionado"
    installed_apps.insert(0, ('', 'No App Selected'))
    return installed_apps

class NonConformity(models.Model):
    app = models.CharField(
        max_length=100,
        choices=get_installed_apps(),
        blank=True,  # Permite que o campo seja deixado em branco
        verbose_name=_("Related App")
    )
    description = models.TextField(verbose_name=_("Description"))
    photo = models.ImageField(upload_to='nonconformity_photos/', blank=True, null=True, verbose_name=_("Photo"))
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Created By"))  # Usuário que criou

    def __str__(self):
        app_display = self.get_app_display() or "No App"
        return f"{app_display} - {self.description[:50]}"
