# locations/forms.py

from django import forms
from .models import Building, Room, Measurement

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'responsible_user', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'responsible_user': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'name': 'Nome do Edifício',
            'address': 'Endereço',
            'responsible_user': 'Usuário Responsável',
            'image': 'Imagem do Edifício',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Building.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Um edifício com este nome já existe.')
        return name

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'floor', 'building', 'capacity', 'responsible_user', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.TextInput(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'responsible_user': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'name': 'Nome da Sala',
            'floor': 'Andar',
            'building': 'Edifício',
            'capacity': 'Capacidade Máxima',
            'responsible_user': 'Usuário Responsável',
            'image': 'Imagem da Sala',
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity < 1:
            raise forms.ValidationError('A capacidade deve ser pelo menos 1.')
        return capacity

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['room', 'temperature', 'humidity']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.1'}),
        }
        labels = {
            'room': 'Sala',
            'temperature': 'Temperatura (°C)',
            'humidity': 'Umidade (%)',
        }

    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')
        if temperature is not None and (temperature < -50 or temperature > 100):
            raise forms.ValidationError('Temperatura fora do intervalo permitido (-50°C a 100°C).')
        return temperature

    def clean_humidity(self):
        humidity = self.cleaned_data.get('humidity')
        if humidity is not None and (humidity < 0 or humidity > 100):
            raise forms.ValidationError('Umidade deve estar entre 0% e 100%.')
        return humidity
