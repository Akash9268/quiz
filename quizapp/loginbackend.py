from django.contrib.auth.backends import BaseBackend
from .models import Student


class StudentAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        student = Student.objects.filter(username=username).first()
        if student.password == password:
            return Student.objects.filter(username=username).first()
        return None