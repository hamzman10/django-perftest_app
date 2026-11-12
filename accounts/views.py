from django.shortcuts import render, redirect
from django.contrib import messages
from .services.auth_service import authenticate_user

   


def login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_id = authenticate_user(username, password)

            

            if user_id is not None:
                request.session['user_id'] = user_id
                request.session['username'] = username

                return redirect('accuil')

            else:
                messages.error(
                    request,
                    'Username ou mot de passe incorrect.'
                )

        except Exception as e:
            print("ERREUR AUTHENTIFICATION :", str(e))

            messages.error(
                request,
                'Une erreur est survenue lors de la connexion.'
            )
    return  render(request,'login/login.html',)



