from django.contrib.auth import authenticate, login, logout
from requests.structures import CaseInsensitiveDict
from django.contrib import messages
from django.shortcuts import render, redirect
import requests as r
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    if request.method == 'POST':
        try:
            url = "http://127.0.0.1:8000/api/login/"
            res = r.post(url, data={
                "email": dict(request.POST)['email'][0],
                "password": dict(request.POST)['password'][0]
            }).json()
            # # print(res)
            user = User.objects.get(email=dict(request.POST)['email'][0])
            response = redirect(profile)
            response.set_cookie("key", "value", max_age=None)
            response.set_cookie('refresh', res['refresh'], max_age=3600)
            response.set_cookie('access', res['access'], max_age=300)
            response.set_cookie('id', user.id, max_age=3600)
            if user is not None:
                # # print(user)
                request.session.set_expiry(300)
                login(request, user)
                user = authenticate(request, email=dict(request.POST)[
                                    'email'][0], password=dict(request.POST)['password'][0])
                return response
            # messages.success(request, "Login successful." )
            else:
                messages.error(
                    request, "Please Check Email & Password or Login again ")

            # return response
        except Exception as e:
            messages.error(
                request, "Please Check Email & Password or Login again ")
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        try:
            url = "http://127.0.0.1:8000/api/register"
            data = dict(request.POST)
            res = r.post(url, data={'first_name': data['fname'][0],
                                    'last_name': data['lname'][0],
                                    'email': data['email'][0],
                                    "address": data['address'][0],
                                    "password": data['password'][0]
                                    }).json()
            # print(res)
            if res['status'] == 400:
                messages.error(request, res['error'])
                return render(request, 'signup.html')

            messages.success(request, "Thanks For registration, Now You Can Login .")
        except:
            messages.error(
                request, "Something went wrong Please recheck Details Or Try To Login.")

        return render(request, 'signup.html')

    return render(request, 'signup.html')


def profile(request):
    try:
        token = request.COOKIES.get('access')
        # print(token)
        if request.user.is_authenticated:
            url = "http://127.0.0.1:8000/api/profile"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = f"Bearer {token}"
            res = r.get(url, data={"id": request.user.id},
                        headers=headers).json()
            # print(res)
            return render(request, 'profile.html', {"user": res['payload']})
    except Exception as e:
        messages.error(request, "Please Login Again")
        # print("error ", e)
    return redirect(home)


def logout_view(request):
    logout(request)
    return render(request, 'index.html')


def update(request):
    if request.method == 'POST':
        try:
            id = request.COOKIES.get("id")
            token = request.COOKIES.get("access")
            url = f"http://127.0.0.1:8000/api/update/{id}"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = f"Bearer {token}"
            res = r.patch(url, data={"first_name": dict(request.POST)['fname'][0],
                                   "last_name": dict(request.POST)['lname'][0],
                                   "email": dict(request.POST)['email'][0], "address": dict(request.POST)['address'][0]}, headers=headers).json()
            # print(res)
        except Exception as e:
            # print(e)
            messages.error(request, "Some Error Occurs, Please Login Again ! ")
            return render(request, "profile.html")
    return render(request, 'profile.html')


def delete(request):
    if request.method == 'POST':
        try:
            logout(request)
            url = "http://127.0.0.1:8000/api/delete"
            id = request.COOKIES.get("id")
            res = r.delete(url, data = {
                "id": id,
            }).json()
            print(res, "jvgjhsdbgdf")
            messages.success(request, res['message'])
        except Exception as e:
            print(e, "fbghsavfdghsjhfcvsdhfjhsdgfjvsdjhgfuyhl")
            messages.success(request, "Something went wrong, Please Login & try again !!!")

        return redirect(home)
    # return render(request, 'profile.html')
        