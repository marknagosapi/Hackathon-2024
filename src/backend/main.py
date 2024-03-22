from routers.router import router 
from config.database import engine
from models import  user, admin, bill, item
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


user.Base.metadata.create_all(bind=engine)
admin.Base.metadata.create_all(bind=engine)
bill.Base.metadata.crate_all(bind=engine)
item.Base.metadata.crate_all(bind=engine)

app.include_router(router)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
