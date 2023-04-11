from .settings import *




DATABASES = {
    "default": env.db("DATABASE_URL_DEPLOY"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
