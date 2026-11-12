
from django.shortcuts import render, redirect
from django.contrib import messages

from .services.lister_project import lister_project, insert_project,update_project,delete_project


def projects(request):
    if request.method == 'POST':
            action = request.POST.get('action')

            # SUPPRESSION
            if action == 'delete':
                id_project = request.POST.get('id_project')

                try:
                    delete_project(id_project)
                    messages.success(
                        request,
                        f'Projet {id_project} supprimé avec succès.'
                    )
                except Exception as e:
                    messages.error(request, f'Erreur de suppression : {e}')

            return redirect('projects')
    if request.method == 'POST':

        id_project = request.POST.get('id_project')
        name_pr = request.POST.get('name_pr')
        description_pr = request.POST.get('description_pr')
        base_url = request.POST.get('base_url')
        owner_id = request.POST.get('owner_id')

        try:

            if not id_project:

                project_id = insert_project(
                    name_pr,
                    description_pr,
                    owner_id,
                    base_url
                )

                messages.success(
                    request,
                    f'Project added successfully. ID: {project_id}'
                )

            else:
                
                project_id = update_project(
                                    id_project,
                                    name_pr,
                                    description_pr,
                                    owner_id,
                                    base_url
                                )
                
                               
                messages.info(request, 'Modification non encore implémentée.')

        except Exception as e:

            messages.error(request, f'Error: {e}')

        return redirect('projects')

    projects = lister_project()

    return render(request, 'projects/projects.html', {
        'projects': projects
    })
