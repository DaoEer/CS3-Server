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
                "name": "随机召唤", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "时间t1", 
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
                            5
                        ], 
                        "Conditions": [], 
                        "id": 5
                    }, 
                    {
                        "comment": "随机状态|喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction84", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001712|C001713", 
                                "param1": "99|20"
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
                                "param2": "25", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "时间t2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [], 
                        "id": 7
                    }, 
                    {
                        "comment": "", 
                        "odds": 0.0, 
                        "Actions": [], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [], 
                        "id": 8
                    }, 
                    {
                        "comment": "t2=5", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 30", 
                                "param1": "1142 4438 1806"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 150", 
                                "param1": "1142 4438 1806"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 270", 
                                "param1": "1142 4438 1806"
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
                                "param2": "5", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "t2=15", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 30", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 150", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 270", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 10
                    }, 
                    {
                        "comment": "t1=15", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "35|8", 
                                "param3": "120", 
                                "param2": "0 0 30", 
                                "param1": "1142 4438 1806"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "35|8", 
                                "param3": "120", 
                                "param2": "0 0 150", 
                                "param1": "1142 4438 1806"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20009516", 
                                "param4": "35|8", 
                                "param3": "120", 
                                "param2": "0 0 270", 
                                "param1": "1142 4438 1806"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "7|9|10|11"
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
                                "param2": "15", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 11
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "招狼", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "随机召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20013428", 
                                "param4": "1", 
                                "param3": "1", 
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
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }, 
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
                        "Conditions": [], 
                        "id": 1
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "招狐", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "随机召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20013429", 
                                "param4": "1", 
                                "param3": "1", 
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
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }, 
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
                        "Conditions": [], 
                        "id": 2
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            4: {
                "name": "招鹰", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "随机召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20013430", 
                                "param4": "1", 
                                "param3": "1", 
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
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }, 
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
                        "Conditions": [], 
                        "id": 3
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            5: {
                "name": "招虎", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "随机召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20013431", 
                                "param4": "1", 
                                "param3": "1", 
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
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }, 
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