from django.contrib import admin

from notification import models


@admin.register(models.NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "name",
        "type",
    )


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "title",
        "template",
        "recipient",
        "status",
    )
