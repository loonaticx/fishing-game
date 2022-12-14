class FishContext:
    MENU_MODE: int  # show stats or play game?
    GAME_MODE: int  # -1 if not game
    LEVELS_UNLOCKED: int  # [0] * len(LocationData), access is LocationData Key - 1
    ROD_ID: int
    LOCATION_ID: int  # currently selected location wrt LocationData
    BUCKET_SIZE: int  # current amt of fish in your bucket
    BUCKET_SIZE_MAX: int  # how many fish can be held in your bucket at once
    JELLYBEANS_TOTAL: int  # "in bank"
    JELLYBEANS_CURRENT: int  # accumulated from bucket
