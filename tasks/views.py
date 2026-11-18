from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.shortcuts import render

from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect


from .forms import TaskForm
from .models import task

def home_page(request):
    return render(request, 'tasks/home.html')

class taskCreateView(LoginRequiredMixin, CreateView):
    model = task
    form_class = TaskForm
    template_name = "tasks/newtask.html"
    success_url = reverse_lazy("tasklist")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class taskListView(LoginRequiredMixin, ListView):
    model = task
    template_name = "tasks/tasklist.html"

    def get_queryset(self):
        return task.objects.filter(author=self.request.user)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasklist')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
