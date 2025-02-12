from pydantic import BaseModel
from fastapi import HTTPException
from pymongo import MongoClient
from pydantic_mongo import PydanticObjectId, AbstractRepository
from pyobjectID import PyObjectId, MongoObjectId
from typing import List, Optional
from random import randint
import uuid
import logging

logging.basicConfig(
    filename="no_gamelogic.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# A turn consists of an iterator, the player who takes the turn, and their selection.
#
# If a user attempts an invalid action, that doesn't "count" for their turn being executed.
class Turn(BaseModel):
    # Starts at 1, iterates until win.
    # Must be provided when posting a move in order to make sure you aren't cheating~
    game_id: PyObjectId
    turn_number: int
    player: uuid.UUID
    row: int
    col: int    

class Game(BaseModel):
    # The ID of the game
    id: PyObjectId = None
    # UUID of the human player
    player_id: uuid.UUID
    # Active player is either the CPU or the player. Capture the string representation here
    active_player: uuid.UUID
    # The current state of the game board. A list of three rows
    game_board: List[List]
    # The current turn number. (Tracking how many turns have occurred.)
    current_turn: int
    # Capture each turn as it happens
    turn_history: Optional[List[Turn]] = []
    # Track if the game has ended
    game_over: bool = False
    # Who won the game if it's over?
    game_winner: Optional[str] = None

class GameStorage(AbstractRepository[Game]):
    class Meta:
        collection_name = "games"

cpu_uuid = uuid.UUID("4711e492-f922-4d20-99cf-51d4606bd314")

# Submit a turn
# This function is the abstraction of a turn into something uniform to save sanity for devs who dare to look at the main.py file.
def submit_turn(submitted_turn):
    
    # Connect to DB
    host = "localhost"
    port = 27017
    try:
        db_client = MongoClient(host, port, uuidRepresentation='standard')
        # Naughts and oughts DB
        db = db_client["naughts"]
        # Games Collection
        db_storage = GameStorage(database=db)
    except ConnectionError:
        print("DB Connection error: " + ConnectionError.message)
        
    turn_validation = validate_turn(submitted_turn, db_storage)
    if turn_validation == True:
        print("executing turn")
        executed_turn = execute_turn(submitted_turn, db_storage)
        if executed_turn == True:
            finalized_turn = finalize_turn(submitted_turn, db_storage)
            if finalized_turn == False:
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
    try:
        # Load the game from the game_id
        loaded_game_from_id = db_storage.find_one_by_id(incoming_turn.game_id)
        current_game = Game(
            player_id=loaded_game_from_id.player_id, 
            game_board=loaded_game_from_id.game_board, 
            current_turn=loaded_game_from_id.current_turn, 
            active_player=loaded_game_from_id.active_player,
            game_over=loaded_game_from_id.game_over
            )
    except:
        logging.info("Error loading the game.")
        
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
        raise HTTPException(status_code=400, detail="Game with ID: " + f"{current_game.id}" + " is not currently on the submitted turn of: " + f"{incoming_turn.turn_number}" + ". It is on turn: " + f"{current_game.current_turn}")
    
    # Is this right player taking a turn?
    if current_game.active_player != incoming_turn.player:
        logging.info("Game with ID: " + f"{current_game.id}" + " is not currently on the player's  turn. Please wait for the CPU to take a turn.")
        raise HTTPException(status_code=400, detail="Game with ID: " + f"{current_game.id}" + " is not currently on the player's  turn. Please wait for the CPU to take a turn.")        
    # Was x and y 1,2 or 3?
    if incoming_turn.col not in {1,2,3}:
        logging.info("Submitted a column value that isn't valid. Submitted: " + f"{incoming_turn.col}")
        raise HTTPException(status_code=400, detail="Submitted a column value that isn't valid. Submitted: " + f"{incoming_turn.col}")
    else:
        if incoming_turn.row not in {1,2,3}:
            logging.info("Submitted a row value that isn't valid. Submitted: " + f"{incoming_turn.row}")
            raise HTTPException(status_code=400, detail="Submitted a row value that isn't valid. Submitted: " + f"{incoming_turn.row}") 
        else:
            logging.info("Valid coordinates submitted.")
    # Was the the (x,y) coordinate Null or populated?
    # Recall this is a list of lists, so we need to fix the index offsets by removing 1
    if current_game.game_board[(incoming_turn.row-1)][incoming_turn.col-1] != "":
        logging.info("Submitted a row and column that isn't empty. Submitted: " + f"{incoming_turn.row}" + " Submitted Column: " + f"{incoming_turn.col}")
        raise HTTPException(status_code=400, detail="Submitted a row and column that isn't empty. Submitted Row: " + f"{incoming_turn.row}" + " Submitted Column: " + f"{incoming_turn.col}") 
    return True

# Attempt to execute a turn
# By the end of this function, we should have commited the turn the DB or returned an error. 
def execute_turn(validated_turn: Turn, db_storage: GameStorage):
    # Pull in the game from the turn
    
    print("Start execution: Game ID: " + f"{validated_turn.game_id}")
    try:
        # Load the game from the game_id
        loaded_game_from_id = db_storage.find_one_by_id(validated_turn.game_id)
        print("Loaded game from DB: " + f"{loaded_game_from_id.model_dump}")
        current_game = Game(
            id=validated_turn.game_id,
            player_id=loaded_game_from_id.player_id, 
            game_board=loaded_game_from_id.game_board, 
            current_turn=loaded_game_from_id.current_turn, 
            active_player=loaded_game_from_id.active_player,
            game_over=loaded_game_from_id.game_over
            )
    except:
        logging.info("Error loading the game.")

    print("Open successful: " + f"{current_game.model_dump}")
    # Update the game object
    # Save the turn into the history
    current_game.turn_history.append(validated_turn)
    logging.info("Completed append to history")
    
    # Set the mark to add to the board
    # Note: Players are always "O" and Cpus are always "X"
    if validated_turn.player == cpu_uuid:
        mark = "X"
    else:
        mark = "O"
    current_game.game_board[validated_turn.row-1][validated_turn.col-1] = mark
    logging.info("Using mark: " + f"{mark}" + " added new play to game board: " + f"{current_game.game_board}")
    
    # Increase the turn count
    current_game.current_turn = current_game.current_turn+1
    
    # Change the player to the CPU or the player
    if current_game.active_player == cpu_uuid:
        current_game.active_player = current_game.player_id
    else:
        current_game.active_player = cpu_uuid
    
    # We know for certain the game is over at turn 9. 
    if validated_turn.turn_number == 9:
        # We know the game will be over here. We don't know the winner, but we know 
        current_game.game_over = True
    # Submit the turn to the DB and update everything.
    db_storage.save(current_game)
    return True
    
# Finalize a turn to figure out if the game is over 
def finalize_turn(executed_turn: Turn, db_storage: GameStorage):
    # Finalization here means we need to:
    # Execute a CPU turn if the user just successfully made a turn
    # Return the new state to the user
    try:
        # Load the game from the game_id
        loaded_game_from_id = db_storage.find_one_by_id(executed_turn.game_id)
        current_game = Game(
            player_id=loaded_game_from_id.player_id, 
            game_board=loaded_game_from_id.game_board, 
            current_turn=loaded_game_from_id.current_turn, 
            active_player=loaded_game_from_id.active_player,
            game_over=loaded_game_from_id.game_over
            )
    except:
        logging.info("Error loading the game.")  
    
    # Win condition check first
    # Row win
    for row_number in {0,1,2}:
        if current_game.game_board[row_number][0] == current_game.game_board[row_number][1] == current_game.game_board[row_number][2]:
            if current_game.game_board[row_number][0] == "":
                logging.info("Row contains only nulls. No win.")
            else:
                # If all the contents are the same, we know someone got a row win.
                if current_game.game_board[row_number][0] == "X":
                    logging.info("CPU has a row win.")
                    current_game.game_over = True
                    current_game.game_winner = cpu_uuid
                else:
                    logging.info("Player has a row win.")
                    current_game.game_over = True
                    current_game.game_winner = current_game.player_id
    
    # Column win
    # I realize this a huge DRY violation. I'm short on time :(. Can I use a "We'll fix it in the next iteration?" here?
    for col_number in {0,1,2}:
        if current_game.game_board[0][col_number] == current_game.game_board[1][col_number] == current_game.game_board[2][col_number]:
            if current_game.game_board[0][col_number] == "":
                logging.info("Column contains only nulls. No column win.")
            else:
                # If all the contents are the same, we know someone got a row win.
                if current_game.game_board[0][col_number] == "X":
                    logging.info("CPU has a column win.")
                    current_game.game_over = True
                    current_game.game_winner = cpu_uuid
                else:
                    logging.info("Player has a column win.")
                    current_game.game_over = True
                    current_game.game_winner = current_game.player_id
    # Diagonal win
    # Yes, this is another huge DRY failure. Clear optimization could come from fixing how this being handled. (Namely, check for all three win states at once.)
    # This would be (0,0) + (1,1) + (2,2)
    # Also would be (0,2) + (1,1) + (2,0)
    if current_game.game_board[0][0] == current_game.game_board[1][1] == current_game.game_board[2][2]:
        if current_game.game_board[1][1] == "":
            logging.info("Row contains only nulls. No diagonal win.")
        else:
            # If all the contents are the same, we know someone got a row win.
            if current_game.game_board[1][1] == "X":
                logging.info("CPU has a diagonal win.")
                current_game.game_over = True
                current_game.game_winner = cpu_uuid
            else:
                logging.info("Player has a diagonal win.")
                current_game.game_over = True
                current_game.game_winner = current_game.player_id
                
    # Other diagonal win.
    if current_game.game_board[0][2] == current_game.game_board[1][1] == current_game.game_board[2][0]:
        if current_game.game_board[1][1] == "":
            logging.info("Row contains only nulls. No diagonal win.")
        else:
            # If all the contents are the same, we know someone got a row win.
            if current_game.game_board[1][1] == "X":
                logging.info("CPU has a diagonal win.")
                current_game.game_over = True
                current_game.game_winner = cpu_uuid
            else:
                logging.info("Player has a diagonal win.")
                current_game.game_over = True
                current_game.game_winner = current_game.player_id
                    
    # If we haven't gotten a win yet, carry on to the next turn setups and executions.
    if current_game.game_over == False:
        if executed_turn.player == cpu_uuid:
            logging.info("Previous turn was a CPU turn. No additional turn needed")
            last_turn_cpu = True
        else:
            logging.info("Previous turn was a player. Perform a CPU turn.")
            last_turn_cpu = False
    
    # Store the state of the game if we made changes
    try:
        db_storage.save(current_game)
    except:
        logging.error("Error saving game updates to DB")
    
    # Submit a new turn if the CPU is up
    if last_turn_cpu == False:
        # Get the current turn
        cpu_turn_number = current_game.current_turn
        
        # Generate random row/col combos until you get a null coordinate
        empty_coordinate = False
        while empty_coordinate == False:
            test_row = randint(1, 3)
            test_col = randint(1,3)
            if current_game.game_board[test_row][test_col] == "":
                empty_coordinate = True
            else:
                cpu_row = test_row
                cpu_col = test_col
        cpu_turn = Turn(turn_number=cpu_turn_number, player="cpu", row=cpu_row, col=cpu_col)
        submit_turn(cpu_turn)
    return True