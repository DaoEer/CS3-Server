
#include "AtkState.h"
#include "Manager/AtkStateMar.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/SpringArmComponentEX.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/ForceManager.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "Manager/AutoFightMar.h"
#include "Manager/CustomTimerManager.h"
#include "Component/SpringArmComponentEX.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "GameFramework/SpringArmComponent.h"

CONTROL_COMPILE_OPTIMIZE_START

TMap<EATTACT_STATE, int32> UAtkStateBase::PriorityDictionary;

UAtkStateBase::UAtkStateBase()
{
	
}

UAtkStateBase::~UAtkStateBase()
{

}

UAtkStateBase* UAtkStateBase::Create(EATTACT_STATE State)
{
	if (UAtkStateBase::PriorityDictionary.Num() <= 0)
	{
		UAtkStateBase::AddPriorityToDictionary();
	}

	UAtkStateBase* AtkState = nullptr;

	switch (State)
	{
	case EATTACT_STATE::NULL_ATT:
		AtkState = NewObject<UAtkNullState>();
		break;
	case EATTACT_STATE::CONTINUITY_ATT:
		AtkState = NewObject<UAtkContinuityState>();
		break;
	case EATTACT_STATE::AUTO_ATT:
		AtkState = NewObject<UAtkAutoFightState>();
		break;
	case EATTACT_STATE::AUTO_ONCE_ATT:
		AtkState = NewObject<UAtkAutoOnceState>();
		break;
	case EATTACT_STATE::SKILL_ONCE_ATT:
		AtkState = NewObject<UAtkSkillOnceState>();
		break;
	case EATTACT_STATE::AUTO_HOMING_SPELL_ATT:
		AtkState = NewObject<UAtkHomingSpellOnceState>();
		break;
	case EATTACT_STATE::HALF_HOMING_SPELL_ATT:
		AtkState = NewObject<UAtkHalfHomingSpellOnceState>();
		break;
	case EATTACT_STATE::AUTO_FIGHT_IN_STORY:
		AtkState = NewObject<UAtkFightInStoryState>();
		break;
	case EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL:
		AtkState = NewObject<UAtkFightInXinMoState>();
		break;
	case EATTACT_STATE::ARDER_FISH_MODE:
		AtkState = NewObject<UArderFishState>();
		break;
	case EATTACT_STATE::ARDER_JINGSU_MODE:
		AtkState = NewObject<UArderJingSuState>();
		break;
	case EATTACT_STATE::BEHAVIOR_CONFUSION:
		AtkState = NewObject<UConfusionState>();
		break;
	case EATTACT_STATE::BEHAVIOR_GLIDING:
		AtkState = NewObject<UGlidingState>();
		break;
	case EATTACT_STATE::BEHAVIOR_SHIELD:
		AtkState = NewObject<UPutOnShieldMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY:
		AtkState = NewObject<UFlyOrbitMode>();
		break;
	case EATTACT_STATE::NAVIGATE_MOVE:
		AtkState = NewObject<UNavigateMoveMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_HEHUA:
		AtkState = NewObject<UOnHehuaMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_LEIZHEN:
		AtkState = NewObject<ULeiZhenMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_SHOOT:
		AtkState = NewObject<UShootMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_CHAOFENG:
		AtkState = NewObject<UChaoFengMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_SHENFENGMIJING:
		AtkState = NewObject<UShenFengMiJingMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_FALL:
		AtkState = NewObject<UFallMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_BAGUAZHEN:
		AtkState = NewObject<UBaGuaZhenMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_FEISHENG:
		AtkState = NewObject<UFeiShengState>();
		break;
	case EATTACT_STATE::BEHAVIOR_MIJING:
		AtkState = NewObject<UArderMiJingState>();
		break;
	case EATTACT_STATE::BEHAVIOR_BATTERY:
		AtkState = NewObject<UBatteryState>();
		break;
	case EATTACT_STATE::BEHAVIOR_GHOSTEYE:
		AtkState = NewObject<UGhostEyeState>();
		break;
	case EATTACT_STATE::BEHAVIOR_TRAINSOLDIER:
		AtkState = NewObject<UTrainSoldierMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_EQUIPBUILD:
		AtkState = NewObject<UEquipBuildMode>();
		break;
	case EATTACT_STATE::BEHAVIOR_MOVEVEHICLE:
		AtkState = NewObject<UMoveVehicleMode>();
		break;
	default:
		break;
	}
	if (AtkState)
	{
		AtkState->InitStateData();
	}

	return AtkState;
}

void UAtkStateBase::InitStateData()
{
	if (UAtkStateBase::PriorityDictionary.Num() > 0)
	{
		if (UAtkStateBase::PriorityDictionary.Contains(GetAttState()))
		{
			Priority = *(UAtkStateBase::PriorityDictionary.Find(GetAttState()));
			return;
		}
	}
	Priority = 0;
}

void UAtkStateBase::Enter(TArray<FVariant> Parameters)
{
	bIsLeaveing = false;
}

void UAtkStateBase::Leave(TArray<FVariant> Parameters)
{
	bIsLeaveing = true;
}

void UAtkStateBase::AddPriorityToDictionary()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		//获取配置数据
		auto OperationPriorityTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_OPERATION_MODE);
		TArray<FOperationModeTable* > OperationPriorities;

		if (OperationPriorityTable)
		{
			//获取所有优先级数据
			OperationPriorityTable->GetAllRows<FOperationModeTable>(OperationPriorities);

			//匹配模式
			for (auto OperationPriority : OperationPriorities)
			{
				PriorityDictionary.Add(OperationPriority->OperationMode, OperationPriority->Priority);
			}
		}
	}
}

void UAtkNullState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::NULL_ATT, false);
	}
}

void UAtkNullState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkContinuityState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
}

void UAtkContinuityState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::CONTINUITY_ATT, false);
	}
}

void UAtkContinuityState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkAutoFightState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_TARGET);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_POS);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::PICKUP_ITEM);
}

void UAtkAutoFightState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UAutoFightMar* AutoFightMar = UAutoFightMar::GetInstanceByCS3GameInstance();
	if (IsValid(AutoFightMar))
	{
		AutoFightMar->OnBeginAutomaticFightOver();
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::AUTO_ATT, false);
	}
	///<自动战斗定时器30分钟退出自动战斗
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(LeaveAtkStateHandle, this, &UAtkAutoFightState::OnLeaveAtkState, 60 * 30.0f, false);
	}
}

void UAtkAutoFightState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);
	if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->CustomTimerManager->IsTimerActive(LeaveAtkStateHandle))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LeaveAtkStateHandle);
	}
	if (Parameters.Num() >= 2)
	{
		UAutoFightMar* AutoFightMar = UAutoFightMar::GetInstanceByCS3GameInstance();
		if (IsValid(AutoFightMar))
		{
			EBreakAutomaticType BreakType = (EBreakAutomaticType)Parameters[0].GetValue<uint8>();
			AutoFightMar->OnBreakFightSuccessed(BreakType, Parameters[1].GetValue<FName>());
		}
	}
	else
	{
		CS3_Warning(TEXT(" UAtkAutoFightState::Leave --- Parameters Is Error!"));
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkAutoFightState::OnLeaveAtkState()
{
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (IsValid(AtkStateMar))
	{
		AtkStateMar->SwitchAutoFight(false, EBreakAutomaticType::NoneBreakType);
	}	
}

void UAtkAutoOnceState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
}

void UAtkAutoOnceState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::AUTO_ONCE_ATT, false);
	}
	
}

void UAtkAutoOnceState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkSkillOnceState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::SKILL_ONCE_ATT, false);
	}
}

void UAtkSkillOnceState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkHomingSpellOnceState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_TARGET);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_POS);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
}

void UAtkHomingSpellOnceState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->GetAtkStateMar()->SwitchHalfHomingSpellAtt(false);
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::AUTO_HOMING_SPELL_ATT, false);
	}
}

void UAtkHomingSpellOnceState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkFightInStoryState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::AUTO_FIGHT_IN_STORY, false);
	}
}

void UAtkFightInStoryState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkFightInXinMoState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_TARGET);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
}

void UAtkFightInXinMoState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_XINMO, true);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL, false);
	}
	SetXinMoParameters(Parameters);
}

void UAtkFightInXinMoState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_XINMO, false);
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->EndAutoAttackFriendEntity();
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkFightInXinMoState::GetXinMoData(TArray<FString>& _ExcludeList, TArray<FString>& _ActForbids)
{
	_ExcludeList = ExcludeList;
	_ActForbids = ActForbids;
}

void UAtkFightInXinMoState::SetXinMoParameters(TArray<FVariant> Parameters)
{
	if (Parameters.Num()>0)
	{
		KBEngine::FVariantArray arr = Parameters[0].GetValue<KBEngine::FVariantArray>();
		for (auto item : arr)
		{
			ExcludeList.Add(item.GetValue<FString>());
		}
		if (Parameters.Num()>1)
		{
			arr = Parameters[1].GetValue<KBEngine::FVariantArray>();
			for (auto item : arr)
			{
				ActForbids.Add(item.GetValue<FString>());
			}
		}
	}
}

void UChaoFengMode::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_TARGET);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
}

void UChaoFengMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_XINMO, true);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_CHAOFENG, false);
	}
}

void UChaoFengMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_XINMO, false);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UAtkHalfHomingSpellOnceState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_TARGET);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_POS);
	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::USE_SKILL);
}

void UAtkHalfHomingSpellOnceState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->GetAtkStateMar()->SwitchHomingSpellAtt(false);
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::HALF_HOMING_SPELL_ATT, false);
	}
}

void UAtkHalfHomingSpellOnceState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

UArderFishState::UArderFishState()
{
	CamUpValue = 80.0f;
}

void UArderFishState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);
	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//获得玩家
	APlayerCharacter* PlayerChara = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//获得摄像机臂杆
	USpringArmComponent* SpringArmCompent = nullptr;
	if (IsValid(PlayerChara))
	{
		SpringArmCompent = PlayerChara->SpringArmCompent;
	}

	if (SpringArmCompent)
	{
		SpringArmCompent->SocketOffset = FVector(SpringArmCompent->SocketOffset.X,
			SpringArmCompent->SocketOffset.Y, SpringArmCompent->SocketOffset.Z + CamUpValue);
	}

	PlayerChara->SetOrientRotationToMovement(false, false);

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_FISH, true);
		PlayerController->SetIsEnabledQuickBar(false);
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::ARDER_FISH_MODE, false);
	}
}

void UArderFishState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//获得玩家
	APlayerCharacter* PlayerChara = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//获得摄像机臂杆
	USpringArmComponent* SpringArmCompent = nullptr;
	if (IsValid(PlayerChara))
	{
		SpringArmCompent = PlayerChara->SpringArmCompent;
	}

	if (SpringArmCompent)
	{
		SpringArmCompent->SocketOffset = FVector(SpringArmCompent->SocketOffset.X,
			SpringArmCompent->SocketOffset.Y, SpringArmCompent->SocketOffset.Z - CamUpValue);
	}

	PlayerChara->SetOrientRotationToMovement(false, false,1,true);

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_FISH, false);
		PlayerController->SetIsEnabledQuickBar(true);
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UArderJingSuState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::VehicleControlMode, CC_MODE_REASON::CCM_VEHICLE_CONTROLLER_MODE);
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_JING_SU, true);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::ARDER_JINGSU_MODE);
	}
}

void UArderJingSuState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_JING_SU, false);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UConfusionState::InitStateData()
{
	Super::InitStateData();

	ActivateBehav.Add(ECAN_ACTIVATE_BEHAV::MOVE_TO_POS);
}

void UConfusionState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_CONFUSION,true);
	}
	else
	{
		CS3_Warning(TEXT("UConfusionState::Enter --- PlayerController Is Null!"));
	}
	
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_CONFUSION, false);
	}
}

void UConfusionState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_CONFUSION, false);

		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		if (IsValid(OperationModeMgr))
		{
			OperationModeMgr->RecoveryMode();
		}
	}
	else
	{
		CS3_Warning(TEXT("UConfusionState::Leave --- PlayerController Is Null!"));
	}
}

UGlidingState::~UGlidingState()
{
	for (auto& FlyTimeHandle : FlyTimeHandles)
	{
		if (FlyTimeHandle.IsValid() && IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(FlyTimeHandle);
		}
	}
}

void UGlidingState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	if (Parameters.Num() >= 2)
	{
		OnEnterGliding(Parameters[0].GetValue<float>(), Parameters[1].GetValue<float>());
	}
	else
	{
		CS3_Warning(TEXT(" UGlidingState::Leave --- Parameters Is Error!"));
	}
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	ACS3PlayerController* PlayerCon = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::GlidingMode, CC_MODE_REASON::CCM_GLIDING_CONTROLLER_MODE);
	}

	if (IsValid(PlayerCon))
	{
		GlidingCamScaleHeadle = PlayerCon->SetCameraRotateScale(0.5f);
		PlayerCon->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_GLIDING, true);
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_GLIDING, false);
	}
}

void UGlidingState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	ACS3PlayerController* PlayerCon = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	OnLeaveGliding();

	if (IsValid(PlayerCon))
	{
		PlayerCon->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_GLIDING, false);
		PlayerCon->RemoveCameraRotateScale(GlidingCamScaleHeadle);
		GlidingCamScaleHeadle = -1;
	}
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->RecoveryMode();
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

int32 UGlidingState::AddFlyForce(int Dire, float ForceSpeed, float ForceTime)
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(ForceMana) && IsValid(PlayerActor))
	{
		int32 FlyForceID = -1;

		switch (Dire)
		{
		case 1:
			FlyForceID = ForceMana->AddForce(PlayerActor, ForceSpeed, ELOCAL_FORCE_DIRE::UP_DIRE);
			break;
		case 2:
			FlyForceID = ForceMana->AddForce(PlayerActor, ForceSpeed, ELOCAL_FORCE_DIRE::DOWN_DIRE);
			break;
		case 3:
			FlyForceID = ForceMana->AddForce(PlayerActor, ForceSpeed, ELOCAL_FORCE_DIRE::LIFT_DIRE);
			break;
		case 4:
			FlyForceID = ForceMana->AddForce(PlayerActor, ForceSpeed, ELOCAL_FORCE_DIRE::RIGHT_DIRE);
			break;
		case 5:
			FlyForceID = ForceMana->AddForce(PlayerActor, ForceSpeed, ELOCAL_FORCE_DIRE::FORWARD_DIRE);
			break;
		case 6:
			FlyForceID = ForceMana->AddForce(PlayerActor, ForceSpeed, ELOCAL_FORCE_DIRE::BACK_DIRE);
			break;
		default:
			CS3_Warning(TEXT("UGlidingState::AddFlyForce ---AddFlyForce can not find ELOCAL_FORCE_DIRE element!"));
			break;
		}

		if (ForceTime > 0.0f)
		{
			FTimerHandle FlyTimeHandle;
			TWeakObjectPtr<UGlidingState> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->
				SetTimer(this, FlyTimeHandle, FTimerDelegate::CreateLambda([DelayThisPtr, FlyForceID]()
			{
				AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
				UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();
				if (DelayThisPtr.IsValid() && IsValid(PlayerActor) && IsValid(ForceMana))
				{
					UGlidingState* ThisPtr = DelayThisPtr.Get();
					if (ThisPtr->FlyForceIDArr.Contains(FlyForceID))
					{
						ThisPtr->FlyForceIDArr.Remove(FlyForceID);
					}
					ForceMana->StopForces(PlayerActor, FlyForceID);
				}
			}), ForceTime, false);
			FlyTimeHandles.Add(FlyTimeHandle);
		}
		else
		{
			ForceMana->StopForces(PlayerActor, FlyForceID);

			CS3_Warning(TEXT("UGlidingState::AddFlyForce -- ForceTime <= 0! "));
			return -1;
		}

		FlyForceIDArr.Add(FlyForceID);

		return FlyForceID;
	}

	CS3_Warning(TEXT("UGlidingState::AddFlyForce -- UForceManager Or PlayerActor Is Null!"));
	return -1;
}

void UGlidingState::OnEnterGliding(float ForwardForceSpeed, float DownForceSpeed)
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(PlayerActor))
	{
		//开启飞行模式
		PlayerActor->GetCharacterMovement()->SetMovementMode(MOVE_Flying);

		//添加对应的前进和下落的速度
		AddAutoFlyForce(ForwardForceSpeed, DownForceSpeed);
	}
}

void UGlidingState::OnLeaveGliding()
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(PlayerActor))
	{
		//关闭飞行模式
		PlayerActor->GetCharacterMovement()->SetMovementMode(MOVE_Walking);

		//停止所有的飞行力
		StopFlyForce();
	}
}

void UGlidingState::AddAutoFlyForce(float ForwardForceSpeed, float DownForceSpeed)
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(ForceMana) && IsValid(PlayerActor))
	{
		int32 FlyForceID = -1;

		FlyForceID = ForceMana->AddForce(PlayerActor, ForwardForceSpeed, ELOCAL_FORCE_DIRE::FORWARD_DIRE);
		FlyForceIDArr.Add(FlyForceID);

		FlyForceID = ForceMana->AddForce(PlayerActor, DownForceSpeed, ELOCAL_FORCE_DIRE::DOWN_DIRE);
		FlyForceIDArr.Add(FlyForceID);

		return;
	}

	CS3_Warning(TEXT("UGlidingState::AddAutoFlyForce -- UForceManager Or PlayerActor Is Null!"));
}

void UGlidingState::StopFlyForce()
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(ForceMana) && IsValid(PlayerActor))
	{
		ForceMana->StopAllForces(PlayerActor, FlyForceIDArr);
	}
}

void UPutOnShieldMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_SHIELD, true);

		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		if (IsValid(OperationModeMgr))
		{
			OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_SHIELD, false);
		}
	}
	else
	{
		CS3_Warning(TEXT("UPutOnShieldMode::Enter: --- PlayerController Is Null!"));
	}

}

void UPutOnShieldMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_SHIELD, false);

		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		if (IsValid(OperationModeMgr))
		{
			OperationModeMgr->RecoveryMode();
		}
	}
	else
	{
		CS3_Warning(TEXT("UPutOnShieldMode::Leave: --- PlayerController Is Null!"));
	}
}

void UFlyOrbitMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_FLY_ORBIT, true);
	}
	else
	{
		CS3_Warning(TEXT("UFlyOrbitMode::Enter: --- PlayerController Is Null!"));
	}

	if (Parameters.Num() > 0)
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

		if (IsValid(PlayerActor))
		{
			PlayerActor->StartFlyPatrol(Parameters[0].GetValue<FString>());
		}
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
		
		if (IsValid(ControllerModeMgr))
		{
			ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::FlyDekuvery, CC_MODE_REASON::CCM_FLYDK_CONTROLLER_MODE, true);
		}

		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		if (IsValid(OperationModeMgr))
		{
			OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY, false);	//操作模式管理器			
			OperationModeMgr->bIsCanTurn = false;
		}
	}
	else
	{
		CS3_Warning(TEXT("UFlyDeliveryMode::Enter: --- Parameters Is Error!"));
	}
}

void UFlyOrbitMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_FLY_ORBIT, false);
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

		if (IsValid(ControllerModeMgr))
		{
			ControllerModeMgr->RecoverySettingMode();
		}
		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		if (IsValid(OperationModeMgr))
		{
			OperationModeMgr->bIsCanTurn = true;
			OperationModeMgr->RecoveryMode();
		}

	}
	else
	{
		CS3_Warning(TEXT("UFlyOrbitMode::Leave: --- PlayerController Is Null!"));
	}

	if (Parameters.Num() > 0)
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

		if (IsValid(PlayerActor))
		{
			PlayerActor->StopFlyPatrol(FSTRING_TO_FLOAT(Parameters[0].GetValue<FString>()));
		}
	}
	else
	{
		CS3_Warning(TEXT("UFlyDeliveryMode::Leave: --- Parameters Is Error!"));
	}
}

void UNavigateMoveMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	if (Parameters.Num() >= 6)
	{
		APlayerCharacter* playerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
		bIsEnterExecuteOperation = false;
		bIsLeaveExecuteOperation = false;
		if (IsValid(playerActor))
		{			
			float AgentMaxStepHeight, AgentMaxSlope;
			GConfig->GetFloat(TEXT("/Script/NavigationSystem.RecastNavMesh"), TEXT("AgentMaxStepHeight"), AgentMaxStepHeight, GEngineIni);
			GConfig->GetFloat(TEXT("/Script/NavigationSystem.RecastNavMesh"), TEXT("AgentMaxSlope"), AgentMaxSlope, GEngineIni);
			playerActor->SetCharacterMovementWalkProperty(AgentMaxStepHeight, AgentMaxSlope);
			playerActor->StartAutoNavigate(Parameters[0].GetValue<FVector>(), Parameters[1].GetValue<float>(),
				Parameters[2].GetValue<FString>(), Parameters[3].GetValue<int>(), Parameters[4].GetValue<bool>(), Parameters[5].GetValue<int>());
		}

		if (IsValid(OperationModeMgr) && !bIsEnterExecuteOperation)
		{
			bIsEnterExecuteOperation = true;
			OperationModeMgr->ChangeMode(EATTACT_STATE::NAVIGATE_MOVE);
		}
	}
	else
	{
		CS3_Warning(TEXT("UNavigateMoveMode::Enter: --- Parameters Is Error!"));
	}
}

void UNavigateMoveMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	if (Parameters.Num() > 0)
	{
		APlayerCharacter* playerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		
		if (IsValid(playerActor)&& !bIsLeaveExecuteOperation)
		{
			bIsLeaveExecuteOperation =true;
			playerActor->SetCharacterMovementDefaultWalkProperty();
			playerActor->StopAutoNavigate(Parameters[0].GetValue<bool>());

			UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
			if (IsValid(OperationModeMgr))
			{
				OperationModeMgr->RecoveryMode();
				bIsEnterExecuteOperation = true;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("UNavigateMoveMode::Leave: --- Parameters Is Error!"));
	}
}

void UOnHehuaMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HEHUA, true);
	}
	else
	{
		CS3_Warning(TEXT("UOnHehuaMode::Enter: --- PlayerController Is Null!"));
	}
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::HeHuaMode, CC_MODE_REASON::CCM_HEHUA_CONTROLLER_MODE, true);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_HEHUA);
	}
}

void UOnHehuaMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HEHUA, false);
	}
	else
	{
		CS3_Warning(TEXT("UOnHehuaMode::Leave: --- PlayerController Is Null!"));
	}
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->RecoverySettingMode();
	}

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

#pragma region	雷阵模式
void ULeiZhenMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::LeiZhen, CC_MODE_REASON::CCM_LEIZHEN_CONTROLLER_MODE);
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_LEIZHEN, true);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_LEIZHEN);
	}
}

void ULeiZhenMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_LEIZHEN, false);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

#pragma endregion

#pragma region	射击模式
void UShootMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	if (Parameters.Num()>0)
	{
		StateType = Parameters[0].GetValue<FString>();
	}
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::ShootMode, CC_MODE_REASON::CCM_SHOOTMODE_CONTROLLER_MODE,true);
		if (!StateType.Compare(TEXT("HUOLINGFU")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HUOLINGFU, true);
		}
		else if (!StateType.Compare(TEXT("TPS")))
		{
			TArray<FString> Values;
			Values.Add(TEXT("1"));
			ControllerModeMgr->ExecuteInputInfor(TEXT("SwitchCone"), "", 0.0f, Values);
		}
		else if (!StateType.Compare(TEXT("ZHG")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_ZHENHAIGONG, true);
		}
		else if(!StateType.Compare(TEXT("SFC")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_SHIFANGCHENG, true);
			if (Parameters.Num() > 1)
			{
				TArray<FString>ParamStrings = UGolbalBPFunctionLibrary::SplitString(Parameters[1].GetValue<FString>());
				if (ParamStrings.Num()>1)
				{
					PlayerController->SetUpAndDownAngle(FSTRING_TO_FLOAT(ParamStrings[0]), FSTRING_TO_FLOAT(ParamStrings[1]));
				}
				if (ParamStrings.Num() > 2)
				{//获取玩家
					APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
					if (IsValid(PlayerActor))
					{
						UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, FSTRING_TO_FLOAT(ParamStrings[2]));
						if (ParamStrings.Num() > 3)
						{
							UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(FSTRING_TO_FLOAT(ParamStrings[3]), 0.0f, 0.0f));
						}
					}
				}
				TArray<FString> Values;
				Values.Add(TEXT("1"));
				ControllerModeMgr->ExecuteInputInfor(TEXT("SwitchCone"), "", 0.0f, Values);
			}			
		}
		else if (!StateType.Compare(TEXT("JINGSHIDONGKU")))
		{
			if (Parameters.Num() > 1)
			{
				OtherValue = Parameters[1].GetValue<FString>();
			}
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HUOLINGFU, true);
		}
		else if (!StateType.Compare(TEXT("YCJMD")))
		{
			if (Parameters.Num() > 1)
			{
				OtherValue = Parameters[1].GetValue<FString>();
			}
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_YCJMD, true);
			if (IsValid(OperationModeMgr))
			{
				OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_SHOOTYCJMD);
			}
		}
		else if (!StateType.Compare(TEXT("HSBZ")))
		{
			if (Parameters.Num() > 1)
			{
				OtherValue = Parameters[1].GetValue<FString>();
			}
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HUOLINGFU, true);
		}
	}

	if (IsValid(OperationModeMgr)&& StateType.Compare(TEXT("YCJMD")))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_SHOOT);
	}
}

void UShootMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (ControllerModeMgr)
	{
		if (!StateType.Compare(TEXT("HUOLINGFU")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HUOLINGFU, false);
		}
		else if (!StateType.Compare(TEXT("TPS")))
		{
			TArray<FString> Values;
			Values.Add(TEXT("0"));
			ControllerModeMgr->ExecuteInputInfor(TEXT("SwitchCone"), "", 0.0f, Values);
		}
		else if (!StateType.Compare(TEXT("ZHG")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_ZHENHAIGONG, false);
		}
		else if (!StateType.Compare(TEXT("SFC")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_SHIFANGCHENG, false);
			PlayerController->SetUpAndDownAngle(-60.0f, 45.0f);
			// 获取玩家
			APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (IsValid(PlayerActor))
			{
				UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 1500.0f);
				UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(-300.0f, 0.0f, 0.0f));
			}
			TArray<FString> Values;
			Values.Add(TEXT("0"));
			ControllerModeMgr->ExecuteInputInfor(TEXT("SwitchCone"), "", 0.0f, Values);
		}
		else if (!StateType.Compare(TEXT("JINGSHIDONGKU")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HUOLINGFU, false);
		}
		else if (!StateType.Compare(TEXT("YCJMD")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_YCJMD, false);
		}
		else if (!StateType.Compare(TEXT("HSBZ")))
		{
			PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_HUOLINGFU, false);
		}

		ControllerModeMgr->RecoverySettingMode();
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
	StateType = TEXT("");
}

#pragma endregion
#pragma region	神风秘径模式
void UShenFengMiJingMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::ShenFengMiJing, CC_MODE_REASON::CCM_SFMJ_CONTROLLER_MODE);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_SHENFENGMIJING);
	}

}

void UShenFengMiJingMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}
#pragma endregion

#pragma region	神风秘径降落模式
void UFallMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::Fall, CC_MODE_REASON::CCM_SFMJJL_CONTROLLER_MODE);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_FALL);
	}

}

void UFallMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}
#pragma endregion

#pragma region	八卦阵模式
void UBaGuaZhenMode::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_BAGUAZHEN);
	}
	if (Parameters.Num() > 0)
	{
		Scale = FSTRING_TO_FLOAT(Parameters[0].GetValue<FString>());
	}
	SetCanMove(true);
}

void UBaGuaZhenMode::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UBaGuaZhenMode::SetCanMove(bool InCanMove)
{
	bCanMove = InCanMove;
}

bool UBaGuaZhenMode::IsCanMove()
{
	return bCanMove;
}

#pragma endregion

#pragma region	飞升模式
void UFeiShengState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::GoUp, CC_MODE_REASON::CCM_GOUP_CONTROLLER_MODE);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_FEISHENG);
	}

	// 获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerActor))
	{
		PlayerActor->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		if (!FeiShengInitTargetActor)
		{
			UClass* GameCharacterClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("GameCharacter"));
			FeiShengInitTargetActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(GameCharacterClass);
			FeiShengInitTargetActor->SetActorEnableCollision(false);
		}
		FVector CharacterDirection = PlayerActor->GetActorForwardVector();
		FVector ToLocation = PlayerActor->GetActorLocation() + CharacterDirection * -(PlayerActor->FeiShengCameraLength);//向后移5米
		FRotator PlayerRotation = PlayerActor->GetActorRotation();
		FeiShengInitTargetActor->SetActorLocation(ToLocation);
		FeiShengInitTargetActor->SetActorRotation(PlayerRotation);
		PlayerController->SetViewTargetWithBlend(FeiShengInitTargetActor, 0.0f,
			EViewTargetBlendFunction::VTBlend_Linear, 0.0f, true);

		PlayerActor->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		PlayerActor->bUseControllerRotationYaw = true;//是否能前后左右转向
		PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;//去掉左右移动时会有轻微的转向
		PlayerController->ClientSetRotation(PlayerRotation);//当bUseControllerRotationYaw为true后，一定要移动控制器朝像
		PlayerActor->GetCharacterMovement()->MaxFlySpeed = PlayerActor->FeiShengRightSpeed;
		PlayerActor->GetCharacterMovement()->BrakingDecelerationFlying = 5000;//使角色左右移动时，松开按键能快速停止
	}
}

void UFeiShengState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
	}
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
	// 获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerActor))
	{
		PlayerActor->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
		PlayerActor->bUseControllerRotationYaw = false;
		PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 100000.0f;
		PlayerActor->SetBaseGravityScale(5.0f);
		PlayerActor->GetCharacterMovement()->MaxFlySpeed = 1500;
		PlayerActor->GetCharacterMovement()->BrakingDecelerationFlying = 0;

		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 1500.0f);
		FRotator Rotation = PlayerActor->GetActorRotation();
		PlayerController->SetControlRotation(Rotation - FRotator(20.0f, 0.0f, 0.0f));
		PlayerController->SetViewTargetWithBlend(PlayerActor, 0.0f,
			EViewTargetBlendFunction::VTBlend_Linear, 0.0f, false);
	}
}
#pragma endregion



void UArderMiJingState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::VehicleControlMode, CC_MODE_REASON::CCM_AMJ_CONTROLLER_MODE);
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_JING_SU, true);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_MIJING);
	}
}

void UArderMiJingState::Leave(TArray<FVariant> Parameters)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_JING_SU, false);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UBatteryState::Enter(TArray<FVariant> Parameters)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::BatteryMode, CC_MODE_REASON::CCM_BATTERY_CONTROLLER_MODE);
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_BATTERY, true);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_BATTERY);
	}
}

void UBatteryState::Leave(TArray<FVariant> Parameters)
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (ControllerModeMgr)
	{
		ControllerModeMgr->RecoveryMode();
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_BATTERY, false);
	}

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
	Super::Leave(Parameters);
}

void UGhostEyeState::Enter(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Enter(Parameters);

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_GHOSTEYE, true);
	}
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::GhostEye, CC_MODE_REASON::CCM_GHOSTEYE_CONTROLLER_MODE);
		
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_GHOSTEYE);
	}
}

void UGhostEyeState::Leave(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Leave(Parameters);

	///屏蔽按键响应
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_GHOSTEYE, false);
	}
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->RecoveryMode();
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UTrainSoldierMode::Enter(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Enter(Parameters);
	
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::TrainSoldierMode, CC_MODE_REASON::CCM_TRAIN_SOLDIER_MODE);

	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER);
	}
	if (Parameters.Num() <= 0)return;
	float ArmLength = 0.0f;
	FVector CameraRotation = FVector(0.0f, 0.0f, 0.0f);
	if (Parameters.Num() >= 2)
	{
		ArmLength = Parameters[0].GetValue<float>();
		CameraRotation = Parameters[1].GetValue<FVector>();
	}
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		USpringArmComponent* SpringArm = Player->SpringArmCompent;
		if (IsValid(SpringArm))
		{
			//设置臂长
			SpringArm->TargetArmLength = ArmLength;
			SpringArm->SetRelativeRotation(FQuat::MakeFromEuler(CameraRotation));
		}
	}
}

void UTrainSoldierMode::Leave(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->RecoveryMode();
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		Player->ResetCameraData();
		Player->SpringArmCompent->SetRelativeRotation(FRotator(0.0f, 0.0f, 0.0f));
	}
}

void UEquipBuildMode::Enter(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Enter(Parameters);
	
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_EQUIPBUILD);
	}
	if (Parameters.Num() > 1)
	{
		ScriptID = Parameters[0].GetValue<FString>();
		ItemUID = Parameters[1].GetValue<FString>();
	}
}

void UEquipBuildMode::Leave(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Leave(Parameters);

	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

void UMoveVehicleMode::Enter(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Enter(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::MoveVehicle, CC_MODE_REASON::CCM_MOVEVEHICLE_CONTROLLER_MODE);

	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_MOVEVEHICLE);
	}
}

void UMoveVehicleMode::Leave(TArray<FVariant> Parameters /*= {}*/)
{
	Super::Leave(Parameters);

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->RecoveryMode();
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->RecoveryMode();
	}
}

CONTROL_COMPILE_OPTIMIZE_END