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
                        "comment": "c1时间标记", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "c1"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "c1到4s招怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "17310 -23598 7514", 
                                "param1": "20009391"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "19647 -27238 7535", 
                                "param1": "20009392"
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
                                "param2": "4", 
                                "param1": "c1"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "c1到6s招怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "17741 -23584 7514", 
                                "param1": "20009391"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "19994 -27252 7517", 
                                "param1": "20009392"
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
                                "param2": "6", 
                                "param1": "c1"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "c1到8s招怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "18156 -23619 7514", 
                                "param1": "20009391"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "20416 -27256 7517", 
                                "param1": "20009392"
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
                                "param2": "8", 
                                "param1": "c1"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "c1到10s招怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "18579 -23585 7514", 
                                "param1": "20009391"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "20900 -27267 7517", 
                                "param1": "20009392"
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
                                "param2": "10", 
                                "param1": "c1"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "c1到12s招怪c1计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "18880 -23592 7514", 
                                "param1": "20009391"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 89.954", 
                                "param2": "21528 -27344 7517", 
                                "param1": "20009392"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|3|5|6"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "c1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "c1"
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
                                "param1": "c1"
                            }
                        ], 
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