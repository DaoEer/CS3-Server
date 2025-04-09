// Fill out your copyright notice in the Description page of Project Settings.

#include "IceBirdEffectEmitter.h"
// UE4
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequenceBase.h"
// 数据类型
#include "GameData/EffectEmitterData.h"
// CS3类型
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"



void AIceBirdEffectEmitter::InitFromConfig()
{
	Super::InitFromConfig();

	//飞行速度默认10米每秒
	FlySpeed = FlySpeed > 0.f ? FlySpeed : 1000.f;
	//冰鸟光效默认有多个阶段
	bCanSpecialMove = true;
	//冰鸟做变换运动的最近距离
	TransformationDistance = TransformationDistance > 0.f ? TransformationDistance : 1000.f;
	//冰鸟不支持按世界飞行
	bIsFlyByTime = false;
	//冰鸟默认的上升高度为10米
	RisingDistance = RisingDistance > 0.f ? RisingDistance : 1000.f;
}

void AIceBirdEffectEmitter::SecondMove(float DeltaTime)
{
	float RisingLength = DeltaTime * 1500.f;

	NormalMove(DeltaTime, FVector(0, 0, RisingLength));
}

void AIceBirdEffectEmitter::GetSecondMoveRotation(FRotator& OutRotation)
{
	// 仰角
	
	float Angle = -FMath::Acos(FlySpeed / 1000.f) * 180 / PI;
	OutRotation.Roll = Angle;
}

void AIceBirdEffectEmitter::EnterNextMove()
{
	switch (FlyType)
	{
		///判断进入第二阶段
	case FLY_TYPE::NORMAL:
		if (bCanSpecialMove && RisingDistance > 0.0f && (GetActorLocation() - TargetPos).Size() < TransformationDistance)
		{
			FlyType = FLY_TYPE::SECOND;
			bCanSpecialMove = false;
			FlySpeed = 300.f;
		}
		break;
		///判断进入第三阶段
	case FLY_TYPE::SECOND:
		if (TotalRisingOffset > RisingDistance)
		{
			FlyType = FLY_TYPE::THIRD;
			FlySpeed = 0.f;
			if (AnimAsset.Num() > 1 && SKComponent)
			{
				SKComponent->PlayAnimation(AnimAsset[1], true);
			}

			FRotator Rotation = GetActorRotation();
			Rotation.Roll = 0.f;
			SetActorRotation(Rotation);

			///进入第三阶段后一秒之后进入第一阶段
			FTimerHandle Handle;
			float Length = 1.0f;
			if (AnimAsset.Num() > 1 && Cast<UAnimSequenceBase>(AnimAsset[1]))
			{
				Length = Cast<UAnimSequenceBase>(AnimAsset[1])->GetPlayLength() / EffectEmitterData->SkeletalMesh.PlayRate;
			}
			TWeakObjectPtr<AIceBirdEffectEmitter> ThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, Handle, FTimerDelegate::CreateLambda([ThisPtr]()
			{
				if (ThisPtr.IsValid())
				{
					AIceBirdEffectEmitter* Self = ThisPtr.Get();

					if (Self->AnimAsset.Num() > 2 && Self->SKComponent)
					{
						Self->SKComponent->PlayAnimation(Self->AnimAsset[2], true);
					}

					Self->FlyType = FLY_TYPE::NORMAL;
					Self->FlySpeed = 3000.f;
					//上升距离清零，因为最后一个阶段是直接飞过去的，没有计算偏移
					Self->TotalRisingOffset = 0.0f;
				}
			}), Length, false);
		}
		break;
	default:
		break;
	}
}

