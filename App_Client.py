import Client
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
import threading

class Chat_Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = '50dp'
        self.spacing = '50dp'

        self.diaplay_label = Label(text = "",size_hint = (1,0.5))
        self.enter_button = Button(text = "Oil quality test",size_hint = (1,0.25))
        self.close_button = Button(text="Close Connect",size_hint = (1,0.25))

        self.enter_button.bind(on_press = self.sned_message)
        self.close_button.bind(on_press=self.close)

        self.add_widget(self.diaplay_label)
        self.add_widget(self.enter_button)
        self.add_widget(self.close_button)

        self.internet = Client.Client()


    def listen_server(self):
        while True:
            print("test")
            try:
                self.diaplay_label.text = self.internet.get_message()
                print("get")
            except:
                print("error")
                self.close("1")
                break


    def sned_message(self,instance):
        self.internet.sned_message("get")
        self.diaplay_label.text = "data getting,palse wait"

    def init(self,ip,port):
        self.internet.init_connect(ip,port)
        threading.Thread(target=self.listen_server).start()


    def close(self,instance):
        self.internet.close_connet()
        self.diaplay_label.text = "close connect"
        chat.screen_manager.current = "loing"



class Loing_Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = '10dp'
        self.spacing = '30dp'

        self.Grid = GridLayout(cols = 2)
        self.Grid.spacing = '5dp'

        self.Grid.add_widget(Label(text='IP:',size_hint = (0.4,1)))  # widget #1, top left
        self.ip = TextInput(text="127.0.0.1", multiline=False,size_hint = (0.6,1))  # defining self.ip...
        self.Grid.add_widget(self.ip) # widget #2, top right

        self.Grid.add_widget(Label(text='Port:',size_hint = (0.4,1)))
        self.port = TextInput(text="8080", multiline=False,size_hint = (0.6,1))
        self.Grid.add_widget(self.port)

        self.Grid.add_widget(Label(text='Username:',size_hint = (0.4,1)))
        self.username = TextInput(text="server", multiline=False,size_hint = (0.6,1))
        self.Grid.add_widget(self.username)

        self.add_widget(self.Grid)

        self.start = Button(text="Start",size_hint = (1,0.2))
        self.start.bind(on_press=self.start_chat)
        self.add_widget(self.start)

        self.Error_box = Popup(size_hint = (None,None),size = (400,400))
        self.Error_layout = BoxLayout(orientation = "vertical")
        self.Error_box_label = Label(text = "",size_hint=(1,0.8))
        self.Error_layout.add_widget(self.Error_box_label)
        self.Error_layout.add_widget(Button(text = "Close",on_press=self.Error_box.dismiss,size_hint=(1,0.2)))
        self.Error_box.content = self.Error_layout

    def start_chat(self,instance):
        try:
            chat.chat_page.init(self.ip.text,int(self.port.text))
            chat.chat_page.sned_message("APP")
            chat.screen_manager.current = "chat"
        except Exception as e:
            self.Error_box.title = "Connect erroe"
            self.Error_box_label.text = "Error connect,check connect set,please try again"
            self.Error_box_label.text_size = (self.Error_box_label.width, None)
            self.Error_box.open()
            print(e)
            pass


class Chat(App):
    def build(self):
        # We are going to use screen manager, so we can add multiple screens
        # and switch between them
        self.screen_manager = ScreenManager()

        self.loing_page = Loing_Layout()
        screen = Screen(name='loing')
        screen.add_widget(self.loing_page)
        self.screen_manager.add_widget(screen)

        self.chat_page = Chat_Layout()
        screen = Screen(name='chat')
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)

        Window.bind(on_request_close=self.on_request_close)

        return self.screen_manager
    def on_request_close(self, *largs):
        print("close")
        self.chat_page.internet.close_connet()

chat = Chat()
chat.run()