from django import template
from profile.models import User
from datetime import timedelta
from django.utils.timezone import now

register = template.Library()

@register.inclusion_tag("userComponent.html")
def userComponent(id):
    if User.objects.filter(pk=id).exists():
        user = User.objects.get(pk=id)
        user.lastConnection = True if (now() - user.lastConnection) <= timedelta(minutes=5) else False
        return {"user": user}
    return {"user": {"username": "Unknown", "eloPong": 400, "eloConnect": 400, "role": "D", "theme": [10935979,5923722,2961991], "lastConnection": False, "playerId": id}}

@register.inclusion_tag("friendButton.html")
def friendButton(userId, friendId):
    if userId == friendId:
        return {"visibility": False}
    friendStatus = User.objects.filter(pk=userId, friends__contains=[friendId]).exists()
    return {"visibility": True, "friendStatus": friendStatus, "friendId": friendId}