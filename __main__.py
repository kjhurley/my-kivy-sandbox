from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout

class AccountDetailsForm(AnchorLayout):
    def login(self):
        print "click it"

class Orkiv(App):
    pass

Orkiv().run()
