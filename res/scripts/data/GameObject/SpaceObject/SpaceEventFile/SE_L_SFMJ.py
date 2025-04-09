# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0.0 0.0 0.0", 
                    "param1": "-25770.0 -9480.0 5964.0", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    2: [
        {
            "title": "10秒倒计时结束，开始副本计时", 
            "describe": "移除定身buff14026201", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14024501", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010005|302010005|302010005", 
                    "param4": "", 
                    "id": 43
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "360", 
                    "param4": "", 
                    "id": 97
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010006|302010006|302010006", 
                    "param4": "", 
                    "id": 43
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000417", 
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
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "5分钟神风密卷大于3个，副本通关", 
            "describe": "副本通关、记录环任务副本统计、将玩家传送至海云帆旁边、完成环任务目标。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "111", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135043", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000465", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010005|302010006|301010118|23001701", 
                    "param4": "", 
                    "id": 24
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000425", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000196|40000728|40000727|40000733|40000726|40000732|40000731|40000729|40000730|40000734|20007933|20007934|20008260|20008261|20008262|20008263|20008264|20008265|20008266|20008267|20008268|20008269|20008270|20008271|20008272|20008273|20008274|20008275|20008276", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "收集神风残卷数量：", 
                    "param2": "80135043", 
                    "param1": "1", 
                    "param4": "10", 
                    "id": 330
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "LoopQuestLife", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "5分钟神风密卷不足3个，副本失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "111", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135043", 
                    "param4": "", 
                    "id": 30
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010005|302010006|301010118|23001701", 
                    "param4": "", 
                    "id": 24
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 325
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000196|40000728|40000727|40000733|40000726|40000732|40000731|40000729|40000730|40000734|20007933|20007934|20008260|20008261|20008262|20008263|20008264|20008265|20008266|20008267|20008268|20008269|20008270|20008271|20008272|20008273|20008274|20008275|20008276", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "1", 
                    "param2": "3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "LoopQuestLife", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    3: [
        {
            "title": "进入副本，完成任务目标1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135043", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    12: [
        {
            "title": "1号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "201", 
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
                    "id": 2, 
                    "param1": "20008269", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "2号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "202", 
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
                    "id": 2, 
                    "param1": "20008273", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "3号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "203", 
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
                    "id": 2, 
                    "param1": "20008270", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "4号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "204", 
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
                    "id": 2, 
                    "param1": "20008272", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "5号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "205", 
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
                    "id": 2, 
                    "param1": "20008271", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "6号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "206", 
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
                    "id": 2, 
                    "param1": "20007934", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "7号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "207", 
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
                    "id": 2, 
                    "param1": "20008276", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "8号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "208", 
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
                    "id": 2, 
                    "param1": "20008275", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "10号台猎鹰销毁，重新刷", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "210", 
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
                    "id": 2, 
                    "param1": "20008274", 
                    "param2": ""
                }
            ], 
            "id": 9
        }
    ], 
    13: [
        {
            "title": "删除额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 120
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701|14024501", 
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
    14: [
        {
            "title": "打开1个宝箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000423", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "add", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "打开3个箱子", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000678", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "3"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "add", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "101破风兽喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "101", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "102指定区域创建怪物", 
            "describe": "1、技能121502001发出的通知。通知创建一个无模型的怪物，用于播放一个预警光效", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20011601", 
                    "param4": "", 
                    "id": 155
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "102", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "102播放一条语音", 
            "describe": "1、技能121502001发出的通知。创建语音的时候播放一条语音，告诉玩家，怪物放技能了快躲呀！！！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000656", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "102", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "103乘骑buff时喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000419", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "103", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "104空盒子播放光效", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11024902", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "104", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "104播放一条语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000424", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "104", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "105 QTE结束之后喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000421", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "105", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "SUCESS事件1", 
            "describe": "QTE成功之后服务器发送给副本的通知，替换玩家技能栏", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14027102", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000420", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "SUCESS", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "FAILS事件", 
            "describe": "QTE失败之后服务器发送给副本的通知", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000422", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "FAILS", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "每次打开一个宝箱，m++", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "m", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "add", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "test，u++", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "u", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到技能通知402，在浮岛2刷出怪物", 
            "describe": "开箱子后，刷出怪物。", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "21", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "402", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到技能通知404，在浮岛4刷出怪物", 
            "describe": "开箱子后，刷出怪物。", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "41", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k4", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "404", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "收到技能通知406，在浮岛6刷出怪物", 
            "describe": "开箱子后，刷出怪物。", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "61", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k6", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "406", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "收到技能通知408，在浮岛8刷出怪物", 
            "describe": "开箱子后，刷出怪物。", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "81", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k8", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "408", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "收到技能通知410，在浮岛10刷出怪物", 
            "describe": "开箱子后，刷出怪物。", 
            "actions": [
                {
                    "delayTime": 1.0, 
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
                    "param1": "k10", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "410", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "点击退出按钮，玩家未完成任务时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 334
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "1", 
                    "param2": "3"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "SignOut", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 19
        }
    ], 
    15: [
        {
            "title": "玩家进入浮岛2，刷出暗怪", 
            "describe": "第一次踏入浮台，刷小怪；后续所有浮台宝箱均被收集，重置。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "21", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "k2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-19861.00000 -9574.00000 17604.05078", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "18000|17104"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入浮岛4，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "41", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k4", 
                    "param4": "", 
                    "id": 13
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "k4", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-23820.00000 -2160.00000 19226.87500", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "19426|19026"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入浮岛6，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "61", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k6", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "k6", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-32112.10156 -5531.67675 9626.38476", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "10926|8626"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家进入浮岛7，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "71", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k7", 
                    "param4": "", 
                    "id": 13
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "k7", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-31060.00000 -5290.00000 19523.00390", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "20523|18523"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "玩家进入浮岛8，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "81", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "k8", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "k8", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-31764.00000 -12076.00000 17402.43359", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "18402|16402"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "玩家进入浮岛10，刷出暗怪", 
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
                    "param1": "k10", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000418", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "k10", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-26452.00000 -15209.00000 16703.43359", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "17703|15703"
                }
            ], 
            "id": 6
        }
    ], 
    16: [
        {
            "title": "m==7,重置m,重置宝箱", 
            "describe": "所有宝箱都被打开，重新刷出场景所有宝箱和2个明怪,重置刷怪控制值K系列", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121502002", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "-7", 
                    "param1": "m", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
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
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
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
                    "delayTime": 2.0, 
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
                    "param1": "12", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "72", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k27", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k47", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k67", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k77", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k87", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k107", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "uu", 
                    "param4": "", 
                    "id": 13
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "m", 
                    "param2": "7"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "test", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121502002", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "-7", 
                    "param1": "u", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "uu", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "u", 
                    "param2": "7"
                }
            ], 
            "id": 2
        }
    ], 
    17: [
        {
            "title": "删除额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 311
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701|23001701|14024501", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010005|302010006|301010118|23001701", 
                    "param4": "", 
                    "id": 24
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    19: [
        {
            "title": "玩家死亡，神风密卷不足3个，副本失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "111", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135043", 
                    "param4": "", 
                    "id": 30
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010005|302010006|301010118|23001701", 
                    "param4": "", 
                    "id": 24
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000196|40000728|40000727|40000733|40000726|40000732|40000731|40000729|40000730|40000734|20007933|20007934|20008260|20008261|20008262|20008263|20008264|20008265|20008266|20008267|20008268|20008269|20008270|20008271|20008272|20008273|20008274|20008275|20008276", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "1", 
                    "param2": "3"
                }
            ], 
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
        }, 
        {
            "title": "玩家死亡但神风密卷大于3个，副本通关", 
            "describe": "副本通关、记录环任务副本统计、将玩家传送至海云帆旁边、完成环任务目标。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "111", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135043", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000465", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010005|302010006|301010118|23001701", 
                    "param4": "", 
                    "id": 24
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000425", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000196|40000728|40000727|40000733|40000726|40000732|40000731|40000729|40000730|40000734|20007933|20007934|20008260|20008261|20008262|20008263|20008264|20008265|20008266|20008267|20008268|20008269|20008270|20008271|20008272|20008273|20008274|20008275|20008276", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "收集神风残卷数量：", 
                    "param2": "80135043", 
                    "param1": "1", 
                    "param4": "10", 
                    "id": 330
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "3"
                }
            ], 
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
            "id": 2
        }
    ], 
    21: [
        {
            "title": "10秒倒计时开始", 
            "describe": "添加定时器t1、环任务倒计时10秒显示、同时播放开头语音Cy000416、给玩家上buff23001701（伤害减少90%）|14024501（定身）、获得302010005（浮光掠影）|302010006（落羽术）", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000965", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "23001701|14024501", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "增加额外的物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 119
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "初次进入浮台可刷小怪", 
            "describe": "初始化刷怪控制值K系列", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k27", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k47", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k67", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k77", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k87", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "k107", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "600", 
                    "param1": "K67", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    30: [
        {
            "title": "10秒倒计时开始", 
            "describe": "添加定时器t1、环任务倒计时10秒显示、同时播放开头语音Cy000416、给玩家上buff23001701（伤害减少90%）|14024501（定身）、获得302010005（浮光掠影）|302010006（落羽术）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000416", 
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
                    "id": 52, 
                    "param1": "Cy000965", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}