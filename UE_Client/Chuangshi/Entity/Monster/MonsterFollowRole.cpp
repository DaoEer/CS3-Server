#include "MonsterFollowRole.h"
#include "KBEMath.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterFollowRole, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterFollowRole, Supper)
DECLARE_PROPERTY_CHANGED_NOTIFY(enemyID, &MonsterFollowRole::set_enemyID, int32)
DECLARE_PROPERTY_CHANGED_NOTIFY(curPosition, &MonsterFollowRole::set_curPosition, FVector)
DECLARE_PROPERTY_CHANGED_NOTIFY(curDirection, &MonsterFollowRole::set_curDirection, FVector)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterFollowRole::MonsterFollowRole()
{
	nextPosition = FVector::ZeroVector;
	nextDirection = FVector::ZeroVector;
}

MonsterFollowRole::~MonsterFollowRole()
{
}

UClass* MonsterFollowRole::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterFollowRole"));
}

void MonsterFollowRole::set_enemyID(const int32& newEnemyID, const int32& oldEnemyID)
{

}

void MonsterFollowRole::set_curPosition(const FVector &newKbePos, const FVector& oldKbePos)
{
	OnSetPosition(KBEMath::KBEngine2UnrealPosition(newKbePos));
}

void MonsterFollowRole::set_curDirection(const FVector &newKbeDir, const FVector& oldKbeDir)
{
	OnSetDirection(KBEMath::KBEngine2UnrealDirection(newKbeDir));
}

void MonsterFollowRole::OnSetPosition(const FVector &unrealPos)
{
	FVector old = position_;
	position_ = lastSyncPos_ = unrealPos;

	if (parent_)
		localPosition_ = parent_->PositionWorldToLocal(position_);
	else
		localPosition_ = position_;
	SyncVolatileDataToChildren(true);

	Set_Position(old);
}

void MonsterFollowRole::OnSetDirection(const FVector &unrealDir)
{
	FVector old = direction_;
	direction_ = lastSyncDir_ = unrealDir;

	if (parent_)
		localDirection_ = parent_->DirectionWorldToLocal(direction_);
	else
		localDirection_ = direction_;
	SyncVolatileDataToChildren(false);

	Set_Direction(old);
}

// 来自服务器：强制位置改变
void MonsterFollowRole::OnPositionSet(const FVector &unrealPos)
{

}

// 来自服务器：强制朝向改变
void MonsterFollowRole::OnDirectionSet(const FVector &unrealDir)
{

}

void MonsterFollowRole::UpdateVolatileDataToServer(const FVector& pos, const FVector& dir)
{

}
CONTROL_COMPILE_OPTIMIZE_END