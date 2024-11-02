import django_filters
from .models import AnalysisRequest, ReceptionItem, Analysis, AnalysisApproval, Disposal
from django_filters import DateFilter, CharFilter

class AnalysisRequestFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label="Title")
    company = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains', label="Company")
    requested_by = django_filters.CharFilter(field_name='requested_by__email', lookup_expr='icontains', label="Requested By")
    created_at = DateFilter(field_name='created_at', lookup_expr='date', label="Creation Date")

    class Meta:
        model = AnalysisRequest
        fields = ['title', 'company', 'requested_by', 'created_at']

class ReceptionItemFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label="Item Name")
    serial_number = CharFilter(field_name='serial_number', lookup_expr='icontains', label="Serial Number")
    company = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains', label="Company")
    received_at = DateFilter(field_name='received_at', lookup_expr='date', label="Reception Date")

    class Meta:
        model = ReceptionItem
        fields = ['name', 'serial_number', 'company', 'received_at']

class AnalysisFilter(django_filters.FilterSet):
    item = CharFilter(field_name='item__name', lookup_expr='icontains', label="Item")
    methodology = CharFilter(field_name='methodology__title', lookup_expr='icontains', label="Methodology")
    analysis_type = CharFilter(field_name='analysis_type', lookup_expr='icontains', label="Analysis Type")
    analyzed_at = DateFilter(field_name='analyzed_at', lookup_expr='date', label="Analysis Date")
    conformity = django_filters.BooleanFilter(field_name='conformity', label="Conformity")

    class Meta:
        model = Analysis
        fields = ['item', 'methodology', 'analysis_type', 'analyzed_at', 'conformity']

class AnalysisApprovalFilter(django_filters.FilterSet):
    analysis = CharFilter(field_name='analysis__item__name', lookup_expr='icontains', label="Analysis Item")
    approved_by = CharFilter(field_name='approved_by__email', lookup_expr='icontains', label="Approved By")
    approval_date = DateFilter(field_name='approval_date', lookup_expr='date', label="Approval Date")
    status = CharFilter(field_name='status', lookup_expr='icontains', label="Status")

    class Meta:
        model = AnalysisApproval
        fields = ['analysis', 'approved_by', 'approval_date', 'status']

class DisposalFilter(django_filters.FilterSet):
    item = CharFilter(field_name='item__name', lookup_expr='icontains', label="Disposed Item")
    disposed_by = CharFilter(field_name='disposed_by__email', lookup_expr='icontains', label="Disposed By")
    disposal_date = DateFilter(field_name='disposal_date', lookup_expr='date', label="Disposal Date")
    reason = CharFilter(field_name='reason', lookup_expr='icontains', label="Reason")

    class Meta:
        model = Disposal
        fields = ['item', 'disposed_by', 'disposal_date', 'reason']
