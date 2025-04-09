# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "t1到达，4选1/记录t2/播放提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 90|0 0 90|0 0 90|0 0 90", 
                    "param2": "-1408.0 5278.0 760.0|-5173.0 5278.0 760.0|-5173.0 1512.0 760.0|-1408.0 1512.0 760.0", 
                    "param1": "20005963|20005963|20005963|20005963", 
                    "param4": "1", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "15", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "t2到达，4选2/记录t3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 90|0 0 90|0 0 90|0 0 90", 
                    "param2": "-1408.0 5278.0 760.0|-5173.0 5278.0 760.0|-5173.0 1512.0 760.0|-1408.0 1512.0 760.0", 
                    "param1": "20005963|20005963|20005963|20005963", 
                    "param4": "2", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "15", 
                    "param1": "t3", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "t3到达，4选3/记录循环t4", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 90|0 0 90|0 0 90|0 0 90", 
                    "param2": "-1408.0 5278.0 760.0|-5173.0 5278.0 760.0|-5173.0 1512.0 760.0|-1408.0 1512.0 760.0", 
                    "param1": "20005963|20005963|20005963|20005963", 
                    "param4": "3", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "15", 
                    "param1": "t4", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t3", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "t4到达，4选（1-3）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 90|0 0 90|0 0 90|0 0 90", 
                    "param2": "-1417.5 5278.0 760.0|-5172.0 5278.5 760.0|-1417.5 1521.9 760.0|-5172.0 1521.9 760.0", 
                    "param1": "20005963|20005963|20005963|20005963", 
                    "param4": "1|3", 
                    "id": 156
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t4", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "t0到达，刷新棋子", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "20005964", 
                    "param4": "", 
                    "id": 157
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t0", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    5: [
        {
            "title": "黑棋/白棋死亡，对Boss发送10", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "20005952", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005955|20005956", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005959|20005962", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    7: [
        {
            "title": "BossHP≤75%，进入阶段二", 
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
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005951|20005953|20005955|20005956|20005957|20005958|20005963|20005964", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 36
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000693", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20005951", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 108
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 125
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005951", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 49, 
                    "param1": "0.75", 
                    "param2": "5"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "同步Boss血量/通知Boss把玩家加入敌人列表", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20005951", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "7", 
                    "param1": "20005951", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 14, 
                    "param1": "20005951", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005951", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "收到3，第一波小怪喊话", 
            "describe": "Q020908替换（Q022708）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022708", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到4，第二波小怪喊话", 
            "describe": "Q020909替换：Q022709", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022709", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到5，刷传送门", 
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
                    "param3": "5", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到1，刷初始化棋盘/Boss血量显示/记录t0循环/记录t1", 
            "describe": "新增加19：（Q022705|Q022706）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "250", 
                    "param1": "230", 
                    "param4": "", 
                    "id": 35
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20005951", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022705|Q022706", 
                    "param4": "", 
                    "id": 19
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
                    "param2": "692"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到XC，创建刷怪陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005953", 
                    "param4": "", 
                    "id": 155
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
                    "param3": "XC", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到6，对Boss发送8", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "8", 
                    "param1": "20005952", 
                    "param4": "", 
                    "id": 10
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
                    "param2": "693"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到Boss的指令9，喊话", 
            "describe": "删掉：17（110000277）43（301010040）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022713|Q022714", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "9", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005952"
                }
            ], 
            "id": 7
        }
    ], 
    15: [
        {
            "title": "玩家进入棋阵，玩法提示/Boss血量显示/记录t0循环/记录t1", 
            "describe": "删掉：19（Q020906）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20005951", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "8", 
                    "param1": "t0", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-7390.0 -1660.0|800.0 -1660.0|800.0 7500.0|-7390.0 7500.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "5000|-5000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入棋阵，开启阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 124
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "509.6 -393.8|510.0 7210.0|-7100.0 7200.0|-7090.0 -400.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "5000|-5000"
                }
            ], 
            "id": 2
        }
    ], 
    30: [
        {
            "title": "最后一句说完，召唤传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "30000834:1", 
                    "param2": "0 0 -95", 
                    "param1": "-3283.0 2592.0 760.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101671", 
                    "param4": "", 
                    "id": 2
                }, 
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
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q022714", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}