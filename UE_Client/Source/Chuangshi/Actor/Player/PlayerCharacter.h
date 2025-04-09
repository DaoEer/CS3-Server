#pragma once

#include "Fight/FightAssist.h"
#include "Actor/ServerCharacter.h"
#include "GameData/NPCPointDatas.h"
#include "GameData/CameraParamsEventData.h"
#include "GameData/FlyPatrolData.h"
#include "GameData/CrossMapConfigData.h"
#include "GameData/CharacterData.h"
#include "Component/Role/PlayerControllerMoveComponent.h"
#include "GameData/Item/ItemBase.h"
#include "Component/CS3CameraComponent.h"
#include "Component/Role/LadderCustomMovementComponent.h"
#include "Component/CS3LightComponent.h"
#include "Kismet/KismetSystemLibrary.h"
#include "PlayerCharacter.generated.h"

/*
* 文件名称：PlayerCharacter.h
* 功能说明：玩家Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/

class GameObject;
class ARiderCharacter;
class AMagicCharacter;
class UPosSyncComponent;
class UFlyPatrolComponent;
class AFlyBindCharacter;
class UJumpComponent;
class URideCarrierComponent;
class ACameraControl;

DECLARE_DELEGATE_OneParam(LeftMouseClickCallbackDelegate, FVector);
DECLARE_DELEGATE_OneParam(MouseScrollCallbackDelegate, float);
DECLARE_DELEGATE(FCreateRidderModelOverDelegate);///飞行坐骑创建完毕通知
DECLARE_DELEGATE(FDisRideOnPetOverDelegate);//下马结束通知
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSkillAssist, FVector,AtkPos);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnChangeTargetDelegate);//设置完目标通知其他
/*
* 玩家Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API APlayerCharacter :public AServerCharacter
{
	GENERATED_BODY()
#pragma region	Avatar功能相关
public:

	virtual void InitFilterActorComponent() override;

	UPosSyncComponent* GetTransFormComp() { return PosSyncComp; };

private:
	//UDumbFilterActorComponent* mDumbFilterComp = nullptr;
	UPosSyncComponent* PosSyncComp = nullptr;

#pragma endregion

public:
	APlayerCharacter();///<构造函数
	virtual void PostInitProperties() override;
	virtual void BeginPlay()override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	void OnMouseLeftButtonClick();///<鼠标左键点击事件
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnSimulateMouseLeftButtonClick(FVector Pos);///<模拟鼠标左键点击事件
	void OnMouseScrollRoll(float Scale);///<鼠标滚轮滚动事件
	virtual void Tick(float DeltaSeconds) override;
	void BreakFalling();
	virtual void SetInitAction() override;///<设置初始化动作
	virtual bool IsCanPlayAction()override;
	virtual void BindLinkEntity(KBEngine::Entity* Entity) override;
	virtual void OnInitialized() override;
	void OnCreateRiderModelOver();///骑乘模式创建完毕(RiderCharacter模型加载完毕后调用)
	virtual void OnCreateModelOver() override;
	virtual void OnCreateApperanceOver() override;
	virtual void CreateAppearance() override;
	virtual void UpdateActorPositionToGround() override;
	virtual void CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap) override;
	FNAVIGATE_NPC_INFO GetNavigateNPCInfo();///使得外部接口可以使用数据
	void ClearNavigateNPCInfo();

	virtual void OnBindToEntity()override;
	virtual void InitCharacterComponent()override;

	virtual void SetPosition(const FVector& newVal, int32 parentID = 0) override;
	void OnPlayerPositionSet(const FVector& newVal);//待优化，备注是加的同地图传送加的，同地图传送不应该写在设位置这里

	void InitPosSyncComponent();
	void InitCameraComponent();
	void InitPlayerControllerMoveComopnent();
	void DeactivatePlayerControllerMoveComopnent();

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void ResetCameraData();///重置摄像机臂长和摄像机朝向

	void reqNetwordTime();
	void clearNetwordTime();
	UFUNCTION(BlueprintNativeEvent, Category = "Game|Player")
		void OnSetNetworkTime( int32 t );//设置网络状态

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnLeaveScenes();

	virtual void ReSetOpenScen3DUI() override;
	
	virtual void OnSignificanceChange() override;

	///检测状态改变
	void CheckChangeState(ENTITY_STATE NewState, ENTITY_STATE OldState);
	virtual void OnEnterDeadState() override;///玩家重写进入死亡状态
	virtual void OnEnterFreeState() override;///玩家重写进入空闲状态
	virtual void OnEnterWarnState() override;///玩家重写进入警戒状态

	void EnterVehicleMode(RIDE_POSTURE_ENUM RidePosture,int32 Profession,
		int32 Gender);
	int32 HasVehicle();
private:
	FTimerHandle reqNetwordTimeHandle;

public:


	/**
	*辅助施法表现，技能施法光圈
	*
	*@param IsAddSkillAssistUi  是否添加(bool)
	*@param SkillId		技能Id(int32)
	*@param FightAssist 战斗辅助实例(UFightAssist*)
	*
	*@return 无
	*/
	void AddSkillAssistUiToScene(bool IsAddSkillAssistUi, int32 SkillId = 0, UFightAssist* FightAssist = nullptr);

	/**
	*辅助施法表现，物品施法光圈
	*
	*@param IsAddSkillAssistUi  是否添加(bool)
	*@param SkillId		技能Id(int32)
	*@param FightAssist 战斗辅助实例(UFightAssist*)
	*
	*@return 无
	*/
	void AddItemAssistUiToScene(bool IsAddSkillAssistUi, FString UID = TEXT(""), int32 SkillId = 0, UFightAssist* FightAssist = nullptr);

	/**
	*辅助施法表现扩展，模型施法辅助
	*
	*@param IsAddSkillAssistUi  是否添加(bool)
	*@param AtkEntity	施法者Entity(CS3Entity*)
	*@param SkillId		技能Id(int32)
	*@param FightAssist 战斗辅助实例(UFightAssist*)
	*
	*@return 无
	*/
	void AddItemAssistUiToSceneExt(bool IsAddSkillAssistUi, FString UID = TEXT(""), int32 SkillId = 0, UFightAssist* FightAssist = nullptr);
	
	/**
	*BlueprintCallable 靠近目标Actor并对话
	*
	*@param TargetActor   目标Actor(AActor*)
	*@param NearbyDistance	靠近距离(float)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void GossipWithNearby(AActor* TargetActor, float NearbyDistance);
	//判断目标玩家是不是敌对的
	UFUNCTION(BlueprintPure, Category = "Game|Player")
	bool IsEnemyPlayer(AActor* TargetActor);
	
	/*----------------镜头功能相关---------------------------*/
	void StartPlayStory(const FString& SequenceId,int32 LoopNum =1);

	void StartPlayStory_P();
	/*----------------切换UE4底层飞行功能相关---------------------------*/
	void SwitchFly(bool bIsSwitch = true, bool bIsFly = true);
	/*----------------飞行功能相关---------------------------*/
	void StartFlyPatrol(FString FlyPatrolID);///<开始传送飞行
	/**
	*BlueprintCallable 进入飞行传送
	*
	*@param FlyPatrolID	飞行路径ID(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void EnterFlyPatrol(FString FlyPatrolID, const FString InCarrierId, const FString FlyModleId);
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StopFlyPatrol(float DelayTime = 0.0f);///<BlueprintCallable 停止飞行传送
	/**
	*BlueprintCallable 接出循环飞行传送
	*
	*@param FlyPatrolID	飞行路径ID(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StopCycleFlyPatrol(FString FlyPatrolID);

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void PauseFlyPatrol();///<暂停飞行

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void ReviveFlyPatrol();///<恢复飞行

	bool IsPausedFlyPatrol();	 //飞行是否暂停
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool IsFlyPatrolState();	//是否在飞行中

	ECollisionEnabled::Type GetOldCollision() { return OldCollision; };
	void SetOldCollision(ECollisionEnabled::Type Collision) { OldCollision = Collision; };

	/*----------------幻阵迷宫飞行功能相关---------------------------*/
	/**
	*BlueprintCallable 幻阵迷宫 飞行表现
	*
	*@param fPatrolID	飞行路径ID(FString)
	*@param sPatrolID	子飞行路径ID(FString)
	*@param pPoint		飞行开始步长(int32)
	*@param speed		飞行目标步长(int32)
	*@param screneID	飞行目标位置(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void EnterFlyToHZMGSpace(const FString fPatrolID, const FString sPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos);
	void StopFlyToHZMGSpace(const FString FlyID);///<结束幻阵迷宫飞行
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
	bool IsHZMGFlyState(); ///<是否处于幻阵迷宫飞行状态
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnChangeHeadInfosByOtherOwner(APlayerCharacter* Character);///<玩家头顶信息改变为其他对象的

	/**
	*BlueprintCallable 移动物品
	*
	*@param SrcOrder 初始格子(int32)
	*@param DstOrder 目标格子(int32)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void MoveItem(int32 SrcOrder, int32 DstOrder);
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnUpdateMoney();///<玩家金钱改变通知蓝图
		
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnHPChanged( const int& HP, const int& HP_Max );///<玩家血量改变通知蓝图

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnGangQiChanged( const int& curGangQi, const int& maxGangQi );///<玩家gangqi改变通知蓝图
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnGangQiStateChanged( const int& gangQiState );///<玩家gangqistate改变通知蓝图
		
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnPlayerNameChanged(const FString& playerName );///<玩家名字改变通知蓝图
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnCampChanged(const int& camp );///<玩家阵营改变通知蓝图
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnTempCampChanged(const int& tempCamp );///<玩家临时阵营改变通知蓝图

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnUpdateBindMoney();///<玩家绑定金钱改变通知蓝图

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnRoleLevelUp(const int32 Level);///<玩家升级

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnRoleXiuweiLevelUp(const int32 Level);///<玩家修为升级

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnRoleJingjieLevelUp(const int32 Level);///<玩家境界升级

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnTitleChanged();///<玩家title改变通知蓝图

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnGangQiProgressChanged( const int& qangQIProcess,  const int& maxGangQi);
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnKillingValueChanged();
		
	///杀气值变化
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnRoleKillingValueChange(const int32 KillingValue);

	/**
	*OnRoleOnWaterAreaChange
	* @brief 玩家进出水面
	* @param const int32 onWaterArea	是否处于水面
	* @return void
	*/
	void OnRoleOnWaterAreaChange(const int32 onWaterArea);

	/**
	*BlueprintPure 玩家是否有某个标志位
	*
	*@param RoleFlag 玩家标志位(ROLE_FLAG)
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		bool HasRoleFlag(ROLE_FLAG RoleFlag);

	/**
	*BlueprintCallable 进入/离开位面
	*
	*@param SpaceScriptID 位面spaceID(FString)
	*@param IsLeave		是否是离开(bool)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnTriggerPlane(const FString SpaceScriptID, bool IsLeave = false);

	/**
	*BlueprintCallable 进入位面
	*
	*@param SpaceScriptID 位面spaceID(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void GotoSpacePlane_(const FString SpaceScriptID);

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void TriggerPlaneEffect(bool IsLeave);///<通知蓝图进入位面特效

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void CreateLightWall(const FString& RowNumber, AREA_LIGHT_WALL_TYPE_ENUM CurrentType);

	//设置是否table所有entity
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnTableAllEntity(bool BoolValue);

	void EnableInputToControll(bool IsCanInput);

	/*----------------模型外观(部件、动作)功能相关---------------------------*/
	///<刷新模型
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void RefreshModel();

	///<重置外观的部件(恢复成服务器默认的部件）
	UFUNCTION(BlueprintCallable, Category = "GameCharacter")
		void ResetModelPart(MODEL_PART_TYPE PartType);

	///<商城预览改变环身光效(游戏场景中)
	///UNCTION(BlueprintCallable, Category = "Game|Player")
	virtual void PreviewBodyLightEffect(FString EffectId)override;

	///<动作切换检查是否隐藏/显示环身光效（此效果只在待机时显示）
	virtual void CheckBodyLightEffect()override;

	///更新正常模型武器部件状态
	void UpdateWeaponState();

	///更换武器---玩家变成黑衣人后四职业对应的武器（夜袭凤栖镇）
	void UpdateWeapontYXFXZ(YXFXZ_COPY_WEAPON_ENUM type);

	///更换武器---玩家远程吃鸡武器（勇闯绝命岛）
	void UpdateWeapontYCJMD(YCJMD_COPY_WEAPON_ENUM Type, const FString& SockeName, const FString& PartId);

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void GetBackAdornTransfrom(FPART_TRANSFORM& Transfrom);///<获取背饰偏移量

	// 设置模型是否可改变颜色
	inline void SetModelColorScheme(uint8 colorScheme) { APlayerCharacter::ModelColorScheme = colorScheme; }
	void ChangeModelColor();
	
	/*----------------野外竞速功能相关---------------------------*/
	void OnStartOutsideCopyGame(float InDelayTime, FString InCarrierId, float InInputYawScale);//开始野外竞速
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnOverOutsideCopyGame();///结束野外竞速

	void OnStartPlayerAutoMoveCopyGame(float InInputYawScale); ///玩家开始自动移动
	void OnOverPlayerAutoMoveCopyGame();///玩家结束自动移动

	void OnPlayerCameraRotation(float RotationTime = 0.0f);

	/*----------------抱宠物功能相关---------------------------*/
	void HoldPet(FName AttachMeshID);///抱宠物
	void DownPet(FName AttachMeshID);///放下宠物

	/*----------------抱金丹功能相关---------------------------*/
	void HoldJinDan(FName AttachMeshID, float buffRemainTime, float TimerInterval);
	void DownJinDan(FName AttachMeshID);

	/**
	*BlueprintImplementableEvent, 通知蓝图，玩家抱起金丹
	*
	*@param buffRemainTime 剩余时间
	*@param TimerInterval 倒计时回调时间间隔
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnHoldJinDanBP(float buffRemainTime, float TimerInterval);

	/**
	*BlueprintImplementableEvent, 通知蓝图，玩家放下金丹
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnDownJinDanBP();

	/**
	*BlueprintImplementableEvent, 当前玩家是否在水域
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnMouseisWaterBP();

	/*----------------跳跃功能相关---------------------------*/
	virtual void OnJumped_Implementation()override;
	virtual void Falling() override;
	virtual void Landed(const FHitResult& Hit) override;
	//virtual void OnMovementModeChanged(EMovementMode PrevMovementMode, uint8 PreviousCustomMode = 0)override;
	virtual void CheckJumpInput(float DeltaTime)override;

	/*----------------随机动作功能相关---------------------------*/
	void StartCheckRandomAction();
	void PlayRandomAction(int32 RandomNumber);///播放随机动作（根据服务器发的种子值）
	void StopRandomAction();///停止随机播放动作

	/*----------------绑定飞行Actor功能相关---------------------------*/
	UFUNCTION()
		void SwitchOffFlyOrbitMode();///<退出飞行模式
	void CreateFlyBindActor(FString FlyBindActorID = TEXT("1"));
	void DestroyFlyBindActor();

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool GetSkillAssistUi() { return HasSkillAssistUi; }
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool IsSkillAssistTurn() { return IsSkillAssistUseTurn; }

	UFUNCTION(BlueprintNativeEvent, Category = "Game|Player")
		void SetCameraParamsEvent(const FString& EventID);///<摄像机事件

	UFUNCTION(BlueprintNativeEvent, Category = "Game|Player")
		void ClearCameraParamsEvent();///<清除摄像机事件

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnClearCameraParamsEventTimer();///<清除摄像机事件定时器

		//CST-6177 程序功能需求（0级）--研究实现一种直观显示技能作用目标和范围的调试方法
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnScopeLocation(int32 SkillID, FVector position, int32 CasterID);///<清除摄像机事件定时器

		//CST-6177 程序功能需求（0级）--研究实现一种直观显示技能作用目标和范围的调试方法
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnScopeActor(int32 SkillID, AActor* Target, int32 CasterID);///<清除摄像机事件定时器
	/**
	* 设置玩家是否受movement的影响
	*
	*@param bValue 是否受影响
	*@param bIsModeChange 是否为模式切换，除了操作模式的设置其他都应该为false
	*@param Count 计数，操作旋转计数
	*@param bIsReduction 是否还原，如果为True，且已经有记录值，则bValue，bIsNeedRecord 无效
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void SetOrientRotationToMovement(bool bValue, bool bIsModeChange, int32 Count = 0, bool bIsReduction = false);
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool GetOrientRotationToMovement();
	/**
	* 进入移动平台
	* @param MovingPlatformID 平台ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnEnterMovingPlatform(int32 MovingPlatformID);

	/**
	* 离开移动平台
	* @param MovingPlatformID 平台ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnLeaveMovingPlatform(int32 MovingPlatformID);

	/**
	* 更新法宝
	*/
	void UpdateFaBao(FString InModelId);

	/**
	* 隐藏显示法宝
	*/
	void HideFaBao(bool IsHideFaBao);

	virtual void SetMeshPartHiddenInGame(MODEL_PART_TYPE MeshPartType, bool IsHiddenInGame) override;

	/**
	* 设置是否正在交互状态
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void SetRoleInteractive(bool IsInteractive);

	///停止玩家移动（外部接口）
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StopPlayerMove();

	/**
	* 创建法宝
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void CreateFaBao(const FString& InFaBaoModeId);

	/**
	* 删除
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void DestroyFaBao();
#pragma region 寻路相关
	/**
	*ShowAllNavigateGuide
	* @brief 显示所有的寻路指引点
	* @param const TArray<FVector> & PathList	得到的寻路指引点坐标列表
	* @param int32 QuestID		任务ID
	* @return void
	*/
	void ShowAllNavigateGuide(const TArray<FVector>& PathList, int32 QuestID = 0);

	/**
	*CheckPlayArriveGuidePoint
	* @brief 检查玩家是否到达自动寻路指引点
	* @param const int32 & LastStartPointIndex	上一次自动寻路到达的指引点索引
	* @param const int32 & LastEndPointIndex	上一次自动寻路指引点结束索引
	* @return void
	*/
	//void CheckPlayArriveGuidePoint(const int32& LastStartPointIndex, const int32& LastEndPointIndex);

	/**
	*ClearAllNavigateGuide
	* @brief 清除任务寻路的寻路指引
	* @return void
	*/
	void ClearAllNavigateGuide(bool IsArrived = true);

	void ClearCrossMapInfos();

	/**
	*DelNavigateGuideByQuestID
	* @brief 根据任务ID删除该任务的任务指引
	* @param const int32 & QuestID	任务ID
	* @return void
	*/
	void DelNavigateGuideByQuestID(const int32& QuestID);

	/**
	*GetAutoNavigatePathList
	* @brief 得到自动寻路的路径
	* @param const FVector & StartPos	开始寻路位置
	* @param const FVector & EndPos		结束寻路位置
	* @param FString SpaceName			目标地图
	* @param TArray<FVector>& FinalAutoPathList			路径点列表
	* @return void
	*/
	void GetAutoNavigatePathList(const FVector& StartPos, const FVector& EndPos, FString SpaceName, TArray<FVector>& FinalAutoPathList);

	/**
	*GetBestNavigatePathList
	* @brief 得到自动寻路的路径
	* @param const FVector & StartPos	开始寻路位置
	* @param const FVector & EndPos		结束寻路位置
	* @param FString SpaceName			目标地图
	* @param TArray<FVector>& FinalAutoPathList			路径点列表
	* @return void
	*/
	void GetBestNavigatePathList(const FVector& StartPos, const FVector& EndPos, FString SpaceName, TArray<FVector>& FinalAutoPathList);

	/**
	*GetNormalNavigatePathList
	* @brief 得到自动寻路的路径
	* @param const FVector & StartPos	开始寻路位置
	* @param const FVector & EndPos		结束寻路位置
	* @param FString SpaceName			目标地图
	* @param TArray<FVector>& FinalAutoPathList			路径点列表
	* @return void
	*/
	void GetNormalNavigatePathList(const FVector& StartPos, const FVector& EndPos, FString SpaceName, TArray<FVector>& FinalAutoPathList);

	/**
	*GetAutoNavPathPoints
	* @brief 得到自动寻路的路线
	* @return const TArray<FVector>&	路径点列表
	*/
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		const TArray<FVector>& GetAutoNavPathPoints();

	/**
	*GetNavigateGuidePathList
	* @brief 得到自动寻路的路线
	* @return const TArray<FVector>&	路径点列表
	*/
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		const TArray<FVector>& GetNavigateGuidePathList();


	/**
	*GetAdjustedAutoNavigatePathList
	* @brief 获得通过投影到寻路系统上得到修正的寻路点
	* @param TArray<FVector> & FinalAutoPathList
	* @return void
	*/
	void GetAdjustedAutoNavigatePathList(TArray<FVector>& FinalAutoPathList);

	/**
	*StartAutoNavigate
	* @brief 开始自动寻路移动
	* @param const FVector & DstPosition	目标位置
	* @param float NearbyRange	靠近距离
	* @param FString DstSpaceName	目标地图，默认为空
	* @param int AutoQuestID	寻路的任务ID
	* @param bool IsSearch	是否是搜索得到目标
	* @return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StartAutoNavigate(const FVector& DstPosition, float NearbyRange = 2.0f, FString DstSpaceName = "", int AutoQuestID = 0, bool IsSearch = false, int32 GossipWithType = 0);

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void SubroutineAutoNavigate(const FVector& DstPosition, float NearbyRange = 0.0f, FString FinalSpaceName = "", int AutoQuestID = 0, bool IsSearch = false);

	/**
	*上马完成后再次调用寻路
	*/
	void AutomaticMount();
	/**
	*CheckAutoNavigate
	* @brief 检测自动寻路是否到达中间节点
	* @param FString DstSpaceName	目标地图，默认为空
	* @param const FVector & DstPosition 目标位置
	* @param float NearbyRange	靠近距离
	* @param bool IsSuccess	是否成功
	* @return void
	*/
	void CheckAutoNavigate(FString DstSpaceName, const FVector& DstPosition, float NearbyRange, bool IsSuccess);

	bool canTargetActorNavigate(AServerCharacter * ServerCharacter);

	/**
	*StopAutoNavigate
	* @brief 停止自动寻路移动
	* @return void
	*/
	void StopAutoNavigate(bool IsArrived);

	/**
	*GetNPCPositionByQuest
	* @brief 根据任务目标或者是完成任务之类的来决定如何找到对应的点，如果是完成任务的寻路，以及击杀怪物，获取物品的寻路，先搜索附近10米有没有，再从配置中找
	* @param FString DstSpaceName	目标地图
	* @param FString NPCScriptID	NPC的ScriptID
	* @param FVector & NPCPosition	最终得到的NPC位置
	* @return bool 是否是搜索得到目标
	*/
	bool GetNPCPositionByQuest(FString DstSpaceName, FString NPCScriptID, bool IsCompletedQuest, FString QuestTaskClass, FVector& NPCPosition);

	/**
	*StartQuestNavigate
	* @brief 开始任务寻路
	* @param bool IsCompletedQuest	是否是交任务行为，如果不是，那就是任务目标寻路
	* @param FString QuestTaskClass	任务目标的Class
	* @param FString NPCScriptID	NPC的ScriptID，如果是直接给位置，这个地方直接给一个""
	* @param const FVector& FinalPosition	直接给的任务寻路位置
	* @param float NearbyRange		靠近距离
	* @param FString DstSpaceName	目标地图，可以为空，为空表示当前地图
	* @param int AutoQuestID		任务的ID
	* @param bool IsCrossMap		是否跨地图
	* @return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StartQuestNavigate(bool IsCompletedQuest, FString QuestTaskClass = "", FString NPCScriptID = "", FString DstSpaceName = "", FVector FinalPosition = FVector::ZeroVector, float NearbyRange = 2.0f, int AutoQuestID = 0, bool IsCrossMap = false, int32 GossipWithType = 0);

	/**
	*StartCrossMapNavigate
	* @brief 开始跨地图寻路
	* @param FString DstSpaceName	目标地图，可以为空，为空表示当前地图
	* @param bool IsCompletedQuest	是否是交任务行为，如果不是，那就是任务目标寻路
	* @param FString QuestTaskClass	任务目标的Class
	* @param FString NPCScriptID	NPC的ScriptID，如果是直接给位置，这个地方直接给一个""
	* @param const FVector& FinalPosition	直接给的任务寻路位置
	* @param float NearbyRange		靠近距离
	* @param int AutoQuestID		任务的ID
	* @return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StartCrossMapNavigate(FString DstSpaceName, bool IsCompletedQuest, FString QuestTaskClass = "",
			FString NPCScriptID = "", FVector FinalPosition = FVector::ZeroVector, float NearbyRange = 2.0f,
			int AutoQuestID = 0, ENUM_NAVIGATE_ACTION_TYPE NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault, int32 GossipWithType = 0);

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnStartCrossMapNavigate(FCROSS_MAP_QUEST_TARGET_INFO& MapQuestTargetInfo);

	void ActivateNavigateMoveModeOperation(bool IsActivate, FVector DstPosition, float NearbyRange, FString DstSpaceName, int AutoQuestID, bool IsSearch, bool IsArrived, int32 GossipWithType = 0);

	void AtuoAdjustViewTargetWithBlend();///<CST-5270寻路中自动转视角
	void UnAdjustViewTargetWithBlend();///<取消调整摄像机视角

	bool CheckItemTeleportStone();
	TArray<UItemBase*> GetItemTeleportStone();

	void OnWaterJumpBegin();

	///<设置是否能离开寻路边缘
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
	void SetWalkOffLedges(bool bCanWalkOffLedges);
	///<获取是否能离开寻路边缘
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
	bool GetCanWalkOffLedges();
#pragma endregion
	void SetCharacterMovementDefaultWalkProperty();
	void SetCharacterMovementWalkProperty(float InMaxStepHeight, float InWalkableFloorAngle);

	///<从玩家视角到指定entity连线上某点的摄像机过渡，后还原到玩家身后的视角
	UFUNCTION(BlueprintCallable, Category = "Global")
		void SetViewTarget(int32 TargetID, FVector DurationTime = FVector::ZeroVector, float Range = 0.0f, FVector StartViewRotator = FVector::ZeroVector, FVector TragetViewRotator = FVector::ZeroVector, bool bIsResetPlayerCamera = true);
	
	/*----------------载具功能相关---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void ChangeRidePet(FString PreviewCarrideId);///<改变骑乘宠物

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		FString GetRidePetCarrierID();///<获取当前骑乘ID

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool IsRidePetState();///<是否骑宠物状态

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool IsCarrierState();///<是否骑乘状态[不包括载具，比如御剑]

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool IsDisCarrierState();///是否在下载具过程状态

	UFUNCTION(BlueprintPure, Category = "Game|Player")
		ARiderCharacter* GetRiderCharacter();
	/*----------------摄像机效果功能相关---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void CameraApproach(float Dist, float ApproachT, float RemainT, float ApproachBackT);
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void RadialBlur(float Intensity, float FadeInT, float RemainT, float FadeOutT);
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void CameraShake(float Intensity, float Rate, float Time, int32 Priority);
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void RadialOffsetX(float Offset, float FadeInT, float RemainT, float FadeOutT);
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void RadialOffsetY(float Offset, float FadeInT, float RemainT, float FadeOutT);
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void CameraUp(float Height, float FadeInT, float RemainT, float FadeOutT);

	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void StopCameraApproach();
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void StopRadialBlur();
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void StopCameraShake();
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void StopRadialOffsetX();
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void StopRadialOffsetY();
	UFUNCTION(BlueprintCallable, Category = "Player|Camera")
		void StopCameraUp();
	///玩家镜头扭曲
	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = Camera)
		void LXDistortScene_P(float fDitortAngle, float fDistortMask, float fStartTimeDistort, float fRecoveryTimeDistort, float HoldTimer);

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = Camera)
		void OnEndLXDistortScene_P();
	/*----------------天气效果功能相关---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "Player|Weather")
		void OnBindWeatherToCamera(UCameraComponent* CameraComp);
	UFUNCTION(BlueprintCallable, Category = "Player|Weather")
		void OnSetWeatherParticle(class UParticleSystem* NewTemplate);

	/*----------------更新当前地板数据相关---------------------------*/
	///更新当前地板数据，在帧数低的时候，多次更新地板数据，避免被穿透，外部调用
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void UpdateCurrentFloor();

	/*----------------交互功能相关---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
	void AddToInteractivityList(AServerCharacter* Target);///<加入可交互列表
	void RemoveFromInteractivityList(AServerCharacter* Target);///<从可交互列表中移除

	/*----------------围绕目标旋转---------------------------*/
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
	void RotateRroundToTarget(AActor* Target, float Speed, float Disatance, float Height, float angle);

	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
	void StopRoateToTarget();

	//UFUNCTION(BlueprintPure, Category = "Game|Player")
	virtual int32 GetFinalCamp();///<获取最终阵营

	void EndAutoAttackFriendEntity();

	/**
	*BlueprintCallable 切换自己为被玩家控制的角色
	*
	*@return 是否切换成功
	*/
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		bool SwitchControlToSelf();

	/*----------------移动相关---------------------------*/
	virtual float GetMoveSpeed() override;///获取角色(包括其他客户端)混合时的速度
	float GetMoveDirection();///获取角色(包括其他客户端)混合时的方向(动画蓝图用)
	virtual bool IsActiveMoveing()override;///是否角色主动移动[除去击退、飞行、没移动]
	void SyncMoveType(CS3_MOVE_TYPE CurrMoveType);///向服务器同步我的移动类型

	void UpdateAimOffsetYawAndPitch(float DeltaSeconds);
	
	
	/*----------------辅助跳跃相关---------------------------*/
	/**
	*BlueprintImplementableEvent, 执行辅助跳跃检测
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void ExecuteLedgesJump();

	///是否能边缘辅助跳跃
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		bool IsCanLedgesJump();

	/**
	* 客户端设置AOI
	*@param Radius 	AOI半径(单位:米)
	*
	*@return 无
	*/
	void ClientSetAoi(const FString& Radius);

	/** 重置AOI
	*
	*@return 无
	*/
	void ClientResetAoi();

	/**
	*BlueprintImplementableEvent, 显示当前玩家与目标的距离
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnTargetDistanceDIsplay();

	/**
	*BlueprintImplementableEvent, 隐藏当前玩家与目标的距离
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnTargetDistanceHiding();

	/*
	*玩家死亡深度检测
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void onPlayerUnderArea();

	//远程吃鸡鼠标右键点击功能表现
	void OnClickRightMouseYCJMD();
	//远程吃鸡右键蓝图事件
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
	void OnClickRightMouseYCJMD_BP();
	//渐变摄像机臂长
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnChangeArmLength(float ArmLength,float time);

#pragma region 玩家设置目标相关
	/**
	*对玩家设置目标后对没有继承BP_CharacterInterface的外部通知
	*/
	UPROPERTY(BlueprintAssignable, Category = "PlayerCharacter")
		FOnChangeTargetDelegate OnChangeTargetDelegate;

	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void SelectOtherPlayer();///<执行ShowSelectTarget操作

		/**
		*设置完目标通知玩家蓝图
		*/
	UFUNCTION(BlueprintImplementableEvent, Category = "PlayerCharacter")
		void BP_OnChangeTarget();

	/**
	*设置目标
	*/
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void SetPlayerTarget(AServerCharacter* PCurPlayerTarget);
#pragma endregion

#pragma region 风力相关

	/**
	* @brief 添加风力
	* @param _WindSpeed 	风速
	* @param _WindDirection 风的方向
	*
	* @return 这个风的ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		int32 AddWindForce(float _WindSpeed, FVector _WindDirection);

	/**
	* @brief 开始某个风力
	*
	* @param WindID 	风ID
	* @param _WindSpeed 	风速(不填则为添加时的风速)
	* @param _WindDirection 风的方向(不填则为添加时的方向)
	*
	* @return 是否成功开启
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool BeginWindForce(int32 WindID, float _WindSpeed = -1.0f, FVector _WindDirection = FVector::ZeroVector);

	/**
	* @brief 开始所有风力
	*
	* @param WindID 	风ID
	* @param _WindSpeed 	风速(不填则为添加时的风速)
	* @param _WindDirection 风的方向(不填则为添加时的方向)
	*
	* @return 是否成功开启
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void BeginAllWindForce();

	/**
	* @brief 暂停某个风力
	* @param WindID 这个风的ID
	*
	* @return 是否成功暂停
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool PauseWindForce(int32 WindID);

	/**
	* @brief 暂停所有风力
	* @param WindID 这个风的ID
	*
	* @return 是否成功暂停
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void PauseAllWindForce();

	/**
	* @brief 停止所有风力
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StopAllWindForces();

#pragma endregion

#pragma region 云梯相关
	/**
	* @brief 是否攻城云梯模式
	*
	* @return 无
	*/
	virtual bool IsLadderMovement()override;
#pragma endregion

#pragma region 跳伞相关
	/// 设置跳伞状态
	inline void SetParachuteState(PARACHUTE_STATE state) { ParachuteState = state; }
	/// 是否在跳伞某个阶段
	inline bool IsParachuteState(PARACHUTE_STATE state) { return ParachuteState == state; }
	/// 是否正在进行跳伞
	inline bool IsJumpParachuteState() { return ParachuteState != PARACHUTE_STATE::PARACHUTE_STATE_NORMAL; }
	/// 是否是跳伞降落阶段（未开伞+开伞）
	inline bool IsSkyParachuteState() { return (ParachuteState == PARACHUTE_STATE::PARACHUTE_STATE_FALL) || (ParachuteState == PARACHUTE_STATE::PARACHUTE_STATE_OPEN); }
#pragma endregion

#pragma region 火炮相关
	/// 设置跳伞状态
	inline void SetOperatorBatteryID(int32 OBID) { OperatorBatteryID = OBID; }

#pragma endregion

#pragma region Exposed调用
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_logoff();	

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_logout();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_SetBlendDir(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onClientSetAoi(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onClientResetAoi();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onPlayerUnderArea();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_enterWaterArea();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_leaveWaterArea();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_enterMaterialArea(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_leaveMaterialArea(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestPlayRandomAction();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_setPositionFromClient(const FVector& POSITION_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_verifyClientTime(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_updateMoveType(const int32& INT32_1);
#pragma endregion

	void OnDodgeRotation();
	///----------------播放镜头状态中------------
	void OnEnterEffectStoryState();
	void OnExitEffectStoryState();

	UFUNCTION(BlueprintImplementableEvent, Category = "PlayerCharacter")
		void BP_OnUpdatePlayerStoryIcon(bool bIsShow);
protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	void InitLocalPlayerComponent();///<本地玩家组件初始化
	void InitNotLocalPlayerComponent();///<非本地玩家组件初始化

	virtual void BaseChange() override;///<重写Character中的BaseChange方法，为了准确判断玩家上/下 移动平台上的触发

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnOpenResurrectionPanelBP();

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Player")
		void OnInteractiveTargetChange();///<交互目标改变
private:
	/*----------------飞行功能相关---------------------------*/
	const FCAMERA_PARAMS_EVENT_DATA* GetCameraParamsEventData(const FString& CameraParamsEventId);
	

	void OnNavigateEndProcess(AServerCharacter* TargetCharacter);

	///调用技能辅助回到
	void SkillAssisCallBack(FVector& AtkPos);

	///CST-4743
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void GetPenetrationAdjustment();

	///在被卡住没有被自动弹开时，激活hit事件，每一帧调用
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void DispatchHitEvent();

	/*----------------交互功能相关---------------------------*/
	void StartCheckingInteractiveTarget();///<开始检测交互
	void StopCheckingInteractiveTarget();///<停止检测交互
	void RefreshInteractiveTarget();///<刷新交互目标
	UFUNCTION(BlueprintCallable, Category = "PlayerCharacter")
		void SetInteractiveTarget(AServerCharacter* Target); ///<设置交互目标
	AServerCharacter* SortInteractiveTarget();///<对交互列表进行排序

	void ResetInteractiveData();///<重置交互数据（列表和当前交互目标）
	void DelayGossipWithNearBy(AActor* TargetActor);///<延迟等待玩家停止移动后再交互spellBox
	/*----------------天气效果功能相关---------------------------*/
	void InitWeatherComponent();///<初始化天气组件
	void UnBindWeatherSoundComp();///<销毁前移除

	/*----------------光照跟随玩家功能相关---------------------------*/
	void InitLightComponent();///<初始化天气组件

	/*----------------模型外观(部件、动作)功能相关---------------------------*/
	void NotifyCreateRoleAppearance();
	void OnNotifyActionChange(FACTION_DATA ActionData);
	void OnNotifyActionChangeFinish(FACTION_DATA ActionData);
	void OnPlayShouBaoDaoActionOver(ACharacter *GameCharacter, FACTION_DATA InActionData);

	/*----------------暂无归类相关---------------------------*/
	void OnChangeTarget();
	void OnEnterStallState();///玩家进入摆摊状态
	UFUNCTION()
		void OnWorldPostActorTick();
	void ClearWorldPostActorTickHandle();

public:
	UPROPERTY(EditAnywhere)
		float CameraMinLength = 50.0;

	UPROPERTY(EditAnywhere)
		float FOVMulity = 0.2;

	UPROPERTY(EditAnywhere)
		float MinFOV = 30;

	UPROPERTY(EditAnywhere)
		float MaxFOV = 90;

	///当前目标
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "PlayerCharacter")
		AServerCharacter* CurPlayerTarget;
	///原有目标
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "PlayerCharacter")
		AServerCharacter* OldPlayerTarget;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UChildActorComponent* ChildActor;///<子Actor组件，当前用于飞行传送与上坐骑

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		class USpringArmComponentEX* SpringArmCompent;///<镜头摇臂

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UCS3LightComponent* CS3LightComponent;///<光照组件

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UCS3CameraComponent* CameraComponent;///<镜头组件

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UJumpComponent* JumpComponent;///<跳跃、轻功组件

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		URideCarrierComponent* RideCarrierComponent;///<骑乘组件

	/*----------------交互功能相关---------------------------*/
	UPROPERTY(BlueprintReadWrite)
		APLAYER_INTERACTIVE_ENUM EPlayerInteractiveState;///<玩家当前交互状态

	bool bIsRoleInteractive;///<是否在交互过程中

	UPROPERTY(BlueprintReadOnly)
		AServerCharacter*  CurInteractiveTarget;///<当前交互目标

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CameraParamsEventID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isOpenLookCamera = false; //玩家转向摄像机开关 CST-7541

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		AMagicCharacter* FabaoCharacter;//玩家法宝Actor

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		AFlyBindCharacter* FlyBindCharacter;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UFlyPatrolComponent* FlyPatrolComponent;

	UPROPERTY(BlueprintReadOnly)
		AActor* CurrentBaseActor;//玩家脚底的actor

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool MouseisWater;//当前玩家鼠标指向的是否为水域

	bool IsNotifyServerUnderArea = false;//是否通知服务器玩家跌落到死亡深度
	bool IsNotifyServerLandFalling = false;	//是否通知服务器掉落的高度

	UPROPERTY(BlueprintAssignable, Category = "PlayerCharacter")
		FOnSkillAssist OnSkillAssist;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsOpenScope = false;///仅供测试使用 开启技能模型调试

	UPROPERTY(BlueprintReadOnly, Category = "PlayerCharacter")
	int32 PetEntityId;///<跟随的宠物id

	FCreateRidderModelOverDelegate OnBroadCreateRidderModelOver;///<骑乘模型创建完毕
	FDisRideOnPetOverDelegate OnDisRideOnPetOver;///<下马结束

	float CurMoveDirection;///当前角色移动方向	
	float OtherMoveDirection;///其他玩家的移动方向
	float CurAimOffsetYaw;///瞄准偏移平移yaw值
	float CurAimOffsetPitch;///瞄准偏移上下Pitch值

	bool bUpdatePos = false;

	bool IsDodgeState = false;
	FRotator DodgeRotator;
	CS3_MOVE_TYPE OtherPlayerMoveType;///其他玩家的移动类型(同步过来的)

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bOnHitBack = false;///被卡住是是否被判定为引擎自动弹开

		//玩家镜头后期处理(只有本地玩家才有用)
	UPROPERTY(Interp, BlueprintReadWrite, Category = "PostProcess")
		struct FPostProcessSettings PostProcessSettings;

	UPROPERTY(BlueprintReadOnly)
		ACameraControl* CameraControl;//摄像机操作

	AActor *FeiShengProcressTargetActor = nullptr;//飞升时切换摄像机过渡的对象
	float FeiShengUpSpeed;//飞升时上升速度
	float FeiShengRightSpeed;//飞升时左右移动速度
	float FeiShengCameraLength;//飞升时摄像机与主角距离

	/*----------------辅助跳跃相关---------------------------*/
	UPROPERTY(BlueprintReadOnly)
		int32 LedgesJumpDownStep = 2;//辅助下跳检测高度（1=1米，2=2米....）
	bool IsLevelOpenLedgesJump = true;//当前关卡是否开启辅助跳

	UPROPERTY(BlueprintReadOnly)
		TEnumAsByte<EDrawDebugTrace::Type> DrawDebugType = EDrawDebugTrace::Type::None;///<辅助跳射线显示类型

	/*----------------攻城战相关---------------------------*/
	UPROPERTY(BlueprintReadOnly)
		ULadderCustomMovementComponent* LadderCustomMovmentCpt;//云梯组件
	
	/*----------------远程吃鸡相关---------------------------*/
	PARACHUTE_STATE ParachuteState;			/// 跳伞状态

	float YCJMDParachuteDirX = 0.0f;///<吃鸡跳伞未开伞AD混合方向(新版吃鸡)
	float YCJMDParachuteDirY = 0.0f;///<吃鸡跳伞未开伞WS混合方向(新版吃鸡)

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsYCJMDAimOffsetState = false;///<是否远程吃鸡瞄准状态(只限于右键瞄准)

	UPROPERTY(BlueprintReadOnly)
		bool bIsYCJMDCopy = false;///<是否远程吃鸡副本状态
	 
private:
	bool HasSkillAssistUi = false;///<是否有施法辅助
	bool IsSkillAssistUseTurn = false;///< 施法辅助是否用到旋转

	bool IsCalNarDirection;
	//玩家前方向
	FVector CapsuleVec;

	//玩家是否受movement影响记录
	bool bModeOrientRotation;///<操作模式的值
	int32 OrientRotationNum;///<非操作模式设置该值的计数

	int32 OperatorBatteryID;	///<操作火炮的ID

	static uint8 ModelColorScheme;	///< 根据临时阵营改变模型颜色(1：为美术版本，2：为程序版本)

	LeftMouseClickCallbackDelegate LeftMouseClickCallback;///<鼠标左键点击回调
	MouseScrollCallbackDelegate MouseScrollCallback;	///< 鼠标滚轮滚动

	/*----------------自动寻路功能相关---------------------------*/
	TArray<int32> NavigateGuideEffectList;
	TArray<FVector> NavigateGuidePathList;
	TArray<bool> NavigateGuideEffctTypeList;
	FTimerHandle AutoNavigateHandle;
	TArray<FVector> AutoNavPathPoints;
	FNAVIGATE_NPC_INFO NavigateNPCInfo;
	FTimerHandle AutoNavigateWaterJumpHandle;
	FTimerHandle SetViewTargetWithBlendHandle;
	bool AtuoAdjustView = false;
	float AtuoAdjustYawAlpha = 0.0f;
	float AtuoAdjustedPitchAlpha = 0.0f;

	float DefaultMaxStepHeight;
	float DefaultWalkableFloorAngle;
	ECollisionEnabled::Type OldCollision;

	FTimerHandle AutoAttackFriendEntityHandle;

	TArray<int32> WindIDArr;///<风的ID容器

	/*----------------野外竞速功能相关---------------------------*/
	int32 OutsideCopyCamScaleHeadle = -1;///<缓存摄像机的旋转速度，在结束时再设置回去
	bool bIsDelayAutoMovement = false;///<野外竞速延时开始自动移动中
	FTimerHandle AutoMovementTimerHander;

	/*----------------围绕目标旋转---------------------------*/
	FTimerHandle RotateToTargetTimerHander;

	FString SequenceId = TEXT("");
	int32 SequenceLoopNum = 1;

	bool LeaveMovePlatform_HitBack = false; ///<在移动平台上被击飞不算离开移动平台

	FTimerHandle RandomActionTimerHander;///随机动作定时器

	int32 NavigateParticleUID = -1;

	FHitResult LastHit;///上一帧检测到被弹开的结果;

	float CurMoveSpeed;///记录当前人物的移动速度
	UPROPERTY()
		UParticleSystemComponent* WeatherParticle;///<天气粒子组件
	/*----------------交互功能相关---------------------------*/
	UPROPERTY()
		TArray<AServerCharacter*> InteractivityList; ///<可交互目标列表

	FTimerHandle InteractiveTimerHandle;///<交互定时器

	FDelegateHandle WorldPostActorTickHandle;

	FTimerHandle DelayGossipWithHandle;
};