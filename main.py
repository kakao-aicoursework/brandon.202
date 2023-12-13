import logging
from fastapi import FastAPI
from presentations import root_router

app = FastAPI()
app.include_router(root_router)

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(name)-16s %(levelname)-8s %(message)s ",
  datefmt="%Y-%m-%d %H:%M:%S"
)

if __name__ == "__main__":
  pass
