from django.contrib import admin

from students.models import Note, Homework, Todo

admin.site.register(Note)
admin.site.register(Homework)
admin.site.register(Todo)
