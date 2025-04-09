// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Barracks/RoleArmyData.h"
#include "GameData/TrainSoldierGroundAreaCfg.h"
#include "RoleTrainSoldierGroundInterface.generated.h"


/*
* 文件名称：RoleTrainSoldierGroundInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-04-18
*/

/**
 * 玩家练兵场数据
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleTrainSoldierGroundInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleTrainSoldierGroundInterface();
	~URoleTrainSoldierGroundInterface();
	static FString GetName() { return TEXT("RoleTrainSoldierGroundInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTrainSoldierGroundInterface.BP_RoleTrainSoldierGroundInterface_C'"); } //获取蓝图对象路径

	/// 打开练兵场详情界面
	void OpenTrainSoldierGroundDetails(const FString& name, int32 lineNumber, uint8 npcState, const FVariant& warNameList, const FVariant& warProfessionList, int32 isTrainSoldier, uint8 trainGroundType ,int32 npcID, const FString& notifyFightTime, uint8 isCanClickCancelDec);

	//跟练兵场 宣战
	UFUNCTION(BlueprintCallable)
	void DeclareTrainSoldierGround(const int32& npcID);

	//跟练兵场 撤销宣战
	UFUNCTION(BlueprintCallable)
	void CancelDeclareTrainSoldierGround(const int32& npcID);

	// 请求练兵场任务数据
	UFUNCTION(BlueprintCallable)
		void RequestTrainGroundQuest();
	/**
	*
	*@param NPCID 对话的npcID
	*@param TGQuestList 练兵场任务
	*@param SuccessQuestIndex 完成的任务（成功）(索引值，对应TGQuestList的任务ID)
	*@param FailQuestIndex 完成的任务（失败）(索引值，对应TGQuestList的任务ID)
	*@param DoingQuestIndex 正在做的任务(索引值，对应TGQuestList的任务ID)
	*@param QuestVar 任务数据
	*
	*@return 无
	*/
	void CLIENT_initTrainGroundQuest(const int32& NPCID, const TArray<FVariant>& TGQuestList, const TArray<FVariant>& SuccessQuestIndex, const TArray<FVariant>& FailQuestIndex, const TArray<FVariant>& DoingQuestIndex, const TArray<FVariant>& QuestVar);
	UFUNCTION(BlueprintCallable)
		bool GetTrainGroundQuestByID(int32 QuestID, FTRAIN_GROUND_QUEST& OutTrainFroundQuest);
	//获得练兵任务状态State 0:未接取,1:正在进行，2:已完成,3:已失败，
	UFUNCTION(BlueprintCallable)
		int32 GetTrainGroundQuestState(int32 Index);
	// 手动刷新任务
	UFUNCTION(BlueprintCallable)
		void RequestRefreshTGQuest();
	// 自动刷新
	UFUNCTION(BlueprintCallable)
		void BeginCalculationAuToRefreshQuest();
	UFUNCTION(BlueprintCallable)
		void EndsCalculationAuToRefreshQuest();
	void AutoRefreshTGQuest();
	// 任务刷新回调
	void CLIENT_OnRefreshTGQuest(const TArray<FVariant>& TGQuestList,const TArray<FVariant>& QuestVar);
	
	// 接受练兵任务
	UFUNCTION(BlueprintCallable)
		void RequestAcceptTGQuest(const int32& Index, const int32& battackID);
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnAcceptTGQuest(const int32& Index, const int32& battackID);

	/** 练兵任务结果 
	*
	*@param Index 任务列表的索引
	*@param Result 任务结果
	*@param Exp 兵营获得总的经验
	*@param addExp 包含buff添加的经验
	*@param BattackID 派出部队的id
	*@param LossNum 损失的兵力
	*@param LossNum 是否已经刷新（可能存在，还有任务正在做！就 刷新了）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_onTGQuestResult(const int32& Index, const int32& Result, const int32& Exp, const int32& addExp, const int32& BattackID, const int32& LossNum, const int32& BRefreshAlready);
	// 部队练兵回到大本营
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_onSoldierFinishQuestBack(const int32& BattackID);

	/**打开练兵场区域查看界面
	*@param roleOccupylineNumber 玩家占领分线编号
	*@param roleOccupyIndex 玩家占领练兵场编号
	*@param AllGroundIndexs 该分线所有练兵场编号
	*@param AllGroundOccDBIDs 该分线所有练兵场占领的玩家DBID
	*@param maxLineNumber 最大分线数
	*/
	void OpenAllGroundDetail(int32 roleOccupylineNumber, int32 roleOccupyIndex, const TArray<FVariant>& AllGroundIndexs, const TArray<FVariant>& AllGroundOccDBIDs, int32 maxLineNumber, int32 NpcID);

	void LoadTrainGroundAreaCfgData();

	// 获得练兵场区域配置
	UFUNCTION(BlueprintCallable)
	FTRAIN_SOLDIER_GROUND_MAP_DATA GetTrainGroundCfgByIndex(int32 index);
	
	// 获得练兵场NPC的配置
	UFUNCTION(BlueprintCallable)
		FTrainSoldierGroundNpcData GetTrainGroundNPCCfgData(int32 index, int32 group);
	// 获得练兵场NPC的配置
	UFUNCTION(BlueprintCallable)
		FTrainSoldierGroundNpcData GetTrainGroundNPCCfgDataByGroup(int32 group);

	// 判断练兵场NPC是否中立
	UFUNCTION(BlueprintCallable)
		bool IsTrainGroundNPCNeutrally(int32 group);

	// 判断练兵场NPC是否被我占领
	UFUNCTION(BlueprintCallable)
		bool IsTrainGroundNPCOccupy(int32 group);

	virtual void InitBlueCB() override;
	virtual void onLeaveWorld() override;
	// 前往某个练兵场
	UFUNCTION(BlueprintCallable)
	void RequestGotoTrainGroundByGroup(int32 lineNumber, int32 group, const FVector& position);

	//请求某条分线的练兵场所有数据
	UFUNCTION(BlueprintCallable)
		void RequestAllGroundDetail(int32 lineNumber,int32 npcID);

	// 低级练兵场 初始化攻方大地图数据(BattackVar：兵营、据点数据)
	void InitGTAttackDatas(const FVariant& BattackVar);
	// 兵营（据点）被占领
	void occupyGTBarrack(const int8& BelongSide, const FString& ScriptID);

	// 低级练兵场 初始化守方方大地图数据
	// @Param BattackVar：兵营、据点数据
	// @Param BatteryVar：火炮数据
	// @Param BattackVar：可传送坐标（ue4坐标）
	// @Param TeleportCD：传送CD时间
	void InitGTProtectDatas(const FVariant& BattackVar, const FVariant& BatteryVar, const TArray<FVariant>& TeleportPos, const int32& TeleportCD_);
	// 火炮被销毁
	void onDestroyGTBattery(const int32& EntityID_);
	

	// 守方玩家，请求攻方位置（策划需求，打开大地图。每5秒请求一次）
	UFUNCTION(BlueprintCallable)
		void RequestAttckPos();
	// 服务器回调攻方位置 （显示 交战图标）
	void onRequestAttackPos(const FVector& Pos);
	// 服务器回调攻方位置 （不显示 交战图标）
	void onRequestAttackPosNone();

	// 守方玩家，请求传送位置 UE4坐标（点击传送后，传送图标置灰）
	UFUNCTION(BlueprintCallable)
		void RequestTeleportPos(const FVector& TeleportPos);
	// 传送CD时间已过，传送图标可点击
	void TeleportCDIsReady();

private:
	void initQuestDatas(const TArray<FVariant>& QuestVar);

	FTimerHandle AutoRefreshHandle;
	TMap<int32, TMap<int32, FTrainSoldierGroundNpcData>> TrainGroundNPCCfgData;
public:
	// 练兵任务 配置
	UPROPERTY(BluePrintReadOnly)
		TMap<int32, FTRAIN_GROUND_QUEST> TrainGroundQuestConfig;
	// 练兵任务 ID
	UPROPERTY(BluePrintReadOnly)
		TArray<int32> TGQuestIDArr;
	// 练兵任务 成功完成的索引
	UPROPERTY(BluePrintReadOnly)
		TArray<int32> SuccessQuestIndexArr;
	// 练兵任务 失败完成的索引
	UPROPERTY(BluePrintReadOnly)
		TArray<int32> FailQuestIndexArr;
	// 练兵任务 正在进行任务的索引
	UPROPERTY(BluePrintReadOnly)
		TArray<int32> DoingQuestIndexArr;

	UPROPERTY(BluePrintReadOnly)
		FString FightTime;
	UPROPERTY(BluePrintReadOnly)
		bool bCanClickCancelDec;
	UPROPERTY(BluePrintReadOnly)
		int32 RoleOccupylineNumber;
	UPROPERTY(BluePrintReadOnly)
		int32 RoleOccupyIndex;
	UPROPERTY(BluePrintReadOnly)
		TMap<int32, FString> AllGroundDict;
	UPROPERTY(BluePrintReadOnly)
		TMap<int32, FTRAIN_SOLDIER_GROUND_MAP_DATA> TrainGroundAreaCfg;

	// 兵营（据点）信息
	UPROPERTY(BluePrintReadOnly)
		TMap<FString, FTG_BARRACK> BarrackDatas;
	// 火炮信息
	UPROPERTY(BluePrintReadOnly)
		TMap<int32, FTG_BATTERY> BatteryDatas;
	//是否为进攻方
	UPROPERTY(BluePrintReadOnly)
		bool bIsBattack;



private:
	int32 TeleportCD;			// 传送CD
};