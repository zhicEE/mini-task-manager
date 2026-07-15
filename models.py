class Task:
    
    def __init__(self, title, deadline, completed=False, task_id=None):
        self.id = task_id
        self.title = title
        self.deadline = deadline
        self.completed = completed