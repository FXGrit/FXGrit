from kivy.app import App
from kivy.uix.label import Label

class FXGritApp(App):
    def build(self):
        return Label(text="✅ FXGrit Bot is Running", font_size=30)

FXGritApp().run()