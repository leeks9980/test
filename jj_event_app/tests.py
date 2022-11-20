from django.test import TestCase

# Create your tests here.

#def 변수 설정 
asd =21
def a(b,asd):
    if b == 'p':
        return 123
    elif b == 's':
        return'%s'%(asd)
print(a('s',asd))

#이미지 출력
from django.core.files.storage import FileSystemStorage
import os
import shutil
image_lable = 0
@csrf_exempt
def test(request):
    global image_lable 
    if request.method == 'GET':
        return HttpResponse('''
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>    
            <form action = "/test/" method="POST" enctype="multipart/form-data">
                <input type = "file" name = image>
                <input type = "submit">
            </form>
        </body>
        </html> 
        ''')
    elif request.method == 'POST':
        a = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(f"image_{image_lable}.jpg", a)
        shutil.move(f"C:/python_workspace/{filename}","C:\python_workspace\static\image")
        image_lable += 1
        #C:\python_workspace\image\image_0.jpg
        return HttpResponse('''
        <!doctype html>
        <html>
        <body>
            <img src="/static/image/%s" alt="image">
        </body>
        </html>
        '''%(filename))   