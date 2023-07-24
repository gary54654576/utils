from google.google_sheets_api import GoogleSheetsAPI

class UserData:
    def __init__(self, google_sheets_api: GoogleSheetsAPI):
        self.google_sheets_api = google_sheets_api
        self.user_data = {}  # Dictionary to store user data in memory
        self._load_data()

    def __del__(self):
        print("UserData: __del__")

    def _load_data(self):
        self.data = self.google_sheets_api.get_user_data()
        for data_tuple in self.data:
            user_id = data_tuple[0]
            self.user_data[user_id] = list(data_tuple) + [None] * (5 - len(data_tuple))

    def get_user_by_id(self, id):
        return self.user_data.get(id, [None] * 5)

    def set_id(self, id):
        if id not in self.user_data:
            self.user_data[id] = [id, None, None, None, None]
            self.update_user_data(self.user_data[id])
        self.save_all_data()

    def set_selected_language(self, id, selected_language):
        user_info = self.get_user_by_id(id)
        user_info[1] = selected_language
        self.update_user_data(user_info)

    def set_selected_action(self, id, selected_action):
        user_info = self.get_user_by_id(id)
        user_info[2] = selected_action
        self.update_user_data(user_info)

    def set_selected_category(self, id, selected_category):
        user_info = self.get_user_by_id(id)
        user_info[3] = selected_category
        self.update_user_data(user_info)

    def set_current_state(self, id, current_state):
        user_info = self.get_user_by_id(id)
        user_info[4] = current_state
        self.update_user_data(user_info)

    def get_selected_language(self, id):
        user_info = self.get_user_by_id(id)
        return user_info[1]

    def get_selected_action(self, id):
        user_info = self.get_user_by_id(id)
        return user_info[2]

    def get_selected_category(self, id):
        user_info = self.get_user_by_id(id)
        return user_info[3]

    def get_current_state(self, id):
        user_info = self.get_user_by_id(id)
        return user_info[4]

    def update_user_data(self, user_info):
        user_id = user_info[0]
        self.user_data[user_id] = user_info

    def get_user_row_by_id(self, id):
        return self.google_sheets_api.get_user_row_by_id(id)

    def save_all_data(self):
        for user_id, user_info in self.user_data.items():
            self.google_sheets_api.update_user_data(user_info)
