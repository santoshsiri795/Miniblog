from django.contrib import admin
from .models import post,Contact

# Register your models here.
@admin.register(post)
class postModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','desc']

admin.site.register(Contact)
#class contactModelAdmin(admin.ModelAdmin):
    #list_display= ['id','name','email','address','message']