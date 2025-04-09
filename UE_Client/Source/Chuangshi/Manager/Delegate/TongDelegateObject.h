// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Manager/Delegate/MailDelegateObject.h"
#include "GameData/BHZBData.h"
#include "GameData/GameDeFine.h"
#include "TongDelegateObject.generated.h"

/**
 * 帮会系统委托声明对象
 */

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveCandidateFromBHZB, FString, MemberDBID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnInitBHZBNPCPointDatas);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataToTongMemberClientProtectData, int32, groupTeamID, int32, pointIndex);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataToTongMemberClientAttackData, int32, groupTeamID, int32, pointIndex);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataNPCPointRestEndTime, int32, pointIndex, FString, restEndTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataNPCPointReadyEndTime, int32, pointIndex, FString, readyEndTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataNPCPointDeclareWarState, int32, pointIndex, uint8, declareWarState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataNPCPointOccupyTongDBID, int32, pointIndex, FString, occupyTongDBID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdataHomeBarracksMapDataToAllMember);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnUpdataMemberPositionToClient);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnShowExitPointSaveSpaceBtn);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnHideExitPointSaveSpaceBtn);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdataMyGroupIDToClient, int32, groupID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataBHZBPointJoinAttackMembers, int32, pointIndex, const TArray<FString>&, joinAttackMemberDBIDs);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataBHZBPointJoinProtectMembers, int32, pointIndex, const TArray<FString>&, JoinProtectMemberDBIDs);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnShowGroupIDAttackPointSign, int32, pointIndex, int32, groupID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHideGroupIDAttackPointSign, int32, pointIndex);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnShowBHZBIntegralRankWin, const TArray<FBHZBTONGINTEGRALDATA>&, rankDatas, int32, delayCloseTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnPlunderMemberChange);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnSetbhzbSignUpMembersIsActive, int32, groupID, bool, isActive, int32, pointIndex);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateBHZBWarDetailIntegralData, int32, integral, int32, rank);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdateBHZBWarDetailOccupyNumber, int32, occupyPointAmount);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(FOnUpdateBHZBWarDetailTeamData, int32, teamNumber, int32, pointIndex, int32, pointState, FString, pointName);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveBHZBWarDetailTeamData, int32, teamNumber);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateBHZBWarDetailOccupyPointData, int32, pointIndex, int32, pointState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnAddBHZBWarDetailOccupyPointData, int32, pointIndex, int32, pointState, FString, pointName);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAddBHZBWarMsgData, int32, statusID, FString, statusArgs);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveBHZBWarrDetailOccupyPoint, int32, pointIndex);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnUpdateNPCPointAttackGroupTeamID, int32, pointIndex, int32, attackGroupTeamID, const FString&, declareTongDBID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdataBHZBPointJoinProtectTeamID, int32, pointIndex, int32, joinProtectTeamID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetTongBattleAllocation, TONG_PICKUP_TYPE, allocation);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetTongPlunderAllocation, TONG_PICKUP_TYPE, allocation);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOpenTongPickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnClosedTongPickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOpenTongDicePickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnClosedTongDicePickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPickUpByLeaderSuccessed, const FString&, uid, const FString&, playerName);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnTongRollRandomDropBoxResult, int32, DropBoxID, const FString&, ItemUid, int32, Roll);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(FOnTongRollRandomMaxDropBox, int32, DropBoxID, const FString&, ItemUid, const FString&, PlayerName, int32, MaxRoll);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnClearAllTongSignMemberData);
UCLASS()
class CHUANGSHI_API UTongDelegateObject : public UMailDelegateObject
{
	GENERATED_BODY()

public:
#pragma region	/** 帮会争霸 */
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnRemoveCandidateFromBHZB  OnRemoveCandidateFromBHZB;
	/**
	* 帮会争霸据点数据更新完成
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnInitBHZBNPCPointDatas OnInitBHZBNPCPointDatas;
	/**
	* 更新防守方的数据
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataToTongMemberClientProtectData  OnUpdataToTongMemberClientProtectData;
	/**
	* 更新进攻方的数据
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataToTongMemberClientAttackData  OnUpdataToTongMemberClientAttackData;
	/**
	* 更新据点重置时间
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataNPCPointRestEndTime OnUpdataNPCPointRestEndTime;
	/**
	* 更新据点准备时间
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataNPCPointReadyEndTime OnUpdataNPCPointReadyEndTime;
	/**
	* 更新据点宣战状态
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataNPCPointDeclareWarState OnUpdataNPCPointDeclareWarState;
	/**
	* 更新据点占领的帮会信息
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataNPCPointOccupyTongDBID OnUpdataNPCPointOccupyTongDBID;
	/**
	* 更新大本营信息
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataHomeBarracksMapDataToAllMember OnUpdataHomeBarracksMapDataToAllMember;
	/**
	* 更新队伍信息到M大地图
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataMemberPositionToClient OnUpdataMemberPositionToClient;
	/**
	* 显示离开据点按钮
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnShowExitPointSaveSpaceBtn OnShowExitPointSaveSpaceBtn;
	/**
	* 隐藏离开据点按钮M大地图
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnHideExitPointSaveSpaceBtn OnHideExitPointSaveSpaceBtn;
	/**
	* 更新玩家所在队伍编号到界面
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataMyGroupIDToClient OnUpdataMyGroupIDToClient;
	/**
	* 更新据点攻占成员
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataBHZBPointJoinAttackMembers OnUpdataBHZBPointJoinAttackMembers;
	/**
	* 更新据点防守成员
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataBHZBPointJoinProtectMembers OnUpdataBHZBPointJoinProtectMembers;
	/**
	* 显示据点进攻标记
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnShowGroupIDAttackPointSign OnShowGroupIDAttackPointSign;
	/**
	* 隐藏据点进攻标记
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnHideGroupIDAttackPointSign OnHideGroupIDAttackPointSign;
	/**
	* 隐藏据点进攻标记
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnShowBHZBIntegralRankWin OnShowBHZBIntegralRankWin;
	/**
        * 设置帮会争霸报名成员队伍状态
        */
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnSetbhzbSignUpMembersIsActive OnSetbhzbSignUpMembersIsActive;
	/**
	* 更新帮会概况积分和排名
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdateBHZBWarDetailIntegralData OnUpdateBHZBWarDetailIntegralData;
	/**
	* 更新帮会概况占领据点数量
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdateBHZBWarDetailOccupyNumber OnUpdateBHZBWarDetailOccupyNumber;
	/**
        * 更新帮会概况某个队伍信息
        */
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdateBHZBWarDetailTeamData OnUpdateBHZBWarDetailTeamData;
	/**
	* 移除帮会概况某个队伍
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnRemoveBHZBWarDetailTeamData OnRemoveBHZBWarDetailTeamData;
	/**
	* 更新帮会概况某个据点状态数据
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdateBHZBWarDetailOccupyPointData OnUpdateBHZBWarDetailOccupyPointData;
	/**
	* 增加帮会概况据点数据
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnAddBHZBWarDetailOccupyPointData OnAddBHZBWarDetailOccupyPointData;
	/**
	* 移除帮会概况据点数据
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
                FOnRemoveBHZBWarrDetailOccupyPoint OnRemoveBHZBWarrDetailOccupyPoint;
	/**
        * 增加帮会系统消息
        */
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnAddBHZBWarMsgData OnAddBHZBWarMsgData;
	/**
	 * 更新据点进攻队伍ID
	 */
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdateNPCPointAttackGroupTeamID OnUpdateNPCPointAttackGroupTeamID;
	/**
	* 更新据点回防队伍ID
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnUpdataBHZBPointJoinProtectTeamID OnUpdataBHZBPointJoinProtectTeamID;
	/**
	* 帮会争霸结束，清除界面数据
	*/
	UPROPERTY(BlueprintAssignable, Category = "Tong|BHZB")
		FOnClearAllTongSignMemberData OnClearAllTongSignMemberData;

#pragma endregion
#pragma region	/** 掠夺战 */
	UPROPERTY(BlueprintAssignable, Category = "Tong|Plunder")
		FOnPlunderMemberChange OnPlunderMemberChange;
#pragma endregion

#pragma region	/** 帮会拾取 */
	//设置帮会争霸分配模式
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnSetTongBattleAllocation OnSetTongBattleAllocation;
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
	//设置帮会掠夺分配模式
		FOnSetTongPlunderAllocation OnSetTongPlunderAllocation;
	//打开帮主分配界面
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnOpenTongPickWnd OnOpenTongPickWnd;
	//关闭帮主分配界面
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnClosedTongPickWnd OnClosedTongPickWnd;
	//打开帮会掷点分配界面
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnOpenTongDicePickWnd OnOpenTongDicePickWnd;
	//关闭帮会掷点分配界面
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnClosedTongDicePickWnd OnClosedTongDicePickWnd;
	//帮主分配成功
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnPickUpByLeaderSuccessed OnPickUpByLeaderSuccessed;
	//帮会掷点结果通知
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnTongRollRandomDropBoxResult OnTongRollRandomDropBoxResult;
	//帮会掷点结果最大值通知
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnTongRollRandomMaxDropBox OnTongRollRandomMaxDropBox;
#pragma endregion
};
