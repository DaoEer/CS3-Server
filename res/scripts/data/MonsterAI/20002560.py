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
                "name": "招怪", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "有玩家计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time"
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
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "25"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "1秒后招3个怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "9758 -6980 3082", 
                                "param1": "20004513"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "9658 -6601 3082", 
                                "param1": "20002766"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "9587 -6199 3088", 
                                "param1": "20002766"
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
                                "param2": "1", 
                                "param1": "time"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "2秒后招4个怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "12117 -6943 4271", 
                                "param1": "20004112"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "12126 -6721 4274", 
                                "param1": "20004112"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "12137 -5319 4287", 
                                "param1": "20004113"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -169", 
                                "param2": "12140 -5138 4281", 
                                "param1": "20004113"
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
                                "param2": "2", 
                                "param1": "time"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "销毁", 
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
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "time"
                            }
                        ], 
                        "id": 5
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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}