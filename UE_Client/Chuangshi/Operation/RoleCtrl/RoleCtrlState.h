#pragma once

#include "GameData/ShortcutKeyData.h"
#include "GameData/CS3Object.h"
#include "RoleCtrlState.generated.h"
/*
* 文件名称：RoleCtrlState.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：huting
* 创建时间：2018-04-28
*/


class UConfigTable;
/**
 *	#角色状态基类
 */
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API URoleCtrlBase : public UCS3Object
{
	GENERATED_BODY()

public:
	URoleCtrlBase();
	~URoleCtrlBase();

	/** 创建不同类型实例 */
	UFUNCTION(BlueprintCallable, Category = "RoleCtrlBase|Create")
	static URoleCtrlBase* Create(UObject* Outer, EROLE_CTRL_STATE State = EROLE_CTRL_STATE::RCS_COMMON);

	/** 获取相关数据 */
	inline const EROLE_CTRL_STATE GetCtrlState() const {
		return CtrlState;
	}

	/** 检测输入是否激活 */
	bool CheckKeyActive(FKey Key);
	bool CheckActionActive(FName Name);
	bool CheckAxisActive(FName Name);
	bool CheckAxisKeyActive(FKey Key);

	/** 输出状态字符 */
	UFUNCTION(BlueprintPure, Category = "RoleCtrlBase|String")
	const FString ToString() const;
	void SetCtrlStateDataIndex(int32 ctrlStateDataIndex = 0);
protected:
	/** 进入该状态 */
	virtual void OnEnter() {}
	/** 离开该状态 */
	virtual void OnLeave() {}
	/** 保存数据 */
	virtual void SaveDatas() {}
	/** 加载数据 */
	virtual void LoadDatas() {}

	/** 初始化相关数据 */
	virtual void InitData();

	/** 获取配置表相关数据 */
	const UConfigTable* GetShortcutKeyConfig();
	const FSHORTCUTKEY_DATA* GetShortcutKeyData(const FString& Id);

protected:
	/** 控制状态 */
	UPROPERTY(VisibleAnywhere)
	EROLE_CTRL_STATE CtrlState;

	/** 配置表中采用的数据索引 
	*如：在镜头状态中有俩种配置：1、在不隐藏玩家的可以操作玩家摄像机的控制配置2、默认控制配置
	*/
	UPROPERTY(VisibleAnywhere)
		int32 CtrlStateDataIndex = 0;
};


/*
 *	#飞行控制状态
 */
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UFlyCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UFlyCtrlState();
	~UFlyCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override;
	/** 离开该状态 */
	virtual void OnLeave() override;

};


/*
 *	#变身控制状态
 */
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UChangeBodyState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UChangeBodyState();
	~UChangeBodyState() {}

	/** 进入该状态 */
	virtual void OnEnter() override;
	/** 离开该状态 */
	virtual void OnLeave() override;

};


/*
 *	#剧情控制状态
 */
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UStoryCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UStoryCtrlState();
	~UStoryCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}

};

/*
*	#仙魔录触发控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UMemoirCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UMemoirCtrlState();
	~UMemoirCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}

};


/*
*	#心魔附身控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UXinMoCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UXinMoCtrlState();
	~UXinMoCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#野外竞速控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UJiingSuCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UJiingSuCtrlState();
	~UJiingSuCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#钓鱼控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UGoFishingCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UGoFishingCtrlState();
	~UGoFishingCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#混乱控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UGoConfusionState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UGoConfusionState();
	~UGoConfusionState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#滑翔控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UGlidingKeyState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UGlidingKeyState();
	~UGlidingKeyState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#举盾控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UPutOnShieldState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UPutOnShieldState();
	~UPutOnShieldState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#举盾控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UFlyOrbitState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UFlyOrbitState();
	~UFlyOrbitState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
}; 

/*
*	#举盾控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UHUOLINGFUState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UHUOLINGFUState();
	~UHUOLINGFUState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#举盾控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UOnHehuaState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UOnHehuaState();
	~UOnHehuaState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#雷阵控制状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ULeiZhenCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	ULeiZhenCtrlState();
	~ULeiZhenCtrlState() {}

	/** 进入该状态 */
	virtual void OnEnter() override {}
	/** 离开该状态 */
	virtual void OnLeave() override {}
};

/*
*	#镇海弓状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UZhenHaiGongCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UZhenHaiGongCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_ZHENHAIGONG; };

};

/*
*	#摆摊状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UStallCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UStallCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_STALL; };

};
/*
*	#十方城
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UShiFangChengCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UShiFangChengCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_SHIFANGCHENG; };
};

/*
*	#对话状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UTalkCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UTalkCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_TALK; };
};

/*
*	#操作炮台状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UBatteryCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UBatteryCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_BATTERY; };
};

/*
*	#鬼瞳之眼探查状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UGhostEyeCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UGhostEyeCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_GHOSTEYE; };
};

/*
*	#勇闯绝命岛射击状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UYCJMDCtrlState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UYCJMDCtrlState() { CtrlState = EROLE_CTRL_STATE::RCS_YCJMD; };
};

/*
*	#推箱子向下俯视状态
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UOVERLOOKState : public URoleCtrlBase
{
	GENERATED_BODY()

public:
	UOVERLOOKState() { CtrlState = EROLE_CTRL_STATE::RCS_OBERLOOK; };
};