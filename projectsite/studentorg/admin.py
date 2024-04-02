from django.contrib import admin

from .models import College, Program, Organization, Student, OrgMember

admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname", "firstname", "middlename", "program")
    search_fields = ("lastname", "firstname")


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "get_member_program", "organization", "date_joined")

    search_fields = ("student__lastname", "student__firstname")

    def get_member_program(self, obj):
        try:
            member = Student.objects.get(id=obj.student_id)
            return member.program

        except Student.DoesNotExist:
            return None