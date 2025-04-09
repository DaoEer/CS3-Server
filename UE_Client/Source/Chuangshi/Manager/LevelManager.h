// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Object.h"
#include "GameData/CS3Object.h"
#include "GameData/LevelHashMap.h"
#include "UObject/UObjectGlobals.h"
#include "LevelManager.generated.h"

/*
* 文件名称：LevelManager.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2016-09-12
*/
/**
 *关卡管理器
 */

class CS3Entity;
class AInWorldLevel;
class ALoginLevel;
class ASelectCampLevel;
class APersonalizeLevel;
class ANewCreateRoleLevel;
class ANewSelectRoleLevel;
class AInWorldStreamLevel;
class AClothesHostsLevel;

UCLASS(Blueprintable)
class CHUANGSHI_API ULevelManager : public UCS3Object
{
	GENERATED_BODY()
public:
	friend class AInWorldLevel;
	friend class ALoginLevel;
	friend class ASelectCampLevel;
	friend class APersonalizeLevel;
	friend class ANewCreateRoleLevel;
	friend class ANewSelectRoleLevel;
	friend class AInWorldStreamLevel;
	friend class AClothesHostsLevel;
public:
	ULevelManager();
	~ULevelManager();
	static ULevelManager* GetInstance();
	virtual void BeginDestroy()override;

	UFUNCTION(BlueprintCallable, Category = "LevelManager")
	void LoadSceneAsyc(const FName& InSpaceScriptID, const LOADING_MODE_ENUM loadingMode = LOADING_MODE_ENUM::LOADING_MODE_NULL);

	void TeleportPlaneLevel(const FName &InSpaceScriptID);

	void TeleportLoginLevel(); ///<跳转到登录关卡

	UFUNCTION(BlueprintCallable, Category = "LevelManager")
		void TeleportSelectRoleLevel(); ///<跳转到角色选择关卡


	UFUNCTION(BlueprintCallable, Category = "LevelManager")
		void TeleportSelectCampLevel(); ///<跳转到阵营选择关卡


	UFUNCTION(BlueprintCallable, Category = "LevelManager")
		void TeleportCreateRoleLevel(); ///<跳转到角色创建关卡


	UFUNCTION(BlueprintCallable, Category = "LevelManager")
		void TeleportNieLianLevel(); ///<跳转到捏脸关卡

	UFUNCTION(BlueprintCallable, Category = "LevelManager")
		void TeleportChangeClothesLevel(); ///<跳转到更衣关卡

	void TeleportNormalLevel(const FName &InSpaceScriptID, const LOADING_MODE_ENUM loadingMode);//跳转到普通关卡

	void AgainTeleportSubStreamLevel(const FName &InSpaceScriptID);//切换关卡

private:
	void LoadSamelevel(const FLEVEL_HASHMAP * newlevelHash, const LOADING_MODE_ENUM loadingMode);

	//不同关卡的加载
	void LoadDifferentlevel(const FLEVEL_HASHMAP * newlevelHash);

	////<传送到对应流关卡的子关卡
	void TeleportSubStreamLevel();

	//加载位面关卡完毕回调
	void OnEndTeleportPlaneLevel();
	
	//加载登录关卡完毕回调
	void OnEndTeleportLoginLevel();

	//加载角色选择关卡完毕回调
	void OnEndTeleportSelectRoleLevel();

	//加载阵营选择关卡完毕回调
	void OnEndTeleportSelectCampLevel();

	//加载角色创建关卡完毕回调
	void OnEndTeleportCreateRoleLevel();

	//加载普通关卡开始回调
	void OnBeginTeleportNormalLevel();

	//加载普通关卡完毕回调
	void OnEndTeleportNormalLevel();

	//加载捏脸关卡完毕回调
	void OnEndTeleportPersonalizeLevel();

	//加载更衣关卡完毕回调
	void OnEndTeleportChangeClothesLevel();

	void LoadLevelAsync(const FString& LevelName, FName OldLevelName,FName CurLevelName);
	void AsyncPackageCallback(const FName& PackageName, UPackage * LevelPackage, EAsyncLoadingResult::Type Result,  FName LevelName, FName OldLevelName, FName CurLevelName, TWeakObjectPtr<ULevelStreaming> LevelStreamingPtr);
	void LoadSubLevelAsync(const FName& LevelName, FName OldLevelName, FName CurLevelName);
public:

	UFUNCTION(BlueprintPure, Category = "LevelManager")
		FName GetCurrLevelName() const;
	UFUNCTION(BlueprintCallable, Category = "LevelManager")
		void AddWaitingEnterList();
	
	void OnSetSpaceData(uint32 spaceID, const FString& key, const FString& value, const LOADING_MODE_ENUM loadingMode= LOADING_MODE_ENUM::LOADING_MODE_NULL);

	void RequestEnterScenes(CS3Entity* obj);

	void RequestLeaveScenes(CS3Entity* obj);

	void GameObjectEnterScenes();

	void OnTimerEnterScenes();///<定时器加载关卡

	void SetSpecialEmptyLogicLevel(const FString& LogicLevel);

	void SetIsLoadNineSubLevelAfterSplit(bool IsLoaded);

	void SetIsLoadAllOtherLevelAfterSplit(bool IsLoaded);

	bool GetIsLoadNineSubLevelAfterSplit();

	bool GetIsLoadAllOtherLevelAfterSplit();

	FString GetSpecialEmptyLogicLevel();

	void SetCurrentLoadCompletedLevel(const FString& LevelName);

	bool IsLevelLoadCompleted();
	/*-----------------------其他------------------------------------*/
	///<获取关卡对应的HashMap数据
	const FLEVEL_HASHMAP * GetLevelHashMapData(const FName &InSpaceScriptID);

	FName GetSubStreamLevelName() { return SubStreamLevel_; };

protected:
	UPROPERTY(BlueprintReadOnly)
		FName oldLevel_ = TEXT("");///<旧的关卡名
	UPROPERTY(BlueprintReadOnly)
		FName newLevel_ = TEXT("");///<新的关卡名
	UPROPERTY(BlueprintReadOnly)
		FName currLevel_ = TEXT("");///<当前关卡名
	UPROPERTY(BlueprintReadOnly)
		FName spaceScriptID = TEXT("");///<当前服务地图ID
	UPROPERTY(BlueprintReadOnly)
		FString CurrentLoadCompletedLevel = TEXT("");///<当前加载完成的关卡名
	UPROPERTY(BlueprintReadOnly)
		FName SubStreamLevel_ = TEXT("");///<流关卡的子关卡名
public:
	int32 GetUUID() { UUID++; return UUID; };///<获取流关卡UUID
	bool GotoIsPlane = false;//当前是否为goto指令进入位面
	
private:
	FTimerHandle TimerHander;///<定时器

	EGAMELEVELTYPE GamelevelType;	//游戏关卡类型

	TArray<CS3Entity*> mWaitingEnterScenes;///<请求加载关卡队列
	FTimerHandle LoaderTimerHander;///<加载定时器
	int32 UUID = 0;///<流关卡UUID

#if WITH_EDITOR
	TSubclassOf<AActor> m_bpCloseTrueSky;		//用来处理TrueSky问题
#endif

	FString SpecialEmptyLogicLevel = TEXT("");
	bool IsLoadNineSubLevelAfterSplit = true;
	bool IsLoadAllOtherLevelAfterSplit = true;
	bool IsTeleportSubStreamLevelCompleted = false;

	TArray<ULevelStreaming*> StreamingLevels;///< 异步加载资源关卡下的子关卡
};
