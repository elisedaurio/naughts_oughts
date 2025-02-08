from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId, AbstractRepository
from typing import List, Optional
import uuid

class Row(BaseModel):
    col_1: Optional[str] = ""
    col_2: Optional[str] = ""
    col_3: Optional[str] = ""

# A turn consists of an iterator, the player who takes the turn, and their selection.
#
# If a user attempts an invalid action, that doesn't "count" for their turn being executed.
class Turn(BaseModel):
    # Starts at 1, iterates until win.
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

# This will be defined if I have time.
#def check_db_for_player(player_id):
#    # Check the DB to see if the player ID exists.
    