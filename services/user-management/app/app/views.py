from django.http import HttpResponse
from django.http import JsonResponse
from . import blockchain
import requests, json

def index(request):
    html = "<html><body>%s</body></html>" % blockchain.test()
    return HttpResponse(html)

def setupContract(request):
    blockchain.setup()
    return HttpResponse("<h1>Ok</h1>")

def add(request):
    blockchain.addGameResult(1, [1, 2], [2, 3], 24, 0, 23)
    return HttpResponse("<h1>Ok</h1>")

def getGameResult(request, id):
    return JsonResponse(blockchain.getGameResult(id), safe=False)
def getGameNumber(request):
    return JsonResponse({'GameNumber': blockchain.getGameNumber()}, status=200)

def show(request, title):
	url = f'http://authentication:8000/book_get/{title}/'
	try:
		response = requests.get(url)
		if response.status_code == 200:
			data = response.json()
			return JsonResponse({'title': data['title'], 'author': data['author'], 'published date': data['published date']}, status=200)
		else:
			return JsonResponse({'error': 'could not retrieve ' + title}, status=response.status_code)
	except requests.exceptions.RequestException as e:
		return JsonResponse({'error': str(e)}, status=500)