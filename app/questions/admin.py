from django.contrib import admin

from app.questions.models import Tag, Question, Session


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_poster', 'group', 'status')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('question', 'get_question_original_poster', 'get_question_group', 'status')

    def get_question_original_poster(self, obj):
        return obj.question.original_poster

    get_question_original_poster.short_description = 'original poster'

    def get_question_group(self, obj):
        return obj.question.group

    get_question_group.short_description = 'group'


admin.site.register(Tag)
admin.site.register(Question, admin_class=QuestionAdmin)
admin.site.register(Session, admin_class=SessionAdmin)
