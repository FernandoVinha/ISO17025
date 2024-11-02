from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from ..models import ReceptionItem, Analysis, Disposal
from ..forms import DisposalForm

# ====== View para listar todos os descartes ======
@login_required
def disposal_list(request):
    search_query = request.GET.get('search', '')
    # Filtra todos os itens de descarte
    disposals = Disposal.objects.all()

    # Aplicar filtro de pesquisa se houver uma consulta
    if search_query:
        disposals = disposals.filter(
            Q(item__name__icontains=search_query) | Q(reason__icontains=search_query)
        )

    # Paginação
    paginator = Paginator(disposals, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    disposals_page = paginator.get_page(page_number)

    return render(request, 'analysis/disposal_list.html', {
        'disposals_page': disposals_page,
        'search_query': search_query,
    })

# ====== View para criar ou editar um descarte ======
@login_required
@permission_required('analysis.can_add_disposal', raise_exception=True)
def create_or_edit_disposal(request, reception_item_id):
    reception_item = get_object_or_404(ReceptionItem, id=reception_item_id)
    # Tenta encontrar um descarte existente ou cria um novo
    disposal, created = Disposal.objects.get_or_create(
        item=reception_item,
        defaults={'disposed_by': request.user}
    )

    if request.method == 'POST':
        form = DisposalForm(request.POST, instance=disposal)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, "Descarte criado com sucesso!")
            else:
                messages.success(request, "Descarte atualizado com sucesso!")
            return redirect('analysis:disposal_list')
        else:
            messages.error(request, "Houve um erro ao salvar o descarte. Verifique os campos e tente novamente.")
    else:
        form = DisposalForm(instance=disposal)

    return render(request, 'analysis/create_or_edit_disposal.html', {
        'form': form,
        'reception_item': reception_item,
        'created': created
    })

# ====== View para deletar um descarte ======
@login_required
@permission_required('analysis.can_delete_disposal', raise_exception=True)
def delete_disposal(request, disposal_id):
    disposal = get_object_or_404(Disposal, id=disposal_id)

    if not request.user.has_perm('analysis.can_delete_disposal'):
        raise PermissionDenied("Você não tem permissão para deletar este descarte.")

    if request.method == 'POST':
        disposal.delete()
        messages.success(request, "Descarte deletado com sucesso!")
        return redirect('analysis:disposal_list')

    return render(request, 'confirm_delete.html', {
        'item_name': f"Descarte de {disposal.item.name}",
        'delete_url': request.path,
        'cancel_url': 'analysis:disposal_list'
    })
