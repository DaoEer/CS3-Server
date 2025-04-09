// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Ser_SetFollowPlayerPos.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/CS3Entity.h"
#include "Entity/Monster/CMonster.h"
#include "AIController.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Interface/Role/RoleCommanderInterface.h"
#include "Actor/Player/PlayerCharacter.h"


void UMAI_Ser_SetFollowPlayerPos::TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
	Super::TickNode(OwnerComp, NodeMemory, DeltaSeconds);
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(actor))
	{
		return;
	}
	CMonster* entity = static_cast<CMonster*>(actor->GetSelfEntity());
	if (!entity)
	{
		return;
	}
	

	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player))
	{
		return;
	}

	URoleCommanderInterface* RoleCommanderInterface = Cast< URoleCommanderInterface >(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleCommanderInterface"), Player->EntityId));
	if (!IsValid(RoleCommanderInterface))
	{
		return;
	}
	FVector LastPlayerPos = OwnerComp.GetBlackboardComponent()->GetValueAsVector(FName("CenterPos"));

	FVector CenterPos = Player->GetActorLocation();
	if (FVector::Dist2D(CenterPos, LastPlayerPos) < 20.f)
	{
		return;
	}

	//用FloorTrace在多层导航的时候返回位置不对 返回的是下层导航的位置
	//CenterPos = Player->FloorTrace(CenterPos);
	CenterPos = RoleCommanderInterface->GetVerticalPos(CenterPos).IsZero() ? Player->FloorTrace(CenterPos) : RoleCommanderInterface->GetVerticalPos(CenterPos);

	FRotator TargetRotator = Player->GetActorRotation();
	int32 entityID = entity->ID();
	FVector TargetPos;
	FVector RelativePos;

	const FARMS_DATA& ArmsData = RoleCommanderInterface->ArmsData;

	if (ArmsData.LeftGuardEntityID != entityID && ArmsData.RightGuardEntityID != entityID )
	{
		const FCLIENT_MOSNTER_AI_DATA* data = RoleCommanderInterface->GetClientMonsterAIConfig(ArmsData.SoldierScriptID);
		//初始化 层数 层间距 等分角
		float Distance = data->Follow.FollowSpace;
		float Extension = data->Follow.FollowStartDist; //起始距离
		int32 IndexMax = (int32)data->Follow.FollowMaxIndex;

		int32 ArmIndex = ArmsData.SoldierEntityIDList.IndexOfByKey(entityID);
		RoleCommanderInterface->CalcInitSoldierFollow(Distance, Extension, IndexMax, ArmIndex, CenterPos, TargetPos, RelativePos, TargetRotator);
	}
	else
	{
		float angle;
		if (ArmsData.LeftGuardEntityID == entityID)
		{
			angle = -90;
		}
		else
		{
			angle = 90;
		}
		float Distance = RoleCommanderInterface->FollowSpace;
		float radian = FMath::DegreesToRadians(TargetRotator.Yaw);
		FVector2D vDir = FVector2D(FMath::Cos(radian), FMath::Sin(radian));
		FVector2D vLeft = vDir.GetRotated(angle) * Distance;
		RelativePos = FVector(vLeft.X, vLeft.Y, 0.0);
		TargetPos = CenterPos + RelativePos;
	}

	OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("TargetPos"), TargetPos);
	OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("CenterPos"), CenterPos);
	OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("RelativePos"), RelativePos);
	OwnerComp.GetBlackboardComponent()->SetValueAsRotator(FName("Rotation"), TargetRotator);
}