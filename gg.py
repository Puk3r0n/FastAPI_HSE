from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import FastAPIUsers

from fastapi import Request

from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth.auth_cookie import *
from database.models.database import Users, get_async_session
from auth.manager import get_user_manager
from auth.chemas import UserRead, UserCreate

from tasks.models import TaskPriority, TaskStatus

from models.models import Users
from tasks.models import Task

app = FastAPI(
    title="School App"
)

fastapi_users = FastAPIUsers[Users, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()

tasks_list = []
task_id_count = 0


async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(Users)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@app.post("/tasks/", response_model=Task, tags=["Tasks"])
async def create_task(task: dict, current_user: Users = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    new_task = Task(**task, user_id=current_user.id)
    session.add(new_task)
    await session.commit()
    return new_task


@app.get("/users/", tags=["Получение зарегестрированных пользователей"])
async def read_users(all_users: list[Users] = Depends(get_all_users)):
    return all_users


@app.get("/tasks/all", response_model=list[Task], tags=["Просмотр всех заданий"])
def get_tasks():
    return tasks_list


@app.get("/tasks/{task_id}", response_model=Task, tags=["Получение задания по id"])
def get_task_by_id(task_id: int):
    if task_id < 0 or task_id >= len(tasks_list):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_list[task_id]


@app.put("/tasks/{task_id}", response_model=Task, tags=["Замена задания по id"])
def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks_list):
        raise HTTPException(status_code=404, detail="Task not found")

    tasks_list[task_id] = task
    task.task_id = task_id

    return task


@app.post("/tasks/all_status", response_model=list[Task], tags=["Получение задания(ий) по статусу"])
def get_tasks_by_status(status: TaskStatus = Query(None)):
    if not tasks_list:
        raise HTTPException(status_code=404, detail="Tasks list is empty")

    filtered_tasks = [task for task in tasks_list if task.status == status]

    if not filtered_tasks:
        raise HTTPException(status_code=404, detail="There are no tasks that satisfy the condition")

    if status:
        if status not in TaskStatus:
            raise HTTPException(status_code=404, detail="Status not found")
        else:
            return filtered_tasks
    else:
        raise HTTPException(status_code=404, detail="Status field is empty")


@app.delete("/tasks/{task_id}", response_model=Task, tags=["Удаление задания по id"])
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks_list):
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = tasks_list.pop(task_id)
    return deleted_task


@app.get("/tasks/priority/", response_model=list[Task], tags=["Топ-N самых приоритетных задач"])
def get_priority_tasks(top_n: int = Query(..., gt=0)):
    if not tasks_list:
        raise HTTPException(status_code=404, detail="Tasks list is empty")

    priority_tasks = sorted(tasks_list,key=lambda x: (
        0 if x.priority == TaskPriority.high else (1 if x.priority == TaskPriority.medium else 2),
        x.title
    ))

    priority_tasks = priority_tasks[:top_n]

    return priority_tasks


@app.post("/tasks/search", response_model=list[Task], tags=["Поиск задачи по тексту"])
def search_tasks_by_text(text: str):
    if not tasks_list:
        raise HTTPException(status_code=404, detail="Tasks list is empty")

    found_tasks = []
    for task in tasks_list:
        if text.lower() in task.title.lower() or text.lower() in task.description.lower():
            found_tasks.append(task)

    if not found_tasks:
        raise HTTPException(status_code=404, detail="No tasks found matching the search criteria")

    return found_tasks




# @app.get("/protected-route")
# def protected_route(user: Users = Depends(current_user)):
#     return f"Hello, {user.username}"


# @app.get("/unprotected-route")
# def unprotected_route():
#     return f"hello, anonym"
