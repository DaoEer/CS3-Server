# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段2“深入道场”完成，播放左右护法出场镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000035", 
                    "param4": "", 
                    "id": 17
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
            "title": "阶段4“破开防护禁制”完成，播放摧毁禁制镜头，销毁光墙与太极禁制", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000036", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20000707|20000766", 
                    "param4": "", 
                    "id": 9
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
        }, 
        {
            "title": "阶段5“夺回太虚境”完成，传送玩家出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_YSC", 
                    "param4": "", 
                    "id": 20
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
            "id": 3
        }
    ], 
    5: [
        {
            "title": "玄机子死亡，通知传送法台取消不可攻击", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4", 
                    "param1": "20000708", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "传送法台死亡，播放获得太虚境镜头，销毁场景中的光效与太虚境", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000037", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20000756|20000125", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20000708", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "收到左右护法出场镜头通知1，刷出左右护法", 
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
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "35"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到破开禁制镜头通知2，玄机子攻击玩家", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20000123", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "36"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到获得太虚境镜头通知5，玩家获得太虚境", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110001005", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "37"
                }
            ], 
            "id": 3
        }
    ], 
    15: [
        {
            "title": "玩家进入范围1，刷暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "20000169", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "5283 43387 12109", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "17000|7000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围2，半身像界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q010290", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "7163 47827 11990", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "16990|8990"
                }
            ], 
            "id": 2
        }
    ]
}