# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "时间到达，法宝碎片计数小于2，副本失败，玩家退出副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "122", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005710|20005711|20005712|30000259|40000096", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000348", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "1", 
                    "param2": "2"
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
            "id": 1
        }, 
        {
            "title": "时间到达，法宝碎片计数大于等于2，副本通关，玩家退出副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "122", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005710|20005711|20005712|30000259|40000096", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000247", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "收集的法宝碎片数量：", 
                    "param2": "60120003", 
                    "param1": "1", 
                    "param4": "10", 
                    "id": 425
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
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "2"
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
        }
    ], 
    9: [
        {
            "title": "副本通关完成任务目标", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "60120003", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 136
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    10: [
        {
            "title": "副本失败重置任务目标", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "60120003", 
                    "param4": "", 
                    "id": 30
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 136
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    12: [
        {
            "title": "法宝碎片再次刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "22|23|24|25|26|27|28|29|30|31|32|33", 
                    "param4": "", 
                    "id": 126
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "30000259", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "能量球再次刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20", 
                    "param4": "", 
                    "id": 135
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000096", 
                    "param2": ""
                }
            ], 
            "id": 2
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
                    "param3": "", 
                    "id": 27, 
                    "param1": "1", 
                    "param2": "2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "SignOut", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "点击退出按钮，玩家完成任务时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 334
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "SignOut", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    16: [
        {
            "title": "法宝碎片计数改变,给副本发送通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 93
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 19, 
                    "param1": "suipian", 
                    "param2": "0"
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "玩家离开时，任务完成，增加任务物品", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "60120003", 
                    "param4": "", 
                    "id": 15
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "玩家离开时，清除副本信息", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 136
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    19: [
        {
            "title": "死亡退出副本，任务重置", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "60120003", 
                    "param4": "", 
                    "id": 30
                }, 
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
            "title": "刷新法宝碎片//设置能量条", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30000259", 
                    "param1": "22|23|24|25|26|27|28|29|30|31|32|33", 
                    "param4": "", 
                    "id": 104
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "100", 
                    "param4": "", 
                    "id": 103
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000245", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30000259", 
                    "param1": "22|23|24|25|26|27|28|29|30|31|32|33", 
                    "param4": "", 
                    "id": 104
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "3|3|3", 
                    "param1": "0;1;2;3;4;5;6|7;8;9;10;11;12;13|14;15;16;17;18;19;20", 
                    "param4": "", 
                    "id": 135
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "23000103", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 137
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "30000259", 
                    "param1": "22|23|24|25|26|27|28|29|30|31|32|33", 
                    "param4": "", 
                    "id": 104
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "30000259", 
                    "param1": "22|23|24|25|26|27|28|29|30|31|32|33", 
                    "param4": "", 
                    "id": 104
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "初始语音结束，倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000246", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "15", 
                    "param1": "300", 
                    "param4": "", 
                    "id": 97
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 2.0, 
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
                    "param3": "", 
                    "id": 52, 
                    "param1": "Cy000245", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}