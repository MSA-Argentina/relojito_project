# -*- coding: utf-8 -*-
from django.db.models import Q
from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, Layout, Reset, Submit
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from .models import Project, Task


class CreateProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                _('Create a project'),
                Field('name', required=True, autofocus=True),
                Field('description'),
                Field('client'),
                Field('color', css_class='color_field'),
                Field('external_url')),
            FormActions(
                Submit('save', _('Create'), css_class='col-md-offset-2'),
                Reset('reset', _('Clean'))
            )
        )

    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'client',
                  'color',
                  'external_url']


class EditProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                _('Edit Project'),
                'name',
                'description',
                'client',
                Field('color', css_class='color_field'),
                'external_url',
                # Field('is_active', css_class='col-md-offset-4'),
                PrependedText('is_active', ''),
                'owner'
            ),
            FormActions(
                Submit('update', _('Update'), css_class='col-md-offset-2')
            ))

    class Meta:
        model = Project


class CreateTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        user = self.request.user
        # The user's projects only
        self.fields['project'].queryset = Project.objects.filter(
            Q(projectcollaborator__user=user) | Q(owner=user),
            is_active=True).distinct()

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                _('Create a task'),
                Field('name', required=True, autofocus=True),
                Field('description', rows=2),
                Field('project', required=True),
                Field('date', css_class='dtpicker date',
                      data_date_format="YYYY-MM-DD"),
                Field('total_hours', min='0', step='0.5'),
                Field('task_type'),
                Field('resolved_as'),
                Field('external_url')),
            FormActions(
                Submit('save', _('Create'), css_class='col-md-offset-2'),
                Reset('reset', _('Clean'))
            )
        )

    class Meta:
        model = Task
        fields = ['name',
                  'description',
                  'project',
                  'task_type',
                  'date',
                  'total_hours',
                  'resolved_as',
                  'external_url'
        ]


class EditTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                _('Edit Task'),
                'name',
                'project',
                'task_type',
                'description',
                Field('date', css_class='dtpicker date',
                      data_date_format="YYYY-MM-DD"),
                Field('total_hours', min='0', step='0.5'),
                'resolved_as',
                'external_url',
                'owner'
            ),
            FormActions(
                Submit('update', _('Update'), css_class='col-md-offset-2')
            ))

    class Meta:
        model = Task
