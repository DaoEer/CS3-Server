// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/GameDeFine.h"
#include "GameStatus.generated.h"

/*
* 文件名称：GameStatus.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：wuxiaoou
* 创建时间：2018-04-28
*/
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FInWorldLoadingOverDelegate);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FLoginLoadingOverDelegate);
class ULoginManager;

UCLASS(Blueprintable)
class CHUANGSHI_API UGameStatus : public UCS3Object
{
	GENERATED_BODY()
public:
	friend class ULevelManager;
	friend class ULoginManager;

public:
	UGameStatus();
	~UGameStatus();
	static UGameStatus* GetInstance();

	UFUNCTION(BlueprintCallable, Category = "GameStatus")
		EGameStatus GetCurrStatus() { return CurrStatus; };
	UFUNCTION(BlueprintCallable, Category = "GameStatus")
		EGameStatus GetLastStatus() { return LastStatus; };
	UFUNCTION(BlueprintCallable, Category = "GameStatus")
		bool IsCurrStatus(EGameStatus status);

	UFUNCTION(BlueprintImplementableEvent, Category = "GameStatus")
		void OnGameStatusChangeBP();

	UFUNCTION(BlueprintImplementableEvent, Category = "GameStatus")
		void BP_OnInWorldLoadingOver();
	void OnInWorldLoadingOver();

	UFUNCTION(BlueprintCallable, Category = "GameStatus")
		bool GetIsInWorldLoadingOver() { return IsInWorldLoadingOver; };
	void SetIsInWorldLoadingOver(bool bIsInWorldLoadingOver) { IsInWorldLoadingOver = bIsInWorldLoadingOver;	};

private:
	void ChangeStatus(EGameStatus status);

	bool CheckChangeStatus(EGameStatus InStatus);

	void OnChangeInWorldStatus();///<切换到InWorld状态

	void OnChangeTeleportStatus();///<切换到Teleport状态

	void OnChangeSelectRoleStatus();///<切换到选择角色状态

	void OnChangeSelectCreateRole();///<切换到创建角色状态

	void OnChangeSelectSelectCamp();///<切换到选择阵营状态

	void OnChangeLogin();///<切换到登录状态

	///<每个状态切换完成（除Teleport、Logoff、InWorld）后处理的事件
	void OnChangeOverEvent();
public:
	FInWorldLoadingOverDelegate InWorldLoadingOver;///<InWorld状态加载完成事件委托
	FLoginLoadingOverDelegate LoginLoadingOver;///<登录状态完成事件委托
private:
	EGameStatus CurrStatus; ///<当前状态
	EGameStatus LastStatus;///<上一个状态
	bool IsInWorldLoadingOver = false;

};
