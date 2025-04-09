// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/LocalDataSave/LocalData.h"
#include "GameData/LocalDataSave/LocalUserSettingData.h"
#include "GameData/LocalDataSave/LocalTongSettingData.h"
#include "GameData/LocalDataSave/LocalRelationData.h"
#include "GameData/LocalDataSave/LocalKitbagData.h"
#include "GameData/LocalDataSave/LocalMessageData.h"
#include "GameData/LocalDataSave/LocalAutoFightData.h"
#include "GameData/CS3Object.h"
#include "GameData/LocalDataSave/LocalChatSettingData.h"
#include "GameData/LocalDataSave/LocalStortcutKeyData.h"
#include "Kismet/GameplayStatics.h"
#include "LocalDataSaveManager.generated.h"

/*
* 文件名称：LocalDataSaveManager.h
* 功能说明：用于统一得管理本地存档得加载和保存
* 文件作者：shuqingping
* 目前维护：yanjingxin
* 创建时间：2018-04-23
*/

UCLASS()
class CHUANGSHI_API ULocalDataSaveManager : public UCS3Object
{
	GENERATED_BODY()
	
public:
	///初始化数据
	void Init();
	///玩家上线
	void OnPlayerEnterWorld();
	///玩家下线
	void OnPlayerLeaveWorld();

	///判断是否存在文件
	template<class T>
	bool DoesLocalFileExist(T* localData)
	{
		return UGameplayStatics::DoesSaveGameExist(localData->GetFileName(), 0);
	};

	///创建保存文件和加载文件数据 蓝图要用数据在直接在manager理操作
	template<class T>
	T* NewLocalDataFile()
	{
		T* NewLocalData = (T*)StaticConstructObject_Internal(T::StaticClass());

		if (DoesLocalFileExist<T>(NewLocalData))
		{
			T* LocadLocalData = Cast<T>(UGameplayStatics::LoadGameFromSlot(NewLocalData->GetFileName(), 0));
			if (!IsValid(LocadLocalData))	//文件坏掉的时候是Null
			{
				DeleteLocalDataFile(NewLocalData);//删除坏掉的文件
			}
			else
			{
				NewLocalData = LocadLocalData;
			}
		}
		return NewLocalData;
	};

	//保存文件
	template<class T>
	bool SaveLocalDataFile(T* localData)
	{
		return UGameplayStatics::SaveGameToSlot(localData, localData->GetFileName(), 0);
	};

	///删除文件
	template<class T>
	bool DeleteLocalDataFile(T* LocalData)
	{
		return UGameplayStatics::DeleteGameInSlot(LocalData->GetFileName(), 0);
	}
	
	///外部调用操作
	#pragma region 本地文件操作

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalDataFile();
	#pragma endregion

	#pragma region 用户文件操作

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool DeosLocalUserSettingDataExist();

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalUserSettingDataFile();
	#pragma endregion

	#pragma region 帮派文件操作

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool NewLocalTongSettingDataFile();
	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalTongSettingDataFile();
	#pragma endregion

#pragma region 关系系统文件操作

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool NewLocalRelationDataFile();
	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalRelationDataFile();
#pragma endregion

#pragma region 物品本地数据

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalItemDataFile();
#pragma endregion

#pragma region 自动战斗文件操作
	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool NewLocalAutoFightDataFile();
	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalAutoFightDataFile();
#pragma endregion

#pragma region 聊天本地数据

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalChatSettingDataFile();
	void InitLocalChatSettingData();
#pragma endregion

#pragma region 今日不再提示本地数据

	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		void InitLocalMessageDataFile();
	UFUNCTION(BlueprintCallable, Category = "LocalDataSaveManager")
		bool SaveLocalMessageDataFile();
#pragma endregion

#pragma region 快捷键本地数据
	bool SaveLocalStortcutKeyDataFile();
	void InitLocalStortcutKeyData();
#pragma endregion

public:
	static ULocalDataSaveManager* GetInstance();
public:
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalData*					LocalData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalUserSettingData*		LocalUserSettingData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalTongSettingData*		LocalTongSettingData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalRelationData*			LocalRelationData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalKitbagData*			LocalKitbagData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalAutoFightData*		LocalAutoFightData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalChatSettingData*		LocalChatSettingData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalStortcutKeyData*		LocalStortcutKeyData;
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = LocalDataSaveManager)
	ULocalMessageData*			LocalMessageData;
};
