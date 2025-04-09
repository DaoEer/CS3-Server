// Fill out your copyright notice in the Description page of Project Settings.

#include "BaseAnimInstance.h"
//UE4
#include "Animation/AnimSequence.h"
#include "Animation/AnimMontage.h"
#include "Animation/AnimInstance.h"
#include "TimerManager.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PawnMovementComponent.h"
//CS3数据
#include "GameData/CharacterData.h"
#include "GameData/GameDeFine.h"
#include "Util/CS3Debug.h"
//CS3
#include "BaseAnimMetaData.h"
#include "CS3Base/GameObject.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/ResourceManager.h"
#include "Actor/GameCharacter.h"
#include "Actor/ServerCharacter.h"
#include "Manager/GameStatus.h"
#include "Manager/ActionManager.h"
#include "Interface/StateInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Entity.h"
#include "Component/Role/JumpComponent.h"
#include "../Player/PlayerCharacter.h"
#include "Component/Role/LadderCustomMovementComponent.h"

DECLARE_CYCLE_STAT(TEXT("NativeUpdateAnimation"), STAT_UBaseAnimInstance_NativeUpdateAnimation, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("PlayAction"), STAT_UBaseAnimInstance_PlayAction, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("StarPlayAction"), STAT_StarPlayAction, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("PlayContinuousActions"), STAT_UBaseAnimInstance_PlayContinuousActions, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("CheckCanPlayNewAction"), STAT_CheckCanPlayNewAction, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("CheckActionDataValid"), STAT_CheckActionDataValid, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("CheckActionPriority"), STAT_CheckActionPriority, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("MontageEndEvent_Implementation"), STAT_MontageEndEvent_Implementation, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("PlayOverCurActionCallBack"), STAT_PlayOverCurActionCallBack, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("PlayStandbyAction"), STAT_PlayStandbyAction, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("PlayMoveAction"), STAT_PlayMoveAction, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("StopFrontAction"), STAT_StopFrontAction, STATGROUP_UBaseAnimInstance);
DECLARE_CYCLE_STAT(TEXT("UpdateActionPauseTime"), STAT_UpdateActionPauseTime, STATGROUP_UBaseAnimInstance);

CONTROL_COMPILE_OPTIMIZE_START
UBaseAnimInstance::UBaseAnimInstance():CurCharacter(nullptr),ActionDynamicId(0), 
 bTickUpdate(false)
{
	IsCompelBreak = false;

	CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK;
	BeforBackActionData = FACTION_DATA();
	CurBackActionData = FACTION_DATA();
	BeforFrontActionData = FACTION_DATA();
	CurFrontActionData = FACTION_DATA();
	CurActionPauseData = FACTION_PAUSE_DATA();
	ActionOverDelegateMap.Empty();
	ContinuousActionOverMap.Empty();
	ActionBlendOutDelegateMap.Empty();

}

UBaseAnimInstance::~UBaseAnimInstance()
{
	ClearData();
}

void UBaseAnimInstance::BeginDestroy()
{
	if (IsValid(this) && IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->ClearObjectHandles(this);
		CurCharacter = nullptr;
	}
	Super::BeginDestroy();
}

void UBaseAnimInstance::ClearData()
{
	BeforBackActionData = FACTION_DATA();
	CurBackActionData = FACTION_DATA();
	CurFrontActionData = FACTION_DATA();
	CurCharacter = nullptr;
	ActionDynamicId = 0;
	IsCompelBreak = false;
}

void UBaseAnimInstance::PostInitProperties()
{
	Super::PostInitProperties(); 
}

void UBaseAnimInstance::NativeInitializeAnimation()
{
	ClearData();	/*CST-4757 因USkeletalMeshComponent::SetAnimInstanceClass在设置新动画蓝图时,会判断如果类型和旧动画蓝图一样就不会重新创建动画蓝图实例;
					  USkeletalMeshComponent::SetSkeletalMesh默认参数会走一遍初始化流程,所以在这初始化一遍动作数据状态*/

	CurCharacter = Cast<AGameCharacter>(GetOwningActor());
	if (!CurCharacter)
	{ 
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::NativeInitializeAnimation : CurCharacter!"));
		return;
	}

	///IsPlayerControll和EntityId都作调试数据日志所用，无其他逻辑功能
	IsPlayerControll = CurCharacter->IsPlayerControlled();
	if (AServerCharacter *ServerCharacter = Cast<AServerCharacter>(CurCharacter))
	{
		if (ServerCharacter->GetSelfEntity())
		{
			EntityId = ServerCharacter->EntityId;
		}
	}

	if (!OnMontageStarted.IsAlreadyBound(this, &UBaseAnimInstance::MontageStartEvent))
	{
		OnMontageStarted.AddDynamic(this, &UBaseAnimInstance::MontageStartEvent);
	}
	if (!OnMontageEnded.IsAlreadyBound(this, &UBaseAnimInstance::MontageEndEvent))
	{ 
		OnMontageEnded.AddDynamic(this, &UBaseAnimInstance::MontageEndEvent);
	}
	if (!OnMontageBlendingOut.IsAlreadyBound(this, &UBaseAnimInstance::MontageBlendOutEvent))
	{
		OnMontageBlendingOut.AddDynamic(this, &UBaseAnimInstance::MontageBlendOutEvent);
	}

	FName InitActionId = CurCharacter->GetInitActionId();
	if (!InitActionId.IsNone())
	{
		PlayInitStandByAction(InitActionId);
	}
	else
	{
		PlayStandbyAction();
	}
}

void UBaseAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseAnimInstance_NativeUpdateAnimation);
	UpdateActionPauseTime(DeltaSeconds);

	if (!bTickUpdate)
	{
		return;
	}

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus) && 
		UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld)
	{
		return;
	}

	if (!IsValid(CurCharacter))
	{
		return;
	}	

	/*KBEngine::Entity* pEntity = CurCharacter->GetSelfEntity();
	EntityId = pEntity ? pEntity->ID() : 0;
	if (!CurCharacter->IsControlled())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseAnimInstance::NativeUpdateAnimation==id=%d,  IsPlayMove=%d"), 
			EntityId, CurCharacter->IsActiveMoveing()?1:0);
	}*/
	
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(CurCharacter);
	if (IsValid(PlayerActor) && PlayerActor->IsLadderMovement())//进入爬梯模式
	{
		ULadderCustomMovementComponent *LadderCustomMovmentCpt = PlayerActor->LadderCustomMovmentCpt;
		if (IsValid(LadderCustomMovmentCpt))
		{
			if (LadderCustomMovmentCpt->TempCustomMovementMode == CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_ROOT_MOTION)
			{
				IsClimbLaddering = LadderCustomMovmentCpt->IsRootMotionHaveUpAction;
			}
			else if (LadderCustomMovmentCpt->TempCustomMovementMode == CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_LADDER)
			{
				IsClimbLaddering = true;
				ClimbLadderActionFramePos = LadderCustomMovmentCpt->ClimbLadderActionFramePos;
			}

			/*CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseAnimInstance::NativeUpdateAnimation[LadderMovement]==id=%d,  ClimbLadderActionFramePos=%f"),
				EntityId, ClimbLadderActionFramePos);*/

			if (IsClimbLaddering)
			{
				PlayClimbLadderAction();
			}
		}
	}
	else if (IsValid(PlayerActor) && PlayerActor->IsSkyParachuteState())//进入吃鸡降落模式
	{
		if (PlayerActor->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_FALL))		// 未开伞状态
		{
			CurMoveDirection = PlayerActor->YCJMDParachuteDirX;
			CurMoveSpeed = PlayerActor->YCJMDParachuteDirY;
			PlayMoveAction();
		}
		else if (PlayerActor->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_OPEN))			// 开伞状态
		{
			CurMoveDirection = PlayerActor->YCJMDParachuteDirX;
			CurMoveSpeed = PlayerActor->YCJMDParachuteDirY;
			PlayFightMoveAction();
		}
		else
		{
			CurMoveDirection = PlayerActor->YCJMDParachuteDirX;
			CurMoveSpeed = PlayerActor->YCJMDParachuteDirY;
			PlayStandbyAction();
		}
	}
	else
	{
		if (CurCharacter->IsActiveMoveing())
		{
			IsClimbLaddering = false;
			if (IsValid(PlayerActor))//玩家
			{
				//IsFalling()用来解决主机跳跃时，导致空中按WASD键会切换到移动动作 
				//IsTheLand()用来解决同步其他角色机跳跃时，导致空中按WASD键会切换到移动动作 
				if ((PlayerActor->ActorIsPlayer() && !CurCharacter->GetCharacterMovement()->IsFalling()) ||
					(!PlayerActor->ActorIsPlayer() && IsValid(PlayerActor->JumpComponent) && PlayerActor->JumpComponent->IsTheLand))
				{
					UpdateMoveDirection();
					UpdateMoveSpeed();
					PlayMoveAction();
				}
			}
			else
			{
				//怪物
				if (!CurCharacter->GetCharacterMovement()->IsFalling())
				{
					UpdateMoveDirection();
					UpdateMoveSpeed();
					PlayMoveAction();
				}
			}
		}
		else
		{
			IsClimbLaddering = false;
			///如果是待机动作中有除了战斗、自由待机外其他的常驻待机状态【Show_FloatRun】,会导致被切回去
			if (CurBackActionData.ActionType != ACTION_TYPE_ENUM::ACTION_TYPE_STANDBY)
			{
				PlayStandbyAction();
			}
		}
	}
}

void UBaseAnimInstance::NativeUninitializeAnimation()
{
	StopFrontAction();
}

void UBaseAnimInstance::PlayAction(FName InActionId, 
	float InStartPostion /*= 0.0f*/, 
	const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/, 
	int32 InContinuousId /*= 0*/,
	const FActionBlendOutDelegate& InActionBlendOutDelegate /*= FActionBlendOutDelegate()*/)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseAnimInstance_PlayAction);

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayAction[1][EntityId=%d,  ActionDataId=%s,  InContinuousId=%d,  ChacterName=%s]"),
		EntityId, *(InActionId.ToString()), InContinuousId, *(CurCharacter->GetName()));
	//bool JumpAir_01 = InActionId.IsEqual("JumpAir_01"); 
	//bool JumpEnd_Stand = InActionId.IsEqual("JumpEnd_Stand");

	FACTION_DATA ActionData = FACTION_DATA();
	bool IsBreakFront = false;
	bool bResult = CheckCanPlayNewAction(InActionId, ActionData, IsBreakFront);
	if (bResult) 
	{
		ActionData.PlayStartPosition = InStartPostion > 0.0f ? InStartPostion : ActionData.PlayStartPosition;
		ActionData.DynamicId = ActionDynamicId++;
		ActionData.ContinuousId = InContinuousId;
		ActionOverDelegateMap.Add(ActionData.DynamicId, InActionOverDelegate);
		ActionBlendOutDelegateMap.Add(ActionData.DynamicId, InActionBlendOutDelegate);

		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayAction[2][EntityId=%d,  ActionDataId=%s,  InContinuousId=%d,  ChacterName=%s,  IsBreakFront=%d,  CurActionPauseDataIsOpen=%d]"),
			EntityId, *(InActionId.ToString()), InContinuousId, *(CurCharacter->GetName()), IsBreakFront?1:0, CurActionPauseData.IsOpen?1:0);
		
		//检测暂停的动作是否要停止
		if (CurActionPauseData.IsOpen)
		{
			//前景暂停动作需要判断后停止，背景可直接停止
			if (CurActionPauseData.ActionData.GroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
			{
				if (IsBreakFront)
				{  
					ClearPauseAction();
				}
			}
			else
			{
				ClearPauseAction();
			}
		}

		//检测前景是否要停止
		if (IsBreakFront)
		{
			if (!SaveCurFrontActionData.Id.IsNone())
			{
				SaveCurFrontActionData = FACTION_DATA();
			}
			StopFrontAction();
		}

		IsCompelBreak = false;
		StarPlayAction(ActionData);
	}
}

void UBaseAnimInstance::StarPlayAction(FACTION_DATA& InActionData)
{
	SCOPE_CYCLE_COUNTER(STAT_StarPlayAction);
	BroadcastActionReadyChange(InActionData);
	switch (InActionData.AnimType)
	{
	case ANIM_TYPE_ENUM::ANIM_TYPE_QEQUENCE:
	{
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.QequenceAction[EntityId=%d,  ActionId=%s,  ChacterName=%s]"),
				EntityId, *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}

		StartPlayBackAction(InActionData);
		break;
	}
	case ANIM_TYPE_ENUM::ANIM_TYPE_DYNAMIC_MONTAGE:
	{
		UAnimSequence* AnimSequenceBase = (UAnimSequence*)InActionData.CurAnimSquenceBase;
		BeforFrontActionData = CurFrontActionData;
		CurFrontActionData = InActionData;
		CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT;
		FName SlotNodeName = GetSlotNameByIndex(GetBlendBoneNameIndex());
		int32 LoopCount = InActionData.IsLoop ? 99999999 : 1;

		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.MontageDynamicAction[EntityId=%d,  ActionId=%s,  SlotNodeName=%s,  ChacterName=%s"),
				EntityId, *(InActionData.Id.ToString()), *SlotNodeName.ToString(), *(CurCharacter->GetName()));
		}

		CurFrontActionData.CurAnimSquenceBase = PlaySlotAnimationAsDynamicMontage(AnimSequenceBase, SlotNodeName,
			InActionData.BlendInTime, InActionData.BlendOutTime, InActionData.PlayRate, LoopCount, -1.0f, InActionData.PlayStartPosition);
		CheckActionPause(CurFrontActionData);
		CheckChangeBackAction(CurFrontActionData);
		
		//设置添加中断标识，供后面播放结束判断回调数据
		UAnimMontage *AnimMontage = (UAnimMontage*)CurFrontActionData.CurAnimSquenceBase;
		if (AnimMontage)
		{
			UBaseAnimMetaData *AnimMeta = NewObject<UBaseAnimMetaData>();
			AnimMeta->SetInterruptedType(ACTION_INTERRUPTED_ENUM::ACTION_INTERRUPTED_OTHER);
			AnimMontage->EmptyMetaData();
			AnimMontage->AddMetaData(AnimMeta);

			if (IsOpenDebug)
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.MontageDynamicAction[EntityId=%d,  ActionId=%s,  AnimMontage=%s,  ChacterName=%s"),
					EntityId, *(InActionData.Id.ToString()), *AnimMontage->GetName(), *(CurCharacter->GetName()));
			}
		}
		break;
	}
	case ANIM_TYPE_ENUM::ANIM_TYPE_MONTAGE:
	{
		UAnimMontage* AnimMontage = (UAnimMontage *)InActionData.CurAnimSquenceBase;

		//设置添加中断标识，供后面播放结束判断回调数据
		UBaseAnimMetaData *AnimMeta = NewObject<UBaseAnimMetaData>();
		AnimMeta->SetInterruptedType(ACTION_INTERRUPTED_ENUM::ACTION_INTERRUPTED_OTHER);
		AnimMontage->EmptyMetaData();
		AnimMontage->AddMetaData(AnimMeta);

		AnimMontage->BlendIn = InActionData.BlendInTime;
		AnimMontage->BlendOut = InActionData.BlendOutTime;
		AnimMontage->BlendOutTriggerTime = -1.0f;
		//设置片段是否循环
		int32 Index = AnimMontage->GetSectionIndex(InActionData.MontageSectionId);
		FCompositeSection& CompositeSection = AnimMontage->GetAnimCompositeSection(Index);
		CompositeSection.NextSectionName = InActionData.IsLoop ? InActionData.MontageSectionId : "None";
		
		InActionData.CurAnimSquenceBase = AnimMontage;
		//蒙太奇在分层骨骼动画节点中的名字
		//FSlotAnimationTrack &SlotAnimationTrack = AnimMontage->SlotAnimTracks.Last(InActionData.MontageSlotIndex);
		//int32 PlaySlotIndex = FCString::Atoi(*((SlotAnimationTrack.SlotName.ToString()).Right(2)));
		BeforFrontActionData = CurFrontActionData;
		CurFrontActionData = InActionData;

		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.MontageAction[EntityId=%d,  ActionId=%s,  AnimMontage=%s,  ChacterName=%s"),
				EntityId, *(InActionData.Id.ToString()), *(AnimMontage->GetName()), *(CurCharacter->GetName()));
		}

		CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT;
		float time = Montage_Play(AnimMontage, 1.0f, EMontagePlayReturnType::MontageLength, InActionData.PlayStartPosition);
		
		FName MontageSectionId = GetMontageSectionId(InActionData);
		if (!MontageSectionId.IsNone())
		{
			Montage_JumpToSection(MontageSectionId, AnimMontage);
		}
		//AnimInstance->Montage_SetNextSection(ActionData->MontageSectionId, "Section03");
		CheckChangeBackAction(CurFrontActionData);
		break;
	}
	case ANIM_TYPE_ENUM::ANIM_TYPE_COMPOSITE:
	{
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.CompositeAction[EntityId=%d,  ActionId=%s,  ChacterName=%s]"),
				EntityId, *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}

		StartPlayBackAction(InActionData);
		break;
	}
	case ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE:
	{
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.AnimTypeBlendSpace[EntityId=%d,  ActionDataId=%s,  ChacterName=%s]"),
				EntityId, *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}

		CurBackActionData = InActionData;
		CheckChangeFrontAction(InActionData);
		break;
	}
	case ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE_1D:
		break;
	case ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE:
	{
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StarPlayAction.AnimTypeOffsetBlendSpace[EntityId=%d,  ActionDataId=%s,  ChacterName=%s]"),
				EntityId, *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}

		AimOffsetActionData = InActionData;
		//CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT;
		break;
	}
	case ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE_1D:
		break;
	default:
		break;
	}
	OnActionChangeFinish.Broadcast(GetCurPlayActionData()); 
	//要考虑到过渡，故做延时处理
	TWeakObjectPtr<UBaseAnimInstance> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, FilterStateDelayHandle, 
		FTimerDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UBaseAnimInstance* ThisPtr = DelayThisPtr.Get();
			ThisPtr->BeforBackActionData = ThisPtr->CurBackActionData;
		}
	}), 0.2f, false);
}

void UBaseAnimInstance::PlayContinuousActions(FACTION_CONTINUOUS &InContinuousAction,
	const FActionContinuousOverDelegate& InContinuousActionOverDelegate /*= FActionContinuousOverDelegate()*/)
{ 
	SCOPE_CYCLE_COUNTER(STAT_UBaseAnimInstance_PlayContinuousActions);

	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayContinuousActions[EntityId=%d,  InContinuousId=%d,   CurContinuousId=%d,  ChacterName=%s]"),
			EntityId, InContinuousAction.Id, CurContinuousAction.Id, *(CurCharacter->GetName()));
	}

	FName ActionDataId = InContinuousAction.ActionIds[0];
	FACTION_DATA ActionData = FACTION_DATA();
	bool IsBreakFront = false;
	bool bResult = CheckCanPlayNewAction(ActionDataId, ActionData, IsBreakFront);
	if (bResult)
	{
		RemoveConutinuousActionDatas(CurContinuousAction.Id);

		CurContinuousAction = InContinuousAction;
		ContinuousActionOverMap.Add(InContinuousAction.Id, InContinuousActionOverDelegate);
		CheckNextContinuousAction();
	}
}

bool UBaseAnimInstance::CheckCanPlayNewAction(FName InActionId, FACTION_DATA& ActionData, bool& IsBreakFront)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckCanPlayNewAction);
	if (!IsValid(CurCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::CheckCanPlayNewAction : CurCharacter!"));
		return false;
	}

	//检测有强制效果则不播放任何动作
	AServerCharacter* CurServerCharacter = Cast<AServerCharacter>(CurCharacter);
	if (IsValid(CurServerCharacter) && !CurServerCharacter->IsCanPlayAction())
	{
		return false;
	}

	ActionData = GetActionDataById(InActionId);
	//检测动作数据有效性
	bool bValidActionData = CheckActionDataValid(ActionData);
	//检测优先级 
	bool bIsCanPriority = CheckActionPriority(ActionData, IsBreakFront);

	//只要优先级满足，则可以通知播放新动作   
	if (bIsCanPriority)
	{
		OnPlayNewAction.Broadcast(ActionData);
	}
	return bValidActionData && bIsCanPriority;
}

bool UBaseAnimInstance::CheckActionDataValid(FACTION_DATA& InActionData)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckActionDataValid);
	if (InActionData.Id.IsNone())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Resource not found.ActionId=None::[UBAnim::PlayAction (EntityId=%d, ModelId=%s, ActionId=%s,  ChacterName=%s)"),
			EntityId, *(CurCharacter->GetCurModelData()->RowName.ToString()), *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		return false;
	}
	if (!InActionData.AnimPath.ToSoftObjectPath().IsValid())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Resource not found.AnimPath=None::[UBAnim::PlayAction (EntityId=%d, ModelId=%s, ActionId=%s, AnimPath=%s,  ChacterName=%s)]"),
			EntityId, *(CurCharacter->GetCurModelData()->RowName.ToString()), *(InActionData.Id.ToString()), *(InActionData.AnimPath.ToString()), *(CurCharacter->GetName()));
		return false;
	}
	if (!InActionData.AnimPath.Get())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Resource not found.AnimPathObject=Null::[UBAnim::StartPlayAction (EntityId=%d, ModelId=%s, ActionId=%s, AnimPath=%s,  ChacterName=%s)]"),
			EntityId, *(CurCharacter->GetCurModelData()->RowName.ToString()), *(InActionData.Id.ToString()), *(InActionData.AnimPath.ToString()), *(CurCharacter->GetName()));
		return false;
	}
	if (InActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_HIT_FLY_GET_UP && IsDead())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("[UBAnim::PlayAction Fail. Character.state = IsDead. (EntityId=%d, ModelId=%s, ActionId=%s,  ChacterName=%s)"),
			EntityId, *(CurCharacter->GetCurModelData()->RowName.ToString()), *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		return false;
	}
	return true;
}

bool UBaseAnimInstance::CheckActionPriority(FACTION_DATA& InActionData, bool &IsBreakFront)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckActionPriority);
	FACTION_DATA ActionData = GetCurPlayActionData();
	UActionManager *ActionManager = UUECS3GameInstance::Instance->ActionManager;
	ACTION_GROUND_TYPE_ENUM GroundType = ActionData.GroundType;
	ACTION_GROUND_TYPE_ENUM InGroundType = InActionData.GroundType;

	//条件成功：新的背景中断当前前景
	if (CurGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT &&
		InGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK)
	{
		//检测是否要中断当背景
		bool IsBreakCurBack = ActionManager->IsBreakAction(CurBackActionData, InActionData);
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayAndCheckActionPriority[1.2]::[EntityId=%d, IsCompelBreak=%d, IsBreakCurBack=%d, CurBackId=%s,  NewActionId=%s,  CharacterName=%s]"),
				EntityId, (IsCompelBreak ? 1 : 0), (IsBreakCurBack ? 1 : 0), *(CurBackActionData.Id.ToString()), *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}
		
		if (IsCompelBreak || IsBreakCurBack)
		{
			//检测是否要中断当前景
			bool IsBreakCurFront = ActionManager->IsBreakAction(ActionData, InActionData);
			
			if (IsOpenDebug)
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayAndCheckActionPriority[1.1]::[EntityId=%d, IsBreakCurFront=%d, CurActionId=%s,  NewActionId=%s,  CharacterName=%s]"),
					EntityId, (IsBreakCurFront ? 1 : 0), *(ActionData.Id.ToString()), *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
			}
			IsBreakFront = IsBreakCurFront;
			return true;
		}
	}
	else if (CurGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT &&
		InGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
	{
		bool IsBreak = ActionManager->IsBreakAction(CurFrontActionData, InActionData);
		
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayAndCheckActionPriority[2]::[EntityId=%d, IsCompelBreak=%d, IsBreak=%d, CurActionId=%s,  NewActionId=%s,  CharacterName=%s]"),
				EntityId, (IsCompelBreak ? 1 : 0), (IsBreak ? 1 : 0), *(ActionData.Id.ToString()), *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}
		
		if (IsCompelBreak || IsBreak)
		{
			if (CurFrontActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_FRONT_SHOW)
			{
				IsBreakFront = true;
			}
			return true;
		}
	}
	else
	{
		//条件成功：背景中断背景  or 前景中断背景
		bool IsBreak = ActionManager->IsBreakAction(CurBackActionData, InActionData);
		
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayAndCheckActionPriority[3]::[EntityId=%d, IsCompelBreak=%d, IsBreak=%d, CurActionId=%s,  NewActionId=%s,  CharacterName=%s]"),
				EntityId, (IsCompelBreak ? 1 : 0), (IsBreak ? 1 : 0), *(ActionData.Id.ToString()), *(InActionData.Id.ToString()), *(CurCharacter->GetName()));
		}
		if (IsCompelBreak || IsBreak)
		{
			return true;
		}
	}
	return false;
}

void UBaseAnimInstance::MontageStartEvent_Implementation(UAnimMontage* MontageToPlay)
{
}

void UBaseAnimInstance::MontageEndEvent_Implementation(UAnimMontage* MontageToPlay, bool bInterrupted)
{
	SCOPE_CYCLE_COUNTER(STAT_MontageEndEvent_Implementation);
	FString CurFrontName = CurFrontActionData.CurAnimSquenceBase ? *CurFrontActionData.CurAnimSquenceBase->GetName() : FString("null");
	FACTION_DATA ActionData = GetCurPlayActionData();
	//获取中断标识类型
	ACTION_INTERRUPTED_ENUM InterruptedType = ACTION_INTERRUPTED_ENUM::ACTION_INTERRUPTED_OTHER;
	if (MontageToPlay->GetMetaData().Num() > 0)
	{
		UBaseAnimMetaData *AnimMeta = (UBaseAnimMetaData *)MontageToPlay->GetMetaData()[0];
		if (IsValid(AnimMeta))
		{
			InterruptedType = AnimMeta->GetInterruptedType();
		}
	}

	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::MontageEndEvent[1][EntityId=%d,  ActionDataId=%s, CurFrontActionId=%s, CurContinuousId=%d, SetInterruptedType=%d, bInterrupted=%d,  CharacterName=%s]"),
			EntityId, *(ActionData.Id.ToString()), *(CurFrontActionData.Id.ToString()),
			CurFrontActionData.ContinuousId, (int32)InterruptedType, bInterrupted, *(CurCharacter->GetName()));
	}

	//此处说明：
	//bInterrupted为true的情况有二种: Montage_Stop停止、蒙太奇在播放中又被另一个蒙太奇(也可以是自己)顶掉
	//bInterrupted为false情况: 蒙太奇正常播完
	if (!bInterrupted)
	{//正常播完
		CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK;
		if (CurFrontActionData.CurAnimSquenceBase == MontageToPlay)
		{
			CallBackForActionOver(CurFrontActionData);
			if (CurFrontActionData.IsReturnStandy)
			{
				CheckChangeFrontAction(CurBackActionData);
			}
		}
	}
	else if (InterruptedType == ACTION_INTERRUPTED_ENUM::ACTION_INTERRUPTED_STOP)
	{//通过Montage_Stop停止
		if (CurFrontActionData.CurAnimSquenceBase == MontageToPlay)
		{
			CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK;
			CallBackForActionOver(CurFrontActionData);
		}
		else if (BeforFrontActionData.CurAnimSquenceBase == MontageToPlay)
		{
			CallBackForActionOver(BeforFrontActionData);
		}
	}
	else
	{//通过B蒙太奇直接顶掉A蒙太奇，没走Montage_Stop
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::MontageEndEvent[2][EntityId=%d,  ActionDataId=%s, BeforFrontActionId=%s, BeforContinuousId=%d,  CharacterName=%s]"),
				EntityId, *(ActionData.Id.ToString()), *(BeforFrontActionData.Id.ToString()), BeforFrontActionData.ContinuousId, *(CurCharacter->GetName()));
		}

		if (BeforFrontActionData.CurAnimSquenceBase == MontageToPlay)
		{
			CallBackForActionOver(BeforFrontActionData);
		}
	}
	//当前景播放完毕变成待机要通知【因为前景播的时候，其实背景就已换成待机，所以需要前景播完通知一遍】
	OnActionChangeFinish.Broadcast(GetCurPlayActionData());
}

void UBaseAnimInstance::MontageBlendOutEvent_Implementation(UAnimMontage* MontageToPlay, bool bInterrupted)
{
	if (CurFrontActionData.CurAnimSquenceBase == MontageToPlay)
	{
		CallBackForActionBlendOut(CurFrontActionData);
	}
}

void UBaseAnimInstance::PlayOverCurActionCallBack()
{ 
	SCOPE_CYCLE_COUNTER(STAT_PlayOverCurActionCallBack);
	FACTION_DATA ActionData = GetCurPlayActionData();
	if (ActionData.IsLoop)
		return;
	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::PlayOverCurActionCallBack[ EntityId=%d,  id=%s, Return_DynamicId=%d, ActionName=%s, IsPlayMove=%d,  CharacterName=%s]"),
			EntityId, *(ActionData.Id.ToString()), ActionData.DynamicId, *ActionData.ActionName, CurCharacter->IsActiveMoveing() ? 1 : 0, *(CurCharacter->GetName()));
	}
	
	//防止背景过渡完成回调时，这时却正在播放前景动作，造成错误结束动作
	if (ActionData.GroundType != ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK)
		return;

	IsCompelBreak = true;
	if (!IsContinuousPlaying())//因为继续动作检测的下一个动作ID
	{
		if (!ActionData.BindBackGroundId.IsNone())
		{
			PlayAction(ActionData.BindBackGroundId);
		}
		else if (CurCharacter->IsActiveMoveing())
		{
			PlayMoveAction();
		}
		else if (ActionData.IsReturnStandy)
		{
			PlayStandbyAction();
		}
	}
	CallBackForActionOver(ActionData);
}

void UBaseAnimInstance::RefreshData()
{
	///如果当前是背景动作，则表示动作发生了改变，因为下面一行会重新设置新的背景动作；反之，前景动作就暂不考虑
	///注：此函数因涉及切表情况，所以不用能GetActionDataById(ID)取FACTION_DATA，因为可能出现A\B二表中有同样的ID,但是ActionPose不一样,所以ActionPose才是标准
	CurBackActionData = GetActionData(CurBackActionData.ActionPose);
	if (CurGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK)
	{
		///FACTION_DATA TempFrontActionData = GetActionData(CurFrontActionData.ActionPose);
		if (CurBackActionData.Id.IsNone())
		{
			ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_STAND_1;
			CurBackActionData = GetActionData(PoseType);
		}
	}
	CurContinuousAction = FACTION_CONTINUOUS();
	///当前动作发生改变广播通知
	OnActionChangeFinish.Broadcast(CurBackActionData);
}

void UBaseAnimInstance::PlayStandbyAction()
{
	SCOPE_CYCLE_COUNTER(STAT_PlayStandbyAction);
	if (!IsValid(CurCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::PlayStandbyAction : CurCharacter!"));
		return;
	}
	
	///背景动作检测顺序：1、死亡 2、同背景过渡时 3、效果动作  4、战斗警戒待机动作  5、普通待机动作
	if (IsDead())
		return;

	if (CurBackActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_FILTER)
		return;

	bool IsEffectPlaying = PlayEffectStateBackAction();
	if (IsEffectPlaying)
	{
		return;
	}

	AServerCharacter* CurServerCharacter = Cast<AServerCharacter>(CurCharacter);
	if (IsValid(CurServerCharacter))
	{
		bool IsFightState = CurServerCharacter->IsState(ENTITY_STATE::EntityStateFight);///战斗状态
		bool IsWarnState = CurServerCharacter->IsState(ENTITY_STATE::EntityStateWarn);///警戒状态
		bool IsAimOffsetState = false;///瞄准偏移射击状态
		APlayerCharacter *CurPlayCharacter = Cast<APlayerCharacter>(CurCharacter);
		if (IsValid(CurPlayCharacter))
		{
			IsAimOffsetState = CurPlayCharacter->bIsYCJMDAimOffsetState;
		}

		if (IsFightState || IsWarnState || IsAimOffsetState)
		{
			PlayFightStandbyAction();
		}
		else
		{
			PlayNormalStandbyAction();
		}
	}
	else
	{
		PlayNormalStandbyAction();
	}
}

void UBaseAnimInstance::PlayMoveAction()
{
	SCOPE_CYCLE_COUNTER(STAT_PlayMoveAction);
	if (!IsValid(CurCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::PlayMoveAction : CurCharacter!"));
		return;
	}
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	GameObject* pEntity = (GameObject*)(CurCharacter->GetSelfEntity());
	UGameObjectInterface * Interface = CS3PlayerEntity->Interface_Cache.GameObjectInterface;
	if (pEntity && Interface->IsForbidMoveAction())
		return;
	if (CurCharacter->GetMovementComponent()->IsFlying())
		return;

	AServerCharacter *CurServerCharacter = Cast<AServerCharacter>(CurCharacter);
	bool IsInTheWater = IsInWater();
	bool IsFightState = CurServerCharacter ? CurServerCharacter->IsState(ENTITY_STATE::EntityStateFight) : false;
	bool IsWarnState = CurServerCharacter ? CurServerCharacter->IsState(ENTITY_STATE::EntityStateWarn) : false;
	APlayerCharacter *CurPlayCharacter = Cast<APlayerCharacter>(CurCharacter);
	bool IsAimOffsetState = false;///瞄准偏移射击状态
	if (IsValid(CurPlayCharacter))
	{
		IsAimOffsetState = CurPlayCharacter->bIsYCJMDAimOffsetState;
	}
	
	if (IsInTheWater)
	{
		PlayWaterMoveAction();
	}
	else if (IsFightState || IsWarnState || IsAimOffsetState)
	{
		PlayFightMoveAction();
	}
	else
	{
		PlayNormalMoveAction();
	}
}

void UBaseAnimInstance::PlayDeadAction(const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/)
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_DEATH_61;
	PlayPoseBackAction(PoseType, InActionOverDelegate);
}

void UBaseAnimInstance::PlayRebornAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_REBORN_131;
	PlayPoseFrontAction(PoseType);
}

void UBaseAnimInstance::PlayDizzyAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_DIZZY_11;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::PlaySleepAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_SLEEP_12;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::PlayFallLandAction()
{
	ACTION_POSE_ENUM PoseType = CurCharacter->IsActiveMoveing() ?
		ACTION_POSE_ENUM::ACTION_POSE_JUMP_END_47 : ACTION_POSE_ENUM::ACTION_POSE_JUMP_END_46;
	PlayPoseFrontAction(PoseType);
}

void UBaseAnimInstance::PlayFallingAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_JUMP_AIR_51;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::PlayRandomAction(FName ActionId)
{
	FACTION_DATA ActionData = GetCurPlayActionData();
	FACTION_DATA NewActionData = GetActionDataById(ActionId);
	if (NewActionData.Id.IsNone() || ActionData.Id == NewActionData.Id)
		return;
	PlayAction(NewActionData.Id);
}

void UBaseAnimInstance::UpdateMoveSpeed()
{
	CurMoveSpeed = CurCharacter->GetMoveSpeed();
}

void UBaseAnimInstance::UpdateMoveDirection()
{
	CurMoveDirection = 0.0f;
}

FName UBaseAnimInstance::GetMontageSectionId(FACTION_DATA& InActionData)
{
	return InActionData.MontageSectionId;
}

void UBaseAnimInstance::PlayPoseBackAction(ACTION_POSE_ENUM ActionPoseType, 
	const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/)
{
	if (!IsValid(CurCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::PlayPoseBackAction : CurCharacter!"));
		return;
	}
	FACTION_DATA NewActionData = GetActionData(ActionPoseType);
	if (NewActionData.Id.IsNone() || CurBackActionData.Id == NewActionData.Id)
		return;
	PlayAction(NewActionData.Id, 0.0f, InActionOverDelegate);
}

void UBaseAnimInstance::PlayPoseFrontAction(ACTION_POSE_ENUM ActionPoseType, 
	const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/)
{
	if (!IsValid(CurCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::PlayPoseFrontAction : CurCharacter!"));
		return;
	}
	FACTION_DATA NewActionData = GetActionData(ActionPoseType);
	FACTION_DATA ActionData = GetCurPlayActionData();
	if (NewActionData.Id.IsNone() || ActionData.Id == NewActionData.Id)
		return;
	PlayAction(NewActionData.Id, 0.0f, InActionOverDelegate);
}

void UBaseAnimInstance::StopAction()
{
	FACTION_DATA ActionData = GetCurPlayActionData();
	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StopAction[EntityId=%d,  ActionId=%s,  CharacterName=%s"),
			EntityId, *(ActionData.Id.ToString()), *(CurCharacter->GetName()));
	}
	RemoveConutinuousActionDatas(CurContinuousAction.Id);
	StopFrontAction();
	StopBackAction();
}

void UBaseAnimInstance::StopBackAction()
{
	FACTION_DATA ActionData = GetCurPlayActionData();
	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StopBackAction[EntityId=%d,  ActionId=%s,  CharacterName=%s"),
			EntityId, *(ActionData.Id.ToString()), *(CurCharacter->GetName()));
	}
	IsCompelBreak = true;
	PlayStandbyAction();
}

void UBaseAnimInstance::StopFrontAction()
{
	SCOPE_CYCLE_COUNTER(STAT_StopFrontAction);
	//瞄准偏移的前景动作类型特殊停止方式
	if (CurFrontActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE ||
		CurFrontActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE_1D)
	{
		CurFrontActionData = FACTION_DATA();
		CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK;
		return;
	}

	if (CurActionPauseData.IsOpen)
	{
		ClearPauseAction();
	}

	UAnimMontage* AnimMontage = Cast<UAnimMontage>(CurFrontActionData.CurAnimSquenceBase);
	//当PlayAction()时，同时IsBreakFront又为true时，中断时需检查前景动作是否是当前连续动作
	if (CurFrontActionData.ContinuousId == CurContinuousAction.Id)
	{
		RemoveConutinuousActionDatas(CurContinuousAction.Id);
	}
	if (IsValid(AnimMontage))
	{
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StopFrontAction[EntityId=%d,  ActionId=%s,  CurContinuousId=%d, CharacterName=%s"),
				EntityId, *(CurFrontActionData.Id.ToString()), CurFrontActionData.ContinuousId, *(CurCharacter->GetName()));
		}

		if (AnimMontage->GetMetaData().Num() > 0)
		{
			UBaseAnimMetaData *AnimMeta = (UBaseAnimMetaData *)AnimMontage->GetMetaData()[0];
			AnimMeta->SetInterruptedType(ACTION_INTERRUPTED_ENUM::ACTION_INTERRUPTED_STOP);
		}
		Montage_Stop(0.0f, AnimMontage);
		CurGroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK;
	}
}

void UBaseAnimInstance::StopActionById(FName InActionId)
{
	FACTION_DATA ActionData = GetActionDataById(InActionId);
	ACTION_GROUND_TYPE_ENUM InGroundType = ActionData.GroundType;
	
	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StopFrontAction[EntityId=%d,  NewActionId=%s, CharacterName=%s"),
			EntityId, *(InActionId.ToString()), *(CurCharacter->GetName()));
	}

	if (InGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
	{
		if (CurFrontActionData.Id.IsEqual(ActionData.Id))
		{
			StopFrontAction();
		}
		//如果是绑定了背景动作的前景动作，也要相应停止背景动作（如：击退表现）
		if (CurFrontActionData.BindBackGroundId.IsEqual(CurBackActionData.Id))
		{
			StopBackAction();
		}
	}
	else if (InGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK)
	{
		if (CurBackActionData.Id.IsEqual(ActionData.Id))
		{
			StopBackAction();
		}
	}
}

void UBaseAnimInstance::StopActionByType(ACTION_TYPE_ENUM InActionType)
{
	FACTION_DATA ActionData;
	if (InActionType == CurBackActionData.ActionType)
		ActionData = CurBackActionData;
	else if (InActionType == CurFrontActionData.ActionType)
		ActionData = CurFrontActionData;

	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StopActionByType[EntityId=%d,  InActionType=%d, NewActionId=%s, CharacterName=%s"),
			EntityId, (int32)InActionType, *(ActionData.Id.ToString()), *(CurCharacter->GetName()));
	}
	
	if (InActionType != ActionData.ActionType)
		return;

	ACTION_GROUND_TYPE_ENUM GroundType = ActionData.GroundType;
	if (GroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
	{
		StopFrontAction();
	}
	else if (GroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK)
	{
		StopBackAction();
	}
}

void UBaseAnimInstance::StopContinuousAction(int32 InContinuousId /*= 0*/)
{
	FACTION_DATA ActionData = GetCurPlayActionData();

	if (IsOpenDebug)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::StopContinuousAction[EntityId=%d,  InContinuousId=%d,  CurContinuousId=%d,  ActionDataContinuousId=%d, CharacterName=%s"),
			EntityId, InContinuousId, CurContinuousAction.Id, ActionData.ContinuousId, *(CurCharacter->GetName()));
	}

	//如果没有找到要停止的对应的连续动作ID，则return,表示发错;如果发的是默认值0，表示强制停止连续动作
	if (InContinuousId != 0 && !ContinuousActionOverMap.Contains(InContinuousId))
	{
		return;
	}

	//有可能连续动作没播放成功，那么当前显示的前后景动作则不是正在播放的连续动作CurContinuousAction
	if (ActionData.ContinuousId == InContinuousId)
	{
		ACTION_GROUND_TYPE_ENUM GroundType = ActionData.GroundType;
		if (GroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
		{
			StopFrontAction();
		}
		else if (GroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK)
		{
			StopBackAction();
		}
	}
	RemoveConutinuousActionDatas(InContinuousId);
}

void UBaseAnimInstance::BroadcastActionReadyChange(FACTION_DATA& InActionData)
{
	FACTION_DATA ActionData = GetCurPlayActionData();
	ACTION_GROUND_TYPE_ENUM GroundType = ActionData.GroundType;
	ACTION_GROUND_TYPE_ENUM InGroundType = InActionData.GroundType;
	//判断条件：根据背景覆盖不了前景的引擎机制[CST-4781]
	if (GroundType == InGroundType || InGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
	{
		OnActionReadyChange.Broadcast(ActionData);
	}
}

void UBaseAnimInstance::CheckActionPause(FACTION_DATA &InActionData)
{ 
	//处理动作暂停在最后一帧的动作表现及回调
	if (!InActionData.IsReturnStandy && !InActionData.IsLoop &&
		InActionData.BindBackGroundId.IsNone() && InActionData.CurAnimSquenceBase)
	{
		float PlayLength = InActionData.CurAnimSquenceBase->GetPlayLength() - 0.05f;
		CurActionPauseData.IsOpen = true;
		CurActionPauseData.ActionData = InActionData;
		CurActionPauseData.TotalSecondsTime = PlayLength;
		CurActionPauseData.CurSecondsTime = 0;
	}
}

void UBaseAnimInstance::CheckChangeBackAction(FACTION_DATA &InActionData)
{ 
	//播放绑定的背景状态机序列动作
	FACTION_DATA BindActionData;
	if (!InActionData.BindBackGroundId.IsNone())
	{
		BindActionData = GetActionDataById(InActionData.BindBackGroundId);
		BindActionData.DynamicId = ActionDynamicId++;
		CurBackActionData = BindActionData;
	}
	else
	{
		if (CurBackActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_MOVE)
		{
			IsCompelBreak = true;
			PlayMoveAction();
			IsCompelBreak = false;
		}
		else
		{
			///如果是需要与背景融合时，就不要切换背景动作了
			int32 BlendIndex = GetBlendBoneNameIndex();
			if (BlendIndex == 0)
			{
				IsCompelBreak = true;
				PlayStandbyAction();
				IsCompelBreak = false;
			}
		}
	}
}

void UBaseAnimInstance::CheckChangeFrontAction(FACTION_DATA &InActionData)
{
	if (InActionData.BindFrontGroundId.IsNone())
	{
		//停止的当前前景动作必须 = 缓存的绑定的前景动作
		if (!SaveCurFrontActionData.Id.IsNone() && (SaveCurFrontActionData.Id.IsEqual(CurFrontActionData.Id)))
		{
			SaveCurFrontActionData = FACTION_DATA();
			StopFrontAction();
		}
	}
	else
	{
		//停止的当前前景动作必须 = 缓存的绑定的前景动作
		if (!SaveCurFrontActionData.Id.IsNone() && (SaveCurFrontActionData.Id.IsEqual(CurFrontActionData.Id)))
		{
			StopFrontAction();
		}
		//解除：目前只应用于移动类型的动作(CST-7853)
		SaveCurFrontActionData = GetActionDataById(InActionData.BindFrontGroundId);
		PlayAction(InActionData.BindFrontGroundId);
	}
}

void UBaseAnimInstance::UpdateActionPauseTime(float DeltaSeconds)
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateActionPauseTime);
	if (CurActionPauseData.IsOpen)
	{
		CurActionPauseData.CurSecondsTime += DeltaSeconds;

		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseAnimInstance::UpdateActionPauseTime[EntityId=%d, ActionId=%s, TotalSecondsTime=%f, CurSecondsTime=%f, DeltaSeconds=%f]"),
				EntityId, *CurActionPauseData.ActionData.Id.ToString(), CurActionPauseData.TotalSecondsTime,
				CurActionPauseData.CurSecondsTime, DeltaSeconds);
		}
		
		if (CurActionPauseData.CurSecondsTime >= CurActionPauseData.TotalSecondsTime)
		{
			if (IsOpenDebug)
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseAnimInstance::UpdateActionPauseTime[EntityId=%d, ActionId=%s, OVER!! ]"),
					EntityId, *CurActionPauseData.ActionData.Id.ToString());
			}

			if (IsValid(this) && Cast<UBaseAnimInstance>(this))
			{
				CurActionPauseData.IsOpen = false;
				//如果是蒙太奇,需手动调一次暂停;背景动作不需要
				FACTION_DATA PauseActionData = CurActionPauseData.ActionData;
				if (UAnimMontage *AnimMontage = Cast<UAnimMontage>(PauseActionData.CurAnimSquenceBase))
				{
					//暂停蒙太奇计时可能有时间误差，所以直接再从动画最后一帧播放一次，立刻又暂停
					float MontagePlayRate = CurActionPauseData.ActionData.PlayRate;
					float MontageTotalSecondsTime = CurActionPauseData.TotalSecondsTime + 0.05f;
					Montage_Play(AnimMontage, MontagePlayRate, EMontagePlayReturnType::MontageLength, MontageTotalSecondsTime);
					Montage_Pause(AnimMontage);
				}

				FACTION_DATA ActionData = GetCurPlayActionData();
				if (ActionData.CurAnimSquenceBase == PauseActionData.CurAnimSquenceBase)
				{
					CallBackForActionOver(ActionData);
				}
			}
		}
	}
}

void UBaseAnimInstance::ClearPauseAction()
{
	CurActionPauseData.IsOpen = false;
	CurActionPauseData.ActionData = FACTION_DATA();
	CurActionPauseData.TotalSecondsTime = 0.0f;
	CurActionPauseData.CurSecondsTime = 0;
}

void UBaseAnimInstance::StartPlayBackAction(FACTION_DATA &InActionData)
{
	//非IsLoop：只针对不循环的动作(dead)，循环的动作没必要刷新
	if (CurGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK && 
		!CurBackActionData.IsLoop && 
		CurBackActionData.Id == InActionData.Id)
	{
		//这里逻辑是处理同背景动作再次播放问题，需要过渡到一个其他状态才能播放再次播放同背景
		FACTION_DATA FilterActionData = GetActionData(ACTION_POSE_ENUM::ACTION_POSE_FILTER_255);
		if (!FilterActionData.Id.IsNone())
		{
			SaveCurBackActionData = CurBackActionData;
			CurBackActionData = FilterActionData;

			TWeakObjectPtr<UBaseAnimInstance> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, FilterSaveStateDelayHandle,
				FTimerDelegate::CreateLambda([DelayThisPtr, FilterActionData]()
			{
				if (DelayThisPtr.IsValid())
				{
					UBaseAnimInstance* ThisPtr = DelayThisPtr.Get();
					if (ThisPtr->CurBackActionData.Id == FilterActionData.Id)
					{
						ThisPtr->CurBackActionData = ThisPtr->SaveCurBackActionData;
						ThisPtr->CheckActionPause(ThisPtr->CurBackActionData);//背景动作也要判断，不然一遍播完会没有回调通知
						ThisPtr->CheckChangeFrontAction(ThisPtr->CurBackActionData);
					}
				}
			}), 0.1f, false);
		}
	}
	else
	{
		CurBackActionData = InActionData;
		CheckActionPause(CurBackActionData);//背景动作也要判断，不然一遍播完会没有回调通知
		CheckChangeFrontAction(CurBackActionData);
	}
}

void UBaseAnimInstance::CheckNextContinuousAction()
{
	FName Id = CurContinuousAction.ActionIds[0];
	float StartTime = CurContinuousAction.ActionStartTimes[0];
	FActionOverDelegate Delegate;
	Delegate.AddUObject(this, &UBaseAnimInstance::OnActionOverForContinuous);
	PlayAction(Id, StartTime, Delegate, CurContinuousAction.Id);
}

void UBaseAnimInstance::RemoveConutinuousActionDatas(int32 InContinuousId)
{
	int32 SaveContinuousActionId = InContinuousId;
	if (InContinuousId == CurContinuousAction.Id)
	{
		CurContinuousAction.Id = 0;
		CurContinuousAction.ActionIds.Empty();
		CurContinuousAction.ActionStartTimes.Empty();
	}

	if (ContinuousActionOverMap.Contains(SaveContinuousActionId))
	{
		if (IsOpenDebug)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::RemoveConutinuousActionDatas[EntityId=%d,  RemoveContinuousId=%d,  FindContinuousId=%d]"),
				EntityId, SaveContinuousActionId, InContinuousId);
		}
		
		FActionContinuousOverDelegate* ContinuousActionOverDelegate = ContinuousActionOverMap.Find(SaveContinuousActionId);
		if (ContinuousActionOverDelegate->IsBound())
		{
			ContinuousActionOverDelegate->Broadcast(CurCharacter, SaveContinuousActionId);
			//ContinuousActionOverDelegate->Clear();
		}
		ContinuousActionOverMap.Remove(SaveContinuousActionId);
	}
}

void UBaseAnimInstance::OnActionOverForContinuous(ACharacter* Character, FACTION_DATA InActionData)
{
	//当一个新的连续前景动作播放时，若当前正在播放前景动作，会触发中断当前前景，并进入MontageEndEvent，
	//再回调到这里，如果删除了当前的新的连续动作，则删除不正确
	if (CurContinuousAction.Id != InActionData.ContinuousId)
	{
		return;
	}
	if (CurContinuousAction.ActionIds.Num() > 0)
	{
		CurContinuousAction.ActionIds.RemoveAt(0);
		CurContinuousAction.ActionStartTimes.RemoveAt(0);
		if (CurContinuousAction.ActionIds.Num() <= 0)
		{
			RemoveConutinuousActionDatas(CurContinuousAction.Id);
		}
		else
		{
			CheckNextContinuousAction();
		}
	}
}

bool UBaseAnimInstance::IsContinuousPlaying()
{
	return CurContinuousAction.Id != 0;
}

FName UBaseAnimInstance::GetSlotNameByIndex(int32 Index)
{
	FName SlotNodeName = "";
	switch (Index)
	{
	case 0:
		SlotNodeName = "SlotRoot01";
		break;
	case 1:
		SlotNodeName = "SlotBody01";
		break;
	case 2:
		SlotNodeName = "SlotFace01";
		break;
	default:
		break;
	}
	return SlotNodeName;
}

void UBaseAnimInstance::PlayInitStandByAction(FName ActionId)
{
	FACTION_DATA ActionData = GetActionDataById(ActionId);
	if (ActionData.Id.IsNone())
		return;
	PlayAction(ActionData.Id);
}

void UBaseAnimInstance::PlayNormalStandbyAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_STAND_1;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::PlayFightStandbyAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_STAND_2;
	PlayPoseBackAction(PoseType);
}

bool UBaseAnimInstance::PlayEffectStateBackAction()
{
	AServerCharacter *CurServerCharacter = Cast<AServerCharacter>(CurCharacter);
	if (IsValid(CurServerCharacter))
	{
		UStateInterface* StateInterface = CurServerCharacter->GetEntityInterface_Cache().StateInterface;

		EFFECT_STATE EffectState = EFFECT_STATE::EFFECT_STATE_NULL;
		if (StateInterface)
		{
			StateInterface->GetCurEffectState(EffectState);
		}

		if (EffectState == EFFECT_STATE::EFFECT_STATE_DIZZY)
		{
			PlayDizzyAction();
			return true;
		}
		else if (EffectState == EFFECT_STATE::EFFECT_STATE_SLEEP)
		{
			PlaySleepAction();
			return true;
		}
		else
		{
			//不处理
			return false;
		}
	}
	return false;
}

void UBaseAnimInstance::PlayNormalMoveAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_MOVE_21;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::PlayFightMoveAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_MOVE_22;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::PlayWaterMoveAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_MOVE_23;
	PlayPoseBackAction(PoseType);
}

void UBaseAnimInstance::CallBackForActionOver(FACTION_DATA InActionData)
{
	if (ActionOverDelegateMap.Contains(InActionData.DynamicId))
	{
		FActionOverDelegate* ActionOverDelegate = ActionOverDelegateMap.Find(InActionData.DynamicId);
		if (ActionOverDelegate->IsBound())
		{
			ActionOverDelegate->Broadcast(CurCharacter, InActionData);
			//ActionOverDelegate->Clear();
		}
		ActionOverDelegateMap.Remove(InActionData.DynamicId);
	}
}

void UBaseAnimInstance::CallBackForActionBlendOut(FACTION_DATA InActionData)
{
	if (ActionBlendOutDelegateMap.Contains(InActionData.DynamicId))
	{
		FActionBlendOutDelegate* ActionBlendOutDelegate = ActionBlendOutDelegateMap.Find(InActionData.DynamicId);
		if (ActionBlendOutDelegate->IsBound())
		{
			ActionBlendOutDelegate->Broadcast(CurCharacter, InActionData);
			//ActionOverDelegate->Clear();
		}
		ActionBlendOutDelegateMap.Remove(InActionData.DynamicId);
	}
}

/*
void UBaseAnimInstance::SetAssetRootMotion(FACTION_DATA& InActionData)
{
	UAnimSequence* AnimSequence = Cast<UAnimSequence>(InActionData.CurAnimSquenceBase);
	if (InActionData.IsResetDisplaceType && AnimSequence)
	{
		if (InActionData.ResetDisplaceType == ACTION_DISPLACE_TYPE::ACTION_DISPLACE_TYPE_REALLY)
		{
			AnimSequence->bEnableRootMotion = true;
			AnimSequence->bForceRootLock = false;
		}
		else if (InActionData.ResetDisplaceType == ACTION_DISPLACE_TYPE::ACTION_DISPLACE_TYPE_FALSE)
		{
			AnimSequence->bEnableRootMotion = false;
			AnimSequence->bForceRootLock = false;
		}
		else
		{
			AnimSequence->bEnableRootMotion = false;
			AnimSequence->bForceRootLock = true;
		}
	}
}*/

FACTION_DATA UBaseAnimInstance::GetCurPlayActionData()
{
	return CurGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK ? CurBackActionData : CurFrontActionData;
}

FACTION_CONTINUOUS UBaseAnimInstance::GetCurPlayContinuousActionData()
{
	return CurContinuousAction;
}

void UBaseAnimInstance::GetFronAndBackAction(FString& BackActionId, FString& FrontActionId)
{
	if (CurGroundType == ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT)
	{
		FrontActionId = FNAME_TO_FSTRING(CurFrontActionData.Id);
	}
	BackActionId = FNAME_TO_FSTRING(CurBackActionData.Id);
}

FACTION_DATA UBaseAnimInstance::GetActionData(ACTION_POSE_ENUM InActionPose)
{
	if (IsValid(CurCharacter))
	{
		return CurCharacter->ActionDatas.FindRef(InActionPose);
	}
	return FACTION_DATA();
}

FACTION_DATA UBaseAnimInstance::GetActionDataById(FName ActionId)
{
	FACTION_DATA FindActionData = FACTION_DATA();
	for (auto& Kvp : CurCharacter->ActionDatas)
	{
		FACTION_DATA ActionData = Kvp.Value;
		if (ActionData.Id == ActionId)
		{
			FindActionData = ActionData;
			break;
		}
	}
	return FindActionData;
}

int32 UBaseAnimInstance::GetBlendBoneNameIndex()
{
	if (!IsValid(CurCharacter))
	{
		return 0;
	}

	FACTION_DATA ActionData = GetCurPlayActionData();
	if (ActionData.Id.IsNone())
	{
		return 0;
	}

	/*FVector CharacterVelocity = CurCharacter->GetVelocity();
	float VelocitySpeed = CharacterVelocity.Size2D();*/
	//bool IsMoving = CurCharacter->IsActiveMoveing();
	if (!ActionData.IsFaceHalfBlend && !ActionData.IsBodyHalfBlend)
	{
		return 0;
	}
	else if (ActionData.IsFaceHalfBlend)
	{
		return 2;
	}
	else if (ActionData.IsBodyHalfBlend && CurCharacter->IsActiveMoveing())
	{
		return 1;
	}
	else
	{
		return 0;
	}
	return 0;
}

bool UBaseAnimInstance::IsDead()
{
	AServerCharacter *ServerCharacter = Cast<AServerCharacter>(CurCharacter);
	if (!IsValid(ServerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseAnimInstance::IsDead : CurCharacter!"));
		return false;
	}
	return ServerCharacter->bDeadState;
}

bool UBaseAnimInstance::IsStandByState()
{
	FACTION_DATA ActionData = GetCurPlayActionData();
	return (ActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_STANDBY && ActionData.ActionPose != ACTION_POSE_ENUM::ACTION_POSE_STAND_2);
}

CONTROL_COMPILE_OPTIMIZE_END
