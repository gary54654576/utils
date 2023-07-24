from google.google_sheets_api import GoogleSheetsAPI
from utils.languages import Languages

class ActionButtons:
    def __init__(self, google_sheets_api: GoogleSheetsAPI, languages: Languages):
        self.google_sheets_api = google_sheets_api
        self.languages = languages
        self.button_names_by_actions = self.google_sheets_api.get_button_names_by_action()

    def get_all_actions(self):
        actions = []
        for button_names_by_action in self.button_names_by_actions:
            actions.extend(button_names_by_action[1:])
        return actions

    def get_button_names_by_action(self, action):
        for button_names_by_action in self.button_names_by_actions:
            if button_names_by_action[0] == action:
                return button_names_by_action[1:]
        return []

    def get_button_names_by_language(self, language):
        index = self.languages.get_language_index(language)
        button_names = []
        for button_names_by_action in self.button_names_by_actions:
            button_names.append(button_names_by_action[index])
        return button_names

    def get_selected_action_by_button_name(self, button_name):
        for button_names_by_action in self.button_names_by_actions:
            if button_name in button_names_by_action:
                return button_names_by_action[0]
        return None

    def get_button_name_by_action_and_language(self, action, language):
        index = self.languages.get_language_index(language)
        for button_names_by_action in self.button_names_by_actions:
            if button_names_by_action[0] == action:
                return button_names_by_action[index]
        return None
