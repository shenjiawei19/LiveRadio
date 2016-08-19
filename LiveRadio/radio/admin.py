from django.contrib import admin
from models import User,Category,Group,Node,Node_detail
# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Category)
admin.site.register(Node)
admin.site.register(Node_detail)
