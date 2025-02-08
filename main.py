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
# This will be done if I have time left to do provided player_ids
# from game import check_db_for_player
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

# There's no requirements on root. So just error out/tell the user what to do.    
@app.get("/")
def read_root():
    return {"message": "Welcome to Naughts and Oughts. Functionality can be found on the /no/* endpoints."}

# Create a new Game.
#
# This involves initializing a new game, with a new player ID.
# TODO: Add optional player ID support.
#
# Requirement:
# Allows me to create a new game of Noughts and Crosses, and returns the game ID.
@app.get("/no/new")
# This can't be async because we're making a hard DB call. (At least, FastAPI thinks it shouldn't be async)
def start_new_game(player_id = None):
    # Set up a game
    
    # "Future" support for a provided player_id
    # Because it's awful UX if you can't used an ID you want to use. But I don't want to think about how to bind it to a specific person
    # Since it's opening up the whole mess of needing to password/secure it, and there's almost certianly not time for this.
    #if player_id == None:
    #    check_db_for_player(player)
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
    game_id = storage.save(new_game).inserted_id
    return {"message":"New game created with ID: "+ f"{game_id}" + "Your player ID for this game is: " + f"{player}"}

# Make a play on an existing game.
# 
# Needs the ID of the game that is being played.
# Needs to have the player ID for that game, else you aren't authorized.
# It'll be a query param for me, most likely. It should really be a header field. I'll do one of these.
#
# Requirement:
# Allows me to make the next move by specifying the co-ordinates I wish to move on. e.g. {"x": 1, "y": 1} 
# would denote a move to the middle square by the requesting player, and returns the new state of the board after the computer has made its move in turn. 
# Note: There is no need to create an AI opponent, random moves are fine
@app.get("/no/play/{game_id}")
def play_game():
    return {"message":"Play a turn on a game"}

# Return the plays done in order of a given game
#
# Requirement:
# Allows me to view all moves in a game, chronologically ordered.
@app.get("/no/{game_id}/history")
def play_history():
    return {"message":"Return the history of plays for the given game_id"}

# Return the play history for a player with the given ID.
#
# Return nothing on a miss, on a hit return the list of game_ids of played games.
#
# Requirement: 
# Allows me to view all games I have played, chronologically ordered.
@app.get("/no/{player_id}/history")
def player_history():
    return {"message":"Get the history of games played for a specific player_id"}