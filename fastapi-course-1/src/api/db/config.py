from decouple import config as decouple_config

DATABASE_URL = decouple_config("DATABASE_URL", default="database url not found") # coge el valor de la variable de entorno del archivo .env y lo pone en la variable


