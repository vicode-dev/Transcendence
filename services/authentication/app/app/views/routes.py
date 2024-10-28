# from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# from .models import Book
import json
from django.shortcuts import render

from app.views.register import *

# def html_page(request):
# 	return render(request, 'test.html')

# @csrf_exempt
# def book_get(request, user_id):
# 	try:
# 		book = Book.objects.get(title=user_id)
# 		return JsonResponse({'title': book.title, 'author': book.author, 'published date': book.published_date}, status=200)
# 	except Book.DoesNotExist:
# 		return JsonResponse({'error': 'title not found'}, status=404)
 
# @csrf_exempt
# @require_http_methods(["GET", "POST"])
# def book_list(request):
# 	if request.method == "GET":
# 		books = list(Book.objects.values())
# 		return JsonResponse(books, safe=False)
# 	if request.method == "POST":
# 		data = json.loads(request.body)
# 		book = Book.objects.create(
# 			title=data['title'],
# 			author=data['author'],
# 			published_date="1-1-1111"
# 		)
# 		return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': str(book.published_date)}, status=201)

# @csrf_exempt
# @require_http_methods(["GET", "PUT", "DELETE"])
# def book_detail(request, pk):
# 	try:
# 		book = Book.objects.get(pk=pk)
# 	except Book.DoesNotExist:
# 		return JsonResponse({'error': 'Book not found'}, status=404)

# 	if request.method == "GET":
# 		return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': str(book.published_date)})

# 	if request.method == "PUT":
# 		data = json.loads(request.body)
# 		book.title = data.get('title', book.title)
# 		book.author = data.get('author', book.author)
# 		book.published_date = data.get('published_date', book.published_date)
# 		book.save()
# 		return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': str(book.published_date)})

# 	if request.method == "DELETE":
# 		book.delete()
# 		return JsonResponse({'message': 'Book deleted'}, status=204)

# @csrf_exempt
# def html(request):
# 	if request.method == "POST":
# 		title = request.POST.get('box1')
# 		author = request.POST.get('box2')
# 		Book.objects.create(title=title, author=author, published_date="1111-1-1")
# 		return HttpResponse("HTML TEST\nTitle: " + title + "\nAuthor: " + author)
# 	if request.method == "GET":
# 		return HttpResponse("HTML TEST GET")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
	if request.method == "GET":
		return get_register()
	if request.method == "POST":
		return post_register()
