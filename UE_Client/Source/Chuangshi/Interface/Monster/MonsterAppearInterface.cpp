// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterAppearInterface.h"

#include "RotationMatrix.h"
#include "Kismet/KismetMathLibrary.h"

#include "CS3Base/CS3Entity.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Component/AvatarFilterActorComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterAppearInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterAppearInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UMonsterAppearInterface::CLIENT_MonsterAppearJump_Implementation(
	const TArray<FName>& Actions, const FString& EffectID, const float& Gravity,
	const float& UpTime, const float& XSpeed, const FVector& TargetPos)
{
	MonsterAppearJump_Implementation(Actions, EffectID, Gravity, UpTime, XSpeed, TargetPos);
}

void UMonsterAppearInterface::MonsterAppearJump_Implementation(
	const TArray<FName>& Actions, const FString& EffectID, const float& Gravity, 
	const float& UpTime, const float& XSpeed, const FVector& TargetPos)
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor) || !IsValid(MonsterActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterAppearInterface::CLIENT_MonsterAppearJump_Implementation : MonsterActor!"));
		return;
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("[MonsterJump]UMonsterAppearInterface::CLIENT[EntityId(%d), ActionsNum(%d), IsChangeAppearanceling(%d), jumpTopos(%s), jumpDatas: gravity(%f), upTime(%f), xSpeed(%f)!"),
		EntityID, Actions.Num(), MonsterActor->bIsChangeAppearanceling ? 1 : 0 , *TargetPos.ToString(), Gravity, UpTime, XSpeed);

	if (MonsterActor->bIsChangeAppearanceling)
	{
		TWeakObjectPtr<UMonsterAppearInterface> DelayThisPtr(this);
		TWeakObjectPtr<AMonsterCharacter> DelayMonsterCharacterPtr(MonsterActor);
		if (MonsterAppearJumpHandle.IsValid())
		{
			MonsterActor->OnModelChangeAppearanceOverDelegate.Remove(MonsterAppearJumpHandle);
			MonsterAppearJumpHandle.Reset();
		}
		MonsterAppearJumpHandle = MonsterActor->OnModelChangeAppearanceOverDelegate.AddLambda([
			DelayThisPtr, DelayMonsterCharacterPtr, Actions, EffectID, Gravity, UpTime, XSpeed, TargetPos]()
		{
			if (DelayThisPtr.IsValid() && DelayMonsterCharacterPtr.IsValid())
			{
				UMonsterAppearInterface* ThisPtr = DelayThisPtr.Get();
				AMonsterCharacter* MonsterActor = DelayMonsterCharacterPtr.Get();

				MonsterActor->MonsterCharacterJumpStart(Actions, EffectID);
				MonsterActor->ChangeCurveFilter(Gravity, UpTime, XSpeed, MonsterActor->FloorTrace(TargetPos, true));
				MonsterActor->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->MonsterAppearJumpHandle);
			}
		});
	}
	else
	{
		MonsterActor->MonsterCharacterJumpStart(Actions, EffectID);
		MonsterActor->ChangeCurveFilter(Gravity, UpTime, XSpeed, MonsterActor->FloorTrace(TargetPos, true));
	}
}

void UMonsterAppearInterface::CLIENT_MonsterAppearJumpWithoutMove_Implementation(
	const TArray<FName>& Actions, const FString& EffectID, float LoopTime)
{
	MonsterAppearJumpWithoutMove_Implementation(Actions, EffectID, LoopTime);
}


void UMonsterAppearInterface::MonsterAppearJumpWithoutMove_Implementation(
	const TArray<FName>& Actions, const FString& EffectID, float LoopTime)
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterAppearInterface::CLIENT_MonsterAppearJumpWithoutMove_Implementation : MonsterActor!"));
		return;
	}
	if (MonsterActor->bIsChangeAppearanceling)
	{
		TWeakObjectPtr<UMonsterAppearInterface> DelayThisPtr(this);
		TWeakObjectPtr<AMonsterCharacter> DelayMonsterCharacterPtr(MonsterActor);
		if (MonsterAppearJumpWithoutMoveHandle.IsValid())
		{
			MonsterActor->OnModelChangeAppearanceOverDelegate.Remove(MonsterAppearJumpWithoutMoveHandle);
			MonsterAppearJumpWithoutMoveHandle.Reset();
		}
		MonsterAppearJumpWithoutMoveHandle = MonsterActor->OnModelChangeAppearanceOverDelegate.AddLambda([DelayThisPtr,
			DelayMonsterCharacterPtr, Actions, EffectID, LoopTime]()
		{
			if (DelayThisPtr.IsValid() && DelayMonsterCharacterPtr.IsValid())
			{
				UMonsterAppearInterface* ThisPtr = DelayThisPtr.Get();
				AMonsterCharacter* MonsterActor = DelayMonsterCharacterPtr.Get();

				MonsterActor->MonsterCharacterJumpWithoutMoveStart(Actions, EffectID, LoopTime);
				MonsterActor->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->MonsterAppearJumpWithoutMoveHandle);
			}
		});
	}
	else
	{
		MonsterActor->MonsterCharacterJumpWithoutMoveStart(Actions, EffectID, LoopTime);
	}
}

void UMonsterAppearInterface::CLIENT_MonsterAppearLineToPoint_Implementation(
	float DX, float DY, float DZ, float Yaw, float MoveSpeed, const FString& ActionID)
{
	MonsterAppearLineToPoint_Implementation(DX, DY, DZ, Yaw, MoveSpeed, ActionID);
}

void UMonsterAppearInterface::MonsterAppearLineToPoint_Implementation(
	float DX, float DY, float DZ, float Yaw, float MoveSpeed, const FString& ActionID)
{
	if (GetEntity() == nullptr)
	{
		return;
	}
	FVector Dest = FVector(DX, DY, DZ);
	FRotator Rotator = UKismetMathLibrary::MakeRotator(0.0f, 0.0f, Yaw);
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	
	if (!IsValid(MonsterActor)) { return; }

	///动作
	MonsterActor->PlayAction(FSTRING_TO_FNAME(ActionID));
	MonsterActor->SetActorRotation(Rotator);
	MonsterActor->ChangeFilter(MoveSpeed, false, Dest);
	//MonsterActor->ChangeLineToPointFilter(MoveSpeed,Dest, Rotator);
}

void UMonsterAppearInterface::MonsterAppearLineToPointOver_Implementation()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) { return; }

	MonsterActor->ResetFilter();
	MonsterActor->StopAction();
	RPC_CELL_onMonsterAppearLineToPoint();
	
}

void UMonsterAppearInterface::CLIENT_MonsterAppearCurveMove_Implementation(const TArray<FName>& Actions,
	float RisingDistance, const FVector& InStartPosition, float MoveSpeed, const FVector& InEndPosition)
{
	MonsterAppearCurveMove_Implementation(Actions, RisingDistance, InStartPosition, MoveSpeed, InEndPosition);
}

void UMonsterAppearInterface::MonsterAppearCurveMove_Implementation(const TArray<FName>& Actions,
	float RisingDistance, const FVector& InStartPosition, float MoveSpeed, const FVector& InEndPosition)
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());

	if (!IsValid(MonsterActor))
	{
		return;
	}

	FVector StartPosition = MonsterActor->FloorTrace(InStartPosition, true);
	FVector EndPosition = MonsterActor->FloorTrace(InEndPosition, true);
	// 重置数据
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CurveMoveHandle);
	}

	RisingPercent = 0.0f;

	// 屏蔽位置同步
	MonsterActor->SetEnableSyncServerPos(false);

	FVector Direction = EndPosition - StartPosition;
	FVector UpVector = FRotationMatrix::MakeFromX(Direction).Rotator().Quaternion().GetAxisZ();

	FRotator LookRotation = FRotationMatrix::MakeFromX(Direction).Rotator();
	MonsterActor->SetActorRotation(FRotator(MonsterActor->GetActorRotation().Pitch, LookRotation.Yaw, 
		MonsterActor->GetActorRotation().Roll));
	
	MonsterActor->MonsterCharacterJumpStart(Actions, "");

	TWeakObjectPtr<UMonsterAppearInterface> ThisPtr(this);

	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(
			this, CurveMoveHandle, FTimerDelegate::CreateLambda([ThisPtr, Direction, 
				UpVector, MoveSpeed, RisingDistance, StartPosition, EndPosition]()
		{
			if (ThisPtr.IsValid())
			{
				UMonsterAppearInterface* MonsterAppearInterface = ThisPtr.Get();
				AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(MonsterAppearInterface->GetActor());
				if (IsValid(MonsterActor))
				{
					MonsterAppearInterface->RisingPercent += MonsterActor->GetWorld()->GetDeltaSeconds() * MoveSpeed / Direction.Size();

					// 大于1的时候清空
					if (MonsterAppearInterface->RisingPercent > 1.0f)
					{
						if (IsValid(UUECS3GameInstance::Instance))
						{
							UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MonsterAppearInterface->CurveMoveHandle);
						}

						MonsterActor->SetActorLocation(EndPosition);
						MonsterActor->MonsterCharacterJumpEnd(false);
						MonsterActor->SetEnableSyncServerPos(true);
					}
					else
					{
						// 计算当前位置
						FVector Offset = FMath::Sin(MonsterAppearInterface->RisingPercent * PI) * RisingDistance * UpVector;
						Offset += (StartPosition + Direction.Size() * MonsterAppearInterface->RisingPercent * Direction.GetSafeNormal());
						MonsterActor->SetActorLocation(Offset);
					}
				}
			}
		}), GetWorld()->GetDeltaSeconds(), true);
	}
}

void UMonsterAppearInterface::CLIENT_MonsterJumpPointToPoint_Implementation(const FVector& InStartPosition, const FVector& InEndPosition, float XMoveSpeed)
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	// 重置数据
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(JumpCurveMoveHandle);
	}
	JumpDeltaTime = 0.0;
	JumpPercent = 0.0;
	// 屏蔽位置同步
	MonsterActor->SetEnableSyncServerPos(false);
	UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(MonsterActor->GetFilterComponent());
	if (Comp)
	{
		Comp->SetActiveComponentTick(false);
		Comp->ResetComponent();
	}
	//播跳跃动作
	MonsterActor->MonsterCharacterJumpStart({ TEXT("Jump_Begin"), TEXT("Jump_Process"), TEXT("Jump_End") }, "");
	
	float Angle = 0.75f;//根据表现可以定义不同的值
	FVector StartPosition = MonsterActor->FloorTrace(InStartPosition, true);
	FVector EndPosition = MonsterActor->FloorTrace(InEndPosition, true);
	FVector Dir = EndPosition - StartPosition;
	FVector XDir = FVector(Dir.X, Dir.Y, 0.0f);

	float UpTime = 0.0f;//向上的时间
	float NeedTime = 0.0f;//整个过程需要的时间
	float Max_RisingDistance = 0.0f;//能上升的最大距离
	if (XDir.Size()<100)//水平距离太短
	{
		NeedTime = FMath::Sqrt(2* abs(Dir.Z)/980);
		UpTime = NeedTime;
		XMoveSpeed = XDir.Size() / NeedTime;
		Angle = 0.5;
		Max_RisingDistance = Dir.Z / FMath::Sin(Angle* PI);
	}
	else
	{
		NeedTime = XDir.Size() / XMoveSpeed;
		if (abs(Dir.Z) < 100)//垂直距离太短
		{
			UpTime = NeedTime / 2;
			Angle = 1.0f;
			Max_RisingDistance = 0.5 * 980 * UpTime * UpTime;
		} 
		else
		{
			UpTime = (NeedTime / (Angle*PI)) * (0.5*PI);
			Max_RisingDistance = Dir.Z / FMath::Sin(Angle* PI);
		}
	}

	float Gravity = 2.0f*abs(Dir.Z) / (NeedTime*NeedTime);
	//float Max_XDir = (XDir.Size() / Angle* PI) * PI;

	FRotator LookRotation = FRotationMatrix::MakeFromX(Dir).Rotator();
	MonsterActor->SetActorRotation(FRotator(MonsterActor->GetActorRotation().Pitch, LookRotation.Yaw, MonsterActor->GetActorRotation().Roll));

	TWeakObjectPtr<UMonsterAppearInterface> ThisPtr(this);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(
			this, JumpCurveMoveHandle, FTimerDelegate::CreateLambda([ThisPtr, Angle, Dir, XDir, 
				XMoveSpeed, StartPosition, EndPosition, UpTime, NeedTime, Max_RisingDistance, Gravity]()
		{
			if (ThisPtr.IsValid())
			{
				UMonsterAppearInterface* MonsterAppearInterface = ThisPtr.Get();
				AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(MonsterAppearInterface->GetActor());
				float DstDistanceZ = 0.0f;
				FVector2D XPercent = FVector2D(0, 0);
				if (IsValid(MonsterActor))
				{
					MonsterAppearInterface->JumpDeltaTime += MonsterActor->GetWorld()->GetDeltaSeconds();
					if (Dir.Z >= 0.0f || abs(Dir.Z) < 100)
					{
						//从低处往高处跳 或者同一水平面跳跃
						//MonsterAppearInterface->JumpPercent += MonsterActor->GetWorld()->GetDeltaSeconds() * XMoveSpeed / Max_XDir;
						MonsterAppearInterface->JumpPercent = MonsterAppearInterface->JumpDeltaTime / (2* UpTime);
						// 大于Angel的时候清空
						if (MonsterAppearInterface->JumpPercent >= Angle || MonsterAppearInterface->JumpDeltaTime >= NeedTime)
						{
							MonsterAppearInterface->StopMonsterJumpPointToPoint(EndPosition);
						}
						else
						{
							DstDistanceZ = StartPosition.Z + FMath::Sin(MonsterAppearInterface->JumpPercent * PI) * Max_RisingDistance;
							XPercent = FVector2D(StartPosition + (XMoveSpeed * MonsterAppearInterface->JumpDeltaTime)* XDir.GetSafeNormal());
							MonsterActor->SetActorLocation(FVector(XPercent.X, XPercent.Y, DstDistanceZ));
						}
					}
					else
					{
						DstDistanceZ = StartPosition.Z - 0.5f * Gravity * (MonsterAppearInterface->JumpDeltaTime * MonsterAppearInterface->JumpDeltaTime);
						//从高处往低处跳
						if (DstDistanceZ <= EndPosition.Z || MonsterAppearInterface->JumpDeltaTime >= NeedTime)
						{
							MonsterAppearInterface->StopMonsterJumpPointToPoint(EndPosition);
						} 
						else
						{
							XPercent = FVector2D(StartPosition + (XMoveSpeed * MonsterAppearInterface->JumpDeltaTime)* XDir.GetSafeNormal());
							MonsterActor->SetActorLocation(FVector(XPercent.X, XPercent.Y, DstDistanceZ));
						}
					}
				}
			}
		}), GetWorld()->GetDeltaSeconds(), true, 0.5);
	}
}

void UMonsterAppearInterface::StopMonsterJumpPointToPoint(FVector Position)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(JumpCurveMoveHandle);
	}
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	MonsterActor->SetActorLocation(Position);
	MonsterActor->MonsterCharacterJumpEnd(false);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		FTimerHandle JumpEndMoveHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(JumpEndMoveHandle, this, &UMonsterAppearInterface::RPC_CELL_onMonsterJumpPointToPointEnd, 1.5f, false);
	}
	MonsterActor->SetEnableSyncServerPos(true);
	UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(MonsterActor->GetFilterComponent());
	if (Comp)
	{
		Comp->ResetComponent();
		Comp->SetActiveComponentTick(true);
	}
}

void UMonsterAppearInterface::RPC_CELL_onMonsterAppearJumpWithoutMoveEnd(ACharacter* Character, FACTION_DATA InActionData )
{
	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterAppearInterface::RPC_CELL_onMonsterAppearJumpWithoutMoveEnd : Monster!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Monster->CellCall(TEXT("CELL_onMonsterAppearJumpWithoutMoveEnd"), Args);
}

void UMonsterAppearInterface::RPC_CELL_onMonsterJumpPointToPointEnd()
{
	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterAppearInterface::RPC_CELL_onMonsterJumpPointToPointEnd : Monster!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Monster->CellCall(TEXT("CELL_onMonsterJumpPointToPointEnd"), Args);
}


void UMonsterAppearInterface::RPC_CELL_onMonsterAppearLineToPoint()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterAppearInterface::RPC_CELL_onMonsterAppearLineToPoint : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onMonsterAppearLineToPoint"), args);
}

void UMonsterAppearInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_MonsterAppearJump");
	ArrBlueFunc.Add("CLIENT_MonsterAppearJumpWithoutMove");
	ArrBlueFunc.Add("CLIENT_MonsterAppearLineToPoint");
	ArrBlueFunc.Add("MonsterAppearLineToPointOver");
	ArrBlueFunc.Add("CLIENT_MonsterAppearCurveMove");
	ArrBlueFunc.Add("CLIENT_MonsterJumpPointToPoint");
	Supper::InitBlueCB();
}
CONTROL_COMPILE_OPTIMIZE_END

