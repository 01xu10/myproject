# Appium

###1.**adb命令建立连接**

- 找到夜神所在目录，在夜神模拟器安装路径下的bin目录下执行cmd进入终端

- 输入 adb devices后，出现提示

  ```
  List of devices attached
  
  \* daemon not running; starting now at tcp:5037
  
  \* daemon started successfully
  ```

- 再输入 nox_adb.exe connect 127.0.0.1:62025后，出现提示

  ```
  connected to 127.0.0.1:62025
  ```

- 最后再次输入adb devices后，出现提示

  ```
  List of devices attached
  127.0.0.1:62001 device
  ```

  ![1625044838448](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625044838448.png)

### 2.**开启Appium并配置运行**

​	获取app包名和进程名

- 打开appium

  ![1625046360731](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625046360731.png)

  选择搜索

  ![1625046400395](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625046400395.png)

- 配置参数

  - platformName 系统名 eg: Android
- platformVersion 系统版本  eg: 7.1.2
  - deviceName 手机型号  eg: TAS-AN00
- appPackage app的包名  eg: com.ss.android.ugc.aweme
  - appActivity app的进程名  eg: .main.MainActivity

  ![1625048024055](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625048024055.png)

- 获取模拟设备的型号


- - 打开设置——关于平板电脑
  - 查看型号，获取模拟设备的型号

- ![1625046796254](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625046796254.png)

- 获取app包名称 以及 app进程名


- - 打开模拟器中的抖音短视频app
  - 在adb连接正确的情况下，在夜神模拟器安装目录的bin目录下的cmd中输入adb shell
  - 进入adb shell后输入 dumpsys activity | grep mFocusedActivity
  - com.ss.android.ugc.aweme就是app包名
  - .main.MainActivity就是进程名 注意前边有个点.

- ![1625047764941](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625047764941.png)

- 填好之后,关闭抖音APP，点击Start Session，恭喜你，连接成功

![1625048443526](C:\Users\Boss\AppData\Roaming\Typora\typora-user-images\1625048443526.png)

![img](E:\my_notes\weixinobU7VjnzCuiD_JrPLZvtqwvOLIcA\adaf2cab5bc64d39af6f8c3079ae1eca\b9法.jpeg)















