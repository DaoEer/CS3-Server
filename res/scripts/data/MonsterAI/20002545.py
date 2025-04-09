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
                "name": "准备中", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令跳状态2", 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "10086", 
                                    "param1": "20002531"
                                }
                            ], 
                            "id": 1
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "工作中", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "开始计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "kaishi"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [], 
                        "id": 2
                    }, 
                    {
                        "comment": "召唤第一波怪物（暂废）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21814 -33002 3304", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22046 -33416 3299", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21986 -32552 3336", 
                                "param1": "20002539"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22262 -33149 3336", 
                                "param1": "20002537"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22235 -32786 3336", 
                                "param1": "20002537"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20002533"
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
                                "param2": "50", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "召唤第二波怪物（暂废）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 87", 
                                "param2": "8527 -28477 3304", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 87", 
                                "param2": "8791 -28118 3336", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 87", 
                                "param2": "8768 -28887 3309", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 87", 
                                "param2": "8934 -28494 3336", 
                                "param1": "20002539"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 87", 
                                "param2": "9054 -28845 3336", 
                                "param1": "20002537"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 87", 
                                "param2": "9180 -28151 3336", 
                                "param1": "20002537"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "100", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "召唤第三波怪物（暂废）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21814 -33002 3304", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22046 -33416 3299", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21986 -32552 3336", 
                                "param1": "20002539"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22262 -33149 3336", 
                                "param1": "20002537"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22235 -32786 3336", 
                                "param1": "20002537"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20002533"
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "130", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "召唤第四波怪物（含精英）（暂废）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21814 -33002 3304", 
                                "param1": "20002546"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22046 -33416 3299", 
                                "param1": "20002539"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21986 -32552 3336", 
                                "param1": "20002539"
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
                                "param2": "80", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "销毁自己（暂停）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0.5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "180", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "召唤第一波怪物（新）（暂废）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22046 -33416 3299", 
                                "param1": "20002536"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21986 -32552 3336", 
                                "param1": "20002539"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "22235 -32786 3336", 
                                "param1": "20002537"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20002533"
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
                                "param2": "70", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "召唤第四波怪物（含精英）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -176", 
                                "param2": "21814 -33002 3304", 
                                "param1": "20002557"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "80", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 12
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令销毁自己", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0.5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "10088", 
                                    "param1": "20002527"
                                }
                            ], 
                            "id": 10
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
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}