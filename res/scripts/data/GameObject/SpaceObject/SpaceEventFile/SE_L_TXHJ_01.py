# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段2深入幻境完成后，刷第二波暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20000819", 
                    "param1": "2", 
                    "param4": "20000143:3", 
                    "id": 28
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "20000819", 
                    "param1": "2", 
                    "param4": "20000144:2", 
                    "id": 28
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "1", 
                    "param2": "20000819", 
                    "param1": "2", 
                    "param4": "20000142:2", 
                    "id": 28
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
            "id": 1
        }, 
        {
            "title": "阶段4探查石像完成后，喊话，对第一波石像发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q010846", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20000145", 
                    "param4": "", 
                    "id": 10
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
            "id": 2
        }
    ], 
    12: [
        {
            "title": "第一波上古天兵死光后发送指令给第二波石像", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20000146", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20000821", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "3", 
                    "param2": "20000145:3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第二波上古天兵死光后发送指令给第三波石像", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20000147", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20000822", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "3", 
                    "param2": "20000146:2|20000821:2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "第三波上古天兵死光后播放镜头，太古心魔出现。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000043", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "3", 
                    "param2": "20000147:2|20000822:3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "接收第一波石像指令，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q010847", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20000145"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "副本接收到心魔出现镜头指令21，刷太古心魔(战)", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "20000129:1", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "21", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "43"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "副本接收到心魔出现镜头指令22，刷太古心魔(剑)", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "20000149:1", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "22", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "43"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到心魔的通知25，播放心魔死亡镜头/销毁心魔", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000044", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 18.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20000129|20000149", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "25", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到镜头44的通知26，播放玩家获得太虚符箓的镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110001004", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "26", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "44"
                }
            ], 
            "id": 5
        }
    ]
}