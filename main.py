from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (500, 800)

class HomeScreen(MDScreen):
    pass

class GeneratorScreen(MDScreen):
    pass

class ImporterScreen(MDScreen):
    pass

class StudyProApp(MDApp):
    def build(self):
        self.title = "StudyPro"
        Builder.load_file("screens/home.kv")
        Builder.load_file("screens/generator.kv")
        Builder.load_file("screens/importer.kv")
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    StudyProApp().run()
