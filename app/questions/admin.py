from django.contrib import admin

from app.questions.models import Tag, Question, Session

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Session)