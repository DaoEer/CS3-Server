#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtJZZYDBInterface.generated.h"

/*
* 文件名称：MonsterExtJZZYDBInterface.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-03-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtJZZYDBInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtJZZYDBInterface();
	~UMonsterExtJZZYDBInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtJZZYDBInterface'"); } //获取蓝图对象路径

	/**
	*服务器通知自身这一组开始进行抢夺
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJZZYDBInterface")
		void onStartOccupy();

	/**
	*服务器通知自身这一组结束抢夺
	*
	@param isPlayerOccupy:是否是玩家占领
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJZZYDBInterface")
		void onEndOccupy(bool isPlayerOccupy);

	//通知服务器，有碰撞。
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYDBInterface")
		void RPC_onCollisionZYDB(FVector pos);

	//通知服务器，玩家进入本区域
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYDBInterface")
		void RPC_onEnterZYDBScope();

	//通知服务器，玩家离开本区域
	UFUNCTION(BlueprintCallable, Category = "UMonsterExtJZZYDBInterface")
		void RPC_onLeaveZYDBScope();
	
	virtual void InitBlueCB() override;
private:
	bool mIsStartOccupy = false;
	int8 mOccupyStatus = 0;		//0:未被占领  1：玩家占领  2：boss占领
};
