#pragma once
#include "CoreMinimal.h"
#include "CombatDamager.h"
#include "GameData/CS3Object.h"
#include "CombatDamagerLoader.generated.h"

/*
* 文件名称：CombatDamagerLoader.h
* 功能说明：基准伤害值
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2020-8-22

*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCOMBAT_DAMAGER_DATA_PROFESSION
{
	GENERATED_BODY();
public:
	UPROPERTY()
		TMap<int32, FCOMBAT_DAMAGER_DATA> value;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UCombatDamagerLoader :public UCS3Object
{
	GENERATED_BODY()
public:
	~UCombatDamagerLoader();
	/*获得/创建单例*/
	static UCombatDamagerLoader* GetInstance();

	void loadAllData();

	FCOMBAT_DAMAGER_DATA GetCombatDamagerData(int32 Level, int32 Profession);

	
private:
	UCombatDamagerLoader();

	static UCombatDamagerLoader* Instance;
private:
	UPROPERTY()
	TMap<int32, FCOMBAT_DAMAGER_DATA_PROFESSION> CombatDamagerDataDic;

};

UCombatDamagerLoader* UCombatDamagerLoader::Instance = nullptr;