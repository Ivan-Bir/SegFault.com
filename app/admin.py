from django.contrib import admin
from . import models

# admin.site.register(TagQuestion)
# admin.site.register(models.Question)
# admin.site.register(models.Answer)
# admin.site.register(models.QuestionInstance)
# admin.site.register(models.LikeQuestion)
# admin.site.register(models.LikeAnswer)

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Profile)
# admin.site.register(Rating)
admin.site.register(models.Tag)