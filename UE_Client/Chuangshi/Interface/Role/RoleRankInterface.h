// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/GameRankData.h"
#include "Entity/Alias.h"
#include "RoleRankInterface.generated.h"

/*
* 文件名称：RoleRankInterface.h
* 功能说明：玩家在线奖励
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-08-15
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleRankInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	URoleRankInterface();
	~URoleRankInterface();
	static FString GetName() { return TEXT("RoleRankInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleRankInterface.BP_RoleRankInterface_C'"); } //获取蓝图对象路径

	
	/* 打开排行榜界面
	* @param NpcID  打开界面NPCid
	* @param RankNum 玩家在本服等级排行榜的排名(未上榜为-1)
	* @param TotalPage  等级排行榜总页数
	* @param LevelRank  排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OpenGameRankBP(const int32& NpcID, const int32& RankNum, const int32& TotalPage, const TArray<FLevelRankData>& LevelRank);

	/* 第一次请求排行榜数据
	* @param RankType  排行榜类型
	* @param Camp 请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	*/
	UFUNCTION(BlueprintCallable)
		void RequestRankFirstTime(EGameRank RankType, const int32& Camp);

	/* 第一次请求等级排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param RankNum 玩家在本服等级排行榜的排名(未上榜为-1)
	* @param TotalPage  等级排行榜总页数
	* @param LevelRank  等级排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestLevelRankFirstTimeBP(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FLevelRankData>& LevelRank);

	/* 第一次请求战力排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param RankNum 玩家在本服战力排行榜的排名(未上榜为-1)
	* @param TotalPage  战力排行榜总页数
	* @param CombatRank  战力排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestCombatRankFirstTimeBP(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FCombatRankData>& CombatRank);

	/* 第一次请求财富排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param RankNum 玩家在本服财富排行榜的排名(未上榜为-1)
	* @param TotalPage  财富排行榜总页数
	* @param MoneyRank  财富排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestMoneyRankFirstTimeBP(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FMoneyRankData>& MoneyRank);

	/* 第一次请求神器排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param RankNum 玩家在本服神器排行榜的排名(未上榜为-1)
	* @param TotalPage  神器排行榜总页数
	* @param WeaponRank  神器排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestWeaponRankFirstTimeBP(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FWeaponRankData>& WeaponRank);

	UFUNCTION(BlueprintNativeEvent)
		void OnRequestRankStoreMoney(const FString& StoreMoney);

	/* 请求排行榜数据
	* @param RankType  排行榜类型
	* @param Camp 请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param Page  请求排行榜页数
	*/
	UFUNCTION(BlueprintCallable)
		void RequestRank(EGameRank RankType, const int32& Camp, const int32& Page);

	/* 第一次请求等级排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param LevelRank  等级排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestLevelRankBP(const int32& Camp, const int32& Page, const TArray<FLevelRankData>& LevelRank);

	/* 第一次请求战力排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param CombatRank  战力排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestCombatRankBP(const int32& Camp, const int32& Page, const TArray<FCombatRankData>& CombatRank);

	/* 第一次请求财富排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param MoneyRank  财富排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestMoneyRankBP(const int32& Camp, const int32& Page, const TArray<FMoneyRankData>& MoneyRank);

	/* 请求神器排行榜回调
	* @param Camp  请求本服（阵营）数据（0-本服排行榜，1-仙道排行榜，2-魔道排行榜）
	* @param WeaponRank  神器排行榜数据
	*/
	UFUNCTION(BlueprintNativeEvent)
		void OnRequestWeaponRankBP(const int32& Camp, const int32& Page, const TArray<FWeaponRankData>& WeaponRank);
	/*
	*通知客户端排行榜已更新，重新请求数据
	* @param RankType 排行榜类型
	*/
	UFUNCTION(BlueprintNativeEvent)
		void Client_updateRankData(const uint8&  RankType);

	UFUNCTION(BlueprintCallable)
		void clearRankData();

	void OpenGameRank(const int32& INT32_1, const int32& INT32_2, const int32& INT32_3, const FVariant& fixedDict );

	void OnRequestCombatRankFirstTime(const int32& INT32_0, const int32& INT32_1, const int32& INT32_2, const FVariant& fixedDict );

	void OnRequestLevelRankFirstTime(const int32& INT32_0, const int32& INT32_1, const int32& INT32_2, const FVariant& fixedDict );

	void OnRequestMoneyRankFirstTime(const int32& INT32_0, const int32& INT32_1, const int32& INT32_2, const FVariant& fixedDict );

	void OnRequestWeaponRankFirstTime(const int32& INT32_0, const int32& INT32_1, const int32& INT32_2, const FVariant& fixedDict );

	virtual void InitBlueCB() override;
	virtual void onLeaveWorld() override;

private:
	inline void GetLevelRankData(const int32& Camp, const int32& Page, TArray<FLevelRankData>& RankType);
	inline void GetCombatRankData(const int32& Camp, const int32& Page, TArray<FCombatRankData>& RankType);
	inline void GetMoneyRankData(const int32& Camp, const int32& Page, TArray<FMoneyRankData>& RankType);
	inline void GetWeaponRankData(const int32& Camp, const int32& Page, TArray<FWeaponRankData>& RankType);
public:
	///玩家自己的财富值
	UPROPERTY(BlueprintReadOnly)
		int64 MoneyRankValue;
private:
	/// 等级排行榜排名
	TMap<int32, int32> LevelRankNum;
	///等级排行榜页数
	TMap<int32, int32> LevelRankPages;
	///等级升降
	TMap<int32, int32> LevelRankAscend;
	/// 仙道等级排行榜
	TArray<FLevelRankData> XianLevelRankList;
	/// 魔道等级排行榜
	TArray<FLevelRankData> MoLevelRankList;
	///全服等级排行榜
	TArray<FLevelRankData> AllLevelRankList;

	/// 战斗力排行榜排名
	TMap<int32, int32> CombatRankNum;
	///战斗力排行榜页数
	TMap<int32, int32> CombatRankPages;
	///战斗力升降
	TMap<int32, int32> CombatRankAscend;
	/// 仙道战斗力排行榜
	TArray<FCombatRankData> XianCombatRankList;
	/// 魔道战斗力排行榜
	TArray<FCombatRankData> MoCombatRankList;
	///全服战斗力排行榜
	TArray<FCombatRankData> AllCombatRankList;

	/// 财富排行榜排名
	TMap<int32, int32> MoneyRankNum;
	///财富排行榜页数
	TMap<int32, int32> MoneyRankPages;
	///财富升降
	TMap<int32, int32> MoneyRankAscend;
	/// 仙道财富排行榜
	TArray<FMoneyRankData> XianMoneyRankList;
	/// 魔道财富排行榜
	TArray<FMoneyRankData> MoMoneyRankList;
	///全服财富排行榜
	TArray<FMoneyRankData> AllMoneyRankList;

	/// 神器排行榜排名
	TMap<int32, int32> WeaponRankNum;
	///神器排行榜页数
	TMap<int32, int32> WeaponRankPages;
	///神器升降
	TMap<int32, int32> WeaponRankAscend;
	/// 仙道神器排行榜
	TArray<FWeaponRankData> XianWeaponRankList;
	/// 魔道神器排行榜
	TArray<FWeaponRankData> MoWeaponRankList;
	///全服神器排行榜
	TArray<FWeaponRankData> AllWeaponRankList;
	///等级排行榜更新标记
	bool levelUptadeMark = false;
	///战力排行榜更新标记
	bool combatUptadeMark = false;
	///财富排行榜更新标记
	bool moneyUptadeMark = false;
	///神器排行榜更新标记
	bool weaponUptadeMark = false;



	/// 请求排行榜时间
	FDateTime requestTime;

};

