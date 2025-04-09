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
                        "comment": "1秒后招2个怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -9", 
                                "param2": "-12841.0 -968.5 956.7", 
                                "param1": "20002505"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -9", 
                                "param2": "-12928.5 -559.5 1016.9", 
                                "param1": "20002505"
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
                        "comment": "2秒后招2个怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -9", 
                                "param2": "-13286.8 -1179.7 1023.9", 
                                "param1": "20002505"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "0 0 -9", 
                                "param2": "-13286.8 -757.8 1053.2", 
                                "param1": "20002505"
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
                        "comment": "3秒发送指令给射手怪（暂废）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "111", 
                                "param2": "20002508|20002509", 
                                "param1": "50"
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
                                "param2": "3", 
                                "param1": "time"
                            }
                        ], 
                        "id": 4
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