from fastapi import APIRouter

router = APIRouter()

# Mock Database for Resources (Ideally this comes from ChromaDB)
RESOURCES_DB = {
    "Cyber Security": [
        {"title": "Cyber Security for Beginners", "platform": "YouTube (Kevin Wallace)", "url": "https://www.youtube.com/watch?v=_S7aX7G0l48", "level": "Beginner"},
        {"title": "TryHackMe - Pre Security", "platform": "TryHackMe", "url": "https://tryhackme.com/path/outline/presecurity", "level": "Beginner"}
    ],
    "Computer Science": [
        {"title": "CS50: Introduction to Computer Science", "platform": "Harvard (EdX)", "url": "https://pll.harvard.edu/course/cs50-introduction-computer-science", "level": "Beginner"}
    ]
}

@router.get("/")
def get_resources(department: str):
    return RESOURCES_DB.get(department, [])
