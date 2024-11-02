from django import forms
from .models import Maintenance, Calibration, Training, StandardOperatingProcedure, CalibrationStandard, DailyVerification
from inventory.models import InventoryItem

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'

class CalibrationForm(forms.ModelForm):
    class Meta:
        model = Calibration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CalibrationForm, self).__init__(*args, **kwargs)
        # Filtrar apenas itens que podem ser calibrados (TOOL, MEASURING, ELECTRONIC)
        self.fields['item'].queryset = InventoryItem.objects.filter(item_type__in=['TOOL', 'MEASURING', 'ELECTRONIC'])

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

class SOPForm(forms.ModelForm):
    class Meta:
        model = StandardOperatingProcedure
        fields = '__all__'

class CalibrationStandardForm(forms.ModelForm):
    class Meta:
        model = CalibrationStandard
        fields = '__all__'

class DailyVerificationForm(forms.ModelForm):
    class Meta:
        model = DailyVerification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DailyVerificationForm, self).__init__(*args, **kwargs)
        # Filtrar apenas itens que podem ser verificados diariamente (TOOL, MEASURING, ELECTRONIC)
        self.fields['item'].queryset = InventoryItem.objects.filter(item_type__in=['TOOL', 'MEASURING', 'ELECTRONIC'])
