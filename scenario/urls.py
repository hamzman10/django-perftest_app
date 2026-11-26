from django.urls import path
from . import views

app_name = 'scenario'

urlpatterns = [

    path(
        'addscenario/',
        views.addscenario,
        name='addscenario'
    ),

    path(
        'api/projects/',
        views.projects_list_api,
        name='projects_list_api'
    ),
    
    path('api/ref-liste/', 
         views.ref_liste_api,
         name='ref_liste_api'
         ),
    path('api/type-test/',
         views.ref_typetest_api,
         name='ref_typetest_api'
         ),
    path('api/protocol/',
         views.ref_protocol,
         name='ref_protocol'
         ),
    path('save/',
        views.save_scenario,
        name='save_scenario'
        ),

]