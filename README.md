# -Oil-quality-inspection-system

運用手機加速度及光線感測器檢測油質。

App
  App_Client.py為可在pc及手機上執行之結果觀測介面。
  還境:
  python 3.7
  kivy
  
  Sensor_Client.py為運用kivy所開發之app，需運用buildozer打包成apk後使用
  還境:
  python 3.7
  kivy
  plyer
  
  Client.py為網路連線client處理之模組，需與App_Client.py及Sensor_Client.py同時使用
  
Server
  Server.py為在server上執行之連線server，接收cilent資訊作處理及回應
  還境:
  python 3.7
  
架構圖
