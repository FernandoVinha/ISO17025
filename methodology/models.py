#methodology/models.py
from django.db import models
from simple_history.models import HistoricalRecords
from inventory.models import InventoryItem  # Import dos itens de inventário
from accounts.models import CustomUser  # Import dos usuários que criam a metodologia
from django.core.exceptions import PermissionDenied

class Methodology(models.Model):
    title = models.CharField(max_length=255, help_text="Título da Metodologia")
    description = models.TextField(help_text="Descrição detalhada da metodologia")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='methodologies',
        help_text="Usuário que criou a metodologia"
    )
    equipment = models.ManyToManyField(
        InventoryItem,
        related_name='methodology_equipment',
        blank=True,
        help_text="Lista de equipamentos utilizados na metodologia"
    )
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_methodology", "Pode visualizar metodologias"),
            ("can_add_methodology", "Pode adicionar metodologias"),
            ("can_change_methodology", "Pode alterar metodologias"),
            ("can_delete_methodology", "Pode deletar metodologias"),
        ]

    def __str__(self):
        return self.title

class MethodologySupply(models.Model):
    methodology = models.ForeignKey(Methodology, on_delete=models.CASCADE, related_name='supplies', help_text="Metodologia à qual o insumo pertence")
    supply = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='used_in_methodologies', help_text="Insumo utilizado")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantidade do insumo utilizado")
    unit = models.CharField(max_length=10, help_text="Unidade de medida, ex: litros, gramas", default="Unidade")
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Verifica se o usuário que está criando/editando tem permissão para modificar a metodologia
        if not self.methodology.author.has_perm('can_change_methodology'):
            raise PermissionDenied("Você não tem permissão para editar insumos dessa metodologia.")
        super(MethodologySupply, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Verifica se o usuário tem permissão para deletar a metodologia
        if not self.methodology.author.has_perm('can_delete_methodology'):
            raise PermissionDenied("Você não tem permissão para deletar insumos dessa metodologia.")
        super(MethodologySupply, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} {self.unit} de {self.supply.name} para {self.methodology.title}"

    class Meta:
        unique_together = ('methodology', 'supply')
        permissions = [
            ("can_view_methodology_supply", "Pode visualizar insumos de metodologias"),
        ]
