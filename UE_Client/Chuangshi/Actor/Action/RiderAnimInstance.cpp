// Fill out your copyright notice in the Description page of Project Settings.

#include "RiderAnimInstance.h"

#include "Util/CS3Debug.h"


CONTROL_COMPILE_OPTIMIZE_START

URiderAnimInstance::URiderAnimInstance()
{
	bTickUpdate = false;
}

URiderAnimInstance::~URiderAnimInstance()
{ 
}

void URiderAnimInstance::PlayAction(FName InActionId, 
	float InStartPostion /*= 0.0f*/, 
	const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/, 
	int32 InContinuousId /*= 0*/, 
	const FActionBlendOutDelegate& InActionBlendOutDelegate /*= FActionBlendOutDelegate()*/)
{
	if (!CurCharacter)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URiderAnimInstance::PlayAction : CurCharacter!"));
		return;
	}
	FACTION_DATA ActionData = GetActionDataById(InActionId);
	bool bValidActionAsset = CheckActionDataValid(ActionData);
	if (!bValidActionAsset)
		return;

	ActionData.PlayStartPosition = InStartPostion > 0.0f ? InStartPostion : ActionData.PlayStartPosition;
	ActionData.DynamicId = ActionDynamicId++;
	ActionOverDelegateMap.Add(ActionData.DynamicId, InActionOverDelegate);
	StarPlayAction(ActionData);
}

void URiderAnimInstance::SetMoveSpeedAndMoveDirection(float InMoveSpeed, float InMoveDirection)
{
	CurMoveSpeed = InMoveSpeed;
	CurMoveDirection = InMoveDirection;
}

CONTROL_COMPILE_OPTIMIZE_END


