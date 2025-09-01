from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class FXGritApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text='📈 Welcome to FXGrit Bot')
        layout.add_widget(self.label)

        self.input = TextInput(hint_text='Enter your Name', multiline=False)
        layout.add_widget(self.input)

        self.button = Button(text='Start Bot')
        self.button.bind(on_press=self.start_bot)
        layout.add_widget(self.button)

        return layout

    def start_bot(self, instance):
        name = self.input.text
        self.label.text = f'🚀 Hello {name}! FXGrit Bot Started ✅'


if __name__ == '__main__':
    FXGritApp().run()