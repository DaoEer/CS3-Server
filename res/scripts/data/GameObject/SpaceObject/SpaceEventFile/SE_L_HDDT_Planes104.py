# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "玩家进入该位面，设置为阶段1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 1
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101550", 
                    "param4": "", 
                    "id": 2
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
            "title": "通知1，播抢夺太虚镜镜头/完成任务目标1", 
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
                    "param1": "627", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20010791|20010792|20010793", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "10", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20010791"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到通知，移除空间动态效果", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "652", 
                    "param4": "", 
                    "id": 208
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "627"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到镜头通知，发送陆吾指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12345607", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "q1", 
                    "param1": "20010791|20010792|20010793", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "99", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "626"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到镜头通知，完成任务", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101550", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010137", 
                    "param4": "", 
                    "id": 43
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "huicheng", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "627"
                }
            ], 
            "id": 4
        }
    ]
}