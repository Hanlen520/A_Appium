# A_Appium（Building...）
[![codebeat badge](https://codebeat.co/badges/7ee7d536-3c4a-413e-b9cb-cd42de40dde1)](https://codebeat.co/projects/github-com-williamfzc-a_appium-master)

**Android_Appium or A-level Appium**

提供便于用例/API及整体测试流程管理的Android测试框架

## 设计目的 ##

- 让人员得到有效分工
- 方便地部署到实际工作中
- 跨平台，有良好扩展性
- 多设备支持

## 自动化测试框架思想

以下几种思想是前人总结的在自动化框架设计上公认比较优秀的思想：

- 模块化思想
- 数据驱动思想
- 关键字驱动思想

### 模块化

将用例中几个不同的测试点拆分，将单个点的测试步骤进行封装，成为一个模块。这里的模块是比较广义的，如果以手机为测试单位，那么每个APP将被对应一个模块；如果以APP为测试单位，模块将变成一个页面，以此类推。

除此之外，模块化是多层次的。很多时候，几个测试用例会共享类似的测试步骤，但可能又有些许的不同。我们要达到最高效的管理，那么我们还可以在原有模块上进行再次模块化（如将小步骤封装为API）。

关于模块化的颗粒度粗细，应该结合实际情况考虑而不应遵照固定形式。

### 数据驱动

- 强调外部数据源的存在，而不是静态的数据。
- 参数化，高度的参数化。
- 不同的数据导致不同结果的产生。
- 可以有效减少内部代码的改动，提高稳定性。

### 关键字

实际上就是一种高度的面向对象（再做了一层封装），用特定的关键字来对应部分行为，用更少的代码更形象地描述更多事情。

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

appium遵从C/S模型，实际上它本身就是个HTTPServer。测试流程如下：

1. 调用appium client封装的方法编写用例脚本
1. 运行脚本，传送HTTP指令给appium server
1. appium server构建会话，根据desired_cap为会话创建对应的driver（android/ios等），建立长连接
1. 根据client发来的HTTP请求通过driver发给设备
1. 设备解析命令（如android会解析成uiautomator命令），并执行，完成后返回结果


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
	- device_list
	    - 由一系列Device对象构成
	- Device
		- server
		- adb
		- driver（from selenium）
	- TestCaseObject（大部分是文本数据，没有实际动作）
		- 选定机型id
		- 用例模块名
		- 载入用例的内容（类）
	- AppiumCase   
		- 读入TestCaseObject
		    - 根据机型id从device_list读入对应Device对象
		    - 载入用例对象
		- 绑定报告生成器
		- 暴露run方法以便在其他地方运行 
	- ReportGenerator
		- 根据case的结果生成一系列.rst文件
	- HtmlBuilder
		- 基于sphinx引擎
		- 将.rst文件编译成html包


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
