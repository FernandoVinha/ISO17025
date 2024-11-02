from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from ..models import AnalysisRequest
from ..forms import AnalysisRequestForm
from ..filters import AnalysisRequestFilter

# ====== View para listar os pedidos de análise ======
@login_required
def analysis_request_list(request):
    if request.user.role == 'employee' and hasattr(request.user, 'company'):
        # Funcionários podem ver todos os pedidos de análise da sua empresa
        analysis_requests = AnalysisRequest.objects.filter(company=request.user.company)
        messages.info(request, "Você está visualizando todos os pedidos de análise da sua empresa.")
    else:
        # Outros usuários só podem ver os pedidos feitos por eles
        analysis_requests = AnalysisRequest.objects.filter(requested_by=request.user)
        messages.info(request, "Você está visualizando os pedidos de análise feitos por você.")

    # Aplicar filtros
    filter = AnalysisRequestFilter(request.GET, queryset=analysis_requests)
    analysis_requests = filter.qs

    return render(request, 'analysis/analysis_request_list.html', {
        'analysis_requests': analysis_requests,
        'filter': filter,
    })

# ====== View para criar um pedido de análise ======
@login_required
@permission_required('analysis.can_add_analysisrequest', raise_exception=True)
def create_analysis_request(request):
    if request.method == 'POST':
        form = AnalysisRequestForm(request.POST, request.FILES)
        if form.is_valid():
            analysis_request = form.save(commit=False)
            analysis_request.requested_by = request.user  # Define o usuário como quem fez o pedido
            analysis_request.save()
            form.save_m2m()  # Salva as relações muitos-para-muitos
            messages.success(request, "Pedido de análise criado com sucesso!")
            return redirect('analysis:analysis_request_list')
        else:
            messages.error(request, "Houve um erro ao criar o pedido de análise. Verifique os campos e tente novamente.")
    else:
        form = AnalysisRequestForm()

    return render(request, 'analysis/create_analysis_request.html', {'form': form})

# ====== View para deletar um pedido de análise ======
@login_required
@permission_required('analysis.can_delete_analysisrequest', raise_exception=True)
def delete_analysis_request(request, pk):
    analysis_request = get_object_or_404(AnalysisRequest, pk=pk)

    # Verifica se o usuário tem permissão para deletar o pedido
    if request.user != analysis_request.requested_by:
        if request.user.role != 'employee' or request.user.company != analysis_request.company:
            # Se o usuário não for o autor ou não for um funcionário da mesma empresa, negar acesso
            messages.error(request, "Você não tem permissão para deletar este pedido de análise.")
            raise PermissionDenied("Você não tem permissão para deletar este pedido de análise.")

    if request.method == 'POST':
        analysis_request.delete()
        messages.success(request, "Pedido de análise deletado com sucesso!")
        return redirect('analysis:analysis_request_list')

    return render(request, 'confirm_delete.html', {
        'item_name': analysis_request.title,
        'delete_url': request.path,
        'cancel_url': 'analysis:analysis_request_list'
    })
