from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import time
import logging

log_api = logging.getLogger("errors")
# @app.middleware("http") 
# como lo declaro a parte no puedo usar el decorador 
# para registrarlo debo convertirlo en Class y usar usar app.add_middleware()
class LogRequestTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request, call_next:RequestResponseEndpoint)-> Response:

        start_time=time.time()
        response = await call_next(request)
        process_time=time.time() - start_time

        log_api.error(f"la request: {request.url} tarda : {process_time:.4f} s")

        return response
    

#  En FastAPI, usas el método dispatch en middleware porque es la implementación 
#   estándar de Starlette para middleware personalizado.