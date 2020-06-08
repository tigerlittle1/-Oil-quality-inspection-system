import socket
import threading
import math
import os
class Server():
    def __init__(self):
        self.HOST = config['Server']['HOST']  # 本機預設伺服器
        self.PORT = int(os.environ.get('PORT'))

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(10)

        print("IP : {} , PORT : {}".format(self.HOST, self.PORT))  # 顯示server端

        self.sensor_connect = {"s_a" : None , "s_l" : None}
        self.control_app = None
        self.APP_client = []

        accept_thread = threading.Thread(target=self.accetp_connet)
        accept_thread.start()

    def clientThreadIn(self,conn,ip):
        while True:
            try:
                clientMessage = conn.recv(1024)
                if not clientMessage:
                    conn.close()
                    break
                else:
                    if clientMessage == "close connect":
                        print("Client IP : {} is close".format(ip))
                        conn.close()
                        break
                    else:
                        print("Client IP : {} , Client message is: {}".format(ip,clientMessage))
                        sensor_message = {"s_a":None,"s_l":None}

                        for sensor in ("s_a","s_l"):
                            try:
                                self.sensor_connect[sensor].sendall("3".encode())
                                sensor_message[sensor] = self.sensor_connect[sensor].recv(1024).decode()
                                print(sensor_message[sensor])
                            except:
                                print(sensor,"is close")
                                self.sensor_connect[sensor] = None
                                sensor_message[sensor] = None

                        if sensor_message["s_a"] != None and sensor_message["s_l"] != None :#兩個sensor都有連上
                            ay = sensor_message["s_a"]
                            l = sensor_message["s_l"]
                            serverMessage = self.caculate_oil(ay,l)  # 計算函式
                        else:#其中一個sensor沒有連上
                            if sensor_message["s_l"] != None :
                                serverMessage = 'Accelerometer sensor error,\nLight acid value:' + str(self.caculate_lige(sensor_message["s_l"]))
                            elif sensor_message["s_a"] != None :
                                serverMessage = 'Light sensor error,\nAccelerometer acid value:'+str(self.caculate_Accelerometer(sensor_message["s_a"]))
                            else:
                                serverMessage = "sensor error"
                        print("send '{}' to {}".format(serverMessage,ip))
                        temp = []
                        print(self.APP_client)
                        for c in self.APP_client:
                            try:
                                c.sendall(serverMessage.encode())
                                temp.append(c)
                            except :
                                pass
                        self.APP_client = temp

            except Exception as e:
                conn.close()
                print("Client IP : {} is close , {}".format(ip,e))
                break
    def caculate_oil(self,ay,l):#當兩個感測器都有連上線
        new_l = self.caculate_lige(l)
        new_ay = self.caculate_Accelerometer(ay)
        if new_l > 2:
            serverMessage = "change oil\nAcid value: " + str(round(ay,5)) + "\nlux :" + str(round(new_l,5))
        else:
            serverMessage = "oil is good\nAcid value: " + str(round(ay,5)) + "\nlux :" + str(round(new_l,5))
        return serverMessage
    def caculate_lige(self,l):#計算光線酸價
        try:
            l = float(l)
        except:
            l = 0
        new_l = l * 0.0003 + 2.8681#在此填上光線計算酸價公式
        return round(new_l,2)

    def caculate_Accelerometer(self,ay):#計算加速度酸價
        try:
            ay = float(ay)
        except:
            ay = 0
        new_ay = ay * 0.0003 + 2.8681#在此填上加速度計算酸價公式
        return round(new_ay,10)
    def accetp_connet(self):
        while 1:
            try:
                conn, addr = self.server.accept()

                name = conn.recv(1024).decode()
                if name == "s_a":  # sensor_Acceleration
                    print("sensor_Acceleration connect,IP: {}".format(addr))
                    self.sensor_connect[name] = conn
                elif name == "s_l":  # sensor_Luminosity
                    print("sensor_Luminosity connect,IP: {}".format(addr))
                    self.sensor_connect[name] = conn
                else:
                    print("Accept APP ,IP: {}".format(addr))
                    conn.sendall("Accept APP".encode())
                    appclient = threading.Thread(target=self.clientThreadIn, args=(conn, addr))
                    appclient.start()
                    self.APP_client.append(conn)
            except:
                pass

server = Server()


