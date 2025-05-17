from django.contrib import admin

# Register your models here.
from .models import MemoryDomande, MemoryRisposte, BanWord

admin.site.register(MemoryDomande)
admin.site.register(MemoryRisposte)
admin.site.register(BanWord)
