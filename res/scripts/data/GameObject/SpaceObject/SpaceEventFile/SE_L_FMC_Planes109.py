# -*- coding: utf-8 -*-
Datas = {
    17: [
        {
            "title": "玩家离开副本时，如果任务1的目标2已完成，则重置", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101662", 
                    "param4": "", 
                    "id": 29
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "2", 
                    "id": 16, 
                    "param1": "20101662", 
                    "param2": "3"
                }
            ], 
            "id": 1
        }
    ], 
    3: [
        {
            "title": "玩家进入副本，检测玩家携带了第二个任务，发送指令给金元童子", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "523", 
                    "param1": "20011872", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "3", 
                    "param3": "1", 
                    "id": 15, 
                    "param1": "20101663", 
                    "param2": "3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到火灵童子的指令11，完成阶段1的目标1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "11", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011872"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到火灵童子的指令21，完成阶段2的目标1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "21", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011872"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到火灵童子的指令31，完成阶段3的目标1，完成任务1的目标2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101662", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
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
                    "param3": "31", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011872"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到火灵童子的指令31，如果玩家第1个任务完成，则继续后面的流程", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "3", 
                    "param3": "1", 
                    "id": 15, 
                    "param1": "20101663", 
                    "param2": "3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "31", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011872"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到玩家发的指令12345，完成阶段3的目标2，给火灵童子发送1234", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1234", 
                    "param1": "20011872", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到火灵童子的指令41，完成阶段4的目标1，完成任务2的目标1，播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101663", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000700", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "41", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011872"
                }
            ], 
            "id": 6
        }
    ]
}