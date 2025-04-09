#include "MAI_Dec_CheckPlayerDistance.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MAI_Public_func.h"
#include "AIController.h"
#include "Actor/Player/PlayerCharacter.h"


bool UMAI_Dec_CheckPlayerDistance::CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const
{
	if (!IsValid(OwnerComp.GetAIOwner()))
	{
		return false;
	}

	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(MonsterCharacter))
	{
		return false;
	}

	if (MonsterCharacter->GetSelfEntity() == nullptr)
	{
		return false;
	}

	APlayerCharacter* PlayerCharacter = GetPlayerActor();
	if (!IsValid(PlayerCharacter))
	{
		return false;
	}

	if (FVector::Dist(MonsterCharacter->GetActorLocation(), PlayerCharacter->GetActorLocation()) >= Distance)
	{
		return true;
	}

	return false;
}

