from django.shortcuts import render

# Create your views here.
def updatePicture(request):
    if request.method == 'post':
        photo = request.FILES['photo']
    if photo:
        picturetime= request.user.username+str(time.time()).split('.')[0]
        picture_last=str(photo).split('.')[-1]
        picturename='photos/%s.%s'%(picturetime,picture_last)
        img=Image.open(photo)
        img.save('media/'+picturename)
