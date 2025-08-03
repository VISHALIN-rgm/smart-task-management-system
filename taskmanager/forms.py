from django import forms
from .models import Team
from accounts.models import CustomUser

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Team
        fields = ['name', 'description', 'members']



from django import forms
from .models import Task, Project
from accounts.models import CustomUser

# taskmanager/forms.py

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'due_date', 'status']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Prevent KeyError
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.user:
            # Only show employees in the manager's company/team
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(role='employee')



