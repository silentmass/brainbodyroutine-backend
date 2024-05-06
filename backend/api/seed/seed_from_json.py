import json
from backend.api.src.routes.taskcategories.controller import (
    create_task_category,
    get_task_category_by_title,
)
from backend.api.src.routes.taskcategories.schemas import TaskCategoryCreate
from backend.api.src.routes.tasks.controller import create_user_task
from backend.api.src.routes.tasks.schemas import TaskBase
from backend.api.src.routes.users.controller import (
    create_user,
    get_user_by_username,
    get_users,
)
from backend.api.src.routes.users.schemas import User, UserCreate
from backend.api.src.routes.utils.db_dependency import get_db


# Function to load data from JSON and seed database
def seed_user_from_json(filepath):
    db = next(get_db())
    # Read JSON file
    with open(filepath, "r") as file:
        data = json.load(file)

    # Create a list of User instances
    for user in data:
        db_user = get_user_by_username(db, user["username"])
        if db_user is None:
            create_user(
                db,
                UserCreate(
                    username=user["username"],
                    password=user["password"],
                    email=user["email"],
                    full_name=user["full_name"],
                    disabled=user["disabled"],
                ),
            )
    users = get_users(db)
    # Close the session
    db.close()
    return users


def seed_task_category_from_json(filepath):
    db = next(get_db())
    # Read JSON file
    with open(filepath, "r") as file:
        data = json.load(file)

    categories = []
    for category in data:
        db_task_category = get_task_category_by_title(
            db, task_category_title=category["title"]
        )
        if db_task_category is None:
            new_category = create_task_category(
                db,
                TaskCategoryCreate(
                    title=category["title"],
                    description=category["description"],
                ),
            )
            categories.append(new_category)
    # Close the session
    db.close()
    return categories


def seed_tasks_from_json(filepath, user: User):
    db = next(get_db())
    # Read JSON file
    with open(filepath, "r") as file:
        data = json.load(file)

    tasks = []
    for task in data:
        new_task = create_user_task(
            db,
            TaskBase(
                title=task["title"],
                task_category_id=task["task_category_id"],
                is_active=task["is_active"],
            ),
            user,
        )
        tasks.append(new_task)
    # Close the session
    db.close()
    return tasks
