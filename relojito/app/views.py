from braces.views import (JSONResponseMixin, LoginRequiredMixin,
                          PermissionRequiredMixin, StaticContextMixin)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django.views.generic.dates import MonthArchiveView
from rest_framework.authtoken.models import Token

from .forms import (CreateProjectForm, CreateTaskForm, EditProjectForm,
                    EditTaskForm)
from .models import Project, Task


@login_required
def total_tasks(request):
    user = request.user
    taskset = set([t.date for t in Task.objects.filter(owner=user)])
    total = []
    for t in taskset:
        d = {}
        d['allDay'] = True
        d['start'] = t
        tx = Task.objects.filter(date=t, owner=user).aggregate(
            Sum('total_hours'))
        d['title'] = str(tx['total_hours__sum']) + ' hs'
        total.append(d)
    return JsonResponse(total, safe=False)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        owned_projects = Project.objects.filter(owner=user, is_active=True)
        collaborator_in = Project.objects.filter(projectcollaborator__user=user,
                                                 is_active=True)

        # Returns latest 5 tasks
        ctx['tasks'] = Task.objects.filter(
            owner=user).order_by('-created_at')[:8]
        # only projects where user is collaborator or owner
        ctx['owned_projects'] = owned_projects
        ctx['collab_projects'] = collaborator_in

        return ctx


class TaskAjaxList(JSONResponseMixin, ListView):
    model = Task
    json_dumps_kwargs = {u"indent": 2}

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    def get(self, request, *args, **kwargs):
        dictionaries = [obj.to_dict() for obj in self.get_queryset()]

        return self.render_json_response(dictionaries)


class TaskTotalTimeList(JSONResponseMixin, ListView):
    model = Task
    json_dumps_kwargs = {u"indent": 2}

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    def get(self, request, *args, **kwargs):
        dictionaries = [obj.to_dict() for obj in self.get_queryset()]

        return self.render_json_response(dictionaries)


class TaskAjaxDetail(JSONResponseMixin, DetailView):
    model = Task
    json_dumps_kwargs = {u"indent": 2}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_dict = {
            u"id": self.object.id,
            u"title": self.object.name + str(self.total_hours),
            u"start": self.object.date,
            u"allDay": False
        }

        return self.render_json_response(context_dict)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('root')
    template_name = 'task_confirm_delete.html'


class TaskMonthlyView(MonthArchiveView):
    queryset = Task.objects.all()
    template_name = 'monthly_tasks.html'
    date_field = "date"
    make_object_list = True
    week_format = "%W"
    allow_future = True


def login_user(request):
    ok = False
    error = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next_out = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                ok = True
            else:
                error = _('Disabled user')
        else:
            error = _('Incorrect data')

    if ok:
        return HttpResponseRedirect(next_out)
    else:
        next_in = request.GET.get('next', '/')
        return render_to_response('login.html',
                                  {"title": _("Login"),
                                   "next": next_in,
                                   "error": error},
                                  context_instance=RequestContext(request))


def logout_user(request):
    logout(request)

    return HttpResponseRedirect('/')


class CreateProject(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    StaticContextMixin,
                    CreateView):
    form_class = CreateProjectForm
    model = Project
    template_name = 'generic_form.html'
    success_url = reverse_lazy('root')
    static_context = {'title': _('Create a project')}

    permission_required = "app.add_project"
    raise_exception = True

    def form_valid(self, form):
        project = Project()
        project.name = form.cleaned_data['name']
        project.description = form.cleaned_data['description']
        project.client = form.cleaned_data['client']
        project.external_url = form.cleaned_data['external_url']
        project.color = form.cleaned_data['color']
        project.owner = self.request.user

        project.save()
        self.object = project

        return HttpResponseRedirect(self.get_success_url())


class EditProject(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  StaticContextMixin, UpdateView):
    template_name = 'generic_form.html'
    success_url = reverse_lazy('root')
    form_class = EditProjectForm
    static_context = {'title': _('Edit project')}

    permission_required = 'app.edit_project'
    raise_exception = True

    def get_object(self, queryset=None):
        obj = Project.objects.get(id=self.kwargs['pk'])
        return obj


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super(ProjectDetail, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            ctx['tasks'] = Task.objects.filter(
                project=self.object).order_by('created_at')
        else:
            ctx['tasks'] = Task.objects.filter(owner=user,
                                               project=self.object).\
                order_by('-created_at')
        return ctx


class CreateTask(LoginRequiredMixin, StaticContextMixin, CreateView):
    form_class = CreateTaskForm
    model = Task
    template_name = 'task_form.html'
    success_url = reverse_lazy('root')
    static_context = {'title': _('Create a task')}

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CreateTask, self).get_form_kwargs(**kwargs)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        task = Task()
        task.name = form.cleaned_data['name']
        task.description = form.cleaned_data['description']
        task.date = form.cleaned_data['date']
        task.project = form.cleaned_data['project']
        task.task_type = form.cleaned_data['task_type']
        task.total_hours = form.cleaned_data['total_hours']
        task.resolved_as = form.cleaned_data['resolved_as']
        task.external_url = form.cleaned_data['external_url']
        task.owner = self.request.user

        task.save()
        self.object = task

        return HttpResponseRedirect(self.get_success_url())


class EditTask(LoginRequiredMixin, StaticContextMixin, UpdateView):
    template_name = 'task_form.html'
    success_url = reverse_lazy('root')
    form_class = EditTaskForm
    static_context = {'title': _('Edit task')}

    def get_form_kwargs(self, **kwargs):
        kwargs = super(EditTask, self).get_form_kwargs(**kwargs)
        kwargs['request'] = self.request
        return kwargs

    def get_object(self, queryset=None):
        obj = Task.objects.get(id=self.kwargs['pk'])
        return obj


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


class GetToken(LoginRequiredMixin, TemplateView):
    template_name = 'get_token.html'

    def get_context_data(self, **kwargs):
        ctx = super(GetToken, self).get_context_data(**kwargs)
        ctx['token'], _ = Token.objects.get_or_create(user=self.request.user)
        return ctx


def reset_token(req):
    Token.objects.filter(user=req.user).delete()
    return redirect('get_token')
