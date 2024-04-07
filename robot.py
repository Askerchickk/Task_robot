import asyncio
import uvicorn
from fastapi import FastAPI, Request
from typing import Optional

app = FastAPI()

# Робот - это отдельный Python-скрипт, который будет работать асинхронно
async def robot(start_from: int = 0):
    """
    Робот, который каждую секунду выводит в консоль числа, начиная с указанного.
    """
    while True:
        print(start_from)
        start_from += 1
        await asyncio.sleep(1)

# Переменная для хранения задачи робота
robot_task = None

@app.get("/start_robot")
async def start_robot(start_from: Optional[int] = 0):
    """
    Запускает робота с указанного числа (по умолчанию - с 0).
    """
    global robot_task
    if robot_task is None or robot_task.done():
        robot_task = asyncio.create_task(robot(start_from))
    return {"message": f"Робот запущен, начиная с числа {start_from}"}

@app.get("/stop_robot")
async def stop_robot():
    """
    Останавливает робота.
    """
    global robot_task
    if robot_task is not None and not robot_task.done():
        robot_task.cancel()
        robot_task = None
    return {"message": "Робот остановлен"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)