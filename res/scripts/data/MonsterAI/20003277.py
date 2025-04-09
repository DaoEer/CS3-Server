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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录时间", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "2秒3米内召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "1", 
                                "param3": "0", 
                                "param2": "3", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "6秒5米内召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "1", 
                                "param3": "1", 
                                "param2": "5", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "6", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "10秒7米内召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "1", 
                                "param3": "0", 
                                "param2": "7", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "14秒3米内召唤2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "1", 
                                "param3": "1", 
                                "param2": "3", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "14", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "18秒5米内召唤2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "1", 
                                "param3": "0", 
                                "param2": "5", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "18", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "22秒7米内召唤2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "1", 
                                "param3": "1", 
                                "param2": "3", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "22", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "26秒10米内召唤，然后重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20003276", 
                                "param4": "2", 
                                "param3": "0", 
                                "param2": "10", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|3|4|5|6|7"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "26", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "60米内没有玩家，调整休整状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "60"
                            }
                        ], 
                        "id": 10
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "休整状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "60米内玩家进入，跳回自由状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "60"
                            }
                        ], 
                        "id": 9
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}