from django.contrib import admin
from .models import *


# add Models to admin panel
admin.site.register(UserRequest)
admin.site.register(ArbInst)
admin.site.register(UserRequestRu)
admin.site.register(ArbInstRu)
admin.site.register(Cost)
admin.site.register(CostRu)
admin.site.register(Rate)
