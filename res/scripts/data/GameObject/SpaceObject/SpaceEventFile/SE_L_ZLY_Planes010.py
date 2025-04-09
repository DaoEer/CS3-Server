# -*- coding: utf-8 -*-
Datas = {
    16: [
        {
            "title": "两只金乌到齐，开始喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041934|Q041935", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "22", 
                    "param1": "20006794", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "ff", 
                    "param2": "2"
                }
            ], 
            "id": 1
        }
    ], 
    3: [
        {
            "title": "玩家进入位面，喊话，移除玩家的九阳神火兽Buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041930|Q041932", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "Q041932语音结束，给九阳神火兽发送指令11", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "11", 
                    "param1": "20006794", 
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
                    "param1": "Q041932", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "Q041935语音结束，给所有人发送指令，开战", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "66", 
                    "param1": "20006775|20006774|20006793", 
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
                    "param1": "Q041935", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "Q041837语音结束，给蓐收发送指令345", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "345", 
                    "param1": "20006793", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "345", 
                    "param1": "20007064", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "345", 
                    "param1": "20007057", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000145", 
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
                    "id": 52, 
                    "param1": "Q041837", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "收到九阳神火兽到达场中央的指令，给祖巫蓐收发送指令，并喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "22", 
                    "param1": "20006793", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041836", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "22", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006794"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到任意一只金乌的指令，播放镜头，销毁第一场中的所有怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000348", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20006793|20006774|20006775|20006794", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006774|20006775"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到第二个镜头的指令，召唤怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
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
                    "param1": "6", 
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
                }, 
                {
                    "delayTime": 0.0, 
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
                    "param3": "6", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "348"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到第2场金乌的指令，销毁所有实体，播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20006796|20006797|20006798|20006799|20006800|20007051|20007052|20007053|20006766|20006767|20006768|20007054|20006769|20006770|20006771|20006772|20006773", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000349", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 15.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006766|20006767|20006768"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到最后一个镜头的指令，刷出防穿帮的准提和蓐收，玩家完成任务，出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102595", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_ZLY", 
                    "param4": "", 
                    "id": 20
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102603", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102633", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "6", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "349"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到蓐收的33指令，召唤金乌，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041837|Q041933", 
                    "param4": "", 
                    "id": 19
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
                    "param3": "33", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006793"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到男金乌的指令，召唤第3批怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "ff", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20007063"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到女金乌的指令，召唤第2批怪", 
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
                    "param2": "1", 
                    "param1": "ff", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20007062"
                }
            ], 
            "id": 8
        }
    ]
}