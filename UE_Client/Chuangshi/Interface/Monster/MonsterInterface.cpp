// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterInterface.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Kismet/KismetMathLibrary.h"
#include "Manager/CustomTimerManager.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/FightComponent.h"
#include "Components/CapsuleComponent.h"
#include "Manager/ParticleManager.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Manager/ShapeManager.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "GameData/GameDeFine.h"
#include <stdlib.h>
#include "Component/Monster/CMonsterPosSyncComponent.h"
#include "Interface/StateInterface.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


UMonsterInterface::UMonsterInterface()
{
}

UMonsterInterface::~UMonsterInterface()
{

}


void UMonsterInterface::CLIENT_PlayAdmissionAction(const FString& ActionId)
{
	if (IsValid(GetActor()))
	{
		AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
		if (!IsValid(MonsterActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::CLIENT_PlayAdmissionAction : MonsterActor!"));
			return;
		}
		MonsterActor->PlayAdmissionAction(FSTRING_TO_FNAME(ActionId));
	}
}

void UMonsterInterface::CLIENT_ShowSpecialProgress_Implementation(const FString& Text, const float& PersistTime, const FString& iconName)
{
	if (IsValid(GetActor()))
	{
		AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
		if (!IsValid(MonsterActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::CLIENT_ShowSpecialProgress_Implementation : MonsterActor!"));
			return;
		}
		MonsterActor->OnShowSpecialProgressBP(Text, PersistTime, iconName);
	}
}

void UMonsterInterface::CLIENT_HideSpecialProgress_Implementation()
{
	if (IsValid(GetActor()))
	{
		AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
		if (!IsValid(MonsterActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::CLIENT_HideSpecialProgress_Implementation : MonsterActor!"));
			return;
		}
		MonsterActor->OnHideSpecialProgressBP();
	}
}

void UMonsterInterface::CLIENT_AddClientAttackTrap(const int32& Shape, const FString& Range, const float& Height)
{
	if (!IsValid(GetActor())) return;

	switch (Shape)
	{
	case 1:
		pAttackShape = CreateCylinderShape(1, Range, Height);
		break;
	case 2:
		pAttackShape = CreateBoxShape(1, Range, Height);
		break;
	case 3:
		pAttackShape = CreateSphereShape(1, Range, Height);
		break;
	default:
		return;
	}
}

void UMonsterInterface::CLIENT_CancelClientAttackTrap()
{
	if (IsValid(pAttackShape))
	{
		pAttackShape->DestoryShape();
		pAttackShape = nullptr;
	}
}

void UMonsterInterface::CLIENT_AddClientInitiativeTrap(const int32& Shape, const FString& ShapeParams, const float& Height)
{
	if (IsValid(pInitiativeShape))
	{
		return;
	}
	if (!IsValid(GetActor())) return;

	switch (Shape)
	{
	case 1:
		pInitiativeShape = CreateCylinderShape(2, ShapeParams, Height);
		break;
	case 2:
		pInitiativeShape = CreateBoxShape(2, ShapeParams, Height);
		break;
	case 3:
		pInitiativeShape = CreateSphereShape(2, ShapeParams, Height);
		break;
	case 4:
		pInitiativeShape = CreateSectorShape(2, ShapeParams, Height);
	default:
		return;
	}
}

void UMonsterInterface::CLIENT_CancelClientInitiativeTrap()
{
	if (IsValid(pInitiativeShape))
	{
		pInitiativeShape->DestoryShape();
		pInitiativeShape = nullptr;
	}


	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(MonsterTrapEffectUID);

}

UBaseShape* UMonsterInterface::CreateBoxShape(int Type, const FString& ShapeParams, const float& Height)
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return nullptr;
	}
	TArray<FString> params = UGolbalBPFunctionLibrary::SplitString(ShapeParams, false, TEXT("|"));
	FVector shapeVector = FVector::ZeroVector;
	if (params.Num() >= 2)
	{
		shapeVector = FVector(FSTRING_TO_FLOAT(params[0]), FSTRING_TO_FLOAT(params[1]), Height);
	}
	else
	{
		shapeVector = FVector(FSTRING_TO_FLOAT(params[0]), FSTRING_TO_FLOAT(params[0]), Height);
	}
	
	if (Type == 1)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::BOX, shapeVector, &UMonsterInterface::OnPlayerEnterAttackRange, &UMonsterInterface::OnPlayerLeaveAttackRange);
	}
	else if (Type == 2)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::BOX, shapeVector, &UMonsterInterface::OnPlayerEnterInitiativeRange, &UMonsterInterface::OnPlayerLeaveInitiativeRange);
	}
	return nullptr;
}
UBaseShape* UMonsterInterface::CreateSphereShape(int Type, const FString& Range, const float& Height)
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return nullptr;
	}

	FVector shapeVector = FVector(FSTRING_TO_FLOAT(Range), FSTRING_TO_FLOAT(Range), Height);
	if (Type == 1)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SHPERE, shapeVector, &UMonsterInterface::OnPlayerEnterAttackRange, &UMonsterInterface::OnPlayerLeaveAttackRange);
	}
	else if (Type == 2)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SHPERE, shapeVector, &UMonsterInterface::OnPlayerEnterInitiativeRange, &UMonsterInterface::OnPlayerLeaveInitiativeRange);
	}
	return nullptr;
}
UBaseShape* UMonsterInterface::CreateCylinderShape(int Type, const FString& Range, const float& Height)
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return nullptr;
	}

	FVector shapeVector = FVector(FSTRING_TO_FLOAT(Range), FSTRING_TO_FLOAT(Range), Height);
	if (Type == 1)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::CYLINDER, shapeVector, &UMonsterInterface::OnPlayerEnterAttackRange, &UMonsterInterface::OnPlayerLeaveAttackRange);
	}
	else if (Type == 2)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::CYLINDER, shapeVector, &UMonsterInterface::OnPlayerEnterInitiativeRange, &UMonsterInterface::OnPlayerLeaveInitiativeRange);
	}
	return nullptr;

}
UBaseShape* UMonsterInterface::CreateSectorShape(int Type, const FString& ShapeParams, const float& Height)
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return nullptr;
	}
	TArray<FString> params = UGolbalBPFunctionLibrary::SplitString(ShapeParams, false, TEXT("|"));
	if (params.Num() < 2)
	{
		return nullptr;
	}
	FVector shapeVector = FVector(FSTRING_TO_FLOAT(params[0]), FSTRING_TO_FLOAT(params[1]), Height);
	if (Type == 1)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SECTOR, shapeVector, &UMonsterInterface::OnPlayerEnterAttackRange, &UMonsterInterface::OnPlayerLeaveAttackRange);
	}
	else if (Type == 2)
	{
		return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SECTOR, shapeVector, &UMonsterInterface::OnPlayerEnterInitiativeRange, &UMonsterInterface::OnPlayerLeaveInitiativeRange);
	}
	return nullptr;
}

void UMonsterInterface::OnPlayerEnterAttackRange()
{
	int playerID = UGolbalBPFunctionLibrary::GetPlayerID();
	OnEnterAttackRange(playerID);
}

void UMonsterInterface::OnPlayerLeaveAttackRange()
{
	int playerID = UGolbalBPFunctionLibrary::GetPlayerID();
	OnLeaveAttackRange(playerID);
}

void UMonsterInterface::OnPlayerEnterInitiativeRange()
{
	int playerID = UGolbalBPFunctionLibrary::GetPlayerID();
	OnEnterInitiativeRange(playerID);
}

void UMonsterInterface::OnPlayerLeaveInitiativeRange()
{
	int playerID = UGolbalBPFunctionLibrary::GetPlayerID();
	OnLeaveInitiativeRange(playerID);
}



void UMonsterInterface::OnEnterAttackRange(int32 EID)
{
	RPC_CELL_onClientEnterAIAttackTrap(EID);
}

void UMonsterInterface::RPC_CELL_onClientEnterAIAttackTrap(int32 EID)
{
	KBEngine::FVariantArray Args;
	Args.Add(EID);
	if (this->GetEntity() == nullptr)
	{
		CS3_Warning(TEXT(" -- UMonsterInterface::OnEnterAttackRangeno this Entity! %d"), EntityID);
		return;
	}
	this->GetEntity()->CellCall(TEXT("CELL_onClientEnterAIAttackTrap"), Args);
}

void UMonsterInterface::RPC_CELL_onClientLeaveAIAttackTrap(int32 EID)
{
	if (GetEntity())
	{
		KBEngine::FVariantArray Args;
		Args.Add(EID);
		GetEntity()->CellCall(TEXT("CELL_onClientLeaveAIAttackTrap"), Args);
	}
}

void UMonsterInterface::OnLeaveAttackRange(int32 EID)
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(PlayerActor))
	{
		auto PlayerEntity = PlayerActor->GetSelfEntity();

		if (nullptr != PlayerEntity)
		{
			RPC_CELL_onClientLeaveAIAttackTrap(EID);
		}
	}
}

void UMonsterInterface::RPC_CELL_onClientEnterInitiativeTrap(int32 EID)
{
	KBEngine::FVariantArray Args;
	Args.Add(EID);
	if (this->GetEntity())
	{
		this->GetEntity()->CellCall(TEXT("CELL_onClientEnterInitiativeTrap"), Args);
	}
}

void UMonsterInterface::OnEnterInitiativeRange(int32 EID)
{
	RPC_CELL_onClientEnterInitiativeTrap(EID);
}

void UMonsterInterface::RPC_CELL_onClientLeaveInitiativeTrap(int32 EID)
{
	KBEngine::FVariantArray Args;
	Args.Add(EID);
	if (this->GetEntity())
	{
		this->GetEntity()->CellCall(TEXT("CELL_onClientLeaveInitiativeTrap"), Args);
	}
}

void UMonsterInterface::OnLeaveInitiativeRange(int32 EID)
{
	RPC_CELL_onClientLeaveInitiativeTrap(EID);
}

void UMonsterInterface::CLIENT_PlayerReTriggerTrap()
{
	if (IsValid(pInitiativeShape))
	{
		pInitiativeShape->Reset();
	}
	if (IsValid(pAttackShape))
	{
		pAttackShape->Reset();
	}
}

void UMonsterInterface::CLIENT_CreateFightArea_Implementation()
{
	if (IsValid(GetActor()))
	{
		AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
		if (MonsterActor && this->GetEntity())
		{
			MonsterActor->FightComponent->OnCreateFightArea.Broadcast(this->GetEntity()->GetDefinedProperty(TEXT("scriptID")), AREA_LIGHT_WALL_TYPE_ENUM::BossLightWall);
		}
	}
}

void UMonsterInterface::CLIENT_OnLeaveFightArea_Implementation()
{
	if (IsValid(GetActor()))
	{
		AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
		if (MonsterActor && this->GetEntity())
		{
			MonsterActor->OnLeaveFightAreaBP();
		}
	}
}

void UMonsterInterface::CLIENT_OpenInitiactiveTrapEffect_Implementation(const int32& Shape, const FString& ShapeParams, const float& Height)
{
	if (!IsValid(GetActor())) return;

	//if (MonsterTrapIsValid(Effect))
	//	MonsterTrapEffect->Stop();
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(MonsterTrapEffectUID);

	if (Shape == 1)	///圆柱形
	{
		float Range = FSTRING_TO_FLOAT(ShapeParams);
		FString EffectID = "Cylinder_360";
		MonsterTrapEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.f, GetActor(), GetActor(), FEffectCreate::CreateLambda([Range](int32 UID)
		{
			AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
			if (Effect)
			{
				Effect->SetActorScale3D(FVector(Range));
			}
		}));
	}
	else if (Shape == 4)	///扇形
	{
		TArray<FString> params = UGolbalBPFunctionLibrary::SplitString(ShapeParams, false, TEXT("|"));
		FString EffectID = "Sector_";
		EffectID.Append(params[1]);
		EffectID.Append("_1");
		float Range = FSTRING_TO_FLOAT(params[0]);
		MonsterTrapEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.f, GetActor(), GetActor(), FEffectCreate::CreateLambda([Range](int32 UID)
		{
			AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
			if (Effect)
			{
				Effect->SetActorScale3D(FVector(Range));
			}
		}));
	}
	else if (Shape == 2)
	{
		float Range = FSTRING_TO_FLOAT(ShapeParams);
		FString EffectID = TEXT("Box_1");
		MonsterTrapEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.f, GetActor(), GetActor(), FEffectCreate::CreateLambda([Range](int32 UID)
		{
			AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
			if (Effect)
			{
				Effect->SetActorScale3D(FVector(Range * 2));
			}
		}));
	}
}

void UMonsterInterface::CLIENT_CloseInitiactiveTrapEffect_Implementation()
{
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(MonsterTrapEffectUID);
}

void UMonsterInterface::CLIENT_SimulationCircle_Implementation(const float & hornSpeed, int32 targetID)
{
	if (isTurning)
	{
		return;
	}

	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
	if (MonsterCharacter && MonsterCharacter->GetSelfEntity())
	{
		KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(targetID);
		if (TargetEntity && TargetEntity->Actor())
		{
			FRotator LookAtRotation = UKismetMathLibrary::FindLookAtRotation(GetActor()->GetActorLocation(), TargetEntity->Actor()->GetActorLocation());

			if (FMath::Abs(GetActor()->GetActorRotation().Yaw - LookAtRotation.Yaw) < 1.0f)
			{
				return;
			}

			isTurning = true;

			TWeakObjectPtr<UMonsterInterface> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TurnTimer, FTimerDelegate::CreateLambda([DelayThisPtr, hornSpeed, targetID]()
			{
				if (DelayThisPtr.IsValid())
				{
					UMonsterInterface* ThisPtr = DelayThisPtr.Get();
					KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(targetID);
					if (TargetEntity == nullptr || !IsValid(TargetEntity->Actor()) || !IsValid(ThisPtr->GetActor()))
					{
						ThisPtr->isTurning = false;
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->TurnTimer);
						return;
					}
					//朝向
					FRotator LookAtRotation = UKismetMathLibrary::FindLookAtRotation(ThisPtr->GetActor()->GetActorLocation(), TargetEntity->Actor()->GetActorLocation());
					//选择选择方向
					float DifferenceYaw = LookAtRotation.Yaw - ThisPtr->GetActor()->GetActorRotation().Yaw;
					DifferenceYaw < -180 ? DifferenceYaw += 360 : (DifferenceYaw > 180 ? DifferenceYaw -= 360 : DifferenceYaw);
					int Direction = DifferenceYaw > 0 ? 1 : -1;
					//旋转
					ThisPtr->GetActor()->AddActorWorldRotation(FRotator(0, Direction * FMath::RadiansToDegrees(hornSpeed) / 20, 0));
					if (FMath::Abs(ThisPtr->GetActor()->GetActorRotation().Yaw - LookAtRotation.Yaw) < (FMath::RadiansToDegrees(hornSpeed) / 20))
					{
						ThisPtr->GetActor()->SetActorRotation(FRotator(0, LookAtRotation.Yaw, 0));
						ThisPtr->isTurning = false;
						ThisPtr->RPC_CELL_notifyChangeMonsterDirection(FLOAT_TO_FSTRING(ThisPtr->GetActor()->GetActorRotation().Yaw));
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->TurnTimer);
					}
				}
			}), 0.05f, true);
		}
		else
		{
			isTurning = false;
		}
	}
	else
	{
		isTurning = false;
	}
}

void UMonsterInterface::RPC_CELL_notifyChangeMonsterDirection(FString yaw)
{
	KBEngine::Entity* entity = GetEntity();
	if (!entity)
	{
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(yaw);
	entity->CellCall(TEXT("CELL_notifyChangeMonsterDirection"), Args);
}

void UMonsterInterface::CLIENT_StopSimulationCircle_Implementation()
{
	isTurning = false;
	RPC_CELL_notifyChangeMonsterDirection(FLOAT_TO_FSTRING(GetActor()->GetActorRotation().Yaw));
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TurnTimer);
}

void UMonsterInterface::CLIENT_FaceToPlayer_Implementation(bool State)
{
	if (!GetActor())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::CLIENT_FaceToPlayer_Implementation : GetActor()!"));
		return;
	}

	if (State)
	{
		if (isLookAt)
		{
			return;
		}

		isLookAt = true;

		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, LookAtTimer, FTimerDelegate::CreateLambda([this]()
		{
			UStateInterface* StateInterface = Cast<UStateInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("StateInterface"), EntityID));
			if (StateInterface && StateInterface->IsHasEffectStates())
			{
				isLookAt = false;
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LookAtTimer);
				return;
			}
			AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
			if (MonsterCharacter && MonsterCharacter->GetSelfEntity())
			{
				KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(MonsterCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("TargetID")));
				if (TargetEntity && TargetEntity->Actor())
				{
					FRotator LookAtRotation = UKismetMathLibrary::FindLookAtRotation(GetActor()->GetActorLocation(), TargetEntity->Actor()->GetActorLocation());
					GetActor()->SetActorRotation(FRotator(0, LookAtRotation.Yaw, 0));
					return;
				}
			}

			CS3_Display(CS3DebugType::CL_Undefined, TEXT("The monster hasn't target entity , please check server code"));

			isLookAt = false;
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LookAtTimer);

		}), GetActor()->GetWorld()->GetDeltaSeconds() / 2, true);
	}
	else
	{
		if (!isLookAt)
		{
			return;
		}
		isLookAt = false;

		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LookAtTimer);
	}

}


void UMonsterInterface::CLIENT_onPlaySpeechBubbles_Implementation(const FString & voiceID)
{
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->PlaySpeechBubble(voiceID);
	}
}

void UMonsterInterface::CLIENT_addMonsterBlow(const FVector & WindDir, const float & WindSpeed)
{
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(Character))
	{
		FVector WindDirection = UKismetMathLibrary::CreateVectorFromYawPitch(WindDir.Z, WindDir.Y);
		WindDirection.Normalize();

		Character->ChangeBlowFilter(WindDirection, WindSpeed);
	}
}

void UMonsterInterface::CLIENT_endMonsterBlow()
{
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->EndBlow();
	}
}

void UMonsterInterface::RPC_CELL_onClientLeaveAIBattleRegion()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_onClientLeaveAIBattleRegion : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_onClientLeaveAIBattleRegion"), args);
}

void UMonsterInterface::OnRep_moveScriptID()
{
	if (IsValid(GetActor()) && GetEntity() != nullptr)
	{
		uint16 moveScriptID = GetEntity()->GetDefinedProperty(TEXT("moveScriptID")).GetValue<uint16>();
		int32 targetID = GetEntity()->GetDefinedProperty(TEXT("targetID")).GetValue<int32>();
		if (moveScriptID == uint16(MOVETYPE::MOVETYPE_CHASE_CLIENT) && targetID != 0)
		{
			chaseEntityID = targetID;
			StartClientChase();
		}
		else
		{
			StopClientChase();
		}
	}
}

void UMonsterInterface::StartClientChase()
{
	GetMoveTargetPosStr();
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, ChaseTimerHandle,
			FTimerDelegate::CreateLambda([this]()
		{
			GetMoveTargetPosStr();
		}
		), 1.0, true);
	}
}

void UMonsterInterface::CLIENT_RemoveChasePosInfo_Implementation()
{
	//清除追击目标对自己的记录
	URolePerformanceInterface * ChaseRPInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), chaseEntityID));
	if (ChaseRPInterface)
	{
		for (auto chaseInfo : ChaseRPInterface->ChasePosInfo)
		{
			for (auto info : chaseInfo.Value)
			{
				if (info.Value == GetEntity()->ID())
				{
					ChaseRPInterface->ChasePosInfo[chaseInfo.Key][info.Key] = 0;
				}
			}
		}

		chaseEntityID = 0;
	}
}

void UMonsterInterface::ShowMonsterLocationTwinkle_Implementation(const int32& bTwinkle)
{
	if (AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor()))
	{
		MonsterCharacter->isTwinkle = bool(bTwinkle);
	}
}

void UMonsterInterface::StopClientChase()
{
	//清楚定时器
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ChaseTimerHandle);

}


void UMonsterInterface::GetMoveTargetPosStr()
{
	if (GetEntity() == nullptr)
	{
		return;
	}

	float distance = 100 * GetEntity()->GetDefinedProperty(TEXT("circleChaseDistance")).GetValue<float>();
	float angle = GetEntity()->GetDefinedProperty(TEXT("circleChaseAngle")).GetValue<float>();
	int32 targetID = GetEntity()->GetDefinedProperty(TEXT("targetID")).GetValue<int32>();
	if (targetID == 0 || chaseEntityID == 0 || angle == 0)
	{
		return;
	}
	else if (targetID != chaseEntityID)
	{
		URolePerformanceInterface * ChaseRPInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), chaseEntityID));
		if (IsValid(ChaseRPInterface))
		{
			for (auto chaseInfo : ChaseRPInterface->ChasePosInfo)
			{
				for (auto info : chaseInfo.Value)
				{
					if (info.Value == GetEntity()->ID())
					{
						//info.Value = 0;
						ChaseRPInterface->ChasePosInfo[chaseInfo.Key][info.Key] = 0;
					}
				}
			}
		}
		chaseEntityID = targetID;
	}
	KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(targetID);

	if (TargetEntity && TargetEntity->Actor())
	{
		URolePerformanceInterface * RPInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), targetID));
		if (!RPInterface)
		{
			return;
		}
		FVector targetPos = TargetEntity->LocalPosition();
		FVector selfPos = GetEntity()->LocalPosition();

		TMap<float, int> tempInfo;
		float distanceExt = 1.0 * 100;
		//首先判断是否有位置记录
		//如果有判断是否能往前补位，不能补位则用记录中的位置继续移动
		//如果没有记录，分配一个新的位置

		float distValue = 0;				//补位层的距离 选择距离目标最近的有空位的一层为补位层
		TArray<float> anglesTArray;			//补位层的空余位置角度
		float distRec = 0, angleRec = 0;	//当前记录的位置
		bool bValue = false;				//是否存在记录
		//获取位置记录
		for (auto chasePosInfo : RPInterface->ChasePosInfo)
		{
			if (bValue) { break; }
			float _dist = chasePosInfo.Key;
			for (auto info : chasePosInfo.Value)
			{
				float _angle = info.Key;
				int32 ID = info.Value;
				if (ID == GetEntity()->ID())
				{
					distRec = _dist;
					angleRec = _angle;
					bValue = true;
					break;
				}
			}
		}

		//如果有判断是否能往前补位，可以则记录新的位置，清除原先的记录，不能补位则用记录中的位置继续移动
		float _dist = distance;
		while (true)
		{
			//寻找前排空位
			//如果没有指定层信息，新生成一个层
			if (!RPInterface->ChasePosInfo.Contains(_dist))
			{
				TMap<float, int> info;
				for (int i = 0; i < 360; i = i + angle)
				{
					info.Add(float(i), 0);
				}
				RPInterface->ChasePosInfo.Add(_dist, info);
			}

			for (auto info : RPInterface->ChasePosInfo[_dist])
			{
				float _angle = info.Key;
				int ID = info.Value;

				if (ID == 0 || ID == GetEntity()->ID() && (int(_angle) % int(angle)) == 0)
				{
					distValue = _dist;
					anglesTArray.Add(_angle);
				}
			}

			if (anglesTArray.Num())
			{
				break;
			}
			else
			{
				_dist += distanceExt;
			}
		}

		FVector pos;
		float minDis = 100000.0;
		float tempAngle = 0.0;
		FVector tempPos;
		for (auto it_angle : anglesTArray)
		{
			//避免怪物僵住不动给个偏差值
			int theta = (rand() % 2) * 10 - 5;
			float Angle = (it_angle + theta) / 180 * PI;
			tempPos.X = distValue * cos(Angle) + targetPos.X;
			tempPos.Y = distValue * sin(Angle) + targetPos.Y;
			tempPos.Z = targetPos.Z;
			if (minDis >= FVector::Dist2D(selfPos, tempPos))
			{
				minDis = FVector::Dist2D(selfPos, tempPos);
				tempAngle = it_angle;
				pos = tempPos;
			}
		}
		if (bValue)
		{
			RPInterface->ChasePosInfo[distRec][angleRec] = 0;
		}

		RPInterface->ChasePosInfo[distValue][tempAngle] = GetEntity()->ID();

		FString posStr = FLOAT_TO_FSTRING(pos.Y / 100.0) + TEXT("|") + FLOAT_TO_FSTRING(pos.Z / 100.0) + TEXT("|") + FLOAT_TO_FSTRING(pos.X / 100.0);
		RPC_CELL_updateMoveTargetPosFromClient(posStr);
		return;
	}
	else
	{
		StopClientChase();
	}

}

void UMonsterInterface::RPC_CELL_updateMoveTargetPosFromClient(FString posStr)
{
	KBEngine::FVariantArray Args;
	Args.Add(posStr);
	if (this->GetEntity())
	{
		this->GetEntity()->CellCall(TEXT("CELL_updateMoveTargetPosFromClient"), Args);
	}
	return;
}

void UMonsterInterface::RPC_CELL_onAttackTarget()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_onAttackTarget : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_onAttackTarget"), args);
}

void UMonsterInterface::RPC_CELL_onSetControlledBy()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_onSetControlledBy : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_onSetControlledBy"), args);
}

void UMonsterInterface::RPC_CELL_startFalling()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_startFalling : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_startFalling"), args);
}

void UMonsterInterface::RPC_onClickCallBack()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_onClickCallBack : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onClickCallBack"), args);
}

void UMonsterInterface::RPC_CELL_OnPlayAdmissionAction()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_OnPlayAdmissionAction : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("CELL_OnPlayAdmissionAction"), args);
}

void UMonsterInterface::RPC_CELL_ChangeMonsterParent(KBEngine::FVariantArray Args)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_ChangeMonsterParent : entity!"));
		return;
	}
	entity->CellCall(TEXT("CELL_ChangeMonsterParent"), Args);
}

void UMonsterInterface::RPC_CELL_OnPlayerBeginPush()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_OnPlayerBeginPush : entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	entity->CellCall(TEXT("CELL_OnPlayerBeginPush"), Args);
}

void UMonsterInterface::RPC_CELL_OnPlayerEndPush()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_OnPlayerEndPush : entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	entity->CellCall(TEXT("CELL_OnPlayerEndPush"), Args);
}

void UMonsterInterface::NotifyMonsterEndFallLand()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::NotifyMonsterEndFallLand : entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	entity->CellCall(TEXT("notifyMonsterEndFallLand"), Args);
}

void UMonsterInterface::CLIENT_DisplayCounodwn_Implementation(const FString& endReviveTime)
{

}

//----------------------test-------------------------------------
void UMonsterInterface::RandomMove_Implementation(float range) {
	if (IsValid(GetActor())) {
		AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
		if (IsValid(MonsterCharacter)) {
			UCMonsterPosSyncComponent* CMonsterPosSyncComponent = Cast<UCMonsterPosSyncComponent>(MonsterCharacter->GetFilterComponent());
			if (CMonsterPosSyncComponent) {
				CMonsterPosSyncComponent->StartRandomWalk(MonsterCharacter->GetActorLocation(), range);
			}
		}
	}
}

void UMonsterInterface::ChaseActor_Implementation(int32 targetID) {
	AActor* Actor = UGolbalBPFunctionLibrary::GetActorByID(targetID);
	if (!IsValid(Actor) || !IsValid(GetActor())) {
		return;
	}
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(MonsterCharacter)) {
		UCMonsterPosSyncComponent* CMonsterPosSyncComponent = Cast<UCMonsterPosSyncComponent>(MonsterCharacter->GetFilterComponent());
		if (CMonsterPosSyncComponent) {
			CMonsterPosSyncComponent->ChaseActor(Actor);
		}
	}
}

void UMonsterInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OpenInitiactiveTrapEffect");
	ArrBlueFunc.Add("CLIENT_CloseInitiactiveTrapEffect");
	ArrBlueFunc.Add("CLIENT_PlayAdmissionAction");
	ArrBlueFunc.Add("CLIENT_ShowSpecialProgress");
	ArrBlueFunc.Add("CLIENT_HideSpecialProgress");
	ArrBlueFunc.Add("CLIENT_AddClientAttackTrap");
	ArrBlueFunc.Add("CLIENT_CancelClientAttackTrap");
	ArrBlueFunc.Add("CLIENT_AddClientInitiativeTrap");
	ArrBlueFunc.Add("CLIENT_CancelClientInitiativeTrap");
	ArrBlueFunc.Add("CLIENT_CreateFightArea");
	ArrBlueFunc.Add("CLIENT_OnLeaveFightArea");
	ArrBlueFunc.Add("CLIENT_PlayerReTriggerTrap");
	ArrBlueFunc.Add("CLIENT_SimulationCircle");
	ArrBlueFunc.Add("CLIENT_StopSimulationCircle");
	ArrBlueFunc.Add("CLIENT_FaceToPlayer");
	ArrBlueFunc.Add("CLIENT_onPlaySpeechBubbles");
	ArrBlueFunc.Add("CLIENT_RemoveChasePosInfo");
	ArrBlueFunc.Add("ShowMonsterLocationTwinkle");
	ArrBlueFunc.Add("CLIENT_DisplayCounodwn");
	ArrBlueFunc.Add("CLIENT_addMonsterBlow");
	ArrBlueFunc.Add("CLIENT_endMonsterBlow");
	ArrBlueFunc.Add("RandomMove");
	ArrBlueFunc.Add("ChaseActor");
	Supper::InitBlueCB();
}
