// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleSpaceContentInterface.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/BaseWindow.h"
#include "Kismet/KismetMathLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/QTEManager.h"
#include "CS3Base/UIManager.h"
#include "Manager/ParticleManager.h"
#include "Manager/AudioManager.h"
#include "Manager/AtkStateMar.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Component/SpringArmComponentEX.h"
#include "Manager/MapManager.h"
#include "Manager/QuestManager.h"
#include "GameData/GameDeFine.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/SkillManager.h"
#include "GameData/Skill/SkillData.h"
#include "GameData/Skill/SkillTableData.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameData/Item/ItemFactory.h"
#include "Component/AppearanceComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameData/AttCityFightData.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"
#include "Engine/EngineTypes.h"
#include "Component/Role/JumpComponent.h"
#include "Component/CollisionComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/VisibleManager.h"
#include "Actor/Particle/EffectEmitter.h"
#include "../Monster/MonsterExtJZZYXYInterface.h"
#include "Manager/EventManager.h"
#include "../../GameData/ShortcutKeyData.h"
#include "Actor/SpellBox/EquipBuildClientCharacter.h"
#include "Manager/MessageManager.h"
#include "Component/Role/FlyPatrolComponent.h"
#include "../GameObjectInterface.h"
#include "Entity.h"
#include "Entity/NPC/MovingPlatformVehicle.h"
#include "NameTypes.h"
#include "Actor/Scene/MovingPlatformVehicleCharacter.h"
#include "GameData/CharacterData.h"
#include "Component/FilterActorComponent.h"
#include "Entity/Alias.h"


CONTROL_COMPILE_OPTIMIZE_START


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleSpaceContentInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnOpenBarracksArmyWin, &URoleSpaceContentInterface::CLIENT_OnOpenBarracksArmyWin, const FVariant&,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnEnterTrainSoldierGround, &URoleSpaceContentInterface::CLIENT_OnEnterTrainSoldierGround, float, FVector)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnLeaveTrainSoldierGround, &URoleSpaceContentInterface::CLIENT_OnLeaveTrainSoldierGround)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowFireCowAngerUI, &URoleSpaceContentInterface::ShowFireCowAngerUI, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowTongSpaceSettlementWin, &URoleSpaceContentInterface::ShowTongSpaceSettlementWin, const int32&, const int32&, const int32&, const int32&, const int32&, const FString&, const FString&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CollectedXLC, &URoleSpaceContentInterface::CollectedXLC, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpDateGCZMemberSoldierDeadNumToClient, &URoleSpaceContentInterface::CLIENT_UpDateGCZMemberSoldierDeadNumToClient, int32,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnOpenWindow, &URoleSpaceContentInterface::OnOpenWindow, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnEnterEquipBuild, &URoleSpaceContentInterface::OnEnterEquipBuild, const FString&, const FString&, const float&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnMountVehicle, &URoleSpaceContentInterface::CLIENT_OnMountVehicle, int32, int32, const FString&, const FString&, uint8)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnDismountVehicle, &URoleSpaceContentInterface::CLIENT_OnDismountVehicle, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_ShowTongPlunderSettlementWnd, &URoleSpaceContentInterface::CLIENT_ShowTongPlunderSettlementWnd, const int32&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_TongPlunderSoldierDead, &URoleSpaceContentInterface::CLIENT_TongPlunderSoldierDead, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_ShowJSSLCJiYuanJieSuanWnd, &URoleSpaceContentInterface::CLIENT_ShowJSSLCJiYuanJieSuanWnd, const int32&, const int32&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_PlaySound, &URoleSpaceContentInterface::CLIENT_PlaySound, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_PlayEffect, &URoleSpaceContentInterface::CLIENT_PlayEffect, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_ShowCurrGotGoldAmount, &URoleSpaceContentInterface::CLIENT_ShowCurrGotGoldAmount, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SetYCJMDBulletSlotMax, &URoleSpaceContentInterface::SetYCJMDBulletSlotMax, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CreateTempEquipBar, &URoleSpaceContentInterface::CreateTempEquipBar, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RemoveTempEquipBar, &URoleSpaceContentInterface::RemoveTempEquipBar)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnStartYCJMDSkyFlyModel, &URoleSpaceContentInterface::OnStartYCJMDSkyFlyModel, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SetIsEnabledQuickBar, &URoleSpaceContentInterface::SetIsEnabledQuickBar, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowZYJJReward, &URoleSpaceContentInterface::ShowZYJJReward, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowYCJMDFinalUI, &URoleSpaceContentInterface::ShowYCJMDFinalUI)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleSpaceContentInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(parachutingState, &URoleSpaceContentInterface::Set_ParachuteState, uint8)
CS3_END_INTERFACE_PROPERTY_MAP()

void URoleSpaceContentInterface::ZhenLongQiJu_OnBossStateChange_Implementation(const int32& state, const int32& bossEntityID, const FString& effectID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("state = %i,entityID = %i------------>>>"), state, bossEntityID);

	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;

	AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(bossEntityID);
	if (!IsValid(actor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::ZhenLongQiJu_OnBossStateChange_Implementation : actor!"));
		return;
	}

	ParticleManager->StopEffectByUID(CurEffectUID);
	/*if (CurEffect)
	{
		CurEffect->Stop();
		CurEffect = nullptr;
	}*/

	CurEffectUID = ParticleManager->PlayParticle(effectID, 0.0f, actor, actor);
	ZhenLongQiJu_OnBossStateChangeBP(state);
}

void URoleSpaceContentInterface::ZhenLongQiJu_OnBossHPChange_Implementation(const int32& hp_Max, const int32& currentHP)
{

}

void URoleSpaceContentInterface::ZhenLongQiJu_StopBossStateChange_Implementation()
{
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(CurEffectUID);
	/*if (CurEffect)
	{
		CurEffect->Stop();
		CurEffect = nullptr;
	}*/
	UGUIManager* uiManager = UGolbalBPFunctionLibrary::GUIManager();
	if (uiManager)
	{
		UBaseWindow* window = uiManager->GetWindow(TEXT("ZhenlongqijuHpBar"));
		if (window)
		{
			window->Hide();
		}
	}
}

void URoleSpaceContentInterface::ZhenLongQiju_ClearData_Implementation()
{
	///离开副本清空光效数据
	CurEffectUID = -1;
}

void URoleSpaceContentInterface::OnMountHeHua_Implementation(int32 heHuaType)
{
	bIsMovingOnHeHua = false;
	bIsMovingToCallCellOnHeHua = false;
}

void URoleSpaceContentInterface::MoveToTargetPosition_Implementation(const FVector& dstPos)
{
	bIsMovingOnHeHua = true;
	bIsMovingToCallCellOnHeHua = true;
}

void URoleSpaceContentInterface::DismountHeHua_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		FName ActionId = "Show_FloatGetoff";
		PlayerActor->PlayAction(ActionId);
	}
	bIsMovingOnHeHua = false;
	bIsMovingToCallCellOnHeHua = false;
}
void URoleSpaceContentInterface::OnDismountHeHua()
{
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("URolePerformanceInterface::OnDismountHeHua --- PlayerActor is Null !"));
		return;
	}
	//移动状态下不可以下荷花
	if (FMath::IsNearlyZero(UKismetMathLibrary::VSize(PlayerActor->GetVelocity())))
	{
		KBEngine::Entity* Player = PlayerActor->GetSelfEntity();
		if (Player == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::OnDismountHeHua : Player!"));
			return;
		}
		KBEngine::FVariantArray Args;

		Player->CellCall(TEXT("dismountHeHua"), Args);
	}
}

bool URoleSpaceContentInterface::IsMovingCallCellOnHeHua()
{
	if (!bIsMovingOnHeHua && !bIsMovingToCallCellOnHeHua)
	{
		return true;
	}
	return false;
}

bool URoleSpaceContentInterface::OnPlayerMoveTypeChange_Implementation(CS3_MOVE_TYPE NewMoveType, CS3_MOVE_TYPE OldMoveType)
{
	return true;
}

void URoleSpaceContentInterface::ShowCircleHPPercentBar_Implementation(UINT8 isOpen, int32 percent)
{

}

void URoleSpaceContentInterface::CLIENT_OnPremierHPChanged_Implementation(int32 index, int32 percent)
{

}

void URoleSpaceContentInterface::CLIENT_onCalculateResults_Implementation(int32 result)
{

}

void URoleSpaceContentInterface::CLIENT_MagicMazeAnswerQuestionEnd_Implementation(const FString& questionResults)
{
	TArray<FMAGICMAZEQUESTION_RESULT_DATA> QuestionResultLists;
	TArray<TSharedPtr<FJsonValue>> JsonParsed;
	TSharedRef< TJsonReader<TCHAR> > JsonReader = TJsonReaderFactory<TCHAR>::Create(questionResults);
	bool bFlag = FJsonSerializer::Deserialize(JsonReader, JsonParsed);
	if (bFlag)
	{
		for (auto data : JsonParsed)
		{
			FMAGICMAZEQUESTION_RESULT_DATA QuestionResult;
			TSharedPtr<FJsonObject> DataObject = data->AsObject();
			QuestionResult.PlayerName = DataObject->GetStringField("playerName");
			QuestionResult.Profession = DataObject->GetIntegerField("profession");
			QuestionResult.Right = DataObject->GetIntegerField("right");
			QuestionResult.Error = DataObject->GetIntegerField("error");
			QuestionResult.Time = DataObject->GetIntegerField("time");
			QuestionResultLists.Add(QuestionResult);
		}
	}
	OnMagicMazeAnswerQuestionEnd(QuestionResultLists);
}

void URoleSpaceContentInterface::CLIENT_ReceiveQuestion_Implementation(const int32& currentQuestionID, const FString& currentDescription, const FString& currentOption)
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
	OnReceiveQuestion(currentQuestionID, currentDescription, currentOptionLists);
}


void URoleSpaceContentInterface::CLIENT_ReceiveQuestionState_Implementation(const int32& questionID, const uint8& Result)
{

}

void URoleSpaceContentInterface::CLIENT_StartMagicMazeQuest_Implementation(const int32& LastTime, const int32& TotalAnswerCount)
{

}

void URoleSpaceContentInterface::playerAnswer(const int32& questionID, const FString& answer)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::playerAnswer : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(questionID);
	args.Add(answer);
	this->GetEntity()->CellCall(TEXT("playerAnswer"), args);
}

void URoleSpaceContentInterface::selectNextQuestion()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::selectNextQuestion : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("selectNextQuestion"), args);
}

void URoleSpaceContentInterface::OnEnterEquipBuild(const FString& ScriptID, const FString& ModelID, const float& ModelScale, const FString& ItemUID)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	if (IsValid(EquipBuildClientCharacter))
	{
		EquipBuildClientCharacter->Destroy();
	}
	FVector MousePos = UGolbalBPFunctionLibrary::GetMouseWorldPos();
	FVector Direction = FVector::ZeroVector;
	Direction.Z = PlayerController->GetControlRotation().Euler().Z;
	EquipBuildClientCharacter = UGolbalBPFunctionLibrary::SpawnActor<AEquipBuildClientCharacter>(AEquipBuildClientCharacter::StaticClass(), MousePos, FRotator::MakeFromEuler(Direction));
	if (IsValid(EquipBuildClientCharacter))
	{
		EquipBuildClientCharacter->GetAppearanceComponent()->CreateAppearance(ModelID);
		if (!FMath::IsNearlyEqual(ModelScale, 1.0f))
		{
			EquipBuildClientCharacter->SetActorScale3D(FVector(ModelScale, ModelScale, ModelScale));
		}
	}
	//切换操作模式
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return;
	}
	AtkStateMar->SwitchEquipBuildMode(true, ScriptID, ItemUID);
}

void URoleSpaceContentInterface::OnLeaveEquipBuild()
{
	if (IsValid(EquipBuildClientCharacter))
	{
		EquipBuildClientCharacter->Destroy();
	}
	EquipBuildClientCharacter = nullptr;
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return;
	}
	AtkStateMar->SwitchEquipBuildMode(false);
}

void URoleSpaceContentInterface::RequestCreateApparatus(const FString& ScriptID, const FString& ItemUID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RequestCreateApparatus : entity!"));
		return;
	}
	if (!IsValid(EquipBuildClientCharacter)) return;
	if (EquipBuildClientCharacter->CanBuild())
	{
		KBEngine::FVariantArray args;
		args.Add(ScriptID);
		args.Add(EquipBuildClientCharacter->GetActorLocation());
		args.Add(EquipBuildClientCharacter->GetActorRotation().Euler());
		args.Add(ItemUID);
		entity->CellCall(TEXT("createApparatus"), args);
		OnLeaveEquipBuild();
	}
	else
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5620);
		}
	}
}

void URoleSpaceContentInterface::NotifyClinetQTEResult(uint8 IsSucceed)
{
}

void URoleSpaceContentInterface::OtherShowQTE()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QTEManager))
	{
		UUECS3GameInstance::Instance->QTEManager->OtherShowQTE();
	}
}

void URoleSpaceContentInterface::CopyRemainTimeAndName_Implementation(int32 time, const FString& name)
{

}

void URoleSpaceContentInterface::EnterFishState_Implementation(int32 smllFishFood, int32 mediumFishFood, int32 bigFishFood)
{
	//获取玩家控制器
	ACS3PlayerController* PlayerCon = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerCon))
	{
		//开启钓鱼模式
		PlayerCon->GetAtkStateMar()->SwitchFishMode(true);
	}

	OnEnterFishState(smllFishFood, mediumFishFood, bigFishFood);
}

void URoleSpaceContentInterface::ShowFishScore_Implementation(int32 fishingScore)
{

}

void URoleSpaceContentInterface::OnAddShield_Implementation(const int32& shieldCurValue, const int32& shieldMaxValue)
{

}

void URoleSpaceContentInterface::OnRemoveShield_Implementation()
{

}

void URoleSpaceContentInterface::OnShieldChanged_Implementation(const int32& shieldCurValue, const int32& shieldMaxValue)
{

}

void URoleSpaceContentInterface::CLIENT_MagicMazeDestinyResult_Implementation(const int32& Result)
{

}

void URoleSpaceContentInterface::CLIENT_CreateDestinyZhuanPan_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_MagicMazeLuckResult_Implementation(const int32& Result)
{

}

void URoleSpaceContentInterface::CLIENT_CreateLuckZhuanPan_Implementation()
{

}

void URoleSpaceContentInterface::CreateExtraItemBar_Implementation(const int32& gridNum, const TArray<FString>& uidList)
{

}

void URoleSpaceContentInterface::RemoveExtralItemBar_Implementation()
{

}

void URoleSpaceContentInterface::UpdateEnergyBar_Implementation(const int32& curValue, const int32& maxValue, const uint8& canAddSpeed)
{

}

void URoleSpaceContentInterface::ShowEnergyMessage_Implementation(const uint8& result)
{

}

void URoleSpaceContentInterface::ShowFaBaoCollectSuccMsg_Implementation(const FString& scriptID)
{

}
void URoleSpaceContentInterface::OnOpenAddSpeedExpendEnergy_Implementation()
{

}
void URoleSpaceContentInterface::OnCloseAddSpeedExpendEnergy_Implementation()
{

}

void URoleSpaceContentInterface::ShowEnterFengQiMsg_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_notifyCameraMove_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_onStartTorureNotice_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_onContinueTorture_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_NotifyClientRecoveryStatus_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_NotifyClientTortureResult_Implementation()
{

}

void URoleSpaceContentInterface::OnAbsorbSoulLayerLevelChanged_Implementation(int32 type)
{

}

void URoleSpaceContentInterface::SpaceZSGGossipComplete_Implementation()
{

}

void URoleSpaceContentInterface::onLeaveWorld()
{
	YCJMDQuickBarItems.Empty();
	bIsEnterYCJMD = false;
	AttCityActivityData.Empty();
	AttCityRoleArmyData.Empty();
	AttCityTitleNameData.Empty();
	LBCActivityMap.Empty();
	OnLeaveEquipBuild();
	Supper::onLeaveWorld();
}
void URoleSpaceContentInterface::CLIENT_NotifyClientStopEffect_Implementation(const FString& effectID)
{
	UParticleManager* ParticleManager = UGolbalBPFunctionLibrary::ParticleManager();
	ParticleManager->StopEffectByID(effectID);
}

void URoleSpaceContentInterface::CLIENT_onProblemDescription_Implementation(const FString& voiceID, int32 count)
{
}

void URoleSpaceContentInterface::CLIENT_SetPausedSpaceVoice_Implementation(const TArray<FString>& CurPauseTypes, const TArray<FString>& CurHideTypes, bool bPause, bool bIsHideVoiceType)
{
	UGolbalBPFunctionLibrary::AudioManager()->SetPausedVoice(CurPauseTypes, CurHideTypes, bPause, bIsHideVoiceType);
}
void URoleSpaceContentInterface::CLIENT_RideCopyGlede_Implementation(const FString& _FlyRoute)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(GetActor());
	if (Player && Player->ActorIsPlayer())
	{
		this->FlyRoute = _FlyRoute;
		// 绑定模型事件创建完毕的回调
		FlyRouteHandle = Player->RideCarrierComponent->OnCreateRoleAppearance.AddUObject(this, &URoleSpaceContentInterface::OnRideCopyGledeBP);
		Player->RideCarrierComponent->RideOnCarrier(TEXT("10009"));
		if (IsValid(Player->SpringArmCompent))
		{
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(Player->SpringArmCompent, FVector(-300.f, 0.f, 350.f));
		}
	}
}
void URoleSpaceContentInterface::CLIENT_DismountCopyGlede_Implementation()
{

}

void URoleSpaceContentInterface::DisRideOnCarrier()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(GetActor());
	if (Player && Player->ActorIsPlayer())
	{
		// 移除回调
		Player->RideCarrierComponent->OnCreateRoleAppearance.Remove(FlyRouteHandle);

		if (IsValid(Player->SpringArmCompent))
		{
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(Player->SpringArmCompent, FVector(-300.f, 0.f, 0.f));
		}
	}
	Player->RideCarrierComponent->DisRideOnCarrier();
}

void URoleSpaceContentInterface::CLIENT_NotifyHealthDisplayScreen_Implementation()
{
}
void URoleSpaceContentInterface::ClIENT_DisplayLocationAndColor_Implementation(const FVector& dstPos, const int32& index)
{
	indexList.Add(index);
	desPosList.Add(dstPos);
}

void URoleSpaceContentInterface::ClIENT_ClearLocationAndColor_Implementation()
{
	indexList.Empty();
	desPosList.Empty();
}

void URoleSpaceContentInterface::CLIENT_OnEnterAimingThrowMode_Implementation(const int32& Type)
{

}

void URoleSpaceContentInterface::CLIENT_OnLeaveAimingThrowMode_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_MatrixMazeResult_Implementation(const TArray<int32>& hzmgIndexList, const TArray<int32>& hzmgResultList)
{
	correspondList = hzmgIndexList;
	resultList = hzmgResultList;
}

void URoleSpaceContentInterface::CLIENT_refreshSpiritCrystal_Implementation(const TArray<int32>& coordXList, const TArray<int32>& coordYList, const TArray<int32>& coordZList, const TArray<int32>& colorNumList)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyStartRebound_Implementation(const int32& colorNum)
{
}

void URoleSpaceContentInterface::CLIENT_dropSpiritCrystal_Implementation(const int32& tiggerID, const int32& num)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyAccordToCount_Implementation(const int32& count)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyMonsterToCount_Implementation(const int32& monsterID, const int32& count)
{
}

void URoleSpaceContentInterface::CLIENT_InitializeCrystalCount_Implementation(const int32& redCount, const int32& yellowCount, const int32& blueCount)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyPlayerAddCount_Implementation(const int32& colorNum, const int32& count, bool isAdd)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyMonsterAddCount_Implementation(const int32& colorNum, const int32& count, bool isAdd)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyPlayerPopCrystal_Implementation(const int32& colorNum)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyMonsterPopCrystal_Implementation(const int32& monsterID, const int32& colorNum, const float& angle, const float& distance)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyCrystalPlayLight_Implementation(const float& distance)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyCrystalStopPlayLight_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_NotifyStartCountdown_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_NotifyStopCountdown_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_OnRotationAngleRange_Implementation(const FVector& dstPos, const float& rotatSpeed)
{
}

void URoleSpaceContentInterface::CLIENT_ProgressDisplayInterface_Implementation()
{
	correspondList.Empty();
	resultList.Empty();
}

void URoleSpaceContentInterface::CLIENT_NotifyMirrorObject_Implementation(const int32& XTBLID, const TArray<int32>& reflectorList)
{
}

void URoleSpaceContentInterface::CLIENT_OnShowJZYTStageTips_Implementation(const int32& stageIndex)
{
}
void URoleSpaceContentInterface::CLIENT_ShowJinZhiYuTingMonster_Implementation()
{
}

void URoleSpaceContentInterface::StopShowJinZhiYuTingMonster_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_ShowBloodPercentBar_Implementation(const int32& percent)
{
}

void URoleSpaceContentInterface::CLIENT_ShowLuckExtraReward_Implementation(const int32& extraReward)
{
}

void URoleSpaceContentInterface::CLIENT_DisplayProblemDescription_Implementation(const FString& voiceID)
{
}
void URoleSpaceContentInterface::CloseProblemDescription_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_NotifyNextRiotTime_Implementation(const FString& nextRiotTime)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyNextExplosionTime_Implementation(const FString& nextExplosionTime)
{
}

void URoleSpaceContentInterface::CLIENT_NotifyStopNextExplosionTime_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_NotifyDisplayItemIcon_Implementation(const int32& key, const int32& value)
{
}

void URoleSpaceContentInterface::OnArrowCrossoverEffect_Implementation()
{
}

void URoleSpaceContentInterface::StopDisplayItemIcon_Implementation()
{
}

void URoleSpaceContentInterface::OnEnterAimingMode_Implementation()
{
}

void URoleSpaceContentInterface::InitRefreshCiku_Implementation(const TArray<int32>& cikuCoordXList, const TArray<int32>& cikuCoordYList, const TArray<int32>& cikuCoordZList)
{
}

void URoleSpaceContentInterface::InitRefreshNormalCiku_Implementation(const TArray<int32>& cikuCoordXList1, const TArray<int32>& cikuCoordYList1, const TArray<int32>& cikuCoordZList1)
{
}

void URoleSpaceContentInterface::StartSendOutGhostGas_Implementation(const int32& initialValue, const float& radius, const float& time, const int32& epsilon)
{
}

void URoleSpaceContentInterface::ShowLoopQuestSpaceFailure_Implementation(const FString& countDown)
{
}

void URoleSpaceContentInterface::OnStartReckonByTime_Implementation(const FString& time, const TArray<int32>& changeTime, const TArray<int32>& changeColor, const int32& type)
{
}

void URoleSpaceContentInterface::ShowLoopQuestResult_Implementation(const int32& result)
{
}

void URoleSpaceContentInterface::ModifySwitchHomingSpellAtt_Implementation()
{
	if (UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchHomingSpellAtt(false);
	}
	else
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchHomingSpellAtt(true);
	}
}

void URoleSpaceContentInterface::OnEnterRidingStoneMode_Implementation()
{
}

void URoleSpaceContentInterface::OnLeaveRidingStoneMode_Implementation()
{
}

void URoleSpaceContentInterface::UpdateOtherPlayer()
{
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp == nullptr || KbeApp->Entities() == nullptr)
	{
		return;
	}

	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity && !Entity->IsPlayer() && !Entity->ClassName().Compare(FString("Role")))
		{
			if (AActor* Actor = Entity->Actor())
			{
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor);
			}
		}
	}
}

void URoleSpaceContentInterface::NotifyLXQDisplayScreen_Implementation(const int32& time)
{
}

void URoleSpaceContentInterface::NotifyLXQCloseScreen_Implementation()
{
}

void URoleSpaceContentInterface::OnLXQEnterAimingMode_Implementation(const int32& skillID)
{
}

void URoleSpaceContentInterface::OnLXQLeaveAimingMode_Implementation()
{
}

void URoleSpaceContentInterface::InitBlueCB()
{
	ArrBlueFunc.Add("ZhenLongQiJu_OnBossStateChange");
	ArrBlueFunc.Add("ZhenLongQiJu_OnBossHPChange");
	ArrBlueFunc.Add("ZhenLongQiJu_StopBossStateChange");
	ArrBlueFunc.Add("ZhenLongQiju_ClearData");
	ArrBlueFunc.Add("OnMountHeHua");
	ArrBlueFunc.Add("MoveToTargetPosition");
	ArrBlueFunc.Add("DismountHeHua");
	ArrBlueFunc.Add("ShowCircleHPPercentBar");
	ArrBlueFunc.Add("CLIENT_MagicMazeAnswerQuestionEnd");
	ArrBlueFunc.Add("CLIENT_ReceiveQuestion");
	ArrBlueFunc.Add("CLIENT_ReceiveQuestionState");
	ArrBlueFunc.Add("CLIENT_StartMagicMazeQuest");
	ArrBlueFunc.Add("CLIENT_MagicMazeDestinyResult");
	ArrBlueFunc.Add("CLIENT_MagicMazeLuckResult");
	ArrBlueFunc.Add("CreateExtraItemBar");
	ArrBlueFunc.Add("RemoveExtralItemBar");
	ArrBlueFunc.Add("UpdateEnergyBar");
	ArrBlueFunc.Add("ShowEnergyMessage");
	ArrBlueFunc.Add("ShowFaBaoCollectSuccMsg");
	ArrBlueFunc.Add("ShowEnterFengQiMsg");
	ArrBlueFunc.Add("OnAddShield");
	ArrBlueFunc.Add("OnRemoveShield");
	ArrBlueFunc.Add("OnShieldChanged");
	ArrBlueFunc.Add("EnterFishState");
	ArrBlueFunc.Add("ShowFishScore");
	ArrBlueFunc.Add("OnOpenAddSpeedExpendEnergy");
	ArrBlueFunc.Add("OnCloseAddSpeedExpendEnergy");
	ArrBlueFunc.Add("CLIENT_CreateLuckZhuanPan");
	ArrBlueFunc.Add("CLIENT_CreateDestinyZhuanPan");
	ArrBlueFunc.Add("NotifyClinetQTEResult");
	ArrBlueFunc.Add("OtherShowQTE");
	ArrBlueFunc.Add("CreateFish");
	ArrBlueFunc.Add("CLIENT_notifyCameraMove");
	ArrBlueFunc.Add("OnAbsorbSoulLayerLevelChanged");
	ArrBlueFunc.Add("CLIENT_onStartTorureNotice");
	ArrBlueFunc.Add("CLIENT_onContinueTorture");
	ArrBlueFunc.Add("CLIENT_NotifyClientRecoveryStatus");
	ArrBlueFunc.Add("CLIENT_NotifyClientTortureResult");
	ArrBlueFunc.Add("ChangeTerrainByBOSS");
	ArrBlueFunc.Add("CLIENT_NotifyClientStopEffect");
	ArrBlueFunc.Add("BrokenFloor");
	ArrBlueFunc.Add("SpaceZSGGossipComplete");
	ArrBlueFunc.Add("CLIENT_OnPremierHPChanged");
	ArrBlueFunc.Add("CLIENT_onProblemDescription");
	ArrBlueFunc.Add("CLIENT_onCalculateResults");
	ArrBlueFunc.Add("CopyRemainTimeAndName");
	ArrBlueFunc.Add("CLIENT_SetPausedSpaceVoice");
	ArrBlueFunc.Add("CLIENT_RideCopyGlede");
	ArrBlueFunc.Add("CLIENT_DismountCopyGlede");
	ArrBlueFunc.Add("CLIENT_NotifyHealthDisplayScreen");
	ArrBlueFunc.Add("ClIENT_DisplayLocationAndColor");
	ArrBlueFunc.Add("ClIENT_ClearLocationAndColor");
	ArrBlueFunc.Add("CLIENT_OnEnterAimingThrowMode");
	ArrBlueFunc.Add("CLIENT_OnLeaveJSDFSpace");
	ArrBlueFunc.Add("CLIENT_MatrixMazeResult");
	ArrBlueFunc.Add("CLIENT_OnLeaveAimingThrowMode");
	ArrBlueFunc.Add("CLIENT_OpenMonsterMirror");
	ArrBlueFunc.Add("CLIENT_CloseMonsterMirror");
	ArrBlueFunc.Add("CLIENT_ShowLingEnergyBar");
	ArrBlueFunc.Add("CLIENT_UpdateLingEnergyBar");
	ArrBlueFunc.Add("CLIENT_HideLingEnergyBar");
	ArrBlueFunc.Add("CLIENT_refreshSpiritCrystal");
	ArrBlueFunc.Add("CLIENT_NotifyStartRebound");
	ArrBlueFunc.Add("CLIENT_dropSpiritCrystal");
	ArrBlueFunc.Add("CLIENT_NotifyAccordToCount");
	ArrBlueFunc.Add("CLIENT_NotifyMonsterToCount");
	ArrBlueFunc.Add("Client_RemoveFloor");
	ArrBlueFunc.Add("Client_AddFloor");
	ArrBlueFunc.Add("Client_CreateFloor");
	ArrBlueFunc.Add("Client_GetTheFloorUnderMouseCursur");
	ArrBlueFunc.Add("CLIENT_NotifyCrystalPlayLight");
	ArrBlueFunc.Add("CLIENT_InitializeCrystalCount");
	ArrBlueFunc.Add("CLIENT_NotifyPlayerAddCount");
	ArrBlueFunc.Add("CLIENT_NotifyMonsterAddCount");
	ArrBlueFunc.Add("CLIENT_NotifyMonsterPopCrystal");
	ArrBlueFunc.Add("CLIENT_NotifyPlayerPopCrystal");
	ArrBlueFunc.Add("CLIENT_NotifyCrystalStopPlayLight");
	ArrBlueFunc.Add("CLIENT_ShowFuDaiReward");
	ArrBlueFunc.Add("CLIENT_ShowJinZhiYuTingRandomEvent");
	ArrBlueFunc.Add("CLIENT_ShowJinZhiYuTingRewards");
	ArrBlueFunc.Add("CLIENT_NotifyStartCountdown");
	ArrBlueFunc.Add("CLIENT_NotifyStopCountdown");
	ArrBlueFunc.Add("CLIENT_OnRotationAngleRange");
	ArrBlueFunc.Add("CLIENT_ProgressDisplayInterface");
	ArrBlueFunc.Add("CLIENT_NotifyMirrorObject");
	ArrBlueFunc.Add("CLIENT_ShowStopDestroyFloorTime");
	ArrBlueFunc.Add("CLIENT_OnShowJZYTStageTips");
	ArrBlueFunc.Add("CLIENT_ShowJinZhiYuTingMonster");
	ArrBlueFunc.Add("CLIENT_ShowPLMJCarrierUI");
	ArrBlueFunc.Add("CLIENT_ActivePLMJCarrierUI");
	ArrBlueFunc.Add("CLIENT_HidePLMJCarrierUI");
	ArrBlueFunc.Add("CLIENT_ShowBloodPercentBar");
	ArrBlueFunc.Add("CLIENT_ShowLuckExtraReward");
	ArrBlueFunc.Add("CLIENT_DisplayProblemDescription");
	ArrBlueFunc.Add("CLIENT_NotifyNextRiotTime");
	ArrBlueFunc.Add("CLIENT_NotifyNextExplosionTime");
	ArrBlueFunc.Add("CLIENT_NotifyStopNextExplosionTime");
	ArrBlueFunc.Add("CLIENT_UpdateMYJXEnergyBar");
	ArrBlueFunc.Add("CLIENT_HideMYJXEnergyBar");
	ArrBlueFunc.Add("CLIENT_ShowMYJXJumpBtn");
	ArrBlueFunc.Add("CLIENT_HideMYJXJumpBtn");
	ArrBlueFunc.Add("CLIENT_JumpToDstPos");
	ArrBlueFunc.Add("CLIENT_ShowJSZZPlaneWall");
	ArrBlueFunc.Add("CLIENT_showJSZZFirstTaskData");
	ArrBlueFunc.Add("CLIENT_showJSZZSecondTaskData");
	ArrBlueFunc.Add("CLIENT_AddJSZZCircleArea");
	ArrBlueFunc.Add("CLIENT_ClearJSZZCircleArea");
	ArrBlueFunc.Add("CLIENT_NotifyClientSecondTaskCanSearch");
	ArrBlueFunc.Add("CLIENT_ShowJSZZAcceptWin");
	ArrBlueFunc.Add("CLIENT_ChangeJSZZSearchBtn");
	ArrBlueFunc.Add("CLIENT_ShowJSZZCurStageRemainTime");
	ArrBlueFunc.Add("CLIENT_ShowNextRefreshMonsterTime");
	ArrBlueFunc.Add("CLIENT_showJSZZQuestTime");
	ArrBlueFunc.Add("ShowJSZZGrowthDegree");
	ArrBlueFunc.Add("ShowJSZZSettlement");
	ArrBlueFunc.Add("ShowJSZZPlantWin");
	ArrBlueFunc.Add("ShowJSZZProtectWin");
	ArrBlueFunc.Add("ShowMonsterCircleHPPercentBar");
	ArrBlueFunc.Add("CLIENT_OnMatchMXSJResult");
	ArrBlueFunc.Add("CLIENT_NotifyDisplayItemIcon");
	ArrBlueFunc.Add("OnArrowCrossoverEffect");
	ArrBlueFunc.Add("StopShowJinZhiYuTingMonster");
	ArrBlueFunc.Add("CLIENT_ShowJSCSCountDownUI");
	ArrBlueFunc.Add("CLIENT_ShowJSCSTipsUI");
	ArrBlueFunc.Add("StopDisplayItemIcon");
	ArrBlueFunc.Add("OnEnterAimingMode");
	ArrBlueFunc.Add("OnLeaveAimingMode");
	ArrBlueFunc.Add("InitRefreshCiku");
	ArrBlueFunc.Add("StartSendOutGhostGas");
	ArrBlueFunc.Add("InitRefreshNormalCiku");
	ArrBlueFunc.Add("ShowLoopQuestSpaceFailure");
	ArrBlueFunc.Add("OnStartReckonByTime");
	ArrBlueFunc.Add("ShowLoopQuestResult");
	ArrBlueFunc.Add("CLIENT_beginLLBZ");
	ArrBlueFunc.Add("CLIENT_startLingQiLock");
	ArrBlueFunc.Add("CLIENT_startLingHuanJue");
	ArrBlueFunc.Add("CLIENT_ShowLLBZRewards");
	ArrBlueFunc.Add("CLIENT_LLBZShowAllDiffcult");
	ArrBlueFunc.Add("CLIENT_ShowSpaceCopyFailedUI");
	ArrBlueFunc.Add("ModifySwitchHomingSpellAtt");
	ArrBlueFunc.Add("OnEnterRidingStoneMode");
	ArrBlueFunc.Add("OnLeaveRidingStoneMode");
	ArrBlueFunc.Add("AddYCJMDSkillBars");
	ArrBlueFunc.Add("RemoveYCJMDSkillBars");
	ArrBlueFunc.Add("OnEnterYCJMDShowSkillBar");
	ArrBlueFunc.Add("OnLeaveYCJMDHideSkillBar");
	ArrBlueFunc.Add("ShowFHJNSpecialWidget");
	ArrBlueFunc.Add("HideFHJNSpecialWidget");
	ArrBlueFunc.Add("UpdateFHJNSpecialWidget");
	ArrBlueFunc.Add("StartFallTZHJFabao");
	ArrBlueFunc.Add("StopFallTZHJFabao");
	ArrBlueFunc.Add("lXQIsHit");
	ArrBlueFunc.Add("LXQEnterAimingMode");
	ArrBlueFunc.Add("LXQLeaveAimingMode");
	ArrBlueFunc.Add("NotifyLXQDisplayScreen");
	ArrBlueFunc.Add("NotifyLXQCloseScreen");
	ArrBlueFunc.Add("NotifyLXQCloseScreen");
	ArrBlueFunc.Add("OnAddAttCityMember");
	ArrBlueFunc.Add("OnAssistsAttCity");
	ArrBlueFunc.Add("OnIntegralChangeAttCity");
	ArrBlueFunc.Add("ShowCampYCJMDPopulationUI");
	ArrBlueFunc.Add("showCampYCJMDPosition");
	ArrBlueFunc.Add("ShowSameCampYCJMDPos");
	ArrBlueFunc.Add("HideCampYCJMDPosition");
	ArrBlueFunc.Add("showCampYCJMDBoxPosition");
	ArrBlueFunc.Add("showCampYCJMDReikiCircle");
	ArrBlueFunc.Add("CLIENT_OnOpenBarracksArmyWin");
	ArrBlueFunc.Add("CloseProblemDescription");
	ArrBlueFunc.Add("OnShowCampYCJMDCountdown");
	ArrBlueFunc.Add("CleanCampYCJMDIcon");
	ArrBlueFunc.Add("CLIENT_UpdateGCZMemberDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ReceiveGCZOtherMemberData");
	ArrBlueFunc.Add("CLIENT_UpdateGCZKillEnemyDataToClient");
	ArrBlueFunc.Add("CLIENT_UpdateGCZKillSoldierDataToClient");
	ArrBlueFunc.Add("CLIENT_UpdateGCZDeadDataToClient");
	ArrBlueFunc.Add("CLIENT_UpdateGCZAssistsDataToClient");
	ArrBlueFunc.Add("CLIENT_UpdateGCZTotalExploitDataToClient");
	ArrBlueFunc.Add("CLIENT_UpdateGCZMemberDataToOtherClientOnLogin");
	ArrBlueFunc.Add("CLIENT_UpDateGCZMemberSoldierDeadNumToClient");
	ArrBlueFunc.Add("CLIENT_ShowBattleFlagProgressBar");
	ArrBlueFunc.Add("CLIENT_UpdateBattleFlagProgressBar");
	ArrBlueFunc.Add("CLIENT_OnOccupyBelongTypeChanged");
	ArrBlueFunc.Add("CLIENT_HideBattleFlagProgressBar");
	ArrBlueFunc.Add("CLIENT_ShowGCZSettlementWnd");
	ArrBlueFunc.Add("OnNotifyJZZYRuDaoBuff");
	ArrBlueFunc.Add("onNotifyJZZYBuffTime");
	ArrBlueFunc.Add("onExtinguishLight");
	ArrBlueFunc.Add("CLIENT_ChangeReadyToClimbLadder");
	ArrBlueFunc.Add("CLIENT_OnLeaveGCZ");
	ArrBlueFunc.Add("SetIsFirstEnterCopy");
	ArrBlueFunc.Add("OnPlayerLeaveYCJMD");
	ArrBlueFunc.Add("ShowShootYCJMDLNUI");
	ArrBlueFunc.Add("CLIENT_AddTrainingGroundMember");
	ArrBlueFunc.Add("CLIENT_updateLBCDeadData");
	ArrBlueFunc.Add("CLIENT_updateLBCKillData");
	ArrBlueFunc.Add("CLIENT_updateLBCKillMTData");
	ArrBlueFunc.Add("CLIENT_OnLBCSpaceResult");
	ArrBlueFunc.Add("CLIENT_notifyProbeTimes");
	ArrBlueFunc.Add("CLIENT_updateLBCLoseSDData");
	ArrBlueFunc.Add("CLIENT_OnJiYuanSpaceJieSuan");
	ArrBlueFunc.Add("CLIENT_NotifyXTBLStopShow");
	ArrBlueFunc.Add("CLIENT_WXHJChangeAttr");
	ArrBlueFunc.Add("CLIENT_ShowWXHJAttrUI");
	Supper::InitBlueCB();
}


void URoleSpaceContentInterface::OnLeaveScenes()
{
	AttCityActivityData.Empty();
	AttCityRoleArmyData.Empty();
	AttCityTitleNameData.Empty();
	OnLeaveScenes_BP();
	Supper::OnLeaveScenes();
}

void URoleSpaceContentInterface::RPC_onPlayerTouchCrystal(const int32& colorNum)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onPlayerTouchCrystal : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(colorNum);
	entity->CellCall(TEXT("CELL_onPlayerTouchCrystal"), args);
}

void URoleSpaceContentInterface::RPC_onMonsterTouchCrystal(const int32& colorNum)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMonsterTouchCrystal : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(colorNum);

	entity->CellCall(TEXT("CELL_onMonsterTouchCrystal"), args);
}

void URoleSpaceContentInterface::RPC_onSpiritCrystalPos(const FVector& Position_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onSpiritCrystalPos : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(Position_1);

	entity->CellCall(TEXT("CELL_onSpiritCrystalPos"), args);
}

void URoleSpaceContentInterface::RPC_onCrystalHitMonster()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onCrystalHitMonster : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onCrystalHitMonster"), args);
}

void URoleSpaceContentInterface::RPC_onRemoveSpiritCrystalPos(const FVector& Position_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onRemoveSpiritCrystalPos : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(Position_1);

	entity->CellCall(TEXT("CELL_onRemoveSpiritCrystalPos"), args);
}

void URoleSpaceContentInterface::RPC_onSpiritCrystalHitPlayer()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onSpiritCrystalHitPlayer : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onSpiritCrystalHitPlayer"), args);
}

void URoleSpaceContentInterface::RPC_onRemoveSpiritCrystalNum(const int32 & Index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onRemoveSpiritCrystalNum : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(Index);

	entity->CellCall(TEXT("CELL_onRemoveSpiritCrystalNum"), args);
}

void URoleSpaceContentInterface::RPC_onLocationBrushStrange(const int32& colorNum, const FVector& Position_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onSpiritCrystalPos : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(colorNum);
	args.Add(Position_1);

	entity->CellCall(TEXT("CELL_onLocationBrushStrange"), args);
}

void URoleSpaceContentInterface::CLIENT_CloseMonsterMirror_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_OpenMonsterMirror_Implementation(const float& high, const float& radius)
{

}

void URoleSpaceContentInterface::CLIENT_ShowLingEnergyBar_Implementation(const int32& maxLingEnergyValue, const int32& curLingEnergyValue)
{

}

void URoleSpaceContentInterface::CLIENT_UpdateLingEnergyBar_Implementation(const int32& maxLingEnergyValue, const int32& curLingEnergyValue, const int32& reduceLingEnergyValue)
{

}

void URoleSpaceContentInterface::CLIENT_HideLingEnergyBar_Implementation()
{

}

void URoleSpaceContentInterface::CELL_openMonsterMirror()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_openMonsterMirror : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_openMonsterMirror"), args);
}

void URoleSpaceContentInterface::CELL_closeMonsterMirror()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_closeMonsterMirror : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_closeMonsterMirror"), args);
}

void URoleSpaceContentInterface::CELL_MonsterListInMonsterMirror(const TArray<int32>& entityIDs)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_MonsterListInMonsterMirror : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(entityIDs));
	entity->CellCall(TEXT("CELL_MonsterListInMonsterMirror"), args);
}

void URoleSpaceContentInterface::CELL_MonsterOutMonsterMirror(const int32& monsterID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_MonsterOutMonsterMirror : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(monsterID);
	entity->CellCall(TEXT("CELL_MonsterOutMonsterMirror"), args);
}

void URoleSpaceContentInterface::RPC_FirstFloorPosition(const FVector& Position, const float& Length, const float& Width)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_FirstFloorPosition : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(Position);
	args.Add(Length);
	args.Add(Width);

	entity->CellCall(TEXT("FirstFloorPosition"), args);
}

void URoleSpaceContentInterface::RPC_FillFloor(const int32 & FloorID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_FillFloor : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(FloorID);

	entity->CellCall(TEXT("FillFloor"), args);
}

void URoleSpaceContentInterface::Client_RemoveFloor_Implementation(const int32 & FloorID)
{
}

void URoleSpaceContentInterface::Client_AddFloor_Implementation(const int32 & FloorID)
{
}

void URoleSpaceContentInterface::Client_CreateFloor_Implementation(const int32 & Row, const int32 & Col)
{
}

void URoleSpaceContentInterface::Client_GetTheFloorUnderMouseCursur_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_ShowCurrGotGoldAmount(const int32& amount)
{
  if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
  {
    UUECS3GameInstance::Instance->GEventManager->OnShowCurrGotGoldAmount.Broadcast(amount);
  }
}

void URoleSpaceContentInterface::CLIENT_ShowFuDaiReward_Implementation(const FString& itemID, const int32& amount)
{
}

void URoleSpaceContentInterface::CLIENT_ShowJinZhiYuTingRandomEvent_Implementation(const FString& key, const FString& endTime)
{

}

void URoleSpaceContentInterface::CLIENT_ShowJinZhiYuTingRewards_Implementation(const int32& fuDaiNum, const FString& itemIDs)
{

}

void URoleSpaceContentInterface::CELL_floorStartFalling()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_floorStartFalling : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_floorStartFalling"), args);
}

void URoleSpaceContentInterface::CLIENT_ShowStopDestroyFloorTime_Implementation(float stopTime)
{

}

void URoleSpaceContentInterface::CLIENT_ShowJSZZPlaneWall_Implementation(const FString& spaceScriptID, const TArray<FVector>& wallPosList)
{
	UMapManager* MapManager = UGolbalBPFunctionLibrary::MapManager();
	if (IsValid(MapManager))
	{
		MapManager->SetPlanePolygon(spaceScriptID, wallPosList);
	}
}

void URoleSpaceContentInterface::CLIENT_showJSZZFirstTaskData_Implementation(const FString& spaceScriptID, const FVector& pos, const float& radius)
{
	JSZZSpaceSctriptID = spaceScriptID;
}

void URoleSpaceContentInterface::CLIENT_showJSZZSecondTaskData_Implementation(const FVector& plantCenterPos, const float& plantRadius)
{
	JSZZPlantPosition = plantCenterPos;
}

void URoleSpaceContentInterface::CELL_ReplyAcceptJSZZQuest(const FString& itemUID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_ReplyAcceptJSZZQuest : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(itemUID);
	entity->CellCall(TEXT("CELL_ReplyAcceptJSZZQuest"), args);
}

void URoleSpaceContentInterface::CLIENT_AddJSZZCircleArea_Implementation(const FString& spaceScriptID, const FVector& plantCenterPos, const float& plantRadius)
{
	UMapManager* MapManager = UGolbalBPFunctionLibrary::MapManager();
	if (IsValid(MapManager))
	{
		MapManager->AddJSZZCircleArea(spaceScriptID, plantCenterPos, plantRadius);
	}
}

void URoleSpaceContentInterface::CLIENT_ClearJSZZCircleArea_Implementation()
{
	UMapManager* MapManager = UGolbalBPFunctionLibrary::MapManager();
	if (IsValid(MapManager))
	{
		MapManager->ClearJSZZCircleArea();
	}
}

void URoleSpaceContentInterface::CLIENT_NotifyClientSecondTaskCanSearch_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_ShowJSZZAcceptWin_Implementation(const TArray<int32>& itemIDs, const int32 & time, const FString & itemUID)
{
}

void URoleSpaceContentInterface::CELL_ClickJSZZSearch()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_ClickJSZZSearch : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_ClickJSZZSearch"), args);
}

void URoleSpaceContentInterface::CLIENT_ChangeJSZZSearchBtn_Implementation(const float & totalTime, const float & showTime)
{
}

void URoleSpaceContentInterface::CELL_ClickJSZZPlant()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_ClickJSZZPlant : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_ClickJSZZPlant"), args);
}

void URoleSpaceContentInterface::CLIENT_ShowJSZZCurStageRemainTime_Implementation(const int32& stage, const int32 & remainTime)
{
}

void URoleSpaceContentInterface::CLIENT_ShowNextRefreshMonsterTime_Implementation(const int32 & remainTime)
{
}

void URoleSpaceContentInterface::CLIENT_showJSZZQuestTime_Implementation(const FString& endTime)
{
}
void URoleSpaceContentInterface::ShowJSZZGrowthDegree_Implementation(const int32& value)
{
}
void URoleSpaceContentInterface::ShowJSZZSettlement_Implementation(const int32 & rewardMoney)
{
}
void URoleSpaceContentInterface::ShowJSZZPlantWin_Implementation(const FVector& plantPosition)
{
	JSZZPlantPosition = plantPosition;
}
void URoleSpaceContentInterface::ClickJSZZSearchBtn()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::ClickJSZZSearchBtn : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("clickJSZZSearchBtn"), args);
}
void URoleSpaceContentInterface::ClickJSZZPlantBtn()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::ClickJSZZPlantBtn : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("clickJSZZPlantBtn"), args);
}

void URoleSpaceContentInterface::ShowMonsterCircleHPPercentBar_Implementation(const int32 & isOpen, const int32 & percent, const FString & describe)
{
}

void URoleSpaceContentInterface::ShowJSZZProtectWin_Implementation(const TArray<int32>& itemIDs)
{

}


void URoleSpaceContentInterface::AddYCJMDSkillBars_Implementation(const int32& index, const int32& qbType, const int32& id)
{
	if (YCJMDQuickBarItems.Contains(index))
	{
		YCJMDQuickBarItems.Remove(index);
	}
	FQB_ITEM item;
	item.SlotIndex = index;
	item.QuickID = 0;
	item.QuickType = QUICK_SKILL_TYPE::QUICK_SKILL_TYPE_NORMAL;
	item.QbType = qbType;
	item.QbID = id;
	item.CurrQbID = id;
	item.BindType = 0;
	item.CurrStage = 0;
	item.RemainHoldTime = 0;
	item.TotalHoldTime = 0;
	YCJMDQuickBarItems.Add(index, item);
	UUECS3GameInstance::Instance->SkillManager->AddTotalSkillData(id);
}

void URoleSpaceContentInterface::RemoveYCJMDSkillBars_Implementation(const TArray<int32>& indexs)
{
	for (auto index : indexs)
	{
		if (YCJMDQuickBarItems.Contains(index))
		{
			YCJMDQuickBarItems.Remove(index);
		}
	}
}

void URoleSpaceContentInterface::OnEnterYCJMDShowSkillBar_Implementation()
{
	bIsEnterYCJMD = true;
}

void URoleSpaceContentInterface::OnLeaveYCJMDHideSkillBar_Implementation()
{
	bIsEnterYCJMD = false;

}

void URoleSpaceContentInterface::RPC_AddYCJMDSkillBarData(const int32 & index, const int32 & type, const int32 & id)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_AddYCJMDSkillBarData : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(index);
	args.Add(type);
	args.Add(id);
	entity->CellCall(TEXT("addYCJMDSkillBarData"), args);
}

void URoleSpaceContentInterface::RPC_RemoveYCJMDSkillBarData(const int32 & index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_RemoveYCJMDSkillBarData : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(index);
	entity->CellCall(TEXT("removeYCJMDSkillBarData"), args);
}

void URoleSpaceContentInterface::RPC_ExchangeYCJMDSkillBarData(const int32 & srcIndex, const int32 & dstIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_ExchangeYCJMDSkillBarData : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(srcIndex);
	args.Add(dstIndex);
	entity->CellCall(TEXT("exchangeYCJMDSkillBarData"), args);
}

int32 URoleSpaceContentInterface::GetSkillRequireItemID(const int32 & skillID)
{
	USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(skillID);
	if (!IsValid(SkillData))
	{
		return 0;
	}
	TArray<FSKILL_REQUIRE> requireList = SkillData->GetCasterRequireList();
	for (auto require : requireList)
	{
		if (require.Type == ENUM_SKILL_REQUIRE_TYPE::RequireCostItem)
		{
			return FSTRING_TO_INT(require.Param1);
		}
	}

	return 0;
}

TArray<FQB_ITEM> URoleSpaceContentInterface::GetYCJMDSkillBarDatas()
{
	TArray<FQB_ITEM> QuickBarItems;
	for (TPair<int32, FQB_ITEM>& Item : YCJMDQuickBarItems)
	{
		QuickBarItems.Add(Item.Value);
	}
	return QuickBarItems;
}

void URoleSpaceContentInterface::ShowFHJNSpecialWidget_Implementation(const int32& maxValue, const int32& curValue, const FString& describe)
{

}

void URoleSpaceContentInterface::HideFHJNSpecialWidget_Implementation()
{

}

void URoleSpaceContentInterface::UpdateFHJNSpecialWidget_Implementation(const int32& maxValue, const int32& curValue)
{

}

void URoleSpaceContentInterface::StartFallTZHJFabao_Implementation(const TArray<FString>& scriptIDList)
{

}
void URoleSpaceContentInterface::StopFallTZHJFabao_Implementation()
{

}

void URoleSpaceContentInterface::SetIsFirstEnterCopy_Implementation(bool IsFirst)
{
	bIsFirstEnterCopy = IsFirst;
}

void URoleSpaceContentInterface::CLIENT_OnEnterScout_Implementation()
{
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STALL,true);
}

void URoleSpaceContentInterface::CLIENT_OnEndScout_Implementation()
{
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STALL,false);
}

void URoleSpaceContentInterface::CLIENT_updateLBCLoseSDData(const int32& PlayerID, const int32& Num)
{
 	if (LBCActivityMap.Contains(PlayerID))
	{
		LBCActivityMap[PlayerID].OwnerSoldierDeadNum = Num;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateLBCLoseSDData.Broadcast(PlayerID, Num);
	}
}

void URoleSpaceContentInterface::CLIENT_OnEnterTrainSoldierGround(float ArmLength, FVector CameraRotation)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return;
	}
	AtkStateMar->SwitchTrainSoldierMode(true, ArmLength, CameraRotation);

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnEnterTrainSoldierGround.Broadcast();
	}
}

void URoleSpaceContentInterface::CLIENT_OnLeaveTrainSoldierGround()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return;
	}
	AtkStateMar->SwitchTrainSoldierMode(false);

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnLeaveTrainSoldierGround.Broadcast();
	}
}

void URoleSpaceContentInterface::ShowTongSpaceSettlementWin(const int32& countDownTime, const int32& useTime, const int32& rewardBarracksExp, const int32& rewardContribution, const int32& rewardTongMoney, const FString& buff, const FString& itemStr, const int32& score, const int32& level)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TongSpaceSettlement"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowTongSpaceSettlementUIEvent.Broadcast(countDownTime, useTime, rewardBarracksExp, rewardContribution, rewardTongMoney, buff, itemStr, score, level);
	}
}

void URoleSpaceContentInterface::RPC_StartHLDRound()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_StartHLDRound : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("StartHLDRound"), args);
}

void URoleSpaceContentInterface::RPC_throwFishRod(const int32& INT32_1, const int32& INT32_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_throwFishRod : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	args.Add(INT32_2);

	entity->CellCall(TEXT("throwFishRod"), args);
}

void URoleSpaceContentInterface::RPC_catchFishCheck(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_catchFishCheck : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->CellCall(TEXT("catchFishCheck"), args);
}

void URoleSpaceContentInterface::RPC_transformShield()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_transformShield : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("transformShield"), args);
}

void URoleSpaceContentInterface::RPC_dismountHeHua()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_dismountHeHua : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("dismountHeHua"), args);
}

void URoleSpaceContentInterface::RPC_move(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_move : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("move"), args);
}

void URoleSpaceContentInterface::RPC_onMagicMazeEndFly()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMagicMazeEndFly : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onMagicMazeEndFly"), args);
}

void URoleSpaceContentInterface::RPC_onMagicMazeNodeFly()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMagicMazeNodeFly : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onMagicMazeNodeFly"), args);
}

void URoleSpaceContentInterface::RPC_playerAnswer(const int32& INT32_1, const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_playerAnswer : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_playerAnswer"), args);
}

void URoleSpaceContentInterface::RPC_selectNextQuestion()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_selectNextQuestion : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_selectNextQuestion"), args);
}

void URoleSpaceContentInterface::RPC_openAddSpeedExpendEnergy()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_openAddSpeedExpendEnergy : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("openAddSpeedExpendEnergy"), args);
}

void URoleSpaceContentInterface::RPC_closeAddSpeedExpendEnergy()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_closeAddSpeedExpendEnergy : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("closeAddSpeedExpendEnergy"), args);
}

void URoleSpaceContentInterface::RPC_receiveFireDamage()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_receiveFireDamage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_receiveFireDamage"), args);
}

void URoleSpaceContentInterface::RPC_receiveFireDamageEnd()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_receiveFireDamageEnd : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_receiveFireDamageEnd"), args);
}

void URoleSpaceContentInterface::RPC_destroyLinkTrap(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_destroyLinkTrap : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_destroyLinkTrap"), args);
}

void URoleSpaceContentInterface::RPC_enterThunderArea()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_enterThunderArea : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_enterThunderArea"), args);
}

void URoleSpaceContentInterface::RPC_onMovingPlatformTriggerBegin(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMovingPlatformTriggerBegin : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("onMovingPlatformTriggerBegin"), args);
}

void URoleSpaceContentInterface::RPC_onMovingPlatformTriggerStart(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMovingPlatformTriggerStart : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_onMovingPlatformTriggerStart"), args);
}

void URoleSpaceContentInterface::RPC_randomMagicMazeZhuanPan()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_randomMagicMazeZhuanPan : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_randomMagicMazeZhuanPan"), args);
}

void URoleSpaceContentInterface::RPC_onPlayeTrampleLotus(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onPlayeTrampleLotus : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("onPlayeTrampleLotus"), args);
}

void URoleSpaceContentInterface::RPC_onFishHitPlayer()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onFishHitPlayer : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("onFishHitPlayer"), args);
}

void URoleSpaceContentInterface::RPC_onTortureNotice(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onTortureNotice : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_onTortureNotice"), args);
}

void URoleSpaceContentInterface::RPC_onEncounteredInDead()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onEncounteredInDead : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onEncounteredInDead"), args);
}

void URoleSpaceContentInterface::RPC_onCameraEndMove()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onCameraEndMove : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onCameraEndMove"), args);
}

void URoleSpaceContentInterface::RPC_onMoveStartTorureNotice()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMoveStartTorureNotice : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onMoveStartTorureNotice"), args);
}

void URoleSpaceContentInterface::RPC_onMoveEndTorureNotice()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onMoveEndTorureNotice : entity!"));
		return;
	} 

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onMoveEndTorureNotice"), args);
}

void URoleSpaceContentInterface::RPC_onPlayerTouchLaser()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onPlayerTouchLaser : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("onPlayerTouchLaser"), args);
}

void URoleSpaceContentInterface::RPC_onPlayerBeHammer()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onPlayerBeHammer : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("onPlayerBeHammer"), args);
}

void URoleSpaceContentInterface::RPC_onPlayerMetSandman()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onPlayerMetSandman : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onPlayerMetSandman"), args);
}
void URoleSpaceContentInterface::RPC_FireWallCallBack()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_FireWallCallBack : entity!"));
		return;
	}
	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_FireWallCallBack"), args);
}


void URoleSpaceContentInterface::RPC_onArmorLockBroke(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onArmorLockBroke : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("onArmorLockBroke"), args);
}

void URoleSpaceContentInterface::RPC_CELL_onPlayerBeHammer(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_CELL_onPlayerBeHammer no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("onPlayerBeHammer"), args);
}

void URoleSpaceContentInterface::RPC_CELL_onRoleDismountCopyGlede(const int32& isThrow)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_CELL_onRoleDismountCopyGlede no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT_TO_FSTRING(isThrow));

	entity->CellCall(TEXT("CELL_onRoleDismountCopyGlede"), args);
}

void URoleSpaceContentInterface::RPC_CELL_OnPlaySpaceIntroduceVoice()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_CELL_OnPlaySpaceIntroduceVoice no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_OnPlaySpaceIntroduceVoice"), args);
}

void URoleSpaceContentInterface::RPC_onStoneInSunShone(const int32& monsterID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onStoneInSunShone : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(monsterID);
	entity->CellCall(TEXT("CELL_onStoneInSunShone"), args);
}

void URoleSpaceContentInterface::RPC_onStoneOutSunShone(const int32& monsterID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onStoneInSunShone : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(monsterID);
	entity->CellCall(TEXT("CELL_onStoneOutSunShone"), args);
}

void URoleSpaceContentInterface::CLIENT_NotifyXTBLStopShow_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_ShowPLMJCarrierUI_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_ActivePLMJCarrierUI_Implementation()
{
}

void URoleSpaceContentInterface::CLIENT_HidePLMJCarrierUI_Implementation()
{
}
void URoleSpaceContentInterface::CELL_roleMountCarrier(const int32 & isMount)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_roleMountCarrier : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(isMount);
	entity->CellCall(TEXT("CELL_roleMountCarrier"), args);
}
void URoleSpaceContentInterface::RPC_inPosRefreshFabao(const FString& scriptID, const FVector& Position_1, const int32& parentID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_roleMountCarrier : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(scriptID);
	args.Add(Position_1);
	args.Add(parentID);
	entity->CellCall(TEXT("inPosRefreshFabao"), args);
}

void URoleSpaceContentInterface::CLIENT_UpdateMYJXEnergyBar_Implementation(const int32& curEnergy, const int32& maxEnergy)
{
}

void URoleSpaceContentInterface::CLIENT_HideMYJXEnergyBar_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_ShowMYJXJumpBtn_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_HideMYJXJumpBtn_Implementation()
{

}

void URoleSpaceContentInterface::CELL_MYJXPressJumBtn()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_MYJXPressJumBtn : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_MYJXPressJumBtn"), args);
}

void URoleSpaceContentInterface::CLIENT_JumpToDstPos_Implementation(const FVector& dstPos,
	float RisingDistance)
{
	//获取玩家
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(
		UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	float MoveSpeed = PlayerCharacter->GetCharacterMovement()->MaxWalkSpeed;
	FVector StartPosition = PlayerCharacter->GetActorLocation();
	FVector EndPosition = PlayerCharacter->FloorTrace(dstPos, true); ;
	RisingPercent = 0.0f;

	FVector Direction = EndPosition - StartPosition;
	FVector UpVector = FRotationMatrix::MakeFromX(Direction).Rotator().Quaternion().GetAxisZ();
	FRotator LookRotation = FRotationMatrix::MakeFromX(Direction).Rotator();
	PlayerCharacter->SetActorRotation(FRotator(PlayerCharacter->GetActorRotation().Pitch, LookRotation.Yaw,
		PlayerCharacter->GetActorRotation().Roll));
	PlayerCharacter->PlayAction(TEXT("JumpStart_Stand"));
	PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Flying);

	TWeakObjectPtr<URoleSpaceContentInterface> ThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, JumpToDsPosHandle,
		FTimerDelegate::CreateLambda([ThisPtr, Direction, UpVector, MoveSpeed, RisingDistance,
			StartPosition, EndPosition, PlayerCharacter]()
	{
		URoleSpaceContentInterface* RoleSpaceContentInterface = ThisPtr.Get();
		if (!RoleSpaceContentInterface)
		{
			return;
		}

		if (IsValid(PlayerCharacter))
		{
			RoleSpaceContentInterface->RisingPercent +=
				PlayerCharacter->GetWorld()->GetDeltaSeconds() * MoveSpeed / Direction.Size();
			// 大于1的时候清空
			if (RoleSpaceContentInterface->RisingPercent > 1.0f)
			{
				PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
				PlayerCharacter->SetActorLocation(EndPosition);
				PlayerCharacter->PlayAction(TEXT("JumpEnd_Stand"));
				UUECS3GameInstance::Instance->GetWorld()->GetTimerManager().ClearTimer(
					RoleSpaceContentInterface->JumpToDsPosHandle);
			}
			else
			{
				// 计算当前位置
				FVector Offset = FMath::Sin(RoleSpaceContentInterface->RisingPercent * PI) * RisingDistance * UpVector;
				Offset += (StartPosition + Direction.Size() * RoleSpaceContentInterface->RisingPercent * Direction.GetSafeNormal());
				PlayerCharacter->SetActorLocation(Offset);
			}
		}
	}), UUECS3GameInstance::Instance->GetWorld()->GetDeltaSeconds(), true);
}

void URoleSpaceContentInterface::RPC_NotifyDropDownCiku()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_NotifyDropDownCiku : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_NotifyDropDownCiku"), args);
}

void URoleSpaceContentInterface::RPC_HitRightCiku(const FVector& ciKuPos)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_HitRightCiku : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(ciKuPos);
	entity->CellCall(TEXT("CELL_HitRightCiku"), args);
}

void URoleSpaceContentInterface::RPC_HitErrorCiku(const FVector& ciKuPos)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_HitErrorCiku : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(ciKuPos);
	entity->CellCall(TEXT("CELL_HitErrorCiku"), args);
}

void URoleSpaceContentInterface::RPC_onCompleteQTENotyfy(const int32& isSucceed)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onCompleteQTENotyfy : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(isSucceed);
	entity->CellCall(TEXT("onCompleteQTENotyfy"), args);
}

void URoleSpaceContentInterface::RPC_onNotyfyCloseSpace(const int32& Result)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onNotyfyCloseSpace : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Result);
	entity->CellCall(TEXT("onNotyfyCloseSpace"), args);
}

void URoleSpaceContentInterface::RPC_onClickSignOutSpace()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_onClickSignOutSpace : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onClickSignOutSpace"), args);
}

void URoleSpaceContentInterface::CLIENT_LLBZShowAllDiffcult_Implementation(const FString& DiffcultStr)
{

}

void URoleSpaceContentInterface::CLIENT_beginLLBZ_Implementation(const FString& RewardList, const FString& uid, const FString& SpaceStr)
{
}

void URoleSpaceContentInterface::CLIENT_startLingQiLock_Implementation(const FString& ScriptID, const int32& Diffculty, const int32& Amount, const int32& Speed)
{

}

void URoleSpaceContentInterface::CLIENT_startLingHuanJue_Implementation(const FString& ScriptID, const int32& Diffculty, const int32& Amount)
{

}

void URoleSpaceContentInterface::CLIENT_ShowLLBZRewards_Implementation(const FString& rewardStr, const int32& HPRate)
{

}

void URoleSpaceContentInterface::CLIENT_ShowSpaceCopyFailedUI_Implementation()
{

}

void URoleSpaceContentInterface::RPC_OnUseLLBZ(const FString& uid, const FString& SpaceStr)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_OnUseLLBZ no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(uid);
	args.Add(SpaceStr);

	entity->CellCall(TEXT("CELL_onUseItemLLBZ"), args);
}

void URoleSpaceContentInterface::RPC_OnLingQiLock(const FString& ScriptID, const int32& Diffculty, const int32& Time)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_OnLingQiLock no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(ScriptID);
	args.Add(Diffculty);
	args.Add(Time);

	entity->CellCall(TEXT("CELL_onLingQiLock"), args);
}

void URoleSpaceContentInterface::RPC_OnLingHuanJue(const FString& ScriptID, const int32& Diffculty, const int32& Time)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_OnLingHuanJue no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(ScriptID);
	args.Add(Diffculty);
	args.Add(Time);

	entity->CellCall(TEXT("CELL_onLingHuanJue"), args);
}

void URoleSpaceContentInterface::RPC_OnLLBZGameComplete()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_OnLLBZGameComplete no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_onLLBZGameComplete"), args);
}

void URoleSpaceContentInterface::RPC_lXQIsHit(const int32& isHit)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_lXQIsHit no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(isHit);
	entity->CellCall(TEXT("lXQIsHit"), args);
}

void URoleSpaceContentInterface::RPC_LXQEnterAimingMode()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_LXQEnterAimingMode no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("LXQEnterAimingMode"), args);
}

void URoleSpaceContentInterface::RPC_LXQLeaveAimingMode()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_LXQLeaveAimingMode no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("LXQLeaveAimingMode"), args);
}

void URoleSpaceContentInterface::CLIENT_OnOpenBarracksArmyWin(const FVariant& Var, int32 defaultArmyIndex)
{
	AttCityRoleArmyData.Empty();
	KBEngine::FVariantArray ArmyDatas = Var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : ArmyDatas)
	{
		FARMYDATA ArmyData = FARMYDATA(data);
		FROLEARMYDATA TempRoleArmyData;
		TempRoleArmyData.Id = ArmyData.id;
		TempRoleArmyData.FirstGuardScriptID = ArmyData.firstGuardScriptID;
		TempRoleArmyData.SecondGuardScriptID = ArmyData.secondGuardScriptID;
		TempRoleArmyData.SoldierScriptID = ArmyData.soldierScriptID;
		TempRoleArmyData.SoldierIDs = ArmyData.soldierIDs;
		AttCityRoleArmyData.Add(TempRoleArmyData);
	}
	OnOpenBarracksArmyWin(defaultArmyIndex);
}


bool URoleSpaceContentInterface::GetAttCityRoleArmyDataByID(int32 ID, FROLEARMYDATA& RoleArmyData)
{
	for (auto data : AttCityRoleArmyData)
	{
		if (data.Id == ID)
		{
			RoleArmyData = data;
			return true;
		}
	}
	return false;
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZMemberDataToOtherClient_Implementation(const int32& id, const FString& name, const int32& belongSide, const int32& killEnemy, const int32& dead, const int32& assists, const int32& killSoldier, const int32& totalExploit, const FString& teamName, const int32& ownerSoldierDeadNum, const FString& enemyTeamName)
{
	if (teamName != "" && !AttCityTitleNameData.Contains(belongSide))
	{
		AttCityTitleNameData.Add(belongSide, teamName);
		int32 enemySide = 1 - belongSide;//因为攻守方belongSide为0和1，而这个参数又不提供敌方所属belongSide，只好用1-己方belongSide，得出敌方belongSide
		AttCityTitleNameData.Add(enemySide, enemyTeamName);
	}
	AddGCZMemberData(id, name, belongSide, killEnemy, dead, assists, killSoldier, totalExploit, ownerSoldierDeadNum);
}

void URoleSpaceContentInterface::CLIENT_ReceiveGCZOtherMemberData_Implementation(const int32& id, const FString& name, const int32& belongSide, const int32& killEnemy, const int32& dead, const int32& assists, const int32& killSoldier, const int32& totalExploit, const FString& teamName, const int32& ownerSoldierDeadNum, const FString& enemyTeamName)
{
	if (teamName != "" && !AttCityTitleNameData.Contains(belongSide))
	{
		AttCityTitleNameData.Add(belongSide, teamName);
		int32 enemySide = 1 - belongSide;//因为攻守方belongSide为0和1，而这个参数又不提供敌方所属belongSide，只好用1-己方belongSide，得出敌方belongSide
		AttCityTitleNameData.Add(enemySide, enemyTeamName);
	}
	AddGCZMemberData(id, name, belongSide, killEnemy, dead, assists, killSoldier, totalExploit, ownerSoldierDeadNum);
}

void URoleSpaceContentInterface::AddGCZMemberData(const int32& id, const FString& name, const int32& belongSide, const int32& killEnemy, const int32& dead, const int32& assists, const int32& killSoldier, const int32& totalExploit, const int32& ownerSoldierDeadNum)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].Name = name;
		AttCityActivityData[id].BelongSide = BELONG_SIDE(belongSide);
		AttCityActivityData[id].KillEnemy = killEnemy;
		AttCityActivityData[id].Dead = dead;
		AttCityActivityData[id].Assists = assists;
		AttCityActivityData[id].KillSoldier = killSoldier;
		AttCityActivityData[id].TotalExploit = totalExploit;
		AttCityActivityData[id].OwnerSoldierDeadNum = ownerSoldierDeadNum;
	}
	else
	{
		FAttCityMemberData tempMemberData;
		tempMemberData.Name = name;
		tempMemberData.BelongSide = BELONG_SIDE(belongSide);
		tempMemberData.KillEnemy = killEnemy;
		tempMemberData.Dead = dead;
		tempMemberData.Assists = assists;
		tempMemberData.KillSoldier = killSoldier;
		tempMemberData.TotalExploit = totalExploit;
		tempMemberData.OwnerSoldierDeadNum = ownerSoldierDeadNum;
		AttCityActivityData.Add(id, tempMemberData);
	}
}

void URoleSpaceContentInterface::CLIENT_UpDateGCZMemberSoldierDeadNumToClient(int32 id, int32 ownerSoldierDeadNum)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].OwnerSoldierDeadNum = ownerSoldierDeadNum;
		BP_UpDateGCZMemberSoldierDeadNumToClient(id, ownerSoldierDeadNum);
	}
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZKillEnemyDataToClient_Implementation(const int32& id, const int32& killEnemy)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].KillEnemy = killEnemy;
	}
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZKillSoldierDataToClient_Implementation(const int32& id, const int32& killSoldier)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].KillSoldier = killSoldier;
	}
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZDeadDataToClient_Implementation(const int32& id, const int32& dead)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].Dead = dead;
	}
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZAssistsDataToClient_Implementation(const int32& id, const int32& assists)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].Assists = assists;
	}
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZTotalExploitDataToClient_Implementation(const int32& id, const int32& totalExploit)
{
	if (AttCityActivityData.Contains(id))
	{
		AttCityActivityData[id].TotalExploit = totalExploit;
	}
}

void URoleSpaceContentInterface::CallArmyToWar(const int32& id)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::CallArmyToWar no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(id);
	entity->CellCall(TEXT("callArmyToWar"), args);
}

void URoleSpaceContentInterface::CLIENT_UpdateGCZMemberDataToOtherClientOnLogin_Implementation(const int32& srcMemberID, const int32& dstMemberID)
{
	if (AttCityActivityData.Contains(srcMemberID))
	{
		FAttCityMemberData tempMemberData = AttCityActivityData[srcMemberID];
		AttCityActivityData.Remove(srcMemberID);
		AttCityActivityData.Add(dstMemberID, tempMemberData);
	}
}

void URoleSpaceContentInterface::CLIENT_ShowBattleFlagProgressBar_Implementation(const int32& battleEntityID, const int32& belongType, const int32& occurProgress, const int32& maxProgress)
{

}

void URoleSpaceContentInterface::CLIENT_UpdateBattleFlagProgressBar_Implementation(const int32& occurProgress, const int32& maxProgress)
{

}

void URoleSpaceContentInterface::CLIENT_OnOccupyBelongTypeChanged_Implementation(const int32& belongType)
{

}

void URoleSpaceContentInterface::CLIENT_HideBattleFlagProgressBar_Implementation(const int32& battleEntityID)
{

}

void URoleSpaceContentInterface::CLIENT_ShowGCZSettlementWnd_Implementation(const int32& isWin, const int32& costTime, const int32& closeTime)
{

}

void URoleSpaceContentInterface::CLIENT_ChangeReadyToClimbLadder_Implementation(const int32& isClimbLadder)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID, isClimbLadder=%d]=======StartEnterLadderBottom"), isClimbLadder);

	IsReadyClimbLadder = isClimbLadder > 0 ? true : false;
	if (IsReadyClimbLadder)
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
		{
			CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d, isClimbLadder=%d]=======StartEnterLadderBottom"),
				UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity()->ID(), isClimbLadder);

			PlayerCharacter->LadderCustomMovmentCpt->StartEnterLadderBottom();
		}
	}
}

void URoleSpaceContentInterface::CLIENT_OnLeaveGCZ_Implementation()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->LadderCustomMovmentCpt->ClearLadderData();
	}
}

int32 URoleSpaceContentInterface::GetMemberSoldierDeadNumByBelongSide(BELONG_SIDE side)
{
	int32 totalSoldierDeadNum = 0;
	for (auto It = AttCityActivityData.CreateIterator();It;++It)
	{
		if (It.Value().BelongSide == side)
		{
			totalSoldierDeadNum += It.Value().OwnerSoldierDeadNum;
		}
	}
	return totalSoldierDeadNum;
}

void URoleSpaceContentInterface::OnShowTongPlunderSettlementWnd_Implementation(const int32& isWin, const int32& costTime, const int32& closeTime)
{

}

void URoleSpaceContentInterface::CLIENT_ShowTongPlunderSettlementWnd(const int32& isWin, const int32& costTime, const int32& closeTime, const FVariant& MemberInfos)
{
	TongPlunderTitleNameData.Empty();
	TongPlunderData.Empty();
	FATT_CITY_MEMBER_DATA Data = FATT_CITY_MEMBER_DATA(MemberInfos);

	TongPlunderTitleNameData.Add((int32)BELONG_SIDE::BELONG_SIDE_ATTACK, Data.AttackName);
	TongPlunderTitleNameData.Add((int32)BELONG_SIDE::BELONG_SIDE_PROTECT, Data.ProtectName);

	for (auto Member : Data.Members)
	{
		FAttCityMemberData TempData;
		TempData.Name = Member.Name;
		TempData.BelongSide = (BELONG_SIDE)Member.BelongSide;
		TempData.KillEnemy = Member.KillEnemy;
		TempData.Dead = Member.Dead;
		TempData.Assists = Member.Assists;
		TempData.KillSoldier = Member.KillSoldier;
		TempData.TotalExploit = Member.TotalExploit;
		TempData.OwnerSoldierDeadNum = Member.OwnerSoldierDeadNum;
		TongPlunderData.Add(INT64_TO_FSTRING(Member.ID), TempData);
	}

	OnShowTongPlunderSettlementWnd(isWin, costTime, closeTime);
}

void URoleSpaceContentInterface::OnTongPlunderSoldierDead_Implementation()
{

}

void URoleSpaceContentInterface::CLIENT_TongPlunderSoldierDead(const int32& SoldierType)
{
	if (SoldierType == 0)
	{
		TongPlunderEnemySoldierDeadNum += 1;
	}
	else if(SoldierType == 1)
	{
		TongPlunderOurSoldierDeadNum += 1;
	}

	OnTongPlunderSoldierDead();
}

void URoleSpaceContentInterface::RPC_JHBIsCatch(bool isCatch)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_JHBIsCatch no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("JHBIsCatch"), args);
}

void URoleSpaceContentInterface::OnStartYCJMDSkyFlyModel(const FString& FlyPathId)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->UpdateWeaponState();
		TWeakObjectPtr<URoleSpaceContentInterface> DelayThisPtr(this);
		PlayerCharacter->OnBroadCreateRidderModelOver.BindLambda([DelayThisPtr, FlyPathId]()
		{
			if (!DelayThisPtr.IsValid())return;
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(DelayThisPtr.Get()->GetActor());
			if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->FlyPatrolComponent))
			{
				PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Falling);
				PlayerCharacter->SetBaseGravityScale(0.0f);
				PlayerCharacter->FlyPatrolComponent->StartYCJMDSkyFly(FlyPathId);
				PlayerCharacter->OnBroadCreateModelOver.Unbind();
				DelayThisPtr.Get()->ChangeParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_CARRIER);
			}
		});
		PlayerCharacter->RideCarrierComponent->RideOnCarrier(Parachute_CarrierID);

		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::YcjmdSkyCarrier, CC_MODE_REASON::CCM_YJSC_CONTROLLER_MODE);

		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_YCJMD_SKY_CARRIER);
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnShowFlyPatrolLine.Broadcast(FlyPathId);
		}
	}
}


void URoleSpaceContentInterface::ChangeParachuteState(const PARACHUTE_STATE state)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleSpaceContentInterface::RPC_JHBIsCatch no this Entity!"));
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->SetParachuteState(state);
	}
	KBEngine::FVariantArray args;
	args.Add(uint8(state));
	entity->CellCall(TEXT("changeParachutingState"), args);
}

void URoleSpaceContentInterface::Set_ParachuteState(const uint8& newState, const uint8& oldState)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter))
	{
		PARACHUTE_STATE newParachute = PARACHUTE_STATE(newState);
		PlayerCharacter->SetParachuteState(newParachute);
		// 非本地玩家 的跳伞模拟
		if (!PlayerCharacter->ActorIsPlayer())			
		{
			if (newParachute == PARACHUTE_STATE::PARACHUTE_STATE_CARRIER)
			{
				//PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Falling);
				//PlayerCharacter->SetBaseGravityScale(0.0f);
				PlayerCharacter->RideCarrierComponent->RideOnCarrier(Parachute_CarrierID);
			}
			else if (newParachute == PARACHUTE_STATE::PARACHUTE_STATE_FALL)		// 自由下落
			{
				PlayerCharacter->RideCarrierComponent->DisRideOnCarrier();
				uint8 gender = (uint8)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("gender")).GetValue<int32>();
				if (Parachute_SexActionTable.Contains(gender))
				{
					PlayerCharacter->GetAppearanceComponent()->CreateAppearance(Parachute_SexActionTable[gender]);
				}
				PlayerCharacter->BindMesh(Parachute_BagID);//绑定降落伞背包
			}
			else if (newParachute == PARACHUTE_STATE::PARACHUTE_STATE_OPEN)		// 开伞
			{
				if (!PlayerCharacter->IsBindMeshState())			// 如果沒綁定東西，就默認 是刚创建的character
				{
					uint8 gender = (uint8)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("gender")).GetValue<int32>();
					if (Parachute_SexActionTable.Contains(gender))
					{
						PlayerCharacter->GetAppearanceComponent()->CreateAppearance(Parachute_SexActionTable[gender]);
					}
					PlayerCharacter->BindMesh(Parachute_BagID);//绑定降落伞背包
				}
				PlayerCharacter->FlyPatrolComponent->CreateParachuteInst();
			}
			// 落地
			if (newParachute == PARACHUTE_STATE::PARACHUTE_STATE_NORMAL && oldState == uint8(PARACHUTE_STATE::PARACHUTE_STATE_OPEN))
			{
				PlayerCharacter->FlyPatrolComponent->LandYCJMDParachute();
				PlayerCharacter->CreateAppearance();
				
			}
		}
	}
}

void URoleSpaceContentInterface::OnYCJMSkyFly()
{
	UBaseWindow* SKillBar = UUECS3GameInstance::Instance->GUIManager->GetWindow("SkillBar");
	if (IsValid(SKillBar))
	{
		SKillBar->Hide();
	}
	UBaseWindow* SpaceCopyBar = UUECS3GameInstance::Instance->GUIManager->GetWindow("SpaceCopyBag");
	if (IsValid(SpaceCopyBar))
	{
		SpaceCopyBar->Hide();
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("YCJMDJumpPlaneTips"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnYCJMSkyFly.Broadcast();
	}
}

void URoleSpaceContentInterface::OnOpenParachute()
{
	UBaseWindow* JumpPlaneTips = UUECS3GameInstance::Instance->GUIManager->GetWindow("YCJMDJumpPlaneTips");
	if (IsValid(JumpPlaneTips))
	{
		JumpPlaneTips->Destroy();
	}
}

void URoleSpaceContentInterface::OnShowYCJMDUI()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("ParachuteInfoWidget"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowYCJMDUI.Broadcast();
	}
}

void URoleSpaceContentInterface::OnHideYCJMDUI()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHideYCJMDUI.Broadcast();
	}

	UBaseWindow* SKillBar = UUECS3GameInstance::Instance->GUIManager->GetWindow("SkillBar");
	if (IsValid(SKillBar))
	{
		SKillBar->Show();
		if(IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
		UUECS3GameInstance::Instance->GEventManager->OnSetQuickBarEnabled.Broadcast(bIsEnableQuickBar);
		}
	}
	UBaseWindow* SpaceCopyBar = UUECS3GameInstance::Instance->GUIManager->GetWindow("SpaceCopyBag");
	if (IsValid(SpaceCopyBar))
	{
		SpaceCopyBar->Show();
	}
}

void URoleSpaceContentInterface::ShowCampYCJMDPopulationUI_Implementation(const int32 & xAmount, const int32 & mAmount)
{
}

void URoleSpaceContentInterface::showCampYCJMDPosition_Implementation(const int32 & ID, const FVector & Position)
{
}

void URoleSpaceContentInterface::ShowSameCampYCJMDPos_Implementation(const int32 & ID, const FVector & Position)
{
}

void URoleSpaceContentInterface::HideCampYCJMDPosition_Implementation()
{
}

void URoleSpaceContentInterface::showCampYCJMDBoxPosition_Implementation(const FVector & Position)
{
}

void URoleSpaceContentInterface::showCampYCJMDReikiCircle_Implementation(const FVector & Position, const int32 & Radius)
{

}

void URoleSpaceContentInterface::OnShowCampYCJMDCountdown_Implementation(const FString& EndTimeStr)
{

}

void URoleSpaceContentInterface::CleanCampYCJMDIcon_Implementation(const FString& ScriptID)
{

}

void URoleSpaceContentInterface::OnPlayerLeaveYCJMD_Implementation(const int32 & ID)
{
}

void URoleSpaceContentInterface::OnNotifyJZZYRuDaoBuff_Implementation(bool isAdd)
{
	bIsHasRuDaoBuffFlag = isAdd;
}

void URoleSpaceContentInterface::onNotifyJZZYBuffTime_Implementation(const int32& t)
{

}

void URoleSpaceContentInterface::onExtinguishLight_Implementation(int32 amount)
{
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	int32 effectLen = FirePointRecord.Num();
	for (int i = effectLen-1; i > 0; i--)
	{
		FString left, right;
		FirePointRecord[i].Split("_", &left, &right);
		AActor* ect = ParticleManager->FindEmitterByUID(FSTRING_TO_INT(right));
		if (!IsValid(ect))return;

		AServerCharacter* monster = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(FSTRING_TO_INT(left)));
		UMonsterExtJZZYXYInterface* Monsterinterface = Cast<UMonsterExtJZZYXYInterface>(monster->GetEntityInterface_Cache().GameObjectInterface);
		if (IsValid(Monsterinterface))
		{
			int32 index = Monsterinterface->EffectUIDs.Find(FSTRING_TO_INT(right));
			//CST-13794
			if (index != -1 && Monsterinterface->SaveSocketNmaes.Num() != 0)
			{
				Monsterinterface->SocketNames.Add(Monsterinterface->SaveSocketNmaes[index]);
				Monsterinterface->SaveSocketNmaes.RemoveAt(index);
				Monsterinterface->EffectUIDs.RemoveAt(index);
			}

		}
		ParticleManager->Stop(Cast<AEffectEmitter>(ect));
		FirePointRecord.RemoveAt(i);

	}
}

void URoleSpaceContentInterface::ShowShootYCJMDLNUI_Implementation(bool isshow)
{
	OnShowShootYCJMDLNUI(isshow);
}


void URoleSpaceContentInterface::CLIENT_AddTrainingGroundMember_Implementation(const int32 & PlayerID, const FString & PlayerName, const int32 & BelongSide)
{
	FAttCityMemberData tempMemberData;
	tempMemberData.Name = PlayerName;
	tempMemberData.BelongSide = BELONG_SIDE(BelongSide);
	tempMemberData.KillEnemy = 0;
	tempMemberData.Dead = 0;
	tempMemberData.Assists = 0;
	tempMemberData.KillSoldier = 0;
	tempMemberData.TotalExploit = 0;
	LBCActivityMap.Add(PlayerID, tempMemberData);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAddTrainingGroundMember.Broadcast(PlayerID, PlayerName, BelongSide);
	}
}

void URoleSpaceContentInterface::CLIENT_updateLBCDeadData_Implementation(const int32 & PlayerID, const int32 & Num)
{
	if (LBCActivityMap.Contains(PlayerID))
	{
		LBCActivityMap[PlayerID].Dead = Num;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateLBCDeadData.Broadcast(PlayerID, Num);
	}
}

void URoleSpaceContentInterface::CLIENT_updateLBCKillData_Implementation(const int32 & PlayerID, const int32 & Num)
{
	if (LBCActivityMap.Contains(PlayerID))
	{
		LBCActivityMap[PlayerID].KillEnemy = Num;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateLBCKillData.Broadcast(PlayerID, Num);
	}
}

void URoleSpaceContentInterface::CLIENT_updateLBCKillMTData_Implementation(const int32 & PlayerID, const int32 & Num)
{
	if (LBCActivityMap.Contains(PlayerID))
	{
		LBCActivityMap[PlayerID].KillSoldier = Num;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateLBCKillMTData.Broadcast(PlayerID, Num);
	}
}

void URoleSpaceContentInterface::CLIENT_OnLBCSpaceResult_Implementation(const int32 & Exploit, const int32 & IsWin, const int32& LiftTime)
{
	int32 PlayerID = UGolbalBPFunctionLibrary::GetPlayerID();
	if (LBCActivityMap.Contains(PlayerID))
	{
		LBCActivityMap[PlayerID].TotalExploit = Exploit;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("BarracksResult"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnLBCSpaceResult.Broadcast(Exploit, IsWin, LiftTime);
	}

}

void URoleSpaceContentInterface::CLIENT_notifyProbeTimes_Implementation(const int32& times)
{
	probeTimes = times;
}

void URoleSpaceContentInterface::ShowFireCowAngerUI(const int32& angerValue)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("FireCowAngerWindow"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowFireCowAngerUI.Broadcast(angerValue);
	}

}
void URoleSpaceContentInterface::CollectedXLC(const int32 & amount)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnNotifyCollectedXLCAmount.Broadcast(amount);
	}
}

void URoleSpaceContentInterface::CELL_mountVehicle(int32 vehicleID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_mountVehicle : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(vehicleID);
	this->GetEntity()->CellCall(TEXT("CELL_mountVehicle"), args);
}

void URoleSpaceContentInterface::CELL_dismountVehicle()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_dismountVehicle : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(this->VehicleID);
	this->GetEntity()->CellCall(TEXT("CELL_dismountVehicle"), args);
}

void URoleSpaceContentInterface::CELL_reqVehicleData(int32 targetPlayerID, int32 InVehicleID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_reqVehicleData : GetEntity()!"));
		return;
	}
	if (VehicleID == InVehicleID)
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetPlayerID);
	args.Add(InVehicleID);
	this->GetEntity()->CellCall(TEXT("CELL_reqVehicleData"), args);
}

void URoleSpaceContentInterface::CELL_InviteMountVehicle(int32 targetPlayerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_InviteMountVehicle : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetPlayerID);
	this->GetEntity()->CellCall(TEXT("CELL_inviteMountVehicle"), args);
}

void URoleSpaceContentInterface::CELL_ApplyMountVehicle(int32 targetPlayerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::CELL_InviteMountVehicle : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetPlayerID);
	this->GetEntity()->CellCall(TEXT("CELL_applyMountVehicle"), args);
}

bool URoleSpaceContentInterface::HasVehicle()
{
	return VehicleID != 0;
}

bool URoleSpaceContentInterface::IsVehicleDriver()
{
	return VehicleID != 0 && DriverID == EntityID;
}


void URoleSpaceContentInterface::SetIsEnabledQuickBar(const uint8& bEnable)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	PlayerController->SetIsEnabledQuickBar((bool)bEnable);
	bIsEnableQuickBar = bool(bEnable);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnSetQuickBarEnabled.Broadcast(bIsEnableQuickBar);
	}
	
}

void URoleSpaceContentInterface::CLIENT_ShowJSSLCJiYuanJieSuanWnd(const int32& CostTime, const int32& Level, const int32& RewardValue, const int32& DieNumber)
{
	OnShowJSSLCJiYuanJieSuanWnd(CostTime, Level, RewardValue, DieNumber);
}

void URoleSpaceContentInterface::OnShowJSSLCJiYuanJieSuanWnd_Implementation(const int32& CostTime, const int32& Level, const int32& RewardValue, const int32& DieNumber)
{

}

void URoleSpaceContentInterface::CLIENT_OnMountVehicle_Implementation(int32 InVehicleID, int32 InDriverID, const FString& SocketName, const FString& CarrierId, uint8 CanControlMove)
{
	VehicleID = InVehicleID;
	DriverID = InDriverID;
	if (!IsValid(GetActor())) return;
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());//上载具的玩家
	if (!IsValid(PlayerCharacter)) return;
	KBEngine::Entity* VehicleEntity = UGolbalBPFunctionLibrary::FindEntity(InVehicleID);
	if (VehicleEntity == nullptr) return;
	AActor* VehicleActor = VehicleEntity->Actor();
	if (!IsValid(VehicleActor)) return;
	AMovingPlatformVehicleCharacter* MovingPlatformVehicleCharacter = Cast<AMovingPlatformVehicleCharacter>(VehicleActor);
	if (!IsValid(MovingPlatformVehicleCharacter)) return;
	if (!CanControlMove)
	{
		PlayerCharacter->GetCharacterMovement()->SetActive(false);
		//创建载具外观
		int32 RoleProfession = (int32)GetEntity()->GetDefinedProperty(TEXT("profession"));
		int32 RoleGender = (int32)GetEntity()->GetDefinedProperty(TEXT("gender"));
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const FCARRIER_DATA *CarrierData = CfgManager->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CARRIER)->GetRow<FCARRIER_DATA>(FSTRING_TO_FNAME(CarrierId));
		if (CarrierData != nullptr)
		{
			//MovingPlatformVehicleCharacter->CreateVehicleAppearance(CarrierData->CarrierModelId);
			PlayerCharacter->EnterVehicleMode(CarrierData->RidePosture, RoleProfession, RoleGender);
		}
		
		//将玩家绑定到载具上
		USkeletalMeshComponent* MeshComp = MovingPlatformVehicleCharacter->GetMesh();
		if (IsValid(MeshComp))
		{
			if (MovingPlatformVehicleCharacter->bIsChangeAppearanceling || (!MovingPlatformVehicleCharacter->GetApperanceLoadingOver()) || !IsValid(MovingPlatformVehicleCharacter->GetMesh()->SkeletalMesh))
			{
				//外观还没创建完成
				TWeakObjectPtr<AServerCharacter> ActorPtr(MovingPlatformVehicleCharacter);
				TWeakObjectPtr<URoleSpaceContentInterface> ThisPtr(this);
				if (MountVehicleHandle.IsValid())
				{
					MovingPlatformVehicleCharacter->OnModelChangeAppearanceOverDelegate.Remove(MountVehicleHandle);
					MountVehicleHandle.Reset();
				}
				MountVehicleHandle = MovingPlatformVehicleCharacter->OnModelChangeAppearanceOverDelegate.AddLambda([
					ThisPtr, ActorPtr, SocketName]()
				{
					URoleSpaceContentInterface* ThisInterface = ThisPtr.Get();
					if (!IsValid(ThisInterface))return;
					AServerCharacter* ServerActor = ActorPtr.Get();//载具
					APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(ThisInterface->GetActor());//上载具的玩家
					if (IsValid(PlayerCharacter) && IsValid(ServerActor) && IsValid(ServerActor->GetMesh()) && IsValid(ServerActor->GetMesh()->SkeletalMesh))
					{
						PlayerCharacter->AttachToComponent(ServerActor->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, FName(*SocketName));//插槽先预留
						PlayerCharacter->SetActorRelativeLocation(FVector(0.0f, 0.0f, PlayerCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()));
						PlayerCharacter->SetActorRotation(ServerActor->GetActorRotation());
						ServerActor->OnModelChangeAppearanceOverDelegate.Remove(ThisInterface->MountVehicleHandle);
					}
				});
			}
			else
			{
				PlayerCharacter->AttachToComponent(MeshComp, FAttachmentTransformRules::KeepRelativeTransform, FName(*SocketName));//插槽先预留
				PlayerCharacter->SetActorRelativeLocation(FVector(0.0f, 0.0f, PlayerCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()));
				PlayerCharacter->SetActorRotation(MovingPlatformVehicleCharacter->GetActorRotation());
				//PlayerCharacter->SetActorRelativeRotation(FRotator(0.0f, 90.0f, 0.0f));
			}
		}

		// 屏蔽位置同步
		PlayerCharacter->SetEnableSyncServerPos(false);
		PlayerCharacter->GetFilterComponent()->SetActiveComponentTick(false);
	}

	if (EntityID == UGolbalBPFunctionLibrary::GetPlayerID())
	{
		//MovingPlatformVehicleCharacter->SwitchCamera(true);//转换摄像机视角
		MovingPlatformVehicleCharacter->SwitchMoveVehicleMode(true);
		//通知UI显示下坐骑按钮
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnSetDismountVehicleVisibility.Broadcast(true);
		}

		if (EntityID == InDriverID)
		{
			//玩家是司机则玩家控制载具
			MovingPlatformVehicle* MovingPlatformVehicleEntity = (MovingPlatformVehicle*)(VehicleEntity);
			if (MovingPlatformVehicleEntity != nullptr)
			{
				MovingPlatformVehicleEntity->OnStartControl(InDriverID);
			}
		}
	}
}

void URoleSpaceContentInterface::CLIENT_OnDismountVehicle_Implementation(int32 InVehicleID)
{
	if (VehicleID == InVehicleID)
	{
		VehicleID = 0;
		if (IsValid(GetActor()))
		{
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
			if (IsValid(PlayerCharacter))
			{
				PlayerCharacter->GetCharacterMovement()->SetActive(true);
				AActor* ParentActor = PlayerCharacter->GetAttachParentActor();
				if (IsValid(ParentActor))
				{
					USkeletalMeshComponent* CoatsPartMesh = Cast<USkeletalMeshComponent>(PlayerCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_COATS));
					CoatsPartMesh->SetSkeletalMesh(nullptr);
					PlayerCharacter->DetachFromActor(FDetachmentTransformRules::KeepWorldTransform);
					PlayerCharacter->AddActorWorldOffset(FVector(0, 300, 0), true);
					FVector Pos = PlayerCharacter->GetGroundPosition();
					PlayerCharacter->SetActorLocation(Pos);
				}
				else
				{
					//加上这个以防止玩家还没上坐骑就按了快捷键调了下坐骑
					AServerCharacter* ServerActor = Cast<AServerCharacter>(ParentActor);
					if (IsValid(ServerActor) && MountVehicleHandle.IsValid())
					{
						ServerActor->OnModelChangeAppearanceOverDelegate.Remove(MountVehicleHandle);
						MountVehicleHandle.Reset();
					}
				}
				PlayerCharacter->CreateAppearance();
				if (EntityID == UGolbalBPFunctionLibrary::GetPlayerID())
				{
					KBEngine::Entity* VehicleEntity = UGolbalBPFunctionLibrary::FindEntity(InVehicleID);
					if (VehicleEntity == nullptr) return;
					AActor* VehicleActor = VehicleEntity->Actor();
					if (!IsValid(VehicleActor)) return;
					AMovingPlatformVehicleCharacter* MovingPlatformVehicleCharacter = Cast<AMovingPlatformVehicleCharacter>(VehicleActor);
					if (!IsValid(MovingPlatformVehicleCharacter)) return;
					//MovingPlatformVehicleCharacter->SwitchCamera(false);//转换摄像机视角
					MovingPlatformVehicleCharacter->SwitchMoveVehicleMode(false);
					//通知UI隐藏下坐骑按钮
					if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
					{
						UUECS3GameInstance::Instance->GEventManager->OnSetDismountVehicleVisibility.Broadcast(false);
					}

					if (EntityID == DriverID)
						//玩家是司机则停止控制
					{
						MovingPlatformVehicle* MovingPlatformVehicleEntity = (MovingPlatformVehicle*)(VehicleEntity);
						if (MovingPlatformVehicleEntity != nullptr)
						{
							MovingPlatformVehicleEntity->OnStopControl();
						}
					}
				}
				// 开启位置同步
				PlayerCharacter->SetEnableSyncServerPos(true);
				PlayerCharacter->GetFilterComponent()->SetActiveComponentTick(true);
			}
		}
		DriverID = 0;
	}	
}

void URoleSpaceContentInterface::OnOpenWindow(const FString& winID, const int32& isOpen)
{

	if (isOpen == 1) {
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, winID);
		}
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnOpenTestWindowByGM.Broadcast(isOpen);
		}
	}
	else
	{
		UBaseWindow* window = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(winID);
		if (window) {
			window->Destroy();
		}
	}
	
}

void URoleSpaceContentInterface::CLIENT_OnJiYuanSpaceJieSuan_Implementation(const FString& itemStr, uint8 grade, const FString& timeStr, int32 dieNum, uint8 countDown)
{
}

void URoleSpaceContentInterface::CLIENT_WXHJChangeAttr_Implementation(const int32& AttrType)
{
}
void URoleSpaceContentInterface::CLIENT_ShowWXHJAttrUI_Implementation(const int32& isOpen)
{
}

void URoleSpaceContentInterface::CLIENT_PlayEffect(const FString& effectID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ParticleManager))
	{
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(effectID, 0.0f, GetActor(), GetActor());
	}
}

void URoleSpaceContentInterface::CLIENT_PlaySound(const FString& soundID)
{
	if (IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		UGolbalBPFunctionLibrary::AudioManager()->PlayVoice(soundID);
	}
}

void URoleSpaceContentInterface::SetYCJMDBulletSlotMax(const int32& BulletID)
{
	YCJMDBulletID = BulletID;
	FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(YCJMDBulletID);
	YCJMDBulletMaxAmont = ItemData.MaxTakeAmount > 100 ? 100 : ItemData.MaxTakeAmount;
}

void URoleSpaceContentInterface::CreateTempEquipBar(const FVariant& variant)
{
	//TMap<int32 itemorder, int32 itemid>
	TArray<int32> ItemOrders;
	TArray<int32> ItemIDs;
	TMap<int32, int32> itemMaps = FDICT_INT_INT(variant).dictData1;
	for (auto It = itemMaps.CreateConstIterator(); It; ++It) 
	{
		ItemOrders.Add(It.Key());
		ItemIDs.Add(It.Value());
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCreateTempEquipBar.Broadcast(ItemOrders, ItemIDs);
	}
}

void URoleSpaceContentInterface::RemoveTempEquipBar()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRemoveTempEquipBar.Broadcast();
	}
}

void URoleSpaceContentInterface::ShowZYJJReward(const FVariant & rewardData)
{
	FZYJJ_REWARD_DATA data = FZYJJ_REWARD_DATA(rewardData);
	ZYJJRewardData.Exp = data.exp;
	ZYJJRewardData.Feats = data.feats;
	ZYJJRewardData.Exploit = data.exploit;
	ZYJJRewardData.Contribution = data.contribution;

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnSetZYJJReward.Broadcast(ZYJJRewardData);
	}
}

void URoleSpaceContentInterface::ShowYCJMDFinalUI()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("YCJMDSettlementWnd"));
	}	
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowYCJMDFinalUI.Broadcast();
	}
}

CONTROL_COMPILE_OPTIMIZE_END


