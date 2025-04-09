// Fill out your copyright notice in the Description page of Project Settings.

#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../GameData/GameDefault.h"
#include "ResourceManager.h"
#include"Chuangshi.h"
//UConfigTable--------------------------------------------------------------------------------------------
bool UConfigTable::CheckRow(const FCSV_TABLE_ROW_BASE* Row, const FName& RowName) const
{
	if (Row == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UConfigTable::CheckRow : Row!"));
		return false;
	}

	//这个状态只在这有修改
	CheckState& NowCheckState = AllRowCheckState.FindOrAdd(RowName);
	switch (NowCheckState)
	{
	case CheckState::NotCheck:
		if (Row->Check())
		{
			NowCheckState = CheckState::Ok;
			return true;
		}
		else
		{
			CS3_Warning(TEXT("ConfigTableName: %s  RowName: %s  Reason: Row->Check() == false"), *(Table->GetName()), *RowName.ToString());
			NowCheckState = CheckState::Error;
			return false;
		}
	case CheckState::Ok: return true;
	case CheckState::Error: return false;
	default: return false;
	}
}

UConfigTable* UConfigTable::CreateCfgTable(UDataTable* Table)
{
	UConfigTable* ConfigTable = NewObject<UConfigTable>();
	ConfigTable->Table = Table;

	TArray<FName> RowNames = ConfigTable->GetRowNames();
	ConfigTable->AllRowCheckState.Reserve(RowNames.Num());
	for (auto& RowName : RowNames)
	{
		ConfigTable->AllRowCheckState.Add(RowName, CheckState::NotCheck);
	};
	return ConfigTable;
}

const UDataTable* UConfigTable::GetBaseTable() const
{
	return Table;
}

TArray<FName> UConfigTable::GetRowNames() const
{
	return Table->GetRowNames();
}


//UCfgManager--------------------------------------------------------------------------------------------
UCfgManager::UCfgManager()
{
	
}


UCfgManager::~UCfgManager()
{
}

UCfgManager* UCfgManager::GetInstance()
{
	cs3_checkNoReentry();

	UCfgManager* Instance = NewObject<UCfgManager>();

	if (IsValid(Instance) && !IsValid(Instance->CsvConfigTable))
	{
		FString path = UUECS3GameInstance::Instance->GameDefault->CsvConfigPath;
#if WITH_EDITOR
		Instance->LoadMainCfg(path, false);
#else
		Instance->LoadMainCfg(path);
#endif
	}
	return Instance;
}

void UCfgManager::LoadMainCfg(FString path, bool preload)
{	
	UDataTable* baseTable = LoadObject<UDataTable>(nullptr, *path);
	checkf(IsValid(baseTable), TEXT("加载主配置表失败：\t%s"), *path);
	if (baseTable)
	{
		UConfigTable* ConfigTable = UConfigTable::CreateCfgTable(baseTable);
		CsvConfigTable = ConfigTable;
	}
	if (preload)
	{
		TArray<FName> RowNames = baseTable->GetRowNames();
		for (FName& rowName : RowNames)
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("%s"), rowName.ToString())

			if (!rowName.ToString().IsEmpty())
			{
				const FCSV_CONFIG_DATA* ConfigData = CsvConfigTable->GetRow<FCSV_CONFIG_DATA>(rowName.ToString());
				if(ConfigData->PreLoading)
				{
					UObject* TableObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(ConfigData->ConfigPath.ToSoftObjectPath());
					if (TableObj)
					{
						UConfigTable* childTable = UConfigTable::CreateCfgTable((UDataTable*)TableObj);
						int tableID = FCString::Atoi(*rowName.ToString());
						TableMap.Add((CSV_CONFIG_TYPE_ENUM)tableID, childTable);
					}
					else
					{
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("加载type配置表失败：\t%s"), *ConfigData->ConfigPath.ToSoftObjectPath().ToString());
					}
				}
			}
		}
	}
}

const UConfigTable* UCfgManager::GetTableByType(CSV_CONFIG_TYPE_ENUM TableType)
{
	UConfigTable* ConfigTable = nullptr;
	if (TableMap.Contains(TableType))
	{
		ConfigTable = TableMap[TableType];
	}
	else
	{
		const FCSV_CONFIG_DATA* ConfigData = CsvConfigTable->GetRow<FCSV_CONFIG_DATA>(FString::FromInt((int)TableType));
		UObject* TableObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(ConfigData->ConfigPath.ToSoftObjectPath());
		checkf(IsValid(TableObj), TEXT("加载type配置表失败：\t%s"), *ConfigData->ConfigPath.ToSoftObjectPath().ToString());
		ConfigTable = UConfigTable::CreateCfgTable((UDataTable*)TableObj);
		TableMap.Add(TableType, ConfigTable);
	}
	return ConfigTable;
}

const UConfigTable* UCfgManager::GetTableByPath(TSoftObjectPtr<UDataTable> ConfigPath)
{
	UConfigTable* ConfigTable = nullptr;
	if (TablePathMap.Contains(ConfigPath))
	{
		ConfigTable = TablePathMap[ConfigPath];
	}
	else
	{
		UObject* TableObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(ConfigPath.ToSoftObjectPath());
		checkf(IsValid(TableObj), TEXT("加载path配置表失败：\t%s"), *ConfigPath.ToSoftObjectPath().ToString());
		ConfigTable = UConfigTable::CreateCfgTable((UDataTable*)TableObj);
		TablePathMap.Add(ConfigPath, ConfigTable);
	}
	return ConfigTable;
}