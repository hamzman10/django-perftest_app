
from projects.models import Projects
from scenario.models import Scenario
import json
from ref_models.models import RefProtocole
from .models import ScenarioRequest

# ============================================
# Liste des projets
# ============================================

def get_projects_execution():

    return Projects.objects.all().order_by(
        'name_pr'
    ).values(
        'id_project',
        'name_pr',
        'description_pr',
        'base_url'
    )


# ============================================
# Liste des scénarios d'un projet
# ============================================

def get_scenarios_execution(id_project):

    return Scenario.objects.filter(
        id_project=id_project,
        actif=True
    ).order_by(
        '-date_creation'
    ).values(
        'id_scenario',
        'name_scenario',
        'description',
        'objectif',
        'id_type_test',
        'id_envir',
        'id_outilt',
        'id_protocol',
        'duree_secondes',
        'nb_threads',
        'ramp_up',
        'think_time',
        'nb_threads_initial',
        'nb_threads_max',
        'step_threads',
        'step_duration_seconds',
        'volume_donnees',
        'seuils_performance',
        'nb_repetitions'
    )




def get_scenario_execution_detail(id_scenario):

    # 1. Récupérer le scénario
    scenario = Scenario.objects.filter(
        id_scenario=id_scenario
    ).values(
        'id_scenario',
        'name_scenario',
        'description',
        'objectif',
        'id_project',
        'id_type_test',
        'id_envir',
        'id_outilt',
        'id_protocol',
        'duree_secondes',
        'nb_threads',
        'ramp_up',
        'think_time',
        'nb_threads_initial',
        'nb_threads_max',
        'step_threads',
        'step_duration_seconds',
        'volume_donnees',
        'seuils_performance',
        'nb_repetitions',
        'url_endpoint',
        'headers',
        'params_url',
        'body'
    ).first()

    if not scenario:
        return None

    # 2. Récupérer la méthode HTTP initiale
    protocole = RefProtocole.objects.filter(
        id_protocol=scenario['id_protocol']
    ).values(
        'desingnation_protocol'
    ).first()

    methode_initiale = (
        protocole['desingnation_protocol']
        if protocole else 'GET'
    )

    # 3. Chercher la dernière configuration HTTP
    request_config = ScenarioRequest.objects.filter(
        id_scenario=id_scenario
    ).order_by(
        '-date_creation',
        '-id_request'
    ).values(
        'id_request',
        'url_cible',
        'methode_http',
        'content_type',
        'headers',
        'parametres',
        'body',
        'auth_type',
        'auth_config'
    ).first()

    # 4. Priorité à scenario_request si disponible
    if request_config:

        configuration = {
            'id_request': request_config['id_request'],
            'url': request_config['url_cible'],
            'method': request_config['methode_http'],
            'content_type': request_config['content_type'],
            'headers': request_config['headers'] or {},
            'params': request_config['parametres'] or {},
            'body': request_config['body'] or '',
            'auth_type': request_config['auth_type'] or 'NONE',
            'auth_config': request_config['auth_config'] or {}
        }

    else:

        # Initialisation depuis la table scenario
        configuration = {
            'id_request': None,
            'url': scenario['url_endpoint'] or '',
            'method': methode_initiale,
            'content_type': 'application/json',
            'headers': scenario['headers'] or {},
            'params': scenario['params_url'] or {},
            'body': scenario['body'] or {},
            'auth_type': 'NONE',
            'auth_config': {}
        }

    return {
        'scenario': scenario,
        'configuration': configuration
    }
