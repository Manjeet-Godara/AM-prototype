from django.contrib import admin
from .models import System, Agent, TestRun, Test, RunEvent

admin.site.register(System)
admin.site.register(Agent)
admin.site.register(TestRun)
admin.site.register(Test)
admin.site.register(RunEvent)