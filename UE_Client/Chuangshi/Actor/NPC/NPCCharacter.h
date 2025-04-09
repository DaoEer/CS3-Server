#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "GameData/Shape/BaseShape.h"
#include "NPCCharacter.generated.h"

/*
* 文件名称：NPCCharacter.h
* 功能说明：NPCCharacter
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/


/*
* NPCCharacter类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ANPCCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()
public:
	ANPCCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason)override;
	virtual void OnCreateApperanceOver() override;
	virtual void GossipWith() override;///<重写GossipWith
	virtual void SetInitAction() override;///<重写SetInitAction
	virtual void PlayDeadEffect() override;

	///玩家靠近
	UFUNCTION(BlueprintNativeEvent, Category = "Game|NPC")
	void OnPlayerBeginOverlap();

	///玩家离开
	UFUNCTION(BlueprintNativeEvent, Category = "Game|NPC")
	void OnPlayerEndOverlap();

	//UFUNCTION(BlueprintPure, Category = "Game|NPC")
	virtual int32 GetFinalCamp();///<获取最终阵营

	/**
	*NPC头像冒泡对话
	*
	* voice : 语音ID
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void BubbleDialogue(const FString& voice);

	UFUNCTION(BlueprintCallable, Category = "Game|NPC")
		void RPC_onCollisionBegin();

	/*-------------------练兵场NPC相关-------------------------------------*/
	/**
	*NPC练兵场宣战状态改变事件
	*
	* State : 宣战状态 
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnDeclareWarStateChanged(int32 State);

	/**
	*练兵场占领玩家改变事件
	*
	* OccupyPlayerName : 占领的玩家名字
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnOccupyPlayerNameChanged(const FString& OccupyPlayerName);

	/**
	*创建练兵场区域事件
	*
	* IsOwnSide True：己方势力，False：敌方势力；
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnCreateTrainSoldierGroundArea(const FString& InScriptID, bool IsOwnSide);
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnUpdaterainSoldierGroundArea(bool IsOwnSide);
	/*----------------------------------------------------------------------*/

	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual FString GetEntityUName() override;///<重写GetEntityUName
	virtual bool IsEntityBoss() override;///<重写IsEntityBoss
	
public:
	UBaseShape* CreateSphereShape();

public:
	///<圆形陷阱检测距离半径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Shape|ReadWrite", DisplayName = "SphereRadius")
	float m_SphereRadius = 5.0f;

private:
	UBaseShape* pNPCShape = nullptr;
};