// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Level/CS3LevelScriptActor.h"
#include "InWorldLevel.generated.h"

/*
* 文件名称：InWorldLevel.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-06-21
*/

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AInWorldLevel : public ACS3LevelScriptActor
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;
	virtual void CreateDynamicRes() override;
	virtual void BeginDestroy() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void Tick(float DeltaSeconds) override;
	void LoadSubLevelsByPositionInInit(const FVector& Position);
	void UpdateSubLevelsByPosition(const FVector& Position);
	TArray<FString> GetCurrLoadedSubLevels();
	FString GetCurrentSubLevelByPosition(const FVector& Position);
	TArray<FString> GetNineSubLevelsByPosition(const FVector& Position);
	TArray<FString>	GetSubLevelByPosition(const FVector& Position, const int32& length);
	ULevelStreaming* FindSubLevelStreamingObject(FName SubLevel);
	TArray<FString> GetAllSubStreamingLevels();
	void AddAllSubLevelsByPosition(const FVector& Position);

	UFUNCTION()
	void LoadBlockStreamLevelFinished();

	
	void ShowLoadingWidget(); //显示加载进度条

	virtual void OnLoadLevelFinished() override;
	virtual bool CheckLoginRun()override;		//是从登录进来的，还是直接在某关卡播放

protected:
	TArray<FString> AllSubLevels;
	bool IsBlockLevelFinished = false;
	bool IsLoadLevelFinished = false;
private:
	TArray<FString> CurrentLoadedSubLevels;
	TArray<FString> SortedAllSubLevels;
	TArray<FString>	AllBlockLoadedSubLevels;	
	int32 LoadedBlockNum = 0;
	
	int32 SplitLength = 10000.0f;

};
