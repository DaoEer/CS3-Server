# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "刷出批次2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    5: [], 
    8: [
        {
            "title": "完成阶段一", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1008", 
                    "param1": "20012497|20012488|20012528|20012527|20012488|20012593", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001559", 
                    "param4": "", 
                    "id": 19
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
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20012502|20012494", 
                    "param4": "", 
                    "id": 9
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
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1008", 
                    "param1": "20012573", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "19", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 15.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20012572", 
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
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    9: [
        {
            "title": "通关时间小于21分钟发竞速奖励邮件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30-39|40-49|50-59", 
                    "param1": "100000009|100000010|100000011", 
                    "param4": "", 
                    "id": 419
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "jingsu", 
                    "param4": "", 
                    "id": 222
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 59, 
                    "param1": "21", 
                    "param2": "2"
                }
            ], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "离开副本，移除BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12256001|12235301|12235302|12235303|12235304|12235305", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到查询进度指令（阶段一）", 
            "describe": "副本在阶段一 回复 2001 指令", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2001", 
                    "param1": "20012584|20012585|20012586|20012587|20012588", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1001", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012584|20012585|20012586|20012587|20012588"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到查询进度指令（阶段二）", 
            "describe": "副本在阶段二 回复 2002 指令", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2002", 
                    "param1": "20012584|20012585|20012586|20012587|20012588", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1001", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012584|20012585|20012586|20012587|20012588"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到西侧兵营被占领指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 397
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001630", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3002", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到东侧兵营被占领指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 397
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001645", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3000", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到城门楼兵营被占领指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 397
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3001", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "初始化兵营占领行为", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 397
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3003", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到 4071 刷出 第一批 攻城火炮器械", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 9.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4071", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到 4001 西墙攻城梯开车", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001429", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4001", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "收到 4002 西墙攻城梯被摧毁", 
            "describe": "西城墙士兵，提前离场", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001431", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "5004", 
                    "param1": "20012490|20012487|20012491|20012493", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4002", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "收到 4031 西墙攻城梯（火炮开火）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001547", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4031", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "收到 4032 西墙攻城梯（神射手开火）", 
            "describe": "需要修改优化", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001548", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4032", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "收到 2011 西城墙（神射手上前准备射击）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2012", 
                    "param1": "20012487|20012490|20012543", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001548", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2011", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "收到 4003 西墙攻城梯搭建成功", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001430", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 3.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001550", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4003", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到 1013 西城墙防御开始", 
            "describe": "赤盾兵上前，长枪兵将领支援（用指令代替刷批次，批次条目暂时保留）", 
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
                    "param1": "C001549", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2015", 
                    "param1": "20012491|20012493|20012589", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5001", 
                    "param1": "20012485|20012590|20014065|20014066", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5005", 
                    "param1": "20012502|20012494|20014055|20014056", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1013", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到 2016 成尚炎请求支援 刷出批次14", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5007", 
                    "param1": "20012592|20012486", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2016", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "收到 2021 收到指令出现堵门盾兵批次18", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "18", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2021", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "收到 2022 呼叫支援并且刷出批次17", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "17", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2023", 
                    "param1": "20012542", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001556", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2022", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "收到 4011 东墙攻城梯开车", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001433", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4011", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "收到 4012 东墙攻城梯被摧毁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001435", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5005", 
                    "param1": "20012502|20012494|20014055|20014056", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4012", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 19
        }, 
        {
            "title": "收到 4041 东墙攻城梯（火炮开火）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001551", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4041", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 20
        }, 
        {
            "title": "收到 4042 东墙攻城梯（神射手开火）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001552", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4042", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 21
        }, 
        {
            "title": "收到 2013 东城墙（神射手上前准备射击）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2014", 
                    "param1": "20012494|20012502|20012544", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001552", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2013", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 22
        }, 
        {
            "title": "收到 4013 东墙攻城梯搭建成功", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001434", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4013", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 23
        }, 
        {
            "title": "收到 1015 东城墙开始防御", 
            "describe": "（用指令代替刷批次，批次条目暂时保留）", 
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
                    "param1": "C001549", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2031", 
                    "param1": "20014055|20014056|20012484", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5002", 
                    "param1": "20012485|20012590|20014065|20014066", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5004", 
                    "param1": "20012490|20012487|20012491|20012493", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1015", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 24
        }, 
        {
            "title": "收到 2032 成尚禹请求支援 刷出批次35", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "35", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5008", 
                    "param1": "20012592|20012486", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2032", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 25
        }, 
        {
            "title": "收到 2033 收到指令出现堵门盾兵批次39", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "39", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2033", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 26
        }, 
        {
            "title": "收到 2034 呼叫支援并且刷出批次37", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "37", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2035", 
                    "param1": "20012542", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001556", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2034", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 27
        }, 
        {
            "title": "收到 4021 撞车开车", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001437", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4021", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 28
        }, 
        {
            "title": "收到 4022 撞车被摧毁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001439", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5006", 
                    "param1": "20014063|20014064|20012573", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4022", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 29
        }, 
        {
            "title": "收到 4025 撞车火炮开火", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001553", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4025", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 30
        }, 
        {
            "title": "收到 2038 城门破门 防御开始", 
            "describe": "赤盾兵上前，长枪兵将领支援（用指令代替刷批次，批次条目暂时保留）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001438", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2036", 
                    "param1": "20014063|20014064|20012545|20012546", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001626", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 15.0, 
                    "param3": "", 
                    "param2": "5003", 
                    "param1": "20012485|20012590|20014065", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "5003", 
                    "param1": "20014066", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001634", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5012", 
                    "param1": "20014060|20014061|20012600|20012582|20012592|20012486", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "5004", 
                    "param1": "20012490|20012487|20012491|20012493", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "5005", 
                    "param1": "20012502|20012494|20014055|20014056", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2038", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 31
        }, 
        {
            "title": "收到 2037 南宫成请求支援 刷出批次7跟8", 
            "describe": "暂时废弃", 
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
                    "delayTime": 15.0, 
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
                    "param1": "C001634", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2037575", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 32
        }, 
        {
            "title": "收到 4051 第一台器械死亡指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4061", 
                    "param1": "20012562|20012564|20012567", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4051", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 33
        }, 
        {
            "title": "收到 4052 第二台器械死亡指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4062", 
                    "param1": "20012562|20012564|20012567", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4052", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 34
        }, 
        {
            "title": "收到 3026 批次20", 
            "describe": "同时给 火炮车发送指令，给一号门外的巡逻将领发送指令", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12506", 
                    "param1": "20012505|20012489", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001627", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12547", 
                    "param1": "20012549", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3026", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 35
        }, 
        {
            "title": "收到 3006 一号门远程兵入场批次5", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3006", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 36
        }, 
        {
            "title": "收到 3007 一号门背后援兵批次22+语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001628", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001642", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "22", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3007", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 37
        }, 
        {
            "title": "收到 3012 批次 播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001629", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3012", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 38
        }, 
        {
            "title": "收到 3013 批次 24", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "24", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3013", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 39
        }, 
        {
            "title": "收到 3015 批次 26", 
            "describe": "20012519 给副本发送 3015 指令", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "26", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3015", 
                    "param1": "20012520", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001644", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3015", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 40
        }, 
        {
            "title": "收到 3016 批次 27", 
            "describe": "废弃", 
            "actions": [], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3016", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 41
        }, 
        {
            "title": "收到 3022 批次 32", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "32", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001772", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001636", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3022", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 42
        }, 
        {
            "title": "收到 3023 批次 33", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "33", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3023", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 43
        }, 
        {
            "title": "收到 3024 批次 34", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "34", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001639", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001640", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3024", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 44
        }, 
        {
            "title": "收到 3021 语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001632", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3021", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 45
        }, 
        {
            "title": "收到 3025 语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001635", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3025", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 46
        }, 
        {
            "title": "突破西城墙防御，刷出批次15", 
            "describe": "收到6015", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001557", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "6015", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 47
        }, 
        {
            "title": "突破东城墙防御，刷出批次36", 
            "describe": "收到6015", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "36", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001773", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "6036", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 48
        }
    ], 
    15: [
        {
            "title": "出现左边区域F按键", 
            "describe": "出现F按键", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12211301", 
                    "param4": "", 
                    "id": 392
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-7380.0 11260.0|-7380.0 12270.0|-10600.0 12270.0|-10600.0 11260.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "400|0"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "出现右边区域F按键", 
            "describe": "出现F按键", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12211301", 
                    "param4": "", 
                    "id": 392
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8490 11890|12180 11890|12180 11410|8490 114108490 11890|12180 11890|12180 11410|8490 11410", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "400|0"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "突破西城墙防御，给指挥陷阱发送6015", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "6015", 
                    "param1": "20012529", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-10700 11400|-10700 10100|-9740 10100|-9740 11400", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "3170|1575"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "突破东城墙防御，给指挥陷阱发送6036", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "6036", 
                    "param1": "20012529", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "11250 11400|11250 10100|9140 10100|9140 11400", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "3170|1575"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "进入西城楼，触发将领列队表现", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "16", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5009", 
                    "param1": "20012600|20012582|20014061|20014060", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5011", 
                    "param1": "20014057|20014058", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1002", 
                    "param1": "20012543|20012589", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-8700 11400|-8700 9200|-2240 9200|-2240 11400", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "3170|1375"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "进入东城楼，触发将领列队表现", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "38", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5010", 
                    "param1": "20012600|20012582|20014061|20014060", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5011", 
                    "param1": "20014057|20014058", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1002", 
                    "param1": "20012544|20012484", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8340 11400|8340 9200|2640 9200|2640 11400", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "3170|1375"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "进攻东侧兵营 刷出 批次28（中间二号门）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "28", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "12547", 
                    "param1": "20012549", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "10376 -8817|13806 -8817|13806 -11307|10376 -11307", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1237|-500"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "玩家突破二号门防御（中间），刷出29", 
            "describe": "给三号区发送指令", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "29", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4127 -13876|6972 -13876|6972 -20630|4127 -20630", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1500|-100"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "玩家进入范围，兵营换防表现", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3011", 
                    "param1": "20012515|20012516|20012517|20012518", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-3680 -4868|-3680 -10868|-6275 -10868|-6275 -4868", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "800|-200"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "从西城墙进入城内，刷出 批次9", 
            "describe": "", 
            "actions": [], 
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
                    "param4": "", 
                    "param3": "-9442 11967|-9442 5777|-2402 5777|-2402 11967", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2500|-400"
                }
            ], 
            "id": 10
        }, 
        {
            "title": "完成阶段1，进入城内，刷出 批次19", 
            "describe": "废弃", 
            "actions": [], 
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
                    "param4": "", 
                    "param3": "-9542 8218|-9542 -2972|12497 -2972|12497 8218", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2600|-400"
                }
            ], 
            "id": 11
        }, 
        {
            "title": "进入东侧二号门，刷出 批次 30", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "10376 -8817|13806 -8817|13806 -11307|10376 -11307", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1237|-500"
                }
            ], 
            "id": 12
        }, 
        {
            "title": "进入东侧二号门战斗区域，刷出 批次 31", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "31", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001643", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "10869 -13385|13045 -13385|13045 -11400|10869 -11400", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1937|-500"
                }
            ], 
            "id": 13
        }, 
        {
            "title": "玩家进入城门射手范围，射手上去攻击玩家", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001554", 
                    "param4": "", 
                    "id": 256
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2012", 
                    "param1": "20014058|20014057", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-4000 16820|-4000 12820|4800 12820|4800 16820", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1087|-587"
                }
            ], 
            "id": 14
        }, 
        {
            "title": "刷出西侧二号门防守怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "25", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-4694 -6958|14723 -6958|14723 -12660|-4694 -12660", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2600|-200"
                }
            ], 
            "id": 15
        }, 
        {
            "title": "请输入标题", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "27", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-2613 -26090|-2613 -18135|-9152 -18135|-9152 -26090", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2283|283"
                }
            ], 
            "id": 16
        }, 
        {
            "title": "大本营防守", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3019", 
                    "param1": "20012527", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3021", 
                    "param1": "20012532|20012528|20012533", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001633", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-2608 -27885|-11428 -27885|-11428 -37875|-2608 -37875", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2500|500"
                }
            ], 
            "id": 17
        }
    ], 
    21: [
        {
            "title": "进入副本，添加BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12256001", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    23: [
        {
            "title": "玩家被击杀事件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "50", 
                    "param4": "", 
                    "id": 391
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    25: [
        {
            "title": "将领被击杀事件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "50", 
                    "param4": "", 
                    "id": 390
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    27: [
        {
            "title": "取消左边区域F按钮", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12211301", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-7380.0 11260.0|-7380.0 12270.0|-10600.0 12270.0|-10600.0 11260.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "400|0"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "取消右边区域F按钮", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12211301", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8490 11890|12180 11890|12180 11410|8490 11410", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "400|0"
                }
            ], 
            "id": 2
        }
    ], 
    28: [
        {
            "title": "占领大本营通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 393
                }, 
                {
                    "delayTime": 0.0, 
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
                    "id": 43, 
                    "param1": "2", 
                    "param2": "1"
                }
            ], 
            "id": 1
        }
    ]
}