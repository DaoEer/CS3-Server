// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Item/ToolCost.h"
#include "GameData/NPCShopData.h"
#include "RoleLunHuiMiJinInterface.generated.h"

/*
* 文件名称：RoleLunHuiMiJinInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-12-09
*/


/**
* 玩家轮回秘境接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleLunHuiMiJinInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("RoleLunHuiMiJinInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleLunHuiMiJinInterface.BP_RoleLunHuiMiJinInterface_C'"); } //获取蓝图对象路径
	/**
	*Define Method
	*BlueprintNativeEvent,进入幻兽捕捉射击模式
	*@param	skillID 射击释放技能
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void EnterHSBZModelTPS(const int32& skillID);

	/**
	*Define Method
	*BlueprintNativeEvent,离开幻兽捕捉射击模式
	*@param	skillID 射击释放技能
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void LeaveHSBZModelTPS();

	/**
	*Define Method
	*BlueprintNativeEvent,捕捉原兽结果
	*@param	result 结果（1：成功，0：失败）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnCatchOriginPetResult(const int32& result);

	/**
	*Define Method
	*BlueprintNativeEvent,通天塔副本失败界面
	*@param	difference 0代表不显示重新挑战按钮， 1代表显示重新挑战按钮
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void TongTinaDaSpaceFailure(const int32& difference);

	/**
	*Define Method
	*BlueprintNativeEvent,通天塔副本成功结算界面
	*@param	money 金钱数
	*@param	exp 经验数
	*@param	itemList 物品 格式：物品ID:数量|物品ID:数量|物品ID:数量 (比如：101040128:1|101040129:2|101040130:3|)
	*@param	difference 1代表显示突破试炼按钮， 0代表显示继续挑战按钮,2代表当前通关的是最后一层
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void TongTinaDaSpaceSuccess(const int32& money, const int32& exp, const FString& itemList, const int32& difference);

	/**
	*玩家点击进入幻兽捕捉射击模式
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onEnterHSBZModelTPS();

	/**
	*玩家切换目标 离开幻兽捕捉射击模式
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onLeaveHSBZModelTPS();

	/**
	*通天塔   重新挑战当前层
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onAgainChallengeCurrentLayer();

	/**
	*通天塔   继续挑战
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onContinueChallengeLayer();

	/**
	*Define Method
	*BlueprintCallable,初始化轮回秘境建筑
	*@param	spaceType 1:洞府（私有），2：仙府（公有）
	*@param	builds {建筑类型：等级} 1：灵泉，2：工坊，3：乾坤鼎，4：兽栏，5：灵田
	*
	*@return 无
	*/
	void CLIENT_initLHMJBuild(const int32& spaceType, const FVariant& BuildVar);

	/**
	*Define Method
	*BlueprintCallable,轮回秘境建筑升级
	*@param	buildType 1：灵泉，2：工坊，3：乾坤鼎，4：兽栏，5：灵田
	*@param	level 等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void CLIENT_OnLHMJBuildLevelChange(const int32& buildType, const int32& level);

	/*
	* 点击洞府按钮，请求玩家洞府所在的线数据
	*/
	UFUNCTION(BlueprintCallable)
		void RequestPlayerDFDatas();
	/*
	*请求回调
	*@param LineNumber 玩家洞府所在的线，如果没洞府 返回1线
	*@param AllLineNumber 轮回秘境一共有几条线
	*@param TotalPage 界面总页数
	*@param FreeDfNum 空余的洞府数量没占领
	*@param DFVari 第一页的洞府数据
	*/
	void OnRequestPlayerDFDatas(const int32& LineNumber, TArray<FVariant>& AllLineNumber, const int32& TotalPage, const int32& FreeDfNum, const FVariant& DFVari);
	/*
	*请求洞府数据
	*@param LineNumber 洞府的几线
	*/
	UFUNCTION(BlueprintCallable)
		void RequestDFDatas(const int32& LineNumber);
	/*
	*请求回调
	*@param TotalPage 界面总页数
	*@param FreeDfNum 空余的洞府数量没占领
	*@param DFVari 第一页的洞府数据
	*/
	void OnRequestDFDatas(const int32& TotalPage, const int32& FreeDfNum, const FVariant& DFVari);

	/*
	*点击翻页按钮，请求洞府数据
	*@param LineNumber 当前界面显示的 第几线
	*@param Page 需要请求的页码（第2页，为2）
	*/
	UFUNCTION(BlueprintCallable)
		void requestDFDatasByPage(const int32& LineNumber, const int32& Page);
	/*
	*请求回调
	*@param DFVari 洞府数据
	*/
	void OnRequestDFDatasByPage(const FVariant& DFVari);

	// 打开界面请求回调，界面显示洞府数据
	void OnFirstShowDFDatas(const int32& LineNumber, const TArray<int32>& AllLineNumber, const int32& TotalPage, const int32& Page, const int32& FreeDfNum, const TArray<FDongFuData>& DongFuDatas);
	// 翻页请求回调，界面显示洞府数据
	void OnShowDFDatas(const int32& LineNumber, const int32& Page, const TArray<FDongFuData>& DongFuDatas);

	/**
	*Define Method
	*BlueprintCallable,玲珑玉令升级
	*@param	level 等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleLunHuiMiJinInterface")
		void CLIENT_onUpgradeJadeItem(const int32& level);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnUpgradeJadeItemBP(const int32& level);
	// 是否占领了洞府/仙府
	UFUNCTION(BlueprintCallable)
		bool IsOccupySpaceType(LHMJ_SPACE_TYPE spaceType);
	// 获取建筑等级
	UFUNCTION(BlueprintCallable)
		int32 GetBuildLevel(LHMJ_BUILD_TYPE buildType);
	// 建筑升级
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnUpdateBuildLevel(const LHMJ_BUILD_TYPE& build, const int32& level);

	/** 
	*Define Method
	*BlueprintNativeEvent,通知打开灵气罗盘UI界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnShowCompassUI();

	/**
	*Define Method
	*BlueprintNativeEvent,通知地基方向位置
	*@param	buildPos 位置
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnNotifyBuildPos(const FVector& buildPos, const int32& npcID);

	/**
	*Define Method
	*BlueprintNativeEvent,占领基地结果
	*@param	result 结果 1：占领成功关闭界面，0：占领失败，重新显示探索
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OccupyBuildResult(const int32& result);

	/**
	*Define Method
	*BlueprintNativeEvent,通知打开建造洞府界面
	*@param	endStrTime 保护状态的结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void StartBuildCaveHouse(const int32& dongfuID, const FString& endStrTime);

	/**
	*Define Method
	*BlueprintNativeEvent,通知打开进入洞府界面
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnEnterCaveHouse(const int32& dongfuID);

	// 进入别人的洞府（挑战）
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnEnterOtherCaveHouse(const int32& dongfuID);
	// 点击进入别人的洞府
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnClieckEnterOtherCaveHouse(const int32& dongfuID);
	/**
	*Define Method
	*,通知打开灵泉界面
	*@param	_ActiveChartID 在激活状态的阵图ID
	*@param	LHMJ_CoverHP  防护罩HP
	*@param	_TotalLingNeng 可获得的总灵能
	*@param	_LQCurrHP  灵泉HP
	*@param	DestroyBuild 被破坏的建筑
	*@param	NPCID 对话NPCID
	*@return 无
	*/
	void OpenLingQuanUI(const int32& _ActiveChartID, const int32& LHMJ_CoverHP, const int32& _TotalLingNeng, const int32& _LQCurrHP, const FVariant& DestroyBuild, const int32& NPCID);

	/* 洞府守卫复活时间（灵泉是否被破坏，见上方方法DestroyBuild）
	* 如果灵泉被破坏了，则界面显示倒计时的值为ReviveTime，且不开始倒计时；
	* 如果灵泉是好的，则界面倒计时的值为下方，开始倒计时；
	* UGolbalBPFunctionLibrary::FromServerTimeToClientTime(ReviveTime) - FDateTime::Now()
	*/
	void OnGuardReviveTime(const int32& ReviveTime);

	/**
	*Define Method
	*BlueprintNativeEvent,开始升级某建筑
	*@param	buildType 建筑类型
	*@param	endStrTime  升级需要的时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void StartBuildUpgrade(const int32& buildType, const FString& endStrTime);

	/**
	*洞府 点击探索按钮
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCliskExplore();

	/**
	*洞府 点击占领按钮
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCliskOccupyBuild();

	/**
	*洞府 点击建造洞府按钮
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCliskBuildCaveHouse(const int32& dongfuID);

	/**
	*洞府 点击进入洞府按钮
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onCliskEnterCaveHouse(const int32& dongfuID);

	/**
	*洞府 点击领取灵能
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onReceiveLingNeng();

	/**
	*洞府 请求升级某建筑
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onUpgradeBuild(const int32& buildType, const int32& buildLevel);

	/**
	*洞府 升级某建筑成功回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onUpgradeBuildSuccess(const int32& buildType);

	/**
	*获取建筑的消耗数据
	*/
	UFUNCTION(BlueprintCallable)
		void GetBuildDepleteData(LHMJ_BUILD_TYPE buildType, const int32& buildLevel, TArray<int32> &itemList, TArray<int32> &amountList, int32 &depleteMoney, int32 &depletePsionic, int32 &depleteTime);

	/**
	*获取灵泉产出数据
	*/
	UFUNCTION(BlueprintCallable)
		void GetLingQuanProduceData(const int32& lingQuanLevel, int32 &timeKey, int32 &outLingNengAmount, int32 &lingNengMaxAmount, int32 &lingQuanMaxHP);
	

	// 开启阵图(阵图ID)
	UFUNCTION(BlueprintCallable)
		void OpenBattleFormations(const int32& ItemID);
	/**
	*BlueprintNativeEvent,开启阵图回调(PS：界面显示的数据 不能去背包获取，因为已经删除了！)
	*@param	_ActiveChartID 在激活状态的阵图ID
	*@param	LHMJ_CoverHP  防护罩HP
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void CLIENT_OnActiveBatteleFormations(const int32& _ActiveChartID, const int32& LHMJ_CoverHP);

	// 关闭阵图
	UFUNCTION(BlueprintCallable)
		void CloseBattleFormations();
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void CLIENT_OnCloseBatteleFormations();

	UFUNCTION(BlueprintCallable)
		void OnLHMJWInClose();

	// 对洞府发起挑战ShowChallenge
	UFUNCTION(BlueprintCallable)
		void RequestLHMJChallenge(const int32& lineNumber, const int32& group);
	// 发起挑战回调
	UFUNCTION(BlueprintCallable)
		void OnRequestLHMJChallenge(const int32& lineNumber, const FString& PlayerName);

	/**
	*BlueprintCallable,被挑战者显示 挑战者的挑战信息
	*@param	PlayerName 挑战者的姓名
	*@param	CanRefuseTime  可以拒绝的次数（次数为0，则拒绝按钮置灰）
	*@return 无
	*/
	UFUNCTION(BlueprintCallable)
		void ShowChallenge(const FString& PlayerName, const int32& CanRefuseTime);
	// 回应挑战结果
	UFUNCTION(BlueprintCallable)
		void ReplayLHMJChallenge(const int32& replay);

	// 挑战者显示 挑战回应
	UFUNCTION(BlueprintCallable)
		void onRequestLHMJChallengeReply(const int32& Replay, const FString& PlayerName, const int32& IsPlunder);

	// 显示被挑战者的洞府信息
	void ShowChallengeMsg(const FVariant& DFVar, const int32& lineNumber, const FVector& Position);
	// 自动寻路到 被挑战的洞府
	UFUNCTION(BlueprintCallable)
		void AutoGotoChallengeSpace();

	// 玩家的洞府信息
	void InitDongFuData(const FVariant& DFVar, const int32& lineNumber, const FVector& Position);
	// 自动寻路到 自己的洞府
	UFUNCTION(BlueprintCallable)
		void AutoGotoDFSpace();

	/**
	*B 洞府活动结果
	*@param	IsChallengeActive （0：掠夺战，1：争夺战）
	*@param	Result  活动结果（0：攻方失败，1：攻方胜利，2：守方失败，3：守方胜利，4：第一阶段守方胜利，5：第一阶段攻方失败）
	*@param	RwItemStr 奖励物品  格式：物品ID:数量|物品ID:数量|物品ID:数量 (比如：101040128:1|101040129:2|101040130:3|)
	*@param	RwMoney  奖励金钱
	*@param	RwPsychic 奖励灵能
	*@param	DestroyBuilds 被破坏的建筑
	*@param	CombatTime 活动时间
	*@param	DeadCount 死亡次数
	*@return 无
	*/
	void OnShowDFActtiveResult(const int8 IsChallengeActive, const int8 Result, const FString& RwItemStr, const int32& RwMoney, const int32& RwPsychic, const TArray<FVariant>& DestroyBuilds_, const int32& CombatTime, const int32& DeadCount);
	
	// 活洞府活动开启
	//*@param	IsPlunderActive （1：掠夺战，0：争夺战）
	void onDFActiveStart(const uint8 IsPlunderActive, const FString& PlayerName);
	// 活动结束
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void onDFActiveEnd();

	// 挑战方的保护罩出现
	void NoticeMECEnter(const int32& EntityID_);
	// 显示怪物的血量信息
	void initDFMonsterInfo(const TArray<FVariant>& EntityIDList);
	void addDFMonsterInfo(const int32& EntityID_);

	// 占领洞府
	UFUNCTION(BlueprintCallable)
		void OnOccupyPlayerDF(const int32& IsOccupy);
	// 占领洞府回调
	void OnOccupyPlayerDFCB(const uint16 MsgID, const FString& PlayerName);
	// 洞府被占领了
	void OnDFBeingOccupy();


	//接口废弃   打开修复建筑界面。itemVar 为修复建筑需要消耗的物品格式{itemID：amount，...}
	void OpenRepairBuildUI(const int32& buildType, const FVariant& itemVar);
	// 通知服务器开始修复建筑
	UFUNCTION(BlueprintCallable)
		void repairDFBuild(const int32& buildType);
	// 修复的建筑回调
	UFUNCTION(BlueprintCallable)
		void OnBeginRepairDFBuild(const int32& buildType, const int32& fixedTime);
	// 建筑修复完成
	void OnRepairDFBuildFinish(const int32& buildType);
	// 获取损坏的建筑
	UFUNCTION(BlueprintCallable)
		void GetDestroyBuilds(TArray<int32>& BuildArr);
	// 建筑是否损坏
	UFUNCTION(BlueprintCallable)
		bool IsDestroyBuild(LHMJ_BUILD_TYPE buildType);
	// 获取修复建筑需要的材料
	UFUNCTION(BlueprintCallable)
		void GetFixBuildCost(const int32& buildType, TMap<int32, int32>& ItemMap);

	// 显示守卫升级提示
	void ShowUpgradeGuardMsg(const int32& MegID, const int32& LingNeng, const int32& MonsterID, int8 mType);
	// 确定守卫升级提示
	void UpgradeDFGurard(const int32& MonsterID, int8 mType);

public:
	virtual void InitBlueCB() override;

	// 添加 计时器，增加灵能
	void BeginAddPsionicTime();
	void AddPsionicPerTime();
	void ClearPsionicTime();

private:
	//升级建筑倒计时
	void UpdateRemainUpLevelTime();

	//修复建筑倒计时
	void UpdateRemainRepairTime();

	// 初始化洞府数据
	void _initDongFuDatas(const int32& LineNumber, const FVariant& DFVariant, TArray<FDongFuData>& Datas);
	void _initDongFuData(const FVariant& DFVariant, FDongFuData & Data);
	void _getDongFuDataByPage(const int32& LineNumber, const int32& Page, TArray<FDongFuData>& DongFuArr);

	// 检查与挑战方的保护罩的距离，小于15米则提示msg
	void CheckDistWithMEC();

public:
	/// 占有的类型
	UPROPERTY(BlueprintReadOnly)
		LHMJ_SPACE_TYPE OccupySpaceType;
	/// 建筑等级
	UPROPERTY(BlueprintReadOnly)
		TMap<LHMJ_BUILD_TYPE, int32> Builds;
	/// 灵泉产出的全部灵能数
	UPROPERTY(BlueprintReadOnly)
		int32 caveHousePsionicSum;
	/// 灵泉当前血量
	UPROPERTY(BlueprintReadOnly)
		int32 lingQuanCurrHP;

	//当前正在升级（或建造）的建筑类型
	UPROPERTY(BlueprintReadOnly)
		LHMJ_BUILD_TYPE UpLevelBuildType;
	//当前正在升级（或建造）的建筑的结束时间
	UPROPERTY(BlueprintReadOnly)
		float RemainUpLevelTime;

	//当前正在修复的建筑类型
	UPROPERTY(BlueprintReadOnly)
		LHMJ_BUILD_TYPE RepairBuildType;
	//当前正在修复的建筑的结束时间
	UPROPERTY(BlueprintReadOnly)
		float RemainRepairTime;

	///当前激活的阵图ID（为0则当前没有激活的阵图）
	UPROPERTY(BlueprintReadOnly)
		int32 ActiveBattleFormationsID;
	///当前激活的阵图防护罩HP
	UPROPERTY(BlueprintReadOnly)
		int32 BattleFormationsHP;

	// 洞府的数据 格式如 {第几线 ： 洞府的数据}
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FDongFuData_Map> DongFuDataMaps;
	// 被挑战的洞府数据
	UPROPERTY(BlueprintReadOnly)
		FDongFuData ChallengeDFData;
	// 自己的洞府数据
	UPROPERTY(BlueprintReadOnly)
		FDongFuData DFData;
	/// 挑战的洞府 线路
	UPROPERTY(BlueprintReadOnly)
		int32 ChallengeLineNumber;
	/// 自己的洞府 线路
	UPROPERTY(BlueprintReadOnly)
		int32 DFLineNumber;
	// 挑战洞府的坐标
	UPROPERTY(BlueprintReadOnly)
		FVector ChallengeDFPos;				
	
private:
	// 被破坏的建筑 格式如：{buildType : { itemID : amount}}
	TMap<int32, TMap<int32, int32>> DestroyBuilds;

	FTimerHandle AddPsionicTimer;
	FTimerHandle UpLevelTimerHandle;
	FTimerHandle RepairTimerHandle;

	int32 RequestPage;					// 正在请求的当前页数，如果服务器数据还没返回就 不再去请求
	int32 RequestLineNumber;
	FVector DFPos;						// 自己洞府的坐标

	bool BActivityStart;				// 活动是否开启
	int32 MExtCoverID;					// 挑战方的保护罩entityID
	FTimerHandle CheckDistTimerHandle;
};