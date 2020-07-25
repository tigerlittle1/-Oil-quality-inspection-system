import socket
import threading
import math

class Server():
    def __init__(self):
        self.HOST = "127.0.0.1"  # 本機預設伺服器
        self.PORT = 8080

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
                                self.sensor_connect[sensor][1].sendall("3".encode())
                                sensor_message[sensor] = self.sensor_connect[sensor][1].recv(1024).decode()
                                print("{} message is {}".format(sensor,sensor_message[sensor]))
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

            except socket.error:
                conn.close()
                print("Client IP : {} is close , {}".format(ip, e))
                break
            except Exception as e:
                serverMessage = str(e)
                # conn.close()
                # print("Client IP : {} is close , {}".format(ip,e))
                # break

            print("send '{}' to {}".format(serverMessage, ip))
            temp = []
            print(self.APP_client)

            for c in self.APP_client:
                try:
                    c.sendall(serverMessage.encode())
                    temp.append(c)
                except :

                    pass
            self.APP_client = temp

    def caculate_oil(self,ay,l):#當兩個感測器都有連上線
        new_l = self.caculate_lige(l)
        new_ay = self.caculate_Accelerometer(ay)
        if new_l > 2:
            serverMessage = "change oil \nAcid value: " + str(round(new_ay,5)) + " \nlux :" + str(round(new_l,5))
        else:
            serverMessage = "oil is good \nAcid value: " + str(round(new_ay,5)) + " \nlux :" + str(round(new_l,5))
        return serverMessage
    def caculate_lige(self,l):#計算光線酸價[取得的亮度,酸價1,亮度1,酸價2,亮度2]
        l = l.split()
        try:
            lux = float(l[0]) #實際測到之光線
            acid1 = float(l[1]) #設定之調整酸價1
            lux1 = float(l[2]) #調整之光線1
            acid2 = float(l[3]) #設定之調整酸價2
            lux2 = float(l[4]) #調整之光線2
        except:
            l = 0

        new_l = acid2-((lux - lux2)/(lux1-lux2))*(acid2 - acid1)#在此填上光線計算酸價公式
        print(new_l)
        return round(new_l,2)

    def caculate_Accelerometer(self,ay):#計算加速度酸價
        try:
            ay = float(ay)
        except:
            ay = 0
        new_ay = ay * 0.0003 + 2.8681#在此填上加速度計算酸價公式
        return round(new_ay,2)

    def accetp_connet(self):
        while 1:
            try:
                conn, addr = self.server.accept()
                name = conn.recv(1024).decode()
                if name == "s_a":  # sensor_Acceleration
                    print("sensor_Acceleration connect,IP: {}".format(addr))
                    self.sensor_connect[name] = [addr,conn]
                    if self.sensor_connect[name][1] == self.sensor_connect["s_l"][1]:
                        self.sensor_connect["s_l"] = None
                elif name == "s_l":  # sensor_Luminosity
                    print("sensor_Luminosity connect,IP: {}".format(addr))
                    self.sensor_connect[name] = [addr,conn]
                    if self.sensor_connect[name][1] == self.sensor_connect["s_a"][1]:
                        self.sensor_connect["s_a"] = None
                else:
                    print("Accept APP ,IP: {}".format(addr))
                    # conn.sendall("Accept APP".encode())
                    appclient = threading.Thread(target=self.clientThreadIn, args=(conn, addr))
                    appclient.start()
                    self.APP_client.append(conn)
            except:
                pass

server = Server()
