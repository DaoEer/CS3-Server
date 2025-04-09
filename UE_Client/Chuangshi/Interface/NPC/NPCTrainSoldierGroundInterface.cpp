#include "NPCTrainSoldierGroundInterface.h"
#include "../../Util/ConvertUtil.h"
#include "../../Util/CS3Debug.h"
#include "../../GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCTrainSoldierGroundInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_CreateTrainSoldierGroundArea, &UNPCTrainSoldierGroundInterface::CLIENT_CreateTrainSoldierGroundArea, const FString&, uint8)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCTrainSoldierGroundInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(lineNumber, &UNPCTrainSoldierGroundInterface::Set_lineNumber, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(index, &UNPCTrainSoldierGroundInterface::Set_index, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(occupyPlayerName, &UNPCTrainSoldierGroundInterface::Set_occupyPlayerName, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(declareWarState, &UNPCTrainSoldierGroundInterface::Set_declareWarState, uint8)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fightEndTime, &UNPCTrainSoldierGroundInterface::Set_fightEndTime, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(trainGroundType, &UNPCTrainSoldierGroundInterface::Set_trainGroundType, uint8)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(occupyPlayerDBID, &UNPCTrainSoldierGroundInterface::Set_occupyPlayerDBID, uint64)
CS3_END_INTERFACE_PROPERTY_MAP()

UNPCTrainSoldierGroundInterface::UNPCTrainSoldierGroundInterface()
{
}

UNPCTrainSoldierGroundInterface::~UNPCTrainSoldierGroundInterface()
{
}

void UNPCTrainSoldierGroundInterface::Set_lineNumber(const int32& newVal, const int32& oldVal)
{
	lineNumber = newVal;
}

void UNPCTrainSoldierGroundInterface::Set_index(const int32& newVal, const int32& oldVal)
{
	index = newVal;
}

void UNPCTrainSoldierGroundInterface::Set_occupyPlayerName(const FString& newVal, const FString& oldVal)
{
	occupyPlayerName = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOccupyPlayerNameChanged.Broadcast(occupyPlayerName);
	}
	ANPCCharacter* Owner = Cast<ANPCCharacter>(GetActor());
	if (IsValid(Owner))
	{
		Owner->OnOccupyPlayerNameChanged(occupyPlayerName);
	}
}

void UNPCTrainSoldierGroundInterface::Set_declareWarState(const uint8& newVal, const uint8& oldVal)
{
	declareWarState = NPCTRAINSOLDIERGROUND_STATE(newVal);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnDeclareWarStateChanged.Broadcast(newVal);
	}
	ANPCCharacter* Owner = Cast<ANPCCharacter>(GetActor());
	if (IsValid(Owner))
	{
		Owner->OnDeclareWarStateChanged(newVal);
	}
}

void UNPCTrainSoldierGroundInterface::Set_fightEndTime(const FString& newVal, const FString& oldVal)
{
	fightEndTime = newVal;
}

void UNPCTrainSoldierGroundInterface::Set_trainGroundType(const uint8& newVal, const uint8& oldVal)
{
	TrainGroundType = NPCTRAINSOLDIERGROUND_TYPE(newVal);
}

void UNPCTrainSoldierGroundInterface::Set_occupyPlayerDBID(const uint64& newVal, const uint64& oldVal)
{
	uint64 rolePlayerDBID = UGolbalBPFunctionLibrary::GetPlayerPlayerDBID();
	AActor* Owner = GetActor();
	if (IsValid(Owner))
	{
		ANPCCharacter* NPCTrainSoldierGround = Cast<ANPCCharacter>(Owner);
		if (NPCTrainSoldierGround && this->GetEntity())
		{
			bool IsOwnSide = rolePlayerDBID == newVal ? true : false;
			NPCTrainSoldierGround->OnUpdaterainSoldierGroundArea(IsOwnSide);
		}
	}
}

void UNPCTrainSoldierGroundInterface::CLIENT_CreateTrainSoldierGroundArea(const FString& InScriptID, uint8 IsOwnSide)
{
	AActor* Owner = GetActor();
	if (IsValid(Owner))
	{
		ANPCCharacter* NPCTrainSoldierGround = Cast<ANPCCharacter>(Owner);
		if (NPCTrainSoldierGround && this->GetEntity())
		{
			NPCTrainSoldierGround->OnCreateTrainSoldierGroundArea(InScriptID, bool(IsOwnSide));
		}
	}
}

int32 UNPCTrainSoldierGroundInterface::GetTrainSoldierGroundLineNumber()
{
	return lineNumber;
}

int32 UNPCTrainSoldierGroundInterface::GetTrainSoldierGroundIndex()
{
	return index;
}

FString UNPCTrainSoldierGroundInterface::GetTrainSoldierGroundOccupyPlayerName()
{
	return occupyPlayerName;
}

NPCTRAINSOLDIERGROUND_STATE UNPCTrainSoldierGroundInterface::GetTrainSoldierGroundState()
{
	return declareWarState;
}

FString UNPCTrainSoldierGroundInterface::GetTrainSoldierGroundFightEndTime()
{
	return fightEndTime;
}

NPCTRAINSOLDIERGROUND_TYPE UNPCTrainSoldierGroundInterface::GetTrainGroundType()
{
	return TrainGroundType;
}

