from enum import IntEnum
# https://michaelcho.me/article/using-python-enums-in-sqlalchemy-models


class FishContext(object):
    # master fish.db
    db = None
    disid = 0

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
            if cls.db:
                # val = eval(f'cls.{func.__name__}')  # func.__name__ returns eg MENU_MODE
                # user = cls.db.User
                # db.session.query(user).filter(disid).update({'context': cls}, synchronize_session = True)
                cls.db.updateContext(cls.disid, cls)

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

    @MENU_MODE.setter
    def GAME_MODE(self, id: IntEnum):
        self._GAME_MODE = id

    @property
    def LOCATION_ID(self):
        return self._LOCATION_ID

    @MENU_MODE.setter
    def LOCATION_ID(self, id: IntEnum):
        self._LOCATION_ID = id

    @property
    def ROD_ID(self):
        return self._ROD_ID

    @MENU_MODE.setter
    def ROD_ID(self, id: IntEnum):
        self._ROD_ID = id

    @property
    def BUCKET_SIZE_MAX(self):
        return self.BUCKET_SIZE_MAX

    @MENU_MODE.setter
    def BUCKET_SIZE_MAX(self, id: IntEnum):
        self.BUCKET_SIZE_MAX = id

    _sync_db = staticmethod(_sync_db)


# FishContext = FishContext()
