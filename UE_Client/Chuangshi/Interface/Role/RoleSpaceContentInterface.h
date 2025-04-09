// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/SpaceHunTingData.h"
#include "GameData/SpaceYeZhanFengQiData.h"
#include "GameData/MagicMazeQuestion.h"
#include "GameData/SpaceYXLMData.h"
#include "GameData/YXLMMatchData.h"
#include "GameData/LingMaiData.h"
#include "GameData/AttCityMemberData.h"
#include "QuickBarInterface.h"
#include "GameData/Barracks/RoleArmyData.h"
#include "GameData/GameDeFine.h"
#include "GameData/ZYJJRewardData.h"
#include "IDelegateInstance.h"
#include "RoleSpaceContentInterface.generated.h"

/*
* 文件名称：RoleSpaceContentInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：all
* 创建时间：2017-07-29
*/

/**
* 玩家副本内容接口类
*/
class AEquipBuildClientCharacter;
UCLASS(BlueprintType)
class CHUANGSHI_API URoleSpaceContentInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("RoleSpaceContentInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleSpaceContentInterface.BP_RoleSpaceContentInterface_C'"); } //获取蓝图对象路径

#pragma region 真龙棋局
	/**
	*Define method
	*BlueprintNativeEvent，真龙棋局副本Boss状态改变回调
	*
	*@param state    Boss状态 1:黑 2:白
	*@param entityID BossID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ZhenLongQiJu_OnBossStateChange(const int32& state, const int32& bossEntityID, const FString& effectID);

	/**
	*Define method
	*BlueprintNativeEvent，真龙棋局副本Boss血量改变
	*
	*@param hp_Max     Boss的最大血量
	*@param currentHP  Boss的当前血量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ZhenLongQiJu_OnBossHPChange(const int32& hp_Max, const int32& currentHP);

	/**
	*
	*BlueprintImplementableEvent，真龙棋局副本Boss状态改变
	*
	*@param state    Boss状态 1:黑 2:白
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void ZhenLongQiJu_OnBossStateChangeBP(const int32& state);

	/**
	*Define method
	*BlueprintNativeEvent，真龙棋局副本停止状态切换,关闭界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ZhenLongQiJu_StopBossStateChange();

	/**
	*Define method
	*BlueprintNativeEvent，真龙棋局副本清除粒子数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ZhenLongQiju_ClearData();
#pragma endregion

#pragma region 荷花法阵
	/**
	*Define Method
	*BlueprintNativeEvent,上荷花
	*@param heHuaType 荷花类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnMountHeHua(int32 heHuaType);

	/**
	*Define Method
	*BlueprintNativeEvent,移动到目标位置
	*@param dstPos :目标位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void MoveToTargetPosition(const FVector& dstPos);

	/**
	*Define Method
	*BlueprintNativeEvent,移动到目标位置
	*@param dstPos :目标位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void DismountHeHua();

	/**
	*通知服务器下荷花
	*BlueprintCallable,移动到目标位置
	*@param dstPos :目标位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void OnDismountHeHua();
	/**
	*Define Method
	*BlueprintNativeEvent,显示圆形血量条
	*@param isOpen :0：关闭，1：打开
	*@param percent：百分比
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowCircleHPPercentBar(UINT8 isOpen, int32 percent);

	/**
	*是否移动荷花
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		bool IsMovingCallCellOnHeHua();

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|HeHua")
		bool OnPlayerMoveTypeChange(CS3_MOVE_TYPE NewMoveType, CS3_MOVE_TYPE OldMoveType);
#pragma endregion

#pragma region 幻阵迷宫问答副本
	/**
	*Define Method
	*BlueprintNativeEvent,幻阵迷宫问答结束
	*
	*@param:questionResults  答题排行数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_MagicMazeAnswerQuestionEnd(const FString& questionResults);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnMagicMazeAnswerQuestionEnd(const TArray<FMAGICMAZEQUESTION_RESULT_DATA>& questionResults);
	/**
	*Define Method
	*BlueprintNativeEvent,客户端接收问题
	*
	*@param:currentQuestionID  问题ID
	*@param:currentDescription  问题描述
	*@param:currentOption  问题选项
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ReceiveQuestion(const int32& currentQuestionID, const FString& currentDescription, const FString& currentOption);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnReceiveQuestion(const int32& currentQuestionID, const FString& currentDescription, const TArray<FString>& currentOptionLists);

	/**
	*Define Method
	*BlueprintNativeEvent,客户端接收问题结果是否答对
	*
	*@param:currentQuestionID  问题ID
	*@param:Result  问题是否答对
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ReceiveQuestionState(const int32& questionID, const uint8& Result);

	/**
	*Define Method
	*BlueprintNativeEvent,客户端开始答题
	*
	*@param:LastTime  答题持续时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_StartMagicMazeQuest(const int32& LastTime, const int32& TotalAnswerCount);

	/**
	*Cell Method
	*BlueprintCallable,幻阵迷宫回答问题
	*
	*@param:currentQuestionID  问题ID
	*@param:answer  回答选项的描述
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void playerAnswer(const int32& questionID, const FString& answer);

	/**
	*Cell Method
	*BlueprintCallable,幻阵迷宫选择下一个问题
	*
	*@param 无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void selectNextQuestion();

#pragma endregion
#pragma region 幻阵迷宫天命副本
	/**
	*Define Method
	*BlueprintNativeEvent,客户端接收天命结果
	*
	*@param:Result	天命结果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_MagicMazeDestinyResult(const int32& Result);

	/**
	*Define Method
	*BlueprintNativeEvent,玩家进入天命转盘地图
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_CreateDestinyZhuanPan();


#pragma endregion
#pragma region 幻阵迷宫气运副本
	/**
	*Define Method
	*BlueprintNativeEvent,客户端接收气运结果
	*
	*@param:Result	气运结果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_MagicMazeLuckResult(const int32& Result);

	/**
	*Define Method
	*BlueprintNativeEvent,玩家进入气运转盘地图
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_CreateLuckZhuanPan();

	/**
	*Define Method
	*BlueprintNativeEvent,显示气运结果的额外奖励
	*
	*@param:extraReward	额外奖励
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowLuckExtraReward(const int32& extraReward);


#pragma endregion
#pragma region 玩家副本专用背包相关
	/**
	*Define Method
	*BlueprintNativeEvent,增加副本额外物品栏
	*
	*@param:gridNum  格子数
	*@param:uidList  玩家副本物品uid列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CreateExtraItemBar(const int32& gridNum, const TArray<FString>& uidList);

	/**
	*Define Method
	*BlueprintNativeEvent,移除副本额外物品栏
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void RemoveExtralItemBar();
#pragma endregion

#pragma region 玩家临时装备背包相关 CST-12212 吃鸡装备栏
	/**
	*Define Method
	*增加临时装备物品栏
	*
	*@param:{orderID:itemID}
	*
	*@return 无
	*/
	void CreateTempEquipBar(const FVariant& variant);

	/**
	*Define Method
	*移除临时装备物品栏
	*
	*@return 无
	*/
	void RemoveTempEquipBar();
#pragma endregion

#pragma region 帮会日常:收集法宝碎片
	/**
	*Define Method
	*BlueprintNativeEvent,更新能量条
	*
	*@param:curValue  当前能量值
	*@param:maxValue  最大能量值
	*@param:canAddSpeed 是否能加速
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void UpdateEnergyBar(const int32& curValue, const int32& maxValue, const uint8& canAddSpeed);

	/**
	*Define Method
	*BlueprintNativeEvent,显示能量条提示消息
	*
	*@param:Result False时提示:能量不足，True时提示:获得能量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowEnergyMessage(const uint8& result);

	/**
	*Define Method
	*BlueprintNativeEvent,显示收集法宝成功提示消息
	*
	*@param:无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowFaBaoCollectSuccMsg(const FString& scriptID);

	/**
	*Define Method
	*BlueprintNativeEvent,加速回调
	*
	*@param:无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnOpenAddSpeedExpendEnergy();

	/**
	*Define Method
	*BlueprintNativeEvent,关闭加速回调
	*
	*@param:无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnCloseAddSpeedExpendEnergy();

#pragma endregion

#pragma region 帮会掠夺战器械建造功能
	/**
	*Define Method
	*进入器械建造模
	*
	*@param ModelID 模型ID
	*@param SkillID 技能ID
	*
	*@return 无
	*/
	void OnEnterEquipBuild(const FString& ScriptID, const FString& ModelID, const float& ModelScale, const FString& ItemUID);
	void OnLeaveEquipBuild();
	void RequestCreateApparatus(const FString& ScriptID, const FString& ItemUID);
#pragma endregion

#pragma region 夜袭凤栖镇
	/**
	*Define Method
	*BlueprintNativeEvent,显示进入凤栖镇的提示
	*
	*@param:无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowEnterFengQiMsg();
#pragma endregion
#pragma region 灵箭化元
	/**
	*Define Method
	*BlueprintNativeEvent,增加化元盾
	*
	*@param shieldCurValue 化元盾当前值
	*@param shieldMaxValue 化元盾最大值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnAddShield(const int32& shieldCurValue, const int32& shieldMaxValue);

	/**
	*Define Method
	*BlueprintNativeEvent,删除化元盾
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnRemoveShield();

	/**
	*Define Method
	*BlueprintNativeEvent,化元盾耐久度改变
	*
	*@param shieldCurValue 化元盾当前值
	*@param shieldMaxValue 化元盾最大值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnShieldChanged(const int32& shieldCurValue, const int32& shieldMaxValue);
#pragma endregion
#pragma region 环任务:钓鱼
	/**
	*Define method
	*BlueprintNativeEvent，进入钓鱼
	*
	*@param smllFishFood 小型鱼饵
	*@param mediumFishFood 中型鱼饵
	*@param bigFishFood 大型鱼饵
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void EnterFishState(int32 smllFishFood, int32 mediumFishFood, int32 bigFishFood);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnEnterFishState(int32 smllFishFood, int32 mediumFishFood, int32 bigFishFood);

	/**
	*Define method
	*BlueprintNativeEvent，钓鱼得分改变回调
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowFishScore(int32 fishingScore);
#pragma endregion
#pragma region boss战
	/**
	*Define method
	*BlueprintNativeEvent，显示boss进度条
	*
	*@param IsSucceed QTE是否成功
	*@param IsQTE 是否有QTE
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void NotifyClinetQTEResult(uint8 IsSucceed);
	/**
	*Define method
	*BlueprintNativeEvent，其他玩家显示QTE提示
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void OtherShowQTE();
#pragma endregion
#pragma region 幻莲天池
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void CreateFish(const int32 ID, const float PositionX, const float PositionY, const float PositionZ, const float Scale);
#pragma endregion
#pragma region 拷问副本
	/**
	*Define Method
	*BlueprintNativeEvent,改变视角
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_notifyCameraMove();

	/**
	*Define Method
	*BlueprintNativeEvent,开始拷问
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_onStartTorureNotice();

	/**
	*Define Method
	*BlueprintNativeEvent,继续拷问
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_onContinueTorture();

	/**
	*Define Method
	*BlueprintNativeEvent,恢复玩家状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyClientRecoveryStatus();

	/**
	*Define Method
	*BlueprintNativeEvent,通知界面显示拷问结果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyClientTortureResult();
#pragma endregion

#pragma region 三源镜柱	
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyClientStopEffect(const FString& effectID);
#pragma endregion

#pragma region 灵魂之誓
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnAbsorbSoulLayerLevelChanged(int32 type);
#pragma endregion

#pragma region 镇煞宫
	/**
	*Define Method
	*BlueprintNativeEvent,交互完成，打开门
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void SpaceZSGGossipComplete();

	/**
	*Define Method
	*BlueprintNativeEvent,交互完成，打开门
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CopyRemainTimeAndName(int32 time, const FString& name);

#pragma endregion

#pragma region 四象变幻
	/**
	*Define Method
	*BlueprintNativeEvent,显示雕像血量
	*@param index :雕像索引
	*@param percent：百分比
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnPremierHPChanged(int32 index, int32 percent);
#pragma endregion

#pragma region 迷幻丛书
	/**
	*Define Method
	*BlueprintNativeEvent,显示题目描述
	*@param voiceID :语音ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_onProblemDescription(const FString& voiceID, int32 count);

	/**
	*Define Method
	*BlueprintNativeEvent,答案反馈
	*@param result:是否正确
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_onCalculateResults(int32 result);
#pragma endregion

#pragma region 重炼宝图
	/**
*Define Method
*BlueprintNativeEvent,暂停副本声音
*
*
*@return 无
*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_SetPausedSpaceVoice(const TArray<FString>& CurPauseTypes, const TArray<FString>& CurHideTypes, bool bPause, bool bIsHideVoiceType);

#pragma endregion

#pragma region 神风秘径
	/**
	*Define Method
	*BlueprintNativeEvent骑上啸风鹰
	*@param FlyRoute:飞行路线
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_RideCopyGlede(const FString& _FlyRoute);

	/**
	*BlueprintImplementableEvent骑上啸风鹰蓝图回调
	*@param FlyRoute:飞行路线
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnRideCopyGledeBP();
	/**
	*Define Method
	*BlueprintNativeEvent,落下啸风鹰
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_DismountCopyGlede();

	/**
	*BlueprintCallable 下坐骑
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void DisRideOnCarrier();

#pragma endregion

#pragma region 梦魇画卷
	/**
	*Define Method
	*BlueprintNativeEvent,通知副本显示界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyHealthDisplayScreen();

	/**
	*Define Method
	*BlueprintNativeEvent,通知副本开始倒计时
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyStartCountdown();

	/**
	*Define Method
	*BlueprintNativeEvent,通知副本开始倒计时
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyStopCountdown();

#pragma endregion

#pragma region 鬼域迷阵
	/**
	*Define Method
	*BlueprintNativeEvent,通知副本显示界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ClIENT_DisplayLocationAndColor(const FVector& dstPos, const int32& index);

	/**
	*Define Method
	*BlueprintNativeEvent,通知清除副本显示界面数据
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ClIENT_ClearLocationAndColor();

#pragma endregion

#pragma region 幻阵迷宫子副本状态更新
	/**
	*Define Method
	*BlueprintNativeEvent,更新幻阵迷宫子副本通关状态到界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_MatrixMazeResult(const TArray<int32>& hzmgIndexList, const TArray<int32>& hzmgResultList);

	/**
	*Define Method
	*BlueprintNativeEvent,通知显示进度界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ProgressDisplayInterface();
#pragma endregion
#pragma region 金枝玉庭
	/**
	*Define Method
	*BlueprintNativeEvent	玩家当前获得的金币总数
	*@Param amount				数量
	*@return 无
	*/
	void CLIENT_ShowCurrGotGoldAmount(const int32& amount);

	/**
	*Define Method
	*BlueprintNativeEvent,	玩家获得物品
	*@Param itemID				获得物品ID， "0"表示金钱,"1"表示潜能
	*@Param amount				数量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowFuDaiReward(const FString& itemID, const int32& amount);

	/**
	*Define Method
	*BlueprintNativeEvent,	通知显示界面随机事件
	*@Param key					随机事件的key， ""没有随机事件
	*@Param amount				结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJinZhiYuTingRandomEvent(const FString& key, const FString& endTime);

	/**
	*Define Method
	*BlueprintNativeEvent,		副本结算获得通过等级以及总物品
	@Param FuDaiNum				副本中接取的福袋总数量
	*@Param itemIDs				获得物品 物品id:数量|物品id:数量... 其中id为"0"表示金钱,id为"1"表示潜能
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJinZhiYuTingRewards(const int32& FuDaiNum, const FString& itemIDs);
	/**
	*Define Method
	*BlueprintNativeEvent,		副本阶段提示
	*@Param stageIndex			副本阶段索引
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnShowJZYTStageTips(const int32& stageIndex);
	/**
	*Define Method
	*BlueprintNativeEvent,
	*@Param Time			怪物出场显示界面提示
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJinZhiYuTingMonster();

	/**
	*Define Method
	*BlueprintNativeEvent,停止显示怪物的界面提示
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void StopShowJinZhiYuTingMonster();

	/**
	*Define Method
	*BlueprintNativeEvent, 盗宝小贼掉落的财宝种类
	*@Param key		0:代表金币，1：代表潜能
	*@Param value	数量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyDisplayItemIcon(const int32& key, const int32& value);

	/**
	*Define Method
	*BlueprintNativeEvent, 停止显示怪物的财宝种类
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void StopDisplayItemIcon();
#pragma endregion 

#pragma region 炼狱之塔
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMovingPlatformTriggerBegin(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMovingPlatformTriggerStart(const FString& STRING_1);
#pragma endregion

#pragma region 晶石洞窟

	/**
	*Define Method
	*BlueprintNativeEvent,通知玩家进入瞄准投掷模式
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnEnterAimingThrowMode(const int32& Type);
	// 离开晶石洞窟副本
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnLeaveJSDFSpace();
	
	/**
	*Define Method
	*BlueprintNativeEvent,通知玩家离开瞄准投掷模式
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnLeaveAimingThrowMode();

	/**
	*Define Method
	*BlueprintNativeEvent,通知开始刷新灵晶
	*@param coordXList :X坐标列表
	*@param coordYList :Y坐标列表
	*@param coordZList :Z坐标列表
	*@param colorNumList :颜色列表
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_refreshSpiritCrystal(const TArray<int32>& coordXList, const TArray<int32>& coordYList, const TArray<int32>& coordZList, const TArray<int32>& colorNumList);

	/**
	*Define Method
	*BlueprintNativeEvent,通知开始反弹
	*@param colorNum：颜色编号
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyStartRebound(const int32& colorNum);

	/**
	*Define Method
	*BlueprintNativeEvent,怪物击中灵晶，开始掉落
	*@param tiggerID :怪物ID
	*@param num :击中的灵晶编号
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_dropSpiritCrystal(const int32& tiggerID, const int32& num);

	/**
	*Define Method
	*BlueprintNativeEvent,玩家拾取灵晶时头顶显示灵晶数量
	*@param count :拾取灵晶数
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyAccordToCount(const int32& count);

	/**
	*Define Method
	*BlueprintNativeEvent,怪物拾取灵晶，怪物头顶显示灵晶数量
	*@param monsterID :怪物ID
	*@param count：灵晶数量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyMonsterToCount(const int32& monsterID, const int32& count);

	/**
	*Define Method
	*BlueprintNativeEvent,初始化目标数量
	*@param colorNum:灵晶对应的颜色编号
	*@param count：数量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_InitializeCrystalCount(const int32& redCount, const int32& yellowCount, const int32& blueCount);

	/**
	*Define Method
	*BlueprintNativeEvent，计数玩家收集到的灵晶
	*@param colorNum:灵晶对应的颜色编号
	*@param count：数量
	*@param isAdd:增加或减少计数，true：增加，false：减少
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyPlayerAddCount(const int32& colorNum, const int32& count, bool isAdd);

	/**
	*Define Method
	*BlueprintNativeEvent，计数怪物收集到的灵晶
	*@param colorNum:灵晶对应的颜色编号
	*@param count：数量
	*@param isAdd:增加或减少计数，true：增加，false：减少
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyMonsterAddCount(const int32& colorNum, const int32& count, bool isAdd);

	/**
	*Define Method
	*BlueprintNativeEvent，晶石从玩家身上弹出
	*@param colorNum:灵晶对应的颜色编号
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyPlayerPopCrystal(const int32& colorNum);

	/**
	*Define Method
	*BlueprintNativeEvent，晶石从怪物身上弹出
	*@param colorNum:灵晶对应的颜色编号
	*@param angle：角度
	*@param distance:距离
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyMonsterPopCrystal(const int32& monsterID, const int32& colorNum, const float& angle, const float& distance);

	/**
	*Define Method
	*BlueprintNativeEvent，通知在玩家一定范围内播放预警以及闪电
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyCrystalPlayLight(const float& distance);

	/**
	*Define Method
	*BlueprintNativeEvent，通知空中所有的黄色灵晶停止播放预警以及闪电
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyCrystalStopPlayLight();

	/**
	*BlueprintCallable，玩家碰到在地上的灵晶
	*@Param colorNum 灵晶颜色
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onPlayerTouchCrystal(const int32& colorNum);

	/**
	*BlueprintCallable，怪物碰到在地上的灵晶
	*@Param colorNum 灵晶颜色
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMonsterTouchCrystal(const int32& colorNum);

	/**
	*BlueprintCallable，怪物打下灵晶掉落的地上位置
	*@Param Position_1	水晶的位置
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onSpiritCrystalPos(const FVector& Position_1);

	/**
	*BlueprintCallable，灵晶击中怪物
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCrystalHitMonster();

	/**
	*BlueprintCallable，灵晶击中玩家
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onSpiritCrystalHitPlayer();

	/**
	*BlueprintCallable，灵晶掉落时，移除服务器已掉落的灵晶
	*@Param Index 灵晶的ID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onRemoveSpiritCrystalNum(const int32& Index);

	/**
	*BlueprintCallable，玩家碰到怪物打下来的灵晶通知服务器
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onRemoveSpiritCrystalPos(const FVector& Position_1);

	/**
	*BlueprintCallable，玩家使用错误的颜色打掉灵晶，通知服务器刷怪
	*@Param colorNum 灵晶颜色
	*@Param Position_1	地上水晶的位置
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onLocationBrushStrange(const int32& colorNum, const FVector& Position_1);

#pragma region

#pragma region 消灭影妖
	/**
	*Define Method
	*BlueprintNativeEvent,服务器通知打开照妖镜
	*@Param high 照妖镜照射高度
	*@Param radius 半径
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OpenMonsterMirror(const float& high, const float& radius);

	/**
	*Define Method
	*BlueprintNativeEvent,服务器通知关闭照妖镜
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_CloseMonsterMirror();

	/**
	*Define Method
	*BlueprintNativeEvent,显示能量条
	*@Param maxLingEnergyValue 最大灵能值
	*@Param curLingEnergyValue 当前灵能值
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowLingEnergyBar(const int32& maxLingEnergyValue, const int32& curLingEnergyValue);

	/**
	*Define Method
	*BlueprintNativeEvent,更新能量条
	*@Param maxLingEnergyValue 最大灵能值
	*@Param curLingEnergyValue 当前灵能值
	*@Param reduceLingEnergyValue 减少的灵能值
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateLingEnergyBar(const int32& maxLingEnergyValue, const int32& curLingEnergyValue, const int32& reduceLingEnergyValue);

	/**
	*Define Method
	*BlueprintNativeEvent,服务器通知隐藏能量条
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_HideLingEnergyBar();

	/**
	*BlueprintCallable，打开照妖镜
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_openMonsterMirror();

	/**
	*BlueprintCallable，关闭照妖镜
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_closeMonsterMirror();

	/**
	*BlueprintCallable，通知服务器某些怪物在照妖镜内
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_MonsterListInMonsterMirror(const TArray<int32>& entityIDs);

	/**
	*BlueprintCallable，通知服务器怪物离开照妖镜
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_MonsterOutMonsterMirror(const int32& monsterID);

#pragma region

#pragma region 仙岛归墟

	/**
	*BlueprintCallable，给服务器发送第一块地板的位置和长宽
	*@Param Position	第一个地板的位置
	*@Param Length		地板的长度
	*@Param Width		地板的宽度
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_FirstFloorPosition(const FVector& Position, const float& Length, const float& Width);

	/**
	*BlueprintCallable，给服务器发送需要修补的地板的ID
	*@Param FloorID		地板的ID (Y*Row + X)
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_FillFloor(const int32& FloorID);

	/**
	*Define Method
	*BlueprintNativeEvent,	服务器通知掉落地板
	*@Param FloorID			地板的ID (Y*Row + X)
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void Client_RemoveFloor(const int32& FloorID);


	/**
	*Define Method
	*BlueprintNativeEvent,	服务器通知增加地板
	*@Param FloorID			地板的ID (Y*Row + X)
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void Client_AddFloor(const int32& FloorID);

	/**
	*Define Method
	*BlueprintNativeEvent,	服务器通知创建地板
	*@Param Row				地板的行
	*@Param Col				地板的列
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void Client_CreateFloor(const int32& Row, const int32& Col);

	/**
	*Define Method
	*BlueprintNativeEvent,	服务器通知检测鼠标指向的地板
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void Client_GetTheFloorUnderMouseCursur();

	/**
	*BlueprintCallable，玩家所站立的格子掉落
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_floorStartFalling();

	/**
	*Define Method
	*BlueprintNativeEvent,	显示停止地板掉落的提示
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowStopDestroyFloorTime(float stopTime);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void StartCheckFillFloor();

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void StopCheckFillFloor();

#pragma region

#pragma region 玄天宝录
	/**
	*BlueprintCallable，	通知反射镜对象
	*@Param entityID		反射镜的entityID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyMirrorObject(const int32& XTBLID, const TArray<int32>& reflectorList);

	/**
	*Define Method
	*BlueprintNativeEvent	通知转动反射镜的角度范围
	*@Param dstPos			大日宝镜的位置
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnRotationAngleRange(const FVector& dstPos, const float& rotatSpeed);

	/**
	*BlueprintCallable，	通知显示结界血条界面
	*@Param percent			血量百分比
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowBloodPercentBar(const int32& percent);

	/**
	*BlueprintCallable，	通知显示下一次暴动的时间
	*@Param percent			时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyNextRiotTime(const FString& nextRiotTime);

	/**
	*BlueprintCallable，	通知显示下一次爆发时间
	*@Param percent			时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyNextExplosionTime(const FString& nextExplosionTime);

	/**
	*BlueprintCallable，	通知停止显示下一次爆发时间界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyStopNextExplosionTime();

	/**
	*BlueprintCallable，	通知服务器怪物石像在日光中
	*@Param monsterID		怪物的entityID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onStoneInSunShone(const int32& monsterID);

	/**
	*BlueprintCallable，	通知服务器怪物石像不在日光中
	*@Param monsterID		怪物的entityID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onStoneOutSunShone(const int32& monsterID);

	/**
	*BlueprintCallable，	通知停止显示爆发倒计时界面（加在副本行为SEAction269中）
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyXTBLStopShow();

#pragma region 

#pragma region CST-6262 蟠龙秘境
	/**
	*Define Method
	*BlueprintNativeEvent	显示龙鳞载具UI
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowPLMJCarrierUI();

	/**
	*Define Method
	*BlueprintNativeEvent	激活龙鳞载具UI
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ActivePLMJCarrierUI();
	/**
	*Define Method
	*BlueprintNativeEvent	隐藏龙鳞载具UI
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_HidePLMJCarrierUI();
	/**
	*BlueprintCallable，	上下载具
	*@Param isMount	0代表下载具 1代表上载具
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_roleMountCarrier(const int32& isMount);

#pragma region 

#pragma region 藏功殿
	/**
	*Define Method
	*BlueprintNativeEvent,通知显示右方的问题描述
	*@param: voiceID 语音ID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_DisplayProblemDescription(const FString& voiceID);

	/**
	*Define Method
	*BlueprintNativeEvent,通知关闭藏功殿答题界面
	*@param: 无
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CloseProblemDescription();

#pragma endregion

#pragma region CST-6526 冥域缉凶
	/**
	*Define Method
	*BlueprintNativeEvent,机关能量条
	*@param: curEnergy 当前能量
	*@param: maxEnergy 最大能量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateMYJXEnergyBar(const int32& curEnergy, const int32& maxEnergy);

	/**
	*Define Method
	*BlueprintNativeEvent,隐藏机关能量条
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_HideMYJXEnergyBar();

	/**
	*Define Method
	*BlueprintNativeEvent,显示弹跳按钮
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowMYJXJumpBtn();

	/**
	*Define Method
	*BlueprintNativeEvent,隐藏弹跳按钮
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_HideMYJXJumpBtn();

	/**
	*BlueprintCallable 点击弹射按钮
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_MYJXPressJumBtn();

	/**
	*Define Method
	*BlueprintNativeEvent,跳到目标点
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_JumpToDstPos(const FVector& dstPos, float RisingDistance);
#pragma endregion

#pragma region CST-7419 金树种子
	/**
	*Define Method
	*BlueprintNativeEvent,设置金树种子光墙数据
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJSZZPlaneWall(const FString& spaceScriptID, const TArray<FVector>& wallPosList);

	/**
	*Define Method
	*BlueprintNativeEvent,显示金树种子第一阶段数据
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_showJSZZFirstTaskData(const FString& spaceScriptID, const FVector& pos, const float& radius);

	/**
	*Define Method
	*BlueprintNativeEvent,显示金树种子第二阶段数据
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_showJSZZSecondTaskData(const FVector& plantCenterPos, const float& plantRadius);

	/**
	*BlueprintCallable 接受金树种子任务
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_ReplyAcceptJSZZQuest(const FString& itemUID);

	/**
	*Define Method
	*BlueprintNativeEvent,增加第二阶段检测区域
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_AddJSZZCircleArea(const FString& spaceScriptID, const FVector& plantCenterPos, const float& plantRadius);

	/**
	*Define Method
	*BlueprintNativeEvent,清除第二阶段检测区域
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ClearJSZZCircleArea();

	/**
	*
	*BlueprintImplementableEvent,进入第二阶段检测区域
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnEnterJSZZCircleArea();

	/**
	*
	*BlueprintImplementableEvent,离开第二阶段检测区域
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnLeaveJSZZCircleArea();

	/**
	*Define Method
	*BlueprintNativeEvent,通知第二阶段可以点击搜索按钮
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_NotifyClientSecondTaskCanSearch();

	/**
	*Define Method
	*BlueprintNativeEvent,通知第二阶段可以点击搜索按钮
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJSZZAcceptWin(const TArray<int32>& itemIDs, const int32& time, const FString& itemUID);

	/**
	*
	*BlueprintCallable,点击第二阶段搜索按钮
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_ClickJSZZSearch();
	/**
	*Define Method
	*BlueprintNativeEvent,切换第二阶段的搜索按钮
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ChangeJSZZSearchBtn(const float& totalTime, const float& showTime);

	/**
	*
	*BlueprintCallable,点击第二阶段种植按钮
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_ClickJSZZPlant();
	/**
	*Define Method
	*BlueprintNativeEvent,通知显示阶段剩余时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJSZZCurStageRemainTime(const int32& stage, const int32& remainTime);

	/**
	*Define Method
	*BlueprintNativeEvent,通知显示剩余刷怪时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowNextRefreshMonsterTime(const int32& remainTime);

	/**
	*Define Method
	*BlueprintNativeEvent,通知显示金树种子任务的结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_showJSZZQuestTime(const FString& endTime);

	/**
	*Define Method
	*BlueprintNativeEvent,显示金树种子成长度
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowJSZZGrowthDegree(const int32& value);

	/**
	*Define Method
	*BlueprintNativeEvent,显示金树种子结算界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowJSZZSettlement(const int32& rewardMoney);

	/**
	*Define Method
	*BlueprintNativeEvent,第二版 显示搜索界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowJSZZPlantWin(const FVector& plantPosition);

	/**
	*
	*BlueprintCallable,点击搜索按钮
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void ClickJSZZSearchBtn();

	/**
	*
	*BlueprintCallable,点击种植按钮
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void ClickJSZZPlantBtn();

	/**
	*Define Method
	*BlueprintNativeEvent,第二版 显示守护阶段界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowJSZZProtectWin(const TArray<int32>& itemIDs);

	/**
	*Define Method
	*BlueprintNativeEvent,显示圆形血量条
	*@param isOpen :0：关闭，1：打开
	*@param percent：百分比
	*@param describe:描述
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowMonsterCircleHPPercentBar(const int32& isOpen, const int32& percent, const FString& describe);

#pragma region 魔像水晶
	/**
	*Define Method
	*BlueprintImplementableEvent,显示匹配失败、成功
	*
	*@param:Result(1-匹配成功；0-匹配失败)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnMatchMXSJResult(const int32& Result);
#pragma endregion

#pragma region 灵气迷宫
	/**
	*Define Method
	*BlueprintNativeEvent,通知显示箭头划过效果
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnArrowCrossoverEffect();

#pragma endregion

#pragma region 急速穿梭
	/**
	*Define Method
	*BlueprintNativeEvent,通知显示传送门刷新倒计时
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJSCSCountDownUI(const FString& endtime);
	/**
	*Define Method
	*BlueprintNativeEvent, 通知传送门刷新提示
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowJSCSTipsUI();

#pragma endregion

#pragma region 冥气人参果

	/**
	*Define Method
	*BlueprintNativeEvent,通知玩家进入瞄准攻击模式
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnEnterAimingMode();

	/**
	*Define Method
	*BlueprintNativeEvent,通知玩家离开瞄准攻击模式
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnLeaveAimingMode();

	/**
	*Define Method
	*BlueprintNativeEvent,通知开始刷新人参果
	*@param coordXList :X坐标列表
	*@param coordYList :Y坐标列表
	*@param coordZList :Z坐标列表
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void InitRefreshCiku(const TArray<int32>& cikuCoordXList, const TArray<int32>& cikuCoordYList, const TArray<int32>& cikuCoordZList);

	/**
	*Define Method
	*BlueprintNativeEvent,通知开始刷新正常的人参果
	*@param coordXList :X坐标列表
	*@param coordYList :Y坐标列表
	*@param coordZList :Z坐标列表
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void InitRefreshNormalCiku(const TArray<int32>& cikuCoordXList1, const TArray<int32>& cikuCoordYList1, const TArray<int32>& cikuCoordZList1);

	/**
	*Define Method
	*BlueprintNativeEvent,通知开始爆发冥气以及周围的人参果开始抖动
	*@param initialValue :	起始爆发冥气个数
	*@param radius :		抖动半径
	*@param time :			间隔时间（每隔time，爆发个数越来越多）
	*@param epsilon :		递增值
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void StartSendOutGhostGas(const int32& initialValue, const float& radius, const float& time, const int32& epsilon);

	/**
	*BlueprintCallable，通知服务器掉落在地上的人参果
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_NotifyDropDownCiku();

	/**
	*BlueprintCallable，通知服务器击中正确的人参果,以及地板位置
	*@param ciKuPos : 对应爆发冥气的人参果地板坐标
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_HitRightCiku(const FVector& ciKuPos);

	/**
	*BlueprintCallable，通知服务器击中错误的人参果,以及地板位置
	*@param ciKuPos : 对应爆发冥气的人参果地板坐标
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_HitErrorCiku(const FVector& ciKuPos);

#pragma region

#pragma region 副本浩灵谷
	/**
	*Define Method
	*BlueprintNativeEvent,通知QTE是否成功
	*@param isSucceed 0：失败，1：成功
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCompleteQTENotyfy(const int32& isSucceed);

#pragma endregion

#pragma region 环任务副本相关
	/**
	*Define Method
	*BlueprintNativeEvent,副本失败通知
	*@param countDown 副本结束倒计时
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowLoopQuestSpaceFailure(const FString& countDown);

	/**
	*Define Method
	*BlueprintNativeEvent,开始进度条倒计时
	*@param time 正计时则为总时间，倒计时则为结束时间
	*@param changeTime  计时到某个时间改变进度条颜色
	*@param changeColor 进度条颜色编号
	*@param type -1为倒计时， 1为正计时
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnStartReckonByTime(const FString& time, const TArray<int32>& changeTime, const TArray<int32>& changeColor, const int32& type);

	/**
	*Define Method
	*BlueprintNativeEvent,环任务点击退出按钮则弹出二次确认界面
	*@param result 0为失败，1为成功
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowLoopQuestResult(const int32& result);

	/**
	*Define Method
	*BlueprintCallable,点击关闭副本通知
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onNotyfyCloseSpace(const int32& Result);

	/**
	*Define Method
	*BlueprintCallable,点击退出副本通知
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onClickSignOutSpace();

#pragma endregion

#pragma region 玲珑宝珠
	/**
	*Define Method
	*BlueprintNativeEvent, 玲珑宝珠显示难度界面
	*@DiffcultStr 格式  SriptID:难度|SriptID:难度|SriptID:难度...
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_LLBZShowAllDiffcult(const FString& DiffcultStr);

	/**
	*Define Method
	*BlueprintNativeEvent,使用开启金枝玉庭物品
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_beginLLBZ(const FString& RewardList, const FString& uid, const FString& SpaceStr);

	/**
	*开始灵气锁游戏
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_startLingQiLock(const FString& ScriptID, const int32& Diffculty, const int32& Amount, const int32& Speed);
	/**
	*开始灵幻决游戏
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_startLingHuanJue(const FString& ScriptID, const int32& Diffculty, const int32& Amount);

	/**
	*玲珑宝珠 结算界面
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowLLBZRewards(const FString& rewardStr, const int32& HPRate);

	/**
	*副本自己退出弹出失败界面
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowSpaceCopyFailedUI();
	/**
	*使用玲珑宝珠后
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnUseLLBZ(const FString& uid, const FString& SpaceStr);

	/**
	*完成灵气锁游戏
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnLingQiLock(const FString& ScriptID, const int32& Diffculty, const int32& Time);
	/**
	*完成灵幻决游戏
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnLingHuanJue(const FString& ScriptID, const int32& Diffculty, const int32& Time);
	/**
	*玲珑宝珠完成所有游戏
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnLLBZGameComplete();
#pragma endregion

#pragma region 巧取熔岩晶
	/**
	*Define Method
	*BlueprintNativeEvent,通知修改副本的辅助模式
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ModifySwitchHomingSpellAtt();

	/**
	*Define Method
	*BlueprintNativeEvent,进入骑乘石头模式
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnEnterRidingStoneMode();

	/**
	*Define Method
	*BlueprintNativeEvent,离开骑乘石头模式
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnLeaveRidingStoneMode();
#pragma endregion

#pragma region CST-9020 勇闯绝命岛
	/**
	*Define Method
	*BlueprintNativeEvent,增加勇闯绝命岛临时快捷栏数据
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void AddYCJMDSkillBars(const int32& index, const int32& qbType, const int32& id);

	/**
	*Define Method
	*BlueprintNativeEvent,移除勇闯绝命岛快捷栏数据
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void RemoveYCJMDSkillBars(const TArray<int32>& indexs);

	/**
	*Define Method
	*BlueprintNativeEvent,进入勇闯绝命岛显示临时快捷栏
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnEnterYCJMDShowSkillBar();

	/**
	*Define Method
	*BlueprintNativeEvent,离开勇闯绝命岛隐藏临时快捷栏
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnLeaveYCJMDHideSkillBar();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_AddYCJMDSkillBarData(const int32& index, const int32& type, const int32& id);

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_RemoveYCJMDSkillBarData(const int32& index);

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_ExchangeYCJMDSkillBarData(const int32& srcIndex, const int32& dstIndex);

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		int32 GetSkillRequireItemID(const int32& skillID);

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		TArray<FQB_ITEM> GetYCJMDSkillBarDatas();

#pragma endregion
	/**
	*Define Method
	*BlueprintNativeEvent,显示血条和血条信息
	*
	*param maxValue 血条最大值
	*param curValue 血条最小值
	*param describe 描述
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowFHJNSpecialWidget(const int32& maxValue, const int32& curValue, const FString& describe);
	/**
	*Define Method
	*BlueprintNativeEvent,移除血条
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void HideFHJNSpecialWidget();

	/**
	*Define Method
	*BlueprintNativeEvent,更新血条
	*
	*param maxValue 血条最大值
	*param curValue 血条最小值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void UpdateFHJNSpecialWidget(const int32& maxValue, const int32& curValue);

#pragma region CST-9348 焚火金牛

#pragma endregion



#pragma region CST-5301 天之幻境
	/**
	*Define Method
	*BlueprintNativeEvent,开始掉落法宝
	*
	*param scriptIDList 掉落的法宝列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void StartFallTZHJFabao(const TArray<FString>& scriptIDList);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void StopFallTZHJFabao();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_inPosRefreshFabao(const FString& scriptID, const FVector& Position_1, const int32& parentID);

#pragma endregion

#pragma region CST-6350 拜访任务 灵兽圈
	/**
	*Define Method
	*BlueprintNativeEvent,显示贴屏按钮
	*
	*param time 按钮cd时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void NotifyLXQDisplayScreen(const int32& time);
	/**
	*Define Method
	*BlueprintNativeEvent,关闭贴屏显示按钮
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void NotifyLXQCloseScreen();
	/**
	*Define Method
	*BlueprintNativeEvent,通知客户端进入灵兽圈瞄准模式
	*
	*param 技能ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnLXQEnterAimingMode(const int32& skillID);
	/**
	*Define Method
	*BlueprintNativeEvent,通知客户退出灵兽圈瞄准模式
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnLXQLeaveAimingMode();
	/**
	*Define Method
	*BlueprintNativeEvent 通知服务器灵兽圈是否命中
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_lXQIsHit(const int32& isHit);
	/**
	*Define Method
	*BlueprintNativeEvent 按下进入瞄准模式按钮通知服务器
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_LXQEnterAimingMode();
	/**
	*Define Method
	*BlueprintNativeEvent 按下退出瞄准模式按钮通知服务器
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_LXQLeaveAimingMode();

#pragma endregion

#pragma region CST-8734 攻城战
	/**
	* Define method
	* 攻城战中玩家部队数据
	*
	* @return 无
	*/
	void CLIENT_OnOpenBarracksArmyWin(const FVariant& Var,int32 defaultArmyIndex);

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|RoleSpaceContentInterfaceC")
		void OnOpenBarracksArmyWin(int32 defaultArmyIndex);

	//通过ID获得攻城战玩家部队数据
	UFUNCTION(BlueprintCallable, Category = "Game|RoleSpaceContentInterfaceC")
		bool GetAttCityRoleArmyDataByID(int32 ID, FROLEARMYDATA& RoleArmyData);

	/**
	*Define Method
	*BlueprintCallable 选择某支部队出战
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CallArmyToWar(const int32& id);

	/**
		*Define method
		*BlueprintNativeEvent，更新攻城战成员数据到客户端
		*
		*@return 无
		*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZMemberDataToOtherClient(const int32& id, const FString& name, const int32& belongSide, const int32& killEnemy, const int32& dead, const int32& assists, const int32& killSoldier, const int32& totalExploit, const FString& teamName,const int32& ownerSoldierDeadNum,const FString& enemyTeamName);

	/**
	*Define method
	*BlueprintNativeEvent，接受攻城战成员数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ReceiveGCZOtherMemberData(const int32& id, const FString& name, const int32& belongSide, const int32& killEnemy, const int32& dead, const int32& assists, const int32& killSoldier, const int32& totalExploit, const FString& teamName, const int32& ownerSoldierDeadNum, const FString& enemyTeamName);

	//通知界面显示队伍名称
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void BP_ShowTeamName();

	void AddGCZMemberData(const int32& id, const FString& name, const int32& belongSide, const int32& killEnemy, const int32& dead, const int32& assists, const int32& killSoldier, const int32& totalExploit, const int32& ownerSoldierDeadNum);

	/**
	*Define method
	*BlueprintNativeEvent，更新攻城战成员的击杀敌人数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZKillEnemyDataToClient(const int32& id, const int32& killEnemy);

	/**
	*Define method
	*BlueprintNativeEvent，更新攻城战成员的击杀士兵数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZKillSoldierDataToClient(const int32& id, const int32& killSoldier);

	/**
	*Define method
	*BlueprintNativeEvent，更新攻城战成员的死亡数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZDeadDataToClient(const int32& id, const int32& dead);

	/**
	*Define method
	*BlueprintNativeEvent，更新攻城战成员的助攻数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZAssistsDataToClient(const int32& id, const int32& assists);

	/**
	*Define method
	*BlueprintNativeEvent，更新攻城战成员的总军功数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZTotalExploitDataToClient(const int32& id, const int32& totalExploit);

	/**
	*Define method
	*BlueprintNativeEvent，重登修改数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateGCZMemberDataToOtherClientOnLogin(const int32& srcMemberID, const int32& dstMemberID);

	void CLIENT_UpDateGCZMemberSoldierDeadNumToClient(int32 id, int32 ownerSoldierDeadNum);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void BP_UpDateGCZMemberSoldierDeadNumToClient(int32 id, int32 ownerSoldierDeadNumsss);
	/**
	*Define method
	*BlueprintNativeEvent，显示战旗进度界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowBattleFlagProgressBar(const int32& battleEntityID, const int32& belongType, const int32& occurProgress, const int32& maxProgress);

	/**
	*Define method
	*BlueprintNativeEvent，更新战旗进度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_UpdateBattleFlagProgressBar(const int32& occurProgress, const int32& maxProgress);

	/**
	*Define method
	*BlueprintNativeEvent，战旗归属改变
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnOccupyBelongTypeChanged(const int32& belongType);

	/**
	*Define method
	*BlueprintNativeEvent，隐藏战旗进度界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_HideBattleFlagProgressBar(const int32& battleEntityID);

	/**
	*Define method
	*BlueprintNativeEvent，显示攻城战结算界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowGCZSettlementWnd(const int32& isWin, const int32& costTime, const int32& closeTime);

	/**
	*Define method
	*BlueprintNativeEvent，玩家从底部进入云梯
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ChangeReadyToClimbLadder(const int32& isClimbLadder);

	/**
	*Define method
	*BlueprintNativeEvent，玩家退出攻城战副本
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnLeaveGCZ();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		int32 GetMemberSoldierDeadNumByBelongSide(BELONG_SIDE side);

#pragma endregion

#pragma region 帮会掠夺战
	/**
	*Define method
	*BlueprintNativeEvent，显示帮会掠夺战结算界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnShowTongPlunderSettlementWnd(const int32& isWin, const int32& costTime, const int32& closeTime);
	void CLIENT_ShowTongPlunderSettlementWnd(const int32& isWin, const int32& costTime, const int32& closeTime, const FVariant& MemberInfos);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnTongPlunderSoldierDead();
	///<帮会掠夺战士兵死亡，SoldierType： 0 敌方士兵，1 我方士兵
	void CLIENT_TongPlunderSoldierDead(const int32& SoldierType);

#pragma endregion

#pragma region CST-6351 接火把

	/**
	*Define Method
	*BlueprintNativeEvent 玩家是否接住火把
	*
	*param isCatch 是否接住
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void RPC_JHBIsCatch(bool isCatch);

#pragma endregion

	/**
	*Define Method
	*BlueprintNativeEvent,进入勇闯绝命岛天空飞行模式
	*
	*param FlyPathId
	*
	*@return 无
	*/
	void OnStartYCJMDSkyFlyModel(const FString& FlyPathId);

	// 改变 跳伞状态
	void ChangeParachuteState(const PARACHUTE_STATE state);
	// 服务器 同步跳伞状态
	void Set_ParachuteState(const uint8& newState, const uint8& oldState);
	
	// 跳伞状态中，在飞行器上
	void OnYCJMSkyFly();
	// 开伞
	void OnOpenParachute();
	// 显示跳伞的高度和下落速度
	void OnShowYCJMDUI();
	void OnHideYCJMDUI();


#pragma region CST-9960 阵营战场-勇闯绝命岛

	/**
	*Define Method
	*BlueprintNativeEvent,显示双方阵营存活人数
	*
	*param xAmount 仙道存活人数
	*param mAmount 魔道存活人数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowCampYCJMDPopulationUI(const int32& xAmount, const int32& mAmount);

	/**
	*Define Method
	*BlueprintNativeEvent,无所遁形，大小地图显示敌对阵营存人位置
	*
	*param ID
	*param Position
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void showCampYCJMDPosition(const int32& ID, const FVector& Position);

	/**
	*Define Method
	*BlueprintNativeEvent,无所遁形，大小地图显示同阵营存人位置
	*
	*param ID
	*param Position
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void ShowSameCampYCJMDPos(const int32& ID, const FVector& Position);

	/**
	*Define Method
	*BlueprintNativeEvent,无所遁形，隐藏大地图玩家位置
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void HideCampYCJMDPosition();

	/**
	*Define Method
	*BlueprintNativeEvent,玩家离开副本
	*
	*param ID
	*param Position
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnPlayerLeaveYCJMD(const int32& ID);

	/**
	*Define Method
	*BlueprintNativeEvent,异宝现世，大小地图显示超级宝箱位置
	*
	*param Position
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void showCampYCJMDBoxPosition(const FVector& Position);

	/**
	*Define Method
	*BlueprintNativeEvent,毒气失控，大小地图显示灵气圈
	*
	*param Position
	*param Radius
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void showCampYCJMDReikiCircle(const FVector& Position, const int32& Radius);

	/**
	*Define Method
	*BlueprintNativeEvent,勇闯绝命岛服务器结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void OnShowCampYCJMDCountdown(const FString& EndTimeStr);

	/**
	*Define Method
	*BlueprintNativeEvent,勇闯绝命岛清除大地图标记
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CleanCampYCJMDIcon(const FString& ScriptID);
	
	/**
	*Define Method
	*显示勇闯绝命岛结算界面
	@param
	*@return 无
	*/
	void ShowYCJMDFinalUI();
	
#pragma endregion

#pragma region CST-4246 九字真言
	/**
	*Define Method
	*BlueprintNativeEvent,增加/移除入道BUFF标记通知
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void OnNotifyJZZYRuDaoBuff(bool isAdd);

	/**
	*Define Method
	*BlueprintNativeEvent,BUFF入体倒计时
	@param t:时间（<=0,移除倒计时，>0:倒计时生效）
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void onNotifyJZZYBuffTime(const int32& t);

	/**
	*Define Method
	*BlueprintNativeEvent,熄灭点亮的点
	@param amount:需要熄灭的数量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void onExtinguishLight(int32 amount);

	TArray<FString> FirePointRecord;//九字真言副本火焰记录 仅供特殊副本进行使用

#pragma endregion

#pragma region CST-9008 勇闯绝命岛（远程）
	/**
	*Define Method
	*BlueprintNativeEvent,显示灵能界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void ShowShootYCJMDLNUI(bool isshow);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnShowShootYCJMDLNUI(bool IsShow);
	/**
	*Define Method
	*BlueprintNativeEvent,修改玩家子弹槽的最大数量
	@param maxAmount 子弹物品ID
	*@return 无
	*/
	void SetYCJMDBulletSlotMax(const int32& BulletID);
#pragma endregion

#pragma region 练兵场
	/**
	*Define Method
	*BlueprintNativeEvent,添加玩家信息
	@param PlayerID 玩家ID
	@param PlayerName 玩家名称
	@param BelongSide 0：攻方/1：守方
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_AddTrainingGroundMember(const int32& PlayerID, const FString& PlayerName, const int32& BelongSide);
	// 更新死亡次数
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_updateLBCDeadData(const int32& PlayerID, const int32& Num);
	// 更新杀敌次数
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_updateLBCKillData(const int32& PlayerID, const int32& Num);
	// 更新杀怪次数
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_updateLBCKillMTData(const int32& PlayerID, const int32& Num);
	// 更新损失士兵数量
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_updateLBCLoseSDData(const int32& PlayerID, const int32& Num);
	// 练兵场结果 Exploit:获得军功， IsWin：是否胜利
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnLBCSpaceResult(const int32& Exploit, const int32& IsWin, const int32& LiftTime);
	//进入不可移动侦察模式
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnEnterScout();
	//退出不可移动侦察模式
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnEndScout();

	void CLIENT_OnEnterTrainSoldierGround(float ArmLength, FVector CameraRotation);
	void CLIENT_OnLeaveTrainSoldierGround();
#pragma endregion

#pragma region 虚空探宝
	//探宝次数通知
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_notifyProbeTimes(const int32& times);

#pragma endregion
#pragma region 通天塔
	/**
	*Define Method
	*BlueprintNativeEvent,通天塔Boss火焰牛显示暴怒值界面
	*
	*param angerValu 暴怒值
	*
	*@return 无
	*/
	void ShowFireCowAngerUI(const int32& angerValue);

#pragma endregion

#pragma region 禁地采药
	/**
	*Define Method
	*BlueprintNativeEvent,采集仙草
	*
	*param amount 采集仙草的数量
	*
	*@return 无
	*/
	void CollectedXLC(const int32& amount);

#pragma endregion

#pragma region 五行画卷
	/**
	*Define Method
	*BlueprintNativeEvent,五行画卷属性改变
	*
	*param AttrIndex 机关的五行属性index
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_WXHJChangeAttr(const int32& AttrIndex);
	/**
	*Define Method
	*BlueprintNativeEvent,显示五行画卷属性界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_ShowWXHJAttrUI(const int32& isOpen);

#pragma endregion


#pragma region 大荒战场
	/**
	*Define Method
	*BlueprintNativeEvent,玩家上可移动骑乘
	*
	*@param:InVehicleID 骑乘ID
	*@param:InDriverID 司机ID
	*@param:SocketName 插槽名称
	*@param:CarrierId 玩家骑乘对应的载体编号ID 
	*@param:CanControlMove 玩家自己是否能控制客户端移动
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnMountVehicle(int32 InVehicleID, int32 InDriverID, const FString& SocketName, const FString& CarrierId, uint8 CanControlMove);

	/**
	*Define Method
	*BlueprintNativeEvent,玩家下可移动骑乘
	*
	*@param:InVehicleID 骑乘ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnDismountVehicle(int32 InVehicleID);
	///<请求上/下骑乘
	void CELL_mountVehicle(int32 vehicleID);
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
	void CELL_dismountVehicle();
	void CELL_reqVehicleData(int32 targetPlayerID, int32 InVehicleID);
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_InviteMountVehicle(int32 targetPlayerID);
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void CELL_ApplyMountVehicle(int32 targetPlayerID);
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		bool HasVehicle();
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		bool IsVehicleDriver();

	///< 快捷键屏蔽/恢复
	void SetIsEnabledQuickBar(const uint8& bEnalbe);
#pragma endregion

#pragma region 机缘玩法 CST-12052

	/**
	*Define Method
	*BlueprintNativeEvent,机缘玩法结算通知
	*
	*@param:itemStr 奖励物品 like:itemID:amount|itemID:amount|...
	*@param:grade 通关档次 like:1,2,3...
	*@param:timeStr 通关时长 like：10分20秒
	*@param:dieNum 死亡次数
	*@param:countDown：倒计时
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void CLIENT_OnJiYuanSpaceJieSuan(const FString& itemStr, uint8 grade, const FString& timeStr, int32 dieNum, uint8 countDown);

#pragma endregion


#pragma region 晶石狩猎场 机缘玩法

	/**
	*Define Method
	*BlueprintNativeEvent,机缘玩法结算通知
	*
	*@param: CostTime 通关消耗时间
	*@param: Level 通关档次
	*@param: RewardValue 奖励金精值
	*@param: DieNumber 玩家死亡次数
	*
	*@return 无
	*/
	void CLIENT_ShowJSSLCJiYuanJieSuanWnd(const int32& CostTime, const int32& Level, const int32& RewardValue, const int32& DieNumber);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleSpaceContentInterface")
		void OnShowJSSLCJiYuanJieSuanWnd(const int32& CostTime, const int32& Level, const int32& RewardValue, const int32& DieNumber);
		

#pragma endregion
	/**
	*Define Method
	*BlueprintNativeEvent,	通知客户端玩家是否是第一次进入该副本

	@param IsFirst
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "cs3|RoleSpaceContentInterface")
		void SetIsFirstEnterCopy(bool IsFirst);

	/**
	*Define Method
	*显示帮会副本结算奖励界面
	@param countDownTime 倒计时
	@param rewardBarracksExp 奖励经验
	@param rewardContribution 奖励帮贡
	@param rewardTongMoney 奖励金钱
	@param useTime 花费时间
	@param level 1:入道  2：出尘 3：问鼎 4：超凡
	@param buff buffID|buffID|...
	@param itemStr itemID:amount|itemID:amount|...
	@param score 分数
	*@return 无
	*/
	void ShowTongSpaceSettlementWin(const int32& countDownTime, const int32& useTime, const int32& rewardBarracksExp, const int32& rewardContribution, const int32& rewardTongMoney, const FString& buff, const FString& itemStr, const int32& score,  const int32& level);

	/**
	*Define Method
	*gm使用(不知道加在哪里合适就加这里了)
	@param winID 界面ID
	@param isOpen 0/1 关闭/打开
	*@return 无
	*/
	void OnOpenWindow(const FString& winID, const int32& isOpen);

	/**
	*Define Method
	*播放光效（获得绿色品质物品）
	@param 
	*@return 无
	*/
	void CLIENT_PlayEffect(const FString& effectID);

	/**
	*Define Method
	*播放光效（获得绿色品质物品）
	@param
	*@return 无
	*/
	void CLIENT_PlaySound(const FString& soundID);
	//显示阵营战场结算额外奖励
	void ShowZYJJReward(const FVariant& rewardData);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_StartHLDRound();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_throwFishRod(const int32& INT32_1, const int32& INT32_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_catchFishCheck(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_transformShield();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_dismountHeHua();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_move(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMagicMazeEndFly();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMagicMazeNodeFly();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_playerAnswer(const int32& INT32_1, const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_selectNextQuestion();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_openAddSpeedExpendEnergy();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_closeAddSpeedExpendEnergy();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveFireDamage();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveFireDamageEnd();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_destroyLinkTrap(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_enterThunderArea();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_randomMagicMazeZhuanPan();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onPlayeTrampleLotus(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onFishHitPlayer();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onTortureNotice(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onEncounteredInDead();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCameraEndMove();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMoveStartTorureNotice();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onMoveEndTorureNotice();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onPlayerTouchLaser();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onPlayerBeHammer();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onPlayerMetSandman();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_FireWallCallBack();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onArmorLockBroke(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_onPlayerBeHammer(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_onRoleDismountCopyGlede(const int32& isThrow);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_OnPlaySpaceIntroduceVoice();

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|RPC")
		void OnLeaveScenes_BP();

	virtual void onLeaveWorld() override;
	virtual void InitBlueCB() override;
	virtual void OnLeaveScenes() override;
private:
	void UpdateOtherPlayer();
protected:

	int32 CurEffectUID = -1;	//当前粒子UID

public:
	UPROPERTY(BlueprintReadWrite)
		bool bIsMovingOnHeHua;//在荷花上是否移动
	UPROPERTY(BlueprintReadWrite)
		bool bIsMovingToCallCellOnHeHua;//在荷花上移动是否已通知服务器
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> indexList;//鬼域迷阵传送门颜色列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FVector> desPosList;//鬼域迷阵传送门对应坐标列表
	UPROPERTY(BlueprintReadWrite)
		FString FlyRoute;//老鹰的飞行路线
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> correspondList;//幻阵迷宫对应
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> resultList;//幻阵迷宫子副本完成结果
	UPROPERTY(BlueprintReadOnly)
		FString JSZZSpaceSctriptID; ///< 金树种子 种植地图
	UPROPERTY(BlueprintReadOnly)
		FVector JSZZPlantPosition; ///<金树种子 种植位置
	UPROPERTY(BlueprintReadOnly)
		bool bIsEnterYCJMD;//是否进入勇闯绝命岛
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsHitNotifyState;//是否已触发石柱跳跃通知状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsHasRuDaoBuffFlag;//是否拥有了入道BUFF（CST-4246 九字真言）

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap< int32, FAttCityMemberData > AttCityActivityData; //攻城战战场数据

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap< int32, FAttCityMemberData > LBCActivityMap; //练兵场战场数据

	UPROPERTY(BlueprintReadOnly)
		TArray<FROLEARMYDATA> AttCityRoleArmyData; //攻城战玩家部队数据

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FString> AttCityTitleNameData; ///<攻城战攻守放名字数据

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<FString, FAttCityMemberData> TongPlunderData; ///<帮会掠夺战数据

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FString> TongPlunderTitleNameData; ///<帮会掠夺战攻守放名字数据
	UPROPERTY(BlueprintReadOnly)
		int32 TongPlunderEnemySoldierDeadNum; ///<帮会掠夺战敌方士兵伤亡
	UPROPERTY(BlueprintReadOnly)
		int32 TongPlunderOurSoldierDeadNum; ///<帮会掠夺战我方士兵伤亡

	UPROPERTY(BlueprintReadOnly)
		bool IsReadyClimbLadder; ///<玩家是否已经准备爬云梯

	UPROPERTY(BlueprintReadOnly)
		int32 probeTimes = 0; ///<探宝次数

	TMap<int32, FQB_ITEM> YCJMDQuickBarItems;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool bIsFirstEnterCopy = false;
	UPROPERTY()
		AEquipBuildClientCharacter* EquipBuildClientCharacter = nullptr;

	UPROPERTY(BlueprintReadOnly)
		int32 YCJMDBulletID = 302010080; ///<勇闯绝命岛子弹ID
	UPROPERTY(BlueprintReadOnly)
		int32 YCJMDBulletMaxAmont; ///<勇闯绝命岛子弹最大数量
	UPROPERTY(BlueprintReadOnly)
		bool bIsEnableQuickBar = true;///<大荒战场是否置灰快捷栏
	UPROPERTY(BlueprintReadOnly)
		FZYJJRewardData ZYJJRewardData;///<5人竞技副本奖励数据
private:
	FDelegateHandle FlyRouteHandle;//起飞路线绑定事件的句柄
	float RisingPercent;
	FTimerHandle JumpToDsPosHandle;
	FTimerHandle DelayBoardBoatHandle;
	FDelegateHandle MountVehicleHandle;
	int32 VehicleID;//大荒战场骑乘ID
	int32 DriverID;//大荒战场骑乘ID
};
