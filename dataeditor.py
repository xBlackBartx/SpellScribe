from pathlib import Path
import pickle

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget

from baseclasses import SpellListData, PurchaseListData


def exit_app():
    MainEditorApp.get_running_app().stop()


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        outer_layout = BoxLayout()
        main_layout = BoxLayout(orientation='vertical')
        outer_layout.add_widget(Widget())
        outer_layout.add_widget(main_layout)
        outer_layout.add_widget(Widget())
        main_layout.add_widget(Widget())
        main_layout.add_widget(Button(
            text='Edit Spell Definitions',
            on_press=lambda _: self.change_screen('data editor')
        ))
        main_layout.add_widget(Button(
            text='Edit Class Lists',
            on_press=lambda _: self.change_screen('list editor')
        ))
        main_layout.add_widget(Button(
            text='Exit',
            on_press=lambda _: exit_app()
        ))
        main_layout.add_widget(Widget())
        self.add_widget(outer_layout)

    def change_screen(self, screen):
        self.manager.current = screen


class DataEditorScreen(Screen):
    def __init__(self, **kwargs):
        super(DataEditorScreen, self).__init__(**kwargs)
        self.spell_data = None
        self.purchase_data = None
        self.load_data()

    def load_data(self):
        data_file = Path('./data.spells')
        if data_file.exists():
            with open(data_file, 'rb') as file:
                self.spell_data, self.purchase_data = pickle.load(file)
        else:
            self.spell_data, self.purchase_data = {}, {}

    def save_data(self):
        data_file = Path('./data.spells')
        with open(data_file, 'wb') as file:
            pickle.dump((self.spell_data, self.purchase_data), file)


class ListEditorScreen(Screen):
    def __init__(self, **kwargs):
        super(ListEditorScreen, self).__init__(**kwargs)


class MainEditorApp(App):
    def build(self):
        screen_manager = ScreenManager()
        menu_screen = MenuScreen(name='menu screen')
        data_editor = DataEditorScreen(name='data editor')
        list_editor = ListEditorScreen(name='list editor')
        screen_manager.add_widget(menu_screen)
        screen_manager.add_widget(data_editor)
        screen_manager.add_widget(list_editor)
        # screen_manager.current = 'menu screen'
        return screen_manager


if __name__ == '__main__':
    MainEditorApp().run()
