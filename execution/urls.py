from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.execution,
         name='execution'),
    path(
        'projets/',
        views.liste_projets,
        name='liste_projets_execution'
    ),

    path(
        'scenarios/<int:id_project>/',
        views.liste_scenarios,
        name='liste_scenarios_execution'
    ),
    path(
    'scenario/<int:id_scenario>/detail/',
    views.detail_scenario_execution,
    name='detail_scenario_execution'
),
]
