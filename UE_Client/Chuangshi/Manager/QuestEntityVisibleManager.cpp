// Fill out your copyright notice in the Description page of Project Settings.

#include "QuestEntityVisibleManager.h"
#include "Interface/Role/RoleQuestInterface.h"
#include "Manager/VisibleManager.h"
#include"Chuangshi.h"
#include "Manager/CfgManager.h"
#include "Manager/QuestManager.h"

CONTROL_COMPILE_OPTIMIZE_START

UQuestEntityVisibleManager::UQuestEntityVisibleManager() 
{
}

UQuestEntityVisibleManager::~UQuestEntityVisibleManager() 
{
	
}

void UQuestEntityVisibleManager::BeginDestroy()
{
	//释放数据
	for (auto& ConfigData : ConfigDatas)
	{
		for (auto& QuestSituation : ConfigData.Value.QuestSituations)
		{
			delete QuestSituation.Value->InvisibleSituation;
			QuestSituation.Value->InvisibleSituation = nullptr;
			delete QuestSituation.Value->VisibleSituation;
			QuestSituation.Value->VisibleSituation = nullptr;
			delete QuestSituation.Value;
			QuestSituation.Value = nullptr;
		}
	}
	Super::BeginDestroy();
}

UQuestEntityVisibleManager* UQuestEntityVisibleManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UQuestEntityVisibleManager>();
}

void UQuestEntityVisibleManager::LoadEntityVisibleConfig(FString EntityScriptID)
{
	if (ConfigDatas.Contains(EntityScriptID) || NotConfigDatas.Contains(EntityScriptID)) return;	///不重复加载

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_QUEST_ENTITY_VISIBLE);
	const FQEV_CFG_ROW_DATA* RowData = ConfigTable->GetRow<FQEV_CFG_ROW_DATA>(EntityScriptID);
	if (!RowData)
	{
		//CST-10838测试中发现这里打印过于频繁导致影响性能
		//CS3_Warning(TEXT("-->Null Pointer error:UQuestEntityVisibleManager::LoadEntityVisibleConfig : RowData!"));
		NotConfigDatas.Add(EntityScriptID);
		return;
	}

	FQEV_ONE_ENTITY_SITUATION OneEntity;

	FString SplitStr = FString(TEXT("|"));
	FString SplitStr1 = FString(TEXT(";"));
	FString SplitStr2 = FString(TEXT(":"));
	TArray<FString> _tempStr;	///一级分隔符切分得到的字符串数组
	TArray<FString> _tempStr1;	///二级分隔符切分得到的字符串数组
	TArray<FString> _tempStr2;	///三级分隔符切分得到的字符串数组

	///=============可见任务状态QuestSituations.VisibleSituation.QuestStates===========================
	_tempStr = UGolbalBPFunctionLibrary::SplitString(RowData->VisibleQuestState, false, SplitStr);	///格式:任务1；任务状态1；任务状态2|任务2；任务状态1；任务状态2 
	for (FString i : _tempStr)
	{
		_tempStr1 = UGolbalBPFunctionLibrary::SplitString(i, false, SplitStr1);
		if (_tempStr1.Num() < 1)
		{
			return;
		}
		int32 _questID = FSTRING_TO_INT(_tempStr1[0]);
		_tempStr1.RemoveAt(0);

		if (!OneEntity.QuestSituations.Contains(_questID))
		{
			//UQuestEntityVisibleManager::BeginDestroy中释放
			FQEV_ONE_QUEST_SITUATION* _newQuest = new FQEV_ONE_QUEST_SITUATION();
			_newQuest->VisibleSituation = new FQEV_SITUATION_STUCT();
			_newQuest->InvisibleSituation = new FQEV_SITUATION_STUCT();
			OneEntity.QuestSituations.Add(_questID, _newQuest);
		}

		for (auto _state : _tempStr1)
		{
			OneEntity.QuestSituations[_questID]->VisibleSituation->QuestStates.Add(FSTRING_TO_INT(_state));
		}
	}

	///==============不可见任务状态QuestSituations.InvisibleSituation.QuestStates===========================
	_tempStr = UGolbalBPFunctionLibrary::SplitString(RowData->InvisibleQuestState, false, SplitStr);	///格式:任务1；任务状态1；任务状态2|任务2；任务状态1；任务状态2
	for (FString i : _tempStr)
	{
		_tempStr1 = UGolbalBPFunctionLibrary::SplitString(i, false, SplitStr1);
		if (_tempStr1.Num() < 1)
		{
			return;
		}
		int32 _questID = FSTRING_TO_INT(_tempStr1[0]);
		_tempStr1.RemoveAt(0);

		if (!OneEntity.QuestSituations.Contains(_questID))
		{
			//UQuestEntityVisibleManager::BeginDestroy中释放
			FQEV_ONE_QUEST_SITUATION* _newQuest = new FQEV_ONE_QUEST_SITUATION();
			_newQuest->VisibleSituation = new FQEV_SITUATION_STUCT();
			_newQuest->InvisibleSituation = new FQEV_SITUATION_STUCT();
			OneEntity.QuestSituations.Add(_questID, _newQuest);
		}

		for (auto _state : _tempStr1)
		{
			OneEntity.QuestSituations[_questID]->InvisibleSituation->QuestStates.Add(FSTRING_TO_INT(_state));
		}
	}

	///==============可见任务目标状态QuestSituations.VisibleSituation.TaskStates===========================
	_tempStr = UGolbalBPFunctionLibrary::SplitString(RowData->VisibleTaskState, false, SplitStr);	///格式:任务1；目标1：目标状态；目标2：目标状态|任务2；目标1：目标状态；目标2：目标状态 
	for (FString i : _tempStr)
	{
		_tempStr1 = UGolbalBPFunctionLibrary::SplitString(i, false, SplitStr1);
		if (_tempStr1.Num() < 1)
		{
			return;
		}
		int32 _questID = FSTRING_TO_INT(_tempStr1[0]);
		_tempStr1.RemoveAt(0);

		if (!OneEntity.QuestSituations.Contains(_questID))
		{
			//UQuestEntityVisibleManager::BeginDestroy中释放
			FQEV_ONE_QUEST_SITUATION* _newQuest = new FQEV_ONE_QUEST_SITUATION();
			_newQuest->VisibleSituation = new FQEV_SITUATION_STUCT();
			_newQuest->InvisibleSituation = new FQEV_SITUATION_STUCT();
			OneEntity.QuestSituations.Add(_questID, _newQuest);
		}

		for (FString j : _tempStr1) 
		{
			_tempStr2 = UGolbalBPFunctionLibrary::SplitString(j, false, SplitStr2);
			if (_tempStr2.Num() < 2)
			{
				return;
			}
			int32 _taskID = FSTRING_TO_INT(_tempStr2[0]);
			int32 _taskState = FSTRING_TO_INT(_tempStr2[1]);

			if (!OneEntity.QuestSituations[_questID]->VisibleSituation->TaskStates.Contains(_taskID))
			{
				OneEntity.QuestSituations[_questID]->VisibleSituation->TaskStates.Add(_taskID, {});
			}
			OneEntity.QuestSituations[_questID]->VisibleSituation->TaskStates[_taskID].Add(_taskState);
		}

	}

	///==============不可见任务目标状态QuestSituations.InvisibleSituation.TaskStates===========================
	_tempStr = UGolbalBPFunctionLibrary::SplitString(RowData->InvisibleTaskState, false, SplitStr);	///格式:任务1；目标1：目标状态；目标2：目标状态|任务2；目标1：目标状态；目标2：目标状态 
	for (FString i : _tempStr)
	{
		_tempStr1 = UGolbalBPFunctionLibrary::SplitString(i, false, SplitStr1);
		if (_tempStr1.Num() < 1)
		{
			return;
		}
		int32 _questID = FSTRING_TO_INT(_tempStr1[0]);
		_tempStr1.RemoveAt(0);

		if (!OneEntity.QuestSituations.Contains(_questID))
		{
			//UQuestEntityVisibleManager::BeginDestroy中释放
			FQEV_ONE_QUEST_SITUATION* _newQuest = new FQEV_ONE_QUEST_SITUATION();
			_newQuest->VisibleSituation = new FQEV_SITUATION_STUCT();
			_newQuest->InvisibleSituation = new FQEV_SITUATION_STUCT();
			OneEntity.QuestSituations.Add(_questID, _newQuest);
		}

		for (FString j : _tempStr1)
		{
			_tempStr2 = UGolbalBPFunctionLibrary::SplitString(j, false, SplitStr2);
			if (_tempStr2.Num() < 2)
			{
				return;
			}
			int32 _taskID = FSTRING_TO_INT(_tempStr2[0]);
			int32 _taskState = FSTRING_TO_INT(_tempStr2[1]);

			if (!OneEntity.QuestSituations[_questID]->InvisibleSituation->TaskStates.Contains(_taskID))
			{
				OneEntity.QuestSituations[_questID]->InvisibleSituation->TaskStates.Add(_taskID, {});
			}
			OneEntity.QuestSituations[_questID]->InvisibleSituation->TaskStates[_taskID].Add(_taskState);
		}
	}

	///================任务优先级Priority==========================
	if (RowData->Priority == "") 
	{
		if (OneEntity.QuestSituations.Num() > 0)
		{
			TArray<int32> _questIDList;
			OneEntity.QuestSituations.GetKeys(_questIDList);
			OneEntity.Priority.Add(_questIDList[0]);
		}
	}
	else 
	{
		_tempStr = UGolbalBPFunctionLibrary::SplitString(RowData->Priority, false, SplitStr);
		for (FString i : _tempStr) 
		{
			_tempStr1 = UGolbalBPFunctionLibrary::SplitString(i, false, SplitStr1);
			if (_tempStr1.Num() < 1)
			{
				return;
			}
			int32 _questID = FSTRING_TO_INT(_tempStr1[0]);
			if (!OneEntity.QuestSituations.Contains(_questID)) continue;

			OneEntity.Priority.Add(_questID);
			_tempStr1.RemoveAt(0);

			TArray<int32> TaskPriority;
			for (FString j : _tempStr1) 
			{
				TaskPriority.Add(FSTRING_TO_INT(j));
			}
			OneEntity.QuestSituations[_questID]->TaskPriority = TaskPriority;
		}
	}
	ConfigDatas.Add(EntityScriptID, OneEntity);
}

int32 UQuestEntityVisibleManager::GetEntityVisible(const FString& EntityScriptID)
{
	URoleQuestInterface* InterfaceObj = Cast<URoleQuestInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleQuestInterface")));
	if (!InterfaceObj) return -1;

	LoadEntityVisibleConfig(EntityScriptID);	///加载此entity的配置
	if (!ConfigDatas.Contains(EntityScriptID)) return -1;

	FQEV_ONE_ENTITY_SITUATION OneEntity = ConfigDatas[EntityScriptID];

	for (int32 questID : OneEntity.Priority) ///按priority中配置的任务顺序进行判断
	{
		FQEV_ONE_QUEST_SITUATION* OneQuest = OneEntity.QuestSituations[questID];

		///===============先验证任务目标状态===============
		if (InterfaceObj->IsQuestStatus(questID, int(QUEST_STATE::QUEST_NOT_DONE)) ||
			InterfaceObj->IsQuestStatus(questID, int(QUEST_STATE::QUEST_IS_DONE)))
		{
			/// 可见任务目标状态
			bool _findVisTask = false;
			int32 _minVisPriorityIndex = 999;		///可见任务最大优先级（下标最小）
			int32 _minVistaskID = -1;					///可见任务目标最大优先级（下标最小）
			for (auto it = OneQuest->VisibleSituation->TaskStates.CreateIterator(); it; ++it) 
			{
				for (auto state : it.Value()) 
				{
					if (InterfaceObj->IsTaskStatus(questID, it.Key(), state)) 
					{
						_findVisTask = true;
						int32 index = OneQuest->TaskPriority.Find(it.Key());
						if (index != -1 && _minVisPriorityIndex > index) 
						{
							_minVisPriorityIndex = index;
							_minVistaskID = UUECS3GameInstance::Instance->QuestManager->GetTaskPriority(questID, it.Key());
						}
						if (_minVisPriorityIndex == 999)
						{
							_minVistaskID = UUECS3GameInstance::Instance->QuestManager->GetTaskPriority(questID, it.Key());
						}
					}
				}			
			}

			/// 不可见任务目标状态
			bool _findInvisTask = false;
			int32 _minInvisPriorityIndex = 999;		///不可见任务最大优先级（下标最小）
			int32 _minInvistaskID = -1;					///不可见任务目标最大优先级（下标最小）
			for (auto it = OneQuest->InvisibleSituation->TaskStates.CreateIterator(); it; ++it)
			{
				for (auto state : it.Value())
				{
					if (InterfaceObj->IsTaskStatus(questID, it.Key(), state))
					{
						_findInvisTask = true;
						int32 index = OneQuest->TaskPriority.Find(it.Key());
						if (index != -1 && _minInvisPriorityIndex > index)
						{
							_minInvisPriorityIndex = index;
							_minInvistaskID = UUECS3GameInstance::Instance->QuestManager->GetTaskPriority(questID, it.Key());
						}
						if (_minInvisPriorityIndex == 999)
						{
							_minInvistaskID = UUECS3GameInstance::Instance->QuestManager->GetTaskPriority(questID, it.Key());
						}

					}
				}
			}

			if (_findVisTask && !_findInvisTask) { return 1; }
			else if (!_findVisTask && _findInvisTask) { return 0; }
			else if (_findVisTask&&_findInvisTask) 
			{
				if (_minVisPriorityIndex < _minInvisPriorityIndex) { return 1; }
				else if (_minVisPriorityIndex > _minInvisPriorityIndex) { return 0; }
				else if (_minVisPriorityIndex == _minInvisPriorityIndex)
				{
					if (_minInvistaskID > _minVistaskID) { return 0; }
					else if (_minInvistaskID < _minVistaskID) { return 1; }
					else { return -1; }
				}
			}

		}

		///===============任务已完成=========================
		if (InterfaceObj->IsQuestStatus(questID, int(QUEST_STATE::QUEST_IS_DONE)))
		{
			if (OneQuest->VisibleSituation->QuestStates.Contains(int(QUEST_STATE::QUEST_IS_DONE))) { return 1; }	///任务完成可见
			if (OneQuest->InvisibleSituation->QuestStates.Contains(int(QUEST_STATE::QUEST_IS_DONE))) { return 0; }	///任务完成不可见
		}

		///===============任务未完成=========================
		if (InterfaceObj->IsQuestStatus(questID, int(QUEST_STATE::QUEST_NOT_DONE))) 
		{
			if (OneQuest->VisibleSituation->QuestStates.Contains(int(QUEST_STATE::QUEST_NOT_DONE))) { return 1; }///任务未完成可见
			if (OneQuest->InvisibleSituation->QuestStates.Contains(int(QUEST_STATE::QUEST_NOT_DONE))) { return 0; }	///任务未完成不可见
		}

		///===============任务已提交（已做过）===============
		if (InterfaceObj->IsQuestStatus(questID, int(QUEST_STATE::QUEST_HAD_FINISH)))
		{
			if (OneQuest->VisibleSituation->QuestStates.Contains(int(QUEST_STATE::QUEST_HAD_FINISH))) {	return 1; }///任务已提交可见
			if (OneQuest->InvisibleSituation->QuestStates.Contains(int(QUEST_STATE::QUEST_HAD_FINISH))) { return 0; }///任务已提交不可见
		}

	}
	
	return -1;
}

void UQuestEntityVisibleManager::UpdateAroundQuestEntityVisible()
{
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp == nullptr || KbeApp->Entities() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuestEntityVisibleManager::UpdateAroundQuestEntityVisible : KbeApp||KbeApp->Entities()!"));
		return;
	}

	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* _Entity = Elem.Value;
		if (_Entity) 
		{
			UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(_Entity->Actor());
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END
