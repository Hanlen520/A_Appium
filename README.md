# A_Appium（Building...）

**Android_Appium or A-level Appium**

提供便于用例/API及整体测试流程管理的Android测试框架

## 设计目的 ##

- 让人员得到有效分工
- 方便地部署到实际工作中
- 跨平台，有良好扩展性
- 多设备支持

## 设计架构 ##

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
    - 不同设备类型
    - 不同版本
    - 不同APP
        - 控件管理（JSON or DB）
        - API（PageObject）
        - Case
        - API封装控件与操作，Case完全由API组合
        
- 用例执行
    - unittest为单位
    - HTMLTestRunner运行，并打印报告
    
## 文件结构 ##

- appium_client  
    - 原有appium_client包
    - appium_server.py用于管理后台的server进程
    - 构建driver对象需要的其他
- result
    - 测试结果会被保存在这里
- case
    - 测试用例的位置
- api
    - 测试用例需要使用的api位置
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