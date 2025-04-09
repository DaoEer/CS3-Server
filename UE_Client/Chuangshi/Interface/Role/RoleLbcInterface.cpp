// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleLbcInterface.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"
#include "Manager/CfgManager.h"
#include "../../GameData/ShortcutKeyData.h"
#include "../../Actor/Player/PlayerCharacter.h"
#include "../../Util/ConvertUtil.h"
#include "../../Component/SpringArmComponentEX.h"
#include "Entity/Alias.h"
#include "GameData/EnumCsvDefine.h"
#include "Util/GolbalBPFunctionLibrary.h"




CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleLbcInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenLbcMapUI, &URoleLbcInterface::OpenLbcMapUI, const FVariant& , const FVariant& , const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(LbcOccupyCost, &URoleLbcInterface::LbcOccupyCost, const int32&, const int32&, const int32&, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateOccupyInfo, &URoleLbcInterface::UpdateOccupyInfo, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateDeclareInfo, &URoleLbcInterface::UpdateDeclareInfo, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateBeDeclaredInfo, &URoleLbcInterface::UpdateBeDeclaredInfo, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateLbcStatusInfo, &URoleLbcInterface::UpdateLbcStatusInfo, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(NotifyDeclarerFight, &URoleLbcInterface::NotifyDeclarerFight, const int32&, const uint8&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(NotifyOccupierFight, &URoleLbcInterface::NotifyOccupierFight, const int32&, const uint8&, const int32&, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleLbcInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()



void URoleLbcInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}


URoleLbcInterface::URoleLbcInterface()
{
}


void URoleLbcInterface::InitData()
{
	//读取配置
	MaxLineNum = LBC_MAX_LINE;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LBC_DATA);
	if (IsValid(ConfigTable))
	{
		TArray<FLbcDatas*> Datas;
		ConfigTable->GetAllRows(Datas);
		//初始化roleLbcData

		for (int line = 1; line <= MaxLineNum; line++)
		{
			roleLbcData.Add(line, {});
			for (auto item : Datas)
			{
				FRoleLbcData data = FRoleLbcData(item->index, item->level, line, 0, item->lbcName, item->position);
				roleLbcData[line].Add(item->index, data);
			}
		}
	}
}

void URoleLbcInterface::ReqOpenLbcMapUI()
{
	if (roleLbcData.Num() == 0)
	{
		InitData();
	}

	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLBCTaskInterface::ReqOpenLbcMapUI : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("reqOpenLbcMapUI"), args);
}

void URoleLbcInterface::OpenLbcMapUI(const FVariant& occupyInfo, const FVariant& declareInfo, const FVariantArray& statusList)
{
	//更新客户端数据
	OccupyInfo = FLBC_OCCUPY_INFO(occupyInfo);
	DeclareInfo = FLBC_DECLARE_INFO(declareInfo);

	for (FVariant var : statusList)
	{
		FLBC_STATUS temp = FLBC_STATUS(var);
		uint8 line = temp.line;
		uint32 index = temp.index;

		if (!roleLbcData.Find(line) || !roleLbcData[line].Find(index))
		{
			continue;
		}

		//更新状态
		roleLbcData[line][index].status = temp.status;
	}

	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			//打开练兵场区域查看界面
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierGroundMap"));
		}
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnUpdateTrainSoldierGroundAreaDatas.Broadcast();
		}
	}
}
void URoleLbcInterface::ReqGotoLbc(uint8 line, int32 index)
{

	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLBCTaskInterface::ReqGotoLbc : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(line);
	args.Add(index);
	entity->CellCall(TEXT("reqGotoLbc"), args);
}

TMap<int32, FRoleLbcData> URoleLbcInterface::GetLineDatas(uint8 line)
{	
	if (roleLbcData.Find(line))
	{
		return roleLbcData[line];
	}
	return {};
	
}
void URoleLbcInterface::LbcOccupyCost(const int32& level, const int32& amount, const int32& money, const FVariantArray& scriptIDList)
{
	
	for (auto var : scriptIDList)
	{
		FString scriptID = var.GetValue<FString>();
		ScriptIDs.Add(scriptID);
	}

	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			//打开特殊天兵营界面
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("SpecialBarracksWindow"));
			//打开特殊养兵交付界面
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DeliverySoldierWindow"));
		}
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnOpenSpecialBarracks.Broadcast();
			UUECS3GameInstance::Instance->GEventManager->OnShowCommitSoldierAndLevel.Broadcast(level, amount,money);
		}
	}

}

void URoleLbcInterface::ReqSubmitOccupyCost(FString soldierScriptID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLBCTaskInterface::ReqSubmitOccupyCost : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(soldierScriptID);
	entity->CellCall(TEXT("reqSubmitOccupyCost"), args);
}

void URoleLbcInterface::ReqCancelDeclareLbc()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLBCTaskInterface::ReqCancelDeclareLbc : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("reqCancelDeclare"), args);
}

void URoleLbcInterface::UpdateOccupyInfo(const FVariant & occupyInfo)
{
	OccupyInfo = FLBC_OCCUPY_INFO(occupyInfo);
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateOccupyInfo.Broadcast();
	}
}

void URoleLbcInterface::UpdateDeclareInfo(const FVariant & declareInfo)
{
	DeclareInfo = FLBC_DECLARE_INFO(declareInfo);
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateDeclareInfo.Broadcast();
	}
}

void URoleLbcInterface::UpdateBeDeclaredInfo(const FVariant & declareInfo)
{
	BeDeclaredInfo = FLBC_DECLARE_INFO(declareInfo);
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateBeDeclaredInfo.Broadcast();
	}
}

void URoleLbcInterface::UpdateLbcStatusInfo(const FVariant & statusInfo)
{
	FLBC_STATUS temp = FLBC_STATUS(statusInfo);
	uint8 line = temp.line;
	uint32 index = temp.index;

	if (!roleLbcData.Find(line) || !roleLbcData[line].Find(index))
	{
		return;
	}

	//更新状态
	roleLbcData[line][index].status = temp.status;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateLbcStatusInfo.Broadcast();
	}
}

void URoleLbcInterface::NotifyDeclarerFight(const int32& countDown, const uint8& line, const int32& index, const FVariant& declareInfo)
{
	DeclareInfo.index = index;
	DeclareInfo.countDown = countDown;

	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			//打开练兵场争夺开战提示界面 
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierDeclareWar"));
		}
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnNotifyDeclareFight.Broadcast();
		}
	}
}


void URoleLbcInterface::NotifyOccupierFight(const int32& countDown, const uint8& line, const int32& index, const FVariant& declareInfo)
{
	BeDeclaredInfo.index = index;
	BeDeclaredInfo.countDown = countDown;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			//打开练兵场争夺开战提示界面
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierDeclareWar"));
		}
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnNotifyBeDeclaredFight.Broadcast();
		}
	}
}

void URoleLbcInterface::DeclarerGiveUpFight(uint8 line, int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLbcInterface::DeclarerGiveUpFight : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(line);
	args.Add(index);
	entity->CellCall(TEXT("declarerGiveUpFight"), args);
}

void URoleLbcInterface::OccupierGiveUpFight(uint8 line, int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLbcInterface::OccupierGiveUpFight : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(line);
	args.Add(index);
	entity->CellCall(TEXT("occupierGiveUpFight"), args);
}

CONTROL_COMPILE_OPTIMIZE_END