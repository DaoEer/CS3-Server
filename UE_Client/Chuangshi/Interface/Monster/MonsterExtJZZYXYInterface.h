#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtJZZYXYInterface.generated.h"

/*
* 文件名称：MonsterExtJZZYXYInterface.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-03-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtJZZYXYInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtJZZYXYInterface();
	~UMonsterExtJZZYXYInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtJZZYXYInterface'"); } //获取蓝图对象路径

	//通知服务器，玩家踩到了虚影
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void RPC_onTreadZYXY();

	//通知服务器，玩家踩完点了
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void RPC_onTreadZYPoint();

	/**
	*服务器通知自身这一组开始进行抢夺
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void onStartOccupy();

	/**
	*服务器通知自身这一组结束抢夺
	*
	@param isPlayerOccupy:是否是玩家占领(boss占领，需要熄灭所有已经点亮的点)
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void onEndOccupy(bool isPlayerOccupy);

	//判断当前是否能点亮虚影
	bool isCanLight(int32 entityID);
	//通知服务器，玩家踩到了虚影
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
	bool BP_isCanLight();

	//通知服务器，玩家踩到了虚影
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void BP_StarStepFloor(float Distance, FString effectID);

	//停止玩家踩到了虚影SetTimer通知
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void BP_StopStepFloor();

	/**
	*服务器通知自身爆炸倒计时(爆炸预警时间)
	*
	@param time: -1:取消预警   0：爆炸效果   >0：爆炸倒计时
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void onNotifyExplodeCountdown(int time);
	/**

	*服务器通知熄灭部分已经点亮的点
	*
	@param num:熄灭的数量,为0则当前字的点全部熄灭
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJZZYXYInterface")
		void onExtinguishLight(int32 num);
	
	virtual void InitBlueCB() override;

	TArray<int32> EffectUIDs;///特效储存器
	TArray<FName> SaveSocketNmaes;
	TArray<FName> SocketNames;//当前需要踩踏的总个数
private:
	bool IsStepFloor = false;



	FTimerHandle CheckStepFloorventHandle;///<检测拆地板生成火焰的定时器
	bool mIsStartOccupy = false;
	int8 mOccupyStatus = 0;		//0:未被占领  1：玩家占领  2：boss占领
};
