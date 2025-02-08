import bson
import logging
from uuid import uuid4
from pymongo import MongoClient
from pymongo import collection
from pymongo import InsertOne
from random import randint
from fastapi import FastAPI
from game import Row
from game import Game
from game import GameStorage
from game import check_db_for_player
from rich import print, print_json

# Start logger
logging.basicConfig(filename="no.log", level=logging.INFO)

# Start the DB for the game.
# Requires a default setup of MongoDB, with a collection at `games`
host = "localhost"
port = 27017

try:
    db_client = MongoClient(host, port, uuidRepresentation='standard')
    # Naughts and oughts DB
    db = db_client["naughts"]
    # Games Collection
    storage = GameStorage(database=db)
except ConnectionError:
    print("DB Connection error: " + ConnectionError.message)


# Start FastAPI
app = FastAPI()
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/no/new")
# This can't be async because we're making a hard DB call. (At least, FastAPI thinks it shouldn't be async)
def start_new_game(player_id = None):
    # Set up a game
    
    if player_id == None:
        check_db_for_player(player)
    # Player ID is unique each time, it's a hyper basic authentication method. We give it to them at the start and call it good.
    # This could be improved by adding support for a provided player ID to let you stack up games on your single ID 
    player = uuid4()
    
    # We need to convert the ID into something that MongoDB is happy storing
    bson_player = bson.Binary.from_uuid(player)
    
    # Initialize the game object
    # Note: The player is always 0 in the turn order. 1 is the Cpu
    first_turn = randint(0,1)
    initial_row = Row()
    initial_board = [initial_row,initial_row,initial_row]
    new_game = Game(player_id=bson_player, game_board=initial_board, current_turn=first_turn)
    logging.info("Created new game. Dumping model")
    logging.info(new_game.model_dump)
    # Insert the new game to the DB
    #game_id = game_repo.insert_one(new_game.model_dump_json).inserted_id
    game_id = storage.save(new_game).inserted_id
    return {"message":"New game created with ID: "+ f"{game_id}" + "Your player ID for this game is: " + f"{player}"}

@app.get("/no/play/{game_id}")
def play_game():
    return {"messaage":"New game created: "}
