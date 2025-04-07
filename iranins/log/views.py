from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from log.models import Log


class Logs(LoginRequiredMixin, View):
    template_name = 'log/logs.html'

    def get(self, request, *args, **kwargs):
        logs = Log.objects.all().order_by('-created_time')

        paginator = Paginator(logs, 40)
        page = request.GET.get('page')
        logs = paginator.get_page(page)

        return render(request, self.template_name, {'logs': logs})