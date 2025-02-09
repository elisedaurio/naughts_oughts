from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId, AbstractRepository
from typing import List, Optional
from pymongo import MongoClient
import uuid
import logging

logging.basicConfig(filename="no_gamelogic.log", level=logging.INFO)

# A turn consists of an iterator, the player who takes the turn, and their selection.
#
# If a user attempts an invalid action, that doesn't "count" for their turn being executed.
class Turn(BaseModel):
    # Starts at 1, iterates until win.
    # Must be provided when posting a move in order to make sure you aren't cheating~
    game_id: uuid
    turn_number: int
    player: uuid
    row: int
    col: int    

class Game(BaseModel):
    # The ID of the game
    id: Optional[PydanticObjectId] = None
    # UUID of the human player
    player_id: uuid.UUID
    # Active player is either the CPU or the player. Capture the string representation here
    active_player: str = None
    # The current state of the game board. A list of three rows
    game_board: List
    # The current turn number. (Tracking how many turns have occurred.)
    current_turn: int
    # Capture each turn as it happens
    turn_history: List[Turn] = None
    # Track if the game has ended
    game_over: bool = False

class GameStorage(AbstractRepository[Game]):
    class Meta:
        collection_name = "games"

# Submit a turn
# This function is the abstraction of a turn into something uniform to save sanity for devs who dare to look at the main.py file.
def submit_turn(submitted_turn, db_storage):
    turn_validation = validate_turn(submitted_turn, db_storage)
    if turn_validation == True:
        executed_turn = execute_turn(submitted_turn)
        if executed_turn == True:
            finalized_turn = finalize_turn(submitted_turn)
            if finalize_turn == False:
                logging.info("Turn failed to finalize.")
            else:
                logging.info("Turn successful.")
        else: 
            logging.info("Turn failed to execute.")
    else: 
        logging.info("Turn failed to validate.")

    
# Make sure the turn is valid.
# This will return true if the turn is valid from what we can tell.
def validate_turn(incoming_turn: Turn, db_storage:GameStorage):
    # This is a set of the rules needed to be followed to make sure a turn is valid.
    
    # Load the game from the game_id
    current_game = Game(db_storage.find_one_by_id(incoming_turn.game_id))
    
    # Validations
    # Is the game over?
    if current_game.game_over == True:
        # Failed
        logging.info("Game with ID: " + f"{current_game.id}" + " is already over.")
        return False
    
    # Was the right turn submitted?
    if current_game.current_turn != incoming_turn.turn_number:
        # The wrong turn was submitted
        logging.info("Game with ID: " + f"{current_game.id}" + " is not currently on the submitted turn of: " + f"{incoming_turn.turn_number}" + ". It is on turn: " + f"{current_game.current_turn}")
        return False
    
    # Is this right player taking a turn?
    if current_game.active_player != incoming_turn.player:
        logging.info("Game with ID: " + f"{current_game.id}" + " is not currently on the player's  turn. Please wait for the CPU to take a turn.")
        return False        
    # Was x and y 1,2 or 3?
    if incoming_turn.col not in { 1,2,3}:
        logging.info("Submitted a column value that isn't valid. Submitted: " + f"{incoming_turn.col}")
        return False
    else:
        if incoming_turn.row not in { 1,2,3}:
            logging.info("Submitted a row value that isn't valid. Submitted: " + f"{incoming_turn.row}")
            return False
        else:
            logging.info("Valid coordinates submitted.")
    # Was the the (x,y) coordinate Null or populated?
    # Recall this is a list of lists, so we need to fix the index offsets by removing 1
    if current_game.game_board[(incoming_turn.row-1)][incoming_turn.col-1] is not "":
        logging.info("Submitted a row and column that isn't empty. Submitted: " + f"{incoming_turn.row}")
        return False
    
    print("Validated the turn. Proceed to submission.")
    return True

# Attempt to execute a turn
# By the end of this function, we should have commited the turn the DB or returned an error. 
# If 
def execute_turn(validated_turn):
    print("Do a turn")

# Finalize a turn to get the next turn opened up
# This is where we commit to the D
def finalize_turn():
    print("Finalized the turn. Replying to user")
    
# This will be defined if I have time.
#def check_db_for_player(player_id):
#    # Check the DB to see if the player ID exists.