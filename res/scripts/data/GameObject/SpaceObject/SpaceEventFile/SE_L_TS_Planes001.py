# -*- coding: utf-8 -*-
Datas = {
    7: [
        {
            "title": "BOSS50%血量，刷夸父", 
            "describe": "夸父来也！", 
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
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046060", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 14, 
                    "param1": "20009094", 
                    "param2": "0.51"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "小怪全部死亡，刷boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1|4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "boss死亡喊话", 
            "describe": "可恶，大巫巫尊定会阻止你们.....", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046061", 
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
                    "param1": "20009094", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    30: [
        {
            "title": "第一波小怪喊话结束，通知进入战斗", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20009095|20009096|20009097", 
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
                    "param1": "Q046055", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "BOSS死亡喊话结束，传送出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_TS", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q046061", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "第一波小怪喊话", 
            "describe": "汤山重地，何人敢闯？\n哼！尔等魔道将十金乌的真身藏于此山，休以为能瞒得过我！\n就算知道又如何，这汤山也不是你想闯就能闯的，拿下！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046052|Q046053|Q046055", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "18", 
                    "param3": "5848.410156 -23965.867188 164.067749", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "664.067749|-464.067749"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "第一波小怪死亡&进入某范围，刷跳出场怪", 
            "describe": "", 
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
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "1278.0 -24815.0 1204.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1704|704"
                }
            ], 
            "id": 2
        }
    ]
}