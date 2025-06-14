from fastapi import FastAPI
from typing import Union

# from api.events.routing import router as events_router
# le puedo quitar el .routing xq desde el __init__ ya lo exporto, por lo q podemos importar directeamente desde el paquete
from api.events import router as events_router

app = FastAPI()
app.include_router(events_router, prefix='/api/events')



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str,None]=None):
    print(item_id)
    return {"item-id": item_id, "q": q}

@app.get('/healthz')
def api_health():
    return  {"status": "ok"}


