from django.contrib import admin
from account.models import Student, Expert, UserAccount

admin.site.register(UserAccount)
admin.site.register(Student)
admin.site.register(Expert)
