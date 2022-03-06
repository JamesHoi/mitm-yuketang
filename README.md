# mitm-yuketang
雨课堂刷题助手

## 介绍
本项目仅用于技术交流使用，使用软件后果由使用者承担！！！  
打开软件后再打开雨课堂习题界面，程序即开始自动完成，刷新网页后即可见到效果  
v2.0新增功能，可同时打开多个习题网页，程序会按打开顺序依次进行  
（目前只支持单选题、多选题、和部分判断题）  

## 教程
直接下载软件请前往[Release](https://github.com/JamesHoi/mitm-yuketang/releases)  
第一次使用此软件先双击打开gen_cert.exe  
点击后在同目录下会出现mitmproxy-ca.p12文件，双击他  
1. 存储位置随便选，按下一步  
![image](https://user-images.githubusercontent.com/33508232/156934781-ba2e66de-72c9-4d0a-9d8b-ebbb7eab25ad.png)

2. 下一步（貌似win11才有这步）  
![image](https://user-images.githubusercontent.com/33508232/156934850-5151ac8e-2b61-4b7c-855e-af44c209fa95.png)

3. 密码留空，直接按下一步  
![image](https://user-images.githubusercontent.com/33508232/156934931-be9fec21-a4ac-437b-9cf7-4a942c17c78c.png)

4. 选择“将所有的证书都放入下列存储”，接着选择“受信任的根证书颁发机构”  
![image](https://user-images.githubusercontent.com/33508232/156934966-89557595-143f-4c25-91f5-ceae40b2e4c0.png)

5. 最后，弹出警告窗口，直接点击“是”  （win11没有这一步）  
若不清楚可以参考[网站](https://www.jianshu.com/p/036e5057f0b9) 当中的 三、mitmproxy证书配置  
  
以上步骤只需做一次，使用时直接打开mitm-yuketang.exe即可  
完成后打开软件即可，关闭软件请按Ctrl+C ！！！！！！！！！  
若不小心直接关闭软件了可能会导致无法上网的问题，请双击文件 关闭代理.reg，即可重新上网  

## 细节
### 正常代理模式  
![image](https://user-images.githubusercontent.com/33508232/156936637-e063e037-78e9-4a8c-bf6f-f5c066112407.png)  
### 二级代理模式  
![image](https://user-images.githubusercontent.com/33508232/156936630-d48abde0-6e44-4cf0-a130-365fc3257116.png)  
由于mitmproxy库速度不行，就利用另一个进程运行二级代理帮助提速，个人认为实际理论上应当是更慢  
测试的时候若不用二级代理，网页会卡住，加上后效果很好  
### 透明代理模式
![image](https://user-images.githubusercontent.com/33508232/156936977-c237bcc8-2c2e-49a4-badf-ef9036910a43.png)  
透明代理理论上做了缓存，测试结果确实更慢了  

## 版本更新
### v1.0
完成基本功能
### v2.0
新增生成证书功能
新增队列、前置代理功能  
自动计算出最大线程数
