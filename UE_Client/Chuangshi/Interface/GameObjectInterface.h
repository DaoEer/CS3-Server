// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/GameDeFine.h"
#include "GameObjectInterface.generated.h"


class UCS3AudioComponent;
/*
* 文件名称：GameObjectInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UGameObjectInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UGameObjectInterface();
	~UGameObjectInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.GameObjectInterface'"); } //获取蓝图对象路径
			
public:
	/**
	*设置模型编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
		virtual void OnRep_modelNumber();


	/**
	*设置额外模型编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
		virtual void OnRep_extraModelNumber();

	/**
	*设置模型缩放
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
		virtual void OnRep_modelScale();
	/**
	*领兵数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
	void OnRep_armyModelList();

	/**
	*同步玩家位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
		virtual void OnRep_SyncPosClient();

	/**
	*设置移动速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|Trap")
		virtual void OnRep_moveSpeed();
	
public:

	/**
	*是否是某种类型entity
	*
	*@param entityID ，（int32）
	*
	*@return bool 如果是，则返回True，反之返回False
	*/
	bool isEntityFlag(ENTITY_TYPE entityFlag);

	/**
	*获取entity类型
	*
	*@param entityID ，（int32）
	*
	*@return bool 如果是，则返回True，反之返回False
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
	ENTITY_TYPE getEntityFlag();


	/**
	*是否是某种类型(二级标识)entity
	*
	*@param entityID ，（int32）
	*
	*@return bool 如果是，则返回True，反之返回False
	*/
	bool IsEntityFlagExt(ENTITY_TYPE_EXT entityFlagExt);

	/**
	*获取entity二级类型
	*
	*@param entityID ，（int32）
	*
	*@return int32 
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
	ENTITY_TYPE_EXT GetEntityFlagExt();

	virtual	 void OnDelayStopAction(float delayStop) {};
	/** 
	*Define method
	*播放动作
	*
	*@param ActionId ，动作ID（FString）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_OnPlayAction(const FString& ActionId, float delayStop);
	
	/**
	*Define method
	*停止动作播放
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		 void CLIENT_StopAction();

	/**
	*Define method
	*停止动作播放
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_StopFrontAction();

	/**
	*Define method
	*播放3d音效
	*
	*@param ActionId ，音效作ID（FString）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_OnPlay3DSound(const FString& SoundID);
	/**
	*Define method
	*停止3d音效
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_OnStop3DSound();
	/**
	*调用客户端方法播放连续动作
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void CLIENT_PlayOneByOneAction(const int32 &ContinuousId, TArray<FName>& ActionIds, TArray<FString>& ActionStartTimes);

	/**
	*设置模型的缩放
	*
	*@param newValue 新的值（float）
	*
	*@return 无
	*/
	virtual void SetModelScale(const float &newValue);

	/**
	*设置模型的缩放[缩放的对象是mesh，如镜头相关的的组件，在缩放过程中镜头就不会晃动]
	*
	*@param newValue 新的值（float）
	*
	*@return 无
	*/
	virtual void SetModelMeshScale(const float &newValue);

	/**
	*标志是否真确
	*
	*@param EntityFlag ，实体标志（ENTITY_FLAG）
	*@param Flags ，标志（int64）
	*
	*@return bool
	*/
	bool IsInFlags(ENTITY_FLAG EntityFlag, int64 Flags);

	/**
	*Define method
	*设置可见
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_ShowInvisible();

	/**
	*Define method
	*设置不可见
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_HideInvisible();

	/**
	*设置不播放移动动作
	*
	*
	*@return 无
	*/
	void SetForbidMoveAction(bool forbidMoveAction) { ForbidMoveAction_ = forbidMoveAction; }
	/**
	*是否禁止播放移动动作
	*
	*
	*@return 无
	*/
	bool IsForbidMoveAction() { return ForbidMoveAction_; }

	/**
	*Define method
	* 接受服务器粒子插槽数据
	*
	*@param EffectID 光效ID
	*@param SoltName 插槽名字
	*@param EffectScale 光效缩放
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_OnPlayParticles(const int32&  TargetID, const FString& EffectID, const FString& SoltName, float EffectScale, FVector Pos);

	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
		virtual void OnPlayParticles_P(const int32&  TargetID, const FString& EffectID, const FString& SoltName, float EffectScale, FVector Pos);

	/**
	*Define method
	* 接受服务器停止光效
	*
	*@param EffectID 光效ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_OnStopParticles();

	/**
	*Define method
	* 金丹显示头顶倒计时
	*
	*@param LifeTime 时长
	*@param TimerInterval 倒计时回调时间间隔
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_ShowTopCountDown(float LifeTime, float TimerInterval);
	/**
	*Define method
	* 金丹隐藏头顶倒计时
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_HideTopCountDown();

	/**
	*Define method
	* 改变模型大小
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_ChangeToDstModelScale(const float& ChangeTime, const float& ChangeModelScaleX, const float& ChangeModelScaleY, const float& ChangeModelScaleZ, const float& NormalModelScale);

	/**
	* 平滑模型大小
	*/
	void TickChangeToDstModelScale();

	/**
	*Define method
	* 还原模型大小
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_ChangeToNormalModelScale(const float& NormalTime, const float& NormalModelScale);

	/**
	* 平滑还原模型
	*/
	void TickChangeToNormalModelScale();

	void SetActorScale(FVector ModelScale);
	void OnsetActorScale();

	/**
	*Define method
	* 开始石化
	*@prama effectType 石化表现类型
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_CastToStone(float StoneSpeed, int32 effectType);
	void CastToStone(float StoneSpeed, int32 effectType);
	void DelayCastToStone(float StoneSpeed, int32 effectType);

	/**
	* 平滑石化
	*/
	void TickCastToStone();
	/**
	*Define method
	* 还原石化
	*@prama effectType 石化表现类型
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_CastToNormal(const float& NormalSpeed, const int32& effectType);

	/**
	* 平滑还原石化
	*/
	void TicCastToNormal();
	void SetActorStone(float Value);

	/**
	* 效果事件改变的通知
	*@prama bBegin     结束还是开始
		*@return 无
	*/
	void OnCastActorStone(bool bBegin);

	///关系改变：此entity影响关系的因素发生改变时，服务器调用此接口通知所有客户端刷新此entity相关功能
	UFUNCTION(BlueprintCallable, Category = "cs3|GameObjectInterface")
		void UpdateRelation();

	void ExecuteTweenModelScale();

	/**
	*Define method
	*绑定表现对象（mesh,光效等）
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_BindDisplayObject(const FString& AttachMeshID);


	/**
	*Define method
	*移除绑定表现对象（mesh,光效等）
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void CLIENT_UnbindDisplayObject(const FString& AttachMeshID);

	/**
	*变换动画蓝图、动作表
	*@param NewModelId 模型ID  ：由于目前的动作表是通过模型ID获取的，所以参数是模型ID
	*@param ActionId     入场动作
	*@param OutActionId  出场动作
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_ChangeShowAnimAndActionPosture(const FString& NewModelId, const FString& InActionId, const FString& OutActionId);

	/**
	*变换动作表
	*
	*@param NewModelId 模型ID  ：由于目前的动作表是通过模型ID获取的，所以参数是模型ID
	*@param ActionId     入场动作
	*@param OutActionId  出场动作
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_ChangeShowPosture(const FString& NewModelId,const FString& InActionId, const FString& OutActionId);

	virtual void InitBlueCB() override;

	void Set_prefixName(const FString& newVal, const FString& oldVal);

protected:
	virtual void onEnterWorld() override;       ///< Entity进入世界时，此方法被调用
	virtual void onLeaveWorld() override;       ///< 当Entity离开世界（被销毁时）时，此方法被调用

private:
	void StartChangeModel();///开始变身(变模型)

	///检查更换姿势(ChangeType 1:更换动画蓝图 + 动作表  2 : 更换动作表)
	void CheckChangePosAnim(int32 ChangeType, const FString& NewModelId, const FString& InActionId, const FString& OutActionId);
	void StartChangePosAnim();///开始换姿势(换动作表)
	
	void UpdateActorPosition();///更新Actor的位置(当模型、胶囊体有大小有变化调用)

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString	old_modelNumber;///<旧的模型大小

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString new_modelNumber;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 old_CollisionType;///<旧的碰撞器种类

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 old_SyncPosClient;

	bool bScaleTweenProcess = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool bUpdateModelScale = true;///引入变量控制是否同步模型放缩（用于解决CST-3928），等待服务器优化引擎同步BUG后可删除
private:
	///声音组件
	UPROPERTY()
		UCS3AudioComponent* AudioComponent;
	bool ForbidMoveAction_ = false;
	FTimerHandle PetScaleHandle;
	TArray<FString> extraModelNumberList;///<额外的模型编号缓存列表
	
	FTimerHandle ChangeScaleHandle;
	float TimeValue;///改变模型时间保存值 用于储存时间
	float ChangeSpeed = 0.0;///<改变模型大小速度
	FVector CurScaleVector = FVector(1.0f, 1.0f, 1.0f);///当前大小
	FVector DtsScaleVector = FVector(1.0f, 1.0f, 1.0f);///目标大小
	float ChangeScaleTick = 0.01;///<平滑改变模型的频率

	float BlendSpeed = 0.0;///<石化混合速度
	float BlendValue = 0.0;///<石化混合值
	float BlendMaxValue = 1.0f;///<石化混合的最大值
	FTimerHandle StoneHandle;
	float StoneTick = 0.01;///<平滑石化的频率
	FTimerHandle CheckStoneHandle;

	int32 CachePosChangeType;///<1:更换动画蓝图 + 动作表  2 : 更换动作表
	FString CachePosNewModelId;
	FName CachePosInActionId;
	FName CachePosOutActionId;

	int32 EffectType = -1;///<当前的效果类型

	UPROPERTY()
		FString extraModelNumber;
	UPROPERTY()
		FString old_extraModelNumber;

	FDelegateHandle ExtraModelHandle;
	FDelegateHandle StoneDelegateHandle;
	FDelegateHandle PosAnimHandle;
protected:
	int32 CurrentUID = -1;

};
