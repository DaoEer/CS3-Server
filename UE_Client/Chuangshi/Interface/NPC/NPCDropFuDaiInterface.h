#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "NPCDropFuDaiInterface.generated.h"

/*
* 文件名称：NPCDropFuDaiInterface.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-12-01
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCDropFuDaiInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCDropFuDaiInterface();
	~UNPCDropFuDaiInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCDropFuDaiInterface'"); } //获取蓝图对象路径
	/**
	*通知服务器碰到地面或者玩家和玩家的绑定光效
	*
	*@Param int32 PlayID 玩家的EntityID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "NPCDropFuDaiInterface|RPC")
	void RPC_onFuDaiCollisionBegin(const int32& PlayID);
	/**
	*通知服务器福袋的光效飞到了玩家手上
	*
	*@Param int32 PlayID 玩家的EntityID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "NPCDropFuDaiInterface|RPC")
	void RPC_onFuDaiCollisionPlayer(const int32& PlayID);
	/**
	*通知服务器怪物收取场景中所有的正在落下和已经楼下的财宝
	*
	*@Param int32 MondterID 怪物的EntityID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "NPCDropFuDaiInterface|RPC")
	void RPC_onFuDaiCollisionMonster(const int32& MonsterID);
	

	virtual void InitBlueCB() override;

	/**
	* 通知客户端开始移动
	*@Param Resistance 重力
	*@Param EffectID 获得奖励的光效(没有光效时记得给个默认光效)
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "NPCDropFuDaiInterface")
		void CLIENT_fuDaiStartMove(const float& Resistance, const FString& EffectID);

	/**
	* 在对应地面位置播放循环光效
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "NPCDropFuDaiInterface")
		void CLIENT_OnPlayFloorEffect(const FString& EffectID);

	/**
	*通知显示金币模型旁边显示数量
	*
	*@Param int32 moneyAmount 金币数量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "NPCDropFuDaiInterface|RPC")
		void NotifyIntegralAmount(const int32& moneyAmount);

public:

	UPROPERTY(BlueprintReadWrite)
		FString PickEffectID;

	UPROPERTY()
		class UTextRenderComponent* TextRenderComponent;///<用来显示金币数量的组件

private:
	///设置位置定时器
	FTimerHandle SetPosTimer;
	void SetJinBiPosition();
};
