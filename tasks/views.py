from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.shortcuts import render

from .forms import CustomUserCreationForm, ShareTaskForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q


from .forms import TaskForm, TaskListForm, ShareListForm
from .models import task, TaskList

User = get_user_model()

def home_page(request):
    return render(request, 'tasks/home.html')

class taskCreateView(LoginRequiredMixin, CreateView):
    model = task
    form_class = TaskForm
    template_name = "tasks/newtask.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if "share" in self.request.POST:
            return reverse("sharetask", kwargs={"pk": self.object.pk})
        return reverse("tasklist")

class taskListView(LoginRequiredMixin, ListView):
    model = task
    template_name = "tasks/tasklist.html"

    def get_queryset(self):
        return task.objects.filter(Q(author=self.request.user) | Q(viewers=self.request.user), task_list__isnull=True
        ).distinct()

def register(request):
    if request.user.is_authenticated:
        return redirect("tasklist")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasklist')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

class taskDeleteView(LoginRequiredMixin, DeleteView):
    model = task
    template_name = "tasks/deletetask.html"
    success_url = reverse_lazy("tasklist")

    def get_queryset(self):
        return task.objects.filter(author=self.request.user, task_list__isnull=True)

@login_required
def share_task(request, pk):
    t = get_object_or_404(task, pk=pk, author=request.user, task_list__isnull=True)
    if request.method == "POST":
        form = ShareTaskForm(request.POST)
        if form.is_valid():
            try:
                viewer = User.objects.get(username=form.cleaned_data["username"])
            except User.DoesNotExist:
                form.add_error("username", "No user with that username.")
            else:
                if viewer != request.user:
                    t.viewers.add(viewer)
                return redirect("sharetask", pk=t.pk)
    else:
        form = ShareTaskForm()
    return render(request, "tasks/sharetask.html", {"form": form, "task": t})

@login_required
def unshare_task(request, pk, user_id):
    t = get_object_or_404(task, pk=pk, author=request.user, task_list__isnull=True)
    if request.method == "POST":
        t.viewers.remove(user_id)
    return redirect("sharetask", pk=t.pk)

@login_required
def leave_task(request, pk):
    t = get_object_or_404(task, pk=pk, viewers=request.user, task_list__isnull=True)
    if request.method == "POST":
        t.viewers.remove(request.user)
    return redirect("tasklist")


def accessible_lists(user):
    return TaskList.objects.filter(Q(owner=user) | Q(members=user)).distinct()


@login_required
def project_lists(request):
    return render(request, "tasks/lists.html", {"lists": accessible_lists(request.user)})


@login_required
def create_list(request):
    form = TaskListForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("listdetail", pk=project.pk)
    return render(request, "tasks/newlist.html", {"form": form})


@login_required
def list_detail(request, pk):
    project = get_object_or_404(accessible_lists(request.user), pk=pk)
    return render(request, "tasks/list_detail.html", {"project": project, "tasks": project.tasks.all()})


@login_required
def share_list(request, pk):
    project = get_object_or_404(TaskList, pk=pk, owner=request.user)
    form = ShareListForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            member = User.objects.get(username=form.cleaned_data["username"])
        except User.DoesNotExist:
            form.add_error("username", "No user with that username.")
        else:
            if member != request.user:
                project.members.add(member)
            return redirect("sharelist", pk=pk)
    return render(request, "tasks/sharelist.html", {"form": form, "project": project})


@login_required
def create_project_task(request, pk):
    project = get_object_or_404(accessible_lists(request.user), pk=pk)
    form = TaskForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        new_task = form.save(commit=False)
        new_task.author = request.user
        new_task.task_list = project
        new_task.save()
        return redirect("listdetail", pk=pk)
    return render(request, "tasks/newtask.html", {"form": form, "project": project})


@login_required
def delete_project_task(request, pk, task_id):
    project = get_object_or_404(accessible_lists(request.user), pk=pk)
    selected_task = get_object_or_404(project.tasks.all(), pk=task_id)
    if request.method == "POST":
        selected_task.delete()
    return redirect("listdetail", pk=pk)


@login_required
@require_POST
def remove_list_member(request, pk, user_id):
    project = get_object_or_404(TaskList, pk=pk, owner=request.user)
    if user_id != project.owner_id:
        project.members.remove(user_id)
    return redirect("sharelist", pk=pk)


@login_required
@require_POST
def leave_list(request, pk):
    project = get_object_or_404(TaskList, pk=pk, members=request.user)
    if project.owner_id == request.user.pk:
        return redirect("listdetail", pk=pk)
    project.members.remove(request.user)
    return redirect("projectlists")


@login_required
def delete_list(request, pk):
    project = get_object_or_404(TaskList, pk=pk, owner=request.user)
    if request.method == "POST":
        project.delete()
        return redirect("projectlists")
    return render(request, "tasks/delete_list.html", {"project": project})
