# accounts/context_processors.py
from django.contrib.auth.models import Permission
from django.conf import settings

def user_permissions(request):
    permissions = {}
    
    if request.user.is_authenticated:
        user_permissions_set = request.user.get_all_permissions()
        
        # Carrega todas as permissões do usuário dinamicamente
        all_permissions = Permission.objects.values_list('content_type__app_label', 'codename')
        for app_label, codename in all_permissions:
            permission_key = f"{app_label}.{codename}"
            permissions[permission_key] = permission_key in user_permissions_set

        # Verifica permissão de gerar convites
        permissions['can_generate_invite'] = request.user.has_perm('accounts.can_generate_invite')
    
    user_info = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        'role': getattr(request.user, 'role', None),
    } if request.user.is_authenticated else {}
    
    project_info = {
        'project_name': getattr(settings, 'PROJECT_NAME', 'ISO17025 Project'),
        'contact_email': getattr(settings, 'CONTACT_EMAIL', 'contact@example.com'),
        'support_phone': getattr(settings, 'SUPPORT_PHONE', '+1 (555) 555-5555'),
        'address': getattr(settings, 'ADDRESS', '1234 Main St, Anytown, USA'),
        'social_links': {
            'facebook': getattr(settings, 'FACEBOOK_URL', 'https://facebook.com'),
            'twitter': getattr(settings, 'TWITTER_URL', 'https://twitter.com'),
            'linkedin': getattr(settings, 'LINKEDIN_URL', 'https://linkedin.com'),
        }
    }
    
    return {
        'permissions': permissions,
        'user_info': user_info,
        'project_info': project_info,
    }
