#pragma once
#include "CoreMinimal.h"
#include "KBEngine.h"
#include "GameData/CharacterData.h"
#include "GameFramework/Character.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3GameViewportClient.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Scene3DComponent.h"
#include "GameData/ModifyFaceData.h"
#include "GameData/ModelPartData.h"
#include "GameData/RoleJumpData.h"
#include "GameplayTagContainer.h"
#include "GameCharacter.generated.h"

/*
* 文件名称：GameCharacter.h
* 功能说明：客户端Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/


class UAppearanceComponent;
class UCollisionComponent;
class UPerformanceComponent;
class UActorTraceMoveComponent;

/*
* 客户端Character基类
*/
DECLARE_DELEGATE(FCreateModelOverDelegate);///模型创建完毕通知
DECLARE_MULTICAST_DELEGATE(FModelChangeAppearanceOverDelegate);///模型改变外观完毕通知

DECLARE_STATS_GROUP(TEXT("AGameCharacter"), STATGROUP_AGameCharacter, STATCAT_Advanced);

class UBaseAnimInstance;
UCLASS(abstract)
class CHUANGSHI_API AGameCharacter : public ACharacter
{
	GENERATED_BODY()
public:
	AGameCharacter();
	virtual void BeginPlay() override;
	virtual void PostInitProperties() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void Destroyed() override;///<重写Destroyed
	virtual void BeginDestroy() override;
	virtual KBEngine::Entity* GetSelfEntity() const;///<获得Actor绑定的Entity

	/*-------------------动作相关-------------------------------------*/
	/**
	*播放动作接口
	*
	*@param InActionId			动作Id(FName)
	*@param InStartPostion		起始位置(float)
	*@param InActionOverDelegate	动作结束回调(FActionOverDelegate)
	*
	*@return 无
	*/
	virtual void PlayAction(FName InActionId, float InStartPostion = 0.0f, 
		const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate(),
		const FActionBlendOutDelegate& InActionBlendOutDelegate = FActionBlendOutDelegate());

	/**
	*播放连续动作接口
	*
	*@param InContinuousId		连续动作ID(int32)
	*@param InActionIds		    连续动作ID数组列表
	*@param InActionStartTimes		    连续动作起始时间数组列表
	*@param InActionOverDelegate	动作结束回调(FActionOverDelegate)
	*
	*@return 无
	*/
	void PlayContinuousActions(int32 InContinuousId, TArray<FName>& InActionIds, TArray<float>& InActionStartTimes,
		const FActionContinuousOverDelegate& InActionOverDelegate = FActionContinuousOverDelegate());
	
	/**
	*停止播放动作
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void StopAction();
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void StopFrontAction();///停止播放前景动作 注:此接口只供GM调用
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void StopActionById(FName ActionId);///停止指定播放的动作
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void StopContinuousAction(int32 InContinuousId);///停止指定播放的动作
	
	virtual void SetInitAction();///<设置初始动作Id
	FName GetInitActionId();///<获得初始动作Id

	virtual bool IsCanPlayAction();///<是否能播放动作

	///检查隐藏部件的动作
	void CheckPartHideByAction(FACTION_DATA ActionData);
	///隐藏Character上某个部件
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		virtual void SetMeshPartHiddenInGame(MODEL_PART_TYPE MeshPartType, bool IsHiddenInGame);
	/*-------------------动作相关-------------------------------------*/

	/*----------------绑定表现对象功能相关---------------------------*/
	UFUNCTION(BlueprintCallable)
		bool IsBindMeshState();
	UFUNCTION(BlueprintCallable)
		void BindMesh(FName AttachMeshID);
	UFUNCTION(BlueprintCallable)
		void UnBindMesh(FName AttachMeshID);
	/*----------------绑定表现对象功能相关---------------------------*/

	/*----------------对象移动组件功能相关---------------------------*/
	void SetBaseGravityScale(float InGravityScaleValue);///设置重力缩放系数的基础值(重力系数=系数基础值*(系数百分比值+1)+系数固增益值)
	void SetGravityScale(float InGravityScale);///设置重力缩放系数
	float GetGravityScale();///获取重力缩放系数
	
	void SetAnimRate(float InRate);///设置动画播放速率
	void SetBrakingDecelerationFalling(float InBrakingDecelerationFalling);///设置横向摩擦力
	void SetMaxWalkSpeed(float InMaxWalkSpeed);///设置水平X速度
	
	void SetCharacterMoveCacheData();///设置玩家移动组件的缓存数据
	FORCEINLINE const FCHARACTER_MOVE_CACHE_DATA& GetCharacterMoveCacheData() { return CharacterMoveCacheData; }

	virtual bool IsMoveing();///是否正在移动中
	virtual bool IsActiveMoveing();///是否主动移动中（不包括击飞相关的位移）
	virtual float GetMoveSpeed();///获取移动速度（主要用于混合动作用[1.3.6.9.12]）
	virtual bool IsLadderMovement();///是否爬梯模式中

	TSharedPtr<FMODEL_DATA> GetCurModelData();///<当前模型数据
	/*----------------对象移动组件功能相关---------------------------*/

	/*----------------对象外观组件功能相关---------------------------*/
	void CheckCreateDynamicPartCpt(FString NewModelId);///检查是否要动态new创建部件组件[怪物使用玩家模型ID时 如:/clone 20000859]

	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void SetCurModifyFaceData();///设置当前脸部数据
	void setIsHitMaterialCreated(bool BValue) { IsHitMaterialCreated = BValue; }

	virtual void CreateAppearance();
	virtual void OnCreateModelOver();
	virtual void OnCreateApperanceOver();
	virtual void OnChangePartOver();
	virtual void CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap);

	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
		void OnBPCreateApprearanceOver();///<创建完毕角色给蓝图回调

	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void ChangeModelPart(MODEL_PART_TYPE InPos, FString PartID);///<改变模型外观的部件

	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		const TMap<MODEL_PART_TYPE, UMeshComponent *>& GetMeshPartComponentDatas()const { return MeshPartComponentDatas; };///<获取所有部件组件
	
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		class UMeshComponent* GetPartMeshComponent(MODEL_PART_TYPE PartType);///<获取对PartType应部件组件

	virtual FName GetWeaponSockName(bool IsLeft);///获取武器的插槽位置
	bool GetApperanceLoadingOver();///是否模型加载完毕
	class UAppearanceComponent* GetAppearanceComponent() const;///<外观组件
	class UCollisionComponent* GetCollisionComponent() const;///<碰撞组件
	class UPerformanceComponent* GetPerformanceComponent() const;///<碰撞组件
	
	/*----------------对象外观组件功能相关---------------------------*/

	/*----------------环身功能相关---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void ChangeBodyLightEffect(FString EffectId);///<改变环身光效

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		virtual void PreviewBodyLightEffect(FString EffectId) {};///<商城预览改变环身光效

	virtual void CheckBodyLightEffect() {};///环身光效发身改变
	/*----------------环身功能相关---------------------------*/

	virtual void UpdateCapsuleComponent();
	virtual void UpdateActorPositionToGround();///统一更新贴地面位置的接口（以后设置位置需全部整合到这里，否则对象的位置太难管理了）
	virtual void UpdateActionPosition(FVector NewPosition);///统一更新位置接口（直接设置，不检测地面）
	virtual void UpdateActorDirection(FRotator NewRotation);///统一更新朝向的接口（直接设置）
	virtual void UpdateOtherCptPosition() {};///更新Character上其它组件及UI的位置

	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		virtual void InitScene3DUIComponent();///初始化头顶ui组件
	///动态修改头顶ui位置方法 
	///jira : CST-5711
	UFUNCTION(BlueprintCallable, Category = "Game")
	void BP_AdjustHeadUIPositionHuman();

	///超出界限像素  https://docs.unrealengine.com/en-us/Engine/Performance/Visualizers/OutOfBoundsPixels
	void PixelsBeyondBounds();	

	void SetOpenScene3DUI(const bool& IsOpen);
	virtual void ReSetOpenScen3DUI();

	TAsyncLoadPriority GetLoadPriority();

	// 获取当前对象的包围盒大小,用于在重要度更新中判断屏幕占比
	virtual float GetBoundRadius();

	// Significance变化事件,在UCS3GameViewportClient::Tick的重要度整体后处理中触发（可以在这里处理一些LOD优化性能）
	virtual void OnSignificanceChange();

	// 如果当前对象重要度达到目标重要度就返回true
	bool IsShowEffect(const SignificanceType TargetSignificance);

	// 统一设置组件的Tick间隔,这个函数主要用来给子类重写,方便在AGameCharacter::OnSignificanceChange()中统一调用
	virtual void SetGameCharacterTickInterval(float TickInterval);

	void SetBaseAnimInstance(UBaseAnimInstance* InAnimInstance);
	UBaseAnimInstance* GetBaseAnimInstance();

	/*----------------对象外观透明相关---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		virtual void SetGameCharacterAlpha(float InAlpha);

	//经过多长时间从不透明变成全透明
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		virtual void SetGameCharacterFadeOut(float InPeriodOfTime);

	//经过多长时间从透明变成不透明
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		virtual void SetGameCharacterDisplay(float InPeriodOfTime);


protected:
	virtual void CreateBaseMesh();///创建基础mesh组件
	virtual void CreateRoleMesh();///创建玩家mesh组件
	virtual void CreateDynamicRoleMesh();///创建动态玩家mesh组件
	void SetSkeletalMeshCptBaseProperty(USkeletalMeshComponent* PartCpt, FString Socket = "");
	void SetStaticMeshCptBaseProperty(UStaticMeshComponent* PartCpt, FString Socket = "");

	virtual void InitBaseComponent();///<初始化组件

	virtual void InitMovementComponent();

	virtual void InitCapsuleComponent();
	
	virtual void InitCollisionComponent();

	virtual void InitPerformanceComponent();

	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		virtual void SetMeshMasterPoseComponent();///<设置部件是否与主mesh共享骨骼

	virtual void SynchronousMeshTick();///<同步子mesh与主mesh的Tick

private:

	UPROPERTY()
		UBaseAnimInstance* BaseAnimInstance;///<动作状态机

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UScene3DUIComponent* HeadInfo3DUI;///<头顶3DUI

	UPROPERTY(Transient, BlueprintReadOnly)
		UAppearanceComponent* AppearanceComponent;///<外观组件

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		UCollisionComponent* CollisionComponent;///<碰撞组件

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		UPerformanceComponent* PerformanceComponent;///<表现组件

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		UActorTraceMoveComponent* ActorTraceMoveComponent;///跟随移动组件
	
	UPROPERTY(BlueprintReadOnly, Category = "GameCharacter")
		TMap<ACTION_POSE_ENUM, FACTION_DATA> ActionDatas;///<动作数据

	UPROPERTY(BlueprintReadOnly, Category = "GameCharacter")
		TArray<FACTION_DATA> RandomActionDatas;///<随机动作数据

	UPROPERTY(EditAnywhere,BlueprintReadWrite, Category = "GameCharacter")
		TArray<FMODIFY_FACE_DATA> ModifyFaceDatas;///<模型捏脸数据

	UPROPERTY(EditAnywhere,BlueprintReadWrite, Category = "GameCharacter")
		FFACE_STYLE_DATA FaceStyleDatas;///脸部样式数据

	FCreateModelOverDelegate OnBroadCreateModelOver;///<模型创建完毕
	FModelChangeAppearanceOverDelegate OnModelChangeAppearanceOverDelegate;///<模型改变外观完毕

	// 所有Gameplay标记,用于给其他功能提供各种查询判断
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "GameCharacter")
	FGameplayTagContainer GameplayTagContainer;

	bool bIsCreateRoleMesh = false;///是否已创建人物部件
	bool bIsClient = false;
	bool bIsChangeAppearanceling = false;///是否在改变模型外观过程中
	float ClientMoveSpeed = 0.0f;///纯单击对象移动速度
	float ClientFilterSpeed = 0.0f;///纯单击对象移动的向量
	float GravityScaleBase = 5.0f;///重力基础值系数
	float GravityScalePercentage = 0.0f;///重力缩放系数百分比
	float GravityScaleAddFixed = 0.0f;///重力缩放系统固定增益值
	FCHARACTER_MOVE_CACHE_DATA CharacterMoveCacheData;///玩家移动组件的缓存数据
	
	UPROPERTY(BlueprintReadWrite)
		int32 ProfessionID;///<角色职业

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<VISIBLE_RULE> VisibleRules;///<模型显示规则
	UPROPERTY(BlueprintReadWrite)
		VISIBLE_STYLE VisibleStyle;///<当前的模型显示样式
	UPROPERTY(BlueprintReadWrite, VisibleAnywhere)
		FName CharacterClassName = TEXT("");///<Character当前标识
	//骨骼数量,判定服务器资源是否完成配置加载。
	int BonesNum;
	//HeadSocket位置
	FVector SocketHeadPos;
	bool bIsGetBone = false;
	bool isStarScene3D = false;

	bool IsLockChangeWeaponSlotNotify = false;///<是否锁定切换武器插槽通知(用于锁定优先级：动作通知上添加武器从右手切换到左手)

	// 当前对象的重要度
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "GameCharacter")
		SignificanceType Significance = SignificanceType::Complete;
	// 上一帧的值,主要用于判断是否需要出发Significance变化事件
	SignificanceType OldSignificance = SignificanceType::Complete;

protected:
	///=========================模型基础部件===========================
	UPROPERTY(Transient)
		TMap<MODEL_PART_TYPE, UMeshComponent *> MeshPartComponentDatas;///<所有部件组件数组

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Heads;///<头部

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Suits;///<套装

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Hair;///<头发 

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Adorn;///<发饰

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_HeadAdorn;///<头饰

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_FaceAdorn;///<面饰

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_BackAdorn;///<背饰

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_WristAdorn;///<腰饰

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Hat;///<帽子

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Coats;///<衣服

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Wrist;///<护腕

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Gloves;///<手套

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Belt;///<腰带

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Necklace;///<项链

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_L_RING;///<左手戒指

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_R_RING;///<右手戒指

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Pants;///<裤子

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Shoes;///<鞋子

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SKMesh_Cloak;///<披风

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UStaticMeshComponent* STMesh_LHweapon;///<左手武器

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UStaticMeshComponent* STMesh_RHweapon;///<右手武器

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UStaticMeshComponent* STMesh_DefaultStatic;///<默认静态组件

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* STMesh_S_LHweapon;///<左手骨架武器

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* STMesh_S_RHweapon;///<右手骨架武器
	///=========================模型基础部件===========================

	bool OpenScene3DUI = false;///当前类型是否需要HeadUI

	FName InitActionId;///<初始动作Id

	UPROPERTY(BlueprintReadWrite)
		bool IsHitMaterialCreated;///<是否创建受击材质

	FString PreviewBodyLightEffectID;///<商城中预览的环身光效ID
	int32 BodyLightEffectUID;///<环身光效UID

private:
	bool IsApperanceLoadingOver;///<是否模型加载完毕	
	bool bIsBindMeshState = false;///<是否绑定表现对象状态
	FDelegateHandle PlayActionHandle;
	FDelegateHandle PlayContinuousActionsHandle;

	UPROPERTY(Transient)
		TMap<FName, UMeshComponent *> BindMeshComponentDatas;///<绑定的mesh组件

	UPROPERTY(Transient)
		TMap<FName, int32> BindMeshEffectUID;///<抱起的光效UID
};

FORCEINLINE UAppearanceComponent* AGameCharacter::GetAppearanceComponent() const { return AppearanceComponent; }
FORCEINLINE UCollisionComponent* AGameCharacter::GetCollisionComponent() const { return CollisionComponent; }
FORCEINLINE UPerformanceComponent* AGameCharacter::GetPerformanceComponent() const { return PerformanceComponent; }