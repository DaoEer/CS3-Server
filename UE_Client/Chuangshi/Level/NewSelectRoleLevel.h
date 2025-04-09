// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Level/LoginSelectLevel.h"
#include "GameData/RoleCreateUIData.h"
#include "NewSelectRoleLevel.generated.h"

class ALoginCharacter;
/**
 * 
 */
UCLASS()
class CHUANGSHI_API ANewSelectRoleLevel : public ALoginSelectLevel
{
	GENERATED_BODY()
public:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void CreateDynamicRes() override;
	virtual void OnCreateModelFinished() override;
	//virtual void OnLoadLevelFinished() override;

	void ChangeSelectRole(const FString& DBID);

	UFUNCTION(BlueprintCallable, Category = "SelectRoleLevel")
		void AddAccountActor(FROLEINFO RoleInfo); ///<增加一个角色, -1表示需要自动查找没有使用的索引

	UFUNCTION(BlueprintCallable, Category = "SelectRoleLevel")
		void OnAddAccount(const FString& DBID);

	UFUNCTION(BlueprintCallable, Category = "SelectRoleLevel")
		void OnDelAccount(const FString& DBID);

	ALoginCharacter* GetActorByDBID(const uint64& dbid);//通过DBID获取BP_Account的Actor
	FROLEINFO GetRoleInfoByDBID(const uint64& dbid);

	void CloseLoadingWidget();///关闭加载进度条
	void CloseWidgetByTimeOut();///加载后30秒自动关闭进度条
	void StopMediaSkip();

private:
	UFUNCTION()
		void  OnSelectRoleByTabKey();///<在角色选择时按Tab选择角色

	UFUNCTION()
		void LoadBlockStreamLevelSelectFinished();///<流关卡四个场景加载完毕

	UFUNCTION()
		void OpenSelectLevel(FRoleCreateUIData RoleCreateUIData);///<打开选中的关卡

	UFUNCTION()
		void OpenSelectCamera(int32 Index, FRoleCreateUIData RoleCreateUIData);///<打开选中的关卡摄像机

	UFUNCTION()
		void OpenSelectRole(FString Dbid);///<打开选中的人物模型
	
	uint64 GetLastLoginDBID();///<获取当前登录角色上次进入游戏的角色的DBID

	int32 GetRowIndex(int32 Profession, int32 Gender, int32 Camp);///获取选中的索引FRoleCreateUIData的rowName[通过职业+性别+阵营转换过来]
	
public:
	UPROPERTY()
		TMap<int32, AActor *> CreateRoleCameras;//key 阵营+职业

	UPROPERTY(BlueprintReadOnly, Category = "SelectRoleLevel")
		TArray<AActor*> AccountActors; ///<创建的角色BP_Account的列表

	UPROPERTY(BlueprintReadOnly, Category = "SelectRoleLevel")
		int32 CurrSelectIndex;	//当前第一个角色的索引，从0开始

	UPROPERTY(BlueprintReadOnly, Category = "SelectRoleLevel")
		FString CurrDBID;

	int32 CreateFinishCount; //创建模型回调的次数

private:
	int32 LoadLevelIndex = 0;

};
