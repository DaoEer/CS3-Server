// Fill out your copyright notice in the Description page of Project Settings.

#include "FlyEffectEmitter.h"
// 数据类型
#include "GameData/EffectEmitterData.h"
// CS3类型
#include "Actor/GameCharacter.h"
#include "Actor/ServerCharacter.h"
#include "Manager/ParticleManager.h"
#include "Component/PerformanceComponent.h"
#include "Util/CS3Debug.h"
#include "Entity.h"


DECLARE_CYCLE_STAT(TEXT("GetFlyTargetPos"), STAT_GetFlyTargetPos, STATGROUP_AFlyEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("GetFlySourcePos"), STAT_GetFlySourcePos, STATGROUP_AFlyEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("NormalMove"), STAT_NormalMove, STATGROUP_AFlyEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("CheckAndSetEmitterBase"), STAT_CheckAndSetEmitterBase, STATGROUP_AFlyEffectEmitter);

CONTROL_COMPILE_OPTIMIZE_START
AFlyEffectEmitter::AFlyEffectEmitter()
{
	
}

void AFlyEffectEmitter::BeginPlay()
{
	// 飞行类光效，统统开启Tick
	PrimaryActorTick.bCanEverTick = true;

	// 绑定飞行光效抵达事件
	OnEffectArrived.AddDynamic(this, &AFlyEffectEmitter::OnFlyFinished);

	Super::BeginPlay();
}

void AFlyEffectEmitter::InitFromConfig()
{
	Super::InitFromConfig();

	// 第二阶段运动相关
	bCanSpecialMove			= EffectData->SpecialData.bCanSpecialMove;
	TransformationDistance	= EffectData->SpecialData.TransformationDistance;
	RisingDistance			= EffectData->SpecialData.RisingDistance;

	// 速度
	FlySpeed				= EffectData->FlyData.FlySpeed;
	bIsFlyByTime				= EffectData->FlyData.bIsFlyByTime;
}

void AFlyEffectEmitter::InitEmitterTransform()
{
	ACharacter* Character = Cast<ACharacter>(FirstTarget);

	//设置位置
	FTransform Transform = Character && FirstTransform->BindSocket != "" ? Character->GetMesh()->GetSocketTransform(FName(*FirstTransform->BindSocket)) : FirstTarget->GetActorTransform();
	//根据bLocationOnWorld属性设置位置
	FVector Location;
	if (FirstTransform->bIsLocationOnWorld)
	{
		Location = FirstTransform->Transform.GetLocation();
	}
	else
	{
		Location = Transform.TransformPosition(FirstTransform->Transform.GetLocation());
	}
	//根据bRotationOnWorld属性设置位置
	FRotator Rotation;
	if (FirstTransform->bIsRotationOnWorld)
	{
		Rotation = FirstTransform->Transform.GetRotation().Rotator();
	}
	else
	{
		Rotation = Transform.TransformRotation(FirstTransform->Transform.GetRotation()).Rotator();
	}
	SetActorLocation(Location);
	SetActorRotation(Rotation);
	//不绑定的光效为配置表缩放
	SetActorScale3D(FirstTransform->Transform.GetScale3D());

	//设置起始点
	SourcePos = GetActorLocation();
	//设置目标点
	GetFlyTargetPos(true);

	//设置朝向
	if (FirstTarget != SecondTarget)
	{
		FRotator LookRotation = FRotationMatrix::MakeFromX(TargetPos - FirstTarget->GetActorLocation()).Rotator();
		SetActorRotation(LookRotation);
	}

	//是否可以做第二阶段运动
	if ((TargetPos - GetActorLocation()).Size() < TransformationDistance && 
		TransformationDistance > 0.0f && RisingDistance > 0.0f)
	{
		bCanSpecialMove = false;
	}

	//设置移动平台相关属性
	if (CheckAndSetEmitterBase() && Cast<AServerCharacter>(ParentActor)->GetSelfEntity())
	{
		AttachToActor(ParentActor, FAttachmentTransformRules::KeepWorldTransform);
	}
	
	//表现组件中添加此光效
	if (Cast<AGameCharacter>(FirstTarget) && EffectData->BaseEffectData.bIsBindingVisibility)
	{
		Cast<AGameCharacter>(FirstTarget)->GetPerformanceComponent()->AddEffect(UID);
	}

	//有路径资源的光效在蓝图中初始化位置
	if (Spline)
	{
		InitSplineTransform();
	}
}

FVector AFlyEffectEmitter::GetFlyTargetPos(bool bInit /* = false */)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFlyTargetPos);

	// 设置目标飞行重点，判断SecondTransform的所有属性设置
	if ((SecondTransform->bIsLocationOnWorld || !SecondTransform->bIsBind) && !bInit)
	{
		return TargetPos;
	}

	if (IsValid(SecondTarget))
	{
		ACharacter* Character = Cast<ACharacter>(SecondTarget);
		//刷新目标点，自己的位置加上相对偏移
		FTransform Transform;
		Transform = Character && SecondTransform->BindSocket != "" ? Character->GetMesh()->GetSocketTransform(FName(*SecondTransform->BindSocket)) : SecondTarget->GetActorTransform();
		TargetPos = Transform.TransformPosition(SecondTransform->Transform.GetLocation());
	}

	if (!SecondTransform->bIsBind && SecondTransform->bIsLocationOnWorld)
	{
		return TargetPos = SecondTransform->Transform.GetLocation();
	}

	return TargetPos;
}

FVector AFlyEffectEmitter::GetFlySourcePos(bool bInit /* = false */)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFlySourcePos);

	// 设置目标飞行重点，判断SecondTransform的所有属性设置
	if ((FirstTransform->bIsLocationOnWorld) && !bInit)
	{
		return SourcePos;
	}

	if (IsValid(FirstTarget))
	{
		ACharacter* Character = Cast<ACharacter>(FirstTarget);
		//刷新目标点，自己的位置加上相对偏移
		FTransform Transform;
		Transform = Character && FirstTransform->BindSocket != "" ? Character->GetMesh()->GetSocketTransform(FName(*FirstTransform->BindSocket)) : FirstTarget->GetActorTransform();
		SourcePos = Transform.TransformPosition(FirstTransform->Transform.GetLocation());
	}
	
	if (FirstTransform->bIsLocationOnWorld)
	{
		return SourcePos = FirstTransform->Transform.GetLocation();
	}

	return SourcePos;
}

void AFlyEffectEmitter::PlayTriggerParticle()
{
	for (auto TriggerID : EffectData->FlyData.FlyArriveEffectList)
	{
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(TriggerID, 0.0f, FirstTarget, SecondTarget);
	}
}

void AFlyEffectEmitter::OnFlyFinished()
{
	PlayTriggerParticle();
}

void AFlyEffectEmitter::Tick(float DeltaTime)
{
	if (bPlaying)
	{
		//刷新目标点
		GetFlyTargetPos();

		//刷新移动平台，只有初始化的时候在移动平台上才检测
		if (ParentActor && !CheckAndSetEmitterBase())
		{
			DetachFromActor(FDetachmentTransformRules::KeepWorldTransform);
		}

		//根据飞行时间更新速度
		if (bIsFlyByTime)
		{
			FlySpeed = (GetActorLocation() - FVector(0, 0, TotalRisingOffset) - TargetPos).Size() / (EffectData->FlyData.FlyTime - CurrentTime);
		}

		switch (FlyType)
		{
		case FLY_TYPE::NORMAL:
			NormalMove(DeltaTime);
			break;
		case FLY_TYPE::SECOND:
			SecondMove(DeltaTime);
			break;
		default:
			break;
		}
	}
	
	AEffectEmitter::Tick(DeltaTime);
}
void AFlyEffectEmitter::SetEffectLocationAndRotation(const float& MoveDistance, const FVector& RisingOffset, const FVector& TargetLocation)
{
	// 世界朝向
	FVector Location;
	FRotator Rotation = FRotationMatrix::MakeFromX(TargetLocation - GetActorLocation()).Rotator();
	if (ParentActor)
	{
		// 相对于移动平台的相对朝向
		FQuat Quaternion = ParentActor->GetActorTransform().InverseTransformRotation(Rotation.Quaternion());
		// Delta，相对位置移动，需要乘以缩放
		Location = (Quaternion.GetAxisX() * MoveDistance + Quaternion.GetAxisZ() * RisingOffset.Z) * GetActorRelativeScale3D();
		// 实际的相对位置更新
		Location += RootComponent->RelativeLocation;
		// 重置朝向，加-90度偏移
		Rotation = (Quaternion * FRotator(0, -90, 0).Quaternion()).Rotator();
		// 上升阶段重置朝向
		if (FlyType == FLY_TYPE::SECOND)
		{
			GetSecondMoveRotation(Rotation);
		}
		SetActorRelativeTransform(FTransform(Rotation, Location, GetActorRelativeScale3D()));
	}
	else
	{
		// 位置
		Location = (TargetLocation - GetActorLocation() + FVector(0, 0, TotalRisingOffset)).GetSafeNormal() * MoveDistance + RisingOffset + GetActorLocation();
		// 重置朝向
		Rotation = (Rotation.Quaternion() * FRotator(0, -90, 0).Quaternion()).Rotator();
		if (FlyType == FLY_TYPE::SECOND)
		{
			GetSecondMoveRotation(Rotation);
		}
		SetActorLocationAndRotation(Location, Rotation, true);
	}
}

void AFlyEffectEmitter::NormalMove(float DeltaTime, FVector RisingOffset /*= FVector(0,0,0)*/)
{
	SCOPE_CYCLE_COUNTER(STAT_NormalMove);

	float MoveLength;
	float FrameDistance = FlySpeed * DeltaTime;
	float RemainMoveDistance = FrameDistance;
	float DefaultMaxDistance = 60;//这边设置为60是应该1倍的胶囊体直径为68，60保证可以接触到
	float TargetDistance = (TargetPos - GetActorLocation() + FVector(0, 0, TotalRisingOffset)).Size(); // 与目标点的距离

	if (TargetDistance <= 1.0f)
	{
		SetActorLocation(TargetPos);
		OnEffectArrived.Broadcast();
		Stop();//结束移动
		return;
	}

	if (FrameDistance < DefaultMaxDistance)
	{
		MoveLength = FMath::Min(FrameDistance, TargetDistance);
		SetEffectLocationAndRotation(MoveLength, RisingOffset, TargetPos);
		TargetDistance = (TargetPos - GetActorLocation() + FVector(0, 0, TotalRisingOffset)).Size();// 重新获取，因为位置已经变了

		if (TargetDistance <= 1.0f)
		{
			SetActorLocation(TargetPos);
			OnEffectArrived.Broadcast();
			Stop();//结束移动
			return;
		}		
	}
	else
	{
		//一帧移动的距离过大分段移动，为了碰撞检测
		while (RemainMoveDistance - DefaultMaxDistance > 0)
		{
			MoveLength = FMath::Min(TargetDistance, DefaultMaxDistance);
			SetEffectLocationAndRotation(MoveLength, RisingOffset, TargetPos);
			RemainMoveDistance -= MoveLength;
			TargetDistance = (TargetPos - GetActorLocation() + FVector(0, 0, TotalRisingOffset)).Size();

			if (TargetDistance <= 1.0f)
			{
				SetActorLocation(TargetPos);
				OnEffectArrived.Broadcast();
				Stop();//结束移动
				return;
			}
		}
		SetEffectLocationAndRotation(FMath::Min(TargetDistance, RemainMoveDistance), RisingOffset, TargetPos);
		TargetDistance = (TargetPos - GetActorLocation() + FVector(0, 0, TotalRisingOffset)).Size();
		if (TargetDistance <= 1.0f)
		{
			SetActorLocation(TargetPos);
			OnEffectArrived.Broadcast();
			Stop();//结束移动
			return;
		}
	}

	// 累计上升高度
	TotalRisingOffset += RisingOffset.Z;

	// 判断是否要进入下一阶段
	EnterNextMove();
}

void AFlyEffectEmitter::SecondMove(float DeltaTime)
{
	LastRisingPercent = RisingPercent;
	// 计算当前的进度
	if (bIsFlyByTime)
	{
		RisingPercent = (CompletedTime - (EffectData->FlyData.FlyTime - CurrentTime)) / CompletedTime;
	}
	else
	{
		float CurrentPercent = 1 - (GetActorLocation() - FVector(0, 0, FMath::Sin(RisingPercent * PI) * RisingDistance) - TargetPos).Size() / TransformationDistance;

		if (CurrentPercent> RisingPercent)
		{
			RisingPercent = CurrentPercent;
		}
	}

	// 上升的距离
	float RisingLength = (FMath::Sin(RisingPercent * PI) - FMath::Sin(LastRisingPercent * PI)) * RisingDistance;
	
	NormalMove(DeltaTime, FVector(0, 0, RisingLength));
}

void AFlyEffectEmitter::GetSecondMoveRotation(FRotator& OutRotation)
{
	// 斜率
	float k = FMath::Cos(RisingPercent * PI) * (RisingDistance / (GetActorLocation() - FVector(0, 0, TotalRisingOffset) - TargetPos).Size());
	float Angle = -atan(k) * 180 / PI;
	OutRotation.Roll = Angle;
}

void AFlyEffectEmitter::EnterNextMove()
{
	// 判断是否要进入曲线阶段
	if (bCanSpecialMove && (GetActorLocation() - TargetPos).Size() < TransformationDistance)
	{
		FlyType = FLY_TYPE::SECOND;
		bCanSpecialMove = false;

		// 播放第二阶段动画
		if (AnimAsset.Num() > 1 && SKComponent)
		{
			SKComponent->PlayAnimation(AnimAsset[1], true);
		}

		if (bIsFlyByTime)
		{
			CompletedTime = EffectData->FlyData.FlyTime - CurrentTime;
		}
	}
}

bool AFlyEffectEmitter::CheckAndSetEmitterBase()
{
	SCOPE_CYCLE_COUNTER(STAT_CheckAndSetEmitterBase);

	// 当施法者和目标都在相同的移动平台上时，绑定光效到移动平台上
	AServerCharacter* SFTarget = Cast<AServerCharacter>(FirstTarget);
	AServerCharacter* SSTarget = Cast<AServerCharacter>(SecondTarget);
	// 初始化的时候，判断两个目标的Parent，否则只判断目标
	if (!ParentActor)
	{
		if (SFTarget && SSTarget && SFTarget->GetSelfEntity() && SSTarget->GetSelfEntity() && SFTarget->GetSelfEntity()->ParentID() != 0
			&& SFTarget->GetSelfEntity()->ParentID() == SSTarget->GetSelfEntity()->ParentID())
		{
			KBEngine::Entity* ParentEntity = SFTarget->GetSelfEntity()->Parent();
			if (ParentEntity != nullptr)
			{
				AActor* MovingPlatform = ParentEntity->Actor();
				if (IsValid(MovingPlatform))
				{
					ParentActor = MovingPlatform;
					return true;
				}
			}
		}
	}
	else
	{
		if (SSTarget && SSTarget->GetSelfEntity() && SSTarget->GetSelfEntity()->ParentID())
		{
			return true;
		}
	}
	// 失败了清空
	ParentActor = nullptr;
	return false;
}

CONTROL_COMPILE_OPTIMIZE_END
