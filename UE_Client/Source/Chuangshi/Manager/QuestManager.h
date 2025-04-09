// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/Quest/QuestBase/QuestBase.h"
#include "GameData/GameDeFine.h"
#include "GameData/Quest/ClientQuestInfo.h"
#include "QuestManager.generated.h"

/*
* 文件名称：QuestManager.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-18
*/

DECLARE_MULTICAST_DELEGATE_OneParam(FDelQuestDelegate,int32);
/**
 * 任务管理类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UQuestManager : public UCS3Object
{
	GENERATED_BODY()
	
public:
	static UQuestManager* GetInstance();
	virtual void onEnterWorld();            ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld();            ///< 当Entity离开世界（被销毁时）时，此方法被调用
	void ClearQuestLog();					///<清除任务描述
	void ClearQuestLogByType(const FString& type);				/// 通过类型清除任务描述 
	/**
	* BlueprintCallable，增加任务
	*
	* @param  QuestInfo	任务信息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void AddQuest(const FString & JsonStr, const QUEST_TYPE type,const int32 ID);

	/**
	* BlueprintCallable，删除任务
	*
	* @param  QuestID	任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void DelQuest(const int32& QuestID);

	/**
	* BlueprintCallable，是否有QuestID的任务
	*
	* @param  QuestID	任务ID
	*
	*@return bool 有QuestID的任务返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		bool HasQuest(const int32& QuestID);

	/**
	* BlueprintCallable，更新任务
	*
	* @param  QuestID	任务ID
	* @param  TaskID	任务目标ID
	* @param  Progress	任务进度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void UpdateQuest(const int32& QuestID,const int32& TaskID, const int32& Progress);

	/**
	* BlueprintCallable，设置任务目标完成
	*
	* @param  QuestID	任务ID
	* @param  TaskID	任务目标ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void SetQuestTaskDone(const int32& QuestID, const int32& TaskID);
	/**
	* BlueprintCallable，提交任务
	*
	* @param  QuestID	任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void CommitQuest(const int32& QuestID);

	/**
	* BlueprintCallable，完成任务
	*
	* @param  QuestID	任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void CompleteQuest(const int32& QuestID);

	/**
	* BlueprintCallable，移除任务描述
	*
	* @param  LogStr	任务描述
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void OnRecvQuestLog(const FString& LogStr);

	/**
	*根据任务ID删除某个已完成任务日志
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void onRemoveQuestLog(const int32& QuestID);

	/**
	* BlueprintPure，QuestID的任务是否是Type类型
	*
	* @param  QuestID	任务ID
	* @param  Type	任务类型
	*
	*@return bool QuestID的任务是Type类型返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintPure, Category = "QuestManager")
		bool IsQuestType(const int32& QuestID, int32 Type);

	/**
	* BlueprintPure，QuestID的任务是否是Status状态
	*
	* @param  QuestID	任务ID
	* @param  Status	任务状态
	*
	*@return bool QuestID的任务是Status状态返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintPure, Category = "QuestManager")
		bool IsQuestStatus(const int32& QuestID, int32 Status);

	/**
	* BlueprintPure，QuestID的任务目标TaskID是否是Status状态
	*
	* @param  QuestID	任务ID
	* @param  TaskID	任务目标ID
	* @param  Status	任务状态
	*
	*@return bool QuestID的任务目标TaskID是Status状态返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintPure, Category = "RoleQuestInterface")
		bool IsTaskStatus(const int32& QuestID, const int32& TaskID, int32 Status);

	/**
	* BlueprintPure，查询QuestID的任务目标TaskID的优先级Priority
	*
	* @param  QuestID	任务ID
	* @param  TaskID	任务目标ID
	*
	*@return int32 QuestID的任务目标TaskID的优先级Priority
	*/
	int32 GetTaskPriority(const int32& QuestID, const int32& TaskID);

	/**
	* BlueprintPure，根据QuestID获取任务数据
	*
	* @param  QuestID	任务ID
	*
	*@return UQuestBase* 任务数据
	*/
	UFUNCTION(BlueprintPure, Category = "QuestManager")
		UQuestBase* GetQuestByID(const int32& QuestID );

	TArray<int32> GetQuestIDsByType(QUEST_TYPE Type);

	/**
	* BlueprintCallable，获取玩家身上所有任务ID
	*
	* @param  QuestID	任务ID
	*
	*@return UQuestBase* 任务数据
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestManager")
		void GetPlayerQuestIDs(TArray<int32>& AllQuests);

	const FCS3ClientQuestInfo* GetQuestConfig(const int32& QuestID);

	bool InQuestTable(int32  ID);
public:
	FDelQuestDelegate  OnDelQuestDelegate;///<删除任务
protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Quest")
	TMap<int32, UQuestBase*> QuestTable;	///<任务数据表
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Quest")
	TArray<int32> QuestLogger;	///<任务描述表

	//static UQuestManager* Instance;
};
