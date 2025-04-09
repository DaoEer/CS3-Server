# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "进入副本开始预备倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "t0", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
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
            "title": "预备倒计时结束，传出副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14000101", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }
            ], 
            "spaceConditions": [], 
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
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14000101", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "进入范围触发竞速倒计时且取消t0", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 47
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t0", 
                    "param4": "", 
                    "id": 13
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
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "3", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14000101", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "-18555.123047 110935.125 3044.050537", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "8000|-2000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入加时区域续秒1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 48
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "7079.996094 119370.070313 3050.037109", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "8000|-2000"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "进入加时区域续秒2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 48
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "21961.578125 92182.625 -949.876953", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5000|-5000"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "进入加时区域续秒3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 48
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "39924.890625 74224.296875 -4540.176758", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|-10000"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "进入加时区域续秒4", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 48
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "71170.101563 69020.03125 -4549.935059", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|-10000"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "进入加时区域续秒5", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 48
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "106458.414063 63898.414063 -4968.225586", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "0|-10000"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "到达终点，10秒后传出副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14000101", 
                    "param4": "", 
                    "id": 26
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
                    "param1": "10", 
                    "param4": "", 
                    "id": 48
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "60120030", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "69929.984375 24639.957031 -7349.970215", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "0|-12000"
                }
            ], 
            "id": 7
        }
    ]
}