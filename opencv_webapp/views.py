from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face


# Create your views here.
def first_view(request):

    return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        form = SimpleUploadForm(request.POST, request.FILES)


        if form.is_valid(): #폼스 파일이 이상이 없는지 벨리데이션 체크.

            myfile = request.FILES['image']# 유저가 업로드한 파일을 얻어낼수있는 코드
            fs = FileSystemStorage()  #파일 관리해주는 심부름꾼
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)# '/media/ses.jpg'

            context = {'form': form, 'uploaded_file_url': uploaded_file_url}# filled form
            return render(request, 'opencv_webapp/simple_upload.html', context)


    else: # GET request
        form = SimpleUploadForm()
        context = {'form': form}# empty form
        return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):

    if request.method == 'POST':

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name

            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            print(form.instance.document.name)

            context = {'form':form, 'post':post}

            return render(request, 'opencv_webapp/detect_face.html', context)

    else:
        form = ImageUploadForm()# empty form
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
