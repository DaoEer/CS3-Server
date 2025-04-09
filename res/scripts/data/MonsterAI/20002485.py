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
                "name": "基础状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "记录时间t1", 
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
                            15, 
                            18, 
                            20
                        ], 
                        "Conditions": [], 
                        "id": 15
                    }, 
                    {
                        "comment": "清除EAI，重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "18"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }
                        ], 
                        "EID": [
                            21, 
                            20
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 21
                    }, 
                    {
                        "comment": "移除加血标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }
                        ], 
                        "EID": [
                            23, 
                            22
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "45", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 23
                    }, 
                    {
                        "comment": "清除EAI，重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "18|20"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "85", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 22
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "接入巡逻路线（上天），记录t2,t5", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "9"
                                }, 
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "0|0", 
                                    "param1": "1"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t2"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t5"
                                }
                            ], 
                            "EID": [
                                8
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2485", 
                                    "param1": ""
                                }
                            ], 
                            "id": 8
                        }, 
                        {
                            "comment": "接入巡逻路线（下地）", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 -90", 
                                    "param2": "-3310 3350 810", 
                                    "param1": "20002492"
                                }
                            ], 
                            "EID": [
                                11
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1870", 
                                    "param1": ""
                                }
                            ], 
                            "id": 11
                        }, 
                        {
                            "comment": "收到指令，销毁自身", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "8"
                                }, 
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0.2"
                                }
                            ], 
                            "EID": [
                                13
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1871", 
                                    "param1": ""
                                }
                            ], 
                            "id": 13
                        }, 
                        {
                            "comment": "怪物喊话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C000077", 
                                    "param1": "50"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t3"
                                }
                            ], 
                            "EID": [
                                14
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "25", 
                                    "param1": "t2"
                                }, 
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "486", 
                                    "param1": ""
                                }
                            ], 
                            "id": 14
                        }, 
                        {
                            "comment": "怪物喊话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C000078", 
                                    "param1": "50"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t4"
                                }
                            ], 
                            "EID": [
                                16
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "25", 
                                    "param1": "t3"
                                }, 
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "487", 
                                    "param1": ""
                                }
                            ], 
                            "id": 16
                        }, 
                        {
                            "comment": "怪物喊话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C000079", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                17
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "25", 
                                    "param1": "t4"
                                }, 
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "488", 
                                    "param1": ""
                                }
                            ], 
                            "id": 17
                        }
                    ], 
                    6: [
                        {
                            "comment": "触发阶段完成", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction59", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "485"
                                }
                            ], 
                            "EID": [
                                12
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }
                            ], 
                            "id": 12
                        }, 
                        {
                            "comment": "血量减少，触发语音", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C000131", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                18, 
                                20
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "id": 18
                        }, 
                        {
                            "comment": "血量增加，触发语音", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C000132", 
                                    "param1": "50"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "22"
                                }
                            ], 
                            "EID": [
                                20, 
                                18
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition54", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "id": 20
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