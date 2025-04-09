#pragma once

#include "GameFramework/PlayerController.h"
#include "Component/Role/PlayerControllerMoveComponent.h"
#include "../Operation/OperationData.h"
#include "Engine/ObjectLibrary.h"
#include "GameData/InputData.h"
#include "GameData/ShortcutKey.h"
#include "Manager/CfgManager.h"
#include "CS3ConsoleMgr.h"
#include "Manager/AtkStateMar.h"
#include "AIController.h"
#include "KeyState.h"
#include "CS3PlayerController.generated.h"


class UAtkStateMar;
class UCS3ConsoleMgr;
class URoleCtrlStateMgr;


/*
* 文件名称：CS3PlayerController.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：huting
* 创建时间：2018-04-28
*/

UENUM(BlueprintType)
enum class CONTROL_MODE : uint8
{
	CONTROL_MODE_NORMAL	= 0	UMETA(DisplayName = "Normal"),	///<0-普通模式
	CONTROL_MODE_ACTION	= 1	UMETA(DisplayName = "Action"),	///<1-动作模式
};

UCLASS(BlueprintType)
class CHUANGSHI_API ACS3PlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	ACS3PlayerController();
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	virtual void FlushPressedKeys();

	virtual void GetSeamlessTravelActorList(bool bToEntry, TArray<class AActor*>& ActorList) override;
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void SetMousePosition(float LocationX, float LocationY);

	static void LoadPlayer();

	bool ProcessConsoleExec(const TCHAR* Cmd, FOutputDevice& Ar, UObject* Executor) override;

	///能否控制玩家移动
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		bool CanMoveControl(bool isForceMove = false);

	/*
	*BlueprintCallable, 追踪Actor移动
	*
	*@param TargetActor			目标Actor(AActor*)
	*@param NearbyRange			靠近距离(float)
	*@param TraceMoveCallback	移动结束回调(FTraceMoveCallback)
	*@param IsStopMove			移动结束是否停止移动（bool）
	*@param TraceStopMoveCallback移动结束停止移动后回调(FTraceMoveCallback)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "TraceTargetActor", Category = "Game|Player")
		void BP_TraceTargetActor(const AActor* TargetActor, const float NearbyRange, FTraceMoveCallback TraceMoveCallback);
	void TraceTargetActor(const AActor* TargetActor, const float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());
	void TraceTargetActorAtClient(const AActor* TargetActor, const float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());

	/*
	*BlueprintCallable, 组队跟随
	*
	*@param TargetActor			目标Actor(AActor*)
	*@param NearbyRange			靠近距离(float)
	*@param TraceMoveCallback	移动结束回调(FTraceMoveCallback)
	*@param IsStopMove			移动结束是否停止移动（bool）
	*@param TraceStopMoveCallback移动结束停止移动后回调(FTraceMoveCallback)
	*
	*@return 无
	*/
	void TeamFollowTraceTarget(const AActor* TargetActor, const float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());

	/*
	*BlueprintCallable, 追踪位置移动
	*
	*@param TargetPostion		目标位置(FVector)
	*@param NearbyRange			靠近距离(float)
	*@param TraceMoveCallback	移动结束回调(FTraceMoveCallback)
	*@param IsStopMove			移动结束是否停止移动（bool）
	*@param TraceStopMoveCallback移动结束停止移动后回调(FTraceMoveCallback)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "TraceTargetPostion", Category = "Game|Player")
		void BP_TraceTargetPostion(const FVector& TargetPostion, const float NearbyRange, FTraceMoveCallback TraceMoveCallback);
	void TraceTargetPostion(const FVector& TargetPostion, const float NearbyRange = 0.0f, FTraceCallback TraceCallback = FTraceCallback(), bool IsStopMove = true, FTraceCallback TraceStopMoveCallback = FTraceCallback());

	/*
	*BlueprintCallable, 玩家被击退移动
	*
	*@param TargetPostion		目标位置(FVector)
	*@param TraceMoveCallback	移动结束回调(FTraceMoveCallback)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void MoveBackToPostion(const float MoveSpeed, const FVector& TargetPostion);
	void EndMoveBack();

	/*
	*BlueprintCallable, 飞行移动至位置（要先设置为飞行模式）
	*
	*@param Location		目标位置(FVector)
	*@param IsFlyPatrol		是否是飞行传送移动(bool)
	*@param FlyMoveCallback	移动结束回调(FTraceMoveCallback)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "FlyToLocation", Category = "Game|Player")
		void BP_FlyToLocation(const FVector& Location, const bool IsFlyPatrol, const bool bIsFixedDirection, FTraceMoveCallback FlyMoveCallback);
	void FlyToLocation(const FVector& Location, const bool IsFlyPatrol = false, const bool bIsFixedDirection = false, FTraceCallback FlyCallback = FTraceCallback());

	void AutoNavigateToLocation(const FVector& DstPosition, FString DstSpaceName = "", float NearbyRange = 2.0f, FTraceCallback AutoNavigateCallback = FTraceCallback());

	void OnTestSpaceAllQuestNavigate(const FString& DstSpaceName, const FString& NPCScriptID);

	void StartJumpInAutoNavigate();

	/**
	* @fn	void ConsumeKeyMovementInput();
	*
	* @brief	消耗键盘输入
	*
	* @date	2017/5/27
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void ConsumeKeyMovementInput();

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void ChangeMoveMode(CHANGE_CHARACTER_MOVEMENT_TYPE ChangeMovementType, bool bIsUseCharacterMovement);

	/**
	* @fn	bool ACS3PlayerController::IsCharacterMovementMode();
	*
	* @brief	是否使用CharacterMovement的移动模式来移动
	*
	* @date	2017/7/17
	*
	* @return	True if character movement mode, false if not.
	*/
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		bool IsCharacterMovementMode();

	/*
	*BlueprintPure, 获得当前移动模式
	*
	*@return 移动模式(CS3_MOVE_TYPE)
	*/
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		CS3_MOVE_TYPE GetMoveType();

	/*
	*BlueprintCallable, 停止移动，并清理数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StopMove();

	//获取飞行数据
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		FFLY_MOVE_INFO GetFlyMoveInfo();

	///是否在飞行状态
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		bool IsFlying();

	///限制控制的角色是否能输入
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void EnableInputToControll(bool IsCanInput);

	/*
	*BlueprintCallable, 设置添加摄像机的旋转速度
	*
	*@param ScaleValue		要设置的数值（百分比）
	*@param ScaleHeadle		要设置的Headle,默认为-1,
							此值为默认值或者不存在则
							会创建一个新的值作为返回变量
	*
	*@return 返回输入的ScaleHeadle，或者新建的ScaleHeadle。
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		int32 SetCameraRotateScale(float ScaleValue, int32 ScaleHeadle = -1);

	/*
	*BlueprintCallable, 刷新摄像机旋转速度
	*
	*@return
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void UpdataCameraRotateScale();

	/*
	*BlueprintCallable, 删除摄像机旋转速度系数
	*
	*@param ScaleHeadle		要恢复的Headle,如果Headle无效则恢复失败,恢复成功headle失效
	*
	*@return 是否成功
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		bool RemoveCameraRotateScale(int32 ScaleHeadle);

	/*
	*BlueprintPure, 是否存在这个Headle
	*
	*@param ScaleHeadle		需要检测的Headle
	*
	*@return 是否存在
	*/
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		bool IsHaveCameraHeadle(int32 ScaleHeadle);

	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void AddMovementArray(FVector InputVector, float axis);

#pragma region	/** 玩家输入控制相关 */

	/** 获取控制状态组件 */
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		URoleCtrlStateMgr* GetStateCtrlComp() const {
		return RoleCtrlStateMgr;
	}
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void SetStateCtrlComp(EROLE_CTRL_STATE CtrlState, bool IsEnter, int32 index = 0);

	/** 获取攻击模式状态组件 */
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		UAtkStateMar* GetAtkStateMar() const {
		return AtkStateMar;
	}
	/** 获取控制状态组件 */
	UFUNCTION(BlueprintPure, Category = "Game|Player")
		float GetMoveLeftRight() const {
		return GetInputAxisValue(TEXT("MoveLeft"))+ GetInputAxisValue(TEXT("MoveRight"));
	}
	/** 获取移动控制组件 */
	inline UPlayerControllerMoveComponent* GetMoveControlComponent() const {
		return MoveControlComponent;
	}

	void  SetPlayerControllerMoveComponentTickEnabled(bool bEnabled);
	/** 动态绑定输入事件 */
	virtual void DynamicBindInputEvent(bool bClearOldBind = true, bool bIsPlayer = false);
	///<动态绑定输入事件
	UFUNCTION(BlueprintImplementableEvent, Category = "CS3PlayerController|Input")
		void BP_DynamicBindInputEvent(bool bClearOldBind = true, bool bIsPlayer = false);
	/**
	*保存快捷键设置数据
	*
	*@param SHORTCUTKEY_TYPE_ENUM 快捷键分类
	*@param TArray<FSHORTCUTKEY> 快捷键数组
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void SaveShortcutKeyDataToFile(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> NewKeys, TArray<FSHORTCUTKEY>& OldKeys);

	/**
	*BlueprintCallable快捷键设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void ApplyShortcutKeyData(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> OldKeys);

	/**
	*BlueprintCallable取消快捷键设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void CancelShortcutKeyData(SHORTCUTKEY_TYPE_ENUM Type);

	/**
	*BlueprintCallable修改后未保存的快捷键是否为空
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		bool ChangedShortcutKeysIsEmpty();

	///<获取Type类型的默认快捷键数据
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		TArray<FSHORTCUTKEY> GetDefaultShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);

	///<获取当前Type的快捷键
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		TArray<FSHORTCUTKEY> GetShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);

	///<恢复默认
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void RestoreDefaultShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);

	///<清除键位
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void ClearShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);

	///<修改键位值  bIsResetedData:表示已处理过本地保存快捷键数据与Keys相同的情况
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		FSHORTCUTKEY ChangeShortcutKeyData(FSHORTCUTKEY ShortcutKey, TArray<FKey>Keys, bool bIsMainKey, FKey OldKey, bool bIsAdd, bool& bIsSuccess, FString& MessageID, FString& Param);
	///<根据ActName获取快捷键数据
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void GetShortcutDataByActName(SHORTCUTKEY_TYPE_ENUM KeyType, FName ActName, FSHORTCUTKEY& ShortcutData, bool bIsChangedKeys = false);
	///<根据Keys重置本地已保存的快捷键数据
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		bool ResetShortcutDataByKey(FSHORTCUTKEY ShortcutData, TArray<FKey>Keys, FSHORTCUTKEY& NewShortcutData);

	///<根据Keys重置本地已保存的快捷键数据
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		bool ResetChangedShortcutDataByKey(FSHORTCUTKEY ShortcutData, TArray<FKey>Keys, FSHORTCUTKEY& NewShortcutData);

	///<根据ActName 获取对应的按键信息
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		FString GetKeyNameByActName(FName ActName, FGROUPKEY_DATA& KeyValue);

	///<根据ActName 获取对应的按键是否按下
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		bool IsKeyDownByActName(FName ActName);

	///<通知快捷键改变事件
	UFUNCTION(BlueprintImplementableEvent, Category = "CS3PlayerController|Input")
		void ChangeShortcutKeyDataBP(FSHORTCUTKEY OldShortcutKey, FSHORTCUTKEY NewShortcutKey);

	///<获取所有包含复合键（Shift、Ctrl、Alt、Cmd）有关的键； Key为复合键
	TArray<FSHORTCUTKEY> GetShortcutDataByGroupKey(FKey Key);

	///<某个按键是否已经执行某Act行为按键
	bool CheckKeyExecutedByActionKey(FKey Key);
	/**------------------------------------Behavior-----------------------------**/
	//状态改变
	UFUNCTION(BlueprintImplementableEvent)
		void OnBehaviorChange(EATTACT_STATE CurState, EATTACT_STATE OldState);

	UFUNCTION(BlueprintImplementableEvent)
		void BP_FKeyGossipWith(const AServerCharacter* TargetCharacter);

	//转换控制模式切换快捷键快捷栏绑定的数据
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		void ChangeBindShortcutKeyByControlMode(ECONTROL_MODE NewType, ECONTROL_MODE OldType);
	//鼠标点击地面后触发特效
	UFUNCTION(BlueprintImplementableEvent)
		void MouseClickOnGround();

	/** 监测输入事件是否激活 // @NOTE 该处判断多个状态中有不激活则不激活该输入 */
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindKeyActive(FKey Key);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindActionActive(FName Name);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindAxisActive(FName Name);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindAxisKeyActive(FKey Key);

	/** 监测输入按键是否超过指定时间*/
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckKeyDuration(FKey Key, float time);
	
	/** @ return true if Alt Key went from down to up since player input was last processed. */
	bool WasAltJustPressedOrReleased() const;

	/** @ return true if  Ctrl Key went from down to up since player input was last processed. */
	bool WasCtrlJustPressedOrReleased() const;

	/** @ return true if  Shift Key went from down to up since player input was last processed. */
	bool WasShiftJustPressedOrReleased() const;

	bool WasCmdJustPressedOrReleased() const;
	bool WasKeyJustPressedOrReleased(FKey Key) const;

	void SetUpAndDownAngle(float upAngle, float downAngle);
	UFUNCTION(BlueprintPure)
		float GetWKeyScale();///<获取W键的Scale
	void OnSwitchControlPlayer();///<切换控制目标
	void SetIsEnabledQuickBar(bool IsEnabled) { IsEnabledQuickBar = IsEnabled; };///<设置快捷栏是否可用

	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Input")
		bool UseQuickKey(int32 ShortcutIndex, bool IsMainQuickKey = true);///<使用快捷栏  

	UFUNCTION(BlueprintNativeEvent, Category = "Input")
		bool BP_OnWSADKeyPressed();///<通知界面按下WSAD键

	UFUNCTION(BlueprintNativeEvent, Category = "Input")
		bool OnEscPressed();///<Esc键按下

	UFUNCTION(BlueprintCallable)
		void  ChangeControlModeFromACTToALT(bool bIsActToAlt);///<从ACT模式到ALT模式
	UFUNCTION(BlueprintCallable, Category = "SpawnActor")
		AActor* CS3SpawnActor(UClass* Class, const FTransform& SpawnTransform, ESpawnActorCollisionHandlingMethod CollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn);

	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetPlayerCharacterProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetPlayerTargetProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetRoleModelProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetPetModelProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetPetPenModelProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetHalfHeadModelProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetRoleHalfHeadModelProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetOtherRoleModelProxy();
	UFUNCTION(BlueprintCallable)
		class AGameCharacter* GetTongNagualModelProxy();
	/** 界面相关 */
	void OnResolutionChanged(FViewport* ViewPort, uint32 val);
	/** 获取当前鼠标移动Scale */
	float GetMouseMoveScale();

protected:
	// Begin UObject Func
	virtual void SetupInputComponent() override;
	// ~End UObject Func


	/** 清除绑定输入事件 */
	UFUNCTION(BlueprintCallable, Category = "CS3PlayerController|Input")
		static void ClearInputEvent(AActor* Obj, bool bClearAll = true, EINPUT_TYPE Type = EINPUT_TYPE::IT_Key);

	/** 获取输入配置表及其数据 */
	const UConfigTable* GetInputConfig();
	const FINPUT_DATA* GetInputData(const FString& Id);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		static FString GetKeyName(FKey Key);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckContainsKey(FKey Key, TArray<FString> Keys);

	/** 按键绑定相关 */
	UFUNCTION(BlueprintNativeEvent)
		bool BindKey_AnyKey_Pressed(FKey Key);
	UFUNCTION(BlueprintNativeEvent)
		bool BindKey_AnyKey_Released(FKey Key);

	//调节方向
	UFUNCTION(BlueprintCallable)
		void KeepForward();

	/**------------------------------------Input ActionMappings-----------------------------**/

	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnMouseLeftButtonClick();

	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnMouseRightButtonClick();

	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnJumpPressed();

	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnJumpReleased();

	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnShowSystemUI();

	//以下部分是技能测试功能用
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnSkillAtkCeShi1(); 
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnSkillAtkCeShi2();
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnSkillAtkCeShi3();

	/**------------------------------------Input Key-----------------------------**/
	//以下是闪避技能使用
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnDodgeFront();///<向前闪避
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnDodgeBack();///<向后闪避
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnDodgeLeft();///<向左闪避
	UFUNCTION(BlueprintCallable, Category = "Input")
		void OnDodgeRight();///<向右闪避

	/**------------------------------------WASD Key-----------------------------**/
	UFUNCTION()
		void OnMoveForward(float Scale);///<向前移动
	UFUNCTION()
		void OnMoveRight(float Scale);///<向右移动
	UFUNCTION()
		void OnLookUp(float Scale);///<上下
	UFUNCTION()
		void OnTurn(float Scale);///<旋转
	UFUNCTION()
		void OnMoveUp(float Scale);///<飞行上升

	UFUNCTION()
		void OnTurnForwardReleased(FKey Key);///<WSAD释放事件
	UFUNCTION()
		void OnTurnBackReleased(FKey Key);///<WSAD释放事件
	UFUNCTION()
		void OnTurnLeftReleased(FKey Key);///<WSAD释放事件
	UFUNCTION()
		void OnTurnRightReleased(FKey Key);///<WSAD释放事件
	UFUNCTION()
		void OnTurnForwardPressed(FKey Key);///<WSAD按下事件
	UFUNCTION()
		void OnTurnBackPressed(FKey Key);///<WSAD按下事件
	UFUNCTION()
		void OnTurnLeftPressed(FKey Key);///<WSAD按下事件
	UFUNCTION()
		void OnTurnRightPressed(FKey Key);///<WSAD按下事件

	UFUNCTION()
		void OnSetTarget(FKey Key);///<选择敌人	
	UFUNCTION()
		void OnSelectSelf(FKey Key);///<选择自己
	UFUNCTION()
		void OnSelectTeammate1(FKey Key);///<选择队友1	
	UFUNCTION()
		void OnSelectTeammate2(FKey Key);///<选择队友2
	UFUNCTION()
		void OnSelectTeammate3(FKey Key);///<选择队友3
	UFUNCTION()
		void OnSelectTeammate4(FKey Key);///<选择队友4
	UFUNCTION()
		void OnSelectTargetToTarget(FKey Key);///<选择目标的目标

	UFUNCTION(BlueprintCallable)
		void OnInteractive(FKey Key);///<F交互
	UFUNCTION(BlueprintCallable)
		void OnUsePrompet(FKey Key);///<Z交互
	UFUNCTION()
		void OnUpdatePlayerModlevisible();///<更新玩家的可见性
	UFUNCTION()
		void OnVehicle();///<上下坐骑
	UFUNCTION()
		void OnAutoForward();///<NumLock自动前行
	UFUNCTION()
		void OnPrintScreen();///<截屏
	
	UFUNCTION()
		void ActionModeMouseEvent();

	UFUNCTION()
		void OnMouseScrollBig();///<鼠标中键（滚轮）放大/缩小镜头
	UFUNCTION()
		void OnMouseScrollSmall();///<鼠标中键（滚轮）放大/缩小镜头
	UFUNCTION()
		void OnMouseLeftPressed(FKey Key);///<鼠标左键事件	
	UFUNCTION()
		void OnMouseLeftReleased(FKey Key);///<鼠标左键事件	
	UFUNCTION()
		void OnMouseRightPressed(FKey Key);///<鼠标右键事件	
	UFUNCTION()
		void OnMouseRightReleased(FKey Key);///<鼠标右键事件	

	UFUNCTION()
		void OnMainSkill0(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill1(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill2(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill3(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill4(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill5(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill6(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill7(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill8(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnMainSkill9(FKey Key);///<按0-9释放技能

	UFUNCTION()
		void OnSecondSkill0(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill1(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill2(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill3(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill4(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill5(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill6(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill7(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill8(FKey Key);///<按0-9释放技能
	UFUNCTION()
		void OnSecondSkill9(FKey Key);///<按0-9释放技能
	/**------------------------------------UI Key-----------------------------**/
	UFUNCTION()
		void OnShiftKeyPressed();///<Shift按下或释放事件
	UFUNCTION()
		void OnShiftkeyReleased();///<Shift按下或释放事件
	UFUNCTION()
		void OnCtrlKeyPressed();///<Ctrl按下或释放事件
	UFUNCTION()
		void OnCtrlKeyReleased();///<Ctrl按下或释放事件
	UFUNCTION()
		void OnAltKeyPressed();///<Alt按下或释放事件
	UFUNCTION()
		void OnAltKeyReleased();///<Alt按下或释放事件
	UFUNCTION()
		void OnMouseRightKeyPressed();///<右键取消特殊鼠标
	/**------------------------------------Open Window Key-----------------------------**/
	UFUNCTION()
		void OnShowActivityCalendarUI();///<Shift+C活动日程
	UFUNCTION()
		void OnShowFPSUI();///<显示FPS界面
	UFUNCTION()
		void OnShowBigMapUI();///<Q大地图
	UFUNCTION()
		void OnShowKitbagUI();///<B背包
	UFUNCTION()
		void OnShowEquipUI();///<E打开装备强化界面
	UFUNCTION()
		void OnShowQuestUI();///<L任务列表
	UFUNCTION()
		void OnShowRolePertyUI();///<C人物装备属性
	UFUNCTION()
		void OnShowRelationUI();///<按F打开关系界面
	UFUNCTION()
		void OnShowMemoirUI();///<M仙魔录
	UFUNCTION()
		void OnShowTransportUI();///<传送面板
	UFUNCTION()
		void OnShowSkillUpgradeUI();///<按N打开技能升级界面
	UFUNCTION()
		void OnShowPetUI();///<P打开幻兽界面
	UFUNCTION()
		void OnShowMallUI();///<商城
	UFUNCTION()
		void OnShowHelpSystemUI();///<Shift+G帮助界面
	UFUNCTION()
		void OnCrtlAddOne();///<Ctrl+ 1进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddTwo();///<Ctrl+ 2进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddThree();///<Ctrl+ 3进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddFour();///<Ctrl+ 4进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddFive();///<Ctrl+ 5进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddSix();///<Ctrl+ 6进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddSeven();///<Ctrl+ 5进行占用  CST-7572
	UFUNCTION()
		void OnCrtlAddEight();///<Ctrl+ 6进行占用  CST-7572
private:
	void BindInputData(FName ActName, TArray<FInputKeyEvent> KeyEvents);
	void RemoveBindInputData(FName ActName, TArray<FInputKeyEvent> KeyEvents);
	void OnStopJumping();
	void RecordValueOfInputAxis(float Scale);
	void OnTurnWASDPressed(FString ActionName, FString InputKey);
	void OnUpdateWindow(FName ActionName, TArray<FString> OtherValue);
	UFUNCTION(BlueprintCallable)
		void OnPlayerMoveTypeChanged(CS3_MOVE_TYPE NewMoveType, CS3_MOVE_TYPE OldMoveType);///<移动模式改变回调

	void UseSpaceCopyItemByQuickKey(const int32& index);
#pragma endregion
public:
	///移动控制组件
	UPROPERTY(VisibleAnywhere)
		UPlayerControllerMoveComponent* MoveControlComponent;

	UPROPERTY(BlueprintReadWrite)
		UCS3ConsoleMgr* CS3ConSoleMgr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		AAIController* BehaviorController;

	///是否处于鼠标点击移动状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsMouseClickNavMove = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		CONTROL_MODE ControlMode;///<操作模式
	///改变移动模式的类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<CHANGE_CHARACTER_MOVEMENT_TYPE> ChangeMovementTypes;
	UPROPERTY(BlueprintReadWrite)
		TArray<FVector> MovementInputs;  ///< 对于wasd按键中输入的值进行保存
	UPROPERTY(BlueprintReadWrite)
		bool bIsKeepDirection;///<保持向前朝向
	UPROPERTY(BlueprintReadWrite)
		FVector ForwardVector;///向前
	UPROPERTY(BlueprintReadOnly)
		float SuckMoveSpeed = 0.0f;///<吸力速度
	UPROPERTY(BlueprintReadOnly)
		FVector SuckPosition = FVector::ZeroVector;///<吸力源

	UPROPERTY(BlueprintReadWrite)
		TArray<AActor*> MoveActors;	//过关卡需要携带过关卡的Actor

	UObjectLibrary* ObjectLibrary;
	TArray<FString> SpaceNavigateInfo;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsEnabledQuickBar = true;///是否开启快捷栏

	/** 界面相关 */
	UPROPERTY()
		class AGameCharacter* PlayerCharacterProxy; //角色左上角头像模型代理
	UPROPERTY()
		class AGameCharacter* PlayerTargetProxy;	//目标头像模型代理
	UPROPERTY()
		class AGameCharacter* RoleModelProxy;	//角色属性模型角色代理
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		class AGameCharacter* PetModelProxy;	//幻兽模型代理（用于幻兽界面）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		class AGameCharacter* PetPenModelProxy;	//幻兽/原兽模型代理（用于兽栏界面）
	UPROPERTY()
		class AGameCharacter* HalfHeadModelProxy;	//半身像模型代理
	UPROPERTY()
		class AGameCharacter* RoleHalfHeadModelProxy;	//角色半身像模型代理
	UPROPERTY()
		class AGameCharacter* OtherRoleModelProxy;	//查看玩家属性模型代理	
	UPROPERTY()
		class AGameCharacter* TongNagualModelProxy;	//帮会神兽召唤模型代理	
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsShiftDown;///<Shift键是否按下	
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsCtrlDown;///<Ctrl键是否按下	
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsAltDown;///<Alt键是否按下	
	FVector2D NewReso;///<新分辨率	
	FVector2D PreReso;///<旧分辨率	
	float PreScale;///<旧缩放比
protected:
	/** 状态控制管理相关 */
	UPROPERTY(VisibleAnywhere)
		URoleCtrlStateMgr* RoleCtrlStateMgr;
	UPROPERTY(VisibleAnywhere)
		UAtkStateMar* AtkStateMar;
private:
	TMap<int32, float> CameraRotateScales;
	int32 CameraRotateScaleCount = 0;
	float fDefaultCameraRotateScale = 0.0f;
	float WScale;///<W按下的Scale
	int32 Count = 0;///<W按下次数	
	float UpAngle = -60.0f;///<up角度	
	float DownAngle = 45.0f;///<Down角度

	TMap<FKey, FKeyState> FlushKeyStateMapSkip;//切换焦点重置键盘状态时忽略的按键
};
