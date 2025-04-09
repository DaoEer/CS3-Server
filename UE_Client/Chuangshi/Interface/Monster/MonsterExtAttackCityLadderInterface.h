// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "GameData/Shape/BaseShape.h"
#include "GameData/CharacterData.h"
#include "MonsterExtAttackCityLadderInterface.generated.h"

/*
* 文件名称：MonsterExtAttackCityLadderInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-14
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtAttackCityLadderInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtAttackCityLadderInterface();

	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_MonsterExtAttackCityLadderInterface.BP_MonsterExtAttackCityLadderInterface_C'"); } //获取蓝图对象路径

	UFUNCTION(BlueprintCallable)
		void AddTrap();

	void OnPlayerBeginOverlap();
	void OnPlayerEndOverlap();

	// 操作攻城梯
	UFUNCTION(BlueprintCallable)
		void OperationLadder(const int32& EntityID_);

	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_CancelTrap();

	//服务器通知:攻城梯移动城墙边-移动结束通知
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_LadderMoveFinish(const FString& actionID);

	virtual void InitBlueCB() override;
private:
	UBaseShape* pShape; //交互陷阱
};