from fastapi import APIRouter, Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create-task")
def create_tasks(body:TaskSchema, db = Depends(get_db)):
    return controller.create_task(body, db)

@task_routes.get("/")
def get_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get("/get-task/{id}")
def get_task(id:int, db = Depends(get_db)):
    return controller.get_task(id, db)

@task_routes.put("/update-task/{id}")
def get_task(body:TaskSchema, id:int, db = Depends(get_db)):
    return controller.update_task(body, id, db)

@task_routes.delete("/delete-task/{id}")
def get_task(id:int, db = Depends(get_db)):
    return controller.delete_task(id, db)