# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "第一波怪死亡，第一个阵眼复苏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12", 
                    "param1": "20008863", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第一个阵眼死亡，第二波怪复苏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "13", 
                    "param1": "20008864", 
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
            "id": 2
        }, 
        {
            "title": "第二波怪死亡，第二个阵眼复苏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14", 
                    "param1": "20008865", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "boss死亡，死亡喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042600", 
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
                    "param1": "20008866", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    14: [
        {
            "title": "重复刷火墙", 
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
                    "id": 6, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008861"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到diyibo，第一波小怪喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042593", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "diyibo", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "走到离火大阵前，旁白提示", 
            "describe": "此离火大阵有两处阵眼，需要依次摧毁方可破阵！\n守卫乃阵眼灵力所化，需要消灭守卫方可摧毁阵眼！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042591|Q042592", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "123", 
                    "param1": "20009557|20009558|20009559|20009560|20009561|20009562|20009563|20009564|20009565|20009566|20009567|20009568|20009569|20009570|20009571|20009572|20009573|20009574|20009575|20009576", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "6", 
                    "param3": "-11113.0 6822.0 352.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5352|-4650"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "启动陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "123", 
                    "param1": "20009557|20009558|20009559|20009560|20009561|20009562|20009563|20009564|20009565|20009566|20009567|20009568|20009569|20009570|20009571|20009572|20009573|20009574|20009575|20009576", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "-1260.0 5950.0 304.4", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5304|-4700"
                }
            ], 
            "id": 2
        }
    ], 
    18: [
        {
            "title": "获得蟠虬之胆，完成任务喊话/刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042601|Q045660", 
                    "param4": "", 
                    "id": 19
                }, 
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
                    "id": 41, 
                    "param1": "301010115", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "进入副本，旁白提示", 
            "describe": "蟠龙道机关密布，请小心躲避！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042590", 
                    "param4": "", 
                    "id": 18
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    28: [
        {
            "title": "阶段1完成，销毁火墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20008861", 
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
                    "id": 43, 
                    "param1": "1", 
                    "param2": "2"
                }
            ], 
            "id": 1
        }
    ]
}