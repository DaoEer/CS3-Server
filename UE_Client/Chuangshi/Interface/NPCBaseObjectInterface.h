// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/GameObjectInterface.h"
#include "NPCBaseObjectInterface.generated.h"


class AServerCharacter;
/*
* 文件名称：NPCBaseObjectInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UNPCBaseObjectInterface : public UGameObjectInterface
{
	GENERATED_BODY()
	typedef UGameObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCBaseObjectInterface();
	~UNPCBaseObjectInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCBaseObjectInterface'"); } //获取蓝图对象路径
	/**
	*设置模型编号
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|NPCBaseObjectInterface")
	virtual void OnRep_modelNumber() override;

	/**
	*同步玩家位置
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|NPCBaseObjectInterface")
	virtual void OnRep_SyncPosClient()override;

	/**
	*播放出生前光效
	*
	*@param actor ，actor（const AActor*）
	*
	*@return 无
	*/
	void PlayBeforeSpawnEffect(AServerCharacter* actor);

	/**
	*更新和显示对象
	*
	*@param actor ，actor（const AActor*）
	*
	*@return 无
	*/
	void ShowAndUpdataActor(AServerCharacter* actor);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_gossipWith();
	
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "NPCBase")
		FString uname;

	virtual void Set_UName(const FString& newVal, const FString& oldVal);

protected:
	virtual void onEnterWorld() override;     ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld() override;     ///< 当Entity离开世界（被销毁时）时，此方法被调用

private:
	UPROPERTY()
		FTimerHandle EffectTimerHandle;
};
