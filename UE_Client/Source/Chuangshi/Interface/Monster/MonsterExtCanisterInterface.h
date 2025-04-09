// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtCanisterInterface.generated.h"

/*
* 文件名称：MonsterExtCanisterInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-17
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtCanisterInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	UMonsterExtCanisterInterface();

	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtCanisterInterface'"); } //获取蓝图对象路径

	UFUNCTION(BlueprintCallable)
		void AddTrap();

	void OnPlayerBeginOverlap();
	void OnPlayerEndOverlap();

	// 操作攻城梯
	UFUNCTION(BlueprintCallable)
		void OperationCanister(const int32& EntityID_);
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnOperationCanister(const int32& Ammo, float CdTime);
	virtual void InitBlueCB() override;

};