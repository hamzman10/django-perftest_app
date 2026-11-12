from django.db import connection

def authenticate_user(username, password):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            CALL public.sp_autentificate(
                %s,
                %s,
                NULL
            )
            """,
            [username, password]
        )

        

        result = cursor.fetchone()

        

        if result:
            return result[0]

    return None