
#include "MonsterAnimInstance.h"

#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
UMonsterAnimInstance::UMonsterAnimInstance()
{
	bTickUpdate = true;
}

UMonsterAnimInstance::~UMonsterAnimInstance()
{
}

bool UMonsterAnimInstance::IsInWater()
{
	return false;
}

void UMonsterAnimInstance::UpdateMoveDirection()
{
	KBEngine::Entity* pEntity = CurCharacter->GetSelfEntity();
	if (pEntity && Cast<AServerCharacter>(CurCharacter)->IsMoveType(MOVETYPE::MOVETYPE_WANDER))//游荡移动
	{
		CurMoveDirection = UGolbalBPFunctionLibrary::GetFloatPropertyValue(pEntity->ID(), TEXT("wanderDirection"));
	}
}

CONTROL_COMPILE_OPTIMIZE_END
