#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "GameData/Shape/BaseShape.h"
#include "SpellBoxCharacter.generated.h"

/*
* 文件名称：SpellBoxCharacter.h
* 功能说明：场景物件Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/

/*
* 场景物件Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ASpellBoxCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()
public:
	ASpellBoxCharacter();///<构造函数

	void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason)override;
	virtual void OnCreateApperanceOver() override;
	virtual void InitFilterActorComponent() override;

	virtual void SetInitAction() override;///<重写SetInitAction
	virtual void GossipWith() override;///<重写GossipWith

	//播放动画移动结束后回调，必须是在有加入延迟时间时才会触发
	UFUNCTION(BlueprintImplementableEvent, Category = "SpellBox")
		void FinshPlayAction(float delayStop);

	UFUNCTION(BlueprintNativeEvent, Category = "SpellBox")
		void OnSetBoxStatus(int32 BoxStatus);///<boxStatus改变通知蓝图

	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };
	/**
	* 金丹显示头顶倒计时通知
	*
	*@param LifeTime 时长
	*@param TimerInterval 倒计时回调时间间隔
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "SpellBox")
		void OnShowTopCountDownBP(float LifeTime, float TimerInterval);

	/**
	*Define method
	* 金丹隐藏头顶倒计时通知
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "SpellBox")
		void OnHideTopCountDownBP();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_reqStartInteractive();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_reqInterruptInteractive();

	///玩家靠近
	UFUNCTION(BlueprintNativeEvent, Category = "SpellBox")
		void OnPlayerBeginOverlap();

	///玩家离开
	UFUNCTION(BlueprintNativeEvent, Category = "SpellBox")
		void OnPlayerEndOverlap();

	void SpellBoxInteractiveInterrupted();///<交互中断
protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual FString GetEntityUName() override;///<重写GetEntityUName

public:
	UBaseShape* CreateSphereShape();

public:
	///<圆形陷阱检测距离半径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Shape|ReadWrite", DisplayName = "SphereRadius")
		float m_SphereRadius = 5.0f;

private:
	UBaseShape* pSpellBoxShape = nullptr;
};