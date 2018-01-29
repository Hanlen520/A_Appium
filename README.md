# A_Appium（Building...）
[![codebeat badge](https://codebeat.co/badges/7ee7d536-3c4a-413e-b9cb-cd42de40dde1)](https://codebeat.co/projects/github-com-williamfzc-a_appium-master)

**Android_Appium or A-level Appium**

提供便于用例/API及整体测试流程管理的Android测试框架

## 设计目的 ##

- 让人员得到有效分工
- 方便地部署到实际工作中
- 跨平台，有良好扩展性
- 多设备支持

## 自动化展望

- 一个完整的自动化测试系统应该包含三个主要部分
    - 提供前端给测试工程师用于输入，用于选择待测试的用例
    - 逻辑处理，即该系统做的事情，包括了测试的主流程与报告的输出
    - 展示测试结果，能够处理测试报告并提供更好的可视化
    
- 这套系统最佳实践应该部署在服务器上，提供网页给用户交互与展示。
    - 在前端选择需要执行的用例，向服务器发送任务（0%）
    - 服务器对任务拆包、测试并输出.rst格式结果（80%）
    - 用sphinx或其他方法将结果嵌入到网页中展示、导出（80%）

## 设计架构 ##

### 执行流程

- 在conf.py中配置机器与其他参数
- 在run.py中选择待测用例
- 执行run.py

### appium的原理 ###

appium遵从C/S模型：
1. 调用appium client封装的driver对象的方法组成用例
1. appium client传送指令给appium server
1. appium server对设备进行实际操作

### 定位 ###

- 框架层应该集中于如何更好地规划流程与优化策略而不是底层实现 
- 这个框架将着重于扩展appium client

## 架构 ##

### 功能结构 ###

- 构建Driver
    - 初始化设备
    - 初始化server
    - 绑定设备与端口
    - 返回Driver实例
    
- 用例管理
    
    - 一个case分配的例子
        - 不同设备类型
        - 不同版本
        - 不同APP
            - 控件管理（JSON or DB）
            - API（PageObject）
            - Case
            - API封装控件与操作，Case完全由API组合
        
- 用例执行
    - conf.py中配置设备队列
    - 初始化设备队列，device/driver/server进行绑定
    - 根据用例所属类型分配设备
    - case中操作设备进行测试
    
### 执行 ###

- AppiumClient
	- device_list（Device）
		- server
		- adb
		- driver（from selenium）
	- TestCaseObject
		- load case info
		- load device_list
		- load report builder
	- AppiumCase   
		- load TestCaseObject
		- get exact appium case content
		- run 
	- ReportGenerator
		- build .rst result file
	- HtmlBuilder
		- use sphinx
		- transform .rst into html page


## 文件结构 ##

- appium_client  
    - appium
        - 原有appium_client包
    - appium_server.py
        - 用于管理后台的server进程
    - appium_client.py
        - appium客户端类，与server通信
    - device包
        - device.py 
            - device对象，包含了设备的相关信息
        - adb.py 
            - adb操作类
    - report_generator包
        - 根据result结果生成.rst文件
    - appium_case.py
        - 测试用例单元
    - console_utils.py
        - 泛用性较强的函数们
- result
    - 测试结果会被保存在这里
    - 测试结果文件夹命名为时间+机型id
    - 包含：
        - 错误截图
        - anrlog
        - 测试报告（htmltestrunner生成）
        - 控制台上的log
        - 手机log（MTK/QC等）
- html_builder
    - html报告制作包, 基于sphinx
- case
    - 测试用例的位置
    - 根据自己需要创建文件夹结构
    - 在conf.py中进行配置
- api
    - 测试用例需要使用的api位置
    - 根据自己需要创建文件夹结构
    - 在conf.py中进行配置
- conf.py
    - 全局配置
- run.py
    - 测试入口
    
## 分工 ##

工程师应该被划分为三种类型。

- 面向case
    - 设计/编写/维护case
    - 着重于设计合适的自动化测试用例
    - 传统的测试工程师
    
- 面向API
    - 针对需要，设计/编写/维护合适的API
    - 对API进行恰当的分类管理
    - 有一定代码基础的测试工程师

- 面向底层
    - 优化/维护appium_client中的内容
    - 在保证client/server的关联性的情况下维持系统的稳定和效率
    - 软件工程师
