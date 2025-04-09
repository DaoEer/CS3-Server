// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/LevelScriptActor.h"
#include "CS3Base/BaseWindow.h"
#include "Entity/Alias.h"
#include "GameData/RoleInfo.h"
#include "GameData/CharacterData.h"
#include "CS3LevelScriptActor.generated.h"

/*
* 文件名称：CS3LevelScriptActor.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：wuxiaoou
* 创建时间：2018-04-28
*/

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ACS3LevelScriptActor : public ALevelScriptActor
{
	GENERATED_BODY()
private:
	// Fileds
	// Functions

public:
	// Fileds 

	// Functions
	ACS3LevelScriptActor(const FObjectInitializer& ObjectInitializer);
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	//use for Cinematics event
	UFUNCTION(BlueprintCallable, Category = "Story")
		void NotifyServerEvent();

	//use for Cinematics event
	UFUNCTION(BlueprintCallable, Category = "Story")
		void PlayVoiceWords();

	UFUNCTION(BlueprintCallable, Category = "Story")
		void PlayTextEvent();

	UFUNCTION(BlueprintCallable, Category = "Story")
		void PlayRedrawViewports();///<BlueprintCallable， 事件：停止渲染

	UFUNCTION(BlueprintNativeEvent, Category = "Story")
		void StoryEventByParams(CSTORY_EVENT_PARAM_TYPE_ENUM EventName, const FString& Param1, const FString& Param2, const FString& Param3, const FString& Param4);

	UFUNCTION(BlueprintCallable, Category = "Story")
		void PlayAnimEvent();

	UFUNCTION(BlueprintCallable, Category = "Story")
		void StopAnimEvent();

	virtual void CreateDynamicRes();

	virtual void OnCreateModelFinished();

	virtual bool CheckLoginRun();		//是从登录进来的，还是直接在某关卡播放
	
	void OnLoadLevelDelay();

	virtual void OnLoadLevelFinished();

	void UpdateSelectWndAndModel(AliasRoleInfoTmap& inst);///<更新角色选择界面，并创建台子和角色模型



	/**
	*BlueprintCallable，创建角色
	*
	*@param playerName 玩家名
	*@param profession 玩家职业
	*@param camp 玩家阵营
	*@param gender 玩家性别
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void CreateRole(FString playerName, int32 profession, int32 camp, int32 gender);

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void OnChangeCreateRole(int32 Profession, int32 Gender);

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void OnChangeSelectRole(const FString& DBID);

	/**
	*增加一个玩家信息
	*
	*@param inst 服务器传过来的玩家信息
	*
	*@return 无
	*/
	void AddRoleInfo(AliasRoleInfo& inst);

	/**
	*删除玩家
	*
	*@param dbid 玩家DBID
	*
	*@return 无
	*/
	void DelRoleInfo(uint64 dbid);

	/**
	*BlueprintCallable，删除角色
	*
	*@param dbid 玩家名
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void DeleteRole(FString dbid);

	/**
	*输入礼包码
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void RequestActivationKey(const FString& key, const FString& playerName);

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void PlayCG(); //播放CG

		//UFUNCTION(BlueprintCallable, Category = "LoginManager")
	void OnAddAccount(const uint64& DBID);

	//UFUNCTION(BlueprintCallable, Category = "LoginManager")
	void OnDelAccount(const uint64& DBID);

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		TArray<AActor*> GetAccountActors();

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		UBaseWindow* GetSelectRoleWidget();//获取角色选择界面

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		int32 GetSelectRoleIndex();//获取角色选择界面

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void SelectRoleByTabKey();///<Tab切换角色

	void ReceiveWattingInfo(const int32& rank, const float& time, const int32& count);

	void OnCancelLoginQueue(const int32& isInQueue);

private:
	void StartShowLoginLevel();
	void OnLanderLandGame();//通过登陆器进入游戏 
	void HideLoginLevel();

private:
	//用于加载多个资源关卡，给一个回调
	TArray<FName> NeedToLoadLevels;
	FLatentActionInfo RecordLatentInfo;
	FTimerHandle DelayHandleLevelLoad;

protected:
	FTimerHandle DelayLoadFinishedHandle;

};
