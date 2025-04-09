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
                "name": "3秒心跳发射灵箭", 
                "tickTimer": 3.0, 
                "statesAI": [
                    {
                        "comment": "第1次只刷出灵箭", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction132", 
                                "param5": "t1||", 
                                "param4": "||", 
                                "param3": "10|15", 
                                "param2": "1|0|0", 
                                "param1": "lingjian1:lingjian_shadow11;lingjian2:lingjian_shadow22;lingjian3:lingjian_shadow33;lingjian4:lingjian_shadow44;lingjian5:lingjian_shadow55|fenjian1:fenjian_shadow11;fenjian2:fenjian_shadow22;fenjian3:fenjian_shadow33;fenjian4:fenjian_shadow44;fenjian5:fenjian_shadow55|yunshi1;yunshi2;yunshi3;yunshi4;yunshi5"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "y1"
                            }
                        ], 
                        "EID": [
                            8, 
                            10
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "灵箭的语音念完，开始释放焚箭", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "8"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "EID": [
                            1, 
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "13", 
                                "param1": "t1"
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
            }, 
            3: {
                "name": "另一个状态", 
                "tickTimer": 3.0, 
                "statesAI": [
                    {
                        "comment": "第2次只刷出灵箭和焚箭", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction132", 
                                "param5": "t1|t2|", 
                                "param4": "|Cy000180|", 
                                "param3": "10|15", 
                                "param2": "0.85|0.15|0", 
                                "param1": "lingjian1:lingjian_shadow11;lingjian2:lingjian_shadow22;lingjian3:lingjian_shadow33;lingjian4:lingjian_shadow44;lingjian5:lingjian_shadow55|fenjian1:fenjian_shadow11;fenjian2:fenjian_shadow22;fenjian3:fenjian_shadow33;fenjian4:fenjian_shadow44;fenjian5:fenjian_shadow55|yunshi1;yunshi2;yunshi3;yunshi4;yunshi5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 8
                    }, 
                    {
                        "comment": "焚箭的语音念完，开始播放陨石", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10"
                            }
                        ], 
                        "EID": [
                            9, 
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "4", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "第3次正常刷箭", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction132", 
                                "param5": "t1|t2|t3", 
                                "param4": "||Cy000192", 
                                "param3": "10|15", 
                                "param2": "0.82|0.17|0.01", 
                                "param1": "lingjian1:lingjian_shadow11;lingjian2:lingjian_shadow22;lingjian3:lingjian_shadow33;lingjian4:lingjian_shadow44;lingjian5:lingjian_shadow55|fenjian1:fenjian_shadow11;fenjian2:fenjian_shadow22;fenjian3:fenjian_shadow33;fenjian4:fenjian_shadow44;fenjian5:fenjian_shadow55|yunshi1;yunshi2;yunshi3;yunshi4;yunshi5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "2分钟加大一次难度", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction132", 
                                "param5": "||", 
                                "param4": "||", 
                                "param3": "10|15", 
                                "param2": "0.75|0.21|0.04", 
                                "param1": "lingjian1:lingjian_shadow11;lingjian2:lingjian_shadow22;lingjian3:lingjian_shadow33;lingjian4:lingjian_shadow44;lingjian5:lingjian_shadow55|fenjian1:fenjian_shadow11;fenjian2:fenjian_shadow22;fenjian3:fenjian_shadow33;fenjian4:fenjian_shadow44;fenjian5:fenjian_shadow55|yunshi1;yunshi2;yunshi3;yunshi4;yunshi5"
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
                                "param2": "120", 
                                "param1": "y1"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "3分钟加大一次难度", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction132", 
                                "param5": "||", 
                                "param4": "||", 
                                "param3": "10|15", 
                                "param2": "0.7|0.25|0.05", 
                                "param1": "lingjian1:lingjian_shadow11;lingjian2:lingjian_shadow22;lingjian3:lingjian_shadow33;lingjian4:lingjian_shadow44;lingjian5:lingjian_shadow55|fenjian1:fenjian_shadow11;fenjian2:fenjian_shadow22;fenjian3:fenjian_shadow33;fenjian4:fenjian_shadow44;fenjian5:fenjian_shadow55|yunshi1;yunshi2;yunshi3;yunshi4;yunshi5"
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
                                "param2": "210", 
                                "param1": "y1"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "4分钟加大一次难度", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction132", 
                                "param5": "||", 
                                "param4": "||", 
                                "param3": "10|15", 
                                "param2": "0.65|0.25|0.1", 
                                "param1": "lingjian1:lingjian_shadow11;lingjian2:lingjian_shadow22;lingjian3:lingjian_shadow33;lingjian4:lingjian_shadow44;lingjian5:lingjian_shadow55|fenjian1:fenjian_shadow11;fenjian2:fenjian_shadow22;fenjian3:fenjian_shadow33;fenjian4:fenjian_shadow44;fenjian5:fenjian_shadow55|yunshi1;yunshi2;yunshi3;yunshi4;yunshi5"
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
                                "param2": "270", 
                                "param1": "y1"
                            }
                        ], 
                        "id": 13
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