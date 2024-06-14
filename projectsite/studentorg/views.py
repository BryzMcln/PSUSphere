from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from studentorg.models import Organization, College, Student, Program, OrgMember
from studentorg.forms import OrganizationForm, CollegesForm, StudentsForm, ProgramForm, OrgMembersForm
from typing import Any

from django.db.models import *
from django.db.models.functions import TruncYear
from datetime import datetime

@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    template_name = 'org_list.html'
    paginate_by = 5
    model = Organization
    context_object_name = 'organization'

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
            Q(description__icontains=query) | Q(college__college_name__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = "college_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegesForm
    template_name = "college_add.html"
    success_url = reverse_lazy('colleges-list') 
    
class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegesForm
    template_name = "college_edit.html"
    success_url = reverse_lazy('colleges-list') 

class CollegeDeleteView(DeleteView):
    model = College
    template_name = "college_del.html"
    success_url = reverse_lazy('colleges-list')

class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = "student_list.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student_id__icontains=query) |
            Q(lastname__icontains=query) | Q(firstname__icontains=query) | 
            Q(middlename__icontains=query) | Q(program__prog_name__icontains=query) )
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentsForm
    template_name = "student_add.html"
    success_url = reverse_lazy('students-list') 
    
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentsForm
    template_name = "student_edit.html"
    success_url = reverse_lazy('students-list') 

class StudentDeleteView(DeleteView):
    model = Student
    template_name = "student_del.html"
    success_url = reverse_lazy('students-list')

class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = "program_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) |
            Q(college__college_name__icontains=query))
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "prog_add.html"
    success_url = reverse_lazy('program-list') 
    
class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "prog_edit.html"
    success_url = reverse_lazy('program-list') 

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "prog_del.html"
    success_url = reverse_lazy('program-list')

class OrgMemList(ListView):
    model = OrgMember
    context_object_name = 'orgmem'
    template_name = "orgmem_list.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student__lastname__icontains=query) |
            Q(student__firstname__icontains=query) | 
            Q(date_joined__icontains=query) | Q(organization__name__icontains=query))
        return qs

class OrgMemCreateView(CreateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = "orgmem_add.html"
    success_url = reverse_lazy('orgmem-list') 
    
class OrgMemUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = "orgmem_edit.html"
    success_url = reverse_lazy('orgmem-list') 

class OrgMemDeleteView(DeleteView):
    model = OrgMember
    template_name = "orgmem_del.html"
    success_url = reverse_lazy('orgmem-list')

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def StudentViewByProg(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.prog_name, COUNT(s.id) as student_count
            FROM studentorg_program p
            LEFT JOIN studentorg_student s ON s.program_id = p.id
            GROUP BY p.prog_name
        """)
        data = cursor.fetchall()

    response_data = [{"prog_name": row[0], "student_count": row[1]} for row in data]
    return JsonResponse(response_data, safe=False)


def StudentViewByOrg(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.name, COUNT(DISTINCT om.id)
            FROM studentorg_organization o
            LEFT JOIN studentorg_orgmember om ON om.organization_id = o.id
            GROUP BY o.id
        """)
        data = cursor.fetchall()

    response_data = [{"name": row[0], "student_count": row[1]} for row in data]
    return JsonResponse(response_data, safe=False)


def GetOrgMembersPerYear(request):
    members_per_year = OrgMember.objects.annotate(year=TruncYear('date_joined')) \
                                 .values('year') \
                                 .annotate(count=Count('id')) \
                                 .order_by('year') \
                                 .values('year', 'count')

    data = list(members_per_year)
    return JsonResponse(data, safe=False)