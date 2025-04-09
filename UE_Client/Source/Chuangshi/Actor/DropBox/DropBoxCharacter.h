#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "GameData/Shape/BaseShape.h"
#include "Engine/EngineTypes.h"
#include "GameData/Item/ItemBase.h"
#include "DropBoxCharacter.generated.h"

/*
* 文件名称：DropBoxCharacter.h
* 功能说明：掉落箱子Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/


DECLARE_DELEGATE_OneParam(FDropBoxDelegate, bool);



/*
* 掉落箱子Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ADropBoxCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()

public:
	ADropBoxCharacter();///<构造函数
	virtual void OnUnBindActorCallBack() override;
	virtual void GossipWith() override;///<重写GossipWith
	virtual void OnCreateApperanceOver() override;
	virtual TArray<UItemBase*> GetBoxItemList();
	/**
	*DropBox对某个玩家是否可见
	*
	*@param PlayerDBID 玩家DBID(UINT64)
	*
	*@return bool
	*/
	virtual bool isVisible(const UINT64 &PlayerDBID);

	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
	void TraceDropBox(float range);///<走近DropBox一定距离
	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")

	/**
	*Define method
	*服务器回调，更新DropBox可见性
	*
	*@return 无
	*/
	void updateDropBoxModelVisible();///<服务器回调，更新DropBox可见性

	/**
	*关闭箱子
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
	void CloseBox();

	/**
	*开启箱子
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
	void OpenBox();

	/**
	*播放粒子
	*
	*@param EffectID 粒子ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
	void PlayEffect(FString EffectID);

	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
		void StopEffect();

	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
		bool IsBoxEmpty();

	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
		void SetBoxEffect();

	void RealTraceDropBox(float range, FDropBoxDelegate Delegate = nullptr);///<走近DropBox一定距离

	///<设置宝箱是否已经请求过服务器宝箱列表信息
	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
		void SetAlreadyRequest(bool IsRequest);

	//< 判断UID在不在宝箱物品列表里面
	UFUNCTION(BlueprintCallable, Category = "Game|DropBox")
		bool HasUIdInDropBoxItemList(const FString& UId);

	///<更新掉落宝箱物品信息列表（UId：拾取物品的UID，LeftAmount：拾取过后宝箱剩余某个物品数量）
	void UpdateDropBoxItemList(const FString& UId, int32 LeftAmount);

	UFUNCTION(BlueprintNativeEvent, Category = "Game|DropBox")
		void RequestPickUpAllItemsOrOpenBox();///<交互时全部拾取或者打开宝箱

	void DropBoxInteractiveFinshed();///<交互状态完成

	/**
	*模拟抛物线位移和缩放
	*
	*@param InStartPosition 起始位置
	*@param InEndPosition 目标位置
	*@param XMoveSpeed 水平移动速度
	*@param Scale 模型最终大小
	*
	*@return 无
	*/
	void CurveMoveAndZoom(const FString& DragActionID, const FString& levitateActionID, const FVector& InStartPosition, const FVector& InEndPosition, float XMoveSpeed, float Scale = 1.0f, float Gravity = 980.0f);

	void OpenDropEffectEvent(FString EffectID1 = TEXT("103088"), FString EffectID2 = TEXT("103088_3"));
	UFUNCTION()
	void OpenDropStayEffectEvent();
	void FlyTargetEffectEvent(int32 TargetID, FString EffectID);
	virtual void FlyTargerOverEvent();//飞行光效到达目标点通知

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual UBaseShape* CreateSphereShape();
	UFUNCTION(BlueprintNativeEvent, Category = "Game|RPC")
		void OnPlayerBeginOverlap();
	virtual void OnPlayerBeginOverlap_Implementation();
	UFUNCTION(BlueprintNativeEvent, Category = "Game|RPC")
		void OnPlayerEndOverlap();
	virtual void OnPlayerEndOverlap_Implementation();

private:
	int32 ConfirmQuality();
	void StopCurveMoveAndZoom(float Scale, const FVector& InEndPosition, const FString& levitateActionID);
	void clearAllStayEffect();

public:
	///<宝箱创建的时候需去请求服务器宝箱物品列表（点击宝箱的时候也会去请求）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Game|DropBox")
		bool IsAlreadyRequest = false;

	///<掉落宝箱的物品列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
		TArray<UItemBase*> DropBox_ItemList;

protected:
		float m_SphereRadius = 6.0f;///<圆形陷阱检测距离半径
		UBaseShape* pDropBoxShape = nullptr;

private:
	TArray<int32> StayEffectUIDList;
	FString StayEffectID;
	int32 CurEmitterUID = -1;
	FTimerHandle CurveMoveHandle;
	float CurveMovePercent = 0.0f;
	float CurveMoveDeltaTime = 0.0f;
	int32 DeletedCount;///用来计数需要删除的粒子数量
};