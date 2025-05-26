from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
import json
import random
import math
import os


SAVE_FILE = "save/moggers_rng_save.json"

LIGHT_THEME = {
    "bg_color": [1, 1, 1, 1],
    "text_color": [1, 1, 1, 1],
    "button_color": [0.8, 0.8, 0.8, 0.8]
}

DARK_THEME = {
    "bg_color": [0.1, 0.1, 0.1, 1],
    "text_color": [1, 1, 1, 1],
    "button_color": [0.3, 0.3, 0.3, 1]
}

titles = {
    "Stinky Mogger": ("1/2", 1 / 2),
    "Chopped Chin": ("1/3", 1 / 3),
    "Indian": ("1/4", 1 / 4),
    "Mouthbreather": ("1/4", 1 / 4),
    "Washed": ("1/6", 1 / 6),
    "Fatty": ("1/7", 1 / 7),
    "Chopped": ("1/8", 1 / 8),
    "NPC": ("1/12", 1 / 12),
    "Gooner": ("1/15", 1 / 15),
    "Caseoh": ("1/17", 1 / 17),
    "Edger": ("1/20", 1 / 20),
    "Beginner Mogger": ("1/25", 1 / 25),
    "Locking In": ("1/50", 1 / 50),
    "Jynxzi": ("1/69", 1 / 69),
    "Locked In": ("1/100", 1 / 100),
    "Mogger": ("1/150", 1 / 150),
    "Beastsaya": ("1/250", 1 / 250),
    "xQc": ("1/420", 1 / 420),
    "NYC Mogger": ("1/500", 1 / 500),
    "Minecraft Steve": ("1/500", 1 / 500),
    "Ken Kaneki": ("1/1000-7", 1 / 993),
    "Jordan Barrett": ("1/999", 1 / 999),
    "Rizz KING": ("1/1,000", 1 / 1000),
    "Hev Abi": ("1/1,103", 1 / 1103),
    "Kendrick Lamar": ("1/1,499", 1 / 1499),
    "Drake": ("1/1,500", 1 / 1500),
    "Xi Jinping": ("1/1988", 1 / 1988),
    "Xi Jinping": ("1/1989", 1 / 1989),
    "Gurt": ("1/2,000", 1 / 2000),
    "Rodrigo Roa Duterte": ("1/2016-2022", 1 / 2016),
    "Young Thug": ("1/2,500", 1 / 2500),
    "NBA Youngboy": ("1/3,000", 1 / 3000),
    "Baby Gronk": ("1/5,000", 1 / 5000),
    "Real Sigma": ("1/7,500", 1 / 7500),
    "Red from Angry Birds": ("1/10,000", 1 / 10000),
    "Doanel Dantes": ("1/12,500", 1 / 12500),
    "Omni Man": ("1/15,000", 1 / 15000),
    "K Shami": ("1/20,000", 1 / 20000),
    "Prime Tom Cruise": ("1/25,000", 1 / 25000),
    "Alden Richards": ("1/33,333", 1 / 33333),
    "Robin Padilla": ("1/40,000", 1 / 40000),
    "Chico Lachowski": ("1/45,000", 1 / 45000),
    "Vessel of Dreamybull": ("1/47,500", 1 / 47500),
    "Aldie Christian Gomez": ("Secret", 1 / 1000000),
    "Prison Pump": ("1/55,000", 1 / 55000),
    "Kumalala": ("1/69,000", 1 / 60000),
    "Savesta": ("1/69,000", 1 / 69000),
    "James Sapphire": ("1/80,000", 1 / 80000),
    "Edging Beast": ("1/100,000", 1 / 100000),
    "Dreamybull PLUS ULTRA": ("1/200,000", 1 / 200000),
    "Daddy Tyga": ("1/500,000", 1 / 500000),
    "Fuego Fredrinn Build": ("1/750,000", 1 / 750000),
    "Samuel Ernest Obregon Music Video": ("1/1,000,000", 1 / 1000000),
    "minarate": ("1/2,000,000", 1 / 2000000),
    "Malupiton": ("1/2,500,000", 1 / 2500000),
    "Flight Reacts": ("1/3,000,000", 1 / 3000000),
    "LEBRON RAYMONE JAMES": ("1/5,000,000", 1 / 5000000),
    "F Student": ("1/7,500,000", 1 / 7500000),
    "aldie pro max": ("1/1,000,000,000", 1 / 1000000000),
    "Yo": ("1/2,000,000", 1 / 2000000),
    "Skylar White Yo": ("1/3,000,000", 1 / 3000000),
    "Prime Cookie King": ("1/4,500,000", 1 / 4500000),
    "YES KING": ("1/50,000,000", 1 / 50000000),
    "Masked Hokage": ("750,000,000", 1 / 750000000),
    "NLE Choppa": ("1/1,000,000,000", 1 / 1000000000),
    "Goat of Mogging": ("GOAT/???", 1 / 20000000000),
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
    return list(adjusted.items())[-1]

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme = DARK_THEME

        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        self.layout = layout

        self.title_label = Label(
            text="Mogger's RNG",
            font_size=60,
            font_name="Bahnschrift",
        )
        layout.add_widget(self.title_label)

        self.subtitle_label = Label(
            text="made by aldiebruh",
            font_size=16,
            font_name="Bahnschrift",
            halign="left",
            valign="top",
            size_hint=(1, None),
            height=20
        )
        self.subtitle_label.bind(size=self.subtitle_label.setter('text_size'))
        layout.add_widget(self.subtitle_label)

        start_btn = Button(
            text="Start Spinning",
            size_hint=(1, 0.2),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=self.theme["button_color"],
            color=self.theme["text_color"]
        )
        start_btn.bind(on_press=self.go_to_spin)
        layout.add_widget(start_btn)

        save_btn = Button(
            text="Save File",
            size_hint=(1, 0.2),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=self.theme["button_color"],
            color=self.theme["text_color"]
        )
        save_btn.bind(on_press=lambda x: self.save_data())
        layout.add_widget(save_btn)

        load_btn = Button(
            text="Load File",
            size_hint=(1, 0.2),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=self.theme["button_color"],
            color=self.theme["text_color"]
        )
        load_btn.bind(on_press=lambda x: self.load_data())
        layout.add_widget(load_btn)

        self.theme_btn = Button(
            text="Switch to Light Mode",
            size_hint=(1, 0.2),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=self.theme["button_color"],
            color=self.theme["text_color"]
        )
        self.theme_btn.bind(on_press=self.toggle_theme)
        layout.add_widget(self.theme_btn)

        exit_btn = Button(
            text="Exit",
            size_hint=(1, 0.2),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=self.theme["button_color"],
            color=self.theme["text_color"]
        )
        exit_btn.bind(on_press=App.get_running_app().stop)
        layout.add_widget(exit_btn)


        self.add_widget(layout)
        Clock.schedule_once(lambda dt: self.apply_theme())

        self.spin_sound = SoundLoader.load("audio/common_sound.wav")
        self.rare_sound = SoundLoader.load("audio/rare_sound.wav")
        self.upgrade_sound = SoundLoader.load("audio/upgrade_sound.wav")
        self.bg_music = SoundLoader.load("audio/background.wav")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5
            self.bg_music.play()

    def toggle_theme(self, instance):
        app = App.get_running_app()
        if app.current_theme == LIGHT_THEME:
            app.current_theme = DARK_THEME
            self.theme_btn.text = "Switch to Light Mode"
        else:
            app.current_theme = LIGHT_THEME
            self.theme_btn.text = "Switch to Dark Mode"

        self.theme = app.current_theme
        self.apply_theme()
        app.spin_screen.apply_theme()

    def apply_theme(self):
        if not hasattr(self, "layout") or not self.layout.parent:
            return

        # Only draw rectangle and color once
        if not hasattr(self, "bg_color_instruction"):
            with self.canvas.before:
                self.bg_color_instruction = Color(*self.theme["bg_color"])
                self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)
        else:
            # Just update the existing color
            self.bg_color_instruction.rgba = self.theme["bg_color"]

        for child in self.layout.children:
            if isinstance(child, Label):
                # Make only the title black in light mode
                if child == self.title_label and self.theme == LIGHT_THEME:
                    child.color = [0, 0, 0, 1]
                else:
                    child.color = self.theme["text_color"]
            elif isinstance(child, Button):
                child.background_color = self.theme["button_color"]
                child.color = [1, 1, 1, 1]  # Always white text on buttons

    def update_rect(self, *args):
        if hasattr(self, "rect"):
            self.rect.pos = self.pos
            self.rect.size = self.size

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
        self.cooldown_start_time = 0
        self.cooldown_event = None

        self.cooldown_upgrade_cost = 50
        self.luck_upgrade_cost = 50

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        from kivy.uix.anchorlayout import AnchorLayout

        storage_anchor = AnchorLayout(anchor_x='right', anchor_y='top', size_hint=(1, None), height=40)
        storage_btn = Button(
            text="Title Storage",
            size_hint=(None, None),
            size=(160, 40),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=App.get_running_app().current_theme["button_color"],
            color=App.get_running_app().current_theme["text_color"]
        )
        storage_btn.bind(
            on_press=lambda x: self.manager.get_screen('storage').refresh_storage() or setattr(self.manager, 'current',
                                                                                               'storage'))
        storage_anchor.add_widget(storage_btn)
        self.layout.add_widget(storage_anchor)

        self.title_label = Label(text="You Got:", font_size=60, font_name="Bahnschrift",)
        self.result_label = Label(text="", font_size=55, font_name="Bahnschrift", height=-10)
        self.store_btn = Button(
            text="Store Title",
            size_hint=(None, 0.15),
            size=(200, 50),
            font_size='30sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=App.get_running_app().current_theme["button_color"],
            color=App.get_running_app().current_theme["text_color"]
        )
        self.store_btn.bind(on_press=self.store_title)
        self.store_btn.opacity = 0  # hidden initially
        self.store_btn.disabled = True
        self.layout.add_widget(self.store_btn)
        self.cooldown_label = Label(text="", font_size=25, font_name="Bahnschrift")
        self.status_label = Label(text="", font_size=25, font_name="Bahnschrift")

        self.title_storage = {}

        from kivy.uix.widget import Widget

        self.spin_button = Button(
            text="Spin",
            size_hint=(1, 0.25),
            font_size='30sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=App.get_running_app().current_theme["button_color"],
            color=App.get_running_app().current_theme["text_color"]
        )
        self.spin_button.bind(on_press=self.spin)

        spacer1 = Widget(size_hint_y=0.02)

        upgrade_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.18), spacing=10)
        self.cooldown_upgrade_btn = Button(
            text="Upgrade Cooldown\n(-0.1s)\nCost: 25 MB",
            size_hint_y=None,
            height=50,  # << Adjust as needed
            font_size='20sp',
            font_name="Bahnschrift",
            halign='center',
            valign='middle',
            padding=(5, 5),
            background_normal='',
            background_color=App.get_running_app().current_theme["button_color"],
            color=App.get_running_app().current_theme["text_color"]
        )
        self.cooldown_upgrade_btn.bind(on_press=self.upgrade_cooldown)

        self.luck_upgrade_btn = Button(
            text="Upgrade Luck\n(+0.1x)\nCost: 50 MB",
            size_hint_y=None,
            height=50,
            font_size='20sp',
            font_name="Bahnschrift",
            halign='center',
            valign='middle',
            padding=(5, 5),
            background_normal='',
            background_color=App.get_running_app().current_theme["button_color"],
            color=App.get_running_app().current_theme["text_color"]
        )

        self.luck_upgrade_btn.bind(on_press=self.upgrade_luck)

        for btn in [self.cooldown_upgrade_btn, self.luck_upgrade_btn]:
            btn.text_size = (btn.width, None)
            btn.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

        upgrade_layout.add_widget(self.cooldown_upgrade_btn)
        upgrade_layout.add_widget(self.luck_upgrade_btn)

        spacer2 = Widget(size_hint_y=0.01)

        back_btn = Button(
            text="Back to Menu",
            size_hint=(1, 0.15),
            font_size='20sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=App.get_running_app().current_theme["button_color"],
            color=App.get_running_app().current_theme["text_color"]
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))

        self.spin_sound = SoundLoader.load("audio/common_sound.wav")
        self.rare_sound = SoundLoader.load("audio/rare_sound.wav")
        self.upgrade_sound = SoundLoader.load("audio/upgrade_sound.wav")
        self.bg_music = SoundLoader.load("audio/background.wav")
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5
            self.bg_music.play()

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.cooldown_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.spin_button)
        self.layout.add_widget(spacer1)
        self.layout.add_widget(upgrade_layout)
        self.layout.add_widget(spacer2)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)
        Clock.schedule_once(lambda dt: self.apply_theme(), 0)
        self.update_ui()


    def apply_theme(self):
        app = App.get_running_app()
        theme = app.current_theme


        if not hasattr(self, "bg_color_instruction"):
            with self.canvas.before:
                self.bg_color_instruction = Color(*theme["bg_color"])
                self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)
        else:
            self.bg_color_instruction.rgba = theme["bg_color"]


        # Ensure all buttons and labels reflect theme
        def apply_theme_to_widget(widget):
            if isinstance(widget, Label):
                # Custom handling for specific labels
                if widget in [self.title_label, self.status_label, self.cooldown_label, self.result_label]:
                    # These should match the theme (black in light, white in dark)
                    if theme == LIGHT_THEME:
                        widget.color = [0, 0, 0, 1]
                    else:
                        widget.color = [1, 1, 1, 1]
                else:
                    widget.color = theme["text_color"]
            elif isinstance(widget, Button):
                widget.color = theme["text_color"]  # 🔥 This sets text color
                widget.background_color = theme["button_color"]
                widget.background_normal = ''
            if hasattr(widget, 'children'):
                for child in widget.children:
                    apply_theme_to_widget(child)



        apply_theme_to_widget(self)

    def update_rect(self, *args):
        if hasattr(self, "rect"):
            self.rect.pos = self.pos
            self.rect.size = self.size

    def spin(self, instance):
        if self.cooldown:
            return
        self.cooldown = True
        self.cooldown_start_time = Clock.get_time()
        self.cooldown_label.text = f"Cooldown: {self.cooldown_time:.1f}s"
        self.spin_count += 1
        title, display, base_prob, adjusted_prob = get_random_title(self.luck_multiplier)
        self.result_label.text = f"{title} ({display})"
        self.store_btn.opacity = 1
        self.store_btn.disabled = False

        if base_prob < 1 / 999
            self.rare_sound.play()
        elif self.spin_sound:
            self.spin_sound.play()

        self.currency += 2 + (self.spin_count // 100)
        self.update_ui()
        self.cooldown_label.text = f"Cooldown: {self.cooldown_time:.1f}s"
        self.cooldown_event = Clock.schedule_interval(self.update_cooldown_display, 0.1)
        Clock.schedule_once(self.reset_cooldown, self.cooldown_time)

    def update_cooldown_display(self, dt):
        elapsed = Clock.get_time() - self.cooldown_start_time
        remaining = max(0, self.cooldown_time - elapsed)
        if remaining > 0:
            self.cooldown_label.text = f"Cooldown: {remaining:.1f}s"
        else:
            self.cooldown_label.text = ""
            return False  # stop the interval

    def reset_cooldown(self, dt):
        self.cooldown = False
        self.cooldown_label.text = ""
        if self.cooldown_event:
            self.cooldown_event.cancel()
            self.cooldown_event = None

    def update_ui(self):
        self.status_label.text = f"Spins: {self.spin_count} | MB: {self.currency} | Luck: {self.luck_multiplier:.2f}x | CD: {self.cooldown_time:.2f}s"
        self.cooldown_upgrade_btn.text = f"Upgrade Cooldown (-0.025s)\nCost: {self.cooldown_upgrade_cost} MB"
        self.luck_upgrade_btn.text = f"Upgrade Luck (+0.1x)\nCost: {self.luck_upgrade_cost} MB"

    def show_message(self, msg):
        Popup(title="Upgrade", content=Label(text=msg), size_hint=(None, None), size=(300, 150)).open()

    def upgrade_cooldown(self, instance):
        if self.cooldown_time <= self.cooldown_min:
            self.show_message("Cooldown already at minimum!")
        elif self.currency >= self.cooldown_upgrade_cost:
            self.currency -= self.cooldown_upgrade_cost
            self.cooldown_time = max(self.cooldown_time - 0.025, self.cooldown_min)
            self.show_message(f"Cooldown reduced to {self.cooldown_time:.2f}s")
            self.upgrade_sound.play()
            self.update_ui()
        else:
            self.show_message("Not enough Mog Bucks!")

    def upgrade_luck(self, instance):
        if self.currency >= self.luck_upgrade_cost:
            self.currency -= self.luck_upgrade_cost
            self.luck_multiplier += 0.1
            self.show_message(f"Luck increased to {self.luck_multiplier:.2f}x")
            self.upgrade_sound.play()
            self.update_ui()
        else:
            self.show_message("Not enough Mog Bucks!")

    def store_title(self, instance):
        title = self.result_label.text.split(' (')[0]
        if title:
            self.title_storage[title] = self.title_storage.get(title, 0) + 1
            self.show_message(f"Stored {title}!")
            self.store_btn.opacity = 0
            self.store_btn.disabled = True


class StorageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme = DARK_THEME
        from kivy.uix.anchorlayout import AnchorLayout

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Label at top of screen
        title_anchor = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=(1, None), height=60)
        self.title_label = Label(text="Stored Titles", font_size=40, font_name="Bahnschrift")
        title_anchor.add_widget(self.title_label)
        self.layout.add_widget(title_anchor)

        # Scroll area or list (can be added next)
        self.list_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 1))
        self.layout.add_widget(self.list_layout)

        back_btn = Button(
            text="Back to Spin Menu",
            size_hint=(1, 0.1),
            font_size='30sp',
            font_name="Bahnschrift",
            background_normal='',
            background_color=self.theme["button_color"],
            color=self.theme["text_color"]
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'spin'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def refresh_storage(self):
        self.list_layout.clear_widgets()
        for title, count in App.get_running_app().spin_screen.title_storage.items():
            entry = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Label(text=f"{title} x{count}", font_size=18, font_name="Bahnschrift", halign='left')
            del_btn = Button(text="Delete", size_hint_x=0.3)
            del_btn.bind(on_press=lambda instance, t=title: self.delete_title(t))
            entry.add_widget(label)
            entry.add_widget(del_btn)
            self.list_layout.add_widget(entry)

    def delete_title(self, title):
        storage = App.get_running_app().spin_screen.title_storage
        if title in storage:
            storage[title] -= 1
            if storage[title] <= 0:
                del storage[title]
            self.refresh_storage()


class MoggersApp(App):
    def build(self):
        self.current_theme = DARK_THEME  # Default theme
        sm = ScreenManager(transition=NoTransition())
        self.main_menu = MainMenu(name="main")
        sm.add_widget(self.main_menu)
        self.spin_screen = SpinScreen(name="spin")
        sm.add_widget(self.spin_screen)
        self.storage_screen = StorageScreen(name="storage")
        sm.add_widget(self.storage_screen)
        return sm


if __name__ == "__main__":
    MoggersApp().run()
