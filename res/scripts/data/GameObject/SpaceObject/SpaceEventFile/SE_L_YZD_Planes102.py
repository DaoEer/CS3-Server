# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "第四阶段完成，完成任务目标，刷新鲲鹏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101730", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20101731", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "16", 
                    "param4": "", 
                    "id": 27
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
            "id": 1
        }, 
        {
            "title": "登上台阶，天河道人喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q030791|Q030792", 
                    "param4": "", 
                    "id": 19
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
            "id": 2
        }, 
        {
            "title": "1阶段完成，刷新精英", 
            "describe": "", 
            "actions": [
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
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    16: [
        {
            "title": "k1=2，召唤三个精英", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14", 
                    "param4": "", 
                    "id": 27
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
                    "param2": "2"
                }
            ], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "1到4批次怪物全部死亡，发送指令给光墙\\2s延迟消耗空气墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20003954", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20003953", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "冰柱死亡，对冰柱阵法发送1/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20003955", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
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
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003947", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "火柱死亡，对火柱阵法发送1/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20003956", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
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
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003948", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "风柱死亡，对风柱阵法发送1/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20003957", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
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
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003949", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "雷柱死亡，对雷柱阵法发送1/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20003958", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
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
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003950", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "冰柱守卫死完，冰柱可被攻击。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "250", 
                    "param1": "20003947", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "10", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 6
        }, 
        {
            "title": "火柱守卫死完，火柱可被攻击。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "250", 
                    "param1": "20003948", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "11", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 7
        }, 
        {
            "title": "风柱守卫死完，风柱可被攻击。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "250", 
                    "param1": "20003949", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "12", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 8
        }, 
        {
            "title": "雷柱守卫死完，雷柱可被攻击。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "250", 
                    "param1": "20003950", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "13", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 9
        }, 
        {
            "title": "所有阵柱摧毁\\怪物死亡，对金色旋涡发送2/对Boss（表演）发送3/播放boss出场镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20003951", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20003946", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "7|10|11|12|13|14", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 10
        }
    ], 
    14: [
        {
            "title": "接收到第三波小怪通知，喊话，刷暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "20003199:3", 
                    "id": 28
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "20003200:2", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "110", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003197"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到鲲鹏就位通知，将玩家传出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_YZD", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "279", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003971"
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "靠近冰柱，召唤第10批次小怪/喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
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
                    "param1": "Q030952", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "16", 
                    "param3": "44110 59290 7910", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "12910|2910"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "靠近火柱，召唤第11批次小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "16", 
                    "param3": "46650 54660 7910", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "12910|2910"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "靠近风柱，召唤第12批次小怪/喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
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
                    "param1": "Q030953", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "16", 
                    "param3": "51290 57220 7910", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "12910|2910"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "靠近雷柱，召唤第13批次小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "13", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "16", 
                    "param3": "48720 61850 7910", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "12910|2910"
                }
            ], 
            "id": 4
        }
    ]
}