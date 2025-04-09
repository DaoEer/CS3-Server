

#include "RoleFilterActorComponent.h"
#include "Interface/CombatInterface.h"
#include "Interface/StateInterface.h"
#include "GameData/GameDeFine.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"


CONTROL_COMPILE_OPTIMIZE_START
void URoleFilterActorComponent::Pos(const int32 vehicleID, const FVector& position, const FVector& direction, const FVector& velocity)
{
	FVector newPos;
	FVector newDir;
	bool IsValidData = GetPositionAndDirection(position, direction, vehicleID, newPos, newDir);
	if (!IsValidData) return;
	//设置位置(不检测地面)
	SafeMove(newPos, newDir, false);
	//更新移动速度
	UpdateMoveSpeed(newPos, newDir, velocity);
}
/*
void URoleFilterActorComponent::OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID)
{
	if (!GetEnableIgnoreServerPos())
	{

		AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());

		if (!IsValid(ServerActor))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleFilterActorComponent::Pos : ServerActor!"));
			return;
		}

		auto *entity = ServerActor->GetSelfEntity();
		if (!entity)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleFilterActorComponent::OnUpdateVolatileDataByParent : entity!"));
			return;
		}

		FVector newPos;
		FVector newDir;
		bool IsValidData = GetPositionAndDirection(position, direction, parentID, newPos, newDir);
		if (!IsValidData) return;
		SafeMove(newPos, newDir, false);

		mLastDir = newDir;
		if (FVector::Dist(vLastPos, newPos) > 0.1)
		{
			entity->SyncAndNotifyVolatileDataToChildren(false);
			vLastPos = newPos;
		}
	}
}
*/
CONTROL_COMPILE_OPTIMIZE_END
