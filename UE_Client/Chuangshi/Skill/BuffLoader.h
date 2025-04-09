#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "Skill/SkillBase/buff.h"
#include "BuffLoader.generated.h"


/*
* 文件名称：BuffLoader.h
* 功能说明：buff实例创建文件
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-20
*/

UCLASS(BlueprintType)
class UBuffLoader :public UCS3Object
{
	GENERATED_BODY()
public:
	~UBuffLoader();

public:
	/*获得/创建单例*/
	static UBuffLoader* GetInstance();

	void loadAllBuff();

	UBuff* CreateBuff(FString BuffID, const FBUFF_TABLE_DATA * buffDat);

	UBuff* getBuffByID(int32 BuffID);

private:
	UBuffLoader();


private:
	UPROPERTY()
	TMap<int32, UBuff*> _buffs;
};


