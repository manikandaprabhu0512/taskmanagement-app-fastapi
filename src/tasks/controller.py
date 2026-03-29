from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body:TaskSchema, db: Session):
    data = body.model_dump()

    new_task = TaskModel(title = data["title"], 
                        description = data["description"],
                        is_completed = data["is_completed"])
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)


    return { "status": "Task create Successfully",
            "data" : new_task }


def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return {"status" : "All tasks", "data" : tasks}

def get_task(id:int, db: Session):
    one_task = db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(404, detail="Task Id incorrect")

    return { "status": "Task fetched Successfully",
            "data" : one_task }

def update_task(body:TaskModel, id:int, db:Session):
    one_task = db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(404, detail="Task Id incorrect")
    
    body = body.model_dump()
    for field, value in body.items():
        setattr(one_task, field, value)
    
    db.add(one_task)
    db.commit()
    db.refresh(one_task)


    return { "status": "Task updated Successfully",
            "data" : one_task }

def delete_task(id:int, db:Session):
    one_task = db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(404, detail="Task Id incorrect")
    
    db.delete(one_task)
    db.commit()

    return { "status": "Task deleted Successfully",
            "data" : one_task }
    
