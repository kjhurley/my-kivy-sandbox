from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
import kivy.uix.textinput
import kivy.uix.modalview
import kivy.uix.label
import kivy.uix.button
#from sleekxmpp import ClientXMPP
import time


#class JabberWrapper(object):
#    def __init__(self, jabber_id, password):
#        self._xmpp = ClientXMPP(jabber_id, password)
#
#    def connect(self):
#        self._xmpp.connect()
#        self._xmpp.process()
#        self._xmpp.send_presence()
#        self._xmpp.get_roster()
        
JABBER_CONNECT_DELAY=5 # seconds
JABBER_CONNECTS=True
JABBER_BUDDIES=["kev","bev","trev","dave","knave"]
JABBER_ID="my.name@test.com"

class JabberStub:
    #  a stub for the class that interacts with xmpp server
    def __init__(self, jabber_id, password):
        self.buddies=[]
        self.jabber_id=jabber_id
        self.password=password
        self.connected=False
    
    def connect(self):
        print "CONNECT TO JABBER USING %s"%self.jabber_id
        time.sleep(JABBER_CONNECT_DELAY)
        if self.jabber_id != JABBER_ID:
            raise RuntimeError("wrong id")
        if JABBER_CONNECTS:
            print "CONNECTED TO JABBER"
            self.buddies=JABBER_BUDDIES
            self.connected=True
        else:
            raise RuntimeError("foo")
    
    def roster_keys(self):
        return self.buddies
    
    def disconnect(self):
        print "DISCONNECTED FROM JABBER"
        self.connected=False
        
    def abort(self):
        print "CONNECTION TO JAMMER ABORTED"
        self.connected=False

class ConnectionModal(kivy.uix.modalview.ModalView):
    def __init__(self, jabber_id, password):
        kivy.uix.modalview.ModalView.__init__(self, auto_dismiss=False, anchor_y="bottom")
        self.label = kivy.uix.label.Label(text="Connecting to %s..."%jabber_id)
        self.add_widget(self.label)
        self.jabber_id=jabber_id
        self.password=password
        self.on_open=self.connect_to_jabber
        
    def connect_to_jabber(self):
        app=Orkiv.get_running_app()
        try:
            app.connect_to_jabber(self.jabber_id,self.password)
            self.label.text="\n".join(app.xmpp.roster_keys())
        except RuntimeError:
            self.label.text="Sorry, couldnt connect"
            button=kivy.uix.button.Button(text="Try Again")
            button.size_hint=(1.0,None)
            button.height="40dp"
            button.bind(on_press=self.dismiss)
            self.add_widget(button)
            app.disconnect_xmpp()

class AccountDetailsTextInput(kivy.uix.textinput.TextInput):
    next = ObjectProperty()
    
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        
        if keycode[0]==9: # tab
            self.next.focus=True
        elif keycode[0]==13: # enter
            self.parent.parent.parent.login() # FIXME
        else:
            return kivy.uix.textinput.TextInput._keyboard_on_key_down(self, window, keycode, text, modifiers)

class AccountDetailsForm(AnchorLayout):
    server_box = ObjectProperty()
    username_box= ObjectProperty()
    password_box = ObjectProperty()
    def login(self):
        jabber_id = self.username_box.text+'@'+self.server_box.text
        modal=ConnectionModal(jabber_id,self.password_box.text)
        modal.open()

class Orkiv(App):
    def __init__(self):
        super(Orkiv,self).__init__()
        self.xmpp=None
        self.on_stop=self.disconnect_xmpp
        
    def connect_to_jabber(self, jabber_id, password):
        self.xmpp=JabberStub(jabber_id,password)
        self.xmpp.connect()
    def disconnect_xmpp(self):
        if self.xmpp and self.xmpp.connected:
            self.xmpp.abort()
        self.xmpp=None
    
Orkiv().run()
