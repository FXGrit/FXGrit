from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

class FXGritBot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.status = Label(text='📈 Bot is now scanning market', font_size=20)
        self.add_widget(self.status)
        self.counter = 0
        Clock.schedule_interval(self.scan_market, 1)

    def scan_market(self, dt):
        if self.counter < 5:
            self.status.text += f"\n🔍 Scanning {self.counter}"
            self.counter += 1
        else:
            self.status.text += "\n✅ Scan complete"
            Clock.unschedule(self.scan_market)

class FXGritApp(App):
    def build(self):
        return FXGritBot()

FXGritApp().run()