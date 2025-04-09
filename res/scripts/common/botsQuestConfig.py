# -*- coding: UTF-8 -*-
import  LoadModule
import json
import os
PATH = "res/scripts/bots/configObject/taskConfig"


#交任务和接任务行为
def accept_commitAction( qID,actionScript , params=""):
	action = {}	
	action["keyid"] = qID
	action["Script"] = actionScript
	action["param1"] = params
	action["navigateData"] = params
	return action

def loadConfig(questData):
	Datas = {}
	for data in questData:
		for qid,qst in data.items():
			cfg = {}
			actions = {}
			index = 1
			temp = sorted(qst["tasks"],key=lambda t : t["priority"])
			for task in temp:
				scripts = TASK_ACTION_MAP[ task["TaskClass"]]["Action" ].split("|")
				for script in scripts:
					action = {}
					action["Script"] = script
					action["taskID"] = task["id"]
					action["keyid"] = qid
					if "navigateData" in task.keys():
						action["navigateData"] = task["navigateData"]
					else:
						action["navigateData"] = ""
					action["param1"] = task["param1"]
					action["param2"] = task["param2"]
					action["param3"] = task["param3"]
					action["goal"]	 = task["goal"]
					actions[ index ] = action
					index += 1
			keys = sorted(actions.keys())
			AtaskID = 0
			CtaskID = 1
			if keys:
				AtaskID = keys[0]-1
				CtaskID = keys[-1]+1
			Aact = accept_commitAction(qid, "Action9", qst["start_by"])
			actions[AtaskID] = Aact
			Cact = accept_commitAction(qid, "Action10", qst["finish_by"])
			actions[CtaskID] = Cact
			
			cfg["Script"] = "Behaviour2"
			cfg["actions"] = actions
			cfg["nextqid"] = qst["nextQuest"]
			Datas[qid] = cfg
	
			#转换编码写入文件
		#cfgText = cfg.decode()
	cfgStr = json.dumps(Datas)
	cfgStr = cfgStr.replace("},", "},\n")
	file = open(os.path.join(PATH,"quest.py"),"w")
	file.write("Datas=")
	file.write( cfgStr )
	file.close()
	print("Load quests finished, total")



TASK_ACTION_MAP={
"QuestTaskKillMonster" :{"Action":"Action1","Target":"Target1"},
"QuestTaskLearnSkill":{"Action":"Action4","Target":""},
"QuestTaskGetTo":{"Action":"Action3","Target":""},
"QuestTaskEventTrigger":{"Action":"Action5","Target":""},
"QuestTaskDaohengLevel":{"Action":"Action7","Target":""},
"QuestTaskGetItem":{"Action":"Action6","Target":""},
"QuestTaskCommitItem":{"Action":"Action8","Target":""},
"QuestTaskUseSkill":{"Action":"Action12",},
"QuestFuncRemoveItems":{"Action":"Action6",},
"QuestTaskTalkWithNPC":{"Action":"Action13",},
"QuestTaskConjurePet":{"Action":"Action16|Action14",},
"QuestTaskMountPet":{"Action":"Action15",},
"QuestTaskGuessGame":{"Action":"Action0",},
"QuestTaskHuanComonEventTrigger":{"Action":"Action0",},
"QuestUseCommitItem":{"Action":"Action16",},
"QuestTaskPlayerLevel":{"Action":"Action17",},
"QuestTaskXiuweiLevel":{"Action":"Action18",},
"QuestTaskEnterPotentialCopy":{"Action":"Action8","Target":""},
"QuestTaskEnterChuanChengCopy":{"Action":"Action8",},
}


loadConfig( LoadModule.openJsonPathCfg("Quest") )