from django.shortcuts import render, reverse, redirect
from library.models import Book
from library.forms import UploadFileForm

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class BookView(APIView):

    renderer_classes = [JSONRenderer]
    def get(self, request):
        books = Book.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BookSerializer(books, many=True)
        return Response({"books": serializer.data})

def index(request):
    documents = Book.objects.all()
    if request.user.is_authenticated:
    
        if request.user.is_staff:
            is_staff = request.user.username
            return render(request, 'library/index.html', {'documents': documents, 'is_staff':is_staff})
        else:
            is_logged_in = request.user.username
            return render(request, 'library/index.html', {'documents': documents, 'is_logged_in':is_logged_in})
    else:
        return render(request, 'library/index.html', {'documents': documents})
def upload(request):
    if request.user.is_staff is True:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = Book(
                    pdf_file = request.FILES['pdf_file'], 
                    title=request.POST['title'], 
                    lowercase_title=request.POST['title'].lower(),
                    image=request.FILES['image']
                )
                newdoc.save()

                # Redirect to the document list after POST
                return HttpResponseRedirect('/upload/')
        else:
            form = UploadFileForm() # A empty, unbound form

        # Load documents for the list page
        documents = Book.objects.all()

        # Render list page with the documents and the form
        return render(
            request,
            'library/upload.html',
            {'documents': documents, 'form': form}
        )
    else:
        redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['inputUsername']
        email = request.POST['inputEmail']
        password = request.POST['inputPassword']
        try:
            u = User.objects.get(username=username)
            return render(
                request,
                'registration/register.html',
                {
                    'message': 'Пользователь с таким юзернеймом уже существует!'
                }
            )
        except:
            pass
        try:
            u = User.objects.get(email=email)
            return render(
                request,
                'registration/register.html',
                {
                    'message': 'Пользователь с такой почтой уже существует!'
                }
            )
        except:
            pass
        u = User.objects.create_user(username=username, email=email, password=password)
        u.save()
        print(username, email, password)
        return render(
            request,
            'registration/login.html',
            {
                'message': 'Вы успешно зарегестрировались!'
            }
        )
    else:
        return render(
            request,
            'registration/register.html'
        )

def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['inputUsername'], password=request.POST['inputPassword'])
        if user is not None:
            django_login(request, user)
            return redirect('/')
        else:
            return render(
                request, 
                'registration/login.html',
                {
                    'bad': 'Пользователь не существует!'
                }
            )
    else:
        return render(
            request,
            'registration/login.html',
        )

def logout(request):
    django_logout(request)
    return redirect('/')

def delete(request):
    if request.user.is_staff:
        pk = request.GET['pk']
        book = Book.objects.get(pk=pk)
        book.delete()
        return redirect('/')
    else:
        return redirect('/')

def search(request):
    try:
        query = request.GET['q']
        documents = Book.objects.filter(lowercase_title__icontains=query)
        if request.user.is_authenticated:
        
            if request.user.is_staff:
                is_staff = request.user.username
                return render(request, 'library/index.html', {'documents': documents, 'is_staff':is_staff})
            else:
                is_logged_in = request.user.username
                return render(request, 'library/index.html', {'documents': documents, 'is_logged_in':is_logged_in})
        else:
            return render(request, 'library/index.html', {'documents': documents})
    except:
        return redirect('/')