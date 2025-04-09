# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段3完成，完成任务“仙府宝库”", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101241", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FLS", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第2阶段完成，才刷影风和周阳长老", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    16: [
        {
            "title": "收到7次指令，完成阶段", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "kk", 
                    "param2": "7"
                }
            ], 
            "id": 1
        }
    ], 
    7: [
        {
            "title": "影风血量低于10%，通知666影风和周阳", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "666", 
                    "param1": "20003703", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "666", 
                    "param1": "20003704", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003703", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 1, 
                    "param1": "0.1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到7只怪物通知标记+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "kk", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "444", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011977|20011978|20011979|20011980|20011981|20011982|20011983"
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家进入范围2，通知影风", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "200", 
                    "param1": "20003703", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "14", 
                    "param3": "43410 11800 -107.813721", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "400|-600"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围1，刷出跳出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q030385|Q030386", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "52590.0 -1440.0|47990.0 -1440.0|47990.0 -210.0|52590.0 -210.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1300|100"
                }
            ], 
            "id": 2
        }
    ]
}