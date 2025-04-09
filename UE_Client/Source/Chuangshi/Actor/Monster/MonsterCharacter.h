#pragma once
#include "GameData/CS3Object.h"
#include "Entity/Monster/Monster.h"
#include "Actor/NPCBaseCharacter.h"
#include "GameData/CharacterData.h"
#include "BehaviorTree/BehaviorTree.h"
#include "Components/BoxComponent.h"
#include "Component/Monster/MonsterLadderMovementComponent.h"
#include "MonsterCharacter.generated.h"

/*
* 文件名称：MonsterCharacter.h
* 功能说明：怪物Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/

class UFilterActorComponent;
class UPhysicsFilterActorComponent;
class UAvatarFilterActorComponent;
class UDumbFilterActorComponent;
class UCurveFilterActorComponent;
class ULineToPointFilterActorComponent;
class UHitBackMoveFilterActorComponent;
class UMonsterPosSyncComponent;
class GameObject;
class UMonsterBlowFilterComponent;
class UMonsterFollowComponent;
class UCMonsterPosSyncComponent;
class UMonsterOptimizeComponent;
class UMonsterExtJDCYComponent;

/*
* 怪物Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AMonsterCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()

#pragma region	Avatar功能相关

public:

	//初始化
	virtual void InitFilterActorComponent() override;
	virtual void ChangeFilter(float moveSpeed, bool isIgnoreServerPos = false, FVector destPos = FVector::ZeroVector)override;
	virtual void ChangeCurveFilter(float Gravity, float UpTime, float XSpeed, FVector DstPos)override;
	virtual void ChangeDumbFilter()override;
	virtual void ChangeLineToPointFilter(float MoveSpeed, FVector DstPos, FRotator Rotator);
	virtual void ChangeHitBackMoveFilter(float MoveSpeed, FVector DestPos = FVector::ZeroVector);
	virtual void ChangeBlowFilter(const FVector& WindDir, const float& WindSpeed);

	virtual void ResetFilter()override;
	virtual void ResetFilterData()override;

	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };

	virtual void CreateAppearance()override;
	virtual void OnCreateModelOver()override;
public:
	UPhysicsFilterActorComponent* PhysicsFilter;
	UAvatarFilterActorComponent* AvatarFilter;
	UCurveFilterActorComponent* CurveFilter;
	UDumbFilterActorComponent* DumbFilter;
	ULineToPointFilterActorComponent* LineToPointFilter;
	UHitBackMoveFilterActorComponent* HitBackMoveFilter;

	UPROPERTY(BlueprintReadWrite)
		UMonsterPosSyncComponent* MonsterPosSyncComponent;
	UPROPERTY()
		UMonsterBlowFilterComponent* BlowFilterComponent;
	UPROPERTY()
		UMonsterFollowComponent* FollowFilterComponent;
	UPROPERTY()
		UMonsterExtJDCYComponent* MonsterExtJDCYComponent;

	UCMonsterPosSyncComponent* CMonsterPosSyncComponent;

	UMonsterOptimizeComponent* MonsterOptimizeComponent;

#pragma endregion
public:
	AMonsterCharacter();///<构造函数
	virtual void BeginPlay()override;
	/**
	*播放入场动作
	*
	*@param ActionId 动作Id(FName)
	*
	*@return 无
	*/
	void PlayAdmissionAction(FName ActionId);

	/**
	*播放入场动作完成回调
	*
	*@param Character 动作主体Actor(ACharacter*)
	*@param ActionId  动作Id(FName)
	*
	*@return 无
	*/
	void CallBackPlayAdmissionActionOver(ACharacter* Character, FACTION_DATA InActionData);

	virtual void CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap) override;
	void MonsterCharacterJumpStart(const TArray<FName>& Actions, const FString& EffectID);
	void CallBackMonsterJumpStartOver(ACharacter* Character, FACTION_DATA InActionData);
	void MonsterCharacterJumpEnd(bool IsCameraShake);
	void OnMonsterAppearJumpEnd(ACharacter* Character, FName ActionId);

	virtual void OnMoveOver( const uint32 movingID, const bool isSuccess );

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
	void NotifyCameraShake();///<跳跃结束播放震屏效果

	/**
	*Define method
	*BlueprintImplementableEvent，显示特殊进度条
	*
	*@param Text，文本(const FString&)
	*@param PersistTime，持续时间(const float&)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
	void OnShowSpecialProgressBP(const FString& Text, const float& PersistTime, const FString& iconName);

	/**
	*Define method
	*BlueprintImplementableEvent，隐藏特殊进度条
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
	void OnHideSpecialProgressBP();

	///离开光墙回调通知
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnLeaveFightAreaBP();

	///怪物头顶聊天泡泡
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void PlaySpeechBubble(const FString& VoiceID);

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void DeathDestructiveEffectBP();

	/**
	* 界面怪物施放技能显示引导条
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnShowMonsterIntonateBarBP(const int32 CasterID, const float HoldTime, const int32 SkillId);

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnHideMonsterIntonateBarBP(const int32 CasterID);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onClickCallBack();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void OnMonsterAppearLineToPoint();

	void MonsterCharacterJumpWithoutMoveStart(const TArray<FName>& Actions, const FString& EffectID, float Time);
	void CallBackMonsterJumpWithoutStartOver(ACharacter* Character, FACTION_DATA InActionData);
	void MonsterCharacterJumpWithoutMoveEnd();
	void CallBackMonsterJumpWithoutEndOver(ACharacter* Character, FACTION_DATA InActionData);

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnMonsterBootyOwnerChangedBP();

	virtual void SetInitAction() override;///<重写SetInitAction
	virtual void PlayDeadEffect() override;

	virtual void OnEnterFightState()override;///<进入战斗状态
	virtual void OnEnterDeadState() override;
	virtual void OnExitDeadState() override;
	virtual void OnEnterShowState() override;
	virtual void OnExitShowState() override;
	virtual void OnEnterResetState() override;
	virtual void OnExitResetState() override;
	virtual void OnEnterFreeState()override;///<进入空闲状态
	virtual void OnExitFightState()override;///<退出战斗状态
	virtual void OnEnterWarnState();///<进入警戒状态
	virtual void OnExitWarnState();///<退出警戒状态

	//UFUNCTION(BlueprintPure, Category = "Game|Monster")
	virtual int32 GetFinalCamp();///<获取最终阵营

	virtual void UpdateRelation_Implementation() override;
	virtual float GetMoveSpeed() override;
	virtual void InitCharacterComponent() override;
	//初始化位置同步组件
	void InitPosSyncComponent();
	virtual bool IsMoveing();///是否正在移动中
	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void CELL_MonsterFloorFalling();
	virtual void EndHitBack();

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void ChasePlayer(float distance);

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void OnChasePlayer();

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void OnLeftMouseClicked();

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void OnActorBeginCursorOver();

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void OnActorEndCursorOver();

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void SetHitMaterial();

	UFUNCTION(BlueprintCallable, Category = "Game|Monster")
		void CreateHitMaterial();
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void BP_OnBaseChange();

	/**
	* 抖动表现
	*
	*@param Peak 波峰
	*@param ShakeTime 抖动时间（最长10秒）
	*
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void BP_OnPictureScrollShake(const float& Peak, const float& ShakeTime);

	/**
	* 开启高亮描边
	*
	*@param Color 描边颜色
	*@param BoundWidth 描边厚度
	@param Time 显示时间
	*
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void BP_OnActivateOutLine(const FVector& Color, const int32& BoundWidth, const float& Time);
	///< 关闭高亮描边
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void BP_OnDeactivateOutLine();

	/**
	*Define method
	*BlueprintImplementableEvent，显示头顶倒计时
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
	void ShowRemainLifeTime(const float & remainTime);

	virtual void GossipWith() override;///<重写GossipWith

	void EndBlow();

	/*-------------------云梯相关-------------------------------------*/
	UFUNCTION()
		void OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp,
			int32 OtherBodyIndex, bool bFromSweep, const FHitResult& OverlapInfo);

	UFUNCTION()
		virtual void OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* Other,
			UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

	void EntityEnterLadder(int32 EnterEntityID);//Entity对象进入云梯区域
	void EntityExitLadder(int32 EnterEntityID);//Entity对象离开云梯区域
	void NofityAllCharacterFallOutToLadder();//通知将所有对象从梯子上掉下去

	FVector GetLadderBottomLocation();//获取云梯底部位置
	FVector GetLadderTopLocation();//获取云梯顶部位置
	FVector GetOtherActorLadderTopLocation();//获取云梯顶部位置
	FVector GetEnterLadderTopLocation();//获取进入云梯(最顶端)顶部位置
	FRotator GetLadderBottomRotation();//获取云梯底部角度值
	FRotator GetLadderTopRotation();//获取云梯顶部角度值
	TArray<int32> GetLadderAllEntityList();//获取云梯上所有Entity对象

	void InitLadderData(AMonsterCharacter *LadderCharacter);//AI怪物初始化梯子相关组件（当进入攻城战副本时）
	void ClearLadderData();//AI怪物清理梯子相关组件（当退出攻城战副本时）
	/*-------------------云梯相关-------------------------------------*/

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual FString GetEntityUName() override;///<重写GetEntityUName
	virtual bool IsEntityMoveType(MOVETYPE MoveType) override;///<重写IsEntityMoveType
	virtual bool IsEntityBoss() override;///<重写IsEntityBoss
	void BaseChange() override;///<重写BaseChange

private:
	void StopMonsterJumpEffect();///<结束出场光效
	void OnNotifyActionChangeFinish(FACTION_DATA ActionData);
	void UpdateFenShengWeaponState();///<根据玩家状态更新分身怪的武器状态

private:
	
	FActionOverDelegate StartJumpDelegate;
	bool IsJumpEnd;
	bool IsForceStopIump;

	FName JumpStartAction;
	FName JumpProcessAction;
	FName JumpEndAction;
	float LoopTime;

	///怪物出场光效
	UPROPERTY()
	//AEffectEmitter* MonsterJumpEffect;

	int32 MonsterJumpEffectUID = -1;
	bool bIsChasePlayer = false;
	float ChaseDistance = 0.0;
	
public:
	UPROPERTY(BlueprintReadWrite)
		bool bIsCursorOver = false;

	UPROPERTY(EditAnywhere, Category = BehaviorTree)
		ENTITY_TYPE_EXT EntityTypeExt;

	FVector SpawnPosition = FVector::ZeroVector; //出生位置用于MonsterAIComponent回走

	//怪物小地图标记是否闪烁
	bool isTwinkle = false;
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnGangQiChanged( const int& curGangQi, const int& maxGangQi );///<怪物gangqi改变通知蓝图
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnGangQiStateChanged( const int& gangQiState );///<怪物gangqistate改变通知蓝图
		
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnHPChanged( const int& HP, const int& HP_Max );///<怪物血量改变通知蓝图
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnCampChanged(const int& camp );///<怪物阵营改变通知蓝图
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnTempCampChanged(const int& tempCamp );///<怪物临时阵营改变通知蓝图
		
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Monster")
		void OnGangQiProgressChanged( const int& qangQIProcess,  const int& maxGangQi);
		
	//======================云梯=====================
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UBoxComponent* TriggerBox;///<碰撞盒

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USceneComponent* Bottom;///<玩家站于梯子时的梯子底部定位器 

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USceneComponent* Top;///<玩家站于梯子时的梯子顶部定位器

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USceneComponent* OtherActorTop;///<其他对象站于梯子时的梯子顶部定位器

	UPROPERTY(BlueprintReadOnly)
		UMonsterLadderMovementComponent* MonsterLadderMovementCpt;//怪物攀爬云梯组件

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		int32 CharacterLadderNum = 4;///<人物长度相当于几节梯子比值

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		float LeaveTopOffsetZ = 0.0f;///<人物顶部离开偏移量

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		int32 StepCount = 48;///<梯子的数量

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		float StepHeight = 50.0f;///<梯子的步长

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		float LadderPitchValue = 10.0f;///<云梯倾斜角度

	TArray<AServerCharacter *> LadderCharacterList;///<云梯上所有的对象

	bool IsEnableCollisionTriggerBox;///<是否开始碰撞盒检测
	//======================云梯=====================


	//======================行为树相关=====================
	UPROPERTY(EditAnywhere, Category = BehaviorTree)
		UBehaviorTree* AIBehaviorTree;
	//======================行为树相关=====================
};