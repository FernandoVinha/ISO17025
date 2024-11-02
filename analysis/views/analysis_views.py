from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from ..models import ReceptionItem, Analysis, Methodology
from ..forms import AnalysisForm

# ====== View para listar itens recepcionados e suas metodologias ======
@login_required
def analysis_list(request):
    # Lista todos os itens recepcionados
    reception_items = ReceptionItem.objects.all()
    analyses = Analysis.objects.all()

    # Criamos uma lista para mostrar cada item de recepção com cada metodologia associada
    reception_methodologies = []
    for reception_item in reception_items:
        for methodology in reception_item.analysis_request.methodologies.all():
            # Verifica se uma análise já foi feita para este item e metodologia
            analysis = analyses.filter(item=reception_item, methodology=methodology).first()
            reception_methodologies.append({
                'reception_item': reception_item,
                'methodology': methodology,
                'analysis': analysis,  # Será None se não houver análise
            })

    # Paginação
    paginator = Paginator(reception_methodologies, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    reception_methodologies_page = paginator.get_page(page_number)

    return render(request, 'analysis/analysis_list.html', {
        'reception_methodologies_page': reception_methodologies_page
    })

# ====== View para criar ou editar uma análise ======
@login_required
@permission_required('analysis.can_add_analysis', raise_exception=True)
def create_or_edit_analysis(request, reception_item_id, methodology_id):
    reception_item = get_object_or_404(ReceptionItem, id=reception_item_id)
    methodology = get_object_or_404(Methodology, id=methodology_id)

    # Tenta encontrar uma análise existente ou cria uma nova
    analysis, created = Analysis.objects.get_or_create(
        item=reception_item,
        methodology=methodology,
        defaults={'analyzed_by': request.user}
    )

    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, "Análise criada com sucesso!")
            else:
                messages.success(request, "Análise atualizada com sucesso!")
            return redirect('analysis:analysis_list')
        else:
            messages.error(request, "Houve um erro ao salvar a análise. Verifique os campos e tente novamente.")
    else:
        form = AnalysisForm(instance=analysis)

    return render(request, 'analysis/create_or_edit_analysis.html', {
        'form': form,
        'reception_item': reception_item,
        'methodology': methodology,
        'analysis': analysis,
        'created': created
    })

# ====== View para deletar uma análise ======
@login_required
@permission_required('analysis.can_delete_analysis', raise_exception=True)
def delete_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)

    if not request.user.has_perm('analysis.can_delete_analysis'):
        raise PermissionDenied("Você não tem permissão para deletar esta análise.")

    if request.method == 'POST':
        analysis.delete()
        messages.success(request, "Análise deletada com sucesso!")
        return redirect('analysis:analysis_list')

    return render(request, 'confirm_delete.html', {
        'item_name': analysis.item.name,
        'delete_url': request.path,
        'cancel_url': 'analysis:analysis_list'
    })
