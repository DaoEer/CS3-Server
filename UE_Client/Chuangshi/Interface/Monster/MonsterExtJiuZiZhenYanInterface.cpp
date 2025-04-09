

#include "MonsterExtJiuZiZhenYanInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Manager/EventManager.h"
#include "CS3Base/UIManager.h"
#include "Util/CS3Debug.h"
#include "CS3Base/BaseWindow.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtJiuZiZhenYanInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onStartOccupy, &UMonsterExtJiuZiZhenYanInterface::onStartOccupy)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onEndOccupy, &UMonsterExtJiuZiZhenYanInterface::onEndOccupy, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPoundPlayer, &UMonsterExtJiuZiZhenYanInterface::onPoundPlayer)

CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtJiuZiZhenYanInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(zhenyanType, &UMonsterExtJiuZiZhenYanInterface::Set_zhenyanType, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(curCorrupt, &UMonsterExtJiuZiZhenYanInterface::Set_curCorrupt, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(maxCorrupt, &UMonsterExtJiuZiZhenYanInterface::Set_maxCorrupt, int32)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtJiuZiZhenYanInterface::UMonsterExtJiuZiZhenYanInterface()
{

}

UMonsterExtJiuZiZhenYanInterface::~UMonsterExtJiuZiZhenYanInterface()
{

}

void UMonsterExtJiuZiZhenYanInterface::onStartOccupy_Implementation()
{
	mIsStartOccupy = true;
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnZhenYanStartOccupy.Broadcast(zhenyanType);
	}
}

void UMonsterExtJiuZiZhenYanInterface::onEndOccupy_Implementation(const uint8& isPlayerOccupy)
{
	mIsStartOccupy = false;
	mOccupyStatus = 2;

	if (isPlayerOccupy)
	{
		mOccupyStatus = 1;
	}
	if (mOccupyStatus != 0)///<被Boss或玩家占领
	{
		if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
		{
			UBaseWindow* nineTruthWnd = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("NineCharacterTruthWnd"));
			if (!IsValid(nineTruthWnd))
			{
				UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::InWorld, TEXT("NineCharacterTruthWnd"));
			}
		}
		if (!IsValid(UUECS3GameInstance::Instance))
			return;
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnZhenYanBeOccupied.Broadcast(mOccupyStatus,zhenyanType);
		}
	}
}

void UMonsterExtJiuZiZhenYanInterface::onPoundPlayer_Implementation()
{

}

void UMonsterExtJiuZiZhenYanInterface::Set_zhenyanType(const int32& newVal, const int32& oldVal)
{
	zhenyanType = newVal;
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnZhenyanTypeChanged.Broadcast(EntityID, zhenyanType);
	}
}

void UMonsterExtJiuZiZhenYanInterface::Set_curCorrupt(const int32& newVal, const int32& oldVal)
{
	curCorrupt = newVal;
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnBossCorruptChanged.Broadcast(EntityID, curCorrupt, maxCorrupt);
	}
	
}

void UMonsterExtJiuZiZhenYanInterface::Set_maxCorrupt(const int32& newVal, const int32& oldVal)
{
	maxCorrupt = newVal;
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnBossCorruptChanged.Broadcast(EntityID, curCorrupt, maxCorrupt);
	}
}
void UMonsterExtJiuZiZhenYanInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}
