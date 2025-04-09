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
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "召唤环绕金币", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20005935", 
                                "param4": "10", 
                                "param3": "1", 
                                "param2": "30", 
                                "param1": "22670 27039 300"
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
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "jinbi1=3时，扔金币", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "6|30|20005936", 
                                "param4": "25|3", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "22670 27039 300"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "jinbi1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "jinbi1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "jinbi1"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "记录标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "jinbi1"
                            }, 
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
                            3
                        ], 
                        "Conditions": [], 
                        "id": 3
                    }, 
                    {
                        "comment": "召唤第一波", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20005935", 
                                "param4": "10", 
                                "param3": "1", 
                                "param2": "30", 
                                "param1": "22670 27039 300"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "6|30|20005936", 
                                "param4": "25|3", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "22670 27039 300"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [], 
                        "id": 4
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