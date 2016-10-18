from django.contrib import admin
from models import System, Item, History, Service, Trigger, \
    Template, Host_group, Host, Action_method, Action, Maintenance, Special, \
    Service_Group, Item_Group, FlowCar, FlowCount
# Register your models here.

class SpecialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'memo',)

admin.site.register(Special, SpecialAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'memo', 'group',)

admin.site.register(Item, ItemAdmin)

class FlowCarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','region', 'operator', 'memo', 'fees',)

admin.site.register(FlowCar, FlowCarAdmin)

class FlowCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'month',)

admin.site.register(FlowCount, FlowCountAdmin)

admin.site.register(System)
admin.site.register(Item_Group)
admin.site.register(History)
admin.site.register(Service)
admin.site.register(Service_Group)
admin.site.register(Trigger)
admin.site.register(Template)
admin.site.register(Host_group)
admin.site.register(Host)
admin.site.register(Action_method)
admin.site.register(Action)
admin.site.register(Maintenance)



