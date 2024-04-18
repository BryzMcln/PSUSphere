from django.forms import ModelForm
from django import forms
from .models import Organization, Program, College, Student, OrgMember


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"
        labels = {
            'name': 'Organization Name',  
            'college': 'College',  
            'description': 'Description',
        }

class CollegesForm(ModelForm):
    class Meta:
        model = College
        fields = "__all__"
        labels = {
            'college_name': 'College Name'
        }

class StudentsForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        labels = {
            'student_id': 'Student ID',  
            'lastname': 'Last Name',  
            'firstname': 'First Name',
            'middlename': 'Middle Name',  
            'program': 'Program',
        }

class OrgMembersForm(ModelForm):
    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    class Meta:
        model = OrgMember
        fields = "__all__"
        labels = {
            'student': 'Student',  
            'organization': 'Organization',  
            'date_joined': 'Date Joined',
        }


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = "__all__"
        labels = {
            'prog_name': 'Program Name',  
            'college': 'College',  
        }