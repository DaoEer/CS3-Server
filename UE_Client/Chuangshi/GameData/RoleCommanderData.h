#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "RoleCommanderData.generated.h"

/**
* 文件名称：RoleCommanderData.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-2-25
*/



USTRUCT(BlueprintType)
struct CHUANGSHI_API FROLE_COMMANDER_FOLLOW_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///起始距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float StartDistance = 3.0;
	///小兵间隔距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float AdjacentDistance = 2.0;
	///每排人数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int NumPerRow;

	int Layer = 1;
	float Distance = 200.0;
	float Extension = 300.0; //起始距离
	int IndexMax = 5;
	int Index = 0;

};




///部队数据
USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FARMS_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	//左卫
		FString LeftGuardScriptID;
		UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "LeftGuardEntityID")
			int32 LeftGuardEntityID;
	//右卫
		FString RightGuardScriptID;
		UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "RightGuardEntityID")
			int32 RightGuardEntityID;
	///士兵scriptID
		UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "SoldierScriptID")
			FString SoldierScriptID;
		UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "SoldierEntityIDList")
			TArray<int32> SoldierEntityIDList;
		void Reset()
		{
			LeftGuardScriptID = "";
			LeftGuardEntityID = 0;
			RightGuardScriptID = "";
			RightGuardEntityID = 0;
			SoldierScriptID = 0;
			SoldierEntityIDList.Empty();
		}

};



enum FSoldierCategory
{
	Normal,
	Sodier,
	LeftGuard,
	RightGuard,
};
