# -*- coding: utf-8 -*-
Datas = {
    7: [
        {
            "title": "玉鼎真人血量低于30%通知句芒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "99", 
                    "param1": "20009940", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20009947", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009946", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 14, 
                    "param1": "20009962", 
                    "param2": "0.35"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    27: [
        {
            "title": "刷第一波跳怪", 
            "describe": "玩家离开复活点，刷跳怪", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "8", 
                    "param3": "-10052.0 -5934.0 1764.9", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "6000|-4000"
                }
            ], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "门口小兵死亡，可以取消炮台无敌", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20009934|20009935", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "6|7", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "炮台死亡，销毁门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009938", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "4|5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "袭击的第一波小怪死亡通知刷怪陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "200", 
                    "param1": "20009941|20009942|20009943|20009944|20009945", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20009947", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009948|20009949|20009950|20009951|20009952|20009953|20009954", 
                    "param2": "1|1|1|1|1|1|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "袭击第二波小怪，死亡刷玉鼎真人", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "20009962:1", 
                    "param2": "0 0 -3", 
                    "param1": "22312 -5918 3235", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20009947", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009955|20009956|20009957|20009958|20009959|20009960|20009961", 
                    "param2": "1|1|1|1|1|1|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }
    ], 
    14: [
        {
            "title": "收到BOSS通知，刷句芒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
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
                    "param2": "20009939"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到句芒，召唤魔鼎", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
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
                    "param3": "20", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009940"
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "第三波暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2254 -4274|492 -7533|3579 -9255|5430 -5814", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "8000|-3000"
                }
            ], 
            "id": 1
        }
    ]
}