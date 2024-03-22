from routers.router import router 
from routers.user_router import router as user_router
from routers.admin_router import router as admin_router
from config.database import engine
from models import  user, admin, bill, item, level
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
bill.Base.metadata.create_all(bind=engine)
item.Base.metadata.create_all(bind=engine)
level.Base.metadata.create_all(bind=engine)



app.include_router(router)
app.include_router(user_router, prefix="", tags=["users"])
app.include_router(admin_router, prefix="", tags=["admins"])


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
