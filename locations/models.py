# locations/models.py

from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.crypto import get_random_string

def building_image_upload_path(instance, filename):
    """
    Define o caminho de upload para imagens de edifícios.
    Armazena as imagens em media/buildings/<nome_do_edificio>/<nome_do_arquivo>.
    """
    return f'buildings/{instance.name}/{filename}'

def room_image_upload_path(instance, filename):
    """
    Define o caminho de upload para imagens de salas.
    Armazena as imagens em media/buildings/<nome_do_edificio>/rooms/<nome_da_sala>/<nome_do_arquivo>.
    """
    return f'buildings/{instance.building.name}/rooms/{instance.name}/{filename}'

class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    responsible_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsible_buildings',
        help_text="Usuário responsável pelo edifício"
    )
    image = models.ImageField(
        upload_to=building_image_upload_path,
        blank=True,
        null=True,
        help_text="Imagem do edifício"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Edifício"
        verbose_name_plural = "Edifícios"
        permissions = [
            ("can_view_building", "Pode visualizar edifícios"),
            ("can_add_building", "Pode adicionar edifícios"),
            ("can_change_building", "Pode alterar edifícios"),
            ("can_delete_building", "Pode deletar edifícios"),
        ]

class Room(models.Model):
    name = models.CharField(max_length=255)
    floor = models.CharField(max_length=50, help_text="Número ou identificador do andar")
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    capacity = models.IntegerField(help_text="Capacidade máxima da sala")
    responsible_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsible_rooms',
        help_text="Usuário responsável pela sala"
    )
    image = models.ImageField(
        upload_to=room_image_upload_path,
        blank=True,
        null=True,
        help_text="Imagem da sala"
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.building.name}"

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        permissions = [
            ("can_view_room", "Pode visualizar salas"),
            ("can_add_room", "Pode adicionar salas"),
            ("can_change_room", "Pode alterar salas"),
            ("can_delete_room", "Pode deletar salas"),
        ]

class Measurement(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    temperature = models.FloatField(help_text="Temperatura em Celsius")
    humidity = models.FloatField(help_text="Percentual de umidade")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="Data e hora da medição")
    history = HistoricalRecords()

    def __str__(self):
        return f"Medição em {self.room.name} às {self.recorded_at.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Medição"
        verbose_name_plural = "Medições"
        permissions = [
            ("can_view_measurement", "Pode visualizar medições"),
            ("can_add_measurement", "Pode adicionar medições"),
            ("can_change_measurement", "Pode alterar medições"),
            ("can_delete_measurement", "Pode deletar medições"),
        ]
