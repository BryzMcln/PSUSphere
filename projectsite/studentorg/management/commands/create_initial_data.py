from django.core.management.base import BaseCommand
from faker import Faker
from studentorg.models import College, Program, Organization, Student, OrgMember

class Command(BaseCommand):
    help = 'create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_organization(10)
        self.create_students(50)
        self.create_membership(10)

    def create_organization(self, count):
        fake = Faker()

        for _ in range(count):
            words = [fake.word() for _ in range(2)]  
            Organization.objects.create(
                name=' '.join(words).title(), 
                college=College.objects.order_by('?').first(),
                description=fake.sentence()
            )
        self.stdout.write(self.style.SUCCESS(
            'Initial data for organizations created successfully.'))

    def create_students(self, count):  
        fake = Faker('en_PH')

        for _ in range(count):
            Student.objects.create(
                student_id=f"{fake.random_int(2020, 2024)}-{fake.random_int(1, 8)}-{fake.random_number(digits=4)}",
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=Program.objects.order_by('?').first()  #
            )
        self.stdout.write(self.style.SUCCESS(
            'Initial data for students created successfully.'))

    def create_membership(self, count):
        fake = Faker()

        for _ in range(count):
            OrgMember.objects.create(
                student=Student.objects.order_by('?').first(),  
                organization=Organization.objects.order_by('?').first(),
                date_joined=fake.date_between(start_date="-2y", end_date="today")
            )
        self.stdout.write(self.style.SUCCESS(
            'Initial data for student organizations created successfully.'
        ))