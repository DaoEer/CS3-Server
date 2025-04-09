# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "倒计时结束，开启副本计时，语音提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "15", 
                    "param1": "360", 
                    "param4": "", 
                    "id": 97
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "60", 
                    "param1": "tip1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "120", 
                    "param1": "tip2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "180", 
                    "param1": "tip3", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "240", 
                    "param1": "tip4", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "300", 
                    "param1": "tip5", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "340", 
                    "param1": "tip6", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "副本生命结束，提示通关失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 325
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 233
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "end", 
                    "param2": "5"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "LoopQuestLife", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "tp计时到达，销毁光效", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "start", 
                    "param1": "20011091|20011092|20011093|20011094|20011095", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tp", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "tip1到达，五行提示", 
            "describe": "通知画卷在附近刷出法阵光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tip", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "8", 
                    "param1": "tp", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tip1", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "tip2到达，五行提示", 
            "describe": "通知画卷在附近刷出法阵光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tip", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "8", 
                    "param1": "tp", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tip2", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "tip3到达，五行提示", 
            "describe": "通知画卷在附近刷出法阵光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tip", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "8", 
                    "param1": "tp", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tip3", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "tip4到达，五行提示", 
            "describe": "通知画卷在附近刷出法阵光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tip", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "8", 
                    "param1": "tp", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tip4", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "tip5到达，五行提示", 
            "describe": "通知画卷在附近刷出法阵光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tip", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "8", 
                    "param1": "tp", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tip5", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "tip6到达，五行提示", 
            "describe": "通知画卷在附近刷出法阵光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tip", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "tp", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tip6", 
                    "param2": ""
                }
            ], 
            "id": 9
        }
    ], 
    12: [
        {
            "title": "所有分身全部被消灭，且画卷全部为空，设置阶段1完成", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "88", 
                    "param4": "", 
                    "id": 222
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "88", 
                    "param1": "20011090|20011115", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 35, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": "20011231|20011232|20011233|20011234|20011235|20011236|20011237|20011238|20011239|20011240"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20011231|20011232|20011233|20011234|20011235|20011236|20011237|20011238|20011239|20011240", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "登录其他地图复活", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "140379001", 
                    "param4": "", 
                    "id": 16
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到通知1，初始表现", 
            "describe": "刷出法阵与初始表现五行分身", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param1": "jin|mu|shui|huo|tu", 
                    "param4": "", 
                    "id": 111
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "201", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到通知jishu，增加计数", 
            "describe": "刷出法阵与初始表现五行分身", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "m", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "jishu", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "测试收到通知1，初始表现", 
            "describe": "刷出法阵与初始表现五行分身", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "202", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到通知444，销毁陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20011116|20011117|20011118|20011119|20011120", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "444", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到通知jin1，剩余空画卷中选择一个设置为金属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "jin2", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "jin2", 
                    "param1": "20011231", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "jin1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到通知mu1，剩余空画卷中选择一个设置为木属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "mu2", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "mu2", 
                    "param1": "20011232", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "mu1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到通知shui1，剩余空画卷中选择一个设置为水属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "shui2", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "shui2", 
                    "param1": "20011233", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "shui1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到通知huo1，剩余空画卷中选择一个设置为火属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "huo2", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "huo2", 
                    "param1": "20011234", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "huo1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "收到通知tu1，剩余空画卷中选择一个设置为土属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tu2", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "tu2", 
                    "param1": "20011235", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "tu1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "蜃妖死亡计数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "889", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "收到通知jin3，剩余空画卷中选择一个设置为金属性", 
            "describe": "通知选中画卷创建傀儡", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "jin4", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "jin4", 
                    "param1": "20011610", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "jin3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "收到通知mu3，剩余空画卷中选择一个设置为木属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "mu4", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "mu4", 
                    "param1": "20011611", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "mu3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "收到通知shui3，剩余空画卷中选择一个设置为水属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "shui4", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "shui4", 
                    "param1": "20011612", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "shui3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到通知huo3，剩余空画卷中选择一个设置为火属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "huo4", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "huo4", 
                    "param1": "20011613", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "huo3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到通知tu3，剩余空画卷中选择一个设置为土属性", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "tu4", 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param4": "", 
                    "id": 112
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "tu4", 
                    "param1": "20011614", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 34, 
                    "param1": "20011106|20011107|20011108|20011109|20011110|20011111|20011112|20011113", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "tu3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "蜃妖金死亡计数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "end", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "101", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "蜃妖木死亡计数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "end", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "102", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "蜃妖水死亡计数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "end", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "103", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "蜃妖火死亡计数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "end", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "104", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 19
        }, 
        {
            "title": "蜃妖土死亡计数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "end", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "105", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 20
        }, 
        {
            "title": "点击退出按钮，玩家未完成任务时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 334
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "end", 
                    "param2": "5"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "SignOut", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 21
        }, 
        {
            "title": "开始属性界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 233
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "UI", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 22
        }
    ], 
    16: [
        {
            "title": "m=5,通知荷花法阵开始切换阵法", 
            "describe": "出场表演蜃妖全部归位画卷", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "start", 
                    "param1": "20011090|20011091|20011092|20011093|20011094|20011095", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "m", 
                    "param2": "5"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "k=1,界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000583", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k", 
                    "param2": "1"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "k=2,界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000654", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k", 
                    "param2": "2"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "k=3,界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000584", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k", 
                    "param2": "3"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "k=4,界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000655", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k", 
                    "param2": "4"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "任务完成，结算", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000425", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "88", 
                    "param4": "", 
                    "id": 222
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "88", 
                    "param1": "20011090|20011115", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20011116|20011117|20011118|20011119|20011120|20011231|20011232|20011233|20011234|20011235", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14022101|14022102|14022201|14022202|14022301|14022302|14022401|14022402|14022501|14022502", 
                    "param1": "20011090", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "10", 
                    "param2": "副本通关时间为：", 
                    "param1": "80135057", 
                    "param4": "", 
                    "id": 331
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135057", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "667", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "140379001", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 233
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "end", 
                    "param2": "5"
                }
            ], 
            "id": 6
        }
    ], 
    19: [
        {
            "title": "玩家死亡，任务失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 325
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 233
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入副本，开始倒计时10秒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135057", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "end", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000708|Cy000577|Cy000578", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}