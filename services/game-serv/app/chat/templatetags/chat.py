from django import template

register = template.Library()

@register.inclusion_tag("chat/room.html")
def chat(id):
    return {"chatId": id}

