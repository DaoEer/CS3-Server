# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "5批怪死亡，刷7批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "7批怪死亡，刷9批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "9", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "7", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "13波怪死亡，发通知111", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20006043|20006040", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "13", 
                    "param2": "20006046:1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "14波怪死亡，发通知222", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20006041|20006043", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "14", 
                    "param2": "20006046:1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }, 
        {
            "title": "15波怪死亡，发通知333", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "333", 
                    "param1": "20006044|20006043", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "15", 
                    "param2": "20006046:1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 5
        }, 
        {
            "title": "16波怪死亡，发通知444", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20006045|20006043", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "16", 
                    "param2": "20006046:1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 6
        }, 
        {
            "title": "BOSS死亡，死亡喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045703", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20006043", 
                    "param2": ""
                }
            ], 
            "id": 7
        }
    ], 
    8: [
        {
            "title": "阶段1完成，刷新精英+小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
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
        }, 
        {
            "title": "阶段2完成，刷新BOSS", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "第三阶段完成，完成任务", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041240", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102554", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102627", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102555", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "收到通知1，刷新第13波怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "13", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041984", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "101", 
                    "param1": "20006040", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "102", 
                    "param1": "20006040", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006043"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到通知2，刷新第14波怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "101", 
                    "param1": "20006041", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "102", 
                    "param1": "20006041", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006043"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到通知3，刷新第15波怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "101", 
                    "param1": "20006044", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "102", 
                    "param1": "20006044", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006043"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到通知4，刷新第16波怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "16", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "101", 
                    "param1": "20006045", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "102", 
                    "param1": "20006045", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006043"
                }
            ], 
            "id": 4
        }
    ], 
    15: [
        {
            "title": "玩家到达某位置，通知第一波怪出场", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20006015|20006016|20006017|20006018|20006019|20006020", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "10510.831055 10149.168945 88.375732", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "588|-588"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家到达某位置，第一波小怪喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045693|Q045694|Q045696", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "10510.831055 10149.168945 88.375732", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "588|-588"
                }
            ], 
            "id": 2
        }
    ], 
    18: [
        {
            "title": "获得噬日精魄，刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "19", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "301010100", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "第一波小怪喊话结束，通知小怪进战", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20006015|20006016|20006017|20006018|20006019|20006020", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q045696", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "精英喊话结束，通知小怪进战", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20006023|20006024|20006025|20006026|20006027|20006042", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q045697", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ]
}