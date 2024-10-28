from django.http import HttpResponse

def get_register():
	return HttpResponse("HTML TEST GET")

def post_register():
	return HttpResponse("HTML TEST POST")