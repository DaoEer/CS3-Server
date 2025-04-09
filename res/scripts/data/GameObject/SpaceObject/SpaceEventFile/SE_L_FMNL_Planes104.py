# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "批次1死亡，刷批次2", 
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
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "批次2死亡，刷批次3", 
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
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    7: [
        {
            "title": "Boss血量低于5%时，播放镜头。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000705", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049303", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20002722", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20011335", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 14, 
                    "param1": "20002722", 
                    "param2": "0.05"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "BOSS在水上战斗召唤冲锋怪（一）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "101", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "10", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20002722"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "BOSS在水上战斗召唤冲锋怪（一，二）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "101", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "102", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "20", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20002722"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "BOSS在水上战斗召唤冲锋怪（一）和浪花", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "101", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "103", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "30", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20002722"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到小怪通知，开始喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q023560|Q022672|Q022761", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "677", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20011815"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "Boss血量低于5%时，出位面，完成任务，播放镜头。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101669", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101669", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FMNL", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "705"
                }
            ], 
            "id": 5
        }
    ], 
    15: [
        {
            "title": "玩家到达BOSS，半身像界面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022674|Q022675|Q022677", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "123", 
                    "param1": "20002722", 
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
                    "param4": "15", 
                    "param3": "115998 -40709 -17138", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-15960|-17960"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入水中心", 
            "describe": "玩家进入水中间，刷水墙，通知BOSS", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022731|Q022732|Q022681", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20002720:1", 
                    "param2": "0 0 40", 
                    "param1": "115998.085938 -29414.845703 -17720.0", 
                    "param4": "", 
                    "id": 6
                }, 
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
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "118110 -27700 -17660", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-10000|-20000"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家到达第一波怪处，给怪物发指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20011814", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20011815", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 11.0, 
                    "param3": "", 
                    "param2": "333", 
                    "param1": "20011814", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "50", 
                    "param3": "114922.375 -55120.28125 -16965.751953", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-10960|-27960"
                }
            ], 
            "id": 3
        }
    ], 
    17: [
        {
            "title": "玩家离开位面，身上如果有无敌Buff，则移除", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049303", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "11049303", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    19: [
        {
            "title": "玩家死亡，给天极神君发指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "279", 
                    "param1": "20002722", 
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
                    "id": 21, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "BOSS站前叫嚣结束-通知BOSS结束", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20002722|20002720", 
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
                    "param1": "Q022677", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "小怪喊话结束，给小怪发指令进战斗，招房顶暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "811", 
                    "param1": "20011815|20011814", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "20002716:1|20002717:2", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q022761", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "第2句语音喊完，招怪", 
            "describe": "玩家进入水中间，刷水墙，通知BOSS", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "200", 
                    "param1": "20002722|20002720", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "212", 
                    "param1": "20011335", 
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
                    "param1": "Q022732", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ]
}