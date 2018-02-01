from django.contrib import admin

from app.topics.models import Tag, Topic, Discussion


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_poster', 'group', 'status')


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'get_topic_original_poster', 'get_topic_group', 'status')

    def get_topic_original_poster(self, obj):
        return obj.topic.original_poster

    get_topic_original_poster.short_description = 'original poster'

    def get_topic_group(self, obj):
        return obj.topic.group

    get_topic_group.short_description = 'group'


admin.site.register(Tag)
admin.site.register(Topic, admin_class=TopicAdmin)
admin.site.register(Discussion, admin_class=DiscussionAdmin)
