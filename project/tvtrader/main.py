import uvicorn
import json
from fastapi import FastAPI
from item import Item
from robot import Robot

app = FastAPI()

@app.post("/buy")
def buy(item: Item):
    robot.on_recieve_command('buy', item)

@app.post("/sell")
def sell(item: Item):
    robot.on_recieve_command('sell', item)

if __name__ == '__main__':
    f = open('config/app.json')
    config = json.load(f)
    robot = Robot(config)
    uvicorn.run(app='main:app', host="0.0.0.0", port=80, reload=True)