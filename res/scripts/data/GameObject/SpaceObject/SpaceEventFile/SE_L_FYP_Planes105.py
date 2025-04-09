# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "第一阶段完成，播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050504", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第二阶段完成，播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050506", 
                    "param4": "", 
                    "id": 19
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
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "第四阶段完成，播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050515|Q050517", 
                    "param4": "", 
                    "id": 19
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
            "id": 3
        }, 
        {
            "title": "第五阶段完成，刷新第4批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }, 
        {
            "title": "第六阶段完成，刷新第5批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 5
        }
    ], 
    30: [
        {
            "title": "小怪叫喊完，给怪物发送指令，停止切磋", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "277", 
                    "param1": "20009887|20009893", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050507|Q050508", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q050506", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "转身警告", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20009887|20009878|20009879|20009880|20009893", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050510|Q050511|Q050512", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q050508", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "语音结束，刷新指示，完成阶段3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
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
                    "id": 52, 
                    "param1": "Q050512", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "语音结束，给小怪发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20009878|20009879|20009880|20009893", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q050517", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "投降语音结束，给BOSS发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "667", 
                    "param1": "20009888", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q050533", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    14: [
        {
            "title": "收到BOSS通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102651", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "101", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009888"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到小怪通知，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050519", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "997", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到怪物通知，刷新传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102651", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.90000009537, 
                    "param3": "", 
                    "param2": "513", 
                    "param1": "20009888", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050534", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "857", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009888"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到BOSS投降通知，播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050525|Q050526|Q050527|Q050529|Q050530|Q050531|Q050533", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "666", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009888"
                }
            ], 
            "id": 4
        }
    ]
}