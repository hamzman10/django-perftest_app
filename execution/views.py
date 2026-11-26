from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .service import get_scenario_execution_detail
from .service import (get_projects_execution,get_scenarios_execution)


@require_GET
def liste_projets(request):

    projets = list(get_projects_execution())

    return JsonResponse({
        'success': True,
        'projets': projets
    })


@require_GET
def liste_scenarios(request, id_project):

    scenarios = list(
        get_scenarios_execution(id_project)
    )

    return JsonResponse({
        'success': True,
        'scenarios': scenarios
    })




@require_GET
def detail_scenario_execution(request, id_scenario):

    result = get_scenario_execution_detail(id_scenario)

    if not result:
        return JsonResponse({
            'success': False,
            'message': 'Scénario introuvable.'
        }, status=404)

    return JsonResponse({
        'success': True,
        'scenario': result['scenario'],
        'configuration': result['configuration']
    })

def execution(request):
    
    
    return render(request, 'execution/execution.html')