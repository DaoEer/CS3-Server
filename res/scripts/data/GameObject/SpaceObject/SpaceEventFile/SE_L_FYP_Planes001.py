# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "BOSS死亡，出位面", 
            "describe": "休要得意，魔道是不会放过夸父的......", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046043", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FYP", 
                    "param4": "", 
                    "id": 20
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20102129", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20102130", 
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
                    "param1": "20009132", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "1阶段完成，刷BOSS及表演怪", 
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
            "id": 1
        }
    ], 
    14: [
        {
            "title": "小怪被夸父秒杀", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "88", 
                    "param1": "20009145|20009146|20009147|20009149|20009151|20009152", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "miaosha", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009133"
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "到达有穷部落完成任务目标一", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20102129", 
                    "param4": "", 
                    "id": 15
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20102130", 
                    "param4": "", 
                    "id": 15
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "12106.479492 -44472.429688 791.647949", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1291|291"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "门口小怪喊话", 
            "describe": "又是尔等魔道鼠辈，居然还敢再来有穷部落！\n夸父一天不死，我魔道绝不善罢甘休！\n哼！我叫你们有来无回！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046033|Q046035|Q046036", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "12106.479492 -44472.429688 791.647949", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1291|291"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "触发魔道围攻夸父剧情", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "11", 
                    "param1": "20009145|20009146|20009147|20009149|20009151|20009152", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "11", 
                    "param1": "20009133", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "88", 
                    "param1": "20009132", 
                    "param4": "", 
                    "id": 10
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "3990.044922 -18525.740234 2653.669922", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3153|2153"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家帮助夸父", 
            "describe": "夸父，我来助你一臂之力！\n天地间唯有夸父身具玄月神力，只要将他除去，尔等仙道便休想救回十金乌。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q046039|Q046040|Q046042", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "44", 
                    "param1": "20009144|20009148|20009150", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "99", 
                    "param1": "20009134|20009135|20009136|20009137", 
                    "param4": "", 
                    "id": 10
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
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "3990.044922 -18525.740234 2653.669922", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3153|2153"
                }
            ], 
            "id": 4
        }
    ], 
    28: [
        {
            "title": "1阶段2目标完成，刷长老", 
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
            "id": 1
        }
    ], 
    30: [
        {
            "title": "门口小怪喊话结束，通知怪物进战", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20009141|20009142|20009143", 
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
                    "param1": "Q046036", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}