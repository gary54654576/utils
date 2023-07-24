from google.google_sheets_api import GoogleSheetsAPI

class Languages:
    def __init__(self, google_sheets_api: GoogleSheetsAPI):
        self.languages = google_sheets_api.get_languages()

    def get_all_languages(self):
        return self.languages

    def get_language_indexes(self):
        language_indexes = {}
        for i, language in enumerate(self.languages, start=1):
            language_indexes[language] = i
        return language_indexes

    def get_language_index(self, language):
        language_indexes = self.get_language_indexes()
        if language not in language_indexes:
            return None
        return language_indexes[language]
