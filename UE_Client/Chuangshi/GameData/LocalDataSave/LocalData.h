// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CsvTableRowBase.h"
#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "LocalData.generated.h"

/**
* 文件名称：LocalData.h
* 功能说明：本地数据结构配置
* 文件作者：shuqingping
* 目前维护：shuqingping
* 创建时间：2018-04-23
*/

 /**
 *剧情预加载类型
 */

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPRELOADSTORY_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///地图名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName MapName;
	/// 地图描叙
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MapDes;
	/// 任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QuestId;
	/// 任务状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QuestState;
	///任务目标
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TasksState;
	///是否副本预加载
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bSpacePreLoad;
	/// 任务名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QuestDes;
	/// 剧情ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StoryId;
	/// 重复剧情
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Repeat;
	/// 播放位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PlayPos;
	/// 剧情描叙
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StoryDes;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		CheckPosDirCheckData(ResultInfo, PlayPos, "PlayPos");

		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
*	
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPRELOADSTORY_SAVEDATA
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> StoryIDs;
};

/**
*
*/
UCLASS()
class CHUANGSHI_API ULocalData : public USaveGame
{
	GENERATED_BODY()
		ULocalData() :FileName(TEXT("_LocalData")) {};
public:
	/**
	*更新本地登陆数据
	*
	*@param inServerIp 服务器IP
	*@param inAccount 账号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalDataManager|ULocalData")
		void UpdateLoginDataToFile(const FString& inServerIp, const FString& inAccount);

	/**
	*保存本地玩家DBID和Index数据
	*
	*@param dbid 玩家DBID
	*@param pos 玩家的Index
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalDataManager|ULocalData")
		void UpdateRolePosToRolePosMap(const FString& dbid, const int32& pos);

	/**
	*根据玩家DBID获取玩家Index数据
	*
	*@param dbid 玩家DBID
	*
	*@return int32 玩家Index
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalDataManager|ULocalData")
		int32 GetRolePosByDbid(const FString& dbid);

	/**
	*获取剧情数据是否成功
	*
	*@param Key 剧情名
	*
	*@return bool 获取剧情数据成功返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintPure, Category = "LocalDataManager|ULocalData")
		bool GetPreLoadStoryLocalData(const FString& Key, const FString StoryID);


	UFUNCTION(BlueprintCallable, Category = "LocalDataManager|ULocalData")
		const FString& GetFileName();

	void OnPlayerEnterWorld();
private:
	UFUNCTION()
		void UpdatePreLoadStoryLocalData(int32 QuestID);
private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字
	
public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		TArray<FString> LoginAccounts;///<登陆账号表

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString LoginServerIp = "127.0.0.1";///<默认登陆IP

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = Basic)
		TArray<FString> EnterRoleDbids;///<进入游戏玩家的DBID表

	UPROPERTY(VisibleAnywhere)
		TMap<FString, int32> AllRolePosMap;///<所有玩家位置表

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		TMap<FString, FPRELOADSTORY_SAVEDATA> PreLoadStoryData;///<本地剧情数据
};
