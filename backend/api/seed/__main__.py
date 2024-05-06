from seed_from_json import (
    seed_task_category_from_json,
    seed_user_from_json,
    seed_tasks_from_json,
)
import os


if __name__ == "__main__":
    users = seed_user_from_json(os.path.join("seed_dataa", r"users.json"))
    categories = seed_task_category_from_json(
        os.path.join("seed_dataa", r"task_categories.json")
    )
    tasks = seed_tasks_from_json(
        os.path.join("seed_dataa", r"tasks.json"), users[0]
    )
