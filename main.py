import bson
import logging
import uuid
from pymongo import MongoClient
from random import randint
from fastapi import FastAPI
from game import Game
from game import GameStorage
from game import Turn
from game import submit_turn
# This will be done if I have time left to do provided player_ids
# from game import check_db_for_player
from rich import print, print_json

# Start logger
logging.basicConfig(
    filename="no.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# Start the DB for the game.
# Requires a default setup of MongoDB, with a collection at `games`
host = "localhost"
port = 27017

# Realistically this should be an environment variable
cpu_uuid = uuid.UUID("4711e492-f922-4d20-99cf-51d4606bd314")

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
def start_new_game():
    # Set up a game
    
    # "Future" support for a provided player_id
    # Because it's awful UX if you can't used an ID you want to use. But I don't want to think about how to bind it to a specific person
    # Since it's opening up the whole mess of needing to password/secure it, and there's almost certianly not time for this.
    #if player_id == None:
    #    check_db_for_player(player)
    # Player ID is unique each time, it's a hyper basic authentication method. We give it to them at the start and call it good.
    
    # This could be improved by adding support for a provided player ID to let you stack up games on your single ID 
    player = uuid.uuid4()
    
    # We need to convert the ID into something that MongoDB is happy storing
    bson_player = bson.Binary.from_uuid(player)
    
    # Initialize the game object
    # Note: The player is always 1 in the turn order. 0 is the Cpu
    first_turn = randint(0,1)
    # We need to set the active player based on this result
    initial_board = [["","",""], ["","",""],["","",""]]
    new_game = Game(player_id=bson_player, game_board=initial_board, current_turn=1, active_player=player)
    
    # Set the active player based on the first_turn outcome
    if first_turn == 0:
        new_game.active_player = cpu_uuid
    else:
        new_game.active_player = player
    
    logging.info("Created new game. Dumping model")
    logging.info(new_game.model_dump)
    # Insert the new game to the DB
    game_id = storage.save(new_game).inserted_id
    
    # We need to take a turn right away if the CPU was given turn 1
    if first_turn == 0:
        # Computer submits a turn
        cpu_turn = Turn(turn_number=1, player=cpu_uuid, row=randint(1,3), col=randint(1,3),game_id=new_game.id)
        submit_turn(cpu_turn)
        return {"message":"New game created with ID: "+ f"{game_id}" + " \nYour player ID for this game is: " + f"{player}" + " Note: The CPU had the first turn, Check the game's history for it's action."}
    else:
        # We return the normal messaging if the human player is the first actor
        return {"message":"New game created with ID: "+ f"{game_id}" + " \nYour player ID for this game is: " + f"{player}"}

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
@app.post("/no/playturn")
def play_game_turn(incoming_turn: Turn):
    # Submit a turn
    # This will require the game_id, the turn contents, and a reference to the storage collection.
    submit_turn(incoming_turn)
    
    # Load the game one last time to deliver the game state on return
    try:
        # Load the game from the game_id
        loaded_game_from_id = storage.find_one_by_id(incoming_turn.game_id)
        current_game_state = Game(
            player_id=loaded_game_from_id.player_id, 
            game_board=loaded_game_from_id.game_board, 
            current_turn=loaded_game_from_id.current_turn, 
            active_player=loaded_game_from_id.active_player,
            game_over=loaded_game_from_id.game_over
            )
    except:
        logging.info("Error loading the game.")        
    return {"message":"Turn completed. New game state: " + f"{current_game_state.model_dump_json}"}

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