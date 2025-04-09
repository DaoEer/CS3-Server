// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Actor/GameCharacter.h"
#include "GameData/VoiceData.h"
#include "GameFramework/Character.h"
#include "ProxyCharacter.generated.h"

/*
* 文件名称：ProxyCharacter.h
* 功能说明：ProxyCharacter
* 文件作者：ranyuan	
* 目前维护：ranyuan
* 创建时间：2018-08-01
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AProxyCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	AProxyCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void OnCreateModelOver() override;
	virtual void OnCreateApperanceOver() override;

	/**
	*BlueprintCallable 创建此模型的外观，通过COPY的对象
	*
	*@param CopyCharacter 目标Actor
	*@param IsClientAppearance 是否copy客户端外观
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "ProxyCharacter")
		virtual void CreateModelAppearance(ACharacter * CopyCharacter, bool IsClientAppearance);

	UFUNCTION(BlueprintCallable, Category = "ProxyCharacter")
		void PlayAction_BP(FString InActionID);///<播放动作

	UFUNCTION(BlueprintCallable, Category = "ProxyCharacter")
		void HeadModelPlayAction_BP(TArray<FHEAD_BUST_MODEL_ACTION_DATA> HeadModelData);///<提供给半身像玩家播放动作接口

	UFUNCTION(BlueprintCallable, Category = "ProxyCharacter")
		void RestActionData();

	UFUNCTION(BlueprintCallable, Category = "ProxyCharacter")
		void UpdateModelApperance(int32 Camp, int32 Profession, TArray<UItemBase*> EquipArray,int32 Gender);///<更新模型以及外观

	UFUNCTION(BlueprintPure, Category = "ProxyCharacter")
		FString GetModelID();

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	
private:
	int32 ModelAcitonIndex;
	FTimerHandle ModelActionEventHandle;///<模型事件定时器
};
