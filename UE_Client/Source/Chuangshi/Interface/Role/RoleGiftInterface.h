// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/OnLineReward.h"
#include "RoleGiftInterface.generated.h"

/*
* 文件名称：RoleGiftInterface.h
* 功能说明：玩家在线奖励
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-08-15
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleGiftInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleGiftInterface();
	~URoleGiftInterface();
	static FString GetName() { return TEXT("RoleGiftInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleGiftInterface.BP_RoleGiftInterface_C'"); } //获取蓝图对象路径

	/**
	*显示在线奖励
	*
	*@param LiftTime 还有多长时间可以领取(单位：秒)
	*@param Reward 奖励
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnShowOnlineReward(const int32& LiftTime, const FString& Reward, const int32& BindType);

	// 领取新手在线奖励
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		void ReceiveNewPlayerGift();
	// 完成新手在线奖励
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnFinishReceiveNewPlayerGift();

	/**
	*签到奖励
	*
	*@param SignInTotalNum 累计签到次数
	*@param SignInTotalRewardNum 领取累计奖励次数
	*@param SignInRewardList 已经领取累计奖励次数
	*@param SignInJson 签到json数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
	void OnShowSignInRewardEnd();

	void OnShowSignInReward(const int32& SignInTotalNum, const int32& SignInTotalRewardNum, const FVariant& SignInRewardList, const FVariant& SignInJson);

	// 某天签到奖励
	// 返回 {ItemID:amount,....}
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		TArray<FSignInReward> GetSignInReward(const int32& Day);

	// 累计签到奖励
	// 返回 {ItemID:amount,....}
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		TArray<FSignInReward> GetTotalSignInReward(const int32& AccumulateDay);

	// 是否已签到
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		bool bSignIn(const int32& year, const int32& month, const int32& day);

	// 签到
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		void SignInOnline();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnSignInOnlineSuccess();

	// 补签一天
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		void AugmentSignIn(const int32& Year, const int32& Month, const int32& Day);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnAugmentSignInSuccess(const int32& Year, const int32& Month, const int32& Day);

	// 补签一个月
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		void AugmentSignInMonth(const int32& Year, const int32& Month);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnAugmentSignInMonthSuccess(const int32& Year, const int32& Month);

	// 领取累计签到奖励
	UFUNCTION(BlueprintCallable, Category = "RoleGiftInterface")
		void ReceiveTotalSignReward(const int32& AccumulateNum);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnReceiveTotalSignRewardSuccess(const int32& AccumulateNum);

	// 达到领取 某累计签到次数
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnReachSignRewardNum(const int32& num);

	// 领取完一轮累计签到次数
	UFUNCTION(BlueprintNativeEvent, Category = "RoleGiftInterface")
		void OnFinishRecSignReward();

	virtual void InitBlueCB() override;
	virtual void onLeaveWorld() override;
public:
	/// 新手在线奖励数据 { itemID : amount ,...}
	UPROPERTY(BlueprintReadOnly)
		TArray<FSignInReward> OnLineRewardItems;

	/// 签到数据
	UPROPERTY(BlueprintReadOnly)
		TArray<FSignInData> SignInList;
	/// 累计奖励次数
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, SIGN_IN_REWARD_TYPE> SignInRewardMap;



private:
	/// 初始化 累计签到数据
	void InitTotalSignInNum();
	/// 生成奖励数据
	void AnalysisItemStr(const FString& ItemStr, const int32& BindType, TArray<FSignInReward>& ItemList);

	void CalculateAugmentSignInMonth(const int32& Month, TArray<int32>& Days);

	/// 增加签到次数
	void AddSignInNum();

private:
	/// 签到计数
	int32 SignInNum;

	/// 领取签到累计奖励 次数
	int32 SignInRewardNum;


};