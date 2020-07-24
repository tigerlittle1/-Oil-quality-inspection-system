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
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from functools import partial

from plyer import light
from plyer import accelerometer

import numpy
import threading
import time


class Sensor_Light_Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = '50dp'
        self.spacing = '50dp'

        self.state_label = Label(text = "")
        self.add_widget(self.state_label)

        self.lium_label = Label(text = "")
        self.add_widget(self.lium_label)

        self.seting_button = Button(text="Set cfg",size_hint = (1,0.25))#設定按鈕
        self.seting_button.bind(on_press=self.setting)
        self.add_widget(self.seting_button)

        self.close_button = Button(text="Close Connect",size_hint = (1,0.25))#關閉按鈕
        self.close_button.bind(on_press=self.close)
        self.add_widget(self.close_button)

        self.internet = Client.Client()
        self.illumination = 0

        self.data = []
        self.Acid1 = 0
        self.Acid2 = 0
        self.lux1 = 0
        self.lux2 = 0

    def listen_sever(self):
        try:
            Clock.schedule_interval(self.get_illumination, 1 / 20.)
            self.state_label.text = "start light"
        except Exception as e:
            self.state_label.text = str(e)
            pass

        while True:
            try:
                self.internet.get_message()#等待要求
                self.state_label.text = "loading"
                message = str(sum(self.data) / len(self.data))#傳送平均lux
                message = "{} {} {} {} {}".format(sum(self.data) / len(self.data) , self.Acid1,self.lux1, self.Acid2,self.lux2)#傳送平均lux,Acid1,Acid2
                self.sned_message(message)
                self.state_label.text = "send : " + message

            except Exception as e:
                print(e)
                self.close()
                break

    def sned_message(self,message):
        self.internet.sned_message(message)

    def close(self,instance=None,change = ""):
        try:
            self.internet.close_connet()
            Clock.unschedule(self.get_illumination)#關閉光線讀取
            light.disable()
            if change != "don't change page":
                chat.screen_manager.current = "loing"
        except :
            pass

    def setting(self,instance):
        self.close(change = "don't change page")
        chat.setting_page.Acid_1.text = str(self.Acid1)
        chat.setting_page.Acid_2.text = str(self.Acid2)
        chat.setting_page.lux_1.text = str(self.lux1)
        chat.setting_page.lux_2.text = str(self.lux2)
        chat.screen_manager.current = "Setting"
    def init_connect(self,ip = '0.tcp.ngrok.io',port = 19446):
        try:
            self.internet.init_connect(ip,port)
            threading.Thread(target=self.listen_sever).start()
            self.state_label.text = "stater connect\nAcid1 : {}\nAcid1 : {}".format(self.Acid1,self.Acid2)
            light.enable()  # 開啟光線讀取
        except:
            pass

    def get_illumination(self, dt):
        try:
            self.illumination = light.illumination or self.illumination
            self.lium_label.text = str(self.illumination)+"lux"
            print(self.illumination)

            if len(self.data) >= 5:#儲存最新的5筆資料
                del self.data[0] #刪除最舊的一筆
                self.data.append(self.illumination)#加入最新資料
            else:
                self.data.append(self.illumination)

        except Exception as e:
            self.illumination = "light error"
            self.lium_label.text = "light error"
            print(e)

class Sensor_Accelerometer_Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = '50dp'
        self.spacing = '50dp'

        self.state_label = Label(text = "111")
        self.add_widget(self.state_label)

#        self.x_label = Label(text = "x:")
#        self.add_widget(self.x_label)
        self.y_label = Label(text = "y:")
        self.add_widget(self.y_label)
#        self.z_label = Label(text = "z:")
#        self.add_widget(self.z_label)
        self.close_button = Button(text="Close Connect",size_hint = (1,0.25))

        self.close_button.bind(on_press=self.close)
        self.add_widget(self.close_button)

        self.internet = Client.Client()
        self.acceleration = [0,0,0]
        self.ask = False

        self.data = []
        self.prdata = []

    def listen_sever(self):
        try:
            self.state_label.text = "start accelerometer"
            Clock.schedule_interval(self.get_acceleration, 1 / 20.)
        except Exception as e:
            self.state_label.text = str(e)
            pass
        while True:
            try:
                time_sleep = self.internet.get_message()#等待要求
                self.state_label.text =" data loading , palse wate" +  time_sleep + "second..."
                self.ask = True

                #time.sleep(float(time_sleep))#暫停2秒以取得2秒內最高值
                Clock.schedule_once(self.set_acceleration,float(time_sleep))

            except ValueError:
                pass
            except Exception as e:
                print(e)
                self.state_label.text = str(e)
                time.sleep(5)
                self.close()
                break

    def sned_message(self,message):
        self.internet.sned_message(message)

    def close(self,instance=None):
        try:
            self.internet.close_connet()
            chat.screen_manager.current = "loing"
            Clock.unschedule(self.get_acceleration)#關閉加速度讀取
            accelerometer.disable()
        except:
            pass

    def init_connect(self,ip = '0.tcp.ngrok.io',port = 19446):
        try:
            self.internet.init_connect(ip,port)
            threading.Thread(target=self.listen_sever).start()
            self.state_label.text = "stater connect"
            accelerometer.enable()#開啟加速度讀取
        except:
            pass

    def get_acceleration(self, dt):
        try:
            self.acceleration = accelerometer.acceleration[:3] or self.acceleration
#            self.x_label.text = "x : "+str(self.acceleration[0])
            self.y_label.text = "y : "+str(round(self.acceleration[1],5)) + "m/s^2"
#            self.z_label.text = "z : "+str(self.acceleration[2])

            if self.ask:#是否要讀取
                self.data.append(self.acceleration)

        except Exception as e:
            self.acceleration = "accelerometer error"
            self.state_label.text = "accelerometer error"

    def set_acceleration(self, dt):
#        while True:
        for i in range(1, len(self.data) - 1):  # 取得y軸波峰
            if self.data[i][1] > self.data[i - 1][1] and self.data[i][1] > self.data[i + 1][1]:
                self.prdata.append(self.data[i][1])

        if len(self.prdata) >= 15:  # 判斷是否有取得15個以上波峰
            self.prdata = self.prdata[0:15]  # 取得前15個波峰

            y = self.prdata
            x = range(1, len(y) + 1)

            message = str(numpy.polyfit(x, numpy.log(y), 1)[0])  # 傳送加速度所取得指數趨勢圖係數

            self.sned_message(message)
            self.data = []
            self.prdata = []
            self.ask = False
            self.state_label.text = "send : " + message

        else:  # 波峰不足，繼續取得資料
            self.prdata = []
            Clock.schedule_once(self.set_acceleration,1)


class Loing_Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = '10dp'
        self.spacing = '30dp'

        self.Grid = GridLayout(cols=2)
        self.Grid.spacing = '5dp'

        self.Grid.add_widget(Label(text='IP:',size_hint = (0.4,1)))  # widget #1, top left
        self.ip = TextInput(text="0.tcp.ngrok.io", multiline=False,size_hint = (0.6,1))  # defining self.ip...
        self.Grid.add_widget(self.ip) # widget #2, top right

        self.Grid.add_widget(Label(text='Port:',size_hint = (0.4,1)))
        self.port = TextInput(text="15013", multiline=False,size_hint = (0.6,1))
        self.Grid.add_widget(self.port)

        self.Grid.add_widget(Label(text='Sensor:',size_hint = (0.4,1)))
        self.username = Spinner(text="Light",values=('Light', 'Acceleration'),size_hint=(0.6,0.1),background_color = (256,256,256,1),color = (0,0,0,1))
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
            if self.username.text == "Light":
                try:
                    with open("acid.cfg", "r") as f:
                        c = f.readlines()
                        a1 = float(c[0].rstrip("\n"))
                        b1 = float(c[1].rstrip("\n"))
                        a2 = float(c[2].rstrip("\n"))
                        b2 = float(c[3])
                        chat.light_page.init_connect(self.ip.text, int(self.port.text))
                        chat.light_page.sned_message("s_l")
                        chat.light_page.Acid1 = a1
                        chat.light_page.Acid2 = a2
                        chat.light_page.lux1 = b1
                        chat.light_page.lux2 = b2
                        chat.screen_manager.current = self.username.text
                except:
                    chat.screen_manager.current = "Setting"
            else:
                chat.acceleration_page.init_connect(self.ip.text,int(self.port.text))
                chat.acceleration_page.sned_message("s_a")
                chat.screen_manager.current = self.username.text
        except Exception as e:
            self.Error_box.title = "Connect erroe"
            self.Error_box_label.text = "Error connect,check connect set,please try again"
            self.Error_box_label.text_size = (self.Error_box_label.width,None)
            self.Error_box.open()
            print("connect error : ",e)
            pass

class Setting_Layout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = '10dp'
        self.spacing = '30dp'

        self.Grid1 = GridLayout(cols=2, size_hint=(1, 0.3))
        self.Grid1.spacing = '5dp'

        self.Grid1.add_widget(Label(text='Acid_1:', size_hint=(0.1, 1)))  #
        self.Acid_1 = TextInput(text="10", multiline=False, size_hint=(0.1, 1),input_type="number")  # defining self.ip...
        self.Grid1.add_widget(self.Acid_1)  # widget #2, top right
        self.Grid1.add_widget(Label(text='lux_1:', size_hint=(0.1, 1)))  # widget #1, top left
        self.lux_1 = TextInput(text="5",readonly=True, multiline=False, size_hint=(0.1, 1))
        self.Grid1.add_widget(self.lux_1)
        self.add_widget(self.Grid1)
        self.get_lux1 = Button(text="get Acid_1 lux", size_hint=(1, 0.1))
        self.get_lux1.bind(on_press=partial(self.get_lux, self.lux_1))
        self.add_widget(self.get_lux1)

        self.Grid2 = GridLayout(cols=2, size_hint=(1, 0.3))
        self.Grid2.spacing = '5dp'
        self.Grid2.add_widget(Label(text='Acid_2:', size_hint=(0.1, 1)))
        self.Acid_2 = TextInput(text="10", multiline=False, size_hint=(0.1, 1), input_type="number")
        self.Grid2.add_widget(self.Acid_2)
        self.Grid2.add_widget(Label(text='lux_2:', size_hint=(0.1, 1)))  # widget #1, top left
        self.lux_2 = TextInput(text="5",readonly=True, multiline=False, size_hint=(0.1, 1))
        self.Grid2.add_widget(self.lux_2)
        self.add_widget(self.Grid2)
        self.get_lux2 = Button(text="get Acid_2 lux", size_hint=(1, 0.1))
        self.get_lux2.bind(on_press=partial(self.get_lux,self.lux_2))
        self.add_widget(self.get_lux2)

        self.set = Button(text="Start", size_hint=(1, 0.2))
        self.set.bind(on_press=self.set_acid)
        self.add_widget(self.set)

        self.Error_box = Popup(size_hint=(None, None), size=(400, 400))
        self.Error_layout = BoxLayout(orientation="vertical")
        self.Error_box_label = Label(text="", size_hint=(1, 0.8))
        self.Error_layout.add_widget(self.Error_box_label)
        self.Error_layout.add_widget(Button(text="Close", on_press=self.Error_box.dismiss, size_hint=(1, 0.2)))
        self.Error_box.content = self.Error_layout

        self.Acid1 = 0
        self.Acid2 = 0
        self.lux1 = 0
        self.lux2 = 0
        self.data = []

    def set_acid(self,instance):
        try:
            with open("acid.cfg", "w") as f:
                self.Acid1 = float(self.Acid_1.text)
                self.Acid2 = float(self.Acid_2.text)
                self.lux1 = float(self.lux_1.text)
                self.lux2 = float(self.lux_2.text)
                f.write(str(self.Acid1) + "\n" + str(self.lux1) + "\n" + str(self.Acid2) + "\n" + str(self.lux2))
            chat.light_page.Acid1 = self.Acid1
            chat.light_page.Acid2 = self.Acid2
            chat.light_page.lux1 = self.lux1
            chat.light_page.lux2 = self.lux2
            chat.light_page.init_connect(chat.loing_page.ip.text, int(chat.loing_page.port.text))
            chat.light_page.sned_message("s_l")
            chat.screen_manager.current = "Light"
        except ValueError:
            self.Error_box.title = "Set erroe"
            self.Error_box_label.text = "Plase enter number,try again"
            self.Error_box_label.text_size = (self.Error_box_label.width,None)
            self.Error_box.open()

    def get_lux(self,textinput,instance):
        try:
#            textinput.text = "Plase place sensor in 2 seconds"
            print(self.lux_1.text)
            light.enable()  # 開啟光線讀取
            Clock.schedule_interval(self.get_illumination, 1 / 20.)
            textinput.text = "Getting lux,plase waite 5 seconds"
            self.get_lux1.disabled = True
            self.get_lux2.disabled = True
            self.set.disabled = True
            Clock.schedule_once(partial(self.set_lux,textinput), 5)


        except Exception as e:
            textinput.text = str(e)

    def set_lux(self,textinput,dt):
        Clock.unschedule(self.get_illumination)  # 關閉光線讀取
        light.disable()
        print(self.data)
        textinput.text = str(sum(self.data) / len(self.data))
        self.data = []
        self.get_lux1.disabled = False
        self.get_lux2.disabled = False
        self.set.disabled = False

    def get_illumination(self,dt):
        try:
            illumination =  light.illumination or 5
            print(illumination)
            if len(self.data) >= 5:#儲存最新的5筆資料
                del self.data[0] #刪除最舊的一筆
                self.data.append(illumination)#加入最新資料
            else:
                self.data.append(illumination)
        except Exception as e:
            print(e)

class Chat(App):
    def build(self):
        # We are going to use screen manager, so we can add multiple screens
        # and switch between them
        self.screen_manager = ScreenManager()
        self.loing_page = Loing_Layout()
        screen = Screen(name='loing')
        screen.add_widget(self.loing_page)
        self.screen_manager.add_widget(screen)

        self.light_page = Sensor_Light_Layout()
        screen = Screen(name='Light')
        screen.add_widget(self.light_page)
        self.screen_manager.add_widget(screen)

        self.acceleration_page = Sensor_Accelerometer_Layout()
        screen = Screen(name='Acceleration')
        screen.add_widget(self.acceleration_page)
        self.screen_manager.add_widget(screen)

        self.setting_page = Setting_Layout()
        screen = Screen(name='Setting')
        screen.add_widget(self.setting_page)
        self.screen_manager.add_widget(screen)

        Window.bind(on_request_close=self.on_request_close)
        return self.screen_manager

    def on_request_close(self, *largs):
        print("close")
        self.light_page.internet.close_connet()
        self.acceleration_page.internet.close_connet()

    def on_pause(self):
        return True

chat = Chat()
chat.run()
