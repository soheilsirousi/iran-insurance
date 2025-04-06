from django.shortcuts import redirect
from django.views import View


class MainPage(View):

    def get(self, request, *args, **kwargs):
        return redirect('profile-dashboard')
