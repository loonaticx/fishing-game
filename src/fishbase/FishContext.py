from enum import IntEnum
# https://michaelcho.me/article/using-python-enums-in-sqlalchemy-models
# TODO: SEPARATE CLIENT SIDED AND SERVER SIDED FISH CONTEXTS


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
    # _db = None
    disid = 0

    _CAUGHT_FISH_SESSION: int = 0  # should always be 0 in beginning of the session
    _IN_TUTORIAL: int = False
    _TUTORIAL_DIALOGUE_ID: int = 0
    _NEW_PLAYER: int = True

    _MENU_MODE: IntEnum  # show stats or play game?
    _GAME_MODE: IntEnum  # -1 if not game
    _LEVELS_UNLOCKED: int  # [0] * len(LocationData), access is LocationData Key - 1
    _ROD_ID: int
    _LOCATION_ID: int  # currently selected location wrt LocationData
    _BUCKET_CONTENTS: list
    _BUCKET_SIZE: int  # current amt of fish in your bucket
    _BUCKET_SIZE_MAX: int  # how many fish can be held in your bucket at once
    _JELLYBEANS_TOTAL: int  # "in bank"
    _JELLYBEANS_CURRENT: int  # accumulated from bucket
    """
    # includes caught species
    # intial dict is empty
    _FISH_DATA: dict = {
        FISH_SPECIES1 { 
            FISH_GENUS1: [
                [MIN_WEIGHT: int, MAX_WEIGHT: int], [caughtrod1, caughtrod2, caughtrod3],
                [other personal data entries go here]
            ],
        } 
    }
    """

    def _sync_db(func):
        """
        static method
        """
        def wrapper(cls, id):
            # execute the root method
            func(cls, id)

            # post-execution operations:
            # update database entry by inserting itself
            if FishInternal.db:
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
    def LOCATION_ID(self):
        return self._LOCATION_ID

    @LOCATION_ID.setter
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
    def JELLYBEANS_CURRENT(self):
        return self._JELLYBEANS_CURRENT

    @MENU_MODE.setter
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
    def TUTORIAL_DIALOGUE_ID(self):
        return self._TUTORIAL_DIALOGUE_ID

    @TUTORIAL_DIALOGUE_ID.setter
    def TUTORIAL_DIALOGUE_ID(self, id: int):
        self._TUTORIAL_DIALOGUE_ID = id

    _sync_db = staticmethod(_sync_db)


# FishContext = FishContext()
