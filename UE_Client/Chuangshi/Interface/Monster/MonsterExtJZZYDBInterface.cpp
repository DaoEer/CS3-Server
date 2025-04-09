

#include "MonsterExtJZZYDBInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtJZZYDBInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtJZZYDBInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtJZZYDBInterface::UMonsterExtJZZYDBInterface()
{

}

UMonsterExtJZZYDBInterface::~UMonsterExtJZZYDBInterface()
{
}

void UMonsterExtJZZYDBInterface::RPC_onCollisionZYDB(FVector pos)
{
	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterExtJZZYDBInterface::RPC_onCollisionZYDB : Monster!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(pos);
	Monster->CellCall(TEXT("onCollisionZYDB"), Args);
}

void UMonsterExtJZZYDBInterface::RPC_onEnterZYDBScope()
{
	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterExtJZZYDBInterface::RPC_onEnterZYDBScope : Monster!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Monster->CellCall(TEXT("onEnterZYDBScope"), Args);
}

void UMonsterExtJZZYDBInterface::RPC_onLeaveZYDBScope()
{
	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterExtJZZYDBInterface::RPC_onLeaveZYDBScope : Monster!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Monster->CellCall(TEXT("onLeaveZYDBScope"), Args);
}

void UMonsterExtJZZYDBInterface::onStartOccupy_Implementation()
{
	mIsStartOccupy = true;
}

void UMonsterExtJZZYDBInterface::onEndOccupy_Implementation(bool isPlayerOccupy)
{
	mIsStartOccupy = false;
	mOccupyStatus = 2;
	
	if (isPlayerOccupy)
		mOccupyStatus = 1;
}

void UMonsterExtJZZYDBInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onStartOccupy");
	ArrBlueFunc.Add("onEndOccupy");
	Supper::InitBlueCB();
}
