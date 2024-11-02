from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from ..models import AnalysisRequest, ReceptionItem
from ..forms import ReceptionItemForm

# ====== View para listar AnalysisRequest sem ReceptionItem e as Receções já feitas ======
@login_required
def reception_list(request):
    # Lista de AnalysisRequest que ainda não têm ReceptionItem
    analysis_requests_without_reception = AnalysisRequest.objects.filter(reception_items__isnull=True)
    
    # Lista de ReceptionItem existentes
    reception_items = ReceptionItem.objects.all()

    # Paginação para ambos os conjuntos de dados
    analysis_request_paginator = Paginator(analysis_requests_without_reception, 10)  # 10 itens por página
    reception_item_paginator = Paginator(reception_items, 10)

    page_number = request.GET.get('page')
    analysis_requests_page = analysis_request_paginator.get_page(page_number)
    reception_items_page = reception_item_paginator.get_page(page_number)

    return render(request, 'analysis/reception_list.html', {
        'analysis_requests_page': analysis_requests_page,
        'reception_items_page': reception_items_page
    })

# ====== View para criar ou editar um ReceptionItem ======
@login_required
@permission_required('analysis.can_add_receptionitem', raise_exception=True)
def create_or_edit_reception_item(request, pk):
    analysis_request = get_object_or_404(AnalysisRequest, pk=pk)

    # Tenta encontrar um ReceptionItem associado ou cria um novo
    reception_item, created = ReceptionItem.objects.get_or_create(
        analysis_request=analysis_request,
        defaults={'company': analysis_request.company}
    )

    if request.method == 'POST':
        form = ReceptionItemForm(request.POST, request.FILES, instance=reception_item)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, "Recepção criada com sucesso!")
            else:
                messages.success(request, "Recepção atualizada com sucesso!")
            return redirect('analysis:reception_list')
        else:
            messages.error(request, "Houve um erro ao salvar a recepção. Verifique os campos e tente novamente.")
    else:
        form = ReceptionItemForm(instance=reception_item)

    return render(request, 'analysis/create_or_edit_reception_item.html', {
        'form': form,
        'reception_item': reception_item,
        'created': created
    })

# ====== View para deletar um ReceptionItem ======
@login_required
@permission_required('analysis.can_delete_receptionitem', raise_exception=True)
def delete_reception_item(request, pk):
    reception_item = get_object_or_404(ReceptionItem, pk=pk)

    # Verifica se o usuário tem permissão para deletar
    if not request.user.has_perm('analysis.can_delete_receptionitem'):
        raise PermissionDenied("Você não tem permissão para deletar esta recepção.")

    if request.method == 'POST':
        reception_item.delete()
        messages.success(request, "Recepção deletada com sucesso!")
        return redirect('analysis:reception_list')

    return render(request, 'confirm_delete.html', {
        'item_name': reception_item.name,
        'delete_url': request.path,
        'cancel_url': 'analysis:reception_list'
    })
