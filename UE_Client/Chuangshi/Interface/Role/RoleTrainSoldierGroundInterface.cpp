// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleTrainSoldierGroundInterface.h"
#include "../../GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "../../Util/CS3Debug.h"
#include "Entity/Alias.h"
#include "CS3Base/UIManager.h"
#include "GameData/Barracks/RoleArmyData.h"
#include "RoleBarracksInterface.h"
#include "GameData/ConstData.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"

CONTROL_COMPILE_OPTIMIZE_START
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTrainSoldierGroundInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenTrainSoldierGroundDetails, &URoleTrainSoldierGroundInterface::OpenTrainSoldierGroundDetails, const FString&,int32, uint8,const FVariant&, const FVariant&,int32, uint8,int32,const FString&, uint8)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_initTrainGroundQuest, &URoleTrainSoldierGroundInterface::CLIENT_initTrainGroundQuest, const int32&, const TArray<FVariant>&, const TArray<FVariant>&, const TArray<FVariant>&, const TArray<FVariant>&, const TArray<FVariant>&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRefreshTGQuest, &URoleTrainSoldierGroundInterface::CLIENT_OnRefreshTGQuest, const TArray<FVariant>&, const TArray<FVariant>&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenAllGroundDetail, &URoleTrainSoldierGroundInterface::OpenAllGroundDetail, int32, int32,const TArray<FVariant>&,const TArray<FVariant>&,int32,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitGTAttackDatas, &URoleTrainSoldierGroundInterface::InitGTAttackDatas, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitGTProtectDatas, &URoleTrainSoldierGroundInterface::InitGTProtectDatas, const FVariant&, const FVariant&, const TArray<FVariant>&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onDestroyGTBattery, &URoleTrainSoldierGroundInterface::onDestroyGTBattery, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(occupyGTBarrack, &URoleTrainSoldierGroundInterface::occupyGTBarrack, const int8&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onRequestAttackPos, &URoleTrainSoldierGroundInterface::onRequestAttackPos, const FVector&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onRequestAttackPosNone, &URoleTrainSoldierGroundInterface::onRequestAttackPosNone)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTrainSoldierGroundInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleTrainSoldierGroundInterface::URoleTrainSoldierGroundInterface()
{

}

URoleTrainSoldierGroundInterface::~URoleTrainSoldierGroundInterface()
{

}

void URoleTrainSoldierGroundInterface::OpenTrainSoldierGroundDetails(const FString& name, int32 lineNumber, uint8 npcState, const FVariant& warNameList, const FVariant& warProfessionList, int32 isTrainSoldier, uint8 trainGroundType, int32 npcID, const FString& notifyFightTime, uint8 isCanClickCancelDec)
{
	KBEngine::FVariantArray warNameArray = warNameList.GetValue<KBEngine::FVariantArray>();
	TArray<FString> WarNames;
	for (FVariant& element:warNameArray )
	{
		FString value = element.GetValue<FString>();
		WarNames.Add(value);
	}
	KBEngine::FVariantArray warProfessionArray = warProfessionList.GetValue<KBEngine::FVariantArray>();
	TArray<int32> WarProfessions;
	for (FVariant& element : warProfessionArray)
	{
		int32 value = element.GetValue<int32>();
		WarProfessions.Add(value);
	}
	FightTime = notifyFightTime;
	bCanClickCancelDec = bool(isCanClickCancelDec);
	bool isInTrainSoldier = isTrainSoldier > 0 ? true : false;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierDeclareWar"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOpenTrainSoldierGroundDetails.Broadcast(npcID, name, lineNumber, npcState, trainGroundType, WarNames, WarProfessions, isInTrainSoldier);
	}
}

void URoleTrainSoldierGroundInterface::DeclareTrainSoldierGround(const int32& npcID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleTrainSoldierGroundInterface::DeclareTrainSoldierGround no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(npcID);
	entity->CellCall(TEXT("declareTrainSoldierGround"), args);
}

void URoleTrainSoldierGroundInterface::CancelDeclareTrainSoldierGround(const int32& npcID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleTrainSoldierGroundInterface::CancelDeclareTrainSoldierGround no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(npcID);
	entity->CellCall(TEXT("cancelDeclareTrainSoldierGround"), args);
}

void URoleTrainSoldierGroundInterface::RequestTrainGroundQuest()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("requestTrainGroundQuest"), args);
}

void URoleTrainSoldierGroundInterface::CLIENT_initTrainGroundQuest(const int32& NPCID, const TArray<FVariant>& TGQuestList, const TArray<FVariant>& SuccessQuestIndex, const TArray<FVariant>& FailQuestIndex, const TArray<FVariant>& DoingQuestIndex,const TArray<FVariant> & QuestVar)
{
	TGQuestIDArr.Empty();
	SuccessQuestIndexArr.Empty();
	FailQuestIndexArr.Empty();
	DoingQuestIndexArr.Empty();
	for (auto q : TGQuestList)
	{
		TGQuestIDArr.Add(q.GetValue<int32>());
	}
	for (auto s : SuccessQuestIndex)
	{
		SuccessQuestIndexArr.Add(s.GetValue<int32>());
	}
	for (auto f : FailQuestIndex)
	{
		FailQuestIndexArr.Add(f.GetValue<int32>());
	}
	for (auto d : DoingQuestIndex)
	{
		DoingQuestIndexArr.Add(d.GetValue<int32>());
	}
	initQuestDatas(QuestVar);
	//打开练兵任务界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierTask"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		//UUECS3GameInstance::Instance->GEventManager->OnOpenTrainSoldierGroundTask.Broadcast(NPCID);
	}
}

bool URoleTrainSoldierGroundInterface::GetTrainGroundQuestByID(int32 QuestID, FTRAIN_GROUND_QUEST& OutTrainFroundQuest)
{
	if (TrainGroundQuestConfig.Contains(QuestID))
	{
		OutTrainFroundQuest = TrainGroundQuestConfig[QuestID];
		return true;
	}
	return false;
}

int32 URoleTrainSoldierGroundInterface::GetTrainGroundQuestState(int32 Index)
{
	//State 0:未接取,1:正在进行，2:已完成,3:已失败，
	if (DoingQuestIndexArr.Contains(Index))
	{
		return 1;
	} 
	else if (SuccessQuestIndexArr.Contains(Index))
	{
		return 2;
	}
	else if (FailQuestIndexArr.Contains(Index))
	{
		return 3;
	}
	else
	{
		return 0;
	}
}

void URoleTrainSoldierGroundInterface::RequestRefreshTGQuest()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("requestRefreshTGQuest"), args);
}

void URoleTrainSoldierGroundInterface::BeginCalculationAuToRefreshQuest()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (!UUECS3GameInstance::Instance->CustomTimerManager->IsTimerActive(AutoRefreshHandle))
		{
			float sec(0.0f);
			FDateTime _now = FDateTime::Now();
			int32 hour = _now.GetHour();
			for (int32 i : TRAIN_GQUEST_REFRESH_TIME)
			{
				if (hour < i)
				{
					FDateTime autoRefreshTime = FDateTime(_now.GetYear(), _now.GetMonth(), _now.GetDay(), i, 0, 0, 0);
					sec = (autoRefreshTime - _now).GetTotalSeconds();
					if (sec > 0.0f)
					{
						UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(AutoRefreshHandle, this,
							&URoleTrainSoldierGroundInterface::AutoRefreshTGQuest, sec, false);
						return;
					}
				}
			}
			
			
		}
	}
}

void URoleTrainSoldierGroundInterface::EndsCalculationAuToRefreshQuest()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoRefreshHandle);
	}
}

void URoleTrainSoldierGroundInterface::AutoRefreshTGQuest()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("autoRefreshTGQuest"), args);
}

void URoleTrainSoldierGroundInterface::CLIENT_OnRefreshTGQuest(const TArray<FVariant>& TGQuestList, const TArray<FVariant> & QuestVar)
{
	TGQuestIDArr.Empty();
	SuccessQuestIndexArr.Empty();
	FailQuestIndexArr.Empty();
	DoingQuestIndexArr.Empty();
	for (auto q : TGQuestList)
	{
		TGQuestIDArr.Add(q.GetValue<int32>());
	}
	initQuestDatas(QuestVar);

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRefreshTrainSoldierGroundTask.Broadcast();
	}
}

void URoleTrainSoldierGroundInterface::RequestAcceptTGQuest(const int32 & Index, const int32 & battackID)
{
	KBEngine::FVariantArray args;
	args.Add(Index);
	args.Add(battackID);
	CellCall(TEXT("requestAcceptTGQuest"), args);
}

void URoleTrainSoldierGroundInterface::CLIENT_OnAcceptTGQuest_Implementation(const int32 & Index, const int32 & battackID)
{
	DoingQuestIndexArr.Add(Index);
	//更新任务状态State 0:未接取,1:正在进行，2:已完成,3:已失败，
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateTrainSoldierTaskState.Broadcast(Index, 1);
	}
	URoleBarracksInterface* baInterface = Cast<URoleBarracksInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleBarracksInterface::GetName()));
	if (baInterface)
	{
		baInterface->OnArmyDoQuest(battackID);
	}
}

void URoleTrainSoldierGroundInterface::CLIENT_onTGQuestResult_Implementation(const int32 & Index, const int32 & Result, const int32 & Exp, const int32& addExp, const int32 & BattackID, const int32 & LossNum, const int32 & BRefreshAlready)
{
	if (TGQuestIDArr.Num() <= Index)
	{
		return;
	}
	if (DoingQuestIndexArr.Contains(Index))
	{
		DoingQuestIndexArr.Remove(Index);
	}
	if (!BRefreshAlready)
	{
		int32 state = 2;
		if (Result > 0)
		{
			SuccessQuestIndexArr.Add(Index);
		}
		else
		{
			state = 3;
			FailQuestIndexArr.Add(Index);
		}
		//打开战报详情界面
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierWarReport"));
		}
		//更新任务状态State 0:未接取,1:正在进行，2:已完成,3:已失败，
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnUpdateTrainSoldierTaskState.Broadcast(Index, state);
			FString soldierID("");
			if (TGQuestIDArr.Num() >= Index && TrainGroundQuestConfig.Contains(TGQuestIDArr[Index]))
			{
				soldierID = TrainGroundQuestConfig[TGQuestIDArr[Index]].SoldierScriptID;
			}
			UUECS3GameInstance::Instance->GEventManager->OnReceiveTrainSoldierTaskResult.Broadcast(Index, Result, BattackID, Exp, addExp, LossNum, soldierID);
		}
	}
	URoleBarracksInterface* baInterface = Cast<URoleBarracksInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleBarracksInterface::GetName()));
	if (baInterface)
	{
		baInterface->OnArmyDoQuestConsume(BattackID, LossNum);
	}
}

void URoleTrainSoldierGroundInterface::CLIENT_onSoldierFinishQuestBack_Implementation(const int32 & BattackID)
{
	URoleBarracksInterface* baInterface = Cast<URoleBarracksInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleBarracksInterface::GetName()));
	if (baInterface)
	{
		baInterface->OnArmyFinishQuestAndBack(BattackID);
	}
}

void URoleTrainSoldierGroundInterface::OpenAllGroundDetail(int32 InRoleOccupylineNumber, int32 InRoleOccupyIndex, const TArray<FVariant>& AllGroundIndexs, const TArray<FVariant>& AllGroundOccDBIDs, int32 InMaxLineNumber,int32 NpcID)
{
	RoleOccupylineNumber = InRoleOccupylineNumber;
	RoleOccupyIndex = InRoleOccupyIndex;
	AllGroundDict.Empty();
	TArray<int32> tempGroundIndexs;
	for (auto index : AllGroundIndexs)
	{
		tempGroundIndexs.Add(index.GetValue<int32>());
	}
	TArray<FString> tempGroundOccDBIDs;
	for (auto dbid: AllGroundOccDBIDs)
	{
		tempGroundOccDBIDs.Add(dbid.GetValue<FString>());
	}
	for (int32 i = 0; i < tempGroundIndexs.Num(); i++)
	{
		AllGroundDict.Add(tempGroundIndexs[i], tempGroundOccDBIDs[i]);
	}
	if (TrainGroundAreaCfg.Num() <= 0)
	{
		LoadTrainGroundAreaCfgData();
	}
	
}

void URoleTrainSoldierGroundInterface::LoadTrainGroundAreaCfgData()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TRAIN_GROUND_AREA_DATA);
		if (IsValid(ConfigTable))
		{
			TArray<FTRAIN_SOLDIER_GROUND_MAP_DATA*> TrainGroundDatas;
			ConfigTable->GetAllRows(TrainGroundDatas);
			for (auto data : TrainGroundDatas)
			{
				TrainGroundAreaCfg.Add(data->Index, *data);
				for (auto npcData: data->TrainSoldierGroundNpcData)
				{
					if (TrainGroundNPCCfgData.Contains(data->Index))
					{
						if (TrainGroundNPCCfgData[data->Index].Contains(npcData.Group))
						{
							TrainGroundNPCCfgData[data->Index].Remove(npcData.Group);
						}
						TrainGroundNPCCfgData[data->Index].Add(npcData.Group, npcData);
					}
					else
					{
						TMap<int32, FTrainSoldierGroundNpcData> tempNPCData;
						tempNPCData.Add(npcData.Group, npcData);
						TrainGroundNPCCfgData.Add(data->Index, tempNPCData);
					}
				}
			}
		}
	}
}

FTRAIN_SOLDIER_GROUND_MAP_DATA URoleTrainSoldierGroundInterface::GetTrainGroundCfgByIndex(int32 index)
{
	if (TrainGroundAreaCfg.Contains(index))
	{
		return TrainGroundAreaCfg[index];
	}
	FTRAIN_SOLDIER_GROUND_MAP_DATA tempTrainGroundAreaCfg;
	return tempTrainGroundAreaCfg;
}

FTrainSoldierGroundNpcData URoleTrainSoldierGroundInterface::GetTrainGroundNPCCfgData(int32 index, int32 group)
{
	if (TrainGroundNPCCfgData.Contains(index) && TrainGroundNPCCfgData[index].Contains(group))
	{
		return TrainGroundNPCCfgData[index][group];
	}
	FTrainSoldierGroundNpcData tempNPCGrounpData;
	return tempNPCGrounpData;
}

FTrainSoldierGroundNpcData URoleTrainSoldierGroundInterface::GetTrainGroundNPCCfgDataByGroup(int32 group)
{
	FTrainSoldierGroundNpcData tempNPCGrounpData;
	for (auto It : TrainGroundNPCCfgData)
	{
		TMap<int32, FTrainSoldierGroundNpcData> tempTrainSoldierGroundNpcDatas = It.Value;
		if (tempTrainSoldierGroundNpcDatas.Contains(group))
		{
			return tempTrainSoldierGroundNpcDatas[group];
		}
	}
	return tempNPCGrounpData;
}

bool URoleTrainSoldierGroundInterface::IsTrainGroundNPCNeutrally(int32 group)
{
	if (AllGroundDict.Contains(group))
	{
		return FSTRING_TO_INT(AllGroundDict[group]) == 0;
	}
	return false;
}

bool URoleTrainSoldierGroundInterface::IsTrainGroundNPCOccupy(int32 group)
{
	if (AllGroundDict.Contains(group))
	{
		FString playerDBIDStr = INT64_TO_FSTRING(UGolbalBPFunctionLibrary::GetPlayerPlayerDBID());
		return playerDBIDStr == AllGroundDict[group];
	}
	return false;
}

void URoleTrainSoldierGroundInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OpenTrainSoldierGroundDetails");
	ArrBlueFunc.Add("CLIENT_OnAcceptTGQuest");
	ArrBlueFunc.Add("CLIENT_onTGQuestResult");
	ArrBlueFunc.Add("CLIENT_onSoldierFinishQuestBack");
	ArrBlueFunc.Add("OpenAllGroundDetail");
	Supper::InitBlueCB();
}

void URoleTrainSoldierGroundInterface::onLeaveWorld()
{
	AllGroundDict.Empty();
	TrainGroundAreaCfg.Empty();
	Supper::onLeaveWorld();
}

void URoleTrainSoldierGroundInterface::RequestGotoTrainGroundByGroup(int32 lineNumber, int32 group, const FVector& position)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::RequestGotoTrainGroundByGroup : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(lineNumber);
	args.Add(group);
	args.Add(position);
	GetEntity()->CellCall(TEXT("requestGotoTrainGroundByGroup"), args);
}

void URoleTrainSoldierGroundInterface::RequestAllGroundDetail(int32 lineNumber,int32 npcID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleBarracksInterface::RequestAllGroundDetail : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(lineNumber);
	args.Add(npcID);
	GetEntity()->CellCall(TEXT("requestAllGroundDetail"), args);
}

void URoleTrainSoldierGroundInterface::InitGTAttackDatas(const FVariant & BattackVar)
{
	BarrackDatas.Empty();
	bIsBattack = true;
	FBATTACK_MAP BattackData_(BattackVar);
	for (auto& data : BattackData_.dictDatas1)
	{
		for (auto& posData : data.datas2)
		{
			FTG_BARRACK barrack;
			barrack.BelongSide = data.belongSide1;
			barrack.ScriptID = posData.key1;
			barrack.Position = posData.value2;
			BarrackDatas.Add(barrack.ScriptID, barrack);
		}
	}
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnInitGTAttackDatasOver.Broadcast();
	}
}

void URoleTrainSoldierGroundInterface::occupyGTBarrack(const int8 & BelongSide, const FString & ScriptID)
{
	if (BarrackDatas.Contains(ScriptID))
	{
		BarrackDatas[ScriptID].BelongSide = BelongSide;
	}

	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOccupyGTBarrack.Broadcast(BelongSide, ScriptID);
	}
}

void URoleTrainSoldierGroundInterface::InitGTProtectDatas(const FVariant& BattackVar, const FVariant& BatteryVar, const TArray<FVariant>& TeleportPos, const int32& TeleportCD_)
{
	BarrackDatas.Empty();
	bIsBattack = false;
	FBATTACK_MAP BattackData_(BattackVar);
	for (auto& data : BattackData_.dictDatas1)
	{
		for (auto& posData : data.datas2)
		{
			FTG_BARRACK barrack;
			barrack.BelongSide = data.belongSide1;
			barrack.ScriptID = posData.key1;
			barrack.Position = posData.value2;
			BarrackDatas.Add(barrack.ScriptID, barrack);
		}
	}

	FBATTERY_MAP BatteryData_(BatteryVar);
	for (auto& datas : BatteryData_.dictDatas1)
	{
		FTG_BATTERY battery;
		battery.EntityID = datas.entityID1;
		battery.ScriptID = datas.scriptID1;
		battery.State = datas.state2;
		battery.Position = datas.pos3;
		BatteryDatas.Add(battery.EntityID, battery);
	}
	TArray<FVector> TPos;
	for (auto pData : TeleportPos)
	{
		TPos.Add(pData.GetValue<FVector>());
	}
	TeleportCD = TeleportCD_;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnInitGTProtectDatasOver.Broadcast(TPos, TeleportCD);
	}
}

void URoleTrainSoldierGroundInterface::onDestroyGTBattery(const int32& EntityID_)
{
	if (BatteryDatas.Contains(EntityID_))
	{
		BatteryDatas[EntityID_].State = 0;
	}
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnDestroyGTBattery.Broadcast(EntityID_);
	}
}

void URoleTrainSoldierGroundInterface::RequestAttckPos()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("requestAttckPos"), args);
}

void URoleTrainSoldierGroundInterface::onRequestAttackPos(const FVector & Pos)
{
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRequestAttackPos.Broadcast(Pos);
	}
}

void URoleTrainSoldierGroundInterface::onRequestAttackPosNone()
{
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRequestAttackPosNone.Broadcast();
	}
}

void URoleTrainSoldierGroundInterface::RequestTeleportPos(const FVector& TeleportPos)
{
	KBEngine::FVariantArray args;
	args.Add(TeleportPos);
	CellCall(TEXT("requestTeleportPos"), args);

	FTimerHandle tempTimer;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(tempTimer, this,
		&URoleTrainSoldierGroundInterface::TeleportCDIsReady, TeleportCD, false);
}

void URoleTrainSoldierGroundInterface::TeleportCDIsReady()
{
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->TeleportCDIsReady.Broadcast();
	}
}

void URoleTrainSoldierGroundInterface::initQuestDatas(const TArray<FVariant>& QuestVar)
{
	TrainGroundQuestConfig.Empty();
	for (auto it : QuestVar)
	{
		FTRAIN_SOLDIER_QUEST_DICT questData(it);
		FTRAIN_GROUND_QUEST config;
		config.QuestID = questData.questID2;
		config.Title = questData.title1;
		config.TaskTitle = questData.taskTitle3;
		config.Reward = questData.reward4;
		config.SoldierScriptID = questData.soldierScriptID5;
		TrainGroundQuestConfig.Add(config.QuestID, config);
	}
}


CONTROL_COMPILE_OPTIMIZE_END