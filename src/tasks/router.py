from typing import List
from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create-task", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_tasks(body:TaskSchema, db:Session = Depends(get_db)):
    return controller.create_task(body, db)

@task_routes.get("/", response_model=List[TaskResponseSchema], status_code=status.HTTP_200_OK)
def get_tasks(db:Session = Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get("/get-task/{id}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
def get_task(id:int, db:Session = Depends(get_db)):
    return controller.get_task(id, db)

@task_routes.put("/update-task/{id}", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def get_task(body:TaskSchema, id:int, db:Session = Depends(get_db)):
    return controller.update_task(body, id, db)

@task_routes.delete("/delete-task/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def get_task(id:int, db:Session = Depends(get_db)):
    return controller.delete_task(id, db)