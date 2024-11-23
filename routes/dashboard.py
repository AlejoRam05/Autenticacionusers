from fastapi import APIRouter

router = APIRouter(prefix="/dashboard")


@router.get("/admin")
async def dashboard_admin():
    pass

@router.put("/admin")
async def logout_admin():
    pass

@router.get("/user")
async def dashboard_user():
    pass

@router.put("/user")
async def logout_user():
    pass


