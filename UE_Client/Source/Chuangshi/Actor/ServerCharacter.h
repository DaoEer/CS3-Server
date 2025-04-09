#pragma once

#include "Components/AudioComponent.h"
#include "Actor/GameCharacter.h"
#include "GameData/ModelPartData.h"
#include "GameData/EnumCsvDefine.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Skill/SkillData.h"
#include "Entity/Alias.h"
#include "GameData/CharacterData.h"
#include "Component/CS3AudioComponent.h"
#include "GameData/EntityDataCache.h"
#include "ServerCharacter.generated.h"

/*
* 文件名称：ServerCharacter.h
* 功能说明：服务器entity对应的客户端Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/

DECLARE_STATS_GROUP(TEXT("AServerCharacter"), STATGROUP_AServerCharacter, STATCAT_Advanced);

//缓存地面查询结果
struct FGroundLocationCacheInfo
{
	float time;
	float location_Z;
	FGroundLocationCacheInfo(float time = 0.f, float location_Z = 0.f) :time(time), location_Z(location_Z) {}
};

UENUM(BlueprintType)
enum class CS3SeverCharacterStatus : uint8
{
	ActorSpawn = 0,				///已创建好Actor
	BindedEntity,			///绑定了Entity
	ComponentCreateFinished,///组件创建好
	AppearanceCreateFinished,///外观创建好
	UnBindedEntity			///解绑Entity
};

class GameObject;
class UFightComponent;
class UFilterActorComponent;
class UCS3EntityInterface;

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FActorCreateFinishDelegate);///ACTOR创建完毕
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FActorVisibleChangedDelegate);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FDeadActionPlayOverDelegate);///死亡动作播放完毕代理
DECLARE_MULTICAST_DELEGATE(FSkillWeaponeBindObjDelegate);///技能时武器绑定对象
/*
* 服务器entity对应的客户端Character基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API AServerCharacter : public AGameCharacter
{
	GENERATED_BODY()

#pragma region	Avatar功能相关

public:

	virtual void OnGotParentEntity();
	virtual void OnLoseParentEntity();

	//初始化
	virtual void InitFilterActorComponent();
	virtual void SetPosition(const FVector& newVal, int32 parentID = 0);
	virtual void SetDirection(const FVector& newVal, int32 parentID = 0);
	virtual void onUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID = 0);
	virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID = 0);
	virtual void OnPositionSet(const FVector& newVal) { }
	virtual void SetMoveSpeed() { }
	virtual void ChangeFilter(float moveSpeed, bool isIgnoreServerPos = false, FVector destPos = FVector::ZeroVector) {};
	virtual void ChangeCurveFilter(float Gravity, float UpTime, float XSpeed, FVector DstPos) {};
	virtual void ChangeDumbFilter() {};
	virtual void ChangeHitBackMoveFilter(float moveSpeed, FVector destPos = FVector::ZeroVector) {};
	virtual void ChangeBlowFilter(const FVector& WindDir, const float& WindSpeed) {};
	virtual void EndHitBack() {};
	virtual void ResetFilter() {};
	virtual void ResetFilterData() {};

	void OnFilterSpeedChanged(float speed);
	///设置FilterActorComponent
	FORCEINLINE void SetFilterComponent(UFilterActorComponent* _comp)
	{
		MFilterComponent = _comp;
	}

	///获取FilterActorComponent
	FORCEINLINE UFilterActorComponent* GetFilterComponent()
	{
		return MFilterComponent;
	}

	void SetEnableSyncServerPos(bool IsEnable);

protected:
	UFilterActorComponent* MFilterComponent = nullptr;
	float FilterSpeed = 0.0;
#pragma endregion

public:
	virtual void SetGameCharacterTickInterval(float TickInterval) override;

public:
	AServerCharacter();///<构造函数

	virtual void BeginPlay() override;///重写BeginPlay
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason)override;
	virtual void BeginDestroy() override;///<重写Destroyed
	inline bool IsInitialized() const { return bInitialized; }///<Actor是否已经创建
	void SetInitialized(bool Initialized);
	virtual void OnInitialized();
	virtual void CreateAppearance()override;
	virtual void OnCreateModelOver()override;
	virtual void OnCreateApperanceOver()override;
	virtual void OnChangePartOver()override;
	virtual void OnUnBindActorCallBack();///entity与Actor关系解除绑定回调时的回调

	/**
	*Actor绑定ID
	*
	*@param Entity 客户端ID
	*
	*@return 无
	*/
	virtual void BindLinkEntity(KBEngine::Entity* Entity);

	virtual void OnBindToEntity();

	virtual void InitCharacterComponent();
	
	virtual KBEngine::Entity* GetSelfEntity() const override;///<重写获得Actor绑定的Entity方法

	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
		void BindActorToEntityBP();///<Entity绑定Actor蓝图回调
	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
		void UnBindActorToEntityBP();///<Entity解绑Actor蓝图回调

	void InitCharacterPosAndDirection();///注:为了统一，此函数后面建议替换UpdateActorPositionToGround()和UpdateActorDirection
	virtual void UpdateActorPositionToGround() override;

	///用Entity的位置检测地面获取地面坐标
	FVector GetGroundPositionByEntity();
	///用Actor的高度值位置检测地面获取地面坐标
	FVector GetGroundPosition();

	///射线查询地面获取位置
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter")
	FVector FloorTrace(const FVector &Vector, bool bForce = false);
	//从Character当前位置朝目标位置移动一定距离（检测碰撞）
	void SetCharacterMovePosition(const float& MoveDistance, const FVector& TargetLocation, bool bAbsolute = true, bool bSweep = false);
	FVector GetModelScaleRevisePos(const FVector &OriginalPosition);

	void ShowInvisible();///<强制可见
	void HideInvisible();///<取消强制可见

	/*----------------状态功能块-------------------------------*/
	virtual void OnEnterDeadState();///<进入死亡状态
	virtual void OnExitDeadState();///<退出死亡状态

	virtual void OnEnterFreeState();///<进入空闲状态
	virtual void OnExitFreeState() {};///<退出空闲状态

	virtual void OnEnterWarnState();///<进入警戒状态
	virtual void OnExitWarnState() {};///<退出警戒状态

	virtual void OnEnterFightState();///<进入战斗状态
	virtual void OnExitFightState();///<退出战斗状态

	virtual void OnEnterShowState() {};///<进入表演状态
	virtual void OnExitShowState() {};///<退出表演状态

	virtual void OnEnterResetState() {};///<进入重置状态
	virtual void OnExitResetState() {};///<退出重置状态

	void OnEnterEffectState(EFFECT_STATE EffectState);///进入效果状态
	void OnExitEffectState(EFFECT_STATE EffectState);///退出效果状态
	
	///是否正在某个状态
	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
		bool IsState(ENTITY_STATE EntityState);
	bool IsInPending();	//判断entity是不是处在准备状态
	///是否处于变身状态
	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
		bool IsChangeModelState();

	virtual bool IsMoveing()override;
	virtual bool IsActiveMoveing()override;
	/*----------------状态功能块-------------------------------*/


	virtual void GossipWith() {};///<对话接口
	virtual void PlayDeadEffect() {};
	virtual void PlayDeadMortuaryEffect();

	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
	void PlayDeadMortuaryEffectBP();///<BlueprintPure 获得Filter速度

	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	FString GetUname();///<BlueprintPure 获得Entity名字

	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	virtual float GetFilterSpeed();///<BlueprintPure 获得Filter速度

	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	virtual int32 GetFinalCamp();///<获取最终阵营

	/**
	*BlueprintPure 是否有某个标志位
	*
	*@param EntityFlag 标志位(ENTITY_FLAG)
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	bool HasFlag(ENTITY_FLAG EntityFlag);

	/**
	*BlueprintPure 是否正在某个移动类型
	*
	*@param MoveType 移动类型(MOVETYPE)
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	bool IsMoveType(MOVETYPE MoveType);

	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	bool IsBoss();///<BlueprintPure 是否是精英怪

	/**
	* 是否是玩家自己（本地客户端）
	*
	* @retrurn bool
	*/
	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
		bool ActorIsPlayer();


	/**
	*BlueprintPure 获取与Actor关系类型
	*
	*@param Actor 目标Actor(AActor*)
	*
	*@return COMBAT_RELATION 关系类型
	*/
	UFUNCTION(BlueprintPure, Category = "ServerCharacter")
	COMBAT_RELATION QueryRelation(AActor* Actor);

	UFUNCTION(BlueprintNativeEvent, BlueprintPure, Category = "ServerCharacter")
	bool CanGossipWith();///<是否可交互
	virtual bool CanGossipWith_Implementation();

	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
	void OnFlagsChanged();///<标志位改变通知蓝图
	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
	void ClearTargetActor();///<失去选中目标通知蓝图
	//改变前缀通知
	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
	void onPrefixNameChange(const FString& prefixName);


	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "ServerCharacter")
	void UpdateRelation();///<关系改变通知蓝图
	virtual void UpdateRelation_Implementation();
	///<怪物名字血条脚底光圈颜色改变(AppearanceColor 0:不改变颜色，1:绿色，2:红色)
	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
	void OnAppearanceColorChanged(const int32 &AppearanceColor);///<Entity绑定Actor蓝图回调

	class UFightComponent* GetFightComponent() const;///<获取战斗组件

	void SetEffectDynamicData(FString SlotName,float EffectScale,FVector pos);//设置AI设置的动态粒子数据(单位m)
	void GetEffectDynamicData(FString SlotName, FTransform EffectTrans);//获取AI设置的动态粒子数据(单位m)

	/** Event fired when the actor enter world */
	UFUNCTION(BlueprintNativeEvent, Category = "ServerCharacter")
		void OnActorCreaterFinish();

	/** Remove dynamic OnActorCreaterFinish */
	void RemoveOnActorCreaterFinishBind();
	///获取脚印列表信息
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter")
		UMaterialInstance* GetFootPrintData(TEnumAsByte<EPhysicalSurface> SurfaceType, FString EntityName, bool LeftORRight);

	/**
	*BlueprintCallable 开启上升力
	*
	*@param speed 速度
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter")
		void OpenUpForce(const float& speed);

	/**
	*BlueprintCallable 关闭上升力
	*
	*@param hitTime 时间
	*@param speed 速度
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter")
		void CloseUpForce();

	/**
	*OnSetModelScale
	* @brief 设置模型缩放给蓝图的回调事件
	* @param const float & newValue
	* @return void
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
		void OnBpSetModelScale(const float &newValue);

	/// 设置自定义模板值
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter")
		void SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL StancilValue);

	// 获取缓存的entity接口,效率比UGolbalBPFunctionLibrary::GetInterfaceByName高
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter|EntityDataCache")
		FEntityInterface_Cache& GetEntityInterface_Cache();

	// 获取entity接口
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter|EntityInterface")
		UCS3EntityInterface *GetInterfaceByName(const FString& name);

	// 获取entity数据
	UFUNCTION(BlueprintCallable, Category = "ServerCharacter|EntityInterface")
		FString GetEntityPropertyValue(const FString& name);




	/**
	*显示模型狂暴效果
	*
	*@param LinearColor	 颜色
	*
	*@return FVector 坐标
	*/
	void OnShowRageEffect(FLinearColor &LinearColor);
	void OnEndRageEffect();

	/**
	* 改变模型对应的动作表
	* @param InActionConfigPath 动作表资源路径
	*
	*/
	void ChangeAnimAction(TSoftClassPtr<UAnimInstance> InAnimationPath, TSoftObjectPtr<UDataTable> InActionConfigPath, 
		FName OutActionId = "None", FName InActionId = "None");
	virtual bool IsCanPlayAction()override;

	/*----------------链条绑定mesh、光效功能相关---------------------------*/
	void BindObjToPartSlot(FPART_SLOT_BIND_OBJ_DATA &InWeaponBindObj);///绑定对象到武器中【用于链刃职业】
	void RemovePartSlotBindObj(int32 InBindId);///删除指定的武器绑定对象【用于链刃职业】
	void RemoveAllPartSlotBindObj();///删除所有的武器绑定对象【用于链刃职业】

	/*----------------模型创建数据功能相关---------------------------*/
	virtual FName GetWeaponSockName(bool IsLeft) override;///获取武器的插槽位置
	
	void SetSeverCharacterStatus(CS3SeverCharacterStatus NewStatus) { CurStatus = NewStatus; };
	CS3SeverCharacterStatus GetSeverCharacterStatus() { return CurStatus; };

	virtual void UpdateOtherCptPosition() override;///更新Character上其它组件及UI的位置

	bool IsMoveFlying();

	virtual FString GetEntityUName();///<获取Entity名字
	virtual bool IsEntityMoveType(MOVETYPE MoveType);///<Entity移动类型
	virtual bool IsEntityBoss();///<Entity是否是精英怪
	virtual void InitBaseComponent();///<初始化组件

	/*-------------------其他------------------------*/
	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter|HeadInfo3DUI")
		void OnUpdateHeadInfo3DUIBP(bool IsFar);///更新头顶图标（用于勇闯绝命岛 CST-13806）
	
private:
	void OnPlayDeadActionOver(ACharacter *GameCharacter, FACTION_DATA InActionData);

	void ResetBindObjToPartSlot(FPART_SLOT_BIND_OBJ_DATA &InWeaponBindObj);

	void SetHeadInfo3DUIVisible(); ///设置头顶信息界面可见性
	
public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
	int32 EntityId = 0;///<EntityId

	UPROPERTY(BlueprintReadWrite)
	bool bIsPlayDeadEffect = false;///<是否已经播放死亡特效

	UPROPERTY(BlueprintReadWrite)
	bool bIsShowInvisible = false;///<正在强制显示

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
	UFightComponent* FightComponent;///<战斗组件

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
	UAudioComponent* SkillCastAudioComponent;///<当前技能释放音效组件
	
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
	TMap<int32, UHoldEffectAudioData*> HoldEffectAudioDatas;///持有效果声音

	bool bInitialized = false;///<是否创建

	UPROPERTY(BlueprintAssignable, Category = "ServerCharacter")
	FActorCreateFinishDelegate OnActorCreateFinish;///<Actor进入世界回调

	UPROPERTY(BlueprintAssignable, Category = "ServerCharacter")
	FActorVisibleChangedDelegate OnVisibleChangedEvent;///<可见性改变蓝图回调

	UPROPERTY(BlueprintAssignable, Category = "ServerCharacter")
	FDeadActionPlayOverDelegate OnDeadActionPlayOver;///死亡动作播放完毕回调（可用于一些表现类功能，不影响流程的）
	
	UPROPERTY(BlueprintReadWrite, Category = "ServerCharacter")
		bool bActorCanSetpOn = false;///用于判断服务器对象是否可站立的属性，移动平台全部可以，可破碎的怪物也可以

	FSkillWeaponeBindObjDelegate OnSkillWeaponBindObj;
	TArray<FPART_SLOT_BIND_OBJ_DATA> WeaponBindObjData;
	bool bDestroy = false;

	UPROPERTY(BlueprintReadWrite, Category = "ServerCharacter")
		bool bDeadState = false;///死亡状态

	//头顶信息可显示的最大距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float HeadInfo3DUIShowDist = 2500;

	bool bIsMotionBlur = false;
private:
	CS3SeverCharacterStatus  CurStatus;
	FString m_EffectSlotName;///<粒子骨骼插槽
	float m_EffectScale;///<粒子缩放
	FVector m_EffectLoction;///<粒子的位置

	//击飞相关属性
	TArray<int32> m_UpForceArr;///<上升力容器
	FLinearColor m_RageLinearColor;///狂暴效果参数
	bool bRageState;///是否狂暴状态

	int32 OrientRotationCount = 0;//改变旋转的计数

	// EntityId属性对应的Entity指针
	KBEngine::Entity* BindEntity = nullptr;

	// 缓存的地面位置信息
	FGroundLocationCacheInfo NowGroundLocation;


public:
#pragma region 领兵功能
	/**
	* @brief 编组军队
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OrganizeArmy(const TArray<FString>& ModelList);

	/**
	* @brief 解散军队
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void DissolutionArmy();

#pragma endregion
};

FORCEINLINE UFightComponent* AServerCharacter::GetFightComponent() const { return FightComponent; }