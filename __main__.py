from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from sleekxmpp import ClientXMPP

class JabberWrapper(object):
    def __init__(self, jabber_id, password):
        self._xmpp = ClientXMPP(jabber_id, password)

    def connect(self):
        self._xmpp.connect()
        self._xmpp.process()
        self._xmpp.send_presence()
        self._xmpp.get_roster()
        


class AccountDetailsForm(AnchorLayout):
    server_box = ObjectProperty()
    username_box= ObjectProperty()
    password_box = ObjectProperty()
    def login(self):
        print self.server_box.text
        print self.username_box.text
        print self.password_box.text

class Orkiv(App):
    def connect_to_jabber(self, jabber_id, password):
        self.xmpp=JabberWrapper(jabber_id,password)
        self.xmpp.connect()
        
Orkiv().run()
