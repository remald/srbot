
class LiveOptions:
    def __init__(self):
        self.memory_storage = dict()

    def __get_client_dict_by_id(self, client_id):
        if client_id not in self.memory_storage:
            self.memory_storage[client_id] = dict()
        return self.memory_storage[client_id]

    def __get_param_by_id(self, client_id, param):
        client_dict = self.__get_client_dict_by_id(client_id)
        if param not in client_dict:
            client_dict[param] = None
        return client_dict[param]

    def set_oom_message_viewed(self, client_id, time):
        self.__get_client_dict_by_id(client_id)['oom_time'] = time

    def set_selected_model(self, client_id, model):
        self.__get_client_dict_by_id(client_id)['model'] = model

    def set_lang(self, client_id, lang):
        self.__get_client_dict_by_id(client_id)['messages'] = lang

    def get_oom_message_viewed(self, client_id):
        return self.__get_param_by_id(client_id, 'oom_time')

    def get_selected_model(self, client_id):
        return self.__get_param_by_id(client_id, 'model')

    def get_lang(self, client_id):
        lang = self.__get_param_by_id(client_id, 'messages')
        return lang if lang is not None else 'en'


__LIVE_OPTIONS__ = LiveOptions()
