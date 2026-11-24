from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView
from django.shortcuts import render

from .forms import CustomUserCreationForm, ShareTaskForm, TaskForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q

from .forms import AddGroupMemberForm 
from .models import task, TaskGroup

User = get_user_model()

def home_page(request):
    return render(request, 'tasks/home.html')

class taskCreateView(LoginRequiredMixin, CreateView):
    model = task
    form_class = TaskForm
    template_name = "tasks/newtask.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

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
        return task.objects.filter(
            Q(author=self.request.user) |
            Q(viewers=self.request.user) |
            Q(group__members=self.request.user)
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
        return task.objects.filter(author=self.request.user)

@login_required
def share_task(request, pk):
    t = get_object_or_404(task, pk=pk, author=request.user)
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
    t = get_object_or_404(task, pk=pk, author=request.user)
    if request.method == "POST":
        t.viewers.remove(user_id)
    return redirect("sharetask", pk=t.pk)

@login_required
def leave_task(request, pk):
    t = get_object_or_404(task, pk=pk, viewers=request.user)
    if request.method == "POST":
        t.viewers.remove(request.user)
    return redirect("tasklist")


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = TaskGroup
    fields = ['name', 'members']
    template_name = 'tasks/group_form.html'
    success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response

class GroupListView(LoginRequiredMixin, ListView):
    model = TaskGroup
    template_name = 'tasks/group_list.html'

    def get_queryset(self):
        return self.request.user.task_groups.all()


@login_required
def manage_group(request, pk):
    group = get_object_or_404(TaskGroup, pk=pk, owner=request.user)
    if request.method == "POST":
        form = AddGroupMemberForm(request.POST)
        if form.is_valid():
            try:
                member = User.objects.get(username=form.cleaned_data["username"])
            except User.DoesNotExist:
                form.add_error("username", "No user with that username.")
            else:
                group.members.add(member)
                return redirect("manage_group", pk=group.pk)
    else:
        form = AddGroupMemberForm()
    return render(request, "tasks/manage_group.html", {"form": form, "group": group})

@login_required
def remove_group_member(request, pk, user_id):
    group = get_object_or_404(TaskGroup, pk=pk, owner=request.user)
    if request.method == "POST" and user_id != group.owner.id:
        group.members.remove(user_id)
    return redirect("manage_group", pk=group.pk)

@login_required
def leave_group(request, pk):
    group = get_object_or_404(TaskGroup, pk=pk, members=request.user)
    if request.method == "POST" and group.owner != request.user:
        group.members.remove(request.user)
    return redirect("group_list")

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskGroup
    template_name = "tasks/delete_group.html"
    success_url = reverse_lazy("group_list")

    def get_queryset(self):
        return TaskGroup.objects.filter(owner=self.request.user)
