# -*- coding: utf-8 -*-
Datas = {
    30: [
        {
            "title": "天尘子投降喊话结束，刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
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
                    "id": 52, 
                    "param1": "Q046024", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "开场喊话结束，刷傀儡/通知天尘子换动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20009619", 
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
                    "param1": "Q046014", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    5: [
        {
            "title": "傀儡死亡，天尘子移除不可见，投降喊话，刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20009619", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4", 
                    "param1": "20102128", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4", 
                    "param1": "20102132", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046017|Q046018|Q046019|Q046021|Q046022|Q046024", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.29999995232, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20009623", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20009619", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "石壁A死亡，移除无敌buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11046801", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009621", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "石壁B死亡，移除无敌buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11046801", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009622", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "刷A组石壁躲大招,4秒后销毁", 
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
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "20009621", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046016", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "shibiA", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009620"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "刷A组石壁躲大招,4秒后销毁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "20009622", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046016", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "shibiB", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009620"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "大招释放完毕，石壁死亡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20009621|20009622", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "xiaohui", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009620"
                }
            ], 
            "id": 3
        }
    ], 
    21: [
        {
            "title": "刷新天尘子、喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046013|Q046014", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}