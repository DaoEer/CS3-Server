# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "boss死亡，死亡喊话/小怪全部死亡/通知阵柱change", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "inshow", 
                    "param1": "20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051223|Q051224", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "change", 
                    "param1": "20014408|20014409", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20014404|20014405|20014406|20014407", 
                    "param4": "", 
                    "id": 130
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20014402", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "城门已破，销毁阻挡墙/太一喊话/刷城内小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20014382|20014380|20014381|20014383", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051219", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
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
            "title": "阵眼全部被毁，销毁落石陷阱/通知太一落下", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20014403|30001172|30001173|20014410", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "dowm", 
                    "param1": "20014384", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051226", 
                    "param4": "", 
                    "id": 19
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
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "收到diyibo，小怪喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051216", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "diyibo", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到huopao，城门剧情太一喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051217|Q051218", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "huopao", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到fire，通知火炮2开炮", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "fire", 
                    "param1": "20014381", 
                    "param4": "", 
                    "id": 10
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
                    "param3": "fire", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到act，刷太一保护罩/太一喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051221", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "act", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到sound，boss战前喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051222", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "sound", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到sound2，分岔路剧情", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051227|Q051229|Q051230", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "sound2", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }
    ], 
    21: [
        {
            "title": "玩家进入副本，开始剧情", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051215", 
                    "param4": "", 
                    "id": 18
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102193", 
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
    28: [
        {
            "title": "阶段1目标1完成，通知太一等人go1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "go1", 
                    "param1": "20014384|20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
                    "param4": "", 
                    "id": 10
                }, 
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
                    "param3": "", 
                    "id": 43, 
                    "param1": "1", 
                    "param2": "1"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段1目标2完成，通知太一等人go2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "go2", 
                    "param1": "20014384|20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
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
                    "id": 43, 
                    "param1": "1", 
                    "param2": "2"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "阶段3目标1完成，刷boss/通知太一go4/刷落石陷阱/延迟8秒播boss喊话：开启落石大阵/通知boss对玩家释放落石技能", 
            "describe": "延迟8秒播boss喊话：开启落石大阵", 
            "actions": [
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
                    "param2": "go4", 
                    "param1": "20014384", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "9", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051220", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 3.5, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20014402", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 3.0, 
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
                    "param3": "", 
                    "id": 43, 
                    "param1": "3", 
                    "param2": "1"
                }
            ], 
            "id": 3
        }
    ], 
    30: [
        {
            "title": "开场剧情结束，通知太一等人开始巡逻", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "go", 
                    "param1": "20014384|20014385|20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
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
                    "param1": "Q051215", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "城门剧情喊话结束，刷火炮", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "move", 
                    "param1": "20014384", 
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
                    "param1": "Q051218", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "破城门剧情结束，通知太一等人go3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "go3", 
                    "param1": "20014384|20014385|20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
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
                    "param1": "Q051219", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "分岔路剧情结束，分头行动/刷传送门/完成阶段4目标1/完成任务目标2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "go6", 
                    "param1": "20014384|20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
                    "param4": "", 
                    "id": 27
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
                    "param2": "2", 
                    "param1": "20102193", 
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
                    "id": 52, 
                    "param1": "Q051230", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "阵眼被毁剧情结束，通知太一等人go5", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "go5", 
                    "param1": "20014384|20014394|20014395|20014396|20014397|20014398|20014399|20014400|20014401", 
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
                    "param1": "Q051226", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ]
}