from lobby.utils.token import get_jwt_data, decode_jwt

class AuthMiddleware:
    
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = ""
        for header in scope['headers']:
            if header[0].decode('ASCII') == 'cookie':
                scope['room_name'] = str(header[0])
                cookies = header[1].decode('ASCII').split(';')
                for cookie in cookies:
                    scope['room_name'] = cookie.split("=")
                    if (cookie.split("=")[0].strip() == "session"):
                        token = (cookie.split("=")[1])
                        break
                break
        decode = decode_jwt(token)
        if "error" in decode:
            scope["token_check"] = "error"
            # await send({'type': 'websocket.close', 'code': 401})
            # return 
        else:
            scope["token_check"] = decode
            # await
        return await self.inner(scope, receive, send)