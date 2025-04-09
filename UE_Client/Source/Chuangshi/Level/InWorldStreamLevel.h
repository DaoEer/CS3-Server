// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Level/InWorldLevel.h"
#include "InWorldStreamLevel.generated.h"

DECLARE_MULTICAST_DELEGATE_OneParam(FLoadNextSubLevelFinishedDelegate, FString);///<

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AInWorldStreamLevel : public AInWorldLevel
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;

	void ChangeToNextSubLevel(FName LevelName);///<切换子关卡

	bool GetIsNextSubLevelFinished() { return IsLoadNextSubLevelFinished; };
private:
	virtual void OnLoadLevelFinished() override;///<关卡加载完成

	void LoadDefaultSubLevel();///<加载默认子关卡
	UFUNCTION()
		void LoadDefaultSubLevelFinished();///<加载默认子关卡完成
	UFUNCTION()
		void DelayNotifyLoadDefaultSubLevelFinished();///<加载默认子关卡完成

	void LoadNextSubLevel(bool bIsShow = false);///<加载下一个子关卡
	UFUNCTION()
		void LoadNextSubLevelFinished();///<加载下一个子关卡完成

	void UnLoadSubLevelByLevelName(FName LevelName);///<卸载子关卡
	UFUNCTION()
		void UnLoadSubLevelFinished();///<卸载子关卡完成

	void LoadSubLevelByLevelName(const FName LevelName, bool bMakeVisibleAfterLoad, bool bShouldBlockOnLoad, FName ExecutionFunction);///<加载子关卡

	void UpdateSubLevelVisiblity(FName VisibleLevelName,FName InvisibleLevelName);///<更新子关卡的可见性	
	UFUNCTION()
		void UpdateSubLevelVisiblityFinished(float FinishedTime=2.0f);///<显示子关卡完成

	void SetNextSubLevelName();///<设置下个子关卡的名字

	UFUNCTION()
		void PostChangeInWorldOver();///<切换到InWard状态后事件
	bool IsCompareLevelManagerSubStreamLevel(FName LevelName);////<是否等于LevelMananger的Level即是否为主场景

	void LoadLevelStreamingByLevelName(FName LevelName);///<加载包含LevelName的流关卡

	void UpdateStreamingVolume();///<更新流送体积

	void DelaySetInvisibleStreamingLevels();///<每一帧隐藏一个流关卡
public:
	FLoadNextSubLevelFinishedDelegate LoadNextSubLevelFinishedDelegate;///<下一个子关卡加载完成

private:
	FTimerHandle DelayNotifyLoadFinishedHandle;
	FString CurSubLevelName = TEXT("");///<当前的子关卡
	FString OldSubLevelName = TEXT("");///<前一个子关卡
	FString NextSubLevelName = TEXT("");///<下一个子关卡
	FString NewSubLevelName = TEXT("");///<新的子关卡
	bool IsLoadNextSubLevelFinished = false;///<下一个子关卡是否加载完成
	bool IsLoadSubLevelFinished = false;
	bool IsLoadStreamingLevel = false;///<是否加载主场景流关卡
	FVector LastEntitypostion = FVector::ZeroVector;
	UPROPERTY()
		TArray<ULevelStreaming*> InvisibleStreamingLevels;
};
