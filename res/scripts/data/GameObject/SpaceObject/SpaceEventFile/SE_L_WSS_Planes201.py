# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "五分钟计时到达，通知虎蛟", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000325", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20005674", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_WSS", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
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
            "id": 1
        }, 
        {
            "title": "倒计时结束，开启副本计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "300", 
                    "param4": "", 
                    "id": 97
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tt1", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    3: [
        {
            "title": "玩家进入位面，发送指令给虎蛟", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "1111", 
                    "param1": "20005674", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000307", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    6: [
        {
            "title": "三叉戟数量为3，发送相关指令，见说明", 
            "describe": "发送指令100给三叉戟\\发送101指令给虎蛟", 
            "actions": [
                {
                    "delayTime": 12.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20005676", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 13.0, 
                    "param3": "", 
                    "param2": "101", 
                    "param1": "20005674", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20005676", 
                    "param2": "3"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "挑战虎蛟阶段完成，完成任务目标", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000328", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "10", 
                    "param2": "副本通关时间为：", 
                    "param1": "60120001", 
                    "param4": "", 
                    "id": 426
                }, 
                {
                    "delayTime": 20.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_WSS", 
                    "param4": "", 
                    "id": 20
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "60120001", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "离开位面复活", 
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
            "title": "收到虎蛟通知，刷五行阵纹\\倒计时5秒显示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "9", 
                    "param1": "tt1", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005674"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到虎蛟通知，播放语音，销毁存货的雷霆护法与三叉戟", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000327", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005675|20005676", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005674"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到雷霆护法通知201，清除玩家身上电涌buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14011613", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "201", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005675"
                }
            ], 
            "id": 3
        }
    ], 
    19: [
        {
            "title": "挑战时间内玩家死亡，播放失败提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000325", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_WSS", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入位面，发送指令给虎蛟", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1111", 
                    "param1": "20005674", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "300", 
                    "param1": "kb", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 47
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}