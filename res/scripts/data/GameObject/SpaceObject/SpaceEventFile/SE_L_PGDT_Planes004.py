# -*- coding: utf-8 -*-
Datas = {
    14: [
        {
            "title": "收到镜头发送99", 
            "describe": "通知Monster开始战斗", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "q1", 
                    "param1": "20010694|20010695|20010696", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12345607", 
                    "param4": "", 
                    "id": 26
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
                    "param2": "552"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到陆吾发送指令播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000553", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20010694|20010695|20010696", 
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
                    "param2": "20010694"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到553镜头的12345，关闭空间动态效果", 
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
                    "param2": "553"
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
                    "param2": "", 
                    "param1": "301010001", 
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
                    "param2": "553"
                }
            ], 
            "id": 4
        }
    ]
}