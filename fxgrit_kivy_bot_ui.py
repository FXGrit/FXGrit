from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import threading
import time

class TradingBotLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.label = Label(text="FXPilot Bot Ready", font_size=20)
        self.add_widget(self.label)
        
        self.start_btn = Button(text="Start Bot", size_hint=(1, 0.2))
        self.start_btn.bind(on_press=self.start_bot)
        self.add_widget(self.start_btn)

        self.stop_btn = Button(text="Stop Bot", size_hint=(1, 0.2))
        self.stop_btn.bind(on_press=self.stop_bot)
        self.add_widget(self.stop_btn)

        self.running = False

    def start_bot(self, instance):
        self.label.text = "📈 Bot is now scanning..."
        self.running = True
        threading.Thread(target=self.run_bot).start()

    def stop_bot(self, instance):
        self.label.text = "🛑 Bot stopped"
        self.running = False

    def run_bot(self):
        count = 0
        while self.running and count < 5:
            self.label.text = f"🔍 Scanning {count}"
            time.sleep(1)
            count += 1
        if self.running:
            self.label.text = "✅ Scan complete"

class FXPilotApp(App):
    def build(self):
        return TradingBotLayout()

FXPilotApp().run()