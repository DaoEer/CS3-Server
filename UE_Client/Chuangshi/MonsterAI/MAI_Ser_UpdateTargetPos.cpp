// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Ser_UpdateTargetPos.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "GameData/GameDefault.h"
#include "Interface/Monster/CMonsterInterface.h"
#include "CS3Base/CS3Entity.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "Entity/Role/CS3Role.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "Interface/Role/RoleCommanderInterface.h"
#include "AIController.h"


void UMAI_Ser_UpdateTargetPos::TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
	Super::TickNode(OwnerComp, NodeMemory, DeltaSeconds);
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if(IsValid(MonsterCharacter))
	{
		CMonster* pCMonster = static_cast<CMonster*>(MonsterCharacter->GetSelfEntity());
		if (pCMonster)
		{
			FVector TargetPos;

			int32 Cmd = OwnerComp.GetBlackboardComponent()->GetValueAsEnum(FName("CurrCmd"));
			if (MONSTER_AI_COMMAND(Cmd) == MONSTER_AI_COMMAND::ATTACK)
			{
				int32 AttackEntityID = OwnerComp.GetBlackboardComponent()->GetValueAsInt(FName("AttackEntityID"));
				CS3Entity* attackEntity = static_cast<CS3Entity*>(UGolbalBPFunctionLibrary::FindEntity(AttackEntityID));
				if (attackEntity && IsValid(attackEntity->Actor()))
				{
					TargetPos = attackEntity->Actor()->GetActorLocation();
				}
				else
				{
					TargetPos = MonsterCharacter->GetActorLocation();
				}
				OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("TargetPos"), TargetPos);
			}
			else if(MONSTER_AI_COMMAND(Cmd) == MONSTER_AI_COMMAND::FOLLOW)
			{
				CS3Role* ControlRole = pCMonster->GetControlRole();
				if (ControlRole)
				{
					FVector LastPlayerPos = OwnerComp.GetBlackboardComponent()->GetValueAsVector(FName("CenterPos"));
					AActor* ControlRoleActor = ControlRole->Actor();
					
					if (IsValid(ControlRoleActor))
					{
						if (FVector::Dist2D(ControlRoleActor->GetActorLocation(), LastPlayerPos)>10.f)
						{
							//FRotator NewRotation = ControlRoleActor->GetActorRotation();
							//FVector LastRelativePos = OwnerComp.GetBlackboardComponent()->GetValueAsVector(FName("RelativePos"));
							//FRotator LastRotation = OwnerComp.GetBlackboardComponent()->GetValueAsRotator(FName("Rotation"));
							//FVector NewRelativePos = LastRelativePos.RotateAngleAxis(NewRotation.Yaw - LastRotation.Yaw, FVector(0, 0, 1));
							//TargetPos = ControlRoleActor->GetActorLocation() + NewRelativePos;
							//TargetPos = MonsterCharacter->FloorTrace(TargetPos);
							
							//OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("RelativePos"), NewRelativePos);
							//OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("TargetPos"), TargetPos);
							//OwnerComp.GetBlackboardComponent()->SetValueAsRotator(FName("Rotation"), NewRotation);
							//OwnerComp.GetBlackboardComponent()->SetValueAsVector(FName("CenterPos"), ControlRoleActor->GetActorLocation());
							URoleCommanderInterface* Interface = Cast<URoleCommanderInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleCommanderInterface")));
							Interface->InitSoldierFollow(pCMonster->ID());
						}
						
					}
				}	
			}
		}
	}
}