from django.db import connection, transaction
""" from django.db import connection ,transaction


def lister_project(): 
    with transaction.atomic():
         with connection.cursor() as cursor:
             cursor.execute("BEGIN")
             cursor.execute("CALL public.sp_projects_list('project_cursor')")
             cursor.execute("FETCH ALL FROM project_cursor")
             columns=[col[0] for col in cursor.description]
             projects=[dict(zip(columns,row))
                  for row in cursor.fetchall()]
    return projects
         """



def lister_project():

    with transaction.atomic():

        with connection.cursor() as cursor:

            cursor.execute(
                "CALL public.sp_projects_list('project_cursor')"
            )

            cursor.execute(
                "FETCH ALL FROM project_cursor"
            )

            columns = [col[0] for col in cursor.description]

            projects = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    return projects

from django.db import connection, transaction

def insert_project(name_pr, description_pr, owner_id, base_url):

    with transaction.atomic():

        with connection.cursor() as cursor:

            cursor.execute("""
                CALL public.sp_insert_project(
                    %s, %s, %s, %s, %s
                )
            """, [
                name_pr,
                description_pr,
                owner_id,
                base_url,
                None
            ])

            result = cursor.fetchone()

            if result:
                return result[0]

    return None




    return None
def update_project(id_project, name_pr, description_pr, owner_id, base_url):

    with transaction.atomic():

        with connection.cursor() as cursor:

            cursor.execute("""
                CALL public.sp_update_project(
                    %s, %s, %s, %s, %s
                )
            """, [
                id_project,
                name_pr,
                description_pr,
                owner_id,
                base_url
            ])

            return id_project


def delete_project(id_project):
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(
                "CALL public.sp_delete_project(%s)",
                [id_project]
            )

    return id_project