import uuid
from dataclasses_json import dataclass_json
INVALID_ID = f"{uuid.UUID(int=0)}"

from typing import List
import dataclasses

@dataclass_json
@dataclasses.dataclass
class AliasTarget:
    language : str = "chs"
    alias_id : str = INVALID_ID
    alias : str = ""
    name : str = ""
    target_id : str = INVALID_ID
    country : str = ""
    location : List = dataclasses.field(default_factory=lambda : [0., 0.]) # [0., 0.] # latitude, longtitude
    target_type : str = ""
    