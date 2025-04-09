# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "开始刷船倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "40", 
                    "param1": "chuan1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "30", 
                    "param1": "chuan2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "35", 
                    "param1": "chuan3", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "复活点", 
            "describe": "未完成阶段1", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 35.0", 
                    "param1": "62013.6 32498.6 808.5", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    2: [
        {
            "title": "倒计时刷船1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "chuan1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "倒计时刷船2", 
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "chuan2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "倒计时刷船3", 
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "chuan3", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "2秒去中毒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12160301", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "zhongdu", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    3: [
        {
            "title": "判断有无瘴气", 
            "describe": "判断BUFF+判断副本阶段", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12160201", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "12160201", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "刷奖励宝箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "414068", 
                    "param2": "SK_ZW0017_NPC|0.5", 
                    "param1": "61873.4 32241.7 799.0|0 0 50", 
                    "param4": "", 
                    "id": 427
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    5: [
        {
            "title": "击杀boss完成通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010771", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20010736", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "1层击杀boss设置2层等级", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 441
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20010736", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 61, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "2层击杀boss掉宝箱设置3层等级", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 441
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "414008", 
                    "param2": "2", 
                    "param1": "SK_ZW0017_NPC", 
                    "param4": "", 
                    "id": 440
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20010736", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 61, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "3层击杀boss掉宝箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "414009", 
                    "param2": "2", 
                    "param1": "SK_ZW0017_NPC", 
                    "param4": "", 
                    "id": 440
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20010736", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 61, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    8: [
        {
            "title": "移除瘴气BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12160301", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "2", 
                    "param1": "zhongdu", 
                    "param4": "", 
                    "id": 12
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
            "title": "阶段3复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 138", 
                    "param1": "56612 51412 884", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
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
        }, 
        {
            "title": "阶段4复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -5", 
                    "param1": "36724 23348 -2838", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "阶段5复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 38", 
                    "param1": "46676 25900 -2917", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
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
            "id": 4
        }, 
        {
            "title": "阶段6复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -114", 
                    "param1": "38299 42436 -4043", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
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
            "id": 5
        }, 
        {
            "title": "阶段2完成，清除中毒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12160301", 
                    "param4": "", 
                    "id": 26
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
            "id": 6
        }, 
        {
            "title": "阶段6完成通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010771", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "id": 7
        }
    ], 
    14: [], 
    15: [
        {
            "title": "清除中毒buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12160301", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "56171 53423 884", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "12160301", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "提示使用火鼎", 
            "describe": "提示火鼎使用", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001314", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "12", 
                    "param3": "62320 32698 807", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "提示靠近火鼎", 
            "describe": "提示靠近火鼎", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001313", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "63630 33840 670", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "提示冥河伤害", 
            "describe": "提示", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001317", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "54870 53130 590", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "提示冥河瘴气", 
            "describe": "提示", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001318", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "50", 
                    "param3": "51690 55590 490", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "提示凶魂显形", 
            "describe": "提示", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001319", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "48320 29410 -3010", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|-5000"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "雾灯怪喊话", 
            "describe": "提示", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001315", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "14", 
                    "param3": "60990 42180 790", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "石头现身怪喊话", 
            "describe": "提示", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001320", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "13", 
                    "param3": "48260 29530 -3030", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "0|-5000"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "石头现身怪喊话2", 
            "describe": "提示", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001321", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "12", 
                    "param3": "41740 45610 -4190", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "0|-5000"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "清除中毒buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12160301", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "56528 51679 884", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1500|0"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "12160301", 
                    "param2": ""
                }
            ], 
            "id": 10
        }
    ], 
    21: []
}