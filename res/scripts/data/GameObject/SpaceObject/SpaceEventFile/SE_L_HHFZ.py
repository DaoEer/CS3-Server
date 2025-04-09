# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "t1=3/k4<6，播放消除正确喊话", 
            "describe": "行为（19）：Q020425修改Q022243", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022243", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k4", 
                    "param2": "3"
                }
            ], 
            "canLoop": 1, 
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
        }
    ], 
    5: [
        {
            "title": "金鲤鱼全部被触发，刷新金鲤鱼", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 60.0, 
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
                    "id": 10, 
                    "param1": "3", 
                    "param2": "20005688:8"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005688", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    7: [
        {
            "title": "同步Boss血量", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20003680", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 14, 
                    "param1": "20003680", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003680", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "BossHP≤85%，k1+100/k2+100/清场/召唤Boss+平台/设置阶段2完成/关闭血条/Boss喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20001331|20005680|20005681|20005682|20005683|20005688|20005689|20003680|20003681|40000076|40000077|30000311|30000244|30000245", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "50000015:1", 
                    "id": 28
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "0 0 0", 
                    "param2": "223.0 34.0 1315.0", 
                    "param1": "L_HHFZ", 
                    "param4": "", 
                    "id": 22
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "20003680", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 108
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "k4", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000263", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 340
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 1, 
                    "param1": "0.85", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003680", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "收到True，k1+1/k2+1/记录t1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "4", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k4", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "True", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到False，k2+1/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "False", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到鲤鱼精发送的1，鲤鱼精喊话", 
            "describe": "行为（19）：Q020434修改Q022242", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022242", 
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
                    "param1": "AI", 
                    "param2": "20005689"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到镜头通知2，刷平台上的Boss", 
            "describe": "收到2，刷新Boss", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "20005679:1", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "263"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到BOSS通知让玩家任务目标完成", 
            "describe": "幻灵护法（20005679）血量低于10%，通知副本让副本内的玩家完成误入幻阵（20101170）任务目标（破解荷塘幻阵）\n让副本阶段目标完成", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101170", 
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
                    "param3": "123", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005679"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到镜头602的通知10，初始化荷花", 
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
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20003680", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022238|Q022239", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 109
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "10", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "602"
                }
            ], 
            "id": 6
        }
    ], 
    16: [
        {
            "title": "k1=1，刷新第一组小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005680:2|20005681:3", 
                    "param4": "", 
                    "id": 129
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "k1=2，刷新第二组小怪/k1-2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005682:3|20005683:3", 
                    "param4": "", 
                    "id": 129
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "-2", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k1", 
                    "param2": "2"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "k2=4，重刷荷花/k2-4", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 110
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "-4", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k2", 
                    "param2": "4"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "k1=1，第一波小怪喊话", 
            "describe": "行为（19）：Q020424修改为Q022241", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022241", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k1", 
                    "param2": "1"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "k3=1，错误提示", 
            "describe": "不需要修改跟最新文档一致", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020426", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "k3", 
                    "param2": "1"
                }
            ], 
            "id": 5
        }
    ], 
    21: [
        {
            "title": "玩家靠近池塘边缘，播镜头602/刷新荷花大阵/设置阶段1完成", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101170", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20101170", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "0 0 0", 
                    "param2": "-1950.0 13.0 234.0", 
                    "param1": "L_HHFZ", 
                    "param4": "", 
                    "id": 22
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}