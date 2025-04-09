// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/SpaceHunTingData.h"
#include "GameData/SpaceYeZhanFengQiData.h"
#include "GameData/LingMaiData.h"
#include "GameData/FrozenFightData.h"
#include "GameData/FHLTMemberData.h"
#include "GameData/SpaceYXLMData.h"
#include "GameData/YXLMMatchData.h"
#include "GameData/SGMZMatchData.h"
#include "GameData/TongStarcraftData.h"
#include "GameData/BigmapActInfo.h"
#include "GameData/CampYCJMDData.h"
#include "GameData/BHZBData.h"
#include "GameData/TrainSoldierGroundAreaCfg.h"
#include "RoleActivityInterface.generated.h"

/*
* 文件名称：RoleActivityInterface.h
* 功能说明：玩家活动
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-07-24
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleActivityInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleActivityInterface();
	~URoleActivityInterface();
	static FString GetName() { return TEXT("RoleActivityInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleActivityInterface.BP_RoleActivityInterface_C'"); } //获取蓝图对象路径

#pragma region 晶石狩猎场
	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 更新金钱数据到客户端 (包括自己)
	*
	*@param playerID 玩家ID(玩家自己)
	*@param money 获得的收益金钱
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateMoneyDataToOtherPlayer(const int32& playerID, const int32& money, const FString& playerName, const int32& camp, const int32& profession, const int32& level);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 接收其他玩家的金钱数据 (包括自己)
	*
	*@param playerID 其他玩家ID(包括自己)
	*@param money 获得的收益金钱
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveOtherMoneyData(const int32& playerID, const int32& money, const FString& playerName, const int32& camp, const int32& profession, const int32& level);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 更新积分(金精)数据到客户端(包括自己)
	*
	*@param playerID 玩家ID
	*@param integral 获得的积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateIntegralDataToOtherClient(const int32& playerID, const int32& integral);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 接收其他玩家的积分(金精)数据 (包括自己)
	*
	*@param playerID 玩家ID
	*@param integral 获得的积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveOtherIntegralData(const int32& playerID, const int32& integral);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 更新其他玩家被击杀的数据到客户端( 包括自己 )
	*
	*@param playerID 玩家ID
	*@param beKill 玩家被击杀次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateBeKillDataToOtherClient(const int32& playerID, const int32& beKill);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 接收其他玩家的被击杀的次数 (包括自己)
	*
	*@param playerID 玩家ID
	*@param beKill 玩家被击杀次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveOtherBeKillData(const int32& playerID, const int32& beKill);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 更新其他玩家击杀的数据到客户端( 包括自己 )
	*
	*@param playerID 玩家ID
	*@param Kill 玩家击杀其他玩家的次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateKillDataToOtherClient(const int32& playerID, const int32& Kill);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 接收其他玩家的击杀的次数 (包括自己)
	*
	*@param playerID 玩家ID
	*@param Kill 玩家击杀其他玩家的次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveOtherKillData(const int32& playerID, const int32& Kill);

	/**
	*
	*BlueprintCallable，晶石狩猎场 增加金钱数据
	*
	*@param playerID 玩家ID
	*@param integral 获得的金钱
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void AddMoneyData(const int32& playerID, const int32& money, const FString playerName, const int32& camp, const int32& profession, const int32& level);

	/**
	*
	*BlueprintCallable，晶石狩猎场 增加积分数据
	*
	*@param playerID 玩家ID
	*@param integral 获得的积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void AddIntegralData(const int32& playerID, const int32& integral);

	/**
	*
	*BlueprintImplementableEvent，晶石狩猎场 增加金钱数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnAddMoneyData(const int32& playerID);

	/**
	*
	*BlueprintImplementableEvent，晶石狩猎场 增加积分数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnAddIntegralData(const int32& playerID);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 设置积分上限
	*
	*@param integral 获得的积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_SetIntegralMax(const int32& integral);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 移除金钱数据
	*
	*@param playerID 玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_HunTingMemberLeave(const int32& playerID);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 显示金钱排名
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowRankList();

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 显示超神界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnGodLike(const FString&  KillerName);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 显示首杀界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnFirstKill(const FString&  KillerName);

	/**
	*Define method
	*BlueprintNativeEvent，晶石狩猎场 清空数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnClearData();

	/**
	*
	*BlueprintCallable，晶石狩猎场 获得排名
	*
	*@param playerID 玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		int32 GetPlayerRank(const int32& playerID);

#pragma endregion
#pragma region 血斗凤栖镇 (个人竞技副本 第二场)
	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇
	*
	*@param:playerID  离开副本的玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_FengQiMemberLeave(const int32& playerID);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 更新自己数据到其他客户端
	*
	*@param:playerID  自己ID
	*@param:integral  积分
	*@param:playerName名称
	*@param:KillNum	 击杀次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateFengQiMemberDataToOtherClient(const int32& playerID, const int32& integral, const FString& playerName, const int32& profession, const int32& killNum);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 接收其他人数据
	*
	*@param:playerID  别人ID
	*@param:integral  积分
	*@param:playerName名称
	*@param:KillNum	 击杀次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveFengQiOtherMemberData(const int32& playerID, const int32& integral, const FString& playerName, const int32& profession, const int32& killNum);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 更新积分数据到客户端(包括自己)
	*
	*@param:playerID  别人ID
	*@param:integral  积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateFengQiIntegralToOtherClient(const int32& playerID, const int32& integral);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 更新其他玩家击杀的数据到客户端( 包括自己 )
	*
	*@param:playerID  别人ID
	*@param:killNum  击杀次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateFengQiKillDataToOtherClient(const int32& playerID, const int32& killNum);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示排名
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowFengQiRank();

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示起始安全范围
	*
	*@param:upLeftOriginPos  左上起点位置
	*@param:upRightOriginPos  右上起点位置
	*@param:downLeftOriginPos  左下起点位置
	*@param:downRightOriginPos  右下起点位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowOriginArea(const FVector& upLeftOriginPos, const FVector& upRightOriginPos, const FVector& downLeftOriginPos, const FVector& downRightOriginPos);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示缩小的安全范围
	*
	*@param:upLeftEndPos  左上终点位置
	*@param:upRightEndPos  右上终点位置
	*@param:downLeftEndPos  左下终点位置
	*@param:downRightEndPos  右下终点位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowEndArea(const FVector& upLeftEndPos, const FVector& upRightEndPos, const FVector& downLeftEndPos, const FVector& downRightEndPos);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 开始缩小安全范围
	*
	*@param:totalUseTime  总缩小范围的时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_StartReduceArea(float totalUseTime);

	/**
	*Define method
	*BlueprintNativeEvent，玩家重登 更新到其他人数据 (除了自己)
	*
	*@param srcMemberID 原玩家ID
	*@param dstMemberID 现在玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateFengQiMemberDataToOtherOnLogin(const int32& srcMemberID, const int32& dstMemberID);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示第一名界面
	*
	*@param:firstName  第一名名称
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowFirstWindow(const FString& firstName);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 更新显示成员人数
	*
	*@param:memberNum  人数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYeZhanFengQiMemberNumber(const int32& memberNum);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 更新击杀数
	*
	*@param:killNum  击杀数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYeZhanFengQiMyKillNumber(const int32& killNum);
	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示起始圆
	*
	*@param:originCenterPos  圆心
	*@param:originRadius  半径
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ClIENT_ShowYeZhanFengQiOriginArea(const FVector& originCenterPos, const float& originRadius);
	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示终点圆
	*
	*@param:endCenterPos  圆心
	*@param:endRadius  半径
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ClIENT_ShowYeZhanFengQiEndArea(const FVector& endCenterPos, const float& endRadius);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 缩小安全区域
	*
	*@param:totalUseTime  总时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ClIENT_StartReduceYeZhanFengQiArea(const float& totalUseTime);

	/**
	*Define Method
	*BlueprintNativeEvent,血斗凤栖镇 显示排名
	*
	*@param:rank  排名
	*@param:killNum 击杀数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowYeZhanFengQiMemberRank(const int32& rank, const int32& killNum);

	/**
	*
	*BlueprintCallable,离开血斗凤栖镇
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CELL_LeaveYeZhanFengQi();
	/**
	*Define method
	*BlueprintNativeEvent，显示进入凤栖镇面板
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ShowEnterYeZhanFengQiWindow();

	/**
	*
	*BlueprintCallable,进入血斗凤栖镇
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void EnterYeZhanFengQi();

#pragma endregion
#pragma region 灵脉战场
	/**
	*Define method
	*BlueprintNativeEvent，灵脉战场，开始匹配
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEnterLingMaiMatchQueue();

	/**
	*Define method
	*BlueprintNativeEvent，开始匹配对手
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEnterLingMaiReadyQueue();

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEnterLingMaiTelPortQueue(const int32& Key);

	/**
	*Define method
	*BlueprintNativeEvent，灵脉战场活动结束（关闭匹配界面）
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnLingMaiActivityEnd();

	/**
	*Define method
	*BlueprintNativeEvent，添加战场数据
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_AddLingMaiMember(const int32& PlayerID, const FString& Name, const int32& camp);

	/**
	*Define method
	*BlueprintNativeEvent，离开战场
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnLeaveLingMai();

	/**
	*Define method
	*BlueprintNativeEvent，显示战场时间，并倒计时（界面参考ShowSpaceLife）
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowLingMaiLife(const FString& Time);

	/**
	*Define method
	*BlueprintNativeEvent，击杀
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnKillLingMai(const int32& DiePlayerID, const int32& KillerID);

	/**
	*Define method
	*BlueprintNativeEvent，助攻
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnAssistsLingMai(const TArray<int32>& PlayerIDList);

	/**
	*Define method
	*BlueprintNativeEvent，某个阵营占领灵塔塔基
	*
	*@param ScriptID
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OccupyPagodaBase(const int32& PlayerID);

	/**
	*Define method
	*BlueprintNativeEvent，某个阵营占领灵塔
	*
	*@param ScriptID 灵塔ScriptID (40000140:极阳灵塔，40000137：极阴灵塔)
	*@param Camp 占领灵塔的阵营(1:仙道，2：魔道)
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OccupyPagoda(const FString& ScriptID, const int32& Camp);

	/**
	*Define method
	*BlueprintNativeEvent，某个阵营占领灵脉
	*
	*@param ScriptID 灵脉scriptID(20006563:北灵脉，20006564：中灵脉，20006565：南灵脉)
	*@param Camp 占领灵脉的阵营(1:仙道，2：魔道)
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OccupyLingMai(const FString& ScriptID, const int32& Camp, const int32& TaosimPoint, const int32& DemonPoint, const TArray<int32>& AssistAttack);

	/**
	*Define method
	*BlueprintNativeEvent，拉葫芦离开阵营
	*
	*@param TaosimPoint  仙道灵能点
	*@param DemonPoint	魔道灵能点
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnGrabGourdLeave(const int32& PlayerID, const int32& TaosimPoint, const int32& DemonPoint);

	/**
	*Define method
	*BlueprintNativeEvent，灵能点数量改变
	*
	*@param TaosimPoint  仙道灵能点
	*@param DemonPoint	魔道灵能点
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnPowerPointChange(const int32& TaosimPoint, const int32& DemonPoint);

	/**
	*Define method
	*BlueprintNativeEvent，获胜（弹出结算界面）
	*
	*@param Camp  获胜阵营
	*@param LeftTime	比赛用时（秒）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnWinGameLingMai(const int32& Camp, const int32& LeftTime, const int32& TaosimPoint, const int32& DemonPoint);

	/**
	*Define method
	*BlueprintNativeEvent，终结超神(参考OnFirstKill)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEndLegendary(const FString& Name);

	// 请求服务器大地图的同一阵营的动态数据
	UFUNCTION(BlueprintCallable)
		void RequestSameCampPos();
	// 显示大地图的同一阵营的动态信息

		void CLIENT_OnRequestSameCampPos(const FVariant& BigmapActInfo);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnRequestSameCampPos_BP(const TArray<FBigmapActInfo>& BigmapActInfo);

	UFUNCTION(BlueprintCallable)
		TArray<FString> GetOccupyLingMaisByCamp(int32 Camp);
	
	UFUNCTION(BlueprintCallable)
		bool IsLingMaiOccupyByCamp(int32 Camp, FString LingMaiScriptID);

#pragma endregion

#pragma region 决战十方城 (个人竞技副本 第一场)
	/**
	*Define method
	*BlueprintNativeEvent，显示通关数据
	*
	*@param passDataList 通关数据
	*@param joinNumber 参加人数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowShiFangChengPassList(const int32& joinNumber, const FString& passDataList);
	/**
	*Define method
	*BlueprintNativeEvent，显示进入十方城面板
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowEnterActBunchWindow();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void EnterActBunch();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void AbandonActBunch();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CELL_EnterShiFangCheng();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CELL_AbandonShiFangeCheng();

	/**
	*Define method
	*BlueprintNativeEvent，显示通关十方成第一名数据
	*
	*@param passName 通关人
	*@param passTime 通关时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void CLIENT_ShowFirstPassShiFangCheng(const FString& passName, const int32& passTime);

	/**
	*Define method
	*BlueprintNativeEvent，显示通关十方成的人数
	*
	*@param passNumber 通关人数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void CLIENT_ShowPassShiFangChengNumber( const int32& passNumber);

#pragma endregion

#pragma region 英雄王座 
	/**
	*Define method
	*BlueprintNativeEvent，更新自己成员数据到其他客户端
	*
	*@param roleID 玩家ID
	*@param roleName 玩家名字
	*@param roleCamp 玩家阵营
	*@param roleKill 玩家击杀数
	*@param roleBeKill 玩家被击杀数
	*@param roleItemList 玩家物品ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYXLMMemberDataToOtherClient(const int32& roleID, const FString& roleName, const int32& roleCamp, const int32& roleKill, const int32& roleBeKill, const TArray<int32>& roleItemIDList);

	/**
	*Define method
	*BlueprintNativeEvent，接收其他玩家的成员数据
	*
	*@param roleID 玩家ID
	*@param roleName 玩家名字
	*@param roleCamp 玩家阵营
	*@param roleKill 玩家击杀数
	*@param roleBeKill 玩家被击杀数
	*@param roleItemList 玩家物品ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveYXLMOtherMemberData(const int32& roleID, const FString& roleName, const int32& roleCamp, const int32& roleKill, const int32& roleBeKill, const TArray<int32>& roleItemIDList);

	/**
	*Define method
	*BlueprintNativeEvent，更新其他玩家击杀的数据到客户端( 包括自己 )
	*
	*@param roleID 玩家ID
	*@param roleKill 玩家击杀数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYXLMKillDataToOtherClient(const int32& roleID, const int32& roleKill);

	/**
	*Define method
	*BlueprintNativeEvent，更新其他玩家被击杀的数据到客户端( 包括自己 )
	*
	*@param roleID 玩家ID
	*@param roleBeKill 玩家击杀数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYXLMBeKillDataToOtherClient(const int32& roleID, const int32& roleBeKill);

	/**
	*Define method
	*BlueprintNativeEvent，更新其他玩家获得物品的数据到客户端( 包括自己 )
	*
	*@param roleID 玩家ID
	*@param itemID 物品ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYXLMAddItemToOtherClient(const int32& roleID, const int32& itemID);

	/**
	*Define method
	*BlueprintNativeEvent，更新其他玩家移除物品的数据到客户端( 包括自己 )
	*
	*@param roleID 玩家ID
	*@param itemID 物品ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYXLMRemoveItemToOtherClient(const int32& roleID, const int32& itemID);

	void AddYXLMMemberData(const int32& roleID, const FString& roleName, const int32& roleCamp, const int32& roleKill, const int32& roleBeKill, const TArray<int32>& roleItemIDList);


	/**
	*Define method
	*BlueprintNativeEvent，匹配成功 显示确定框
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_CampYXLMOnMatchSuccess();

	/**
	*Define method
	*BlueprintNativeEvent，隐藏确定框
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_CampYXLMHideAffirmWindow();

	/**
	*Define method
	*BlueprintNativeEvent，更新等待确认的列表
	*
	*@param idList 等待玩家确定的ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_CampYXLMUpdateWaitAffirmList(const TArray<int32>& idList);

	/**
	*Define method
	*BlueprintNativeEvent，玩家点确定按钮，显示数据
	*
	*@param idList 等待玩家确定的ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_CampYXLMShowAffirmData(const FString& affirmData);

	/**
	*Define method
	*BlueprintNativeEvent，玩家重登 更新到其他人数据 (除了自己)
	*
	*@param srcMemberID 原玩家ID
	*@param dstMemberID 现在玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateYXLMMemberDataToOtherOnLogin(const int32& srcMemberID, const int32& dstMemberID);

	/**
	*Define method
	*BlueprintNativeEvent，所有成员显示数据界面
	*
	*@param winCamp 赢的阵营
	*@param rewardExp 奖励经验
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowYXLMBattlefieldWin(const int32& winCamp,const int32& rewardExp);
	/**
	*Define method
	*BlueprintNativeEvent，报名成功后的回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_CampYXLMSignUpSuccess();

	/**
	*BlueprintCallable，点击确认框
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CampYXLMonAffirm(int32 result);

	/**
	*BlueprintCallable，取消报名
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CampYXLMCancelSignUp();

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功都确认后，显示倒计时进入副本时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowEnterYXLMTime(float enterTime);

	/**
	*BlueprintCallable，回城
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CELL_YXLMBackToCity();

	/**
	*Define method
	*BlueprintNativeEvent，显示英雄王座副本时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowYXLMSpaceLife(const FString& spaceLifeTime);

	/**
	*Define method
	*BlueprintNativeEvent，显示英雄王座快捷背包
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_showYXLMQuickBag();

	/**
	*Define method
	*BlueprintNativeEvent，隐藏英雄王座快捷背包
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_hideYXLMQuickBag();

	/**
	*Define method
	*BlueprintNativeEvent，显示随机出现小兵购买界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowYXLMRandomScriptIDs(const FString& jsonData);

	/**
	*BlueprintCallable，购买小兵
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CELL_YXLMBuyRandomScriptID(const FString& scriptID);

	/**
	*Define method
	*BlueprintNativeEvent，显示位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_showEnemyPos(const TArray<FVector>& enemyMemberPos);

	/**
	*Define method
	*BlueprintNativeEvent，隐藏位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_HideEnemyPos();

	void ClearYXLMMemberData();

#pragma endregion
#pragma region 帮会争霸 第一场
	/**
	*BlueprintCallable，报名第一场
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	void TongStarcraft_firstSignUp( TArray<FString> firstTeamNames, TArray<FString> secondTeamNames, TArray<FString> thirdTeamNames, TArray<FString> fourTeamNames);

	/**
	*Define method
	*BlueprintNativeEvent，显示第一场报名成功面板
	*
	*@param signData 报名成功数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void CLIENT_ShowTongSignSuccessWindow(const FString& signData);

	/**
	*Define method
	*BlueprintNativeEvent，显示通关第一场数据面板
	*
	*@param passData 通关数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowPassFirstTongStarcraft(const FString& passData);

	/**
	*Define method
	*BlueprintNativeEvent，显示帮会成员面板
	*
	*@param number 报名最大成员数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowTongMemberWindow(const int32& number);
#pragma endregion
#pragma region 帮会争霸 第二场
	/**
	*Define method
	*BlueprintNativeEvent，更新成员积分
	*
	*@param playerID 玩家ID
	*@param integral 积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateMemberIntegral(const int32& playerID, const int32& integral);

	/**
	*Define method
	*BlueprintNativeEvent，更新成员积分
	*
	*@param tongName 帮会名称
	*@param integral 帮会积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateTongIntegral(const FString& tongName, const int32& tongIntegral);

	/**
	*Define method
	*BlueprintNativeEvent，更新成员积分
	*
	*@param firstGroupNames 第一组帮会名称
	*@param secondGroupNames 第二组帮会名称
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OpenSecondTongStarcraftGroup(const TArray<FString>& firstGroupNames, const TArray<FString>& secondGroupNames);

	/**
	*BlueprintCallable，报名第二场
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void TongStarcraft_SecondSignUp(TArray<FString> signUpNames);

	/**
	*Define method
	*BlueprintNativeEvent，显示报名的帮会
	*
	*@param firstGroupNames 第一组帮会名称
	*@param secondGroupNames 第二组帮会名称
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void ShowTongStarcraftFirstSignUpTong(const TArray<FString>& firstGroupNames, const TArray<FString>& secondGroupNames);

	/**
	*BlueprintCallable，CST-7904 报名第一场
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	void firstTongStarcraftSignUp(TArray<FString> signUpPlayerNames);

	/**
	*Define method
	*BlueprintNativeEvent，玩家重登 修改玩家ID
	*
	*@param srcEntityID 原玩家ID
	*@param dstEntityID 现玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void UpdateTongStarcraftLoginMemToOtherClient(const int32& srcEntityID, const int32& dstEntityID);

#pragma endregion
#pragma region 帮会争霸 第三场
	/**
	*Define method
	*BlueprintNativeEvent，更新成员积分
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param integral 帮会积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftIntegral(const int32& tongSide, const int32& tongIntegral);

	/**
	*Define method
	*BlueprintNativeEvent，接收所有帮会积分
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param tongName 帮会名称
	*@param integral 帮会积分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void CLIENT_ReceiveAllThirdTongStarcraftIntegral(const int32& tongSide, const FString& tongName,const int32& tongIntegral);

	/**
	*Define method
	*BlueprintNativeEvent，接收所有被占领水晶的数据
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param boxScriptIDs 占领水晶ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveThirdTongStarcraftAllOccupySpellBox(const int32& tongSide, const TArray<FString>& boxScriptIDs);
	/**
	*Define method
	*BlueprintNativeEvent，增加某方的占领水晶的数据
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param boxScriptID 占领水晶
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_AddThirdTongStarcraftOccupySpellBox(const int32& tongSide, const FString& boxScriptID);
	/**
	*Define method
	*BlueprintNativeEvent，删除某方的占领水晶的数据
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param boxScriptID 占领水晶
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_RemoveThirdTongStarcraftOccupySpellBox(const int32& tongSide, const FString& boxScriptID);

	/**
	*BlueprintCallable，获得某一方占领水晶的数据
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*
	*@return TArray<FString>
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		TArray<FString> GetThirdTongStarcraftOccupySpellBoxByTongSide(int32 tongSide);

	/**
	*Define method
	*BlueprintNativeEvent，显示胜利界面
	*
	*@param isWin 是否胜利 0：失败 1：胜利
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowWinTong(const int32& isWin);

	/**
	*Define method
	*BlueprintNativeEvent，显示副本生命时间
	*
	*@param spaceLife 副本剩余时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowThirdTongStarcraftLife(const FString& spaceLife);

	/**
	*Define method
	*BlueprintNativeEvent，接受所有成员的数据
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*@param roleName 玩家名字
	*@param kill 玩家击杀数
	*@param beKill 玩家被击杀数
	*@param assists 玩家助攻数
	*@param occupy 玩家占领水晶数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ReceiveAllThirdTongStarcraftMemberData(const int32& tongSide, const int32& roleID, const FString& roleName, const int32& kill,const int32& beKill,const int32& assists,const int32& occupy);

	/**
	*Define method
	*BlueprintNativeEvent，更新自己数据到其他客户端
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*@param roleName 玩家名字
	*@param kill 玩家击杀数
	*@param beKill 玩家被击杀数
	*@param assists 玩家助攻数
	*@param occupy 玩家占领水晶数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftMemToOtherClient(const int32& tongSide, const int32& roleID, const FString& roleName, const int32& kill, const int32& beKill, const int32& assists, const int32& occupy);

	/**
	*Define method
	*BlueprintNativeEvent，重登修改玩家ID
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param srcRoleID 原玩家ID
	*@param dstRoleID 现玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftLoginMemToOtherClient(const int32& tongSide, const int32& srcRoleID, const int32& dstRoleID);

	/**
	*Define method
	*BlueprintNativeEvent，更新玩家的击杀数
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*@param kill 击杀数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftMemKill(const int32& tongSide, const int32& roleID, const int32& kill);

	/**
	*Define method
	*BlueprintNativeEvent，更新玩家的被击杀数
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*@param beKill 被击杀数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftMemBeKill(const int32& tongSide, const int32& roleID, const int32& beKill);

	/**
	*Define method
	*BlueprintNativeEvent，更新玩家的助攻数
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*@param assists 助攻数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftMemAssists(const int32& tongSide, const int32& roleID, const int32& assists);

	/**
	*Define method
	*BlueprintNativeEvent，更新玩家的占领水晶数
	*
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*@param occupy 占领水晶数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_UpdateThirdTongStarcraftMemOccupy(const int32& tongSide, const int32& roleID, const int32& occupy);

	void AddThirdTongStarcraftMember(const int32& tongSide, const int32& roleID, const FString& roleName, const int32& kill, const int32& beKill, const int32& assists, const int32& occupy);

	/**
	*BlueprintCallable，获得某一方成员数据
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*
	*@return FTHIRD_TONGSTARCRAFT_MEMBERDATA
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	FTHIRD_TONGSTARCRAFT_MEMBERDATA GetThirdTongStarcraftMemberData(int32 tongSide,int32 roleID);

	/**
	*BlueprintCallable，获得某一方成员数据
	*@param tongSide 帮会归属方 0：红方 1：蓝方
	*@param roleID 玩家ID
	*
	*@return FTHIRD_TONGSTARCRAFT_MEMBERDATA
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	TMap<int32, FTHIRD_TONGSTARCRAFT_MEMBERDATA> GetThirdTongStarcraftAllMemberData(int32 tongSide);

#pragma endregion
#pragma region 帮会阵营战
	/**
	*BlueprintCallable，帮会阵营战 该帮会的报名人员
	*
	*@param signUpMemberNames 报名成员
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void TongCampWarSignUp(const TArray<FString>& signUpMemberNames);

	/**
	*Define method
	*BlueprintNativeEvent，帮会阵营战 该帮会的报名人员
	*
	*@param signUpMemberNames 报名成员
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void OnQueryTongSignUpData(const TArray<FString>& signUpMemberNames, const int32& signUpMaxNumber);
#pragma endregion

	virtual void onLeaveWorld() override;
	virtual void InitBlueCB() override;
	virtual void OnLeaveScenes() override;
public:
	UPROPERTY(BlueprintReadOnly)
		int32 integralMax;  // 积分上限
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FSPACEHUNTING> moneyDatas;	//所有玩家的金钱数据 晶石狩猎场
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> integralDatas; //所有玩家的积分数据 晶石狩猎场

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FSPACEYEZHANFENGQI> YeZhanFengQiMemberDatas; //血斗凤栖镇成员数据

	UPROPERTY(BlueprintReadOnly)
		TArray<FVector> OriginPosList;//血斗凤栖镇 起始安全区域

	UPROPERTY(BlueprintReadOnly)
		TArray<FVector> EndPosList;//血斗凤栖镇 缩小的安全区域

	UPROPERTY(BlueprintReadOnly)
		TMap< int32, FLingMaiData > LingMaiActivityData; //灵脉战场数据

	UPROPERTY(BlueprintReadOnly)
		TMap <int32, FString> LingMaiOccupyPagodas; //灵脉战场被占的灵塔数据
	
	TMap<int32, TArray<FString>> LingMaiOccupyLingMais; //灵脉战场被占的灵脉数据

	UPROPERTY(BlueprintReadOnly)
		TMap< FString, FString > passDataMap; //十方城通关的数据

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FSPACEYXLMDATA> YXLMMemberDatas;//英雄王座成员数据

	UPROPERTY(BlueprintReadOnly)
		TMap<FString, int32> YXLMRandomScriptIDDatas;//英雄王座随机小兵购买数据

	UPROPERTY(BlueprintReadWrite)
		TArray<FYXLMMATCHDATA> YXLMXianTeamData;//英雄王座匹配仙道Team数据
	UPROPERTY(BlueprintReadWrite)
		TArray<FYXLMMATCHDATA> YXLMMoTeamData;//英雄王座匹配魔道Team数据
	UPROPERTY(BlueprintReadWrite)
		TArray<FFIRST_TONGSTARCRAFT_SIGNDATA> FirstTongStarcraftSignDatas; //第一场报名成功数据
	UPROPERTY(BlueprintReadWrite)
		TArray<FFIRST_TONGSTARCRAFT_PASSDATA> FirstTongStarcraftPassDatas; //第一场通关成功数据

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> MemberIntegralMap;//第二场成员积分
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, int32> TongIntegralMap;//第二场帮会积分

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> ThirdTongIntegralMap;//第三场帮会积分 帮会归属方:积分 0：红方 1：蓝方

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FString> ThirdTongNameMap;//第三场帮会积分 帮会归属方:帮会名称 0：红方 1：蓝方

	TMap<int32, TArray<FString>> ThirdTongOccupyBoxMap;//第三场帮会积分 帮会归属方:占领水晶ID列表 0：红方 1：蓝方

	TMap<int32, TMap<int32, FTHIRD_TONGSTARCRAFT_MEMBERDATA>> ThirdTongMemberDict; ///<帮会争霸第三场 成员数据

	UPROPERTY(BlueprintReadOnly)
		TMap< int32, FFrozenFightData > FrozenFightActivityData; //冰雪之战数据

	UPROPERTY(BlueprintReadWrite)
		TArray<FSGMZMATCHDATA> SGMZXianTeamData;//上古密阵仙道Team数据
	UPROPERTY(BlueprintReadWrite)
		TArray<FSGMZMATCHDATA> SGMZMoTeamData;//上古密阵魔道Team数据

	UPROPERTY(BlueprintReadOnly)
		int32 TongCampWarSignUpMaxNumber; ///<帮会阵营战报名最大人数

	UPROPERTY(BlueprintReadOnly)
		TMap< int32, FFHLTMemberData > FHLTActivityData; //烽火连天战场数据

	UPROPERTY(BlueprintReadOnly)
		TMap< int32, FCampYCJMDData > CampYCJMDActivityData; //阵营战场“勇闯绝命岛”数据

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> BHZBTeamProtectDict; /// 帮会争霸队伍防守数据 <据点Index,队伍ID>
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> BHZBTeamAttackDict; /// 帮会争霸队伍进攻数据 <据点Index,队伍ID>
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FBHZBPOINTDATA> BHZBPointDict; /// 帮会争霸据点数据 <据点Index,BHZBPOINTDATA>
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FBHZBMAPHOMEBARRACKSDATA> BHZBHomeBarrackMapDict; /// 帮会争霸大本营大地图数据 <大本营编号,FBHZBMAPHOMEBARRACKSDATA>
	UPROPERTY(BluePrintReadOnly)
		TArray<FBHZBMEMBERPOSDATA> BHZBMemberPosDatas; ///<帮会争霸成员坐标信息

	UPROPERTY(BluePrintReadOnly)
		TMap<int32, FBHZB_POINT_TABLE_DATA> BHZBPointCfgData; /// 帮会争霸据点配置数据 <据点编号，FBHZB_POINT_TABLE_DATA>
	
	UPROPERTY(BluePrintReadOnly)
		FBHZBTONGWARDETAIL BHZBTongWarDetailMgr; /// 帮会争霸战场详情数据

	UPROPERTY(BluePrintReadOnly)
		int32 RequestPointIndex = 0;	/// 被请求据点编号
	UPROPERTY(BluePrintReadOnly)
		bool bIsManualRequestOpen = false;  ///
	
	UPROPERTY(BlueprintReadOnly, Category = "RoleActivityInterface")
		POINTREQURY_TYPE PointRequryType = POINTREQURY_TYPE::POINTREQURY_TYPE_NONE;	//指挥大地图据点数据请求类型
	
	UPROPERTY(BluePrintReadOnly)
		int32 MyTeamGroupID = 0;	/// 玩家所在队伍ID

#pragma region 冰雪之战
	/**
	*Define method
	*BlueprintNativeEvent，冰雪之战，开始匹配
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEnterFrozenFightMatchQueue();

	/**
	*Define method
	*BlueprintNativeEvent，开始匹配对手
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEnterFrozenFightReadyQueue();

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnEnterFrozenFightTelPortQueue(const int32& Key);

	/**
	*Define method
	*BlueprintNativeEvent，冰雪之战活动结束（关闭匹配界面）
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnFrozenFightActivityEnd();

	/**
	*Define method
	*BlueprintNativeEvent，添加战场数据
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_AddFrozenFightMember(const int32& PlayerID, const FString& Name, const int32& camp);

	/**
	*Define method
	*BlueprintNativeEvent，离开战场
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnLeaveFrozenFight();

	/**
	*Define method
	*BlueprintNativeEvent，显示战场时间，并倒计时（界面参考ShowSpaceLife）
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowFrozenFightLife(const FString& Time);

	/**
	*Define method
	*BlueprintNativeEvent，击杀
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnKillFrozenFight(const int32& DiePlayerID, const int32& KillerID);

	/**
	*Define method
	*BlueprintNativeEvent，助攻
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnAssistsFrozenFight(const TArray<int32>& PlayerIDList);


	/**
	*Define method
	*BlueprintNativeEvent，某个阵营占领哨塔
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnFrozenFightOccupyTower(const FString& ScriptID, const int32& PlayerCamp, const int32& PlayerID);

	/**
	*Define method
	*BlueprintNativeEvent，某个阵营占领复活点
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnFrozenFightOccupyRivivePos(const FString& ScriptID, const int32& PlayerCamp, const int32& PlayerID);


	/**
	*Define method
	*BlueprintNativeEvent，资源点数量改变
	*
	*@param TaosimPoint  仙道资源点
	*@param DemonPoint	魔道资源点
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnFrozenFightPointChanged(const int32& TaosimPoint, const int32& DemonPoint);

	/**
	*Define method
	*BlueprintNativeEvent，更新面板玩家冰晶提交数据
	*
	*@param playerID  玩家ID
	*@param submits	数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnFrozenFightSubmit(const int32& playerID, const int32& submits);

	/**
	*Define method
	*BlueprintNativeEvent，获胜（弹出结算界面）
	*
	*@param Camp  获胜阵营
	*@param LeftTime	比赛用时（秒）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnWinGameFrozenFight(int32 WinnerCamp, int32 WinnerPoint, int32 LoserPoint, int32 Duration);


	/**
	*Define method
	*BlueprintCallable，取消匹配冰雪之战
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CancelMatchFrozenFight();

	/**
	*Define method
	*BlueprintCallable，进入冰雪之战
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void BeginEnterFrozenFight(int32 key);

	/**
	*Define method
	*BlueprintCallable，退出冰雪之战
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void Cell_leaveFrozenFight();


#pragma endregion
#pragma region 福袋玩法
	/**
	*Define Method
	*BlueprintNativeEvent,使用开启金枝玉庭物品
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
	void CLIENT_beginJZYT(const FString& RewardList, const FString& uid, const FString& SpaceStr);

	/**
	*选择使用金枝玉庭物品回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnUseJZYT(const FString& uid, const FString& SpaceStr);

	/**
	*Define Method
	*BlueprintNativeEvent,显示罗盘
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowGoldTreeCompass(const int32& Compass);

		/**
	*在大地图界面显示，目标区域
	*
	*@param  SpaceScriptID 地图脚本ID
	*@param  坐标中心点
	*@param  半径
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ShowAreaInBigMapUI(const FString& SpaceScriptID, const FVector& position, const float& Range);

	/**
	*增加圆形活动区域检测
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_AddActivityCircleArea(const FString& SpaceScriptID, const FVector& position, const float& Range, const int32& Index);

	/**
	*删除圆形活动区域检测
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_ClearActivityCircleArea();


	/**
	*进入圆形活动区域检测回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnEnterActivityCircleArea(const int32& index);

	/**
	*离开圆形活动区域检测回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnLeaveActivityCircleArea(const int32& index);
#pragma endregion

#pragma region 虚空探宝活动
	/**
	*Define Method
	*BlueprintNativeEvent,使用开启虚空探宝活动物品
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnNotifyStartXKTB(const FString& RewardList, const FString& uid, const FString& SpaceStr);

	/**
	*Define Method
	*BlueprintNativeEvent,通知归元盾充能值总数（比如：0.05 = 5%，传过来的是0.05）
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void NotifyRechargeableValue(const float& rechargeableValue);

	/**
	*选择使用虚空探宝活动物品回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onUseItemXKTB(const FString& uid, const FString& SpaceStr);
#pragma endregion

#pragma region 上古密阵
	/**
	*Define method
	*BlueprintNativeEvent，报名成功后的回调
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CampSGMZSignUpSuccess();

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功 显示确定框
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CampSGMZOnMatchSuccess();

	/**
	*Define method
	*BlueprintNativeEvent，隐藏确定框
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CampSGMZHideAffirmWindow();

	/**
	*Define method
	*BlueprintNativeEvent，玩家点确定按钮，显示数据
	*@param idList 等待玩家确定的ID列表
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CampSGMZShowAffirmData(const FString& affirmData);

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功都确认后，显示倒计时进入副本时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ShowEnterSGMZTime(float enterTime);

	/**
	*BlueprintCallable，取消报名
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CampSGMZCancelSignUp();

	/**
	*BlueprintCallable，点击确认框
	result 代表是否点击了确认
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CampSGMZOnAffirmp(const int32& result);
#pragma endregion

#pragma region 神秘福袋玩法 禁地采药
	/**
	*Define Method
	*BlueprintNativeEvent,使用开启天机盘物品
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_beginTJP(const FString& RewardList, const FString& uid, const FString& SpaceStr);

	/**
	*选择使用天机盘物品回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnUseTJP(const FString& uid, const FString& SpaceStr);
#pragma endregion

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_cancelMatchLingMai();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_beginEnterLingMai(const int32& INT32_1);

#pragma region 烽火连天
	/**
	*Define method
	*BlueprintNativeEvent，烽火连天，开是匹配
	*@param Number：人数
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnEnterFHLTMatchQueue(const int32& Number);

	/**
	*Define method
	*BlueprintNativeEvent，开始匹配对手
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnEnterFHLTReadyQueue();

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnEnterFHLTTelPortQueue(const int32& Key);

	/**
	*Define method
	*BlueprintNativeEvent，烽火连天活动结束（关闭匹配界面）
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnFHLTActivityEnd();

	/**
	*Define method
	*BlueprintNativeEvent，添加烽火连天战场数据
	*@param PlayerID 玩家的ID
	*@param Name 玩家名字
	*@param camp 玩家阵营
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnAddFHLTMember(const int32& PlayerID, const FString& Name, const int32& camp);

	/**
	*Define method
	*BlueprintNativeEvent，离开烽火连天战场
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnLeaveFHLT();

	/**
	*Define method
	*BlueprintNativeEvent，击杀
	*@param DiePlayerID 死亡玩家ID
	*@param KillerID  击杀者ID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnKillFHLT(const int32& DiePlayerID, const int32& KillerID);

	/**
	*Define method
	*BlueprintNativeEvent，助攻
	*@param PlayerIDList  玩家ID列表
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnAssistsFHLT(const TArray<int32>& PlayerIDList);

	/**
	*Define method
	*BlueprintNativeEvent，积分改变
	*@param TaosimIntegral  仙道积分
	*@param DemonIntegral	魔道积分
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnIntegralChange(const int32& taosimIntegral, const int32& demonIntegral);

	/**
	*Define method
	*BlueprintNativeEvent，获胜（弹出结算界面）
	*@param Camp  获胜阵营
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnWinGameFHLT(const int32& Camp, const int32& taosimIntegral, const int32& demonIntegral);

	/**
	*Define method
	*BlueprintNativeEvent，显示战场时间，并倒计时（界面参考ShowSpaceLife）
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ShowFHLTLife(const FString& Time);

	/**
	*Define method
	*BlueprintCallable，取消匹配烽火连天
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_cancelMatchFHLT();

	/**
	*Define method
	*BlueprintCallable，立即进入烽火连天战场
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_beginEnterFHLT(const int32& INT32_1);

	/**
	*Define method
	*BlueprintCallable，退出烽火连天副本
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onLeaveActivityFHLTCopy();
#pragma endregion

#pragma region 锦绣莲池
	/**
	*Define Method
	*BlueprintNativeEvent,使用五色鱼叉物品
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_beginJXLC(const FString& RewardList, const FString& uid, const FString& SpaceStr);

	/**
	*选择使用五色鱼叉物品回调
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnUseWSYC(const FString& uid, const FString& SpaceStr);

#pragma endregion

#pragma region 阵营战场-勇闯绝命岛

	/**
	*Define method
	*BlueprintNativeEvent，添加战场数据
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_AddCampYCJMDMember(const int32& PlayerID, const FString& Name, const int32& camp);

	/**
	*Define method
	*BlueprintNativeEvent，离开战场
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnLeaveCampYCJMD();


	/**
	*Define method
	*BlueprintNativeEvent，击杀
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnKillCampYCJMD(const int32& DiePlayerID, const int32& KillerID);

	/**
	*Define method
	*BlueprintNativeEvent，助攻
	*
	*@param
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void CLIENT_OnAssistsCampYCJMD(const TArray<int32>& PlayerIDList);

#pragma endregion

#pragma region 阵营战场随机匹配

	/**
	*Define method
	*BlueprintNativeEvent，开始随机匹配
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnCampRandomFitStart();

	/**
	*Define method
	*BlueprintNativeEvent，随机匹配成功
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnCampRandomFitSuccess();

	/**
	*Define method
	*BlueprintNativeEvent，中断随机匹配回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void OnCampRandomFitInterrupt();

	/**
	*Define method
	*BlueprintNativeEvent，匹配成功都确认后，显示倒计时进入副本时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ShowEnterRandomFitTime(float enterTime);

	/**
	*Define method
	*BlueprintNativeEvent，显示玩家剩余活动次数
	*@param ActivityTypeList	活动类型列表
	*@param MaxDegreeList		活动最大次数列表
	*@param DegreeList			活动参加次数列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleActivityInterface")
		void ShowPublicActRecordUI(const TArray<int32>& ActivityTypeList, const TArray<int32>& MaxDegreeList, const TArray<int32>& DegreeList);

	/**
	*中断随机匹
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CampRandomFitInterrupt();
#pragma endregion

#pragma region CST-9910 帮会争霸
	/**
	* 宣战据点
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void DeclareBHZBPoint(const int32& pointIndex,const int32& groupID);

	/**
	* 取消宣战
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CancelDeclareBHZBPoint(const int32& pointIndex);

	/**
	* 参与据点争夺战斗
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void JoinBHZBPointFight(const int32& pointIndex, const int32& groupID);

	/**
	* 撤销回防
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void cancelJoinBHZBPointFight(const int32& pointIndex);

	/**
	* 帮会争霸积分排名
	*/
	void OpenBHZBIntegralRank(const FVariant& Var);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnOpenBHZBIntegralRank(const TArray<FBHZBTONGINTEGRALDATA>& integralRankDatas);

	/**
	* 帮会争霸报名帮会排名
	*/
	void OpenSignUpBHZBRankWin(const FVariant& Var);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnOpenSignUpBHZBRankWin(const TArray<FBHZBTONGSIGNUPRANKDATA>& SignupRankDatas);

	/**
	* 召唤某一队去防守
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	void CallTeamToProtect(const int32& groupTeamID,const int32& pointIndex,const FString& pointName);

	/**
	* 召唤某一队去进攻
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	void CallTeamToAttack(const int32& groupTeamID, const int32& pointIndex, const FString& pointName);

	/**
	* 更新防守方的数据
	*/
	void UpdataToTongMemberClientProtectData(int32 groupTeamID, int32 pointIndex);

	/**
	* 更新进攻方的数据
	*/
	void UpdataToTongMemberClientAttackData(int32 groupTeamID,int32 pointIndex);
	/**
	* 打开据点详情面板
	*/
	void OpenNPCExtPointDetails(const FString& name, uint8 pointType, uint8 npcState, const FVariant& warNameList, const FVariant& warMemberNumList, int32 maxJoinNum, const FString& endTime,const FVariant& warTongDBIDList, const FVariant& joinAttackMems,const FVariant& joinProtectMems);

	/**
	* 请求打开据点大地图
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void RequestOpenBHZBNpcPointMap(const bool IsManualRequestOpen);

	void InitBHZBNPCPointDatas(const FVariant& Var);

	void UpdataNPCPointRestEndTime(int32 pointIndex, const FString& restEndTime);

	void UpdataNPCPointReadyEndTime(int32 pointIndex, const FString& readyEndTime);

	void UpdataNPCPointDeclareWarState(int32 pointIndex, uint8 declareWarState);

	void UpdateNPCPointAttackGroupTeamID(int32 pointIndex, int32 attackGroupTeamID, uint64 declareTongDBID);

	void UpdataBHZBPointJoinProtectTeamID(int32 pointIndex, int32 joinProtectTeamID);

	void UpdataNPCPointOccupyData(int32 pointIndex, uint64 occupyTongDBID,uint64 playerDBID,const FString& playerName, const FString& tongName);

	/**
	* 判断据点是否被我方占领
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		bool IsOccupyBHZBPoint(const int32& pointIndex);

	/**
	* 判断据点是否中立
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		bool IsBHZBPointNeutrally(const int32& pointIndex);

	void UpdataHomeBarracksMapDataToAllMember(const FVariant& Var);

	/**
	* 是否为我方大本营
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		bool IsMyBHZBHomeBarrack(const int32& index);

	/**
	* 请求传送到沙盘某个据点
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void RequestGotoStandMapPoint(const FVector& position);

	/**
	* 请求传送到大本营
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void RequestGotoBHZBHomeBarrack(const FString& tongDBID);

	void UpdataMemberPositionToClient(const FVariant& Var);
	
	/**
	* 加载帮会争霸据点配置数据
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	void LoadBHZBPointCfgData(bool bIsClickMKeyOpen);
	/**
	* 加载帮会争霸据点配置数据结束
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void LoadBHZBPointCfgDataOver();

	/**
	* 获得帮会争霸某个据点配置数据
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		FBHZB_POINT_TABLE_DATA GetBHZBPointCfgData( const int32& Index );

	void UpdataMyGroupIDToClient(int32 groupID);

	/**
	* 请求帮会争霸某个据点详情
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
	void RequestPointDetails(const int32& pointIndex, const POINTREQURY_TYPE RequryOperteType);

	/**
	* 布防帮会争霸某个据点
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void DefenseBHZBPoint(const int32& pointIndex,const int32& groupID);

	/**
	* 显示退出布防按钮
	*/
	void ShowExitPointSaveSpaceBtn();

	/**
	* 隐藏退出布防按钮
	*/
	void HideExitPointSaveSpaceBtn();

	/**
	* 据点详情蓝图回调
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnOpenNPCExtPointDetails(const FString& name, const int32& pointType, const int32& npcState, const TArray<FString>& warNames, const TArray<int32>& warMemberNums, const int32& maxJoinNum, const FString& endTime, const TArray<FString>& warTongDBIDs, const TArray<FString>& joinAttackMemList, const TArray<FString>& joinProtectMemList);
	/**
    * 弹出据点右键菜单
    */
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnPopRightMouseMenu(const int32& npcState, const TArray<FString>& warNames, const FString& endTime, const TArray<FString>& warTongDBIDs, const TArray<FString>& joinAttackMemList, const TArray<FString>& joinProtectMemList);
	/**
	* 弹出据点右键菜单
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleActivityInterface")
		void OnRequryWarTongDBIDsCB(const TArray<FString>& warTongDBIDs);
	/**
	* 更新据点攻占成员
	*/
	void UpdataBHZBPointJoinAttackMembers(int32 pointIndex, const FVariant& var);
	/**
	* 更新据点防守成员
	*/
	void UpdataBHZBPointJoinProtectMembers(int32 pointIndex, const FVariant& var);
	/**
	* 显示据点进攻标记
	*/
	void ShowGroupIDAttackPointSign(int32 pointIndex, int32 groupID);
	/**
	* 隐藏据点进攻标记
	*/
	void HideGroupIDAttackPointSign(int32 pointIndex);

	/**
	* 请求打开帮会争霸积分排行
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void RequestOpenBHZBIntegralRank();

	/**
	* 显示帮会争霸积分排行
	*/
	void ShowBHZBIntegralRankWin(const FVariant& Var,int32 delayCloseTime);

	TArray<FBHZBTONGINTEGRALDATA> GetBHZBRankDatasByFVariant(const FVariant& Var);

	/**
	* 初始化帮会争霸详情数据
	*/
	void InitBHZBWarDetailData(const FVariant& Var);

	/**
	* 更新帮会争霸详情积分和排名数据
	*/
	void UpdateBHZBWarDetailIntegralData(int32 integral, int32 rank);
	/**
	* 更新帮会争霸详情占领的据点数据
	*/
	void UpdateBHZBWarDetailOccupyNumber(int32 occupyPointAmount);
	/**
	* 更新帮会争霸详情队伍数据
	*/
	void UpdateBHZBWarDetailTeamData(int32 teamNumber, int32 pointIndex, int32 pointState, const FString& pointName);
	/**
	* 移除帮会争霸详情队伍数据
	*/
	void RemoveBHZBWarDetailTeamData(int32 teamNumber);
	/**
	* 更新帮会争霸详情据点占领数据
	*/
	void UpdateBHZBWarDetailOccupyPointData(int32 pointIndex, int32 pointState, const FString& pointName);
	/**
	* 移除帮会争霸详情占领据点
	*/
	void RemoveBHZBWarrDetailOccupyPoint(int32 pointIndex);
	/**
	* 增加帮会争霸详情提示消息数据
	*/
	void AddBHZBWarMsgData(int32 statusID, const FString& statusArgs);

	void QueryAllBHZBIntegralData(const FVariant& Var, int32 npcID);

#pragma endregion
#pragma region CST-12515 攻城战
	/**
	* 打开参加攻城战面板
	* numGCZsVar 攻城战场次
	* gczStartTimesVar 攻城战开始时间
	* gczRemainJoinNumsVar 攻城战剩余参加人数
	* npcID NPCID
	*/
	void OpenJoinGCZWin(const FVariant& numGCZsVar, const FVariant& gczStartTimesVar,const FVariant& gczRemainJoinNumsVar, int32 npcID);

	/**
	* 报名攻城战
	* number 场次
	* npcID 
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void SignUpGCZ(const int32 number, const int32& npcID);
	/**
	* 通知开始匹配 显示匹配界面
	*/
	void NotifyToStartMatchGCZ(int32 curNumber);

	/**
	* 通知取消匹配 关闭匹配界面
	*/
	void NotifyCancelMatchGCZ();

	/**
	* 取消匹配攻城战
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
		void CancelMatchGCZ();

#pragma endregion

#pragma region 大荒战场
	/**
    * 显示匹配界面回调
    */
	void OnBattleMatchStart();

	/**
	* 取消匹配大荒战场
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleActivityInterface")
                void InterruptBattleActivityMatch();
#pragma endregion
private:
	/// 客户端模拟灵能点的更新
	void AddTaosimPointPerSecond();
	void AddDemonPointPerSecond();
private:
	TMap<FString, FTimerHandle> PagodaTimerDict;			// 灵塔时间 tick,用于模拟灵能点增加
	int32 TaosimPownerPoint;								// 仙道灵能点
	int32 DemonPownerPoint;									// 魔道灵能点
	int32 TaosimIntegral;									// 仙道积分
	int32 DemonIntegral;									// 魔道积分
	TMap<FString, TArray<FALLBHZBTONGINTEGRALDATA>> AllBHZBTongIntegralDatas; //帮会争霸历届排行数据
};