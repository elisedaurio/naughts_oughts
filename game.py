from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId, AbstractRepository
from typing import List, Optional
import uuid

class Row(BaseModel):
    col_1: Optional[str] = ""
    col_2: Optional[str] = ""
    col_3: Optional[str] = ""

class Game(BaseModel):
    id: Optional[PydanticObjectId] = None
    player_id: uuid.UUID
    game_board: List[Row]
    current_turn: int

class GameStorage(AbstractRepository[Game]):
    class Meta:
        collection_name = "games"

def check_db_for_player(player_id):
    # Check the DB to see if the player ID exists.
    