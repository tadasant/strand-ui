from django.contrib import admin

from app.questions.models import Tag, Question, Session


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_poster', 'is_solved')


admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Session)
