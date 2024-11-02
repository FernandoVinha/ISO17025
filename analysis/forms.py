from django import forms
from .models import AnalysisRequest, ReceptionItem, Analysis, AnalysisApproval, Disposal

class AnalysisRequestForm(forms.ModelForm):
    class Meta:
        model = AnalysisRequest
        fields = [
            'title',
            'company',
            'requested_by',
            'methodologies',
            'comments',
            'sample_image',
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'methodologies': forms.CheckboxSelectMultiple(),
        }

class ReceptionItemForm(forms.ModelForm):
    class Meta:
        model = ReceptionItem
        fields = [
            'name',
            'serial_number',
            'weight',
            'analysis_request',
            'company',
            'condition',
            'sample_image',
            'shipment_date',
            'shipment_location',
            'max_days_for_result',
        ]
        widgets = {
            'condition': forms.TextInput(attrs={'placeholder': 'Describe the condition of the item'}),
            'shipment_location': forms.TextInput(attrs={'placeholder': 'Location details'}),
        }

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = [
            'item',
            'methodology',
            'analysis_type',
            'conformity',
            'results',
            'analyzed_by',
        ]
        widgets = {
            'results': forms.Textarea(attrs={'rows': 5}),
            'conformity': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation logic if needed
        return cleaned_data

class AnalysisApprovalForm(forms.ModelForm):
    class Meta:
        model = AnalysisApproval
        fields = [
            'analysis',
            'approved_by',
            'status',
            'comments',
        ]
        widgets = {
            'status': forms.Select(choices=[('approved', 'Approved'), ('rejected', 'Rejected')]),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

class DisposalForm(forms.ModelForm):
    class Meta:
        model = Disposal
        fields = [
            'item',
            'analysis',
            'disposed_by',
            'disposal_date',
            'reason',
            'comments',
        ]
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }
