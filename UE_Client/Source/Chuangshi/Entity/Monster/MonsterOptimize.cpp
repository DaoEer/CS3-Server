

#include "MonsterOptimize.h"
#include "Interface/Monster/MonsterOptimizeInterface.h"

#include "Util/GolbalBPFunctionLibrary.h"

DEF_INTERFACE_BEGIN(MonsterOptimize, Supper)
DEF_INTERFACE(UMonsterOptimizeInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterOptimize, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterOptimize, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterOptimize::MonsterOptimize()
{
}

MonsterOptimize::~MonsterOptimize()
{
}

void MonsterOptimize::InitInterfaceCache()
{
	Supper::InitInterfaceCache();
	GameObjectInterface = Cast< UMonsterOptimizeInterface >(*(m_interfaceContainer.Find("GameObjectInterface")));
}

void MonsterOptimize::DestroyInterfaces()
{
	GameObjectInterface = nullptr;
	Supper::DestroyInterfaces();
}

void MonsterOptimize::OnMoveOver(const uint32 movingID, const bool isSuccess)
{
	if ( IsValid(GameObjectInterface))
		GameObjectInterface->OnMoveOver(movingID, isSuccess);
}

UClass* MonsterOptimize::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterOptimize"));
}

void MonsterOptimize::Set_Position(const FVector &oldVal)
{
	Supper::Set_Position(oldVal);
	if (IsValid(GameObjectInterface))
		GameObjectInterface->Set_Position(oldVal);
}
