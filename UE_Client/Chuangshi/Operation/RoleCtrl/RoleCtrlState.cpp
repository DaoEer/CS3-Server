// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleCtrlState.h"
#include "KBEngine.h"
#include "Chuangshi.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"

CONTROL_COMPILE_OPTIMIZE_START

URoleCtrlBase::URoleCtrlBase()
	:Super()
	,CtrlState(EROLE_CTRL_STATE::RCS_COMMON)
	, CtrlStateDataIndex(0)
{
	// 默认初始化
	if (StaticClass() == URoleCtrlBase::StaticClass()) InitData();
}

URoleCtrlBase::~URoleCtrlBase()
{
}

URoleCtrlBase* URoleCtrlBase::Create(UObject* Outer, EROLE_CTRL_STATE State)
{
	switch (State)
	{
	// 创建通用控制状态
	case EROLE_CTRL_STATE::RCS_COMMON:
	{
		return NewObject<URoleCtrlBase>(Outer);
	}
	// 创建飞行控制状态
	case EROLE_CTRL_STATE::RCS_FLY:
	{
		return NewObject<UFlyCtrlState>(Outer);
	}
	// 创建变身控制状态
	case EROLE_CTRL_STATE::RCS_CHANGE_BODY:
	{
		return NewObject<UChangeBodyState>(Outer);
	}
	// 创建剧情控制状态
	case EROLE_CTRL_STATE::RCS_STORY:
	{
		return NewObject<UStoryCtrlState>(Outer);
	}
	// 创建仙魔录触发控制状态
	case EROLE_CTRL_STATE::RCS_MEMOIR:
	{
		return NewObject<UMemoirCtrlState>(Outer);
	}
	//心魔附身触发控制状态
	case EROLE_CTRL_STATE::RCS_XINMO: 
	{
		return NewObject<UXinMoCtrlState>(Outer);
	}
	//野外竞速触发控制状态
	case EROLE_CTRL_STATE::RCS_JING_SU:
	{
		return NewObject<UJiingSuCtrlState>(Outer);
	}
	//钓鱼控制状态
	case EROLE_CTRL_STATE::RCS_FISH:
	{
		return NewObject<UGoFishingCtrlState>(Outer);
	}
	//混乱控制状态
	case EROLE_CTRL_STATE::RCS_CONFUSION:
	{
		return NewObject<UGoConfusionState>(Outer);
	}
	//滑翔控制状态
	case EROLE_CTRL_STATE::RCS_GLIDING:
	{
		return NewObject<UGlidingKeyState>(Outer);
	}
	//滑翔控制状态
	case EROLE_CTRL_STATE::RCS_SHIELD:
	{
		return NewObject<UPutOnShieldState>(Outer);
	}
	//举盾控制状态
	case EROLE_CTRL_STATE::RCS_FLY_ORBIT:
	{
		return NewObject<UFlyOrbitState>(Outer);
	}
	//火灵符射击状态
	case EROLE_CTRL_STATE::RCS_HUOLINGFU:
	{
		return NewObject<UHUOLINGFUState>(Outer);
	}
	//镇海弓状态
	case EROLE_CTRL_STATE::RCS_ZHENHAIGONG:
	{
		return NewObject<UZhenHaiGongCtrlState>(Outer);
	}
	//摆摊状态
	case EROLE_CTRL_STATE::RCS_STALL:
	{
		return NewObject<UStallCtrlState>(Outer);
	}
	//十方城状态
	case EROLE_CTRL_STATE::RCS_SHIFANGCHENG:
	{
		return NewObject<UShiFangChengCtrlState>(Outer);
	}
	//对话状态
	case EROLE_CTRL_STATE::RCS_TALK:
	{
		return NewObject<UTalkCtrlState>(Outer);
	}
	// 操作火炮状态
	case EROLE_CTRL_STATE::RCS_BATTERY:
	{
		return NewObject<UBatteryCtrlState>(Outer);
	}
	//鬼瞳之眼探查状态
	case EROLE_CTRL_STATE::RCS_GHOSTEYE:
	{
		return NewObject<UGhostEyeCtrlState>(Outer);
	}
	//勇闯绝命岛射击状态
	case EROLE_CTRL_STATE::RCS_YCJMD:
	{
		return NewObject<UYCJMDCtrlState>(Outer);
	}
	//推箱子向下俯视状态
	case EROLE_CTRL_STATE::RCS_OBERLOOK:
	{
		return NewObject<UOVERLOOKState>(Outer);
	}
	default:
	{
		CS3_Warning(TEXT("URoleCtrlBase::Create -> Input State is Invalid, Create Fail~"));
	}break;
	}

	return nullptr;
}

bool URoleCtrlBase::CheckKeyActive(FKey Key)
{
	FString Id = INT_TO_FSTRING((int32) CtrlState);
	const FSHORTCUTKEY_DATA* SK_Data = GetShortcutKeyData(Id);
	// 未配置该状态默认激活
	if (!SK_Data|| SK_Data->ShortcutKeyCtrl.Num()<=0|| (CtrlStateDataIndex >=SK_Data->ShortcutKeyCtrl.Num())) return true;
	FSHORTCUTKEYCTRL ShortcutKeyCtrl = SK_Data->ShortcutKeyCtrl[CtrlStateDataIndex];
	// 配置不激活所有按键
	if (ShortcutKeyCtrl.bNotActiveAnyKey) return false;
	// 配置只激活按键链表
	if (ShortcutKeyCtrl.OnlyActiveKeys.Num() > 0 &&
		!ShortcutKeyCtrl.OnlyActiveKeys.Contains(Key))
	{
		return false;
	}
	// 配置不激活按键链表
	if (ShortcutKeyCtrl.NotActiveKeys.Num() > 0 &&
		ShortcutKeyCtrl.NotActiveKeys.Contains(Key))
	{
		return false;
	}
	return true;
}

bool URoleCtrlBase::CheckActionActive(FName Name)
{
	FString Id = INT_TO_FSTRING((int32)CtrlState);
	const FSHORTCUTKEY_DATA* SK_Data = GetShortcutKeyData(Id);
	// 未配置该状态默认激活
	if (!SK_Data || SK_Data->ShortcutKeyCtrl.Num() <= 0 || (CtrlStateDataIndex >= SK_Data->ShortcutKeyCtrl.Num())) return true;
	FSHORTCUTKEYCTRL ShortcutKeyCtrl = SK_Data->ShortcutKeyCtrl[CtrlStateDataIndex];

	// 配置不激活动作输入链表
	if (ShortcutKeyCtrl.bNotActiveAnyActions) return false;
	// 配置只激活动作输入链表
	if (ShortcutKeyCtrl.OnlyActiveActions.Num() > 0 &&
		!ShortcutKeyCtrl.OnlyActiveActions.Contains(Name))
	{
		return false;
	}

	// 配置不激活动作输入链表
	if (ShortcutKeyCtrl.NotActiveActions.Num() > 0 &&
		ShortcutKeyCtrl.NotActiveActions.Contains(Name))
	{
		return false;
	}
	return true;
}

bool URoleCtrlBase::CheckAxisActive(FName Name)
{
	FString Id = INT_TO_FSTRING((int32)CtrlState);
	const FSHORTCUTKEY_DATA* SK_Data = GetShortcutKeyData(Id);
	// 未配置该状态默认激活
	if (!SK_Data || SK_Data->ShortcutKeyCtrl.Num() <= 0 || (CtrlStateDataIndex >= SK_Data->ShortcutKeyCtrl.Num())) return true;
	FSHORTCUTKEYCTRL ShortcutKeyCtrl = SK_Data->ShortcutKeyCtrl[CtrlStateDataIndex];

	// 配置不激活轴输入链表
	if (ShortcutKeyCtrl.NotActiveAxis.Num() > 0 &&
		ShortcutKeyCtrl.NotActiveAxis.Contains(Name))
	{
		return false;
	}
	return true;
}

bool URoleCtrlBase::CheckAxisKeyActive(FKey Key)
{
	FString Id = INT_TO_FSTRING((int32)CtrlState);
	const FSHORTCUTKEY_DATA* SK_Data = GetShortcutKeyData(Id);
	// 未配置该状态默认激活
	if (!SK_Data || SK_Data->ShortcutKeyCtrl.Num() <= 0 || (CtrlStateDataIndex >= SK_Data->ShortcutKeyCtrl.Num())) return true;
	FSHORTCUTKEYCTRL ShortcutKeyCtrl = SK_Data->ShortcutKeyCtrl[CtrlStateDataIndex];


	// 配置不激活轴输入链表
	if (ShortcutKeyCtrl.NotActiveAxisKey.Num() > 0 &&
		ShortcutKeyCtrl.NotActiveAxisKey.Contains(Key))
	{
		return false;
	}
	return true;
}

void URoleCtrlBase::SetCtrlStateDataIndex(int32 ctrlStateDataIndex /*= 0*/)
{
	if (CtrlStateDataIndex < 0)
	{
		CtrlStateDataIndex = 0;
		return;
	}
	CtrlStateDataIndex = ctrlStateDataIndex;
}

const FString URoleCtrlBase::ToString() const
{
	switch (CtrlState)
	{
	case EROLE_CTRL_STATE::RCS_COMMON:		return FString("RCS_COMMON");
	case EROLE_CTRL_STATE::RCS_FLY:			return FString("RCS_FLY");
	case EROLE_CTRL_STATE::RCS_CHANGE_BODY: return FString("RCS_CHANGE_BODY");
	case EROLE_CTRL_STATE::RCS_STORY:		return FString("RCS_STORY");
	case EROLE_CTRL_STATE::RCS_MEMOIR:		return FString("RCS_MEMOIR");
	case EROLE_CTRL_STATE::RCS_XINMO:		return FString("RCS_XINMO");
	case EROLE_CTRL_STATE::RCS_JING_SU:		return FString("RCS_JING_SU");
	case EROLE_CTRL_STATE::RCS_FISH:		return FString("RCS_FISH");
	case EROLE_CTRL_STATE::RCS_CONFUSION:	return FString("RCS_CONFUSION");
	case EROLE_CTRL_STATE::RCS_GLIDING:	    return FString("RCS_GLIDING");
	case EROLE_CTRL_STATE::RCS_SHIELD:	    return FString("RCS_GLIDING");
	case EROLE_CTRL_STATE::RCS_FLY_ORBIT:	return FString("RCS_FLY_ORBIT");
	case EROLE_CTRL_STATE::RCS_HUOLINGFU:   return FString("RCS_HUOLINGFU");
	case EROLE_CTRL_STATE::RCS_HEHUA:		return FString("RCS_HEHUA");
	case EROLE_CTRL_STATE::RCS_LEIZHEN:		return FString("RCS_LEIZHEN");
	case EROLE_CTRL_STATE::RCS_ZHENHAIGONG:	return FString("RCS_ZHENHAIGONG");
	case EROLE_CTRL_STATE::RCS_STALL:		return FString("RCS_STALL");
	case EROLE_CTRL_STATE::RCS_SHIFANGCHENG:return FString("RCS_SHIFANGCHENG");
	case EROLE_CTRL_STATE::RCS_TALK        :return FString("RCS_TALK");
	case EROLE_CTRL_STATE::RCS_YCJMD       :return FString("RCS_YCJMD");
	case EROLE_CTRL_STATE::RCS_OBERLOOK    :return FString("RCS_OBERLOOK");
	}
	return FString("RCS_NONE");
}

const UConfigTable* URoleCtrlBase::GetShortcutKeyConfig()
{
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)
	{
		return UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SHORTCUT_KEY);
	}
	return nullptr;
}

const FSHORTCUTKEY_DATA* URoleCtrlBase::GetShortcutKeyData(const FString& Id)
{
	const UConfigTable* ShortcutKeyConfig = GetShortcutKeyConfig();
	return (IsValid(ShortcutKeyConfig)) ? ShortcutKeyConfig->GetRow<FSHORTCUTKEY_DATA>(Id) : nullptr;
}

void URoleCtrlBase::InitData()
{
}

UFlyCtrlState::UFlyCtrlState()
	:Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_FLY;
}

void UFlyCtrlState::OnEnter()
{

}

void UFlyCtrlState::OnLeave()
{

}

UChangeBodyState::UChangeBodyState()
	:Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_CHANGE_BODY;
}

void UChangeBodyState::OnEnter()
{

}

void UChangeBodyState::OnLeave()
{

}

UStoryCtrlState::UStoryCtrlState()
	:Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_STORY;
}

UMemoirCtrlState::UMemoirCtrlState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_MEMOIR;
}

UXinMoCtrlState::UXinMoCtrlState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_XINMO;
}

UJiingSuCtrlState::UJiingSuCtrlState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_JING_SU;
}

UGoFishingCtrlState::UGoFishingCtrlState() 
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_FISH;
}

UGoConfusionState::UGoConfusionState() 
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_CONFUSION;
}

UGlidingKeyState::UGlidingKeyState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_GLIDING;
}

UPutOnShieldState::UPutOnShieldState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_SHIELD;
}

UFlyOrbitState::UFlyOrbitState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_FLY_ORBIT;
}

UHUOLINGFUState::UHUOLINGFUState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_HUOLINGFU;
}

UOnHehuaState::UOnHehuaState()
	: Super()
{
	CtrlState = EROLE_CTRL_STATE::RCS_HEHUA;
}


ULeiZhenCtrlState::ULeiZhenCtrlState()
{
	CtrlState = EROLE_CTRL_STATE::RCS_LEIZHEN;
}

CONTROL_COMPILE_OPTIMIZE_END
