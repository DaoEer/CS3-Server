# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "初始化计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "300", 
                    "param1": "time", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "0", 
                    "param2": "600", 
                    "param1": "time1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "290", 
                    "param1": "time123", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 48
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    2: [
        {
            "title": "计时到达", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "3013", 
                    "param1": "3012", 
                    "param4": "", 
                    "id": 446
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 467
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20014196", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 1
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "销毁防御器械", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40001006|40001007|40001008|40001009|40001010|40001011|40001012", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time1", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "时间到达，防守方获胜", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3013", 
                    "param4": "", 
                    "id": 222
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time12", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "开启战斗", 
            "describe": "倒计时开启，增加副本时间", 
            "actions": [
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5962", 
                    "param4": "", 
                    "id": 127
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
                    "param3": "", 
                    "param2": "", 
                    "param1": "1800", 
                    "param4": "", 
                    "id": 48
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "1795", 
                    "param1": "time12", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "90", 
                    "param1": "time1234", 
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
                    "param1": "time123", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "时间到达，重复检测副本内人数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3013", 
                    "param1": "3012", 
                    "param4": "", 
                    "id": 446
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time1234", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    3: [
        {
            "title": "开启副本道具栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 119
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "给道具", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "303010051", 
                    "param4": "", 
                    "id": 468
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 73, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    13: [
        {
            "title": "关闭副本道具栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 120
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "303010051|302010084|302010085|302010086|302010087|302010088|302010089|302010090|302010091", 
                    "param4": "", 
                    "id": 23
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12261201", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "进攻方胜利", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 429
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "2-2|3-3|4-4|5-5", 
                    "param2": "300601001|300601001|300601001|300601001", 
                    "param1": "300601002|300601003|300601004|300601005", 
                    "param4": "", 
                    "id": 466
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "C001942", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "C001943", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "", 
                    "param1": "5639", 
                    "param4": "", 
                    "id": 451
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "", 
                    "param1": "5640", 
                    "param4": "", 
                    "id": 451
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 467
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 448
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3012", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "防守方胜利", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 429
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "C001944", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "C001945", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "", 
                    "param1": "5847", 
                    "param4": "", 
                    "id": 451
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "", 
                    "param1": "5848", 
                    "param4": "", 
                    "id": 451
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "2-2|3-3|4-4|5-5", 
                    "param2": "300601001|300601001|300601001|300601001", 
                    "param1": "300601002|300601003|300601004|300601005", 
                    "param4": "", 
                    "id": 466
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 467
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 448
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3013", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "西庭兵营被占领", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "C001935", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "C001936", 
                    "param4": "", 
                    "id": 452
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3001", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "中庭兵营被占领", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "C001937", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "C001938", 
                    "param4": "", 
                    "id": 452
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3002", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "东庭兵营被占领", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "C001939", 
                    "param4": "", 
                    "id": 452
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "C001940", 
                    "param4": "", 
                    "id": 452
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3003", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    17: [
        {
            "title": "玩家离开副本，检查剩余人数", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3013", 
                    "param1": "3012", 
                    "param4": "", 
                    "id": 446
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "time1234", 
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
            "title": "玩家进入副本，触发语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "C001934", 
                    "param1": "C001918", 
                    "param4": "", 
                    "id": 459
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5861", 
                    "param4": "", 
                    "id": 460
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12261201", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    23: [
        {
            "title": "玩家死亡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "80", 
                    "param4": "", 
                    "id": 391
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    25: [
        {
            "title": "小兵死亡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "80", 
                    "param4": "", 
                    "id": 390
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}