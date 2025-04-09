#include "BuffLoader.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/Skill/BuffTableData.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Skill/Buff/BuffClientHold.h"
#include "Skill/Buff/BuffClientHit.h"
#include "Skill/Buff/BuffClientHitBack.h"
#include "Skill/Buff/BuffClientLoop.h"
#include "Skill/Buff/BuffClientStackable.h"
#include "Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START
UBuffLoader::UBuffLoader()
{
}

UBuffLoader::~UBuffLoader()
{
	
}

UBuffLoader * UBuffLoader::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UBuffLoader>();
}

void UBuffLoader::loadAllBuff()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* BuffConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF);
		for (auto RowName : BuffConfig->GetRowNames())
		{
			FString BuffID = FNAME_TO_FSTRING(RowName);
			const FBUFF_TABLE_DATA* BuffData = BuffConfig->GetRow<FBUFF_TABLE_DATA>(BuffID);
			UBuff* buffInstance = CreateBuff(BuffID, BuffData);
			if (nullptr != buffInstance)
			{
				_buffs.Emplace(FSTRING_TO_INT(BuffID), buffInstance);
			}
		}
		const UConfigTable* BuffConfigTest = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF_TEST);
		for (auto RowName : BuffConfigTest->GetRowNames())
		{
			FString BuffID = FNAME_TO_FSTRING(RowName);
			const FBUFF_TABLE_DATA* BuffData = BuffConfigTest->GetRow<FBUFF_TABLE_DATA>(BuffID);
			UBuff* buffInstance = CreateBuff(BuffID, BuffData);
			if (nullptr != buffInstance)
			{
				_buffs.Emplace(FSTRING_TO_INT(BuffID), buffInstance);
			}
		}
	}
}

UBuff * UBuffLoader::CreateBuff(FString BuffID, const FBUFF_TABLE_DATA * buffDat)
{
	UBuff* BuffInstance = nullptr;
	if (buffDat->BuffType == ENUM_BUFF_CLASS_TYPE::BuffClientHold)
	{
		UBuffClientHold* Temp = NewObject<UBuffClientHold>();
		Temp->init(BuffID, buffDat);
		BuffInstance = (UBuff*)Temp;
		BuffInstance->AddToRoot();
	}
	else if (buffDat->BuffType == ENUM_BUFF_CLASS_TYPE::BuffClientHit)
	{
		UBuffClientHit* Temp = NewObject<UBuffClientHit>();
		Temp->init(BuffID, buffDat);
		BuffInstance = (UBuff*)Temp;
		BuffInstance->AddToRoot();
	}
	else if (buffDat->BuffType == ENUM_BUFF_CLASS_TYPE::BuffClientHitBack)
	{
		UBuffClientHitBack* Temp = NewObject<UBuffClientHitBack>();
		Temp->init(BuffID, buffDat);
		BuffInstance = (UBuff*)Temp;
		BuffInstance->AddToRoot();
	}
	else if (buffDat->BuffType == ENUM_BUFF_CLASS_TYPE::BuffClientLoop)
	{
		UBuffClientLoop* Temp = NewObject<UBuffClientLoop>();
		Temp->init(BuffID, buffDat);
		BuffInstance = (UBuff*)Temp;
		BuffInstance->AddToRoot();
	}
	else if (buffDat->BuffType == ENUM_BUFF_CLASS_TYPE::BuffClientStackable)
	{
		UBuffClientStackable* Temp = NewObject<UBuffClientStackable>();
		Temp->init(BuffID, buffDat);
		BuffInstance = (UBuff*)Temp;
		BuffInstance->AddToRoot();
	}
	return BuffInstance;
}

UBuff * UBuffLoader::getBuffByID(int32 BuffID)
{
	if (_buffs.Contains(BuffID))
	{
		return _buffs[BuffID];
	}
	return nullptr;
}

CONTROL_COMPILE_OPTIMIZE_END