from django.urls import path
from .views import (
    analysis_approval_views,
    analysis_request,
    analysis_views,
    disposal_views,
    reception_views
)

app_name = 'analysis'

urlpatterns = [
    # URLs para Analysis Views
    path('analysis/', analysis_views.analysis_list, name='analysis_list'),
    path('analysis/create/<int:reception_item_id>/<int:methodology_id>/', analysis_views.create_or_edit_analysis, name='create_or_edit_analysis'),
    path('analysis/delete/<int:analysis_id>/', analysis_views.delete_analysis, name='delete_analysis'),

    # URLs para Analysis Request Views
    path('request/', analysis_request.analysis_request_list, name='analysis_request_list'),
    path('request/create/', analysis_request.create_analysis_request, name='create_analysis_request'),
    path('request/delete/<int:pk>/', analysis_request.delete_analysis_request, name='delete_analysis_request'),

    # URLs para Disposal Views
    path('disposal/', disposal_views.disposal_list, name='disposal_list'),
    path('disposal/create/<int:reception_item_id>/', disposal_views.create_or_edit_disposal, name='create_or_edit_disposal'),
    path('disposal/delete/<int:disposal_id>/', disposal_views.delete_disposal, name='delete_disposal'),

    # URLs para Analysis Approval Views
    path('approval/', analysis_approval_views.analysis_approval_list, name='analysis_approval_list'),
    path('approval/create/<int:analysis_id>/', analysis_approval_views.create_or_edit_analysis_approval, name='create_or_edit_analysis_approval'),
    path('approval/delete/<int:approval_id>/', analysis_approval_views.delete_analysis_approval, name='delete_analysis_approval'),

    # URLs para Reception Views
    path('reception/', reception_views.reception_list, name='reception_list'),
    path('reception/create/<int:pk>/', reception_views.create_or_edit_reception_item, name='create_or_edit_reception_item'),
    path('reception/delete/<int:pk>/', reception_views.delete_reception_item, name='delete_reception_item'),
]
