// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/GameDeFine.h"
#include "GameData/Quest/CS3QuestInfo.h"
#include "GameData/Quest/CS3RewardInfo.h"
#include "GameData/TongDailyQuestData.h"
#include "RoleQuestInterface.generated.h"

/*
* 文件名称：RoleQuestInterface.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/
/**
 * 玩家任务接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleQuestInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleQuestInterface();
	~URoleQuestInterface();
	static FString GetName() { return TEXT("RoleQuestInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleQuestInterface.BP_RoleQuestInterface_C'"); } //获取蓝图对象路径

	
	virtual void PostInitProperties() override;


	/**
	*Define mothed
	*设置任务数据
	*
	*@param JsonStr 任务数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onSetQuestContent(const FString& JsonStr);

	/**
	*Define mothed
	*接受任务
	*
	*@param JsonStr 任务数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onAcceptQuest(const FString& JsonStr);

	/**
	*Define mothed
	*提交任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onCommitQuest(const int32& QuestID);

	/**
	*Define mothed
	*增加任务
	*
	*@param JsonStr 任务数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onAddQuest(const FString& JsonStr);

	/**
	*Define mothed
	*放弃任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onAbandonQuest(const int32& QuestID);

	/**
	*Define mothed
	*完成任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onQuestComplete(const int32& QuestID);

	/**
	*Define mothed
	*接收任务描述
	*
	*@param QuestLog 任务描述
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onRecvQuestLog(const FString& QuestLog);

	/**
	*Define mothed
	*根据任务ID删除某个已完成任务日志
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onRemoveQuestLog(const int32& QuestID);

	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onRemoveQuestLogByType(const FString& QuestType);


	/**
	*Define mothed
	*清空已完成任务日志
	*
	*@param 无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onClearQuestLog();
	/**
	*Define mothed
	*更新任务目标数据
	*
	*@param QuestID 任务ID
	*@param TaskID 任务目标ID
	*@param Progress 任务进度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void onUpdateQuestTask(const int32 & QuestID, const int32& TaskID, const int32& Progress);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void onQuestTaskFinish(const int32 & QuestID, const int32& TaskID);

	/**
	*任务QuestID的类型是否是Type类型
	*
	*@param QuestID 任务ID
	*@param Type 任务类型
	*
	*@return bool 任务QuestID的类型是Type类型返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		bool IsQuestType(const int32& QuestID, int32 Type);

	/**
	*任务QuestID的状态是否是Status状态
	*
	*@param QuestID 任务ID
	*@param Status 任务状态
	*
	*@return bool 任务QuestID的状态是Status状态返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		bool IsQuestStatus(const int32& QuestID, int32 Status);

	/**
	*任务QuestID的任务目标是否是Status状态
	*
	*@param QuestID 任务ID
	*@param TaskID 任务目标
	*@param Status 任务状态
	*
	*@return bool 任务QuestID的任务目标是Status状态返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		bool IsTaskStatus(const int32& QuestID, const int32& TaskID, int32 Status);

	/**
	*BlueprintImplementableEvent，设置任务数据
	*
	*@param QuestInfo 任务数据
	*@param NpcQuestID NPC任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnSetQuestContentBP(const FCS3QuestInfo& QuestInfo, const int32& NpcQuestID);
	/**
	*BlueprintImplementableEvent，接受任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnAcceptQuestBP(const int32& QuestID);

	/**
	*BlueprintImplementableEvent，提交任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnCommitQuestBP(const int32& QuestID);

	/**
	*BlueprintImplementableEvent，增加任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnAddQuestBP(const int32& QuestID);
	
	/**
	*BlueprintImplementableEvent，放弃任务
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnAbandonQuestBP(const int32& QuestID);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnQuestStatusChangeBP();///<BlueprintImplementableEvent，改变任务状态

	/**
	*BlueprintImplementableEvent，任务完成
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnQuestCompleteBP(const int32& QuestID);


	/**
	*BlueprintImplementableEvent，显示环任务奖励提示
	*
	*@param QuestID 任务ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void ShowLoopRewardTip(const FString& Msg, int32 Exp, int32 Money, int32 AddedMoney, int32 AddedExp);

	/**
	*BlueprintNativeEvent，显示帮会日常任务任务树
	*
	*@param AcceptIndex 接取任务的索引（如果是-1，则表示没有接取任务）
	*@param FinishQuestidData 完成的任务ID
	*@param TreeJson 任务树数据
	*@param TreeNodeMapQuest 任务树节点映射任务ID
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
	void OnRequestTongDailyQuest(const int16& AcceptIndex, const FVariant& FinishQuestidData, const FVariant& TreeJson, const FVariant& TreeNodeMapQuest);

	/**
	*BlueprintImplementableEvent，蓝图接收帮会日常任务树某一天的任务数据
	*
	*@param  Layer 任务树层级
	*@param TreeJson 任务树数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void BP_OnReceiveTongDailyQuest(int32 AcceptIndex, const TArray<int32>& FinishQuestIDs, const TArray<FTongDailyQuestTreeDATA>& DailyQuestDatas);

	/**
	*Define Method
	*BlueprintNativeEvent,帮会日常任务副本通关结算
	*@param Msg  描述
	*@param Statistics 统计数
	*@param rewardStr 奖励数据（0代表帮贡，1代表帮会资金，2：养兵经验，3：修为 格式：0:帮贡|1：帮会资金|2：养兵经验|3：修为）
	*@param gradeScore 评分
	@param buff buffID|buffID|...
	@param itemStr itemID:amount|itemID:amount|... 
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void ShowTongDailyQuestSpaceWin(const FString& Msg, const FString& Statistics, const FString& RewardStr, const int32& GradeScore, const int32& CountDown, const FString& itemStr, const FString& buff);

	/**
	*Define Method
	*BlueprintNativeEvent,客户端接收问题
	*@param:questID  任务ID
	*@param:currentQuestionID  问题ID
	*@param:currentDescription  问题描述
	*@param:currentOption  问题选项
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void OnReceiveTongKnowledge(const int32& questID, const int32& currentQuestionID, const FString& currentDescription, const FString& currentOption);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		void OnReceiveTongKnowledgeBP(const int32& questID, const int32& currentQuestionID, const FString& currentDescription, const TArray<FString>& currentOptionLists);
	/**
	*Define Method
	*BlueprintNativeEvent,客户端接收问题结果是否答对
	*
	*@param:currentQuestionID  问题ID
	*@param:Result  问题是否答对
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void OnKnowledgeAnswerResult(const int32& questionID, const uint8& Result);

	/**
	*Define Method
	*BlueprintNativeEvent,关闭帮会问答日常任务界面
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void CLIENT_CloseTongKnowledge();

	// 通过代理的方式实现
	//UFUNCTION(BlueprintImplementableEvent, Category = "RoleQuestInterface")
		//void OnUpdateTaskDatasBP(const int32& QuestID,const int32& TaskID, const int32& Progress);

#pragma region 传话任务相关
		/**
	*Define Method
	*BlueprintNativeEvent,开始传话
	*
	*@param:RootQuestID  根任务ID
	*@param:NpcSoundID  NPC开始对话ID
	*@param:StartSoundID  玩家开始对话ID
	*@param:Dialogue  传话内容
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void StartWhisperQuest(const int32& RootQuestID, const int32 & TaskID, const FString& NpcSoundID, const FString& StartSoundID, const FString& Dialogue);

	/**
	*Define Method
	*BlueprintNativeEvent,开启任务倒计时
	*
	*@param:StrTime 倒计时结束时间
	*@param:QuestID 根任务ID
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void StartTimeQuest( const FString& StrTime, const int32& QuestID);
	/**
	*Define Method
	*BlueprintNativeEvent,设置任务目完成
	*@param QuestID 任务ID
	*@param TaskID 任务目标
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void SetQuestTaskDone(const int32 & QuestID, const int32& TaskID);

	/*完成传话任务*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_completeWhisperQuest(const int32& RootQuestID, const int32 & TaskID, const int32& IsSucced);
	
	/**
	*Define Method
	*BlueprintNativeEvent,传话是否成功回调
	*
	*@param:QuestID  根任务ID
	*@param:TaskID  NPC开始对话ID
	*@param:isSucced  是否成功
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		void OnCompleteWhisperQuest(const int32& QuestID, const int32& TaskID, const uint8& IsSucced);
	
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void OnCompleteWhisperQuestBP(const int32& QuestID, const int32& TaskID, const bool IsSucced);
	
#pragma endregion

#pragma region 环任务奖励相关
	/**
	*Define Method
	*BlueprintNativeEvent,环任务副本通关结算
	*@param Msg  描述
	*@param Statistics 统计数
	*@param rewardStr 奖励数据（0代表金钱，1代表经验 格式：0:金钱数|1：经验值）
	*@param gradeScore 评分
	*@param countDown 副本结束倒计时
	@param buff buffID|buffID|...
	@param itemStr itemID:amount|itemID:amount|...
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void ShowLoopQuestSpaceWin(const FString& Msg, const FString& Statistics, const FString& RewardStr, const int32& GradeScore, const int32& CountDown, const FString& itemStr, const FString& buff);

	/**
	*Define Method
	* 显示环任务面板
	*/
	void ShowLoopQuestWin();

	/**
	*Define Method
	*BlueprintImplementableEvent,显示不同阶段的奖励
	*@param Money 金钱
	*@param Exp 经验
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void ShowDynamicRewards(const int32& Money, const int32& Exp);

	/**
	*BlueprintCallable，获取物品ItemBase，用于Tips显示
	*
	*@param  FString dataString 物品动态属性数据
	*
	*@return ItemBase
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		UItemBase* getItemByDataString(const FString& dataString, const int32 & itemId);

#pragma endregion

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_rquestToAcceptQuest(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestToCommitQuest(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestToAbandonQuest(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_questChooseReward(const FString& STRING_1, const FString& STRING_2, const FString& STRING_3);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestTongDailyQuest(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_acceptTongDailyQuest(const int32& INDEX_1, const int32& INDEX_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_playerAnswerTongQuestion(const int32& QUESTID_1, const int32& INT32_1, const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_selectNextTongQuestion(const int32& QUESTID_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_stopTongQuestion(const FString& STRING_1);

	void onEnterWorld() override;            ///< 当Entity进入世界时，此方法被调用
	void onLeaveWorld() override;            ///< 当Entity离开世界（被销毁时）时，此方法被调用
	
	virtual void InitBlueCB() override;

	void RPC_broadcastQuestEvent(FString QuestID, FString TaskID);

private:
	/**
	*获取任务对话信息
	*
	*@param JsonStr 新的任务目标信息
	*@param QuestInfo 任务信息
	*@param NpcQuestID NPC任务ID
	*
	*@return 无
	*/
	void GetTalkInfoByJson(const FString& JsonStr, FCS3QuestInfo& QuestInfo);

	/**
	*获取任务信息
	*
	*@param JsonStr 新的任务信息
	*@param QuestInfo 任务信息
	*
	*@return 无
	*/
	void GetQuestInfoByJson(const FString& JsonStr, FCS3QuestInfo& QuestInfo);


	///任务状态改变
	void OnQuestStatusChange(const int32& questID, const QUEST_STATE& newState);///<改变任务状态

protected:
	UPROPERTY(BlueprintReadOnly, Category = "RoleQuestInterface")
		int32 RumorQuestID = 0; ///<传话任务ID
	UPROPERTY(BlueprintReadOnly, Category = "RoleQuestInterface")
		int32 RumorTaskID = 0; ///<传话任务目标ID
	UPROPERTY(BlueprintReadOnly, Category = "RoleQuestInterface")
		FString RumorDialogue = TEXT("");///<传话内容
	UPROPERTY(BlueprintReadOnly, Category = "RoleQuestInterface")
		FString PlayerSoundID = TEXT("");///<玩家对话语音ID

};
