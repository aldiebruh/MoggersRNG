from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import json
import random
import math
import os

SAVE_FILE = "save/moggers_rng_save.json"

titles = {
        "Stinky Mogger": ("1/2", 1 / 2),
    "Mouthbreather": ("1/4", 1 / 4),
    "Washed": ("1/6", 1 / 6),
    "Chopped": ("1/8", 1 / 8),
    "NPC": ("1/12", 1 / 12),
    "Gooner": ("1/15", 1 / 15),
    "Edger": ("1/20", 1 / 20),
    "Beginner Mogger": ("1/25", 1 / 25),
    "Locking In": ("1/50", 1 / 50),
    "Jynxzi": ("1/69", 1 / 69),
    "Locked In": ("1/100", 1 / 100),
    "Mogger": ("1/150", 1 / 150),
    "Beastsaya": ("1/250", 1 / 250),
    "xQc": ("1/420", 1 / 420),
    "NYC Mogger": ("1/500", 1 / 500),
    "Minecraft Steve": ("1/500", 1/500),
    "Ken Kaneki": ("1/1000-7", 1 / 993),
    "Rizz KING": ("1/1000", 1 / 1000),
    "Hev Abi": ("1/1103", 1 / 1103),
    "Kendrick Lamar": ("1/1499", 1 / 1499),
    "Drake": ("1/1500", 1 / 1500),
    "Xi Jinping": ("1/1988", 1 / 1988),
    "Xi Jinping": ("1/1989", 1 / 1989),
    "Gurt": ("1/2000", 1 / 2000),
    "Rodrigo Roa Duterte": ("1/2016-2022", 1 / 2016),
    "Young Thug": ("1/2500", 1 / 2500),
    "NBA Youngboy": ("1/3000", 1 / 3000),
    "Baby Gronk": ("1/5000", 1 / 5000),
    "Real Sigma": ("1/7500", 1 / 7500),
    "Red from Angry Birds": ("1/10000", 1 / 10000),
    "Doanel Dantes": ("1/12500", 1 / 12500),
    "Omni Man": ("1/15000", 1 / 15000),
    "K Shami": ("1/20000", 1 / 20000),
    "Prime Tom Cruise": ("1/25000", 1 / 25000),
    "Alden Richards": ("1/33333", 1 / 33333),
    "Chico Lachowski": ("1/45000", 1 / 45000),
    "Vessel of Dreamybull": ("1/47500", 1 / 47500),
    "Aldie Christian Gomez": ("Secret", 1 / 1000000),
    "Prison Pump": ("1/55000", 1 / 55000),
    "Kumalala": ("1/69000", 1 / 60000),
    "Savesta": ("1/69000", 1 / 69000),
    "Edging Beast": ("1/100000", 1 / 100000),
    "Dreamybull PLUS ULTRA": ("1/200000", 1 / 200000),
    "Daddy Tyga": ("1/500000", 1 / 500000),
    "Fuego Fredrinn Build": ("1/750000", 1 / 750000),
    "Samuel Ernest Obregon Music Video": ("1/1000000", 1 / 1000000),
    "minarate": ("1/2000000", 1 / 2000000),
    "Malupiton": ("1/2500000", 1 / 2500000),
    "Flight Reacts": ("1/3000000", 1 / 3000000),
    "LEBRON RAYMONE JAMES": ("1/5000000", 1 / 5000000),
    "F Student": ("1/7500000", 1 / 7500000),
    "aldie pro max": ("1/1000000", 1 / 1000000),
    "Yo": ("1/2000000", 1 / 2000000),
    "Goat of Mogging": ("GOAT/???", 1 / 200000000),
}

def get_random_title(luck_multiplier=1.0):
    adjusted = {
        title: (display, base_prob, base_prob ** (1 / math.sqrt(luck_multiplier)))
        for title, (display, base_prob) in titles.items()
    }
    total = sum(adjusted_prob for _, _, adjusted_prob in adjusted.values())
    rand = random.uniform(0, total)
    cum = 0
    for title, (display, base_prob, adjusted_prob) in adjusted.items():
        cum += adjusted_prob
        if rand <= cum:
            return title, display, base_prob, adjusted_prob
    # fallback
    title, (display, base_prob, adjusted_prob) = list(adjusted.items())[-1]
    return title, display, base_prob, adjusted_prob


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        layout.add_widget(Label(text="Welcome to Mogger's RNG", font_size=32))
        start_btn = Button(text="Start Spinning", size_hint=(1, 0.2))
        start_btn.bind(on_press=self.go_to_spin)
        layout.add_widget(start_btn)

        save_btn = Button(text="Save", size_hint=(1, 0.2))
        save_btn.bind(on_press=lambda x: self.save_data())
        layout.add_widget(save_btn)

        load_btn = Button(text="Load", size_hint=(1, 0.2))
        load_btn.bind(on_press=lambda x: self.load_data())
        layout.add_widget(load_btn)

        exit_btn = Button(text="Exit", size_hint=(1, 0.2))
        exit_btn.bind(on_press=App.get_running_app().stop)
        layout.add_widget(exit_btn)
        self.add_widget(layout)

        self.spin_sound = SoundLoader.load("audio/common_sound.wav")
        self.rare_sound = SoundLoader.load("audio/rare_sound.wav")
        self.upgrade_sound = SoundLoader.load("audio/upgrade_sound.wav")

        self.bg_music = SoundLoader.load("audio/background.wav")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5  # Adjust volume as desired
            self.bg_music.play()

    def go_to_spin(self, instance):
        self.manager.current = "spin"

    def save_data(self):
        app = App.get_running_app()
        data = {
            "spin_count": app.spin_screen.spin_count,
            "currency": app.spin_screen.currency,
            "luck_multiplier": app.spin_screen.luck_multiplier,
            "cooldown_time": app.spin_screen.cooldown_time
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        self.show_message("Data saved!")

    def load_data(self):
        app = App.get_running_app()
        if not os.path.exists(SAVE_FILE):
            self.show_message("No save file found.")
            return
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        app.spin_screen.spin_count = data.get("spin_count", 0)
        app.spin_screen.currency = data.get("currency", 0)
        app.spin_screen.luck_multiplier = data.get("luck_multiplier", 1.0)
        app.spin_screen.cooldown_time = data.get("cooldown_time", 2.0)
        app.spin_screen.update_ui()
        self.show_message("Data loaded!")

    def show_message(self, message):
        Popup(title="Info", content=Label(text=message), size_hint=(None, None), size=(300, 150)).open()

class SpinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.luck_multiplier = 1.0
        self.spin_count = 0
        self.currency = 0
        self.cooldown_time = 2.0
        self.cooldown_min = 0.5
        self.cooldown = False

        self.cooldown_upgrade_cost = 25
        self.luck_upgrade_cost = 50

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.title_label = Label(text="You Got:", font_size=28)
        self.result_label = Label(text="", font_size=24)
        self.cooldown_label = Label(text="", font_size=18)
        self.status_label = Label(text="", font_size=20)

        self.spin_button = Button(text="Spin", size_hint=(1, 0.2))
        self.spin_button.bind(on_press=self.spin)

        self.cooldown_upgrade_btn = Button(size_hint=(1, 0.15))
        self.cooldown_upgrade_btn.bind(on_press=self.upgrade_cooldown)

        self.luck_upgrade_btn = Button(size_hint=(1, 0.15))
        self.luck_upgrade_btn.bind(on_press=self.upgrade_luck)

        back_btn = Button(text="Back to Menu", size_hint=(1, 0.15))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))

        self.spin_sound = SoundLoader.load("audio/common_sound.wav")
        self.rare_sound = SoundLoader.load("audio/rare_sound.wav")
        self.upgrade_sound = SoundLoader.load("audio/upgrade_sound.wav")
        self.bg_music = SoundLoader.load("audio/background.wav")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5  # Adjust volume as desired
            self.bg_music.play()

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.cooldown_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.spin_button)
        self.layout.add_widget(self.cooldown_upgrade_btn)
        self.layout.add_widget(self.luck_upgrade_btn)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)
        self.update_ui()

    def spin(self, instance):
        if self.cooldown:
            return
        self.cooldown = True
        self.spin_count += 1
        title, display, base_prob, adjusted_prob = get_random_title(self.luck_multiplier)
        self.result_label.text = f"{title} ({display})"

        if base_prob <= 1 / 1000 and self.rare_sound:
            self.rare_sound.play()
        elif self.spin_sound:
            self.spin_sound.play()

        self.currency += 2 + (self.spin_count // 100)
        self.update_ui()
        self.cooldown_label.text = f"Cooldown: {self.cooldown_time:.1f}s"
        Clock.schedule_once(self.reset_cooldown, self.cooldown_time)

    def reset_cooldown(self, dt):
        self.cooldown = False
        self.cooldown_label.text = ""

    def update_ui(self):
        self.status_label.text = f"Spins: {self.spin_count} | MB: {self.currency} | Luck: {self.luck_multiplier:.2f}x | CD: {self.cooldown_time:.2f}s"
        self.cooldown_upgrade_btn.text = f"Upgrade Cooldown (-0.1s)\\nCost: {self.cooldown_upgrade_cost} MB"
        self.luck_upgrade_btn.text = f"Upgrade Luck (+0.25x)\\nCost: {self.luck_upgrade_cost} MB"

    def show_message(self, msg):
        Popup(title="Upgrade", content=Label(text=msg), size_hint=(None, None), size=(300, 150)).open()

    def upgrade_cooldown(self, instance):
        if self.cooldown_time <= self.cooldown_min:
            self.show_message("Cooldown already at minimum!")
        elif self.currency >= self.cooldown_upgrade_cost:
            self.currency -= self.cooldown_upgrade_cost
            self.cooldown_time = max(self.cooldown_time - 0.1, self.cooldown_min)
            self.show_message(f"Cooldown reduced to {self.cooldown_time:.2f}s")
            self.upgrade_sound.play()
            self.update_ui()
        else:
            self.show_message("Not enough Mog Bucks!")

    def upgrade_luck(self, instance):
        if self.currency >= self.luck_upgrade_cost:
            self.currency -= self.luck_upgrade_cost
            self.luck_multiplier += 0.25
            self.show_message(f"Luck increased to {self.luck_multiplier:.2f}x")
            self.upgrade_sound.play()
            self.update_ui()
        else:
            self.show_message("Not enough Mog Bucks!")

class MoggersApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainMenu(name="main"))
        self.spin_screen = SpinScreen(name="spin")
        sm.add_widget(self.spin_screen)
        return sm

if __name__ == "__main__":
    MoggersApp().run()
