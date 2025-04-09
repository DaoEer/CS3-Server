# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "副本剩余10秒时触发倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 25, 
                    "param1": "t4", 
                    "param2": "10"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "10秒后下落第一批人参果", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000420", 
                    "param4": "", 
                    "id": 64
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
            "id": 2
        }, 
        {
            "title": "30秒后下落第二批人参果", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000421", 
                    "param4": "", 
                    "id": 64
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t2", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "60秒后下落第三批人参果", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000422", 
                    "param4": "", 
                    "id": 64
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t3", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "副本时间到达，奖励开关拨动", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "已摘取人参果", 
                    "param2": "80135030", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 83
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135030", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "10"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t0", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    3: [
        {
            "title": "进入副本5秒倒计时后副本倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 47
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "60", 
                    "param1": "t3", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "305", 
                    "param1": "t0", 
                    "param4": "", 
                    "id": 12
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
            "title": "生成原色果后通知下落", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 57
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 31, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000420", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "生成金色果后通知下落", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 57
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 31, 
                    "param1": "t2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000421", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "生成绿色果后通知下落", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 57
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 31, 
                    "param1": "t3", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000422", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "生成紫色果后通知下落", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 57
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 31, 
                    "param1": "t4", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000423", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "生成褐色果后通知下落", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 57
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 31, 
                    "param1": "t5", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000424", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    12: [
        {
            "title": "原色果销毁重刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2|2|2|2|2", 
                    "param1": "10000420|10000421|10000422|10000423|10000424", 
                    "param4": "", 
                    "id": 66
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000420", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "金色果销毁重刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3|3|3|3|3", 
                    "param1": "10000420|10000421|10000422|10000423|10000424", 
                    "param4": "", 
                    "id": 66
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000421", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "绿色果销毁重刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20|20|20|20|20", 
                    "param1": "10000420|10000421|10000422|10000423|10000424", 
                    "param4": "", 
                    "id": 66
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000422", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "紫色果销毁重刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10|10|10|10|10", 
                    "param1": "10000420|10000421|10000422", 
                    "param4": "", 
                    "id": 66
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000423", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "褐色果销毁重刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "15|15|15|15|15", 
                    "param1": "10000420|10000421|10000422", 
                    "param4": "", 
                    "id": 66
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000424", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    14: [
        {
            "title": "紫色销毁召唤虫子", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20004396:1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 51
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "worm", 
                    "id": 9, 
                    "param1": "TALK", 
                    "param2": "10000423"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "褐色销毁召唤粘液", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20004397:1", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 51
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "mucus", 
                    "id": 9, 
                    "param1": "TALK", 
                    "param2": "10000424"
                }
            ], 
            "id": 2
        }
    ], 
    17: [
        {
            "title": "摘取不到10个健康人参果副本失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135030", 
                    "param4": "", 
                    "id": 30
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "1", 
                    "param2": "10"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    19: [
        {
            "title": "玩家死亡，副本失败，传出副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}