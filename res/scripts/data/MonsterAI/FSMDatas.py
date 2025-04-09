# -*- coding: utf-8 -*-
Datas = {
    1: {
        "groupStates": [
            {
                "tiggerEventType": "10", 
                "groupName": "准备状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition30", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "pead", 
                "isDefault": "1"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "自由状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition6", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "free", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "战斗状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition4", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "fight", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "死亡状态", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition8", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "dead", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "重置状态", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition7", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "reset", 
                "isDefault": "0"
            }
        ], 
        "name": "普通状态机", 
        "script": "AIFSMCommon"
    }, 
    2: {
        "groupStates": [
            {
                "tiggerEventType": "10", 
                "groupName": "准备状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition30", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "pead", 
                "isDefault": "1"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "自由状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition6", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "free", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "战斗状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition4", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "fight", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "死亡状态", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition8", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "dead", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "重置状态", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition7", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "reset", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "表演状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition31", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "show", 
                "isDefault": "0"
            }
        ], 
        "name": "表演状态机", 
        "script": "AIFSMCommon"
    }, 
    3: {
        "groupStates": [
            {
                "tiggerEventType": "10", 
                "groupName": "准备状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition30", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "pead", 
                "isDefault": "1"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "死亡状态", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition8", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "dead", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "混合状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition43", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "stable", 
                "isDefault": "0"
            }
        ], 
        "name": "机关怪状态机", 
        "script": "AIFSMExt1"
    }, 
    4: {
        "groupStates": [
            {
                "tiggerEventType": "10", 
                "groupName": "自由状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition6", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "free", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "战斗状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition4", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "fight", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "重置状态", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition7", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "reset", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "死亡状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition8", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "dead", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "准备状态", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition30", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "pead", 
                "isDefault": "1"
            }
        ], 
        "name": "重生状态机", 
        "script": "AIFSMCommon"
    }, 
    5: {
        "groupStates": [
            {
                "tiggerEventType": "25", 
                "groupName": "1级", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition85", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "1"
                    }
                ], 
                "groupID": "level_1", 
                "isDefault": "1"
            }, 
            {
                "tiggerEventType": "25", 
                "groupName": "2级", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition85", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "2"
                    }
                ], 
                "groupID": "level_2", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "25", 
                "groupName": "3级", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition85", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "3"
                    }
                ], 
                "groupID": "level_3", 
                "isDefault": "0"
            }
        ], 
        "name": "勇闯夺命岛大BOSS状态机", 
        "script": "AIFSM_YCDMD_BOSS"
    }, 
    6: {
        "groupStates": [
            {
                "tiggerEventType": "25", 
                "groupName": "跟随", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition103", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "1", 
                        "param1": "aiStatus"
                    }
                ], 
                "groupID": "follow", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "25", 
                "groupName": "矩形列阵", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition103", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "2", 
                        "param1": "aiStatus"
                    }
                ], 
                "groupID": "rectFormation", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "25", 
                "groupName": "圆形矩阵", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition103", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "3", 
                        "param1": "aiStatus"
                    }
                ], 
                "groupID": "circleFormation", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "25", 
                "groupName": "攻击", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition103", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "4", 
                        "param1": "aiStatus"
                    }
                ], 
                "groupID": "attack", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "死亡", 
                "isStartTick": "0", 
                "triggerConditions": [
                    {
                        "script": "AICondition8", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "dead", 
                "isDefault": "0"
            }, 
            {
                "tiggerEventType": "10", 
                "groupName": "准备", 
                "isStartTick": "1", 
                "triggerConditions": [
                    {
                        "script": "AICondition30", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
                    }
                ], 
                "groupID": "pend", 
                "isDefault": "1"
            }
        ], 
        "name": "攻城战小兵", 
        "script": "AIFSMSoldier"
    }
}