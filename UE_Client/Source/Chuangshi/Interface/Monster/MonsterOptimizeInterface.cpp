// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterOptimizeInterface.h"
#include "Runtime/NavigationSystem/Public/NavigationSystem.h"
#include "Runtime/NavigationSystem/Public/NavigationPath.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"

#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"

#include "Actor/ServerCharacter.h"
#include "MonsterAI/MonsterCommonController.h"
#include "kbengine.h"
#include "KBEMath.h"
#include "Util/GlobalFunctions.h"
#include "CS3Base/CS3Entity.h"
#include "Manager/CustomTimerManager.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/Monster/MonsterOptimizeComponent.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "BehaviourInterface.h"

CONTROL_COMPILE_OPTIMIZE_START


CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterOptimizeInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(movingToPointReady, &UMonsterOptimizeInterface::movingToPointReady, const uint64&, const FVector&, const float& )
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterOptimizeInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(clientMovingID, &UMonsterOptimizeInterface::Set_clientMovingID, uint64)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(clientMovingPathPoints, &UMonsterOptimizeInterface::Set_clientMovingPathPoints, KBEngine::FVariantArray)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(clientMovingPathIdx, &UMonsterOptimizeInterface::Set_clientMovingPathIdx, uint8)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(clientMovingToEntityID, &UMonsterOptimizeInterface::Set_clientMovingToEntityID, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(clientMovingToEntityDis, &UMonsterOptimizeInterface::Set_clientMovingToEntityDis, float)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(moveScriptID, &UMonsterOptimizeInterface::Set_moveScriptID, uint16)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(useRVOAvoidance, &UMonsterOptimizeInterface::Set_useRVOAvoidance, uint8)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(rvoRadius, &UMonsterOptimizeInterface::Set_rvoRadius, float)
CS3_END_INTERFACE_PROPERTY_MAP()



UMonsterOptimizeInterface::UMonsterOptimizeInterface()
{
	movingToEntityDistance = 100.0;
}

UMonsterOptimizeInterface::~UMonsterOptimizeInterface()
{
	
}


void UMonsterOptimizeInterface::Set_Position(const FVector &oldVal)
{
	KBEngine::Entity* e = GetEntity();
	clientMovingTempUp = false;
	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (IsValid(Character))
	{
		if (FVector::Distance(Character->GetActorLocation(), e->Position()) > 100.0)
			Character->SetActorLocation(e->Position());
	}
}

void UMonsterOptimizeInterface::OnMoveOver(const uint32 movingID, const bool isSuccess)
{
	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (IsValid(Character))
	{
		if (
			clientMovingPathPoints.Num() > clientMovingPathIdx &&
			FVector::Distance(Character->GetActorLocation(), clientMovingPathPoints[clientMovingPathIdx]) < 100.0f
			)
		{
			moveToPathStepOver();
		}

	}
}

void UMonsterOptimizeInterface::Set_clientMovingID(const uint64& newVal, const uint64& oldVal)
{
	clientMovingID = newVal;
}

void UMonsterOptimizeInterface::movingToPointReady(const uint64& movingID, const FVector& targetPos, const float& pointMaxDis )
{
	//FVector curPos = LocalPosition();
	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (!IsValid(Character))
	{
		return;
	}
	//如果开启普通移动，先停掉跟随

	FVector gotoPos = FVector(targetPos.Z, targetPos.X, targetPos.Y) * 100.0;
	FVector floorTargetPos = Character->FloorTrace(gotoPos);

	KBEngine::FVariantArray args;
	float c_pointMaxDis = pointMaxDis * 100;
	KBEngine::FVariantArray serverPosList;

	const UNavigationSystemV1 *navSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(Character->GetWorld());
	const UNavigationPath *navPath = navSys->FindPathToLocationSynchronously(Character->GetWorld(), Character->GetActorLocation(), floorTargetPos, Character->GetWorld()->GetFirstPlayerController());
	if ( navSys != nullptr && navPath && !navPath->IsPartial() && navPath->PathPoints.Num() > 0)
	{
		FVector prev_pos = navPath->PathPoints[0];
		for (FVector pos : navPath->PathPoints)
		{
			if (FVector::Distance(prev_pos, pos) < c_pointMaxDis)
			{
				serverPosList.Add(KBEngine::KBEMath::Unreal2KBEnginePosition(pos));
			}
			else
			{
				FVector t_dir = pos - prev_pos;
				t_dir.Normalize();
				while (FVector::Distance(prev_pos, pos) > c_pointMaxDis )
				{
					prev_pos = prev_pos + t_dir * c_pointMaxDis;
					serverPosList.Add(KBEngine::KBEMath::Unreal2KBEnginePosition( prev_pos ));
				}

				serverPosList.Add(KBEngine::KBEMath::Unreal2KBEnginePosition(pos));
			}
			prev_pos = pos;
		}
	}
	args.Add(movingID);
	args.Add(serverPosList);
	CellCall(TEXT("clientMovingPointReadyCB"), args);
}

void UMonsterOptimizeInterface::Set_clientMovingPathPoints(const  KBEngine::FVariantArray& newVal, const  KBEngine::FVariantArray& oldVal)
{
	clientMovingPathPoints.Empty();
	for (auto &it : newVal)
	{
		FVector t_pos = it.GetValue<FVector>();
		//换成虚幻坐标，加入列表
		clientMovingPathPoints.Add(KBEngine::KBEMath::KBEngine2UnrealPosition(t_pos));
	}
	//如果有坐标
	if (clientMovingPathPoints.Num())
	{
		moveToPathPoints();
		UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;

		if (!IsValid(TimeMgr))
		{
			return;
		}

		if (moveToPathHandle.IsValid())
		{
			TimeMgr->ClearTimer(moveToPathHandle);
		}
		//if (movingToEntityHandle.IsValid())
		//{
		//	TimeMgr->ClearTimer(movingToEntityHandle);
		//}
		//AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
		//if (IsValid(Character))
		//{
		//	UBehaviourInterface* BehaviourInterface = Cast<UBehaviourInterface>(Character->GetInterfaceByName(TEXT("BehaviourInterface")));
		//	if (IsValid(BehaviourInterface) && BehaviourInterface->GetIsUsingSkill())
		//	{
		//		return;
		//	}
		//}
		TimeMgr->SetTimer(moveToPathHandle, this, &UMonsterOptimizeInterface::moveToPathTick, 1.0, true, 0.0);
		clientMovingTempUp = true;
	}
	else
	{
		UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
		if (IsValid(TimeMgr) && moveToPathHandle.IsValid())
		{
			TimeMgr->ClearTimer(moveToPathHandle);
		}
	}
}

void UMonsterOptimizeInterface::Set_clientMovingPathIdx(const uint8& newVal, const uint8& oldVal)
{
	if (clientMovingPathPoints.Num())
	{
		clientMovingTempUp = false;
		clientMovingPathIdx = newVal;
		moveToPathStep();
	}
}


void UMonsterOptimizeInterface::moveToPathPoints()
{
	moveToPathStep();
}



void UMonsterOptimizeInterface::moveToPathStep()
{
	AServerCharacter* characterPtr = Cast<AServerCharacter>(GetActor());
	if (IsValid(characterPtr) && clientMovingPathPoints.Num() > clientMovingPathIdx)
	{
		AMonsterCommonController* controllerPtr = Cast< AMonsterCommonController >(characterPtr->GetController());
		if (IsValid(controllerPtr))
		{
			//UAIBlueprintHelperLibrary::SimpleMoveToLocation(controllerPtr, clientMovingPathPoints[clientMovingPathIdx]);
			controllerPtr->MoveToLocation(clientMovingPathPoints[clientMovingPathIdx]);
		}
	}
}

void UMonsterOptimizeInterface::moveToPathStepOver()
{
	KBEngine::FVariantArray args;
	args.Add(clientMovingPathIdx);
	CellCall(TEXT("clientMovingPointUpNodeIdx"), args);
}

void UMonsterOptimizeInterface::moveToPathTick()
{
	if (clientMovingPathPoints.Num() == 0)
	{
		UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
		if (IsValid(TimeMgr) && moveToPathHandle.IsValid())
		{
			TimeMgr->ClearTimer(moveToPathHandle);
		}

		return;
	}
	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (!IsValid(Character))
	{
		return;
	}
	if (clientMovingTempUp == true)
	{
		
		if ( clientMovingPathIdx >1 && clientMovingPathPoints.Num() > clientMovingPathIdx)
		{
			float dist_1 = FVector::Distance(Character->GetActorLocation(), clientMovingPathPoints[clientMovingPathIdx]);//当前位置到目标点
			float dist_2 = FVector::Distance(clientMovingPathPoints[clientMovingPathIdx - 1], clientMovingPathPoints[clientMovingPathIdx]); //下个点到目前点
			if (dist_1 < dist_2) //如果当前位置到目标点比两个点之间的距离近，则表示前当是靠近目标点的，进行一次更新
			{
				KBEngine::FVariantArray args;
				args.Add(KBEngine::KBEMath::Unreal2KBEnginePosition(Character->GetActorLocation()));
				CellCall(TEXT("clientMovingPointUpWait"), args);
				return;
			}
		}
		moveToPathStep();
	}
	clientMovingTempUp = true;
}


void UMonsterOptimizeInterface::Set_clientMovingToEntityID(const int32& newVal, const int32& oldVal)
{
	if (newVal == 0)
	{
		UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
		if (IsValid(TimeMgr) && movingToEntityHandle.IsValid())
		{
			TimeMgr->ClearTimer(movingToEntityHandle);
		}
	}

	CS3Entity* e = CS3::GetEntity<CS3Entity*>(newVal);
	if (e != nullptr)
	{
		movingToEntityID = newVal;
		movingToEntityStart();
	}
}

void UMonsterOptimizeInterface::Set_clientMovingToEntityDis(const float& newVal, const float& oldVal)
{
	movingToEntityDistance = newVal*100;
}

void UMonsterOptimizeInterface::Set_moveScriptID(const uint16 & newVal, const uint16 & oldVal)
{
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	moveScriptID = newVal;

	if (!IsValid(Character))
	{
		return;
	}
	
	AMonsterCommonController* controllerPtr = Cast< AMonsterCommonController >(Character->GetController());

	if (newVal == uint16( MOVETYPE::MOVETYPE_STOP) )
	{
		UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
		if (IsValid(TimeMgr))
		{
			if (moveToPathHandle.IsValid())
			{
				TimeMgr->ClearTimer(moveToPathHandle);
			}
			if (movingToEntityHandle.IsValid())
			{
				TimeMgr->ClearTimer(movingToEntityHandle);
			}
			
		}

		if (IsValid(controllerPtr))
		{
			controllerPtr->StopMovement();
		}
	}
	else if (newVal == uint16(MOVETYPE::MOVETYPE_CHASE))
	{
		if (!IsValid(Character->MonsterOptimizeComponent))
		{
			Character->MonsterOptimizeComponent = NewObject<UMonsterOptimizeComponent>(Character, "MonsterOptimizeComponent", RF_NoFlags, nullptr, false, nullptr);
		}

		if (Character->GetFilterComponent() && Character->MonsterOptimizeComponent != Character->GetFilterComponent())
		{
			Character->GetFilterComponent()->SetActiveComponentTick(false);
			Character->GetFilterComponent()->UnregisterComponent();
			Character->MonsterOptimizeComponent->RegisterComponent();
			Character->SetFilterComponent(Character->MonsterOptimizeComponent);
			Character->MonsterOptimizeComponent->InitFilter(true);
		}
	}
	else
	{
		
		if (!IsValid(Character->AvatarFilter))
		{
			Character->AvatarFilter = NewObject<UAvatarFilterActorComponent>(Character, "AvatarFilter", RF_NoFlags, nullptr, false, nullptr);
		}

		if (Character->GetFilterComponent() && Character->AvatarFilter != Character->GetFilterComponent())
		{
			Character->GetFilterComponent()->SetActiveComponentTick(false);
			Character->GetFilterComponent()->UnregisterComponent();
			Character->AvatarFilter->RegisterComponent();
			Character->SetFilterComponent(Character->AvatarFilter);
			Character->AvatarFilter->InitFilter(true);
		}
	}
}

void UMonsterOptimizeInterface::Set_useRVOAvoidance(const uint8 & newVal, const uint8 & oldVal)
{
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->GetCharacterMovement()->bUseRVOAvoidance = bool(newVal);
	}
}

void UMonsterOptimizeInterface::Set_rvoRadius(const float & newVal, const float & oldVal)
{
	if (newVal <= 0)
	{
		return;
	}
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->GetCharacterMovement()->AvoidanceConsiderationRadius = newVal;
	}
}

//开始移动
void UMonsterOptimizeInterface::movingToEntityStart()
{
	UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
	if (!IsValid(TimeMgr))
	{
		return;
	}

	//if (moveToPathHandle.IsValid())
	//{
	//	TimeMgr->ClearTimer(moveToPathHandle);
	//}
	if (movingToEntityHandle.IsValid())
	{
		TimeMgr->ClearTimer(movingToEntityHandle);
	}
	//AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	//if (IsValid(Character))
	//{
	//	UBehaviourInterface* BehaviourInterface = Cast<UBehaviourInterface>(Character->GetInterfaceByName(TEXT("BehaviourInterface")));
	//	if (IsValid(BehaviourInterface) && BehaviourInterface->GetIsUsingSkill())
	//	{
	//		return;
	//	}
	//}
	TimeMgr->SetTimer(movingToEntityHandle, this, &UMonsterOptimizeInterface::movingToEntityTick, 0.3, true, 0.0 );
}

//跟随移动心跳
void UMonsterOptimizeInterface::movingToEntityTick()
{

	AMonsterCharacter* Character = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(Character))
		return;

	if (UUECS3GameInstance::pKBEApp)
	{
		CS3Entity* movingToEntity = CS3::GetEntity<CS3Entity*>(movingToEntityID);
		if (movingToEntity == nullptr)
		{
			KBEngine::FVariantArray args;
			args.Add(clientMovingID);
			args.Add(KBEngine::KBEMath::Unreal2KBEnginePosition(Character->GetActorLocation()));
			CellCall(TEXT("clientMovingAheadOver"), args);
			UCustomTimerManager* TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
			if (!IsValid(TimeMgr))
			{
				return;
			}
			TimeMgr->ClearTimer(movingToEntityHandle);
			return;
		}

		////先给服务器更新一下自身位置
		if (UUECS3GameInstance::pKBEApp->PlayerID() == movingToEntityID || movingToEntity->IsControlled())
		{
			KBEngine::FVariantArray args;
			args.Add(KBEngine::KBEMath::Unreal2KBEnginePosition(Character->GetActorLocation()));
			CellCall(TEXT("clientMovingToEntityTickUp"), args);
		}

		AServerCharacter* followActorPtr = Cast<AServerCharacter>(movingToEntity->Actor());
		if (IsValid(followActorPtr))
		{
			AMonsterCommonController* controllerPtr = Cast< AMonsterCommonController >(Character->GetController());
			if (IsValid(controllerPtr))
			{
				float distTarget = FVector::Distance(Character->GetActorLocation(), followActorPtr->GetActorLocation());
				bool isMoverOver = abs( distTarget - movingToEntityDistance ) < 50.0; //暂时定为0.5米
				if (isMoverOver == false)
				{
					if (distTarget > movingToEntityDistance)
					{
						controllerPtr->MoveToActor(followActorPtr);
					}
					else
					{
						FVector t_dir = Character->GetActorLocation() - followActorPtr->GetActorLocation();
						t_dir.Normalize();
						FVector targetPos = Character->GetActorLocation() + t_dir * (movingToEntityDistance);
						FVector newPos;
						if (UNavigationSystemV1::NavigationRaycast(this, Character->GetActorLocation(), targetPos, newPos))
						{
							targetPos = newPos;
						}
						controllerPtr->MoveToLocation(targetPos);

					}
				}
				else
				{
					UCustomTimerManager*  TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
					if (IsValid(TimeMgr) && movingToEntityHandle.IsValid())
					{
						TimeMgr->ClearTimer(movingToEntityHandle);
					}
					controllerPtr->StopMovement();

					KBEngine::FVariantArray args;
					args.Add(clientMovingID);
					CellCall(TEXT("clientMovingOver"), args);
				}

			}
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END