' GBT小土豆全能开发者 守护进程启动器
' 开机静默启动, 无窗口
CreateObject("Wscript.Shell").Run "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File ""C:\Users\ADMIN\.gbt\gbt-daemon.ps1"" -Silent", 0, False
