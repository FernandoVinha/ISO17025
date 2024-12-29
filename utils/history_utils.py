from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

def get_model_history(model_name, object_id=None, limit=30):
    """
    Fetch the historical records for a given model.
    
    Args:
        model_name (str): Name of the model (app_label.ModelName).
        object_id (int, optional): ID of the specific object to filter the history.
        limit (int): Number of records to fetch (default is 30).
    
    Returns:
        QuerySet: Historical records for the model or object.
    """
    try:
        # Get the model class from the provided model name
        model = apps.get_model(model_name)
        history_queryset = model.history.all().order_by('-history_date')

        # Filter by object ID if provided
        if object_id:
            history_queryset = history_queryset.filter(id=object_id)

        # Return the limited results
        return history_queryset[:limit]
    except LookupError:
        raise ValueError(f"Model '{model_name}' not found.")
    except ObjectDoesNotExist:
        return []
