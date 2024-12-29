from utils.history_utils import get_model_history  # Supondo que a lógica de histórico esteja aqui

def global_history(request):
    """
    Adiciona o histórico ao contexto global, disponível para todos os templates.
    """
    if request.user.is_authenticated:
        # Busca os últimos 30 registros do histórico global
        history = get_model_history('accounts.RelationshipType', limit=30)  # Altere para o modelo relevante
        return {'simple_history': history}
    return {}
