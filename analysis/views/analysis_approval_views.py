from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from ..models import Analysis, AnalysisApproval
from ..forms import AnalysisApprovalForm

# ====== View para listar análises feitas e aprovadas ou não ======
@login_required
def analysis_approval_list(request):
    search_query = request.GET.get('search', '')
    # Filtra as análises que já foram feitas, mas ainda não aprovadas
    analyses_not_approved = Analysis.objects.filter(approved_by__isnull=True)
    # Filtra as análises que já foram aprovadas
    analyses_approved = Analysis.objects.filter(approved_by__isnull=False)

    # Aplicar filtro de pesquisa se houver uma consulta
    if search_query:
        analyses_not_approved = analyses_not_approved.filter(
            Q(item__name__icontains=search_query) | Q(methodology__title__icontains=search_query)
        )
        analyses_approved = analyses_approved.filter(
            Q(item__name__icontains=search_query) | Q(methodology__title__icontains=search_query)
        )

    # Paginação
    paginator_not_approved = Paginator(analyses_not_approved, 10)  # 10 itens por página
    paginator_approved = Paginator(analyses_approved, 10)

    page_number_not_approved = request.GET.get('page_not_approved')
    page_number_approved = request.GET.get('page_approved')

    analyses_not_approved_page = paginator_not_approved.get_page(page_number_not_approved)
    analyses_approved_page = paginator_approved.get_page(page_number_approved)

    return render(request, 'analysis/analysis_approval_list.html', {
        'analyses_not_approved_page': analyses_not_approved_page,
        'analyses_approved_page': analyses_approved_page,
        'search_query': search_query,
    })

# ====== View para aprovar uma análise ou editar uma aprovação existente ======
@login_required
@permission_required('analysis.can_add_analysisapproval', raise_exception=True)
def create_or_edit_analysis_approval(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)

    # Tenta encontrar uma aprovação existente ou cria uma nova
    approval, created = AnalysisApproval.objects.get_or_create(
        analysis=analysis,
        defaults={'approved_by': request.user}
    )

    if request.method == 'POST':
        form = AnalysisApprovalForm(request.POST, instance=approval)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, "Análise aprovada com sucesso!")
            else:
                messages.success(request, "Aprovação atualizada com sucesso!")
            return redirect('analysis:analysis_approval_list')
        else:
            messages.error(request, "Houve um erro ao salvar a aprovação. Verifique os campos e tente novamente.")
    else:
        form = AnalysisApprovalForm(instance=approval)

    return render(request, 'analysis/create_or_edit_analysis_approval.html', {
        'form': form,
        'analysis': analysis,
        'created': created
    })

# ====== View para deletar uma aprovação ======
@login_required
@permission_required('analysis.can_delete_analysisapproval', raise_exception=True)
def delete_analysis_approval(request, approval_id):
    approval = get_object_or_404(AnalysisApproval, id=approval_id)

    if not request.user.has_perm('analysis.can_delete_analysisapproval'):
        raise PermissionDenied("Você não tem permissão para deletar esta aprovação.")

    if request.method == 'POST':
        approval.delete()
        messages.success(request, "Aprovação deletada com sucesso!")
        return redirect('analysis:analysis_approval_list')

    return render(request, 'confirm_delete.html', {
        'item_name': f"Aprovação de {approval.analysis.item.name}",
        'delete_url': request.path,
        'cancel_url': 'analysis:analysis_approval_list'
    })
