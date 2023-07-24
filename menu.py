from google.google_sheets_api import GoogleSheetsAPI
from google.google_drive_api import GoogleDriveAPI
from utils.languages import Languages

class Menu:
    def __init__(self, google_sheets_api: GoogleSheetsAPI, google_drive_service: GoogleDriveAPI, languages: Languages):
        self.google_drive_service = google_drive_service
        self.google_sheets_api = google_sheets_api
        self.languages = languages
        self.categories = self.google_sheets_api.get_menu_categories()
        self.titles = self.google_sheets_api.get_titles()
        self.descriptions = self.google_sheets_api.get_descriptions()
        self.category_button_names = self.google_sheets_api.get_menu_category_button_names()
        self.common_data = self.google_sheets_api.get_common_data()

    def get_all_category_names(self):
        category_names = []
        for category in self.category_button_names:
            category_names.extend(category[1:])
        return category_names

    def get_all_titles(self):
        dish_title = []
        for title in self.titles:
            dish_title.extend(title[1:])
        return dish_title

    def get_category_names_by_language(self, language):
        index = self.languages.get_language_index(language)
        names = []
        for category_names in self.category_button_names:
            names.append(category_names[index])
        return names

    def get_dish_names_by_language(self, language):
        index = self.languages.get_language_index(language)
        names = []
        for dish_names in self.titles:
            names.append(dish_names[index])
        return names

    def get_selected_category_by_name(self, category_name):
        for category_names in self.category_button_names:
            if category_name in category_names:
                return category_names[0]
        return None

    def get_selected_title_by_name(self, dish_name):
        for dish_names in self.titles:
            if dish_name in dish_names:
                return dish_names[0]
        return None

    def get_keys_for_category(self, category, common_data):
        keys_for_category = []
        for row in common_data:
            if row[-1] == category:
                keys_for_category.append(row[0])
        return keys_for_category

    def get_dishes_titles_by_category_and_language(self, category_name, language):
        category = self.get_selected_category_by_name(category_name)
        keys = self.get_keys_for_category(category, self.common_data)
        data = self.get_titles_by_keys_and_language(keys, language)
        dishes_data = []
        if data:
            for item in data:
                message_text = f'{item["title"]}'
                dish_data = {
                    'text': message_text
                }
                dishes_data.append(dish_data)
        return dishes_data

    def get_title_by_key_and_language(self, key, language):
        index = self.languages.get_language_index(language)
        for title_tuple in self.titles:
            if title_tuple[0] == key:
                title = title_tuple[index]
                return title

    def get_description_by_key_and_language(self, key, language):
        index = self.languages.get_language_index(language)
        for description_tuple in self.descriptions:
            if description_tuple[0] == key:
                description = description_tuple[index]
                return description
        return None

    def get_price_and_image_id_by_key(self, key):
        for row in self.common_data:
            if row[0] == key:
                price = row[1]
                image_id = row[2]
                return price, image_id
        return None, None

    def get_data_by_key_and_language(self, key, language):
        result_data = []
        title = self.get_title_by_key_and_language(key, language)
        description = self.get_description_by_key_and_language(key, language)
        price, image_id = self.get_price_and_image_id_by_key(key)

        if title and description and price:
            data = {
                'key': key,
                'title': title,
                'description': description,
                'price': price,
                'image_id': image_id
            }
            result_data.append(data)

        return result_data

    def get_titles_by_keys_and_language(self, keys, language):
        result_data = []
        for key in keys:
            title = self.get_title_by_key_and_language(key, language)
            if title:
                data = { 'title': title }
                result_data.append(data)
        return result_data

    def get_dish_data_by_title_and_language(self, dish_name, language):
        title = self.get_selected_title_by_name(dish_name)
        key = self.get_key_for_title(title)
        data = self.get_data_by_key_and_language(key, language)
        if data:
            for item in data:
                message_text = f'<b>{item["title"]}</b>\n'
                message_text += f'{item["description"]}\n'
                message_text += f'<b>{item["price"]}</b>\n'
                image_id = item["image_id"]
                if image_id != '' and image_id != None:
                    image_file = self.google_drive_service.get_file_by_id(image_id)
                    dish_data = {
                        'text': message_text,
                        'image': image_file
                    }
                    data = dish_data
                else:
                    dish_data = {
                        'text': message_text,
                        'image': None
                    }
                    data = dish_data
        return data

    def get_key_for_title(self, title):
        key_for_title = None
        for row in self.common_data:
            if row[0] == title:
                key_for_title = row[0]

        return key_for_title