#pragma once

#include "CoreMinimal.h"
#include "Manager/Delegate/SpaceDelegateObject.h"
#include "GameData/Item/ToolCost.h"
#include "GameData/ZYJJRewardData.h"
#include "SpaceContentDelegateObject.generated.h"

/**
 *  副本玩法委托声明对象
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnShowCompassUI);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnNotifyBuildPos, FVector, BuildPos, int32, NpcID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOccupyBuildResult, int32, Result);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnShowBuildUI, FString, EndBuildTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnStartBuildCaveHouse, int32, DongfuID, FString, EndStrTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnEnterCaveHouse, int32, DongfuID, bool, IsSelfCaveHouse);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnStartBuildUpgrade, int32, BuildType, float, RemainUpLevelTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnXKTBTextStatusChange, FString, CurrentText, int32, state);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnXKTBCancelDisplayCurrentText);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnAddTrainingGroundMember, int32, PlayerID, FString, PlayerName, int32, BelongSide);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateLBCDeadData, int32, PlayerID, int32, Num);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateLBCKillData, int32, PlayerID, int32, Num);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateLBCKillMTData, int32, PlayerID, int32, Num);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnLBCSpaceResult, int32, Exploit, int32, IsWin, int32, LiftTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnRoleCmdControlled, int32, Category, FString, ScriptID, int32, EntityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_EightParams(FOpenTrainSoldierGroundDetails, int32, npcID, FString, name, int32, lineNumber, int32, npcState, int32, trainGroundType, const TArray<FString>&, warNameList, const TArray<int32>&, warProfessionList, bool, isTrainSoldier);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOpenTrainSoldierGroundTask, FString, TaskDsp, int32, RewardExp);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FRefreshTrainSoldierGroundTask);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateTrainSoldierTaskState, int32, Index, int32, State);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateLBCLoseSDData, int32, PlayerID, int32, Num);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_SevenParams(FOnReceiveTrainSoldierTaskResult, int32, QuestIndex, int32, Result, int32, BattackID, int32, Exp, int32, addExp, int32, LossNum, FString, SoldierScriptID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_SixParams(FOnShowLbcTaskResult, int32, result, FString, fistGuardScriptID,int32, exp, int32, addExp, int32, lossNum, FString, cmdrerScriptID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdateTrainSoldierGroundAreaDatas);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnEnterTrainSoldierGround);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnLeaveTrainSoldierGround);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FShowLingTianPlantUI, int32, EntityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FShowGrowUpMsgUI, int32, EntityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOpenWorkShopQuenchingUI, int32, EntityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOpenLingQuanUI, int32, EntityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_SixParams(FOnFirstUpdateDFListDatas, int32, LineNumber, const TArray<int32>&, AllLineNumber, int32, TotalPage, int32, Page, int32, FreeDfNum, const TArray<FDongFuData>&, DongFuDatas);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnUpdateDFListDatas, int32, LineNumber, int32, Page, const TArray<FDongFuData>&, DongFuDatas);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnReceiveDongfuChallengeInvite, FString, PlayerName, int32, CanRefuseTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOtherAcceptDongfuChallenge, FString, PlayerName);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnShowFireCowAngerUI, int32, angerValue);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FActiveBattleFormations);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FCloseBattleFormations);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_NineParams(FOnShowTongSpaceSettlementUI, int32, CountDownTime, int32, UseTime, int32, RewardBarracksExp, int32, RewardContribution, int32, RewardTongMoney, FString, Buff, FString, ItemStr, int32, Score, int32, Level);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnOpenSpecialBarracks);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNotifyCollectedXLCAmount, int32, amount);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnRecvActivityTimesData);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnStartBuildRepair, int32, BuildType, float, RemainRepairTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnEndBuildRepair, int32, BuildType);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDestroyGTBattery, int32, BatteryID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRequestAttackPos, FVector, AttackPos);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnOccupyGTBarrack, int32, BelongSide, FString, ScriptID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnRequestAttackPosNone);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FTeleportCDIsReady);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnInitGTProtectDatasOver, const TArray<FVector>&, TeleportPos, int32, TeleportCD);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnInitGTAttackDatasOver);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdateIsCanOpenBarracks);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_EightParams(FOpenDFActtiveResultUI, int32, IsChallengeActive, int32, Result, FString, RwItemStr, int32, RwMoney, int32, RwPsionic, const TArray<int32>&, IDList,int32, CombatTime,int32,DeadCount);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnShowCommitSoldierAndLevel, int32, level, int32, amount, int32, money);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdateOccupyInfo);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdateDeclareInfo);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdateBeDeclaredInfo);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdateLbcStatusInfo);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FShowChallengeMsg, FVector, Position);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnInitDFMonsterInfo, const TArray<int32>&, entityIDList);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAddDFMonsterInfo, int32, entityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnGuardReviveTime, int32, entityID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnShowLoopQuestWin);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnShowCurrGotGoldAmount, int32, amount);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnShowHaoLinGuUIEvent, float, time, FString, AllKeys);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnHaoLinGuKeyBackEvent, int32, IsSuccess, FString, KeyName, int32, ContinueInedx);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHaoLinGuUpdateAllKeysEvent, FString, AllKeys);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnYCJMSkyFly);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnShowYCJMDUI);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnHideYCJMDUI);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FUpdateYCJMDSpeed, float, Speed);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(FOnOpenJoinGCZWin, int32, NPCID, const TArray<int32>&, Numbers, const TArray<FString>&, StartTimes, const TArray<int32>&, RemainJoinNums);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNotifyToStartMatchGCZ, int32, CurNumber);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnNotifyCancelMatchGCZ);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnShowFlyPatrolLine, FString, FlyPathId);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnCreateTempEquipBar, const TArray<int32>&, ItemOrders, const TArray<int32>&, ItemIDs);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnRemoveTempEquipBar);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnBattleMatchStart);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetQuickBarEnabled, bool, isEnabled);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetZYJJReward, FZYJJRewardData, ZYJJReward);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnLingMaiBossDamageChanged, int32, DamageCamp, float, DamagePercent);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnLingMaiBossHPChanged, int32, HP, int32, HPMax);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnShowYCJMDFinalUI);
UCLASS()
class CHUANGSHI_API USpaceContentDelegateObject : public USpaceDelegateObject
{
	GENERATED_BODY()
public:

#pragma region	/** 轮回秘境 */
	//打开淬炼界面
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOpenWorkShopQuenchingUI OpenWorkShopQuenchingUIEvent;
	//打开灵泉界面
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOpenLingQuanUI OpenLingQuanUIEvent;
	//洞府守卫复活时间
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnGuardReviveTime OnGuardReviveTime;
#pragma endregion

#pragma region	/** 轮回秘境洞府 */
	/**
	*打开罗盘界面
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnShowCompassUI OnShowCompassUIEvent;
	/**
	*通知地基方向位置
	*@param	buildPos 位置
	*@param	npcID
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnNotifyBuildPos OnNotifyBuildPosEvent;
	/**
	*占领基地结果
	*@param	result 结果 1：占领成功关闭界面，0：占领失败，重新显示探索
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnOccupyBuildResult OnOccupyBuildResultEvent;
	/**
	*通知打开洞府头顶UI界面
	*@param	endBuildTime 建造结束时间
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnShowBuildUI OnShowBuildUIEvent;
	/**
	*通知打开建造洞府界面
	*@param	dongfuID 洞府ID
	*@param	endStrTime 保护状态的结束时间
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnStartBuildCaveHouse OnStartBuildCaveHouseEvent;
	/**
	*通知打开进入洞府界面
	*@param	dongfuID 洞府ID
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnEnterCaveHouse OnEnterCaveHouseEvent;
	/**
	*开始升级某建筑
	*@param	buildType 建筑类型
	*@param	RemainUpLevelTime  剩余升级时间
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnStartBuildUpgrade OnStartBuildUpgradeEvent;
	//灵泉全部灵能数值更新
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnPropertyChangedEventInt OnCaveHousePsionicSumChanged;
	//灵泉当前血量数值更新
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnPropertyChangedEventInt OnLingQuanCurrHPChanged;
	//第一次更新洞府列表数据（打开界面时）
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnFirstUpdateDFListDatas OnFirstUpdateDFListDatasEvent;
	//更新洞府列表数据（翻页时）
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnUpdateDFListDatas OnUpdateDFListDatasEvent;
	//收到洞府挑战
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnReceiveDongfuChallengeInvite ReceiveDFChallengeInviteEvent;
	//被挑战者回复
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnOtherAcceptDongfuChallenge OtherAcceptDongfuChallengeEvent;
	/**
	*开始修复某建筑
	*@param	buildType 建筑类型
	*@param	RemainRepairTime  剩余修复时间
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnStartBuildRepair OnStartBuildRepairEvent;
	/**
	*结束修复某建筑
	*@param	buildType 建筑类型
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnEndBuildRepair OnEndBuildRepairEvent;

	/**
	*打开洞府活动结算界面
	*@param	IsChallengeActive （0：掠夺战，1：争夺战）
	*@param	Result  活动结果（0：攻方失败，1：攻方胜利，2：守方失败，3：守方胜利）
	*@param	RwItemStr 奖励物品  格式：物品ID:数量|物品ID:数量|物品ID:数量 (比如：101040128:1|101040129:2|101040130:3|)
	*@param	RwMoney  奖励金钱   
	*@param	RwPsionic 奖励灵能
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOpenDFActtiveResultUI OpenDFActtiveResultUIEvent;

#pragma endregion

#pragma region	/** 轮回秘境灵田种植 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FShowLingTianPlantUI ShowLingTianPlantUIEvent;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FShowGrowUpMsgUI ShowGrowUpMsgUIEvent;
#pragma endregion

#pragma region	/** 轮回秘境阵图 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FActiveBattleFormations OnActiveBattleFormationsEvent;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FCloseBattleFormations OnCloseBattleFormationsEvent;
#pragma endregion

#pragma region	/** 轮回秘境大地图 */
	//显示洞府标记
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FShowChallengeMsg ShowChallengeMsg;
#pragma endregion

#pragma region	/** 轮回秘境傀儡 */
	//初始化傀儡
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnInitDFMonsterInfo OnInitDFMonsterInfo;
	//添加傀儡
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LHMJ")
		FOnAddDFMonsterInfo OnAddDFMonsterInfo;
#pragma endregion

#pragma region	/** 虚空探宝 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|XKTB")
		FOnXKTBTextStatusChange OnXKTBTextStatusChangeEvent;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|XKTB")
		FOnXKTBCancelDisplayCurrentText OnXKTBCancelDisplayCurrentText;
#pragma endregion

#pragma region	/** 九字真言 */
	//真言类型变化
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|MonsterExtJiuZiZhenYan")
		FOnPropertyChangedEventEntityIDInt OnZhenyanTypeChanged;
	//当前被Boss腐化进度
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|MonsterExtJiuZiZhenYan")
		FOnPropertyChangedEventEntityIDIntInt OnBossCorruptChanged;
	//被玩家或boss占领
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|MonsterExtJiuZiZhenYan")
		FOnPropertyChangedEventEntityIDInt OnZhenYanBeOccupied;
	//真言开始被腐化
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|MonsterExtJiuZiZhenYan")
		FOnPropertyChangedEventInt OnZhenYanStartOccupy;
#pragma endregion

#pragma region	/** 练兵场 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOpenTrainSoldierGroundDetails OnOpenTrainSoldierGroundDetails;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnPropertyChangedEventString OnOccupyPlayerNameChanged;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnPropertyChangedEventInt OnDeclareWarStateChanged;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOpenTrainSoldierGroundTask OnOpenTrainSoldierGroundTask;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FRefreshTrainSoldierGroundTask OnRefreshTrainSoldierGroundTask;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateTrainSoldierTaskState OnUpdateTrainSoldierTaskState;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnReceiveTrainSoldierTaskResult OnReceiveTrainSoldierTaskResult;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnShowLbcTaskResult OnShowLbcTaskResult;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateTrainSoldierGroundAreaDatas OnUpdateTrainSoldierGroundAreaDatas;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnEnterTrainSoldierGround OnEnterTrainSoldierGround;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnLeaveTrainSoldierGround OnLeaveTrainSoldierGround;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnDestroyGTBattery OnDestroyGTBattery;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnRequestAttackPos OnRequestAttackPos;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnOccupyGTBarrack OnOccupyGTBarrack;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnRequestAttackPosNone OnRequestAttackPosNone;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FTeleportCDIsReady TeleportCDIsReady;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnInitGTProtectDatasOver OnInitGTProtectDatasOver;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnInitGTAttackDatasOver OnInitGTAttackDatasOver;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateOccupyInfo OnUpdateOccupyInfo;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateDeclareInfo OnUpdateDeclareInfo;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateBeDeclaredInfo OnUpdateBeDeclaredInfo;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateLbcStatusInfo OnUpdateLbcStatusInfo;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateBeDeclaredInfo OnNotifyDeclareFight;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TrainSoldierGround")
		FOnUpdateBeDeclaredInfo OnNotifyBeDeclaredFight;
#pragma endregion

#pragma region	/** 养兵争夺战 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|baracks")
		FOnAddTrainingGroundMember OnAddTrainingGroundMember;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|baracks")
		FOnUpdateLBCDeadData OnUpdateLBCDeadData;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|baracks")
		FOnUpdateLBCKillData OnUpdateLBCKillData;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|baracks")
		FOnUpdateLBCKillMTData OnUpdateLBCKillMTData;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|baracks")
		FOnLBCSpaceResult OnLBCSpaceResult;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|baracks")
		FOnUpdateLBCLoseSDData OnUpdateLBCLoseSDData;
#pragma endregion

#pragma region	/** 攻城战副本 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|gcz")
		FOnPropertyChangedEventInt OnRoleRemoveSoldier;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|gcz")
		FOnRoleCmdControlled OnRoleCmdControlled;
	/**
	* 打开参加攻城战面板
	* npcID NPCID
	* Numbers 攻城战场次
	* StartTimes 攻城战开始时间
	* RemainJoinNums 攻城战剩余参加人数
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|gcz")
		FOnOpenJoinGCZWin OnOpenJoinGCZWinEvent;
	/**
	* 通知开始匹配 显示匹配界面
	* CurNumber 当前匹配进度
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|gcz")
		FOnNotifyToStartMatchGCZ OnNotifyToStartMatchGCZEvent;
	/**
	* 通知取消匹配 关闭匹配界面
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|gcz")
		FOnNotifyCancelMatchGCZ OnNotifyCancelMatchGCZEvent;

#pragma endregion

#pragma region	/** 通天塔 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TongTianTa")
		FOnShowFireCowAngerUI  OnShowFireCowAngerUI;
#pragma endregion

#pragma region	/** 帮会副本 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TongSpace")
		FOnShowTongSpaceSettlementUI  OnShowTongSpaceSettlementUIEvent;
#pragma endregion

#pragma region	/** 特殊天兵营 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|SpecialTBY")
		FOnOpenSpecialBarracks OnOpenSpecialBarracks;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|SpecialTBY")
		FOnShowCommitSoldierAndLevel OnShowCommitSoldierAndLevel;
#pragma endregion

#pragma region	/** 禁地采药 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|JDCY")
		FOnNotifyCollectedXLCAmount OnNotifyCollectedXLCAmount;
#pragma endregion

#pragma region	/** 活动日程 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|Crond")
		FOnRecvActivityTimesData OnRecvActivityTimesDataEvent;
#pragma endregion

#pragma region	/** 天兵营 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TBY")
		FOnUpdateIsCanOpenBarracks OnUpdateIsCanOpenBarracks;
#pragma endregion

#pragma region	/** 剧情副本显示环任务追踪界面 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LoopQuest")
		FOnShowLoopQuestWin OnShowLoopQuestWin;
#pragma endregion

#pragma region	/**金枝玉庭获取金币数量更新 */
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|JZYT")
		FOnShowCurrGotGoldAmount OnShowCurrGotGoldAmount;
#pragma endregion

#pragma region	/**浩灵谷QTE玩法 */
	/**
	*浩灵谷显示UI功能
	*
	*@param time 时间
	*@param AllKeys 当前记录的所有按键
	*
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|HLG|QTE")
		FOnShowHaoLinGuUIEvent OnShowHaoLinGuUIEvent;
	/**
	*浩灵谷返回按键消息
	*
	*@param IsSuccess 是否成功 0：成功 1：失败
	*@param KeyName 按键名
	*
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|HLG|QTE")
		FOnHaoLinGuKeyBackEvent OnHaoLinGuKeyBackEvent;
	/**
	*浩灵谷QTE玩法重新生成随机字符串更新
	*
	*@param AllKeys 当前记录的所有按键
	*
	*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|HLG|QTE")
		FOnHaoLinGuUpdateAllKeysEvent OnHaoLinGuUpdateAllKeysEvent;
#pragma endregion

#pragma region	/**大荒战场*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnYCJMSkyFly OnYCJMSkyFly;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnShowYCJMDUI OnShowYCJMDUI;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnHideYCJMDUI OnHideYCJMDUI;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FUpdateYCJMDSpeed OnUpdateYCJMDSpeed;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnShowFlyPatrolLine OnShowFlyPatrolLine;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnCreateTempEquipBar OnCreateTempEquipBar;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnRemoveTempEquipBar OnRemoveTempEquipBar;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnBattleMatchStart OnBattleMatchStart;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnSetQuickBarEnabled OnSetQuickBarEnabled;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|YCJMD")
		FOnShowYCJMDFinalUI OnShowYCJMDFinalUI;
#pragma endregion
	
#pragma region	/**5人阵营竞技奖励*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|ZYJJ")
		FOnSetZYJJReward OnSetZYJJReward;
#pragma endregion
	
#pragma region	/**灵脉战场Boss伤害*/
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LMZCBoss")
		FOnLingMaiBossDamageChanged OnLingMaiBossDamageChanged;
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|LMZCBoss")
		FOnLingMaiBossHPChanged OnLingMaiBossHPChanged;
#pragma endregion
};