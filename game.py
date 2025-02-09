from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId, AbstractRepository
from typing import List, Optional
import uuid
import logging

logging.basicConfig(filename="no_gamelogic.log", level=logging.INFO)

class Row(BaseModel):
    col_1: Optional[str] = ""
    col_2: Optional[str] = ""
    col_3: Optional[str] = ""

# A turn consists of an iterator, the player who takes the turn, and their selection.
#
# If a user attempts an invalid action, that doesn't "count" for their turn being executed.
class Turn(BaseModel):
    # Starts at 1, iterates until win.
    # Must be provided when posting a move in order to make sure you aren't cheating~
    turn_number: int
    player: str
    row: int
    col: int    

class Game(BaseModel):
    id: Optional[PydanticObjectId] = None
    player_id: uuid.UUID
    game_board: List[Row]
    current_turn: int
    turn_history: List[Turn]
    game_over: bool

class GameStorage(AbstractRepository[Game]):
    class Meta:
        collection_name = "games"

# Submit a turn
# This function is the abstraction of a turn into something uniform to save sanity for devs who dare to look at the main.py file.
def submit_turn(submitted_turn):
    turn_validation = validate_turn(submitted_turn)
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
def validate_turn(incoming_turn):
    # This is a set of the rules needed to be followed to make sure a turn is valid.
    print("Validated the turn. Proceed.")

# Attempt to execute a turn
# By the end of this function, we should have commited the turn the DB or returned an error. 
# If 
def execute_turn():
    print("Do a turn")

# Finalize a turn to get the next turn opened up
# This is where we commit to the D
def finalize_turn():
    print("Finalized the turn. Replying to user")
    
# This will be defined if I have time.
#def check_db_for_player(player_id):
#    # Check the DB to see if the player ID exists.