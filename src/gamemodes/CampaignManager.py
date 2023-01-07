from gamemodes.Campaign import Campaign


class CampaignManager:
    def __init__(self):
        self.isActive = True
        pass

    def requestCampaign(self):
        # todo:
        # check if instance is new
        # pass wantTutorial flag if needed
        return Campaign()
