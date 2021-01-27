class CommonOptions:
    def __init__(self):
        self.oom_message_viewed = 0
        self.selected_model = 'st'


class LiveOptions:
    def __init__(self):
        self.oom_message_viewed = dict()
        self.selected_model = dict()

    def __get_value_by_id(self, client_id, dictionary):
        if client_id in dictionary:
            return dictionary[client_id]
        else:
            return None

    def set_oom_message_viewed(self, client_id, time):
        self.oom_message_viewed[client_id] = time

    def set_selected_model(self, client_id, model):
        self.selected_model[client_id] = model

    def get_oom_message_viewed(self, client_id):
        return self.__get_value_by_id(client_id, self.oom_message_viewed)

    def get_selected_model(self, client_id):
        return self.__get_value_by_id(client_id, self.selected_model)


__LIVE_OPTIONS__ = LiveOptions()
