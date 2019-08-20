from django.contrib import admin
from .models import AccountDetail, CacheVoterData, WorkerProfile, Task
# Register your models here.
admin.site.register(AccountDetail)
admin.site.register(CacheVoterData)
admin.site.register(WorkerProfile)
admin.site.register(Task)
