from typing import List, Optional
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int



class Project(BaseModel):
    project_id: int
    title: str
    owner: User
    tags: List[str]
    description: Optional[str] = None


def create_user(user_id: int, name: str, email: str, age: int) -> User:
    return User(
        id=user_id,
        name=name,
        email=email,
        age=age
    )


def get_user_name(user: User) -> str:
    return user.name


def get_project_title(project: Project) -> str:
    return project.title


def count_tags(project: Project) -> int:
    return len(project.tags)


def is_adult(user: User) -> bool:
    return user.age >= 18



user = create_user(
    1,
    "Anurag",
    "anurag@gmail.com",
    20
)


project = Project(
    project_id=101,
    title="AI Engineering Roadmap",
    owner=user,
    tags=["python", "pydantic", "mypy"]
)


print("User Name:", get_user_name(user))
print("Project Title:", get_project_title(project))
print("Number of Tags:", count_tags(project))
print("Is Adult:", is_adult(user))


print("\nUser Details:")
print(user)

print("\nProject Details:")
print(project)


