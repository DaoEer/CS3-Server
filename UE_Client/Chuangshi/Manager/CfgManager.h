// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "../GameData/CsvConfigData.h"
#include "../GameData/EnumCsvDefine.h"
#include "../GameData/CsvTableRowBase.h"
#include "GameData/CS3Object.h"
#include "GameData/EntityInterfaceDefine.h"
#include "NameTypes.h"
#include "CfgManager.generated.h"

/*
* 文件名称：CfgManager.h
* 功能说明：
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-10-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UConfigTable :public UCS3Object
{
	GENERATED_BODY()
private:
	UPROPERTY()
		UDataTable* Table;

	enum CheckState
	{
		NotCheck,
		Ok,
		Error,
	};

	//用来记录行是否已经检查过了(防止每次都检查一遍)
	mutable TMap<FName, CheckState> AllRowCheckState;

	//检查行数据
	bool CheckRow(const FCSV_TABLE_ROW_BASE* Row, const FName& RowName) const;

public:
	static UConfigTable* CreateCfgTable(UDataTable* Table);

	const UDataTable* GetBaseTable() const;

	TArray<FName> GetRowNames() const;

	template < class T = FCSV_TABLE_ROW_BASE>
	const T* GetRow(FString RowName) const
	{
		FName CurRowName = FName(*RowName);
		T* RowTable = (T*)Table->FindRowUnchecked(CurRowName);
		if (RowTable == nullptr)
		{
			return nullptr;
		}
		if (CheckRow(RowTable, CurRowName))
		{
			RowTable->RowName = CurRowName;
			return RowTable;
		}
		else
		{
			return nullptr;
		}
	}

	template < class T = FCSV_TABLE_ROW_BASE>
	const T* GetRow(FName RowName) const
	{
		T* RowTable = (T*)Table->FindRowUnchecked(RowName);
		if (CheckRow(RowTable, RowName))
		{
			RowTable->RowName = RowName;
			return RowTable;
		}
		else
		{
			return nullptr;
		}
	}

	template <class T>
	//void UConfigTable::GetAllRows(OUT TArray<T*>& OutRowArray) const
	void GetAllRows(OUT TArray<T*>& OutRowArray) const
	{
		Table->GetAllRows(TEXT(""), OutRowArray);
	}
};



/**
 * 配置表管理器
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UCfgManager : public UCS3Object
{
	GENERATED_BODY()

public:
	UCfgManager();
	~UCfgManager();

	static UCfgManager* GetInstance();///<获取CfgManager实例，返回static UCfgManager*  CfgManager实例对象

	/**
	 *获取配置列表数据
	 *
	 *@param TableType 列表类型
	 *
	 *@return  const UConfigTable
	 */
	const UConfigTable* GetTableByType(CSV_CONFIG_TYPE_ENUM TableType);

	/*
	*获取配置列表数据
	*
	*@param ConfigPath 配置表路径
	*
	*@return  const UConfigTable* 配置列表数据
	*/
	const UConfigTable* GetTableByPath(TSoftObjectPtr<UDataTable> ConfigPath);


private:
	void LoadMainCfg(FString path, bool preload = true);///<加载配置表

public:
	UPROPERTY()
		UConfigTable* CsvConfigTable;///CSV配置表数据表
	UPROPERTY()
		TMap<CSV_CONFIG_TYPE_ENUM, UConfigTable*> TableMap;///CSV配置表
	UPROPERTY()
		TMap<TSoftObjectPtr<UDataTable>, UConfigTable*> TablePathMap;///CSV配置表路径表

	UPROPERTY()
		TMap<FString, FINTERFACEDEFINEARRAY> InterfaceDefineDatas;	///entity接口配置


	TArray<FINTERFACEDEFINE*> InterfaceDatasCfg;

private:
	//static UCfgManager* Instance;///<CfgManager实例

};

//后台加载永不释放的核心资源.
//TableType: CSV_CONFIG_TYPE_ENUM	类型
//RowClass : FCSV_TABLE_ROW_BASE	类型
//Attribute: const FSoftObjectPath& 类型
//示例: BackstageAsyncLoad_Table_One(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS, FStrToClass, ClassPath.ToSoftObjectPath());
#define BackstageAsyncLoad_Table_One(TableType, RowClass, Attribute)\
{\
	checkf(IsValid(UUECS3GameInstance::Instance), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance == nullptr || Instance->ResourceManager == nullptr"));\
	checkf(IsValid(UUECS3GameInstance::Instance->ResourceManager), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance->ResourceManager == nullptr"));\
	checkf(IsValid(UUECS3GameInstance::Instance->CfgManager), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance->CfgManager == nullptr"));\
	const UConfigTable* table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(TableType);\
	TArray<RowClass*> RowArray;\
	table->GetAllRows(RowArray);\
	for (auto Row : RowArray)\
	{\
		if (Row->GetIsBackstageAsyncLoad())\
		{\
			UUECS3GameInstance::Instance->ResourceManager->BackstageAsyncLoad_ObjectPath(Row->Attribute);\
		}\
	}\
}

//后台加载永不释放的核心资源.
#define BackstageAsyncLoad_Table_Double(TableType, RowClass, Attribute1, Attribute2)\
{\
	checkf(IsValid(UUECS3GameInstance::Instance), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance == nullptr || Instance->ResourceManager == nullptr"));\
	checkf(IsValid(UUECS3GameInstance::Instance->ResourceManager), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance->ResourceManager == nullptr"));\
	checkf(IsValid(UUECS3GameInstance::Instance->CfgManager), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance->CfgManager == nullptr"));\
	const UConfigTable* table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(TableType);\
	TArray<RowClass*> RowArray;\
	table->GetAllRows(RowArray);\
	for (auto Row : RowArray)\
	{\
		if (Row->GetIsBackstageAsyncLoad())\
		{\
			UUECS3GameInstance::Instance->ResourceManager->BackstageAsyncLoad_ObjectPath(Row->Attribute1);\
			UUECS3GameInstance::Instance->ResourceManager->BackstageAsyncLoad_ObjectPath(Row->Attribute2);\
		}\
	}\
}

//后台加载永不释放的核心资源.
#define BackstageAsyncLoad_Table_Three(TableType, RowClass, Attribute1, Attribute2, Attribute3)\
{\
	checkf(IsValid(UUECS3GameInstance::Instance), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance == nullptr || Instance->ResourceManager == nullptr"));\
	checkf(IsValid(UUECS3GameInstance::Instance->ResourceManager), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance->ResourceManager == nullptr"));\
	checkf(IsValid(UUECS3GameInstance::Instance->CfgManager), TEXT("FStrToClass::StarBackstageAsyncLoad()  Instance->CfgManager == nullptr"));\
	const UConfigTable* table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(TableType);\
	TArray<RowClass*> RowArray;\
	table->GetAllRows(RowArray);\
	for (auto Row : RowArray)\
	{\
		if (Row->GetIsBackstageAsyncLoad())\
		{\
			UUECS3GameInstance::Instance->ResourceManager->BackstageAsyncLoad_ObjectPath(Row->Attribute1);\
			UUECS3GameInstance::Instance->ResourceManager->BackstageAsyncLoad_ObjectPath(Row->Attribute2);\
			UUECS3GameInstance::Instance->ResourceManager->BackstageAsyncLoad_ObjectPath(Row->Attribute3);\
		}\
	}\
}