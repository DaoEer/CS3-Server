# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "机关全部死亡，发通知111", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20006236|20007110|20007181|20007182|20007183", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 13, 
                    "param1": "5", 
                    "param2": "2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "BOSS死亡，死亡喊话/完成任务目标1", 
            "describe": "你们是救不了金乌的……\n没想到十金乌竟被带往了金星，我得速去回禀帝俊前辈。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045216|Q045217", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102071", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20006236", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "机关A死亡，清除boss身上连线buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "11024503", 
                    "param1": "20006236", 
                    "param4": "", 
                    "id": 237
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007109", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "机关B死亡，清除boss身上连线buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "11024505", 
                    "param1": "20006236", 
                    "param4": "", 
                    "id": 237
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20006216", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    14: [
        {
            "title": "收到tips，旁白提示", 
            "describe": "注意别靠巡逻守卫太近。以免露出破绽。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045206", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "tips", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家到达某地，发通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20007102|20007103", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-1730 8600 2392", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2892|1892"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家到达某地，发通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20007104|20007105", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-12690 8570 3630", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "4130|3130"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家到达某地，发通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20007106|20007107", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-24289 8600 4832", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5332|4332"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家到达平台1，添加脱战buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "stop", 
                    "param1": "20007102|20007103|20007104|20007105|20007106|20007107", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-7964.922852 8611.579102 3563.624023", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "4063|3063"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "玩家到达平台2，添加脱战buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "stop", 
                    "param1": "20007102|20007103|20007104|20007105|20007106|20007107", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-18958.042969 8611.579102 4934.495605", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5434|4434"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "玩家到达平台3，添加脱战buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "stop", 
                    "param1": "20007102|20007103|20007104|20007105|20007106|20007107", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-30019.324219 8611.579102 4733.916992", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5233|4233"
                }
            ], 
            "id": 6
        }
    ], 
    17: [
        {
            "title": "玩家离开副本，清除变身相关buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11022501|11022502|11022503|11022505", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入副本，添加BUFF/旁白提示玩家使用符咒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045205", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11022502", 
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
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    24: [
        {
            "title": "玩家脱战，加BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11022502", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 33, 
                    "param1": "1", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 39, 
                    "param1": "11022502", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "变身期间，清除提示变身BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11022502", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "11022501", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进战，小怪识破变身喊话Q045285", 
            "describe": "有敌人潜入！快拿下！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045285", 
                    "param4": "", 
                    "id": 19
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
                    "id": 33, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    30: [
        {
            "title": "死亡喊话结束，起飞回太阳宫", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110002155", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q045217", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}