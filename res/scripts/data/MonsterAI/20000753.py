# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {
            1: {
                "name": "救援道场—位面围殴（战斗远程）", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录t2/k1/重新设置出生点", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction50", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "-31355 -48530 15312"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "k1"
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "2%的血量保护", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "t2=5，攻击所有人", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000190|20000191|20000192|20000193|20000748|20000749|20000109", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "5", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "围殴用远程普攻——冰", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100114001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100114001"
                            }
                        ], 
                        "id": 13
                    }
                ], 
                "eventsAI": {
                    5: [
                        {
                            "comment": "攻击离自己最近的敌人", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction54", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 23
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "救援道场—20000753", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "存在k1，改变朝向/通知副本6", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction53", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "6"
                            }
                        ], 
                        "EID": [
                            22
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "k1"
                            }
                        ], 
                        "id": 22
                    }, 
                    {
                        "comment": "攻击20000190", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000190", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000190", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 1
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {
            1: {
                "name": "名字设置", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "有炫火，名字设置为修罗殿弟子", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction78", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "修罗殿弟子"
                            }
                        ], 
                        "EID": [
                            24
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000194", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "有问天，名字设置为逍遥门弟子", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction78", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "逍遥门弟子"
                            }
                        ], 
                        "EID": [
                            25
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000793", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 25
                    }, 
                    {
                        "comment": "有无霜，名字设置为缥缈阁弟子", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction78", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "缥缈阁弟子"
                            }
                        ], 
                        "EID": [
                            26
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000782", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 26
                    }, 
                    {
                        "comment": "有悟道，名字设置为摩诃殿弟子", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction78", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "摩诃殿弟子"
                            }
                        ], 
                        "EID": [
                            27
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000783", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 27
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }
}