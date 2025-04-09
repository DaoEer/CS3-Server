
#include "RoleAnimInstance.h"
//CS3
#include "GameFramework/PawnMovementComponent.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Component/Role/JumpComponent.h"

CONTROL_COMPILE_OPTIMIZE_START
URoleAnimInstance::URoleAnimInstance():IsInJumpAir(false), IsOnLandingFromJumpAir(false)
{
	bTickUpdate = true;
}

URoleAnimInstance::~URoleAnimInstance()
{
}

void URoleAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(CurCharacter);
	if (!IsValid(PlayerCharacter))
	{
		return;
	}

	//瞄准偏移射击模式
	if (PlayerCharacter->bIsYCJMDCopy)
	{
		FACTION_DATA ActionData = GetCurPlayActionData();
		if (!ActionData.BindAimOffsetId.IsNone())
		{
			FACTION_DATA TemActionData = GetActionDataById(ActionData.BindAimOffsetId);
			StarPlayAction(TemActionData);
			UpdateAimOffsetDirction();
			IsAimOffsetBlend = true;
		}
		else
		{
			IsAimOffsetBlend = false;
			AimOffsetActionData = FACTION_DATA();
		}
	}
	else
	{
		IsAimOffsetBlend = false;
		AimOffsetActionData = FACTION_DATA();
	}
}

bool URoleAnimInstance::IsInWater()
{ 
	KBEngine::Entity* pEntity = CurCharacter->GetSelfEntity();
	if (pEntity)
	{
		return UGolbalBPFunctionLibrary::GetIntPropertyValue(pEntity->ID(), TEXT("onWaterArea")) == 1 ? true : false;
	}
	return false;
}

void URoleAnimInstance::UpdateMoveDirection()
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(CurCharacter);
	if (IsValid(PlayerCharacter))
	{
		CurMoveDirection = PlayerCharacter->GetMoveDirection();
	}
}

FName URoleAnimInstance::GetMontageSectionId(FACTION_DATA& InActionData)
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(CurCharacter);
	if (IsValid(PlayerCharacter) && PlayerCharacter->bIsYCJMDCopy)
	{
		if (!PlayerCharacter->IsActiveMoveing())
		{
			return InActionData.MontageSectionId;
		}

		if (CurMoveDirection > -45.0f && CurMoveDirection < 45.0f)
		{
			return "Front";
		}
		else if (CurMoveDirection < -45.0f && CurMoveDirection > -135.0f)
		{
			return "Left";
		}
		else if (CurMoveDirection > 45.0f && CurMoveDirection < 135.0f)
		{
			return "Right";
		}
		else
		{
			return "Back";
		}
	}
	return InActionData.MontageSectionId;
}

void URoleAnimInstance::UpdateAimOffsetDirction()
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(CurCharacter);
	if (IsValid(PlayerCharacter))
	{
		CurAimOffsetYaw = PlayerCharacter->CurAimOffsetYaw;
		CurAimOffsetPitch = PlayerCharacter->CurAimOffsetPitch;
	}
}

void URoleAnimInstance::PlayShouDaoAction(const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/)
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_SHIFT_16;
	PlayPoseFrontAction(PoseType, InActionOverDelegate);
}

void URoleAnimInstance::PlayBaDaoAction(const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/)
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_SHIFT_17;
	PlayPoseFrontAction(PoseType, InActionOverDelegate);
}

void URoleAnimInstance::PlayClimbLadderAction()
{
	ACTION_POSE_ENUM PoseType = ACTION_POSE_ENUM::ACTION_POSE_CLIMB_LADDER_15;
	PlayPoseBackAction(PoseType);
}

CONTROL_COMPILE_OPTIMIZE_END
