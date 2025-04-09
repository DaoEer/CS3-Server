# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段1完成，刷第2波怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
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
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段2完成，刷第3波怪", 
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
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "阶段4完成，给箭塔发送指令，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "gongji", 
                    "param1": "20012924|20012925", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050730", 
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
                    "id": 4, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "阶段5完成，销毁光墙等", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20012926|20012928|20012927", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12", 
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
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    14: [
        {
            "title": "收到第1波小怪的通知，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050732", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "kaishi", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012912|20012913"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到第2波小怪的通知，刷暗怪", 
            "describe": "", 
            "actions": [
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
                    "param3": "324", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012914"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到20012916的指令555，完成阶段3", 
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
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "555", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012916"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到Boss的zhaoguai指令，召唤怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "13", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "16", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "zhaoguai", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012929"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到boss的结束指令，播放镜头，完成任务和阶段", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000734", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102677", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "jieshu", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012929"
                }
            ], 
            "id": 5
        }
    ], 
    30: [
        {
            "title": "Q050655语音结束，开始战斗", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "kaishi", 
                    "param1": "20012916|20012917|20012918", 
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
                    "param1": "Q050655", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "Q050728喊话结束，给箭塔发送指令kaishi", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "kaishi", 
                    "param1": "20012924|20012925", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "9", 
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
                    "param1": "Q050728", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "Q050729喊话结束，所有的人都开始战斗", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "kaishi", 
                    "param1": "20012919|20012920|20012921", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "17", 
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
                    "param1": "Q050729", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "Q050662喊话结束，给Boss发送指令kaishi", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "kaishi", 
                    "param1": "20012929", 
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
                    "param1": "Q050662", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "Q050657喊话结束，给Boss发送指令idle", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "idle", 
                    "param1": "20012929", 
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
                    "param1": "Q050657", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    15: [
        {
            "title": "进入精英范围，发送指令，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hanhua", 
                    "param1": "20012916|20012917|20012918", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050651|Q050652|Q050653|Q050655", 
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
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "1207.645874 6519.429199 4852.340332", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "6666|3333"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入院子，喊话，给精英、小怪、柱子等发指令。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hanhua", 
                    "param1": "20012919|20012920|20012921", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050728|Q050729", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "13800.12207 6145.107422 5343.504883", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "6666|4333"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "进入Boss范围，给Boss和表演怪发送指令，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hanhua", 
                    "param1": "20012929|20012930", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050656", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050657|Q050659|Q050660|Q050662", 
                    "param4": "", 
                    "id": 19
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
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "30348.103516 6208.230957 5982.591797", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "7777|4444"
                }
            ], 
            "id": 3
        }
    ]
}