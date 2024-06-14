from django.contrib import admin
from django.urls import path, re_path
from studentorg.views import (
    HomePageView, OrganizationList, OrganizationCreateView, 
    OrganizationUpdateView, OrganizationDeleteView, CollegeList, 
    CollegeCreateView, CollegeUpdateView, CollegeDeleteView, StudentList, 
    StudentCreateView, StudentUpdateView, StudentDeleteView, ProgramList, 
    ProgramCreateView, ProgramUpdateView, ProgramDeleteView, OrgMemList, 
    OrgMemCreateView, OrgMemUpdateView, OrgMemDeleteView, ChartView,
    GetOrgMembersPerYear, StudentViewByOrg, StudentViewByProg,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin URL
    path("admin/", admin.site.urls),
    
    # Home page
    path('', HomePageView.as_view(), name='home'),
    
    #Charts
    path('charts', ChartView.as_view(), name='charts'),
    path('student_count_by_program/', StudentViewByProg, name='chart'),
    path('student-distribution-by-organization/', StudentViewByOrg, name='chart'),
    path('org-members-per-year/', GetOrgMembersPerYear, name='chart'),

    # Organization URLs
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),
    
    # College URLs
    path('college_list', CollegeList.as_view(), name='colleges-list'),
    path('college_list/add', CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>', CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete', CollegeDeleteView.as_view(), name='college-delete'),
    
    # Student URLs
    path('student_list', StudentList.as_view(), name='students-list'),
    path('student_list/add', StudentCreateView.as_view(), name='student-add'),
    path('student_list/<pk>', StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete', StudentDeleteView.as_view(), name='student-delete'),
    
    # Organization Member URLs
    path('orgmem_list', OrgMemList.as_view(), name='orgmem-list'),
    path('orgmem_list/add', OrgMemCreateView.as_view(), name='orgmem-add'),
    path('orgmem_list/<pk>', OrgMemUpdateView.as_view(), name='orgmem-update'),
    path('orgmem_list/<pk>/delete', OrgMemDeleteView.as_view(), name='orgmem-delete'),
    
    # Program URLs
    path('program_list', ProgramList.as_view(), name='program-list'),
    path('program_list/add', ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<pk>', ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete', ProgramDeleteView.as_view(), name='program-delete'),
    
    # Authentication URLs
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]
