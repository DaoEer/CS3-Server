// Fill out your copyright notice in the Description page of Project Settings.



#include "RoleLunHuiMiJinInterface.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RolePetInterface.h"
#include "Interface/Role/RoleWorkShopInterface.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/Role/RoleSpaceStageInterface.h"
#include "Component/SpringArmComponentEX.h"
#include "Manager/MessageManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/BuildDepleteData.h"
#include "GameData/LingQuanProduceData.h"
#include "Manager/CfgManager.h"
#include "Manager/EventManager.h"
#include "CS3Base/UIManager.h"
#include "Manager/CustomTimerManager.h"
#include "Interface/Role/RoleInterface.h"
#include "GameData/Item/ItemFactory.h"

CONTROL_COMPILE_OPTIMIZE_START


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleLunHuiMiJinInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_initLHMJBuild, &URoleLunHuiMiJinInterface::CLIENT_initLHMJBuild, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestPlayerDFDatas, &URoleLunHuiMiJinInterface::OnRequestPlayerDFDatas, const int32&, TArray<FVariant>&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestDFDatas, &URoleLunHuiMiJinInterface::OnRequestDFDatas, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestDFDatasByPage, &URoleLunHuiMiJinInterface::OnRequestDFDatasByPage, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowChallengeMsg, &URoleLunHuiMiJinInterface::ShowChallengeMsg, const FVariant&, const int32&, const FVector&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitDongFuData, &URoleLunHuiMiJinInterface::InitDongFuData, const FVariant&, const int32&, const FVector&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenLingQuanUI, &URoleLunHuiMiJinInterface::OpenLingQuanUI, const int32&, const int32&, const int32&, const int32&, const FVariant&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenRepairBuildUI, &URoleLunHuiMiJinInterface::OpenRepairBuildUI, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnEnterOtherCaveHouse, &URoleLunHuiMiJinInterface::OnEnterOtherCaveHouse, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRepairDFBuildFinish, &URoleLunHuiMiJinInterface::OnRepairDFBuildFinish, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onDFActiveEnd, &URoleLunHuiMiJinInterface::onDFActiveEnd)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnDFBeingOccupy, &URoleLunHuiMiJinInterface::OnDFBeingOccupy)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnShowDFActtiveResult, &URoleLunHuiMiJinInterface::OnShowDFActtiveResult, const int8, const int8, const FString&, const int32&, const int32&,const TArray<FVariant>&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowUpgradeGuardMsg, &URoleLunHuiMiJinInterface::ShowUpgradeGuardMsg, const int32&, const int32&, const int32&, int8)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnCloseBatteleFormations, &URoleLunHuiMiJinInterface::CLIENT_OnCloseBatteleFormations)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnGuardReviveTime, &URoleLunHuiMiJinInterface::OnGuardReviveTime, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onDFActiveStart, &URoleLunHuiMiJinInterface::onDFActiveStart, const uint8, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(NoticeMECEnter, &URoleLunHuiMiJinInterface::NoticeMECEnter, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(initDFMonsterInfo, &URoleLunHuiMiJinInterface::initDFMonsterInfo, const TArray<FVariant>&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(addDFMonsterInfo, &URoleLunHuiMiJinInterface::addDFMonsterInfo, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnOccupyPlayerDFCB, &URoleLunHuiMiJinInterface::OnOccupyPlayerDFCB, const uint16, const FString&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleLunHuiMiJinInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void URoleLunHuiMiJinInterface::EnterHSBZModelTPS_Implementation(const int32& skillID)
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(true, TEXT("HSBZ"), INT_TO_FSTRING(skillID));
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
	{
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 550.0f);
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 125.0f));
	}
}

void URoleLunHuiMiJinInterface::LeaveHSBZModelTPS_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(false);
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
	{
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 0.0f));
	}
}

void URoleLunHuiMiJinInterface::OnCatchOriginPetResult_Implementation(const int32& result)
{
	//显示动画提示
	FString tempMessageStr = TEXT("");
	switch (result)
	{
	case 0:
		tempMessageStr = TEXT("CatchFail");
		break;
	case 1:
		tempMessageStr = TEXT("CatchSuccess");
		break;
	default:
		break;
	}

	if (tempMessageStr != TEXT("") && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(FSTRING_TO_FNAME(tempMessageStr));
	}
}

void URoleLunHuiMiJinInterface::TongTinaDaSpaceFailure_Implementation(const int32& difference)
{
}

void URoleLunHuiMiJinInterface::TongTinaDaSpaceSuccess_Implementation(const int32& money, const int32& exp, const FString& itemList, const int32& difference)
{
}

void URoleLunHuiMiJinInterface::OnShowCompassUI_Implementation()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DongfuCompass"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowCompassUIEvent.Broadcast();
	}
}

void URoleLunHuiMiJinInterface::OnNotifyBuildPos_Implementation(const FVector& buildPos, const int32& npcID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnNotifyBuildPosEvent.Broadcast(buildPos, npcID);
	}
}

void URoleLunHuiMiJinInterface::OccupyBuildResult_Implementation(const int32& result)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOccupyBuildResultEvent.Broadcast(result);
	}
}

void URoleLunHuiMiJinInterface::StartBuildCaveHouse_Implementation(const int32& dongfuID, const FString& endStrTime)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DongfuInteractive"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnStartBuildCaveHouseEvent.Broadcast(dongfuID, endStrTime);
	}
}

void URoleLunHuiMiJinInterface::OnEnterCaveHouse_Implementation(const int32& dongfuID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DongfuInteractive"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnEnterCaveHouseEvent.Broadcast(dongfuID, true);
	}
}

void URoleLunHuiMiJinInterface::OpenLingQuanUI(const int32& _ActiveChartID, const int32& LHMJ_CoverHP, const int32& _TotalLingNeng, const int32& _LQCurrHP, const FVariant& DestroyBuild, const int32& NPCID)
{
	caveHousePsionicSum = _TotalLingNeng;
	lingQuanCurrHP = _LQCurrHP;
	ActiveBattleFormationsID = _ActiveChartID;
	FDICT_INT_INTDICT Data(DestroyBuild);
	DestroyBuilds.Empty();
	for (auto It = Data.dictData1.CreateConstIterator(); It; ++It)
	{
		DestroyBuilds.Add(It.Key(), It.Value().dictData1);
	}

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("LingQuan"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OpenLingQuanUIEvent.Broadcast(NPCID);
		UUECS3GameInstance::Instance->GEventManager->OnCaveHousePsionicSumChanged.Broadcast(caveHousePsionicSum);
		UUECS3GameInstance::Instance->GEventManager->OnLingQuanCurrHPChanged.Broadcast(lingQuanCurrHP);
	}
	
	BeginAddPsionicTime();
}

void URoleLunHuiMiJinInterface::OnGuardReviveTime(const int32& ReviveTime)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("LingQuan"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnGuardReviveTime.Broadcast(ReviveTime);
	}
}

void URoleLunHuiMiJinInterface::StartBuildUpgrade_Implementation(const int32& buildType, const FString& endStrTime)
{
	UpLevelBuildType = LHMJ_BUILD_TYPE(buildType);
	FTimespan DstTime = UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime(endStrTime) - FDateTime::Now();
	RemainUpLevelTime = DstTime.GetTotalSeconds();
	if (RemainUpLevelTime <= 0.0f)
	{
		RPC_onUpgradeBuildSuccess(buildType);
	}
	else
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnStartBuildUpgradeEvent.Broadcast(buildType, RemainUpLevelTime);
		}
		UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(UpLevelTimerHandle, this, &URoleLunHuiMiJinInterface::UpdateRemainUpLevelTime, 1.0f, true);
	}
}

void URoleLunHuiMiJinInterface::UpdateRemainUpLevelTime()
{
	RemainUpLevelTime = RemainUpLevelTime - 1;
	if (RemainUpLevelTime <= 0.0f)
	{
		RPC_onUpgradeBuildSuccess((int32)UpLevelBuildType);
		UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(UpLevelTimerHandle);
	}
}

void URoleLunHuiMiJinInterface::_initDongFuDatas(const int32& LineNumber, const FVariant& DFVariant, TArray<FDongFuData>& Datas)
{
	CLIENT_DONGFUDATA_ARR DFDatas(DFVariant);
	if (!DongFuDataMaps.Contains(LineNumber))
	{
		DongFuDataMaps.Add(LineNumber, FDongFuData_Map());
	}
	auto dfArr = DongFuDataMaps[LineNumber].DongFuDatas;
	for (auto data : DFDatas.datas)
	{
		FDongFuData dfData;
		dfData.batteleID = data.batteleID;
		dfData.challengeState = LHMJ_CHANLLENGE_TYPE(data.challengeState);
		dfData.dongFuType = data.dongFuType;
		dfData.group = data.group;
		dfData.level = data.level;
		dfData.playerName = data.playerName;
		dfArr.Add(dfData);
		Datas.Add(dfData);
	}
}

void URoleLunHuiMiJinInterface::_initDongFuData(const FVariant& DFVariant, FDongFuData & Data)
{
	CLIENT_DONGFUDATA DFData_(DFVariant);
	Data.batteleID = DFData_.batteleID;
	Data.challengeState = LHMJ_CHANLLENGE_TYPE(DFData_.challengeState);
	Data.dongFuType = DFData_.dongFuType;
	Data.group = DFData_.group;
	Data.level = DFData_.level;
	Data.playerName = DFData_.playerName;
}

void URoleLunHuiMiJinInterface::_getDongFuDataByPage(const int32& LineNumber, const int32& Page, TArray<FDongFuData>& DongFuArr)
{
	if (DongFuDataMaps.Contains(LineNumber))
	{
		int32 offset = 0;
		if (ChallengeDFData.group)offset += 1;
		if (DFData.group) offset += 1;
		if (DongFuDataMaps[LineNumber].DongFuDatas.Num() >= Page * LHMJ_DONG_FU_SHOW_ENTRY - offset)
		{
			int32 head = FMath::Max((Page - 1) * LHMJ_DONG_FU_SHOW_ENTRY - offset, 0);
			int32 tail = Page * LHMJ_DONG_FU_SHOW_ENTRY - offset;
			for (auto Index = head; Index <= tail; ++Index)
			{
				DongFuArr.Add(DongFuDataMaps[LineNumber].DongFuDatas[Index]);
			}
		}
	}
}

void URoleLunHuiMiJinInterface::CheckDistWithMEC()
{
	auto monster = UGolbalBPFunctionLibrary::GetActorByID(MExtCoverID);
	auto player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(monster) && IsValid(player))
	{
		if (FVector::Dist2D(player->GetActorLocation(), monster->GetActorLocation()) <= 1500.0 )
		{
			UGolbalBPFunctionLibrary::StatusMessage(5814, ChallengeDFData.playerName);
			UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(CheckDistTimerHandle);
		}
	} 
	else
	{
		UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(CheckDistTimerHandle);
	}
}

void URoleLunHuiMiJinInterface::GetBuildDepleteData(LHMJ_BUILD_TYPE buildType, const int32& buildLevel, TArray<int32> &itemList, TArray<int32> &amountList, int32 &depleteMoney, int32 &depletePsionic, int32 &depleteTime)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (!IsValid(CfgManager))
		return;
	const UConfigTable* BuildDepleteTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BULID_DEPLETE_DATA);
	if (!IsValid(BuildDepleteTable))
		return;
	const FBULID_DEPLETE_DATA* BuildData = BuildDepleteTable->GetRow<FBULID_DEPLETE_DATA>(FString::FromInt(buildLevel));
	if (BuildData)
	{
		int32 index = int32(buildType);
		if (BuildData->buildDepleteMoney.Contains(index))
		{
			depleteMoney = BuildData->buildDepleteMoney[index];
		}
		if (BuildData->buildDepletePsionic.Contains(index))
		{
			depletePsionic = BuildData->buildDepletePsionic[index];
		}
		if (BuildData->buildDepleteTime.Contains(index))
		{
			depleteTime = BuildData->buildDepleteTime[index];
		}
		
		

		switch (buildType)
		{
		case LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN://灵泉数据
		{
			for (auto It = BuildData->lingQuan.CreateConstIterator(); It; ++It)
			{
				itemList.Add(It.Key());
				amountList.Add(It.Value());
			}
			break;
		}
		case LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG://工坊数据
		{
			for (auto It = BuildData->gongFang.CreateConstIterator(); It; ++It)
			{
				itemList.Add(It.Key());
				amountList.Add(It.Value());
			}
			break;
		}
		case LHMJ_BUILD_TYPE::LHMJ_BUIILD_QIAN_KU_DING://乾坤鼎数据
		{
			for (auto It = BuildData->qianKuDing.CreateConstIterator(); It; ++It)
			{
				itemList.Add(It.Key());
				amountList.Add(It.Value());
			}
			break;
		}
		case LHMJ_BUILD_TYPE::LHMJ_BUIILD_SHOU_LAN://兽栏数据
		{
			for (auto It = BuildData->shouLan.CreateConstIterator(); It; ++It)
			{
				itemList.Add(It.Key());
				amountList.Add(It.Value());
			}
			break;
		}
		case LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_TIAN://灵田数据
		{
			for (auto It = BuildData->lingTian.CreateConstIterator(); It; ++It)
			{
				itemList.Add(It.Key());
				amountList.Add(It.Value());
			}
			break;
		}
		default:
			break;
		}


	}
}

void URoleLunHuiMiJinInterface::GetLingQuanProduceData(const int32& lingQuanLevel, int32 &timeKey, int32 &outLingNengAmount, int32 &lingNengMaxAmount, int32 &lingQuanMaxHP)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (!IsValid(CfgManager))
		return;
	const UConfigTable* LingQuanProduceTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LINGQUAN_PRODUCE_DATA);
	if (!IsValid(LingQuanProduceTable))
		return;
	const FLINGQUAN_PRODUCE_DATA* LingQuanProduceData = LingQuanProduceTable->GetRow<FLINGQUAN_PRODUCE_DATA>(FString::FromInt(lingQuanLevel));
	timeKey = LingQuanProduceData->timeKey;
	outLingNengAmount = LingQuanProduceData->outLingNengAmount;
	lingNengMaxAmount = LingQuanProduceData->lingNengMaxAmount;
	lingQuanMaxHP = LingQuanProduceData->lingQuanMaxHP;
}

void URoleLunHuiMiJinInterface::OnLHMJWInClose()
{
	ClearPsionicTime();
}

void URoleLunHuiMiJinInterface::RequestLHMJChallenge(const int32& lineNumber, const int32& group)
{
	if (ChallengeLineNumber)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5489);
		return;
	}
	if (IsOccupySpaceType(LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_NONE))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5487);
		return;
	}
	int32 srcLevel = GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN);

	if (!DongFuDataMaps.Contains(lineNumber))return;
	int32 dstLevel = DongFuDataMaps[lineNumber].GetDongFuLevel(group);
	if (srcLevel <= 3)
	{
		if (srcLevel < dstLevel)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5491);
			return;
		}
	}
	else
	{
		if (srcLevel < dstLevel - 1)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5491);
			return;
		}
	}
	KBEngine::FVariantArray args;
	args.Add(lineNumber);
	args.Add(group);
	CellCall(TEXT("requestLHMJChallenge"), args);
}

void URoleLunHuiMiJinInterface::OnRequestLHMJChallenge(const int32& lineNumber, const FString& PlayerName)
{
	ChallengeLineNumber = lineNumber;
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(5492, PlayerName);
}

void URoleLunHuiMiJinInterface::ShowChallenge(const FString& PlayerName, const int32& CanRefuseTime)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DongfuChallengeInvite"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->ReceiveDFChallengeInviteEvent.Broadcast(PlayerName, CanRefuseTime);
	}
}

void URoleLunHuiMiJinInterface::ReplayLHMJChallenge(const int32& replay)
{
	KBEngine::FVariantArray args;
	args.Add(uint8(replay));
	CellCall(TEXT("replayLHMJChallenge"), args);
}

void URoleLunHuiMiJinInterface::onRequestLHMJChallengeReply(const int32& Replay, const FString& PlayerName, const int32& IsPlunder)
{
	if (Replay)
	{
		if (IsPlunder)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5493, PlayerName);
		} 
		else
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5494, PlayerName);
		}
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OtherAcceptDongfuChallengeEvent.Broadcast(PlayerName);
		}
	}
	else
	{
		ChallengeLineNumber = 0;
		if (IsPlunder)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5497, PlayerName);
		}
		else
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5498, PlayerName);
		}
	}
}

void URoleLunHuiMiJinInterface::ShowChallengeMsg(const FVariant& DFVar, const int32& lineNumber, const FVector& Position)
{
	ChallengeLineNumber = lineNumber;
	ChallengeDFPos = KBEMath::KBEngine2UnrealPosition(Position);
	_initDongFuData(DFVar, ChallengeDFData);

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->ShowChallengeMsg.Broadcast(ChallengeDFPos);
	}
}

void URoleLunHuiMiJinInterface::AutoGotoChallengeSpace()
{
	if (ChallengeLineNumber)
	{
		// 同地图寻路
		if (FSTRING_TO_INT( UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_DATA_LINE_NUMBER")) ) == ChallengeLineNumber &&
			UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID"))) == LUN_HUI_MI_JIN_SCRIPTID)
		{
			APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
			if (IsValid(player))
			{
				player->StartAutoNavigate(ChallengeDFPos, 2.0f, LUN_HUI_MI_JIN_SCRIPTID);
			}
		} 
		else
		{
			URolePerformanceInterface* perfomanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URolePerformanceInterface::GetName()));
			if (!IsValid(perfomanceInterface))return;
			TArray<FCROSS_MAP_TARGET_INFO> crossInfos;
			FCROSS_MAP_TARGET_INFO info;
			info.SpaceName = LUN_HUI_MI_JIN_SCRIPTID;
			info.Position = ChallengeDFPos;
			crossInfos.Add(info);
			perfomanceInterface->SetCrossMapTargetInfo(crossInfos);

			KBEngine::FVariantArray args;
			CellCall(TEXT("autoGoToChallengeSpaceDongFu"), args);
		}
	}
}

void URoleLunHuiMiJinInterface::InitDongFuData(const FVariant& DFVar, const int32& lineNumber, const FVector& Position)
{
	DFLineNumber = lineNumber;
	DFPos = Position;
	_initDongFuData(DFVar, DFData);
}

void URoleLunHuiMiJinInterface::AutoGotoDFSpace()
{
	// 同地图寻路
	if (FSTRING_TO_INT(UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_DATA_LINE_NUMBER"))) == DFLineNumber &&
		UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID"))) == LUN_HUI_MI_JIN_SCRIPTID)
	{
		APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
		if (IsValid(player))
		{
			player->StartAutoNavigate(KBEMath::KBEngine2UnrealPosition(DFPos), 2.0f, LUN_HUI_MI_JIN_SCRIPTID);
		}
	}
	else
	{
		URolePerformanceInterface* perfomanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URolePerformanceInterface::GetName()));
		if (!IsValid(perfomanceInterface))return;
		TArray<FCROSS_MAP_TARGET_INFO> crossInfos;
		FCROSS_MAP_TARGET_INFO info;
		info.SpaceName = LUN_HUI_MI_JIN_SCRIPTID;
		info.Position = KBEMath::KBEngine2UnrealPosition(DFPos);
		crossInfos.Add(info);
		perfomanceInterface->SetCrossMapTargetInfo(crossInfos);

		KBEngine::FVariantArray args;
		CellCall(TEXT("autoGoToLHMJSpace"), args);
	}
	
}

void URoleLunHuiMiJinInterface::OnShowDFActtiveResult(const int8 IsChallengeActive, const int8 Result, const FString& RwItemStr, const int32& RwMoney, const int32& RwPsychic, const TArray<FVariant>& _DestroyBuilds, const int32& CombatTime, const int32& DeadCount)
{
	ChallengeDFData.group = 0;
	ChallengeDFData.playerName.Empty();
	ChallengeDFData.level = 0;
	ChallengeLineNumber = 0;
	ChallengeDFPos = FVector::ZeroVector;
	TArray<int32> IDList;
	for (auto& Fva : _DestroyBuilds)
	{
		IDList.Add(Fva.GetValue<int32>());
	}

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DFActtiveResult"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OpenDFActtiveResultUIEvent.Broadcast(IsChallengeActive, Result, RwItemStr, RwMoney, RwPsychic, IDList,CombatTime, DeadCount);
	}
}

void URoleLunHuiMiJinInterface::onDFActiveStart(const uint8 IsPlunderActive, const FString& PlayerName)
{
	BActivityStart = true;
	int32 spaceType = FSTRING_TO_INT(UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_TYPE")));
	if (spaceType == int32(ENUM_SPACE_TYPE::SPACE_TYPE_MULTILINE))
	{
		int MsgID(0);
		if (IsPlunderActive)
		{
			if (ChallengeLineNumber)
			{
				MsgID = 5810;
			}
			else
			{
				MsgID = 5811;
			}
		}
		else
		{
			if (ChallengeLineNumber)
			{
				MsgID = 5812;
			}
			else
			{
				MsgID = 5813;
			}
		}
		TWeakObjectPtr<URoleLunHuiMiJinInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(MsgID, PlayerName, FBtnClick::CreateLambda([DelayThisPtr](RT_BTN_TYPE BtnType)
		{
			if (DelayThisPtr.IsValid())
			{
				if (DelayThisPtr.Get()->ChallengeLineNumber)
				{
					DelayThisPtr.Get()->AutoGotoChallengeSpace();
				}
			}
		}));
	}

	if (MExtCoverID > 0)
	{
		if (!UGolbalBPFunctionLibrary::CustomTimerManager()->IsTimerActive(CheckDistTimerHandle))
		{
			UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(CheckDistTimerHandle, this, &URoleLunHuiMiJinInterface::CheckDistWithMEC, 1.0f, true);
		}
	}
}

void URoleLunHuiMiJinInterface::onDFActiveEnd_Implementation()
{
	BActivityStart = false;
	ChallengeDFData.group = 0;
	ChallengeDFData.playerName.Empty();
	ChallengeDFData.level = 0;
	ChallengeLineNumber = 0;
	ChallengeDFPos = FVector::ZeroVector;
	URoleInterface* interface_ = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleInterface::GetName()));
	if (IsValid(interface_))
	{
		interface_->updateLHMJChanllengeRelation(0);
	}
	URoleSpaceStageInterface* spaceStageInterface_ = Cast<URoleSpaceStageInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleSpaceStageInterface::GetName()));
	if (IsValid(spaceStageInterface_))
	{
		spaceStageInterface_->CLIENT_hideSpaceStageWin();
	}
}

void URoleLunHuiMiJinInterface::NoticeMECEnter(const int32& EntityID_)
{
	MExtCoverID = EntityID_;
	if (BActivityStart)
	{
		if (!UGolbalBPFunctionLibrary::CustomTimerManager()->IsTimerActive(CheckDistTimerHandle))
		{
			UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(CheckDistTimerHandle, this, &URoleLunHuiMiJinInterface::CheckDistWithMEC, 1.0f, true);
		}
	}
}

void URoleLunHuiMiJinInterface::initDFMonsterInfo(const TArray<FVariant>& EntityIDList)
{
	FTimerHandle temp;
	TArray<int32> entityIDList;
	for (auto& Fva : EntityIDList)
	{
		entityIDList.Add(Fva.GetValue<int32>());
	}
	UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(this,temp, FTimerDelegate::CreateLambda([entityIDList]()
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("PuppetList"));
		}
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnInitDFMonsterInfo.Broadcast(entityIDList);
		}
	}), 3.0, false);

	
	
}

void URoleLunHuiMiJinInterface::addDFMonsterInfo(const int32& EntityID_)
{
	FTimerHandle temp;
	UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(this, temp, FTimerDelegate::CreateLambda([EntityID_]()
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("PuppetList"));
		}
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnAddDFMonsterInfo.Broadcast(EntityID_);
		}
	}), 1.5, false);
	
}

void URoleLunHuiMiJinInterface::OnOccupyPlayerDF(const int32& IsOccupy)
{
	KBEngine::FVariantArray args;
	args.Add(IsOccupy);
	CellCall(TEXT("onOccupyPlayerDF"), args);
}

void URoleLunHuiMiJinInterface::OnOccupyPlayerDFCB(const uint16 MsgID, const FString& PlayerName)
{
	FTimerHandle temp;
	TWeakObjectPtr<URoleLunHuiMiJinInterface> DelayThisPtr(this);
	UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(this, temp, FTimerDelegate::CreateLambda([DelayThisPtr, MsgID, PlayerName]()
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(MsgID, PlayerName, FBtnClick::CreateLambda([DelayThisPtr](RT_BTN_TYPE BtnType)
		{
			if (DelayThisPtr.IsValid())
			{
				DelayThisPtr.Get()->AutoGotoDFSpace();
			}
		}));
	}),2.0,false);
}

void URoleLunHuiMiJinInterface::OnDFBeingOccupy()
{
	DFLineNumber = 0;
	DFData.batteleID = 0;
	DFData.playerName = TEXT("");
	DFData.group = 0;
}

void URoleLunHuiMiJinInterface::OpenRepairBuildUI(const int32& buildType, const FVariant& itemVar)
{
	TMap<int32, int32> itemMaps = FDICT_INT_INT(itemVar).dictData1;
}

void URoleLunHuiMiJinInterface::repairDFBuild(const int32 & buildType)
{
	KBEngine::FVariantArray args;
	args.Add(buildType);
	CellCall(TEXT("repairDFBuild"), args);
}

void URoleLunHuiMiJinInterface::OnBeginRepairDFBuild(const int32& buildType, const int32& fixedTime)
{
	FDateTime fixTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(fixedTime);
	FTimespan DstTime = fixTime - FDateTime::Now();
	RemainRepairTime = DstTime.GetTotalSeconds();
	RepairBuildType = LHMJ_BUILD_TYPE(buildType);
	if (RemainRepairTime > 0.0f)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnStartBuildRepairEvent.Broadcast(buildType, RemainRepairTime);
		}
		UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(RepairTimerHandle, this, &URoleLunHuiMiJinInterface::UpdateRemainRepairTime, 1.0f, true);
	}
}

void URoleLunHuiMiJinInterface::UpdateRemainRepairTime()
{
	RemainRepairTime = RemainRepairTime - 1;
	if (RemainRepairTime <= 0.0f)
	{
		RemainRepairTime = 0;
		UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(RepairTimerHandle);
	}
}

void URoleLunHuiMiJinInterface::OnRepairDFBuildFinish(const int32& buildType)
{
	RemainRepairTime = 0;
	if (DestroyBuilds.Contains(buildType))
	{
		DestroyBuilds.Remove(buildType);
	}
	if (RepairTimerHandle.IsValid())
	{
		UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(RepairTimerHandle);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnEndBuildRepairEvent.Broadcast(buildType);
	}
}

void URoleLunHuiMiJinInterface::GetDestroyBuilds(TArray<int32>& BuildArr)
{
	DestroyBuilds.GetKeys(BuildArr);
}

bool URoleLunHuiMiJinInterface::IsDestroyBuild(LHMJ_BUILD_TYPE buildType)
{
	if (DestroyBuilds.Contains((int32)buildType))
	{
		return true;
	}
	return false;
}

void URoleLunHuiMiJinInterface::GetFixBuildCost(const int32& buildType, TMap<int32, int32>& ItemMap)
{
	if (DestroyBuilds.Contains(buildType))
	{
		ItemMap = DestroyBuilds[buildType];
	}
}

void URoleLunHuiMiJinInterface::ShowUpgradeGuardMsg(const int32& MegID, const int32& LingNeng, const int32& MonsterID, int8 mType)
{
	TWeakObjectPtr<URoleLunHuiMiJinInterface> DelayThis(this);
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(MegID, INT_TO_FSTRING(LingNeng), FBtnClick::CreateLambda([DelayThis, MonsterID, mType](RT_BTN_TYPE RtType)
	{
		if (DelayThis.IsValid())
		{
			URoleLunHuiMiJinInterface* interface_ = DelayThis.Get();
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				interface_->UpgradeDFGurard(MonsterID, mType);
			}
		}
	}));
}

void URoleLunHuiMiJinInterface::UpgradeDFGurard(const int32& MonsterID, int8 mType)
{
	KBEngine::FVariantArray args;
	args.Add(MonsterID);
	args.Add(mType);
	CellCall(TEXT("upgradeDFGuard"), args);
}

void URoleLunHuiMiJinInterface::InitBlueCB()
{
	Supper::InitBlueCB();
	ArrBlueFunc.Add("EnterHSBZModelTPS");
	ArrBlueFunc.Add("LeaveHSBZModelTPS");
	ArrBlueFunc.Add("TongTinaDaSpaceFailure");
	ArrBlueFunc.Add("TongTinaDaSpaceSuccess");
	ArrBlueFunc.Add("OnCatchOriginPetResult");
	ArrBlueFunc.Add("OnShowCompassUI");
	ArrBlueFunc.Add("OnNotifyBuildPos");
	ArrBlueFunc.Add("CLIENT_OnLHMJBuildLevelChange");
	ArrBlueFunc.Add("CLIENT_onUpgradeJadeItem");
	ArrBlueFunc.Add("OccupyBuildResult");
	ArrBlueFunc.Add("StartBuildCaveHouse");
	ArrBlueFunc.Add("OnEnterCaveHouse");
	ArrBlueFunc.Add("StartBuildUpgrade");
	ArrBlueFunc.Add("CLIENT_OnActiveBatteleFormations");
	ArrBlueFunc.Add("OnRequestLHMJChallenge");
	ArrBlueFunc.Add("ShowChallenge");
	ArrBlueFunc.Add("onRequestLHMJChallengeReply");
	ArrBlueFunc.Add("OnBeginRepairDFBuild");
}


void URoleLunHuiMiJinInterface::BeginAddPsionicTime()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (!UUECS3GameInstance::Instance->CustomTimerManager->IsTimerActive(AddPsionicTimer))
		{
			int32 timeKey;
			int32 outLingNengAmount;
			int32 lingNengMaxAmount;
			int32 temp;
			GetLingQuanProduceData(GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN), timeKey, outLingNengAmount, lingNengMaxAmount, temp);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(AddPsionicTimer, this, &URoleLunHuiMiJinInterface::AddPsionicPerTime, timeKey * 60, true);
		}
	}
	
}

void URoleLunHuiMiJinInterface::AddPsionicPerTime()
{
	int32 timeKey;
	int32 outLingNengAmount;
	int32 lingNengMaxAmount;
	int32 temp;
	GetLingQuanProduceData(GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN), timeKey, outLingNengAmount, lingNengMaxAmount, temp);
	caveHousePsionicSum = FMath::Min(lingNengMaxAmount, caveHousePsionicSum + outLingNengAmount);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCaveHousePsionicSumChanged.Broadcast(caveHousePsionicSum);
	}
	if (caveHousePsionicSum == lingNengMaxAmount)
	{
		ClearPsionicTime();
	}
}

void URoleLunHuiMiJinInterface::ClearPsionicTime()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AddPsionicTimer);
	}
}

void URoleLunHuiMiJinInterface::RPC_onEnterHSBZModelTPS()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onEnterHSBZModelTPS no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onEnterHSBZModelTPS"), args);
}

void URoleLunHuiMiJinInterface::RPC_onLeaveHSBZModelTPS()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onLeaveHSBZModelTPS no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onLeaveHSBZModelTPS"), args);
}

void URoleLunHuiMiJinInterface::RPC_onAgainChallengeCurrentLayer()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onAgainChallengeCurrentLayer no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onAgainChallengeCurrentLayer"), args);
}

void URoleLunHuiMiJinInterface::RPC_onContinueChallengeLayer()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onContinueChallengeLayer no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onContinueChallengeLayer"), args);
}

void URoleLunHuiMiJinInterface::CLIENT_initLHMJBuild(const int32 & spaceType, const FVariant& BuildVar)
{
	TMap<int32, int32> builds(FDICT_INT_INT(BuildVar).dictData1);
	OccupySpaceType = LHMJ_SPACE_TYPE(spaceType);
	for (auto It = builds.CreateConstIterator(); It; ++It)
	{
		LHMJ_BUILD_TYPE _build = LHMJ_BUILD_TYPE(It.Key());
		Builds.Add(_build, It.Value());
		OnUpdateBuildLevel(_build, It.Value());
	}
	if (OccupySpaceType == LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_PUBLIC)
	{
		int32 level(1);
		if (Builds.Contains(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN))
		{
			level = Builds[LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN];
		}
		OnUpgradeJadeItemBP(level);
	}
	URolePetInterface* petInterface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface")));
	if (IsValid(petInterface))
	{
		petInterface->OnOccypySpaceTypeChange(OccupySpaceType);
	}
	URoleWorkShopInterface* wsInterface = Cast<URoleWorkShopInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleWorkShopInterface")));
	if (IsValid(wsInterface))
	{
		wsInterface->OnOccypySpaceTypeChange(OccupySpaceType);
	}
}

void URoleLunHuiMiJinInterface::RequestPlayerDFDatas()
{
	if (RequestPage > 0)
	{
		return;
	}
	RequestPage = 1;
	DongFuDataMaps.Empty();				// 关闭界面，重新打开！清除数据，重新获取
	KBEngine::FVariantArray args;
	CellCall(TEXT("requestPlayerDFDatas"), args);
}

void URoleLunHuiMiJinInterface::OnRequestPlayerDFDatas(const int32& LineNumber, TArray<FVariant>& AllLineNumber, const int32& TotalPage, const int32& FreeDfNum, const FVariant& DFVari)
{
	TArray<FDongFuData> Datas;
	TArray<int32> LHMJAllLineNumber;
	for (auto& ln : AllLineNumber)
	{
		LHMJAllLineNumber.Add(ln.GetValue<int32>());
	}
	_initDongFuDatas(LineNumber, DFVari, Datas);
	OnFirstShowDFDatas(LineNumber, LHMJAllLineNumber, TotalPage, 1, FreeDfNum, Datas);
	RequestPage = 0;
	RequestLineNumber = 0;
}

void URoleLunHuiMiJinInterface::RequestDFDatas(const int32& LineNumber)
{
	if (RequestPage > 0)
	{
		return;
	}
	TArray<FDongFuData> Datas;
	_getDongFuDataByPage(LineNumber, 1, Datas);
	if (Datas.Num() > 0)
	{
		OnShowDFDatas(LineNumber, 1, Datas);
		return;
	}
	

	RequestPage = 1;
	RequestLineNumber = LineNumber;
	KBEngine::FVariantArray args;
	args.Add(LineNumber);
	CellCall(TEXT("requestDFDatas"), args);
}

void URoleLunHuiMiJinInterface::OnRequestDFDatas(const int32& TotalPage, const int32& FreeDfNum, const FVariant& DFVari)
{
	TArray<FDongFuData> Datas;
	_initDongFuDatas(RequestLineNumber, DFVari, Datas);
	
	OnShowDFDatas(RequestLineNumber, 1, Datas);

	RequestPage = 0;
	RequestLineNumber = 0;
}

void URoleLunHuiMiJinInterface::requestDFDatasByPage(const int32& LineNumber, const int32& Page)
{
	if (RequestPage > 0)
	{
		return;
	}
	TArray<FDongFuData> Datas;
	_getDongFuDataByPage(LineNumber, Page, Datas);
	if (Datas.Num() > 0)
	{
		OnShowDFDatas(LineNumber, 1, Datas);
		return;
	}
	RequestPage = Page;
	RequestLineNumber = LineNumber;
	KBEngine::FVariantArray args;
	args.Add(LineNumber);
	args.Add((int8)Page);
	CellCall(TEXT("requestDFDatasByPage"), args);
}

void URoleLunHuiMiJinInterface::OnRequestDFDatasByPage(const FVariant& DFVari)
{
	TArray<FDongFuData> Datas;
	_initDongFuDatas(RequestLineNumber, DFVari, Datas);
	
	OnShowDFDatas(RequestLineNumber, RequestPage, Datas);
	RequestPage = 0;
	RequestLineNumber = 0;
}

void URoleLunHuiMiJinInterface::OnFirstShowDFDatas(const int32& LineNumber, const TArray<int32>& AllLineNumber, const int32& TotalPage, const int32& Page, const int32& FreeDfNum, const TArray<FDongFuData>& DongFuDatas)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnFirstUpdateDFListDatasEvent.Broadcast(LineNumber, AllLineNumber, TotalPage, Page, FreeDfNum, DongFuDatas);
	}
}

void URoleLunHuiMiJinInterface::OnShowDFDatas(const int32& LineNumber, const int32& Page, const TArray<FDongFuData>& DongFuDatas)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateDFListDatasEvent.Broadcast(LineNumber, Page, DongFuDatas);
	}
}

void URoleLunHuiMiJinInterface::CLIENT_OnLHMJBuildLevelChange_Implementation(const int32 & buildType, const int32 & level)
{
	//升级成功要清除升级剩余时间和timer（正常情况下是客户端倒计时到0再通知服务器升级成功的，这里不清没问题，但GM命令可以直接清除倒计时升级，这里不清就会有问题）
	RemainUpLevelTime = 0;
	if (UpLevelTimerHandle.IsValid())
	{
		UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(UpLevelTimerHandle);
	}

	LHMJ_BUILD_TYPE tempBuildType = LHMJ_BUILD_TYPE(buildType);
	Builds.Add(tempBuildType, level);
	OnUpdateBuildLevel(tempBuildType, level);
	//显示升级提示
	FString tempMessageStr = TEXT("");
	switch (tempBuildType)
	{
	case LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN:
		tempMessageStr = TEXT("HouseUp") + INT_TO_FSTRING(level);
		break;
	case LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG:
		tempMessageStr = TEXT("WorkShopUp") + INT_TO_FSTRING(level);
		break;
	case LHMJ_BUILD_TYPE::LHMJ_BUIILD_QIAN_KU_DING:
		tempMessageStr = TEXT("TripodUp") + INT_TO_FSTRING(level);
		break;
	case LHMJ_BUILD_TYPE::LHMJ_BUIILD_SHOU_LAN:
		tempMessageStr = TEXT("PetPenUp") + INT_TO_FSTRING(level);
		break;
	case LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_TIAN:
		tempMessageStr = TEXT("FieldUp") + INT_TO_FSTRING(level);
		break;
	default:
		break;
	}	
	
	if (tempMessageStr != TEXT("") && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(FSTRING_TO_FNAME(tempMessageStr));
	}
}

void URoleLunHuiMiJinInterface::CLIENT_onUpgradeJadeItem(const int32 & level)
{
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(5394, INT_TO_FSTRING(level));
	Builds.Add(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN, level);
	OnUpgradeJadeItemBP(level);
	FString tempMessageStr = TEXT("LingLongTokenUp") + INT_TO_FSTRING(level);
	if (tempMessageStr != TEXT("") && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(FSTRING_TO_FNAME(tempMessageStr));
	}
}

bool URoleLunHuiMiJinInterface::IsOccupySpaceType(LHMJ_SPACE_TYPE spaceType)
{
	return OccupySpaceType == spaceType;
}

int32 URoleLunHuiMiJinInterface::GetBuildLevel(LHMJ_BUILD_TYPE buildType)
{
	if (IsOccupySpaceType(LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_PUBLIC))
	{
		if (Builds.Contains(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN))
		{
			return Builds[LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_QUAN];
		}
	}
	else if (Builds.Contains(buildType))
	{
		return Builds[buildType];
	}

	return 1;
}

void URoleLunHuiMiJinInterface::OnEnterOtherCaveHouse(const int32& dongfuID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DongfuInteractive"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnEnterCaveHouseEvent.Broadcast(dongfuID, false);
	}
}

void URoleLunHuiMiJinInterface::OnClieckEnterOtherCaveHouse(const int32& dongfuID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onCliskBuildCaveHouse no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(dongfuID);
	entity->CellCall(TEXT("onCliskEnterChallengeCaveHouse"), args);
}

void URoleLunHuiMiJinInterface::RPC_onCliskExplore()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onCliskExplore no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onCliskExplore"), args);
}

void URoleLunHuiMiJinInterface::RPC_onCliskOccupyBuild()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onCliskOccupyBuild no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onCliskOccupyBuild"), args);
}

void URoleLunHuiMiJinInterface::RPC_onCliskBuildCaveHouse(const int32& dongfuID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onCliskBuildCaveHouse no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(dongfuID);
	entity->CellCall(TEXT("onCliskBuildCaveHouse"), args);
}

void URoleLunHuiMiJinInterface::RPC_onCliskEnterCaveHouse(const int32& dongfuID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onCliskEnterCaveHouse no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(dongfuID);
	entity->CellCall(TEXT("onCliskEnterCaveHouse"), args);
}

void URoleLunHuiMiJinInterface::RPC_onReceiveLingNeng()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onReceiveLingNeng no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onReceiveLingNeng"), args);

	// 没有回调函数，只能在这里处理
	caveHousePsionicSum = 0;
	UUECS3GameInstance::Instance->GEventManager->OnCaveHousePsionicSumChanged.Broadcast(caveHousePsionicSum);
	BeginAddPsionicTime();
}

void URoleLunHuiMiJinInterface::RPC_onUpgradeBuild(const int32& buildType, const int32& buildLevel)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onReceiveLingNeng no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(buildType);
	entity->CellCall(TEXT("onUpgradeBuild"), args);
}

void URoleLunHuiMiJinInterface::RPC_onUpgradeBuildSuccess(const int32& buildType)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleLunHuiMiJinInterface::RPC_onReceiveLingNeng no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(buildType);
	entity->CellCall(TEXT("onUpgradeBuildSuccess"), args);
}

void URoleLunHuiMiJinInterface::OpenBattleFormations(const int32 & ItemID)
{
	KBEngine::FVariantArray args;
	args.Add(ItemID);
	CellCall(TEXT("openBattleFormations"), args);
}

void URoleLunHuiMiJinInterface::CLIENT_OnActiveBatteleFormations_Implementation(const int32 & _ActiveChartID, const int32 & LHMJ_CoverHP)
{
	ActiveBattleFormationsID = _ActiveChartID;
	DFData.batteleID = _ActiveChartID;
	BattleFormationsHP = LHMJ_CoverHP;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnActiveBattleFormationsEvent.Broadcast();

		auto itemData = UGolbalBPFunctionLibrary::ItemFactory()->GetStaticDataByItemID(ActiveBattleFormationsID);
		UGolbalBPFunctionLibrary::StatusMessage(5826, itemData.ItemName);
	}
}

void URoleLunHuiMiJinInterface::CloseBattleFormations()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("closeBattleFormations"), args);
	CLIENT_OnCloseBatteleFormations();
}

void URoleLunHuiMiJinInterface::CLIENT_OnCloseBatteleFormations_Implementation()
{
	int32 oldID = ActiveBattleFormationsID;
	ActiveBattleFormationsID = 0;
	BattleFormationsHP = 0;
	DFData.batteleID = 0;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCloseBattleFormationsEvent.Broadcast();

		auto itemData = UGolbalBPFunctionLibrary::ItemFactory()->GetStaticDataByItemID(oldID);
		UGolbalBPFunctionLibrary::StatusMessage(5827, itemData.ItemName);
	}
}

CONTROL_COMPILE_OPTIMIZE_END

