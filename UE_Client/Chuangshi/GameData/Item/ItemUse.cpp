// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemUse.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/SkillInterface.h"
#include "Actor/ServerCharacter.h"
#include "GameData/MessageID.h"
#include "Manager/SkillManager.h"
#include "Manager/CustomTimerManager.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "CS3Base/CS3Entity.h"
#include "CS3Base/GameObject.h"

void UItemUse::BeginDestroy()
{
	Super::BeginDestroy();
}

int32 UItemUse::Use(AServerCharacter* player)
{
	//清除新品状态
	RecordOpertation();
	int32 useresult = UseQuery(player);
	if (useresult == (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG))		//条件检测通过
	{
		if (!IsUseItemToPosition())
		{
			NotityUseItemToCell();
		}
		else
		{
			UseItemToPosition();
		}
	}
	else
	{
		UGolbalBPFunctionLibrary::StatusMessage(useresult, TEXT(""));
	}
	return useresult;
}

int32 UItemUse::UseQuery(AServerCharacter* player)
{
	//检测CD
	if (IsCoolDowning())
	{
		return UUECS3GameInstance::Instance->GMessageID->ITEM_INCD;
	}
	if (!player)
	{
		return UUECS3GameInstance::Instance->GMessageID->ITEM_USE_LV_LESS_MSG;
	}
	int32 entityID = UGolbalBPFunctionLibrary::GetPlayerID();
	if (IsValid(player))
	{
		entityID = player->EntityId;
	}
	KBEngine::Entity *entity = UGolbalBPFunctionLibrary::FindEntity(entityID);
	if (entity)
	{
		//检测等级
		if (!CheckLevel(player))
		{
			return UUECS3GameInstance::Instance->GMessageID->ITEM_USE_LV_LESS_MSG;
		}
		//检测职业
		if (!CheckReqClass(player))
		{
			return UUECS3GameInstance::Instance->GMessageID->ITEM_USE_CLASS_NOTMATCH;
		}
	}
	return UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG;
}

void UItemUse::NotityUseItemToCell()
{
	int32 playerID = UGolbalBPFunctionLibrary::GetPlayerID();
	int32 targetID = UGolbalBPFunctionLibrary::GetTargetEntityID();
	//FString methodname = TEXT("CELL_useItem");
	//TArray<FString> args;
	//args.Add(UID);
	//args.Add(FString::FromInt(targetID));
	URoleKitBagInterface * RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (RoleKitBagInterface)
	{
		RoleKitBagInterface->RPC_useItem(UID, FString::FromInt(targetID));
	}
	//UGolbalBPFunctionLibrary::CellCall(playerID, methodname, args);
}

bool UItemUse::IsUsing()
{
	//FString usingItemUid = UGolbalBPFunctionLibrary::GetEntityPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("usingItemUid"));
	//return UID.Equals(usingItemUid);
	
	KBEngine::Entity* _entity = UGolbalBPFunctionLibrary::FindEntity(UGolbalBPFunctionLibrary::GetPlayerID());
	if (_entity)
	{
		uint64 usingItemUid = _entity->GetDefinedProperty(TEXT("usingItemUid")).GetValue<uint64>();
		return UID.Equals(INT64_TO_FSTRING(usingItemUid));
	}
	CS3_Warning(TEXT("Can not find entity!"));
	return false;
	
}

bool UItemUse::IsCanUse()
{
	AServerCharacter* player = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	int32 entityID = UGolbalBPFunctionLibrary::GetPlayerID();
	KBEngine::Entity *entity = UGolbalBPFunctionLibrary::FindEntity(entityID);
	if (entity)
	{
		//检测等级
		if (!CheckLevel(player))
		{
			return false;
		}
		//检测职业
		if (!CheckReqClass(player))
		{
			return false;
		}
	}
	return true;
}


bool UItemUse::IsCoolDowning()
{
	return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(CdTimerHandle) > 0;
}

void UItemUse::StartCdTime(float TimeRemaining)
{
	if (IsCoolDowning())
	{
		StopCdTime();
	}

	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CdTimerHandle, this, &UItemUse::StopCdTime, TimeRemaining, false);
}

void UItemUse::StopCdTime()
{
	if (CdTimerHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CdTimerHandle);
	}
}

float UItemUse::GetCDRemainningTime()
{
	return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(CdTimerHandle);
}

float UItemUse::GetCDPersistTime()
{
	return CDPersistTime;
}

void UItemUse::SetCDPersistTime(float PersistTime)
{
	CDPersistTime = PersistTime;
}

bool UItemUse::IsUseItemToPosition()
{
	USkillData* SkillData = UGolbalBPFunctionLibrary::SkillManager()->GetSkillDataById(SkillID);

	if (IsValid(SkillData))
	{
		if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition)
		{
			return true;
		}
	}

	return false;
}

void UItemUse::UseItemToPosition()
{
	USkillInterface* skillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;

	if (skillInterface)
	{
		skillInterface->UsePositionItem(UID, SkillID);
	}
}

void UItemUse::SetUseItemToPositionBeforeNotifyServer()
{

}

void UItemUse::CancelUseItemToPositionBeforeNotifyServer()
{

}

