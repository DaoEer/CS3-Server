// Fill out your copyright notice in the Description page of Project Settings.

#include "BeamEffectEmitter.h"
// UE4
#include "GameFramework/Character.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Particles/ParticleSystemComponent.h"
// 数据类型
#include "Util/CS3Debug.h"
#include "GameData/EffectEmitterData.h"
// CS3类型
#include "Actor/GameCharacter.h"
#include "Actor/GameCharacter.h"
#include "Component/PerformanceComponent.h"

DECLARE_CYCLE_STAT(TEXT("UpdateBeamCollisionList"), STAT_UpdateBeamCollisionList, STATGROUP_ABeamEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("Move"), STAT_Move, STATGROUP_ABeamEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("SetTargetTangent"), STAT_SetTargetTangent, STATGROUP_ABeamEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("SetComponentTransform"), STAT_SetComponentTransform, STATGROUP_ABeamEffectEmitter);

CONTROL_COMPILE_OPTIMIZE_START

ABeamEffectEmitter::ABeamEffectEmitter()
{

}

void ABeamEffectEmitter::InitEmitterTransform()
{
	//初始化一下起点和终点
	GetFlySourcePos(true);
	GetFlyTargetPos(true);

	///设置起始点
	SetSourcePoint();
	//设置终点
	SetTargetPoint();
	//设置特殊的粒子属性
	SetBeamAttribute();
	//设置连线在目标那边的切线
	SetTargetTangent();

	//设置位置
	FVector Scale3D = FirstTransform->bIsBind ? FirstTransform->Transform.GetScale3D() * FirstTarget->GetActorScale3D() : FirstTransform->Transform.GetScale3D();
	SetActorTransform(FTransform(FRotator(0.f), SourcePos, Scale3D));

	//表现组件中添加此光效
	if (Cast<AGameCharacter>(FirstTarget) && EffectData->BaseEffectData.bIsBindingVisibility)
	{
		Cast<AGameCharacter>(FirstTarget)->GetPerformanceComponent()->AddEffect(UID);
	}
}

void ABeamEffectEmitter::SetBeamAttribute()
{
	GetParticleSystemComponent()->SetVectorParameter("ParticleSize", FVector(EffectData->BeamData.ParticleSize, 1.f, 1.f));
	GetParticleSystemComponent()->SetFloatParameter("ParticleRange", EffectData->BeamData.ParticleRange);

	//启用弯曲模式的时候，他是碰撞时不准确的，所有直接让他不可用
	if (!STComponent)
	{
		return;
	}

	if (EffectData->BeamData.IsBendFromTarget)
	{
		STComponent->SetStaticMesh(nullptr);
	}
	else
	{
		//需要动态的设置位置，不跟随Actor移动，以免产生错误的碰撞
		FTransform CurrentComponentTransform = STComponent->GetComponentTransform();
		STComponent->SetAbsolute(true, true, true);
		STComponent->SetWorldTransform(CurrentComponentTransform);
		STComponent->SetWorldScale3D(FVector(EffectData->BeamData.ParticleSize *  EffectData->BeamData.ParticleRange / 100.f));
	}
}

FVector ABeamEffectEmitter::GetFlySourcePos(bool bInit /* = false */)
{
	// 设置目标飞行重点，判断SecondTransform的所有属性设置
	if ((FirstTransform->bIsLocationOnWorld || !FirstTransform->bIsBind) && !bInit)
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

	if (!FirstTransform->bIsBind && FirstTransform->bIsLocationOnWorld)
	{
		return SourcePos = FirstTransform->Transform.GetLocation();
	}

	return SourcePos;
}

void ABeamEffectEmitter::SetSourcePoint()
{
	///实时更新位置
	if (IsValid(FirstTarget))
	{
		GetFlySourcePos();

		for (int32 i = 0; i < GetParticleSystemComponent()->Template->Emitters.Num(); i++)
		{
			GetParticleSystemComponent()->SetBeamSourcePoint(i, SourcePos, 0);
		}
	}
}

void ABeamEffectEmitter::SetTargetTangent()
{
	SCOPE_CYCLE_COUNTER(STAT_SetTargetTangent);

	if (IsValid(FirstTarget) && EffectData->BeamData.IsBendFromTarget)
	{
		for (int32 i = 0; i < GetParticleSystemComponent()->Template->Emitters.Num(); i++)
		{
			//GetParticleSystemComponent()->SetBeamSourceTangent(i, FirstTarget->GetActorForwardVector() * OtherEffectData->Beam_BendStrength, 0);

			// 起点到终点的Rotation的yaw
			float temp = (SecondTarget->GetActorLocation() - FirstTarget->GetActorLocation()).Rotation().Yaw;
			// 角色相對坐標系所在的方位 保證角色不管在哪個象限面朝目標時都是直綫
			float Fst2Snd = 90.f - temp;
			// 角度以FirstTarget面朝SecondTarget為0做偏移
			float offset = (temp - FirstTarget->GetActorRotation().Yaw);
			// tangent值由起点面朝终点为0做基准，FirstTarget朝向偏移来决定
			FVector tangent( FMath::Sin(FMath::DegreesToRadians(Fst2Snd + offset)), FMath::Cos(FMath::DegreesToRadians(Fst2Snd + offset)), 0);				
			GetParticleSystemComponent()->SetBeamSourceTangent(i, tangent, 0);
			
			// Tangent的强度由起点到终点的距离，配合填表的强度来决定
			float strength = (SecondTarget->GetActorLocation() - FirstTarget->GetActorLocation()).Size2D() * EffectData->BeamData.BendStrength;
			GetParticleSystemComponent()->SetBeamSourceStrength(i, strength, 0);
		}
	}
}

void ABeamEffectEmitter::SetTargetPoint()
{
	if (IsValid(SecondTarget))
	{
		GetFlyTargetPos();

		for (int32 i = 0; i < GetParticleSystemComponent()->Template->Emitters.Num(); i++)
		{
			GetParticleSystemComponent()->SetBeamTargetPoint(i, TargetPos, 0);
		}
	}
}

void ABeamEffectEmitter::Move()
{
	SCOPE_CYCLE_COUNTER(STAT_Move);

	//当光效移动的时候，光效的位置在移动的点
	FVector Direction = TargetPos - SourcePos;
	if (CurrentDistance < Direction.Size())
	{
		Direction.Normalize();
		for (int32 i = 0; i < GetParticleSystemComponent()->Template->Emitters.Num(); i++)
		{
			GetParticleSystemComponent()->SetBeamTargetPoint(i,
				SourcePos + Direction * CurrentDistance, 0);
		}
		SetActorLocationAndRotation(SourcePos + Direction * CurrentDistance, FRotationMatrix::MakeFromX(Direction).Rotator());
	}
	else
	{
		CurrentDistance = 0.f;
		FlySpeed = 0.f;
		OnEffectArrived.Broadcast();
		//到达了，设置位置到TargetPos
		SetActorLocationAndRotation(TargetPos, FRotationMatrix::MakeFromX(Direction).Rotator());
	}
}

void ABeamEffectEmitter::SetComponentTransform()
{
	SCOPE_CYCLE_COUNTER(STAT_SetComponentTransform);

	FVector TargetPoint;
	GetParticleSystemComponent()->GetBeamTargetPoint(0, 0, TargetPoint);

	FVector SourcePoint;
	GetParticleSystemComponent()->GetBeamSourcePoint(0, 0, SourcePoint);

	STComponent->SetWorldLocation((TargetPoint + SourcePoint) / 2);
	STComponent->SetWorldRotation(FRotationMatrix::MakeFromX(TargetPoint - SourcePoint).Rotator());
	FVector Scale = STComponent->GetComponentScale();
	STComponent->SetWorldScale3D(FVector((TargetPoint - SourcePoint).Size() / 100.f, Scale.Y, Scale.Z));
}


void ABeamEffectEmitter::OnEmitterCollisionBegin(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (BeamCollisionList.Contains(Other))
	{
		if (!BeamCollisionList[Other].bOverlap)
		{
			Super::OnEmitterCollisionBegin(OverlappedComp, Other, OtherComp, OtherBodyIndex, bFromSweep, SweepResult);
			BeamCollisionList[Other].bOverlap = true;
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Beam Collision : Actor named %s"), *Other->GetName());
		}
	}
	else
	{
		BeamCollisionList.Add(Other, Data(true, 0.0f));
		Super::OnEmitterCollisionBegin(OverlappedComp, Other, OtherComp, OtherBodyIndex, bFromSweep, SweepResult);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Beam Collision : Actor named %s"), *Other->GetName());
	}
}

void ABeamEffectEmitter::UpdateBeamCollisionList(float DeltaTime)
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateBeamCollisionList);

	for (auto it = BeamCollisionList.CreateIterator(); it; ++it)
	{
		if (IsValid(it.Key()))
		{
			if (it.Value().bOverlap)
			{
				it.Value().Time += DeltaTime;

				if (it.Value().Time >= 1.0f)
				{
					it.Value().Time = 0.0f;
					it.Value().bOverlap = false;
					it.RemoveCurrent();
				}
			}
		}
		else
		{
			it.RemoveCurrent();
		}
	}
}

void ABeamEffectEmitter::Tick(float DeltaTime)
{
	AEffectEmitter::Tick(DeltaTime);

	if (bPlaying)
	{
		//更新碰撞列表
		if (STComponent && STComponent->GetStaticMesh())
		{
			UpdateBeamCollisionList(DeltaTime);
		}

		//设置起点
		SetSourcePoint();
		//设置终点
		SetTargetPoint();
		//设置目标点的切线
		SetTargetTangent();
	
		if (FlySpeed > 0.f)
		{
			///更新要移动的长度
			CurrentDistance += DeltaTime * FlySpeed;
			//移动
			Move();
		}

		if (STComponent && STComponent->GetStaticMesh() && !EffectData->BeamData.IsBendFromTarget)
		{
			SetComponentTransform();
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END

