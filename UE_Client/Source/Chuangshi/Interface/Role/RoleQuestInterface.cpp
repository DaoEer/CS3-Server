// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleQuestInterface.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "RoleTalkInterface.h"
#include "GameData/GameDefine.h"
#include "GameData/Item/ItemFactory.h"
#include "Actor/Player/PlayerCharacter.h"
#include "KBEngine.h"
#include "Manager/QuestManager.h"
#include "Manager/VisibleManager.h"
#include "Manager/QuestEntityVisibleManager.h"
#include "Manager/TutorialManager.h"
#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "Manager/SystemSwitchManager.h"
#include "GameData/Quest/ClientQuestInfo.h"
#include "Manager/AudioManager.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleQuestInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestTongDailyQuest, &URoleQuestInterface::OnRequestTongDailyQuest, const int16&, const FVariant&, const FVariant&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnCompleteWhisperQuest, &URoleQuestInterface::OnCompleteWhisperQuest, const int32&, const int32&, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowLoopQuestWin, &URoleQuestInterface::ShowLoopQuestWin)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleQuestInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleQuestInterface::URoleQuestInterface()
{
	
}

URoleQuestInterface::~URoleQuestInterface()
{
}

void URoleQuestInterface::PostInitProperties()
{
	Super::PostInitProperties();
}


void URoleQuestInterface::onEnterWorld()
{
	if (GetEntity() && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->onEnterWorld();
	}
	Supper::onEnterWorld();
}

void URoleQuestInterface::onLeaveWorld()
{
	if (GetEntity() && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->onLeaveWorld();
	}
}

void URoleQuestInterface::ShowLoopQuestSpaceWin_Implementation(const FString& Msg, const FString& Statistics, const FString& RewardStr, const int32& GradeScore, const int32& CountDown, const FString& itemStr, const FString& buff)
{
}

void URoleQuestInterface::ShowDynamicRewards_Implementation(const int32& Money, const int32& Exp)
{
}

void URoleQuestInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onAcceptQuest");
	ArrBlueFunc.Add("onAddQuest");
	ArrBlueFunc.Add("onAbandonQuest");
	ArrBlueFunc.Add("onCommitQuest");
	ArrBlueFunc.Add("onUpdateQuestTask");
	ArrBlueFunc.Add("onRecvQuestLog");
	ArrBlueFunc.Add("onSetQuestContent");
	ArrBlueFunc.Add("onQuestComplete");
	ArrBlueFunc.Add("onRemoveQuestLog");
	ArrBlueFunc.Add("onRemoveQuestLogByType");
	ArrBlueFunc.Add("onClearQuestLog");
	ArrBlueFunc.Add("ShowLoopRewardTip");
	ArrBlueFunc.Add("OnReceiveTongKnowledge");
	ArrBlueFunc.Add("OnKnowledgeAnswerResult");
	ArrBlueFunc.Add("CLIENT_CloseTongKnowledge");
	ArrBlueFunc.Add("ShowLoopQuestSpaceWin");
	ArrBlueFunc.Add("ShowDynamicRewards");
	ArrBlueFunc.Add("StartWhisperQuest");
	ArrBlueFunc.Add("StartTimeQuest");
	ArrBlueFunc.Add("SetQuestTaskDone");
	ArrBlueFunc.Add("ShowTongDailyQuestSpaceWin");
	Supper::InitBlueCB();
}

void URoleQuestInterface::onSetQuestContent(const FString& JsonStr)
{
	FCS3QuestInfo QuestInfo;
	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));
	int32 NpcQuestID = FSTRING_TO_INT(JsonData->GetString(TEXT("questNpcID")));

	GetTalkInfoByJson(JsonStr, QuestInfo);
	OnSetQuestContentBP(QuestInfo, NpcQuestID);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->SetRoleInteractive(true);
	}
}

void URoleQuestInterface::onAcceptQuest(const FString & JsonStr)
{	
	FCS3QuestInfo QuestInfo;

	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));
	int32 ID = FSTRING_TO_INT(JsonData->GetString(TEXT("id")));
	QUEST_TYPE Type = QUEST_TYPE(FSTRING_TO_INT(JsonData->GetString(TEXT("type"))));

	//GetQuestInfoByJson(JsonStr, QuestInfo);

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->AddQuest(JsonStr, Type, ID);
		OnAcceptQuestBP( ID);
		OnQuestStatusChange( ID, QUEST_STATE::QUEST_NOT_DONE);	///任务状态改变 需更新npc头顶任务标识
	}
}

void URoleQuestInterface::onCommitQuest(const int32 & QuestID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		OnCommitQuestBP(QuestID);
		UUECS3GameInstance::Instance->QuestManager->CommitQuest(QuestID);
		OnQuestStatusChange(QuestID, QUEST_STATE::QUEST_HAD_FINISH);
	}
}

void URoleQuestInterface::onAddQuest(const FString & JsonStr)
{
	FCS3QuestInfo QuestInfo;
	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));
	int32 ID = FSTRING_TO_INT(JsonData->GetString(TEXT("id")));
	QUEST_TYPE Type = QUEST_TYPE(FSTRING_TO_INT(JsonData->GetString(TEXT("type"))));

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->AddQuest(JsonStr, Type, ID);
		OnAddQuestBP(ID);

		//onAddQuest为登录时发送的数据，也需要新手指引
		if (UGolbalBPFunctionLibrary::TutorialManager())
		{
			UGolbalBPFunctionLibrary::TutorialManager()->OnChangeQuestState(ID);
		}
		//系统开启
		if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->SystemSwitchManager)
		{
			UUECS3GameInstance::Instance->SystemSwitchManager->OnChangeQuestState(ID);
		}
	}
}

void URoleQuestInterface::onAbandonQuest(const int32 & QuestID)
{
	OnAbandonQuestBP(QuestID);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->DelQuest(QuestID);
		OnQuestStatusChange(QuestID, QUEST_STATE::QUEST_NOT_ACCEPT);
	}
}

void URoleQuestInterface::OnQuestStatusChange(const int32& questID, const QUEST_STATE& newState)
{
	OnQuestStatusChangeBP();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->SetRoleInteractive(false);
	}
	//新手指引
	if (UGolbalBPFunctionLibrary::TutorialManager())
	{
		UGolbalBPFunctionLibrary::TutorialManager()->OnChangeQuestState(questID);
	}
	//系统开启
	if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->SystemSwitchManager)
	{
		UUECS3GameInstance::Instance->SystemSwitchManager->OnChangeQuestState(questID);
	}

	///更新周围SpellBox交互状态
	URoleTalkInterface * talkInterface = Cast<URoleTalkInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTalkInterface")));
	talkInterface->RefreshAroundBoxStatus(int32(SPELL_BOX_LISTEN_EVENT::EVENT_QUEST_CHANGE));

	///更新周围任务相关Entity可见性
	UUECS3GameInstance::Instance->QuestEntityVisibleManager->UpdateAroundQuestEntityVisible();
}

void URoleQuestInterface::onQuestComplete(const int32 & QuestID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->CompleteQuest(QuestID);
		OnQuestCompleteBP(QuestID);
		OnQuestStatusChange(QuestID, QUEST_STATE::QUEST_IS_DONE);
	}
}

void URoleQuestInterface::onRecvQuestLog(const FString & QuestLog)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->OnRecvQuestLog(QuestLog);
	}
}

void URoleQuestInterface::onRemoveQuestLog(const int32 & QuestID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->onRemoveQuestLog(QuestID);
		OnQuestStatusChange(QuestID, QUEST_STATE::QUEST_NOT_DONE);
	}
}

void URoleQuestInterface::onRemoveQuestLogByType(const FString& QuestType)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		//移除相关任务类型 Quest logger 的记录
		UUECS3GameInstance::Instance->QuestManager->ClearQuestLogByType(QuestType);
		//改变改类型的状态为非完成状态。
	}
}


void URoleQuestInterface::onClearQuestLog()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->ClearQuestLog();
		//OnQuestStatusChange();
	}
}

void URoleQuestInterface::onUpdateQuestTask(const int32 & QuestID, const int32& TaskID,const int32& Progress)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->UpdateQuest(QuestID, TaskID, Progress);
		///更新周围SpellBox交互状态
		URoleTalkInterface * talkInterface = Cast<URoleTalkInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTalkInterface")));
		talkInterface->RefreshAroundBoxStatus(int32(SPELL_BOX_LISTEN_EVENT::EVENT_QUEST_CHANGE));

		///更新周围任务相关Entity可见性
		UUECS3GameInstance::Instance->QuestEntityVisibleManager->UpdateAroundQuestEntityVisible();

		if (IsTaskStatus(QuestID, TaskID, (int32)QUEST_TASK_STATE::TASK_IS_DONE))
		{
			onQuestTaskFinish(QuestID, TaskID);
		}
		//OnUpdateTaskDatasBP(QuestID, TaskID, Progress);

		//新手指引
		UGolbalBPFunctionLibrary::TutorialManager()->OnUpdateQuestTaskState(QuestID, TaskID);
	}
}

void URoleQuestInterface::onQuestTaskFinish_Implementation(const int32 & QuestID, const int32& TaskID)
{
	
}

bool URoleQuestInterface::IsQuestType(const int32 & QuestID, int32 Type)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		return UUECS3GameInstance::Instance->QuestManager->IsQuestType(QuestID, Type);
	}
	return false;
}

bool URoleQuestInterface::IsQuestStatus(const int32 & QuestID, int32 Status)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		return UUECS3GameInstance::Instance->QuestManager->IsQuestStatus(QuestID, Status);
	}
	return false;
}

bool URoleQuestInterface::IsTaskStatus(const int32 & QuestID, const int32 & TaskID, int32 Status)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		return UUECS3GameInstance::Instance->QuestManager->IsTaskStatus(QuestID, TaskID, Status);
	}
	return false;
}

void URoleQuestInterface::GetTalkInfoByJson(const FString & JsonStr, FCS3QuestInfo& QuestInfo)
{
	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));
	TArray<FCS3Task> Tasks;

	QuestInfo.ID = FSTRING_TO_INT(JsonData->GetString(TEXT("id")));
	QuestInfo.Type = QUEST_TYPE(FSTRING_TO_INT(JsonData->GetString(TEXT("type"))));

	QuestInfo.State = QUEST_STATE(FSTRING_TO_INT(JsonData->GetString(TEXT("status"))));
	auto QusetTable1 = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_QUEST_DATA);
	const FCS3ClientQuestInfo* questInfo = QusetTable1->GetRow<FCS3ClientQuestInfo>(INT_TO_FSTRING(QuestInfo.ID));
	if (!questInfo)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleQuestInterface::GetTalkInfoByJson : Data!"));
		return ;
	}
	QuestInfo.QuestName = questInfo->Title;
	if (QuestInfo.State == QUEST_STATE::QUEST_IS_DONE)
		QuestInfo.Description = questInfo->FinishTaskDes;
	else
		QuestInfo.Description = questInfo->Description;

	QuestInfo.IsAutoAccept = (INT_TO_FSTRING(questInfo->IsAutoAccept)).ToBool();
	QuestInfo.IsAutoCommit = (INT_TO_FSTRING(questInfo->IsAutoAccept)).ToBool();
	QuestInfo.NextQuestID = FSTRING_TO_INT(questInfo->NextQuest);
	QuestInfo.LogDesc = questInfo->TaskLogDes;

	if (QuestInfo.Type == QUEST_TYPE::QUEST_TYPE_LOOP)
	{
		int taskNum = JsonData->GetStringArray(TEXT("taskID")).Num();
		for (int i = 0; i < taskNum; ++i)
		{ 
			FCS3Task task;
			task.TaskID = FSTRING_TO_INT(JsonData->GetStringArray(TEXT("taskID"))[i]);
			task.Progress = FSTRING_TO_INT(JsonData->GetStringArray(TEXT("progress"))[i]);
			for (int j = 0; j < taskNum; ++j)
			{
				if (task.TaskID != questInfo->Tasks[i].ID)
				{
					continue;
				}
				task.TaskClass = questInfo->Tasks[i].TaskClass;
				task.TaskName = questInfo->Tasks[i].Name;
				task.Goal = questInfo->Tasks[i].Goal;
				
				task.TaskParam1 = questInfo->Tasks[i].Param1;
				task.TaskParam2 = questInfo->Tasks[i].Param1;
				task.TaskParam3 = questInfo->Tasks[i].Param3;
				task.Priority = questInfo->Tasks[i].Priority;
				task.NavigateData = questInfo->Tasks[i].NavigateData;
				Tasks.Add(task);
				break;
			}
		}
		QuestInfo.loopQuestNum = FSTRING_TO_FLOAT(JsonData->GetString((TEXT("loopQuestNum"))));
	}
	QuestInfo.Tasks = Tasks;
	TArray<FCS3RewardInfo> RewardInfos;
	UJsonFieldData* RewardData = JsonData->GetObject(TEXT("rewards"));
	for (FString RewardStr : RewardData->GetObjectKeys(UUECS3GameInstance::Instance->GetWorld()))
	{
		FCS3RewardInfo RewardInfo;
		RewardInfo.Type = REWARED_TYPE(FSTRING_TO_INT(RewardStr));
		if (RewardInfo.Type == REWARED_TYPE::REWARD_TYPE_ITEM_CHOOSE)///<可选任务奖励数据
		{
			TArray<UJsonFieldData*> DataArray = RewardData->GetObjectArray(UUECS3GameInstance::Instance->GetWorld(), RewardStr);
			FString InfoStr = TEXT("");
			for (UJsonFieldData* Data : DataArray)
			{
				FString IndexStr = Data->GetString(TEXT("index"));
				FString DataString = Data->GetString(TEXT("Datas"));
				InfoStr += IndexStr + TEXT("|") + DataString + TEXT("||");
			}
			RewardInfo.Value = InfoStr;
		}
		else
		{
			RewardInfo.Value = RewardData->GetString(RewardStr);
		}
		RewardInfos.Add(RewardInfo);
	}
	QuestInfo.RewardInfo = RewardInfos;
}


void URoleQuestInterface::StartWhisperQuest_Implementation(const int32 & RootQuestID, const int32 & TaskID,  const FString & NpcSoundID, const FString & StartSoundID, const FString & Dialogue)
{
	RumorQuestID = RootQuestID;
	RumorTaskID = TaskID;
	PlayerSoundID = StartSoundID;
	RumorDialogue = Dialogue;	
		
}

void URoleQuestInterface::StartTimeQuest_Implementation(const FString & StrTime, const int32 & QuestID)
{

}

void URoleQuestInterface::OnCompleteWhisperQuest(const int32& QuestID, const int32& TaskID, const uint8& IsSucced)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		UUECS3GameInstance::Instance->AudioManager->SetIsPlayRumorVoice(false);
	}
	OnCompleteWhisperQuestBP(QuestID,TaskID, bool(IsSucced));
	RumorQuestID = 0;
	RumorTaskID = 0;
	PlayerSoundID = TEXT("");
	RumorDialogue = TEXT("");
}

void URoleQuestInterface::OnCompleteWhisperQuestBP_Implementation(const int32& QuestID, const int32& TaskID, const bool IsSucced)
{
	
}

void URoleQuestInterface::SetQuestTaskDone(const int32 & QuestID, const int32& TaskID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuestManager))
	{
		UUECS3GameInstance::Instance->QuestManager->SetQuestTaskDone(QuestID, TaskID);
	}
}

void URoleQuestInterface::RPC_completeWhisperQuest(const int32 & RootQuestID, const int32 & TaskID, const int32 & IsSucced)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_completeWhisperQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(RootQuestID);
	args.Add(TaskID);
	args.Add(IsSucced);
	entity->CellCall(TEXT("completeWhisperQuest"), args);
}


void URoleQuestInterface::ShowLoopQuestWin()
{
  if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
  {
     UUECS3GameInstance::Instance->GEventManager->OnShowLoopQuestWin.Broadcast();
  }
}

UItemBase * URoleQuestInterface::getItemByDataString(const FString & dataString, const int32 & itemId)
{
	if (dataString.IsEmpty())return nullptr;
	FString jsonStr = dataString.Replace(TEXT("/"), TEXT("|"));
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(jsonStr);
	auto itemdata = returnvalue->GetObject(TEXT("ROOT"));
	UItemBase* ItemBase = UItemFactory::GetItemByID(itemId);
	if (IsValid(ItemBase) && ItemBase->IsEquip())
	{
		UEquip* Equip = Cast<UEquip>(ItemBase);
		Equip->Amount = FSTRING_TO_INT(itemdata->GetString(TEXT("amount")));
		Equip->BindType = FSTRING_TO_INT(itemdata->GetString(TEXT("bindType")));
		Equip->Hardiness = FSTRING_TO_INT(itemdata->GetString(TEXT("hardiness")));
		Equip->CombatPower = FSTRING_TO_INT(itemdata->GetString(TEXT("combatPower")));
		Equip->AttackPropertiesStr = itemdata->GetString(TEXT("attackProperties"));
		Equip->AttachPropertiesStr = itemdata->GetString(TEXT("attachProperties"));
		return Equip;
	}
	else
	{
		ItemBase->Amount = FSTRING_TO_INT(itemdata->GetString(TEXT("amount")));
		ItemBase->BindType = FSTRING_TO_INT(itemdata->GetString(TEXT("bindType")));
		return ItemBase;
	}
	return nullptr;
}


void URoleQuestInterface::OnRequestTongDailyQuest(const int16& AcceptIndex, const FVariant& FinishQuestidData, const FVariant& TreeJson, const FVariant& TreeNodeMapQuest)
{
	UQuestManager* questMgr = UUECS3GameInstance::Instance->QuestManager;
	if (!IsValid(questMgr))return;
	KBEngine::FVariantMap variantMap = FinishQuestidData.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("data")].GetValue<KBEngine::FVariantArray>();
	TArray<int32> FinishQuestIndexs;
	for (FVariant& signRewards : variantArray_Data)
	{
		int32 QuestID = signRewards.GetValue<int32>();
		FinishQuestIndexs.Add(QuestID);
	}
	FDICT_INT_INT32_LIST NodeMapQuest(TreeNodeMapQuest);
	FDICT_INT_INT32_LIST TreeQest(TreeJson);

	TArray<int32> HasLoadTreeNode;
	TArray<FTongDailyQuestTreeDATA> TreeData;
	for(int i = 0; i <= 2; i++)
	{
		int layer(0);
		TArray<int32> NodeArr;
		TArray<int32> NextNodeArr;
		if (NodeMapQuest.dictData1.Contains(i) && TreeQest.dictData1.Contains(i))
		{
			NextNodeArr = TreeQest.dictData1[i];
			FTongDailyQuestTreeDATA data;
			data.layer = layer;
			data.nodeIndex = i;
			if (NodeMapQuest.dictData1[i].Num() >= 2)
			{
				data.questID = NodeMapQuest.dictData1[i][0];
				data.genre = NodeMapQuest.dictData1[i][1];
				const FCS3ClientQuestInfo* questInfo = questMgr->GetQuestConfig(data.questID);
				if (questInfo)
				{
					data.title = questInfo->Title;
				}
				data.route = NextNodeArr;
			}
			TreeData.Add(data);
		}
		while (NextNodeArr.Num() > 0)
		{
			layer += 1;
			NodeArr = NextNodeArr;
			NextNodeArr.Empty();
			for (int node : NodeArr)
			{
				if (HasLoadTreeNode.Contains(node))continue;
				HasLoadTreeNode.Add(node);
				if (NodeMapQuest.dictData1.Contains(node) && TreeQest.dictData1.Contains(node))
				{
					NextNodeArr.Append(TreeQest.dictData1[node]);
					FTongDailyQuestTreeDATA data;
					data.layer = layer;
					data.nodeIndex = node;
					if (NodeMapQuest.dictData1[node].Num() >= 2)
					{
						data.questID = NodeMapQuest.dictData1[node][0];
						data.genre = NodeMapQuest.dictData1[node][1];
						const FCS3ClientQuestInfo* questInfo = questMgr->GetQuestConfig(data.questID);
						if (questInfo)
						{
							data.title = questInfo->Title;
						}
						data.route = TreeQest.dictData1[node];
					}
					TreeData.Add(data);
				}
			}
		}
	}
	BP_OnReceiveTongDailyQuest((int32)AcceptIndex, FinishQuestIndexs, TreeData);
}

void URoleQuestInterface::OnReceiveTongKnowledge_Implementation(const int32& questID, const int32& currentQuestionID, const FString& currentDescription, const FString& currentOption)
{
	TArray<FString> currentOptionLists;
	TArray<TSharedPtr<FJsonValue>> JsonParsed;
	TSharedRef< TJsonReader<TCHAR> > JsonReader = TJsonReaderFactory<TCHAR>::Create(currentOption);
	bool bFlag = FJsonSerializer::Deserialize(JsonReader, JsonParsed);
	if (bFlag)
	{
		for (auto data : JsonParsed)
		{
			currentOptionLists.Add(data->AsString());
		}
	}
	OnReceiveTongKnowledgeBP(questID, currentQuestionID, currentDescription, currentOptionLists);
}
void URoleQuestInterface::OnKnowledgeAnswerResult_Implementation(const int32& questionID, const uint8& Result)
{

}
void URoleQuestInterface::CLIENT_CloseTongKnowledge_Implementation()
{

}

void URoleQuestInterface::RPC_rquestToAcceptQuest(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_rquestToAcceptQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("rquestToAcceptQuest"), args);
}

void URoleQuestInterface::RPC_requestToCommitQuest(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_requestToCommitQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("requestToCommitQuest"), args);
}

void URoleQuestInterface::RPC_requestToAbandonQuest(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_requestToAbandonQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("requestToAbandonQuest"), args);
}

void URoleQuestInterface::RPC_questChooseReward(const FString& STRING_1, const FString& STRING_2, const FString& STRING_3)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_questChooseReward : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);
	args.Add(STRING_3);

	entity->CellCall(TEXT("questChooseReward"), args);
}

void URoleQuestInterface::RPC_requestTongDailyQuest(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_requestTongDailyQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	entity->CellCall(TEXT("requestTongDailyQuest"), args);
}

void URoleQuestInterface::RPC_acceptTongDailyQuest(const int32& BeforeNodeIndex, const int32& AcceptNodeIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_acceptTongDailyQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(BeforeNodeIndex);
	args.Add(AcceptNodeIndex);

	entity->CellCall(TEXT("acceptTongDailyQuest"), args);
}

void URoleQuestInterface::RPC_playerAnswerTongQuestion(const int32& QUESTID_1, const int32& INT32_1, const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_playerAnswerTongQuestion : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(QUESTID_1);
	args.Add(INT32_1);
	args.Add(STRING_1);

	entity->CellCall(TEXT("playerAnswerTongQuestion"), args);
}

void URoleQuestInterface::RPC_selectNextTongQuestion(const int32& QUESTID_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RPC_selectNextTongQuestion : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(QUESTID_1);

	entity->CellCall(TEXT("selectNextTongQuestion"), args);
}

void URoleQuestInterface::RPC_CELL_stopTongQuestion(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleQuestInterface::RPC_CELL_stopTongQuestion no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("stopTongQuestion"), args);
}

void URoleQuestInterface::RPC_broadcastQuestEvent(FString QuestID, FString TaskID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleQuestInterface::RPC_broadcastQuestEvent no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(QuestID);
	args.Add(TaskID);

	entity->CellCall(TEXT("broadcastQuestEvent"), args);
}

void URoleQuestInterface::ShowTongDailyQuestSpaceWin_Implementation(const FString& Msg, const FString& Statistics, const FString& RewardStr, const int32& GradeScore, const int32& CountDown, const FString& itemStr, const FString& buff)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("LoopQuestSettlement"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowTongDailyQuestSpaceWin.Broadcast(Msg, Statistics, RewardStr, GradeScore,CountDown,itemStr,buff);
	}
}