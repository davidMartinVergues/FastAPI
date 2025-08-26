from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import time
import logging
import json
log_api = logging.getLogger("api")
# @app.middleware("http") 
# como lo declaro a parte no puedo usar el decorador 
# para registrarlo debo convertirlo en Class y usar usar app.add_middleware()
class LogRequestHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request, call_next:RequestResponseEndpoint)-> Response:

        response = await call_next(request)

        headers_dict = dict(request.headers)
        headers_json = json.dumps(headers_dict, indent=2,
        ensure_ascii=False)
        log_api.info(f"Request: {request.url}\n Headers:\n{headers_json}")

        return response
    

#  En FastAPI, usas el método dispatch en middleware porque es la implementación 
#   estándar de Starlette para middleware personalizado.