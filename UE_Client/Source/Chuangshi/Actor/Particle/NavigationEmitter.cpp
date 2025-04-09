// Fill out your copyright notice in the Description page of Project Settings.

#include "NavigationEmitter.h"
// UE4
#include "GameFramework/CharacterMovementComponent.h"
#include "Particles/ParticleSystemComponent.h"
#include "Components/SplineComponent.h"
#include "Components/CapsuleComponent.h"
// CS3类型
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/ParticleManager.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"

CONTROL_COMPILE_OPTIMIZE_START

ANavigationEmitter::ANavigationEmitter()
{
	NavigationTrace = CreateDefaultSubobject<USplineComponent>(TEXT("NavigationTrace"));
	NavigationTrace->AttachToComponent(GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
	NavigationTrace->SetAbsolute(true, true, true);

	SpiralTrace = CreateDefaultSubobject<USplineComponent>(TEXT("SpiralTrace"));
	SpiralTrace->AttachToComponent(GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);

	RisingTrace = CreateDefaultSubobject<USplineComponent>(TEXT("RisingTrace"));
	RisingTrace->AttachToComponent(GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
	RisingTrace->SetAbsolute(true, true, true);
}

void ANavigationEmitter::BeginPlay()
{
	PrimaryActorTick.bCanEverTick = true;

	Super::BeginPlay();

	InitNavigationTrace();

	CalculateScale();
}

void ANavigationEmitter::InitNavigationTrace()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (Player)
	{
		// 获取导航点
		NavLocationList = Player->GetNavigateGuidePathList();

		NavigationTrace->SetSplinePoints(NavLocationList, ESplineCoordinateSpace::World, true);

		TArray<FVector> NewPointList;
		for (int32 i = 0; i < NavigationTrace->GetNumberOfSplinePoints(); i++)
		{
			FRotator Rotation = NavigationTrace->GetRotationAtSplinePoint(i, ESplineCoordinateSpace::World);
			// 新的轨迹点，位于玩家的右上方
			NewPointList.Add(NavLocationList[i] + FRotationMatrix(Rotation).GetScaledAxis(EAxis::Y) * 0.f + FVector(0, 0, 150));
		}

		NavigationTrace->SetSplinePoints(NewPointList, ESplineCoordinateSpace::World, true);

		MoveSpeed = Player->GetCharacterMovement()->GetMaxSpeed() * 2;
	}
}

void ANavigationEmitter::CalculateScale()
{
	if (NavLocationList.Num() < 2)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);
		return;
	}
	
	float NavLength = 0.0f;
	for (int32 i = 1; i < NavLocationList.Num(); i++)
	{
		NavLength += (NavLocationList[i] - NavLocationList[i - 1]).Size();
	}

	Scale = NavigationTrace->GetSplineLength() / NavLength;
}

void ANavigationEmitter::UpdateMoveSpeed(float DeltaSeconds)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	
	if (Player)
	{
		// 判断是否处于正常速度
		if (bNormalSpeed)
		{
			// 根据位置动态调整缩放
			float CurrentScale = Scale;
			FVector Location = GetActorLocation();
			FVector PlayerLocation = Player->GetActorLocation();
			if ((Location - PlayerLocation).Size() < ForwardDiatance / 2.f || bSpeedUp)
			{
				
				if (AdjustScale < 0.5f)
				{
					// 加速
					AdjustScale += 0.5f * DeltaSeconds;
					bSpeedUp = true;
				}
				else
				{
					// 加速到最大了
					bSpeedUp = false;
				}
				
				CurrentScale += AdjustScale;
			}
			else if ((Location - PlayerLocation).Size() > ForwardDiatance * 1.5f)
			{
				// 超过了最大距离，开始减速
				AdjustScale -= DeltaSeconds;
				CurrentScale += AdjustScale;
			}
			else
			{
				// 来回摆动
				if(AdjustScale < 0)
				{
					AdjustScale += 0.02f;
					CurrentScale += AdjustScale;
				}
				else
				{
					AdjustScale -= 0.02f;
					CurrentScale += AdjustScale;
				}
			}

			// 跳起来的时候不计算Z方向的速度
			if (Player->GetCharacterMovement()->IsFalling())
			{
				MoveSpeed = Player->GetCapsuleComponent()->ComponentVelocity.Size2D() * CurrentScale;
			}
			else
			{
				MoveSpeed = Player->GetCapsuleComponent()->ComponentVelocity.Size() * CurrentScale;
			}
			return;
		}

		MoveSpeed -= DeltaSeconds * Player->GetCharacterMovement()->GetMaxSpeed();

		if (MoveSpeed < Player->GetCharacterMovement()->GetMaxSpeed() * Scale)
		{
			bNormalSpeed = true;
			// 粒子在玩家前方的距离
			ForwardDiatance = (GetActorLocation() - Player->GetActorLocation()).Size();
			MoveSpeed = Player->GetCharacterMovement()->Velocity.Size() * Scale;
		}
	}
}

void ANavigationEmitter::Tick(float DeltaSeconds)
{
	if (bPlaying)
	{
		CurrentTime += DeltaSeconds;

		// 光效逐渐消散
		UpdateTransparency(DeltaSeconds);

		if (!bSpiralRising)
		{
			UpdateMoveSpeed(DeltaSeconds);
			Distance += MoveSpeed * DeltaSeconds;
		}
	
		//当前要到达的位置
		FVector Location;
		FRotator Rotation;

		//判断开始上升
		if (!bSpiralRising && Distance > NavigationTrace->GetSplineLength())
		{
			bSpiralRising = true;
			MoveSpeed = 1200.f;

			//设置上升曲线的位置和方向
			Location = NavigationTrace->GetLocationAtSplinePoint(NavigationTrace->GetNumberOfSplinePoints() - 1, ESplineCoordinateSpace::World);
			Rotation = NavigationTrace->GetRotationAtSplinePoint(NavigationTrace->GetNumberOfSplinePoints() - 1, ESplineCoordinateSpace::World);
			Rotation.Yaw += 90.f;
			RisingTrace->SetWorldLocationAndRotation(Location, Rotation);

			OtherDistance = 0.0f;
		}

		if (bSpiralRising)
		{
			MoveSpeed += 800.f * DeltaSeconds;
			OtherDistance += DeltaSeconds * MoveSpeed;
				
			if (OtherDistance < RisingTrace->GetSplineLength())
			{
				Location = RisingTrace->GetLocationAtDistanceAlongSpline(OtherDistance, ESplineCoordinateSpace::World);
				Rotation = RisingTrace->GetRotationAtDistanceAlongSpline(OtherDistance, ESplineCoordinateSpace::World);
			}
			else
			{
				Stop();
				return;
			}
		}
		else
		{
			// 计算随机旋转
			RandTime += DeltaSeconds;

			if (RandTime > RandFrequency)
			{
				if (FMath::RandRange(-1.f, 1.f) >= 0)
				{
					SpiralSpeed = 400;
				}
				else
				{
					SpiralSpeed = 0;
				}

				RandFrequency = FMath::RandRange(2, 8);
				RandTime = 0.0f;
			}
			
			// 计算螺旋点
			OtherDistance += SpiralSpeed * DeltaSeconds;
			float length = SpiralTrace->GetSplineLength();
			OtherDistance = (OtherDistance / length - FMath::TruncToInt(OtherDistance / length)) * SpiralTrace->GetSplineLength();

			// 添加螺旋偏移
			FTransform Transform = NavigationTrace->GetTransformAtDistanceAlongSpline(Distance, ESplineCoordinateSpace::World);
			Location = Transform.TransformPosition(SpiralTrace->GetLocationAtDistanceAlongSpline(OtherDistance, ESplineCoordinateSpace::Local));
			Rotation = NavigationTrace->GetRotationAtDistanceAlongSpline(Distance, ESplineCoordinateSpace::World);
		}

		// 设置光效位置
		SetActorLocationAndRotation(Location, Rotation.Quaternion());
	}
	
	AEmitter::Tick(DeltaSeconds);
}

CONTROL_COMPILE_OPTIMIZE_END
