# main.py
import logging.config
import os
import uvicorn
from fastapi import FastAPI
from routers import client_router

# Asumimos que tienes un logging.ini similar al del otro servicio
# Si no, puedes eliminar estas líneas por ahora.
# logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "logging.ini"))
# logger = logging.getLogger(__name__)

DESCRIPTION = """
Client service to interact with manufacturing microservices.
"""

app = FastAPI(
    title="Client Service",
    description=DESCRIPTION,
    version="1.0.0",
)

app.include_router(client_router.router)

if __name__ == "__main__":
    # Ejecutaremos este servicio en un puerto diferente, por ejemplo, 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)