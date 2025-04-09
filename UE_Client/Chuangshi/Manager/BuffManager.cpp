// Fill out your copyright notice in the Description page of Project Settings.


#include "BuffManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ResourceManager.h"
#include"Chuangshi.h"
#include "GameData/EnumCsvDefine.h"
#include "CfgManager.h"
#include "Skill/BuffLoader.h"

UBuffManager::UBuffManager()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->BuffLoader))
	{
		 UUECS3GameInstance::Instance->BuffLoader->loadAllBuff();
	}
}

UBuffManager::~UBuffManager()
{
}

UBuffManager* UBuffManager::GetInstance()
{
	cs3_checkNoReentry();

	//预加载
	UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF);
	UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF_TEST);
	return NewObject<UBuffManager>();
}

void UBuffManager::AsyncLoadBuffAsset(FStreamableDelegate DelegateToCall, int32 BuffID)
{
	const FBUFF_TABLE_DATA* TableData = GetBuffDataByBuffID(BuffID);
	if (TableData)
	{
		if (TableData->BuffIcon.IsValid() && !IsValid(TableData->BuffIcon.Get()) )
		{

			TArray<FStringAssetReference> AssetReferenceArr;
			AssetReferenceArr.Add(TableData->BuffIcon.ToSoftObjectPath());
			UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, AssetReferenceArr, DelegateToCall, RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER);
			return;
		}
	}
	if (DelegateToCall.IsBound())
	{
		DelegateToCall.Execute();
	}
	
}

FBuffUIData UBuffManager::CreateBuffUIData(const int32& BuffIndex, const int32& BuffID, const float& BuffTotalTime, const float& BuffTime, const int32& Layer)
{
	FBuffUIData fData = FBuffUIData();
	const FBUFF_TABLE_DATA* TableData = GetBuffDataByBuffID(BuffID);
	if (TableData)
	{
		fData.BuffIndex = BuffIndex;
		fData.BuffName = TableData->BuffName;
		fData.Description = TableData->Description;
		fData.IsShowIcon = TableData->IsShowIcon;
		fData.TotalTime = BuffTotalTime;
		fData.RemainTime = BuffTime;
		fData.Layer = Layer;
		fData.CanInterrupt = false;
		for (auto TempEvent : TableData->TargetInterruptBuffEvent)
		{
			if (TempEvent.EventType == ENUM_SKILL_EVENT::InitiaiveStopBuffEvent)
			{
				fData.CanInterrupt = true;
				break;
			}
		}
		if (IsValid(TableData->BuffIcon.Get()))
		{
			fData.BuffIcon = TableData->BuffIcon.Get();
		}
		else if (TableData->BuffIcon.ToSoftObjectPath().IsValid())
		{
			UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(TableData->BuffIcon.ToSoftObjectPath());
			fData.BuffIcon = TableData->BuffIcon.Get();
		}
	}
	return fData;
}

const FBUFF_TABLE_DATA* UBuffManager::GetBuffDataByBuffID(int32 BuffId)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		const UConfigTable* ConfigTableTest = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF_TEST);
		const FBUFF_TABLE_DATA* _BuffTestTableData = ConfigTableTest->GetRow<FBUFF_TABLE_DATA>(INT_TO_FSTRING(BuffId));
		if (_BuffTestTableData)
		{
			return _BuffTestTableData;
		}
		else
		{
			const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF);
			return ConfigTable->GetRow<FBUFF_TABLE_DATA>(INT_TO_FSTRING(BuffId));
		}
	}

	return nullptr;
}

UTexture2D* UBuffManager::GetIconByBuffID(int32 BuffId)
{
	const FBUFF_TABLE_DATA* TableData = GetBuffDataByBuffID(BuffId);
	if (TableData)
	{
		if (IsValid(TableData->BuffIcon.Get()))
		{
			return TableData->BuffIcon.Get();
		}

		if (TableData->BuffIcon.ToSoftObjectPath().IsValid())
		{
			UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(TableData->BuffIcon.ToSoftObjectPath());
			return TableData->BuffIcon.Get();
		}

	}
	return nullptr;
}

FString UBuffManager::GetNameByBuffID(int32 BuffId)
{
	const FBUFF_TABLE_DATA* TableData = GetBuffDataByBuffID(BuffId);
	if (TableData)
	{
		return TableData->BuffName;
	}
	return TEXT("");
}

FString UBuffManager::GetTargetActForbidDescribe(int32 BuffId)
{
	const FBUFF_TABLE_DATA* TableData = GetBuffDataByBuffID(BuffId);
	if (!TableData)
	{
		return UGolbalBPFunctionLibrary::GetChinese(TEXT("Unknown"));
	}
	//优先描述配置
	if (!TableData->TargetActForbidDescribe.Equals(TEXT("")))
	{
		return TableData->TargetActForbidDescribe;
	}
	//如果没有配置描述，则获取开关条件配置
	else
	{
		ACTION_FLAG TargetActForbid = TableData->TargetActForbid;
		const UConfigTable* DataTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BUFF_TARGETACTFORBID_DATA);
		if (IsValid(DataTable))
		{
			for (auto RowName : DataTable->GetRowNames())
			{
				const FBUFF_TARGETACTFORBID_DATA* ConfigData = DataTable->GetRow<FBUFF_TARGETACTFORBID_DATA>(RowName);
				if (ConfigData && ConfigData->TargetActForbid == TargetActForbid)
				{
					return ConfigData->ChineseDesc;
				}
			}
		}
		return UGolbalBPFunctionLibrary::GetChinese(TEXT("Unknown"));
	}
	return UGolbalBPFunctionLibrary::GetChinese(TEXT("Unknown"));
}
