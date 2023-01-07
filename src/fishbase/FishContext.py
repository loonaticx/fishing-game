from enum import IntEnum
# https://michaelcho.me/article/using-python-enums-in-sqlalchemy-models
# TODO: SEPARATE CLIENT SIDED AND SERVER SIDED FISH CONTEXTS
from fishbase.EnumBase import *


class FishInternal:
    """
    Shared with all users and is set from the first execution of /gofish upon bot init.

    Allows selective attributes of FishContext to store their values into the server
    """
    # master fish.db, shared with all users
    _db = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db):
        self._db = db


class FishContext(object):
    _db = None  # this _db variable is required. do not remove!
    disid = 0  # discord id

    # session-based values
    _CAUGHT_FISH_SESSION: int = 0  # should always be 0 in beginning of the session
    _MENU_MODE: MainMenuChoice = MainMenuChoice.NONE  # show stats or play game?
    _GAME_MODE: GameMode = GameMode.NONE  # -1 if not game
    _SESSION_MENU: SessionMenu.NONE
    _NEW_SPECIES: bool = False  # resets every cast
    _NEW_RECORD: bool = False  # resets every cast

    _IN_TUTORIAL: int = False
    _TUTORIAL_DIALOGUE_ID: int = 0
    _NEW_PLAYER: int = True

    _LEVELS_UNLOCKED: int  # [0] * len(LocationData), access is LocationData Key - 1
    _ROD_ID: FishingRod.TWIG_ROD
    _LOCATION_ID: int = Location.NONE  # currently selected location wrt LocationData

    _BUCKET_CONTENTS: list = []  # [['Sad Clown Fish', 40, 13]] -> [caughtFish, weight, fishValue]
    _BUCKET_SIZE: int = 0  # current amt of fish in your bucket
    _BUCKET_SIZE_MAX: int = 20  # how many fish can be held in your bucket at once, default is 20
    _BUCKET_FULL: bool = False

    _JELLYBEANS_TOTAL: int = 0  # "in bank"
    _JELLYBEANS_CURRENT: int = 0  # accumulated from bucket

    # Cheats / Debug entries
    _USE_FISHING_BUCKET: bool = True


    # WARNING: keys may not be sorted in numerical order
    _FISH_DATA = dict()
    """
    # includes caught species
    # intial dict is empty
    _FISH_DATA: dict = {
        FISH_GENUS_1 { 
            FISH_SPECIES_1: [
                [SMALLEST_WEIGHT: int, LARGEST_WEIGHT: int], [caughtrod1, caughtrod2, caughtrod3],
                [other personal data entries go here]
            ],
        } 
    }
    """

    def _sync_db(func):
        """
        Decorator to indicate that the SETTER method should call an update to the active database after setting.
        Use this for attributes that should always be in sync with the database.

        static method
        """
        def wrapper(cls, id):
            # execute the root method
            func(cls, id)

            # post-execution operations:
            # update database entry by inserting itself
            if FishInternal.db and hasattr(FishInternal.db, 'updateContext'):
                # maybe do the if hasattr check here and then throw an exception that u screwed up
                # val = eval(f'cls.{func.__name__}')  # func.__name__ returns eg MENU_MODE
                # user = cls.db.User
                # db.session.query(user).filter(disid).update({'context': cls}, synchronize_session = True)
                FishInternal.db.updateContext(cls.disid, cls)

        return wrapper


    @property
    def MENU_MODE(self):
        return self._MENU_MODE

    @MENU_MODE.setter
    def MENU_MODE(self, id: IntEnum):
        self._MENU_MODE = id

    @property
    def GAME_MODE(self):
        return self._GAME_MODE

    @GAME_MODE.setter
    @_sync_db
    def GAME_MODE(self, id: IntEnum):
        self._GAME_MODE = id

    @property
    def SESSION_MENU(self):
        return self._SESSION_MENU

    @SESSION_MENU.setter
    def SESSION_MENU(self, id: IntEnum):
        self._SESSION_MENU = id

    @property
    def LOCATION_ID(self):
        return self._LOCATION_ID

    @LOCATION_ID.setter
    # might turn into a db sync for campaign. we'll see
    def LOCATION_ID(self, id: IntEnum):
        self._LOCATION_ID = id

    @property
    def ROD_ID(self):
        return self._ROD_ID

    @ROD_ID.setter
    @_sync_db
    def ROD_ID(self, id: IntEnum):
        self._ROD_ID = id

    @property
    def BUCKET_SIZE_MAX(self):
        return self._BUCKET_SIZE_MAX

    @BUCKET_SIZE_MAX.setter
    @_sync_db
    def BUCKET_SIZE_MAX(self, id: IntEnum):
        self._BUCKET_SIZE_MAX = id

    @property
    def BUCKET_CONTENTS(self):
        return self._BUCKET_CONTENTS

    # sync the bucket contents to the db just in case the player leaves their session midway
    @BUCKET_CONTENTS.setter
    @_sync_db
    def BUCKET_CONTENTS(self, contents: list):
        self._BUCKET_CONTENTS = contents

    @property
    def JELLYBEANS_CURRENT(self):
        return self._JELLYBEANS_CURRENT

    # Tied to fishing bucket context
    # might wanna rename this to like JELLYBEANS_BUCKET
    @JELLYBEANS_CURRENT.setter
    @_sync_db
    def JELLYBEANS_CURRENT(self, id: IntEnum):
        self._JELLYBEANS_CURRENT = id

    @property
    def JELLYBEANS_TOTAL(self):
        return self._JELLYBEANS_TOTAL

    @JELLYBEANS_TOTAL.setter
    @_sync_db
    def JELLYBEANS_TOTAL(self, amt:int):
        self._JELLYBEANS_TOTAL = amt

    @property
    def CAUGHT_FISH_SESSION(self):
        return self._CAUGHT_FISH_SESSION

    @CAUGHT_FISH_SESSION.setter
    def CAUGHT_FISH_SESSION(self, id: int):
        self._CAUGHT_FISH_SESSION = id

    @property
    def FISH_DATA(self):
        return self._FISH_DATA

    @FISH_DATA.setter
    @_sync_db
    def FISH_DATA(self, newData):
        self._FISH_DATA = newData

    # since this is suppose to be a data class we should probably move this to different function so that its not saved
    def register_fish_record(self, genus, species, weight):
        """
        register fish & its vitals to player's fish history, avoid short-term stuff like adding to fish bucket

        FISH_DATA is only for checking if the player has ever caught such fish yet
        """
        genus_entry = self.FISH_DATA.get(genus)  # type: set
        if not genus_entry:
            # new genus, cool! let's add an entry to the db real quick
            self.FISH_DATA[genus] = dict()
        species_entry = self.FISH_DATA[genus].get(species)
        if not species_entry:
            # NEW SPECIES! Set default weights for 'em
            # small hack for min weight upon new species:
            species_entry = [[weight, 0]]
            self.NEW_SPECIES = True
        else:
            self.NEW_SPECIES = False

        # check to see if this fish's weight is a new record for either smallest or largest entry
        minWeight, maxWeight = species_entry[0]
        # check if there's a change in fish data for the weight records, indicating a new record:
        self.NEW_RECORD = (minWeight > weight) or (maxWeight < weight)

        species_entry[0][0] = min(minWeight, weight)
        species_entry[0][1] = max(maxWeight, weight)

        self.FISH_DATA[genus][species] = species_entry


    @property
    def NEW_SPECIES(self):
        return self._NEW_SPECIES

    @NEW_SPECIES.setter
    def NEW_SPECIES(self, flag):
        self._NEW_SPECIES = flag

    @property
    def NEW_RECORD(self):
        return self._NEW_RECORD

    @NEW_RECORD.setter
    def NEW_RECORD(self, flag):
        self._NEW_RECORD = flag

    @property
    def BUCKET_FULL(self):
        # sanity check to ensure bucket is actually full:
        if len(self._BUCKET_CONTENTS) >= self._BUCKET_SIZE_MAX:
            self._BUCKET_FULL = True
        else:
            self._BUCKET_FULL = False
        return self._BUCKET_FULL

    @BUCKET_FULL.setter
    @_sync_db
    def BUCKET_FULL(self, flag):
        self._BUCKET_FULL = flag

    @property
    def TUTORIAL_DIALOGUE_ID(self):
        return self._TUTORIAL_DIALOGUE_ID

    @TUTORIAL_DIALOGUE_ID.setter
    def TUTORIAL_DIALOGUE_ID(self, id: int):
        self._TUTORIAL_DIALOGUE_ID = id

    @property
    def USE_FISHING_BUCKET(self):
        return self._USE_FISHING_BUCKET

    @USE_FISHING_BUCKET.setter
    def USE_FISHING_BUCKET(self, flag: bool):
        self._USE_FISHING_BUCKET = flag

    _sync_db = staticmethod(_sync_db)


# FishContext = FishContext()
