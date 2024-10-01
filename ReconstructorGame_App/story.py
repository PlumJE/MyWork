from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from folder_paths import GUI_folder


Builder.load_file(GUI_folder + '/story_GUI.kv')

class StoryScreen(Screen):
    def prev(self, *args, **kwargs):
        pass
    def next(self, *args, **kwargs):
        pass
    def move_to_game(self, *args, **kwargs):
        self.manager.current = 'Game'
storyscreen = StoryScreen(name='Story')