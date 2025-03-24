from Project.libs.Dataconnector import DataConnector


class AdminController:
    def __init__(self):
        self.dc = DataConnector()

    def get_all_players(self):
        return self.dc.players

    def get_all_regions(self):
        return list(self.dc.regions.keys())

    def get_all_provinces(self):
        provinces = set()
        for plist in self.dc.regions.values():
            provinces.update(plist)
        return sorted(list(provinces))

    def get_question_count_by_province(self, province):
        return len(self.dc.get_questions_by_province(province))

    def get_total_collected_cards(self, player):
        return len(player.collected_cards)

    def reset_player_progress(self, player):
        player.unlocked_regions = ["TayBacBo"]
        player.collected_cards = []
        self.dc.save_players()