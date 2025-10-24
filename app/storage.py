import json
from typing import List, Optional
from .models import Todo

# Storage is Redis:
# - a sorted list of todo IDs in key: TODOS_ORDER
# - each todo stored as hash at key: TODO:<id>  (or JSON string)
# Using JSON strings to keep it simple.

TODOS_ORDER = "TODOS_ORDER"

class TodoStorage:
    def __init__(self, redis_client):
        self.r = redis_client

    def _todo_key(self, todo_id: str) -> str:
        return f"TODO:{todo_id}"

    def add(self, todo: Todo) -> Todo:
        pipe = self.r.pipeline()
        pipe.set(self._todo_key(todo.id), json.dumps(todo.to_dict()))
        # add to ordered list (left push = newest first)
        pipe.lpush(TODOS_ORDER, todo.id)
        pipe.execute()
        return todo

    def get(self, todo_id: str) -> Optional[Todo]:
        raw = self.r.get(self._todo_key(todo_id))
        if not raw:
            return None
        data = json.loads(raw)
        return Todo(**data)

    def list_all(self) -> List[Todo]:
        ids = self.r.lrange(TODOS_ORDER, 0, -1)  # bytes
        todos: List[Todo] = []
        for b in ids:
            tid = b.decode()
            t = self.get(tid)
            if t:
                todos.append(t)
        return todos

    def update(self, todo: Todo) -> bool:
        if not self.r.exists(self._todo_key(todo.id)):
            return False
        self.r.set(self._todo_key(todo.id), json.dumps(todo.to_dict()))
        return True

    def toggle(self, todo_id: str) -> Optional[Todo]:
        t = self.get(todo_id)
        if not t:
            return None
        t.done = not t.done
        self.update(t)
        return t

    def delete(self, todo_id: str) -> bool:
        pipe = self.r.pipeline()
        pipe.delete(self._todo_key(todo_id))
        pipe.lrem(TODOS_ORDER, 0, todo_id)
        res = pipe.execute()
        # res[0] = number of keys removed, res[1] = number removed from list
        return bool(res and (res[0] or res[1]))

    def clear_completed(self) -> int:
        # Walk list and remove completed ones
        ids = [b.decode() for b in self.r.lrange(TODOS_ORDER, 0, -1)]
        removed = 0
        for tid in ids:
            t = self.get(tid)
            if t and t.done:
                if self.delete(tid):
                    removed += 1
        return removed

    def reset_all(self):
        # Dev helper
        ids = [b.decode() for b in self.r.lrange(TODOS_ORDER, 0, -1)]
        for tid in ids:
            self.r.delete(self._todo_key(tid))
        self.r.delete(TODOS_ORDER)
