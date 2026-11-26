from django.shortcuts import render
from django.http import JsonResponse
from .service import get_projects,get_environment,get_testtool,get_typetest,get_protocol
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .service import insert_scenario

def addscenario(request):

    
    return render(request, 'scenario/addscenario.html')


def projects_list_api(request):

    projects = list(get_projects())

    return JsonResponse({
        'success': True,
        'projects': projects
    })
def ref_liste_api(request):
    environment=get_environment()
    testtool=get_testtool()
    return JsonResponse({
        'success':True,
        'environment':environment,
        'testtool':testtool,
    })

def ref_typetest_api(request):
    typetest=get_typetest()
    return JsonResponse({
        'success': True,
        'typetest':typetest
    })
def ref_protocol(request):
    protocol=get_protocol()
    return JsonResponse({
        'success':True,
        'protocol':protocol
    }
    )

@require_POST
def save_scenario(request):

    # Vérifier la session utilisateur
    user_id = request.session.get('user_id')

    if not user_id:
        return JsonResponse({
            'success': False,
            'message': 'Session expirée. Veuillez vous reconnecter.'
        }, status=401)

    try:
        data = json.loads(request.body)

        # Convertir les zones JSON du formulaire
        headers = json.loads(data.get('headers') or '{}')
        params_url = json.loads(data.get('params_url') or '{}')

        body_text = data.get('body', '').strip()
        body = json.loads(body_text) if body_text else None

        data['headers'] = headers
        data['params_url'] = params_url
        data['body'] = body

        # Vérifier les champs obligatoires
        required_fields = [
            'name_scenario',
            'id_project',
            'id_type_test',
            'id_envir',
            'id_outilt',
            'id_protocol',
            'method',
            'url_endpoint',
            'duree_secondes',
            'nb_threads'
        ]

        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'Le champ {field} est obligatoire.'
                }, status=400)

        result = insert_scenario(data, user_id)

        return JsonResponse({
            'success': True,
            'message': 'Scénario enregistré et fichiers générés avec succès.',
            'id_scenario': result['id_scenario'],
            'k6_file': result['k6_path'],
            'locust_file': result['locust_path']
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Le format JSON des headers, paramètres ou body est incorrect.'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

