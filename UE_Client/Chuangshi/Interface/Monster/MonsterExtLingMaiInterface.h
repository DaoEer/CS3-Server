// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtLingMaiInterface.generated.h"

/**
* 文件名称：MonsterExtLingMaiInterface.h
* 功能说明：
* 文件作者：fangpengjun
* 目前维护：fangpengjun
* 创建时间：2021-01-19
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtLingMaiInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtLingMaiInterface();
	~UMonsterExtLingMaiInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtLingMaiInterface'"); } //获取蓝图对象路径
	virtual void InitBlueCB() override;
	void onEnterWorld() override;
	void onLeaveWorld() override;
	
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterExtLingMaiInterface")
	void OnRep_xianDamage();
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterExtLingMaiInterface")
	void OnRep_moDamage();
	
	void LingMaiBossHPChanged();

private:
	int32 xianDamage = 0;
	int32 moDamage = 0;		//0:未被占领  1：玩家占领  2：boss占领	
};
