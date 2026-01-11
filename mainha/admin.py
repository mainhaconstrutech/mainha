from django.contrib import admin

from mainha import models as MainhaModels

admin.site.register(MainhaModels.Project)
admin.site.register(MainhaModels.Standard)
admin.site.register(MainhaModels.StandardRule)
