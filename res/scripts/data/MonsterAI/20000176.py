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
                "name": "陷阱1-1（营救风橙）", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "t1=1，召唤暗怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 160", 
                                "param2": "-50177.65 -31259.88 12183.96", 
                                "param1": "20000178"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 160", 
                                "param2": "-49977.65 -31309.88 12138.10", 
                                "param1": "20000179"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 160", 
                                "param2": "-50047.64 -31089.88 12120.26", 
                                "param1": "20000178"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 1
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "有暗怪，召唤出生光效/记录t1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 -160", 
                                    "param2": "-50177.65 -31259.88 12183.96", 
                                    "param1": "20000177"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 -160", 
                                    "param2": "-49977.65 -31309.88 12138.10", 
                                    "param1": "20000177"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 -160", 
                                    "param2": "-50047.64 -31089.88 12120.26", 
                                    "param1": "20000177"
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
                                2
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Role"
                                }
                            ], 
                            "id": 2
                        }
                    ]
                }, 
                "initiativeAreaXZ": "10.000000", 
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