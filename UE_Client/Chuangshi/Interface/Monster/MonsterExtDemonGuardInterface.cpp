// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterExtDemonGuardInterface.h"
#include "Runtime/NavigationSystem/Public/NavigationSystem.h"
#include "Runtime/NavigationSystem/Public/NavigationPath.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util//CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ShapeManager.h"
#include "Actor/ServerCharacter.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtDemonGuardInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtDemonGuardInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UMonsterExtDemonGuardInterface::CLIENT_CreateViewShapeTrap_Implementation(float Range, float Angle, float Height)
{
	pViewShape = CreateViewShape(Range, Angle, Height);
}

UBaseShape* UMonsterExtDemonGuardInterface::CreateViewShape(float Range, float Angle, float Height)
{
	AActor* AMonster = Cast<AActor>(GetActor());
	if (!IsValid(AMonster))
	{
		return nullptr;
	}
	FVector shapeVector = FVector(Range, Angle, Height);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(AMonster, this, SHAPE_TYPE::SECTOR, shapeVector, &UMonsterExtDemonGuardInterface::OnPlayerEnterViewRange, &UMonsterExtDemonGuardInterface::OnPlayerLeaveViewRange);
}


void UMonsterExtDemonGuardInterface::OnPlayerEnterViewRange()
{
	//如果玩家重新进入视野 则不移除checkViewTimerHandle
	if (delaySetViewTimerHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(delaySetViewTimerHandle);
	}

	//开启视野检测Tick
	if (!checkViewTimerHandle.IsValid())
	{
		int playerID = UGolbalBPFunctionLibrary::GetPlayerID();
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, checkViewTimerHandle,
				FTimerDelegate::CreateLambda([this, playerID]()
			{
				CheckIsInView(playerID);
			}
			), 0.1, true);
		}
	}

}

void UMonsterExtDemonGuardInterface::OnPlayerLeaveViewRange()
{
	//立即停止视野检测
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(checkViewTimerHandle);

	//玩家脱离视野两秒后 通知服务器玩家脱离视野
	if (!delaySetViewTimerHandle.IsValid())
	{

		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, delaySetViewTimerHandle,
			FTimerDelegate::CreateLambda([this]()
		{
			
			//通知服务器 玩家脱离视野
			KBEngine::FVariantArray Args;
			uint8 isPlayerInView = false;
			Args.Add(isPlayerInView);
			if (this->GetEntity())
			{
				this->GetEntity()->CellCall(TEXT("CELL_SetIsPlayerInViewRange"), Args);
			}
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(delaySetViewTimerHandle);
		}
		), 2.0, false);

	}
}



void UMonsterExtDemonGuardInterface::CheckIsInView(int32 targetID)
{
	KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(targetID);
	
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr || TargetEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterInterface::RPC_CELL_onAttackTarget : entity!"));
		return;
	}

	FVector StartPos;
	FRotator PlayerRotation;

	StartPos = TargetEntity->LocalPosition();
	FVector EndLocation = GetEntity()->LocalPosition();

	FVector LineTrace = EndLocation;

	//DrawDebugLine(GetWorld(), StartPos, EndLocation, FColor(255, 0, 0),
	//	false, 5.0f, 0.0f, 10.0f);
	//FHitResult LightWallHitResult;
	//FCollisionQueryParams QueryParams1 = FCollisionQueryParams("", false, GetActor());
	//GetWorld()->LineTraceSingleByChannel(LightWallHitResult, StartPos,
	//	LineTrace,
	//	ECollisionChannel::ECC_GameTraceChannel11,
	//	QueryParams1);

	FCollisionQueryParams TraceParams = FCollisionQueryParams("", true, this->GetActor());
	TraceParams.bTraceComplex = false;
	TraceParams.bReturnPhysicalMaterial = false;
	TraceParams.bIgnoreTouches = true;
	TraceParams.AddIgnoredActor(TargetEntity->Actor());
		

	FHitResult CommonHitResult;
	//FCollisionQueryParams QueryParams2 = FCollisionQueryParams("", false, GetActor());
	GetWorld()->LineTraceSingleByChannel(CommonHitResult, StartPos,
		LineTrace,
		ECollisionChannel::ECC_Visibility,
		TraceParams);


	//更新isPlayerInView
	//AActor *LightWallHitObject = LightWallHitResult.GetActor();
	AActor *CommonHitObject = CommonHitResult.GetActor();

	const int32 eid = entity->ID();
	if (IsValid(CommonHitObject))
	{
		//UE_LOG(LogTemp, Warning, TEXT("Name: %s"), *(HitObject->GetName()));
		//被光墙怪遮挡 两秒后将玩家移出视野
		if (!delaySetViewTimerHandle.IsValid())
		{
			
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, delaySetViewTimerHandle,
				FTimerDelegate::CreateLambda([this, eid]()
			{
				uint8 isPlayerInView = 0;
				KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(eid);
				
				//通知服务器 玩家脱离视野
				if (!entity)
				{
					return;
				}
				else {

					isPlayerInView = entity->GetDefinedProperty(TEXT("isPlayerInView")).GetValue<uint8>();
				}

				if (isPlayerInView)
				{
					isPlayerInView = false;
					KBEngine::FVariantArray Args;
					Args.Add(isPlayerInView);
					entity->CellCall(TEXT("CELL_SetIsPlayerInViewRange"), Args);
				}
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(delaySetViewTimerHandle);
			}
			), 2.0, false);
		}
	}
	else
	{
		uint8 isPlayerInView = entity->GetDefinedProperty(TEXT("isPlayerInView")).GetValue<uint8>();
		if (!isPlayerInView)
		{
			isPlayerInView = true;
			KBEngine::FVariantArray Args;
			Args.Add(isPlayerInView);
			entity->CellCall(TEXT("CELL_SetIsPlayerInViewRange"), Args);
		}
		if (delaySetViewTimerHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(delaySetViewTimerHandle);
		}
	}

}


void UMonsterExtDemonGuardInterface::CLIENT_GetClientNavPoint_Implementation(FVector targetPos)
{
	FVector StartPos = GetEntity()->LocalPosition();
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	FVector EndPos = FVector(targetPos.Z, targetPos.X, targetPos.Y)*100.0;
	StartPos = ServerCharacter->FloorTrace(StartPos);
	EndPos = ServerCharacter->FloorTrace(EndPos);

	UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());;
	UNavigationPath *const NavPath = NavSys->FindPathToLocationSynchronously(GetWorld(), StartPos, EndPos, GetWorld()->GetFirstPlayerController());
	KBEngine::Entity* entity = GetEntity();
	if (!entity)
	{
		return;
	}

	KBEngine::FVariantArray args;
	FString posListStr;
	if (NavPath != NULL && !NavPath->IsPartial() && NavPath->PathPoints.Num() > 0)
	{
		TArray<FVector> FinalAutoPathList = NavPath->PathPoints;

		if (FinalAutoPathList.Num() > 1)
		{		
			if (entity)
			{	
				for (int i = 1; i < FinalAutoPathList.Num(); i++) {
					FVector pos = FinalAutoPathList[i];
					FString posStr = FLOAT_TO_FSTRING(pos.Y / 100.0) + TEXT("|") + FLOAT_TO_FSTRING(pos.Z / 100.0) + TEXT("|") + FLOAT_TO_FSTRING(pos.X / 100.0) + TEXT(";");
					posListStr += posStr;
				}
				posListStr.RemoveFromEnd(TEXT(";"));
				args.Add(posListStr);
				entity->CellCall(TEXT("CELL_recieveMovePointsfromClient"), args);
			}
		}
	}
	else
	{
		FVector LineTrace = EndPos;

		//DrawDebugLine(GetWorld(), StartPos, EndPos, FColor::Red,
		//	false, 5.0f, 0.0f, 10.0f);
		//FHitResult LightWallHitResult;
		//FCollisionQueryParams QueryParams1 = FCollisionQueryParams("", false, GetActor());
		//GetWorld()->LineTraceSingleByChannel(LightWallHitResult, StartPos,
		//	LineTrace,
		//	ECollisionChannel::ECC_GameTraceChannel11,
		//	QueryParams1);

		FCollisionQueryParams TraceParams = FCollisionQueryParams("", true, this->GetActor());
		TraceParams.bTraceComplex = false;
		TraceParams.bReturnPhysicalMaterial = false;
		TraceParams.bIgnoreTouches = true;
		
		FHitResult HitResult;
		GetWorld()->LineTraceSingleByChannel(HitResult, StartPos,
			LineTrace,
			ECollisionChannel::ECC_GameTraceChannel11,
			TraceParams);


		//更新isPlayerInView
		//AActor *LightWallHitObject = LightWallHitResult.GetActor();
		AActor *HitObject = HitResult.GetActor();
		if (!IsValid(HitObject))
		{
			//如果找不到点 并且和目标中间没有光墙 向服务器发送空字符串 服务器接受后使用服务器移动到目标点
			KBEngine::FVariantArray Args;
			posListStr = "";
			Args.Add(posListStr);
			entity->CellCall(TEXT("CELL_recieveMovePointsfromClient"), Args);
		}
		//else {
		//	FVector pos = HitObject->GetActorLocation();
		//	KBEngine::FVariantArray args;
		//	FString posStr = FLOAT_TO_FSTRING(pos.Y / 100.0) + TEXT("|") + FLOAT_TO_FSTRING(pos.Z / 100.0) + TEXT("|") + FLOAT_TO_FSTRING(pos.X / 100.0);
		//	args.Add(posStr);
		//	entity->CellCall(TEXT("CELL_recieveMovePointsfromClient"), args);
		//}


	}

}


void UMonsterExtDemonGuardInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_CreateViewShapeTrap");
	ArrBlueFunc.Add("CLIENT_GetClientNavPoint");
	Supper::InitBlueCB();
}