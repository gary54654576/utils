from google.google_sheets_api import GoogleSheetsAPI
from utils.languages import Languages

class Messages:
    def __init__(self, google_sheets_api: GoogleSheetsAPI, languages: Languages):
        self.messages = google_sheets_api.get_messages()
        self.languages = languages

    def get_message_by_key_and_language(self, key, language):
        for message_tuple in self.messages:
            if message_tuple[0] == key:
                language_index = self.languages.get_language_index(language)
                message = message_tuple[language_index]
                return message
        return None