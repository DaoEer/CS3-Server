#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "GameData/Shape/BaseShape.h"
#include "TrapCharacter.generated.h"


/*
* 文件名称：TrapCharacter.h
* 功能说明：陷阱Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/



/*
* 陷阱Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ATrapCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()
#pragma region	Avatar功能相关
public:

	virtual void InitFilterActorComponent() override;

#pragma endregion

public:
	ATrapCharacter();///<构造函数

	UFUNCTION(BlueprintCallable, Category = "Game|Trap")
	int32 GetTriggerShape();///<获取陷阱形状

	UFUNCTION(BlueprintPure, Category = "Game|Trap")
	FVector GetTriggerLocation();///<获取位置

	//UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	virtual float GetFilterSpeed() override;///<BlueprintPure 获得Filter速度
	/**
	*BlueprintCallable Entity进入陷阱回调
	*
	*@param eID	 EntityId(int32)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Trap")
	void OnEnterTrap(int32 eID);

	/**
	*BlueprintCallable Entity离开陷阱回调
	*
	*@param eID	 EntityId(int32)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Trap")
	void OnLeaveTrap(int32 eID);

	void AddTrapShape();///<加客户端陷阱

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Trap")
	void ChangeProgressBar(float value);///< 陷阱特殊进度条 CST-3740

	UFUNCTION(BlueprintNativeEvent, Category = "Game|Trap")
	void CLIENT_DelayToAddTrap(float value);///延时添加陷阱

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Trap|TrapBattleFlag")
		void OnOccupyProgressChanged( int32 occurProgress, int32 maxProgress);///<战旗占领进度改变通知蓝图

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Trap|TrapBattleFlag")
		void OnOccupyBelongTypeChanged(int32 belongType);///<战旗归属被改变通知蓝图

	void OnBeginOverlap();///玩家进入Shape回调
	void OnEndOverlap();///玩家离开Shape回调

	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };

	UBaseShape* CreateBoxShape();
	UBaseShape* CreateSphereShape();
	UBaseShape* CreateCylinderShape();
	virtual void OnInitialized() override;
	virtual void SetInitAction() override;
	virtual float GetMoveSpeed() override;
protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual FString GetEntityUName() override;///<重写GetEntityUName
	virtual bool IsEntityMoveType(MOVETYPE MoveType) override;///<重写IsEntityMoveType

private:
	UBaseShape* pTrapShape = nullptr;
};