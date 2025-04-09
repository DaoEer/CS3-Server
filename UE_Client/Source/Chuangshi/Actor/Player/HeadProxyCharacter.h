#pragma once
#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "GameData/VoiceData.h"
#include "Engine/StreamableManager.h"
#include "LevelSequenceActor.h"
#include "NoExportTypes.h"
#include "../ServerCharacter.h"
#include "HeadProxyCharacter.generated.h"

/*
* 文件名称：HeadProxyCharacter.h
* 功能说明：用于半身像对话，动态半身像功能
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2018-10-09
*/


UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AHeadProxyCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	AHeadProxyCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void OnCreateModelOver() override;
	virtual void OnCreateApperanceOver() override;

public:
	///通过HeadID更换模型
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void ChangeModelByHeadID(FString HeadID);
	///通过半身像模型数据更换模型
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void ChangeModelByHeadModelData(FHEAD_MODEL_DATA HeadModelData);
	///通过HeadID更换动作
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void TargetPlayAction(AGameCharacter* Target,bool IsPlayer, FString HeadModelID);
	///通过半身像模型数据更换动作
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void TargetPlayActionByHeadModelData(AGameCharacter* Target, bool IsPlayer, FHEAD_MODEL_DATA HeadModelData);

	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void PlayAction_BP(AGameCharacter* Target,FName ActionID);

	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void ResetCharacterAction();

	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void PlayParticleModel(AGameCharacter* Target, TArray<FHEAD_MODEL_EFFECT_DATA> EffectData);
	///测试用，不进游戏，没有玩家
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		void PlayParticleModelTest(AGameCharacter* Target, TArray<FHEAD_MODEL_EFFECT_DATA> EffectData);

	UFUNCTION(BlueprintPure, Category = "HeadProxyCharacter")
	float GetSequenceRate();
	UFUNCTION(BlueprintPure, Category = "HeadProxyCharacter")
	FString GetModelID();
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
	void ResetModelData();


protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	FName CurCharacterActionID;///玩家当前动画数据
	UPROPERTY()
	AGameCharacter* CurCharacter;///所有修改动作了的actor

private:
	void SetForceMipStreaming(bool IsForceMipStreaming);

	void StartModelAction(FHEAD_MODEL_DATA HeadModelData, AGameCharacter* Target);
	void StartHeadModelAction(FHEAD_MODEL_DATA HeadModelData);
	void ChangeModel(FHEAD_MODEL_DATA HeadModelData);
	void PlayParticle(AGameCharacter* Target, ACharacter* Player, TArray<FHEAD_MODEL_EFFECT_DATA> EffectData);
	
private:
	FStreamableManager StreamManager;///<资源流管理器
	FTimerHandle EffectEventHandle;///特效事件定时器
	FTimerHandle ModelActionEventHandle;///<模型事件定时器
	FTimerHandle HeadModelActionEventHandle;///<半身像事件定时器

	TArray<int32> EffectArray;
	bool LoadISOver = false;
	FName BustActionID;///半身像动画储存
	FName BustBackActonID;///半身像背景动画储存
	int32 ActionIndex;///动画播放序列
	int32 HeadActionIndex;///半身像动画播放序列
	int32 EffectIndex;///特效播放序列
};
