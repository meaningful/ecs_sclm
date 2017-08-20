from django.contrib import admin
from prodire.models import Pro_icon
# Register your models here.

def updatePicture(request):
    if request.method == 'post':
        picture = request.FILES['picture']

    if picture:
        picturetime= request.user.username+str(time.time()).split('.')[0]
        picture_last=str(picture).split('.')[-1]
        picturename='photos/%s.%s'%(picturetime,picture_last)
        img=Image.open(picture)
        img.save('media/'+picturename)

class Pro_iconAdmin(admin.ModelAdmin):

    fields = ('icon_name', 'photo_tag', )
    readonly_fields = ('photo_tag',)
    actions = [updatePicture]
admin.site.register(Pro_icon, Pro_iconAdmin)
# admin.site.register(Pro_icon)
# 
