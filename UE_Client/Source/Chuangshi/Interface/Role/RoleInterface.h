// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/GameObjectInterface.h"
#include "RoleInterface.generated.h"

/*
* 文件名称：RoleInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FSpaceDynamicEffectDelegate, TArray<int32>, EffectList);

UCLASS(BlueprintType)
class CHUANGSHI_API URoleInterface : public UGameObjectInterface
{
	GENERATED_BODY()
		typedef UGameObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	URoleInterface();
	~URoleInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.RoleInterface'"); } //获取蓝图对象路径
	
	/**
	*money(金钱)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	void OnRep_money();

	/**
	*玩家身上拥有的金钱
	*
	*@return int64 金钱
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	void OnRep_bindmoney();

	/**
	*玩家身上拥有的金钱
	*
	*@return int64 金钱
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		int64 GetMoney();
	/**
	*玩家身上拥有的绑定金钱
	*
	*@return int64 绑金
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		int64 GetBindMoney();
	/**
	*获取玩家拥有的金、银、铜
	*
	*@return 金、银、铜
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void GetRoleGoldSilverCopperByMoney(int64& goldValue, int64& silverValue, int64& copperValue);
	/**
	*判断金钱（普通金钱）是否足够
	*
	*moneyValue 需要的金钱
	*
	*@return bool 金钱是否足够
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		bool IsMoneyEnough(int64 moneyValue);

	/**
	*判断绑金是否足够
	*
	*moneyValue 需要的绑金
	*
	*@return bool 绑金是否足够
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		bool IsBindMoneyEnough(int64 moneyValue);

	/**
	*判断金钱（普通金钱和绑金之和）是否足够
	*
	*moneyValue 需要的金钱
	*
	*@return bool 金钱是否足够
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		bool IsAllMoneyEnough(int64 moneyValue);

#pragma region	/** 界面显示金钱文本用 */
	/**
	*money(INT64)属性服务器转换为金
	*
	*@return FString, 金
	*/
	UFUNCTION(BlueprintPure, Category = "cs3|RoleInterface")
		FString GetPlayerStrGold();

	/**
	*money(INT64)属性服务器转换为银
	*
	*@return FString, 银
	*/
	UFUNCTION(BlueprintPure, Category = "cs3|RoleInterface")
		FString GetPlayerStrSilver();

	/**
	*money(INT64)属性服务器转换为铜
	*
	*@return FString, 铜
	*/
	UFUNCTION(BlueprintPure, Category = "cs3|RoleInterface")
		FString GetPlayerStrCopper();
	/**
	*将金钱值转换为金、银、铜
	*
	*@return 金、银、铜
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		bool GetGoldSilverCopperByMoney(int64 moneyValue, FString& goldStr, FString& silverStr, FString& copperStr);
	/**
	*将输入的金、银、铜转换为金钱值
	*
	*@return 金钱值
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		int64 GetMoneyByGoldSilverCopper(FString goldInput, FString silverInput, FString copperInput);

	/**
	*新金钱规则将输入的字符串换为金钱值
	*
	*@return 金钱值
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		int64 GetMoneyByString(FString goldInput);
	/**
	*获得比较后：金值
	*
	*@param goldInput   输入金值
	*@param silverInput 输入银值
	*@param copperInput 输入铜值
	*
	*@return FString 金
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		FString GetCompareGoldValueStr(int64 money, FString goldInput, FString silverInput, FString copperInput);

	/**
	*获得比较后：银值
	*
	*@param goldInput   输入金值
	*@param silverInput 输入银值
	*@param copperInput 输入铜值
	*
	*@return FString 银
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		FString GetCompareSilverValueStr(int64 money, FString goldInput, FString silverInput, FString copperInput);

	/**
	*获得比较后：铜值
	*
	*@param goldInput   输入金值
	*@param silverInput 输入银值
	*@param copperInput 输入铜值
	*
	*@return FString 铜
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		FString GetCompareCopperValueStr(int64 money, FString goldInput, FString silverInput, FString copperInput);

	/**
	*获得比较后：金钱
	*
	*@param goldInput   输入金值
	*
	*@return FString 金值
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		FString GetCompareMoneyValueStr(int64 money, FString goldInput);

#pragma endregion

	/**
	*设置碰撞器种类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnRep_CollisionType();

	/**
	*设置空间动态效果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void OnUpdataEffectData(TArray<int32> EffectList);
	
	/**
	*level(等级)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	void OnRep_level();

	/**
	*killingValue(杀气值)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void OnRep_killingValue();

	/**
	*xiuweiLevel(修为等级)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	void OnRep_xiuweiLevel();

	/**
	*jingjieLevel(境界等级)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void OnRep_jingjieLevel();

	/**
	*玩家修为值
	*
	*@return int32, 修为值
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		int32 GetXiuwei();

	/**
	*onWaterArea(是否在水中)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void OnRep_onWaterArea();

	/**
	*判断当前是否具有RoleFlag标志位
	*
	*@param RoleFlag 需要判断的标志位
	*@param Flags flags属性值
	*
	*@return bool，当前具有RoleFlag返回true，否则为false
	*/
	bool IsInFlags(ROLE_FLAG RoleFlag, int64 Flags);

	/**
	*Direction调用客户端方法播放随机动作（根据服务器发的种子值）
	*
	*@param RandomNumber 种子值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	void PlayRandomAction(int32 RandomNumber);

	/**
	*设置跳跃数据
	*
	*@param InJumpShowType 新的值（float）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void OnSetJumpData(int32 InJumpShowType, float InHeight, float InGravityScale,
			float InBrakingDecelerationFalling, float InMaxWalkSpeed);

	/**
	*设置主角玩家附加重力
	*
	*@param InGravityScalePercentage 重力附件值百分比（float）
	*@param InGravityScaleAddFixed 重力附件值固定增益值（float）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|GameObjectInterface")
		void OnSetPlayerAddGravityScale(float InGravityScalePercentage, float InGravityScaleAddFixed);

	/**
	*同步其他客户端混合空间方向
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void OnSetBlendDir(int32 Dir);
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestBlendDir(float Dir);

	/**
	* 服务器通知同步 远程吃鸡瞄准偏移混合空间方向
	*
	*@param YawValue 水平值
	*@param PitchValue 垂直值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_OnSetAimOffsetBlend(float YawValue, float PitchValue);
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestAimOffsetBlend(float YawValue, float PitchValue);

	/**
	*瞄准绑定武器
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void SetWeapontYCJMD(int32 Type, const FString& SockeName, const FString& PartId);

	/**
	* 服务器通知同步 是否远程吃鸡副本状态
	*
	*@param ShootState 是否射击状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStateInterface")
		void CLIENT_OnRepYCJMDCopyState(uint8 ShootState);
	void RequestChangeYCJMDCopyState(uint8 ShootState);


	/**
	* 服务器通知同步 是否远程吃鸡右键瞄准状态
	*
	*@param AimOffsetState 右键瞄准状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStateInterface")
		void CLIENT_OnRepYCJMDAimOffsetState(uint8 AimOffsetState);
	void RequestYCJMDAimOffsetState(uint8 AimOffsetState);

	/**
	*设置移动类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void OnUpdateMoveType(int32 MoveType);

	///触发周围陷阱
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	void ReTriggerNearTrap(const float& Range);

	/**
	*添加风力
	*
	*@param WindDirectionX 方向，下同
	*@param WindDirectionY
	*@param WindDirectionZ
	*@param WindSpeed 风速度（米）
	*
	*@return 
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void AddAxternalVelocity(const float& WindRotatorX, const float& WindRotatorY, const float& WindRotatorZ, const float& WindSpeed);

	/**
	*更改额外风力百分比（默认为0，更改后风的速度为 speed = speed + speed * Percentage）
	*
	*@param Percentage 百分比
	*
	*@return
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void ChangeAxternalPercentage(const float& Percentage);

	/**
	*移除风力
	*
	*@param WindDirectionX 方向，下同
	*@param WindDirectionY
	*@param WindDirectionZ
	*@param WindSpeed 风速度（米）
	*
	*@return bool，当前具有RoleFlag返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		void RemoveAxternalVelocity(const float& WindRotatorX, const float& WindRotatorY, const float& WindRotatorZ, const float& WindSpeed);
	
	/**
	*获取当前有效的关系规则
	*
	*@return int32
	*/
	UFUNCTION(BlueprintPure, Category = "cs3|RoleInterface")
	int32 GetRelationRule();

	///获取按pk模式决定的战斗关系
	COMBAT_RELATION GetPkModeRelation(KBEngine::Entity* TargetPlayer);

	///获取战斗列表
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
	TMap<int32, int32> GetEnemyList();

	///获取伤害列表
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		TMap<int32, int32> GetDamageList();
	/**
	*Define method
	*野外竞速骑法宝
	*
	*@param SequenceId 过场动画配置表中的每个过场动画资源对应的唯一ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		 void OnMountTalisman(float DelayTime, const FString& CarrierId, float InputYawScale);
	
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		virtual void OnDismountTalisman();
	
	/**
	*Define method
	*玩家在某副本自动前进
	*
	*@param InputYawScale 旋转速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void OnStartRoleAutoMove( float InputYawScale);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void OnDisRoleAutoMove();

	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		virtual void OnPlayerCameraRotation(float RotationTime);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void OnSetClientTime(const FString& diffTime, const int32& severIndex);
	/**
	*Define method
	*BlueprintNativeEvent 播放视频动画
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void OnPlayVideo(const FString& VideoID);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_BreakFalling();
	/**
	*Define method
	*BlueprintNativeEvent 玩家开始匀速下降
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_StartConstantFall();
	/**
	*Define method
	*BlueprintNativeEvent 玩家结束匀速下降
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_EndConstantFall();

	/**
	*Define method
	*BlueprintNativeEvent 玩家开始跳伞下降
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_StartParachuteLand();
	/**
	*Define method
	*BlueprintNativeEvent 玩家结束跳伞下降
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_EndParachuteLand();

	/**
	*Define method
	*BlueprintNativeEvent 玩家新建角色首次进入游戏时，通知弹出操作模式引导界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void FirstEnterGameNotify();

	/**
	*Define method
	*BlueprintNativeEvent 玩家在副本变身后，对变身后的黑衣人切换武器（类似吃鸡捡到武器后更新玩家手中的武器一样）
	*
	**@param Type 武器类型（参照枚举COPY_GAME_WEAPON_ENUM）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
		void CLIENT_SetCopyGameWeapon(int32 Type);
	
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleInterface")
	void OnDodgeRotation();

	// 对战玩家DBID
	FORCEINLINE void updateLHMJChanllengeRelation(const int32& entityID);
	FORCEINLINE const int32 &ChallengePlayerID() { return ChallengeID_; }

	virtual void InitBlueCB() override;

protected:
	virtual void onEnterWorld() override;     ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld() override;     ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void OnEnterScenes() override;	  ///<开始场景
	virtual void OnLeaveScenes() override;    ///<离开场景
private:

	FTimerHandle DropHandle;///<玩家下落检测地面的句柄
	int32 ForceID;///<玩家下落的风力

	FDelegateHandle SetWeapontHandle;
private:
	bool bFirstEnterSpace = true;     ///<第一次进入游戏地图（地图加载完成） 

	int32 ChallengeID_;				// 对战玩家DBID
public:
	bool bIsPlayerCharacterReady;
	UPROPERTY(BlueprintReadOnly, Category = "RoleInterface")
		int32 old_level;///<等级
	UPROPERTY()
		int32 old_xiuweiLevel;///<修为等级
	UPROPERTY()
		int32 old_jingjieLevel;///<境界等级
	UPROPERTY()
		FSpaceDynamicEffectDelegate SpaceDynamicEffectDelegate;

	void onClientSetAoi(const FString& STRING_1);

	void onClientResetAoi();

	void onPlayerUnderArea();///<通知服务器玩家跌落到死亡深度

	void LandEndFalling(float LastVelocitySize);///<通知服务器玩家空中掉落死亡高度

	void enterWaterArea();

	void leaveWaterArea();

	void enterMaterialArea(const FString& STRING_1);

	void leaveMaterialArea(const FString& STRING_1);

	void RequestPlayRandomAction();

	void onLandMovingPlatform(const int32& OBJECT_ID_1);

	void onDeviateMovingPlatform();

	void setPositionFromClient(const FVector& POSITION_1);

	void verifyClientTime(const int32& INT32_1);

	void updateMoveType(const int32& INT32_1);

	void RPC_ChangeFlySpaceEffect(const FString& STRING_1);
};
