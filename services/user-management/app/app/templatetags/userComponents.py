from django import template
from app.models import User

register = template.Library()

@register.inclusion_tag("userComponent.html")
def userComponent(id):
    username = User.objects.filter(pk=id).values_list("username", flat=True).first()
    return {"user": {"username": username, "playerId": id}}

@register.inclusion_tag("friendButton.html")
def friendButton(userId, friendId):
    if userId == friendId:
        return {"visibility": False}
    friendStatus = User.objects.filter(pk=userId, friends__contains=[friendId]).exists()
    return {"visibility": True, "friendStatus": friendStatus, "friendId": friendId}