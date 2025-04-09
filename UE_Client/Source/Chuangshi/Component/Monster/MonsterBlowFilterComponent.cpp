// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterBlowFilterComponent.h"
#include "Manager/TimeManager.h"
#include "Util/CS3Debug.h"
#include "Actor/ServerCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START

void UMonsterBlowFilterComponent::InitData(const FVector & BlowDir_, const float& Speed)
{
	BlowDir = BlowDir_;
	BlowSpeed = Speed * 100;
}

void UMonsterBlowFilterComponent::OnUpdateVolatileData(const FVector & position, const FVector & direction, int32 parentID)
{
	if (CanUpdatePos(position))
	{
		BUndatePos = true;
		Supper::OnUpdateVolatileData(position, direction, parentID);
	}
	else
	{
		BUndatePos = false;
		Supper::OnUpdateVolatileData(GetOwner()->GetActorLocation(), direction, parentID);

// 		AServerCharacter* Owner = Cast<AServerCharacter>(GetOwner());
// 		if (IsValid(Owner))
// 		{
// 			Owner->SetActorLocation(Owner->OnGroundPos(position));
// 		}
	}
	
}

void UMonsterBlowFilterComponent::SetPosition(const FVector & position, int32 parentID)
{
	// 服务器通过设置position，作吹风位置变化！客户端模拟
	FVector newPos;
	FVector newDir;
	if (GetPositionAndDirection(position, FVector::ZeroVector, parentID, newPos, newDir))
	{
		BlowPosArr.Add(newPos);
	}
}

void UMonsterBlowFilterComponent::Pos(const int32 vehicleID, const FVector& position, const FVector& direction, const FVector& velocity)
{
	if (BUndatePos)
	{
		Supper::Pos(vehicleID, position, direction, velocity);
	}
}

void UMonsterBlowFilterComponent::SimulateMovement(float DeltaTime)
{
	Supper::SimulateMovement(DeltaTime);

	AServerCharacter* Owner = Cast<AServerCharacter>(GetOwner());
	if (IsValid(Owner))
	{
		FVector Location = BlowSpeed * DeltaTime * BlowDir + Owner->GetActorLocation();
		Owner->SetActorLocation(Owner->FloorTrace(Location));
	}
}

void UMonsterBlowFilterComponent::EndBlow()
{

// 	if (IsValid(UGolbalBPFunctionLibrary::ForceManager()))
// 	{
// 		UGolbalBPFunctionLibrary::ForceManager()->PauseForce(ForceID);
// 	}
}

bool UMonsterBlowFilterComponent::CanUpdatePos(const FVector & NewPos)
{
	for (auto Vpos = BlowPosArr.CreateConstIterator(); Vpos; Vpos++)
	{
		if (FVector::Dist2D(NewPos, BlowPosArr[Vpos.GetIndex()]) <= 20)
		{
			BlowPosArr.RemoveAt(Vpos.GetIndex());
			return false;
				
		}
	}
	return true;
}
CONTROL_COMPILE_OPTIMIZE_END