from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.post("/reads/")
def start_reading():
    session_id = None
    return {"session_id": session_id}


@app.put("/reads/{session_id}")
def stop_reading(session_id: int):
    return {"session_id": session_id}
