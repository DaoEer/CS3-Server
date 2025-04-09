// Fill out your copyright notice in the Description page of Project Settings.


#include "AtkStateMar.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Kismet/KismetMathLibrary.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameData/Item/ItemUse.h"
#include "Interface/Role/RoleReviveInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/Role/RoleInterface.h"
#include "Interface/Monster/MonsterOwnerInterface.h"
#include "GameData/MessageID.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/ConvertUtil.h"
#include "Interface/StateInterface.h"
#include "MapManager.h"
#include "GameDevelop/CS3GameInstance.h"

CONTROL_COMPILE_OPTIMIZE_START

UAtkStateMar::UAtkStateMar()
{
	AddAllState();

	m_DstPosition = FVector::ZeroVector;
	m_NearbyRange = 2.0f;
	m_DstSpaceName = "";
	m_AutoQuestID = 0;
	m_IsSearch = false;
	OldState = EATTACT_STATE::NULL_ATT;
}

UAtkStateMar::~UAtkStateMar()
{

}

void UAtkStateMar::BeginDestroy()
{
	Super::BeginDestroy();
	ActivateState.Empty();
	AllState.Empty();
}

void UAtkStateMar::Leave()
{	
	if (AllState.Num() > 0)
	{
		//删除前恢复到无状态
		SwitchNullAtt(true);
	}	
}

void UAtkStateMar::AddAllState()
{
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::NULL_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::CONTINUITY_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::AUTO_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::AUTO_ONCE_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::SKILL_ONCE_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::AUTO_HOMING_SPELL_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::HALF_HOMING_SPELL_ATT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::AUTO_FIGHT_IN_STORY));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::ARDER_FISH_MODE));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::ARDER_JINGSU_MODE));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_CONFUSION));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_GLIDING));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_SHIELD));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::NAVIGATE_MOVE));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_HEHUA));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_LEIZHEN));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_SHOOT));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_CHAOFENG));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_SHENFENGMIJING));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_FALL));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_BAGUAZHEN));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_FEISHENG));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_MIJING));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_BATTERY));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_GHOSTEYE));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_EQUIPBUILD));
	AllState.Add(UAtkStateBase::Create(EATTACT_STATE::BEHAVIOR_MOVEVEHICLE));
	SwitchNullAtt(true);
}

void UAtkStateMar::SwitchNullAtt(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnNullAtt = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::NULL_ATT)->Enter();
			DelayThis->OnNullAtt = FAtkNoParamDelegate();
		}
	});

	//添加
	AddAttackState(EATTACT_STATE::NULL_ATT);

	//空状态必定激活，会顶掉当前状态
	ActivateFuntion(EATTACT_STATE::NULL_ATT);

	//设置当前状态离开时需要的数据
	CurStateLeaveParameters.Empty();
}

void UAtkStateMar::SwitchContinuityAtt(bool IsActivate)
{

}

void UAtkStateMar::SwitchAutoFight(bool IsActivate, EBreakAutomaticType BreakType, FName level /*= ""*/, FString IDString /*= ""*/)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnAutoFight = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::AUTO_ATT)->Enter();
			DelayThis->OnAutoFight = FAtkNoParamDelegate();
		}
	});

	TArray<FVariant> TemParameters;
	TemParameters.Add(FVariant((uint8)BreakType));
	TemParameters.Add(FVariant(level));

	//激活
	if (IsActivate)
	{
		//替换技能栏时不能自动战斗CST-10788
		if (UUECS3GameInstance::Instance->QuickBarManager->IsReplace)
			return;
		if (AddAttackState(EATTACT_STATE::AUTO_ATT))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters = TemParameters;
			ActivateFuntion(EATTACT_STATE::AUTO_ATT);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::AUTO_ATT, TemParameters);
	}

}

void UAtkStateMar::SwitchAutoOnceAtt(bool IsActivate)
{

}

void UAtkStateMar::SwitchSkillOnceAtt(bool IsActivate)
{

}

void UAtkStateMar::SwitchHomingSpellAtt(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnHomingSpellAtt = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::AUTO_HOMING_SPELL_ATT)->Enter();
			DelayThis->OnHomingSpellAtt = FAtkNoParamDelegate();
		}
	});

	//激活
	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::AUTO_HOMING_SPELL_ATT);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT);
	}
}

void UAtkStateMar::SwitchHalfHomingSpellAtt(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnHalfHomingSpellAtt = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::HALF_HOMING_SPELL_ATT)->Enter();
			DelayThis->OnHalfHomingSpellAtt = FAtkNoParamDelegate();
		}
	});

	//激活
	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::HALF_HOMING_SPELL_ATT))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::HALF_HOMING_SPELL_ATT);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::HALF_HOMING_SPELL_ATT);
	}
}

void UAtkStateMar::SwitchFightInStoryAtt(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnFightInStoryAtt = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::AUTO_FIGHT_IN_STORY)->Enter();
			DelayThis->OnFightInStoryAtt = FAtkNoParamDelegate();
		}
	});

	//激活
	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::AUTO_FIGHT_IN_STORY))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::AUTO_FIGHT_IN_STORY);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::AUTO_FIGHT_IN_STORY);
	}
}

void UAtkStateMar::SwitchFightInXinMo(bool IsActivate, const TArray<FString>& ExcludeSkillList, const TArray<FString>& ActForbidList)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnFightInXinMo= FAtkNoParamDelegate::CreateLambda([DelayThisPtr, ExcludeSkillList, ActForbidList]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			TArray<FVariant> TemParameters;
			TemParameters.Add(UGolbalBPFunctionLibrary::ListToFVariant(ExcludeSkillList));
			TemParameters.Add(UGolbalBPFunctionLibrary::ListToFVariant(ActForbidList));

			DelayThis->FindAtkStateByStateID(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL)->Enter(TemParameters);

			DelayThis->OnFightInXinMo = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		//添加心魔状态
		if (AddAttackState(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL);
		}
	}
	else
	{
		//移除心魔状态
		RemoveAttackState(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL);
	}
}

void UAtkStateMar::SwitchChaoFengMode(bool IsActivate)
{	
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnChaoFengMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_CHAOFENG)->Enter();
			DelayThis->OnChaoFengMode = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		//添加嘲讽
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_CHAOFENG))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_CHAOFENG);
		}
	}
	else
	{
		//移除嘲讽
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_CHAOFENG);
	}
}
void UAtkStateMar::SwitchFishMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnArderFishMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::ARDER_FISH_MODE)->Enter();
			DelayThis->OnArderFishMode = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		//添加钓鱼模式
		if (AddAttackState(EATTACT_STATE::ARDER_FISH_MODE))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::ARDER_FISH_MODE);
		}
	}
	else
	{
		//移除钓鱼模式
		RemoveAttackState(EATTACT_STATE::ARDER_FISH_MODE);
	}
}

void UAtkStateMar::SwitchJingSuMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnArderJingsuMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::ARDER_JINGSU_MODE)->Enter();
			DelayThis->OnArderJingsuMode = FAtkNoParamDelegate();
		}
		
	});

	if (IsActivate)
	{
		//野外竞速模式
		if (AddAttackState(EATTACT_STATE::ARDER_JINGSU_MODE))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::ARDER_JINGSU_MODE);
		}
	}
	else
	{
		//野外竞速模式
		RemoveAttackState(EATTACT_STATE::ARDER_JINGSU_MODE);
	}
}

void UAtkStateMar::SwitchLeiZhenMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnLeiZhenMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_LEIZHEN)->Enter();
			DelayThis->OnLeiZhenMode = FAtkNoParamDelegate();
		}
		
	});

	if (IsActivate)
	{
		//雷阵模式
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_LEIZHEN))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_LEIZHEN);
		}
	}
	else
	{
		//雷阵模式
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_LEIZHEN);
	}
}

void UAtkStateMar::SwitchConfusionMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnConfusionMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_CONFUSION)->Enter();
			DelayThis->OnConfusionMode = FAtkNoParamDelegate();
		}
		
	});

	if (IsActivate)
	{
		//混乱模式
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_CONFUSION))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_CONFUSION);
		}
	}
	else
	{
		//混乱模式
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_CONFUSION);
	}
}

void UAtkStateMar::SwitchGlidingMode(bool IsActivate,float ForwardForceSpeed, float DownForceSpeed)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnGlidingMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr, ForwardForceSpeed, DownForceSpeed]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			TArray<FVariant> TemParameters;
			TemParameters.Add(ForwardForceSpeed);
			TemParameters.Add(DownForceSpeed);

			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_GLIDING)->Enter(TemParameters);

			DelayThis->OnGlidingMode = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		//滑翔模式
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_GLIDING))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_GLIDING);
		}
	}
	else
	{
		//滑翔模式
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_GLIDING);
	}
}

void UAtkStateMar::SwitchPutOnShieldMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnPutOnShieldMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_SHIELD)->Enter();

			DelayThis->OnPutOnShieldMode = FAtkNoParamDelegate();
		}
		
	});

	if (IsActivate)
	{
		//举盾模式
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_SHIELD))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_SHIELD);
		}
	}
	else
	{
		//举盾模式
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_SHIELD);
	}
}

void UAtkStateMar::SwitchOnHehuaMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnHehuaMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_HEHUA)->Enter();
			DelayThis->OnHehuaMode = FAtkNoParamDelegate();
		}
		
	});

	if (IsActivate)
	{
		//荷花模式
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_HEHUA))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_HEHUA);
		}
	}
	else
	{
		//荷花模式
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_HEHUA);
	}
}

void UAtkStateMar::SwitchFlyOrbitMode(bool IsActivate, FString FlyPatrolID, float DelayTime/*=0.0f*/)
{
	OnFlyDeliveryMode = FAtkNoParamDelegate::CreateLambda([FlyPatrolID,this]()
	{
		TArray<FVariant> TemParameters;
		TemParameters.Add(FlyPatrolID);

		FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY)->Enter(TemParameters);

		OnFlyDeliveryMode = FAtkNoParamDelegate();
	});

	if (IsActivate)
	{
		//飞行传送
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY))
		{
			CurStateLeaveParameters.Empty();
			CurStateLeaveParameters.Add(FVariant(FLOAT_TO_FSTRING(DelayTime)));
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY);
		}
	}
	else
	{
		//飞行传送
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY, CurStateLeaveParameters);
	}
}

void UAtkStateMar::SwitchNavigateMoveMode(bool IsActivate, FVector DstPosition,
	float NearbyRange, FString DstSpaceName, int AutoQuestID, bool IsSearch, bool IsArrived, int32 GossipWithType)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnNavigateMoveMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr, GossipWithType]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			TArray<FVariant> TemParameters;
			TemParameters.Add(DelayThis->m_DstPosition);
			TemParameters.Add(DelayThis->m_NearbyRange);
			TemParameters.Add(DelayThis->m_DstSpaceName);
			TemParameters.Add(DelayThis->m_AutoQuestID);
			TemParameters.Add(DelayThis->m_IsSearch);
			TemParameters.Add(GossipWithType);

			DelayThis->FindAtkStateByStateID(EATTACT_STATE::NAVIGATE_MOVE)->Enter(TemParameters);

			DelayThis->OnNavigateMoveMode = FAtkNoParamDelegate();
		}
		
	});

	
	m_DstPosition = DstPosition;
	m_NearbyRange = NearbyRange;
	m_DstSpaceName = DstSpaceName;
	m_AutoQuestID = AutoQuestID;
	m_IsSearch = IsSearch;

	if (IsActivate)
	{
		//自动寻路
		if (AddAttackState(EATTACT_STATE::NAVIGATE_MOVE))
		{
			//设置当前状态离开时需要的数据
			CurStateLeaveParameters.Empty();
			CurStateLeaveParameters.Add(false);
			ActivateFuntion(EATTACT_STATE::NAVIGATE_MOVE);
		}
	}
	else
	{
		TArray<FVariant> TemParameters;
		TemParameters.Add(IsArrived);
		//自动寻路
		RemoveAttackState(EATTACT_STATE::NAVIGATE_MOVE, TemParameters);
	}
}


void UAtkStateMar::SwitchShootMode(bool IsActivate, FString StateType/*=TEXT("")*/, FString Param1/* = TEXT("")*/)
{
	OnShootMode = FAtkNoParamDelegate::CreateLambda([StateType, Param1, this]()
	{
		TArray<FVariant> TemParameters;
		TemParameters.Add(StateType);
		TemParameters.Add(Param1);
		FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_SHOOT)->Enter(TemParameters);

		OnShootMode = FAtkNoParamDelegate();
	});

	if (IsActivate)
	{
		//
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_SHOOT))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_SHOOT);
		}
	}
	else
	{
		//
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_SHOOT);
	}

}

void UAtkStateMar::SwitchShenFengMiJingMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnShenFengMiJingMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_SHENFENGMIJING)->Enter();
			DelayThis->OnShenFengMiJingMode = FAtkNoParamDelegate();
		}
		
	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_SHENFENGMIJING))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_SHENFENGMIJING);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_SHENFENGMIJING);
	}
}

void UAtkStateMar::SwitchFallMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnFallMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_FALL)->Enter();
			DelayThis->OnFallMode = FAtkNoParamDelegate();
		}

	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_FALL))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_FALL);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_FALL);
	}
}

void UAtkStateMar::SwitchBaGuaZhenMode(bool IsActivate, float Scale/* = 10.0f*/)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnBaGuaZhenMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr,Scale]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			TArray<FVariant> TemParameters;
			TemParameters.Add(FLOAT_TO_FSTRING(Scale));
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_BAGUAZHEN)->Enter(TemParameters);
			DelayThis->OnBaGuaZhenMode = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_BAGUAZHEN))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_BAGUAZHEN);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_BAGUAZHEN);
	}
}


void UAtkStateMar::SwitchFeiShengMode(bool IsActivate, float Scale /*= 10.0f*/)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnFeiShengMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr, Scale]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			TArray<FVariant> TemParameters;
			TemParameters.Add(FLOAT_TO_FSTRING(Scale));
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_FEISHENG)->Enter(TemParameters);
			DelayThis->OnFeiShengMode = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_FEISHENG))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_FEISHENG);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_FEISHENG);
	}
}

void UAtkStateMar::SwitchMiJingMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnArderMiJingMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_MIJING)->Enter();
			DelayThis->OnArderMiJingMode = FAtkNoParamDelegate();
		}

	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_MIJING))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_MIJING);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_MIJING);
	}
}

void UAtkStateMar::SwitchBatteryMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnArderBatteryMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_BATTERY)->Enter();
			DelayThis->OnArderBatteryMode = FAtkNoParamDelegate();
		}

	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_BATTERY))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_BATTERY);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_BATTERY);
	}
}

void UAtkStateMar::SwitchGhostEyeMode(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnGhostEyeMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_GHOSTEYE)->Enter();
			DelayThis->OnGhostEyeMode = FAtkNoParamDelegate();
		}

	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_GHOSTEYE))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_GHOSTEYE);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_GHOSTEYE);
	}
}


void UAtkStateMar::SwitchTrainSoldierMode(bool IsActivate, float ArmLength /*= 1500.0f*/, FVector CameraRotation /*= FVector(0.0f, 0.0f, 0.0f)*/)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnTrainSoldierMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr, ArmLength, CameraRotation]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			TArray<FVariant> TemParameters;
			TemParameters.Add(ArmLength);
			TemParameters.Add(CameraRotation);
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER)->Enter(TemParameters);
			DelayThis->OnTrainSoldierMode = FAtkNoParamDelegate();
		}
	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_TRAINSOLDIER);
	}
}

void UAtkStateMar::SwitchEquipBuildMode(bool IsActivate, const FString& ScriptID, const FString& ItemUID)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnEquipBuildMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr, ScriptID, ItemUID]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			if (IsValid(DelayThis))
			{
				TArray<FVariant> TemParameters;
				TemParameters.Add(ScriptID);
				TemParameters.Add(ItemUID);
				DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_EQUIPBUILD)->Enter(TemParameters);
				DelayThis->OnEquipBuildMode = FAtkNoParamDelegate();
			}
		}
	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_EQUIPBUILD))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_EQUIPBUILD);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_EQUIPBUILD);
	}
}

FString UAtkStateMar::GetEquipScriptID()
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_EQUIPBUILD) && IsValid(CurAtkState) && IsValid(Cast<UEquipBuildMode>(CurAtkState)))
	{
		return Cast<UEquipBuildMode>(CurAtkState)->GetEquipScriptID();
	}
	return TEXT("");
}

FString UAtkStateMar::GetEquipItemUID()
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_EQUIPBUILD) && IsValid(CurAtkState) && IsValid(Cast<UEquipBuildMode>(CurAtkState)))
	{
		return Cast<UEquipBuildMode>(CurAtkState)->GetEquipItemUID();
	}
	return TEXT("");
}

void UAtkStateMar::SwitchMoveVehicle(bool IsActivate)
{
	TWeakObjectPtr<UAtkStateMar> DelayThisPtr(this);
	OnMoveVehicleMode = FAtkNoParamDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UAtkStateMar* DelayThis = DelayThisPtr.Get();
			DelayThis->FindAtkStateByStateID(EATTACT_STATE::BEHAVIOR_MOVEVEHICLE)->Enter();
			DelayThis->OnMoveVehicleMode = FAtkNoParamDelegate();
		}

	});

	if (IsActivate)
	{
		if (AddAttackState(EATTACT_STATE::BEHAVIOR_MOVEVEHICLE))
		{
			CurStateLeaveParameters.Empty();
			ActivateFuntion(EATTACT_STATE::BEHAVIOR_MOVEVEHICLE);
		}
	}
	else
	{
		RemoveAttackState(EATTACT_STATE::BEHAVIOR_MOVEVEHICLE);
	}
}

bool UAtkStateMar::IsActivateState(const EATTACT_STATE AttackState)
{
	return FindAtkStateByStateID(AttackState) == CurAtkState;
}

bool UAtkStateMar::IsCurAutoState()
{
	if (IsValid(CurAtkState))
	{
		return CurAtkState->IsAutoState();
	}

	return false;
}

bool UAtkStateMar::IsCanActivateBehav(ECAN_ACTIVATE_BEHAV Behav)
{
	if (IsValid(CurAtkState))
	{
		return CurAtkState->IsCanActivateBehav(Behav);
	}

	return false;
}

void UAtkStateMar::GetXinMoData(TArray<FString>& _ExcludeList, TArray<FString>& _ActForbids)
{
	if (IsHaveState(EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL) && IsValid(CurAtkState) && IsValid(Cast<UAtkFightInXinMoState>(CurAtkState)))
	{
		Cast<UAtkFightInXinMoState>(CurAtkState)->GetXinMoData(_ExcludeList, _ActForbids);
	}
}

#pragma region	行为功能

AActor* UAtkStateMar::SearchTargets(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
	const TArray<ENTITY_FLAG>& MaskFlags,float SearchRange, FVector SearchCenter)
{
	//先获取选中的怪物
	int32 TargetId = UGolbalBPFunctionLibrary::GetTargetEntityID();

	TArray<AActor*> TargetList;

	//判断是否为当前玩家
	if (TargetId != UGolbalBPFunctionLibrary::GetPlayerID())
	{
		AActor* PlayerTarget = UGolbalBPFunctionLibrary::GetActorByID(TargetId);

		if (PlayerTarget && IsValid(PlayerTarget) && (PlayerTarget->GetActorLocation() - SearchCenter).Size() / 100.f < SearchRange)
		{
			TargetList.Add(PlayerTarget);
		}
	}

	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	//获取附近所有目标
	TArray<AActor*> SearchList;

	if (FVector::ZeroVector == SearchCenter)
	{
		SearchList = UGolbalBPFunctionLibrary::GetActorsInRange(SearchClass, SearchRange * 100.0f);
	}
	else
	{
		SearchList = UGolbalBPFunctionLibrary::GetActorsInRange(SearchClass, SearchRange * 100.0f, SearchCenter);
	}

	//判断列表有没有重复
	for (auto TargetActor : TargetList)
	{
		if (TargetActor && IsValid(TargetActor) && SearchList.Contains(TargetActor))
		{
			SearchList.Remove(TargetActor);
		}
	}

	//将搜索到的目标添加到目标列表里
	TargetList.Append(SearchList);

	TArray<AActor*> CanbeAtkActorList;
	for (auto TargetActor : TargetList)
	{
		AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);

		//判断目标是否可以被选为目标
		if (IsValid(TargetCharacter) &&
			IsValid(PlayerCharacter) &&
			IsRelationshipOk(PlayerCharacter, TargetActor, CombatRelation) &&
			!IsTargetHideInGame(PlayerCharacter, TargetCharacter) &&
			!IsEntityBeMask(TargetCharacter->EntityId) &&
			!IsTargetClassBeMask(MaskClass, TargetCharacter) &&
			!IsTargetStateBeMask(MaskState, TargetCharacter) &&
			!IsTargetFlagBeMask(MaskFlags, TargetCharacter)
			)
		{
			CanbeAtkActorList.Add(TargetActor);
			//return TargetActor;
		}
	}
	//排序，打最近的
	if (CanbeAtkActorList.Num())
	{
		CanbeAtkActorList.Sort([SearchCenter](AActor& First, const AActor& Second)->bool
		{
			return (First.GetActorLocation() - SearchCenter).Size() < (Second.GetActorLocation() - SearchCenter).Size();
		});

		return CanbeAtkActorList[0];
	}

	return nullptr;
}

bool UAtkStateMar::IsTargetOK(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState, const TArray<ENTITY_FLAG>& MaskFlags, AActor* TargetActor)
{
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	//判断目标是否可以被选为目标
	if (IsValid(TargetCharacter) &&
		IsValid(PlayerCharacter) &&
		IsRelationshipOk(PlayerCharacter, TargetActor, CombatRelation) &&
		!IsTargetHideInGame(PlayerCharacter, TargetCharacter) &&
		!IsEntityBeMask(TargetCharacter->EntityId) &&
		!IsTargetClassBeMask(MaskClass, TargetCharacter) &&
		!IsTargetStateBeMask(MaskState, TargetCharacter) &&
		!IsTargetFlagBeMask(MaskFlags, TargetCharacter)
		)
	{
		return true;
	}

	return false;
}

AActor* UAtkStateMar::SearchTargetsOfAutoAtt(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
	const TArray<ENTITY_FLAG>& MaskFlags, const TArray<AServerCharacter*>& MaskActors, float SearchRange, FVector SearchCenter, bool bReturnNotInEnemyList)
{
	//先获取选中的怪物
	int32 TargetId = UGolbalBPFunctionLibrary::GetTargetEntityID();
	AActor* PlayerTarget;
	TArray<AActor*> TargetList;

	//判断是否为当前玩家
	if (TargetId != UGolbalBPFunctionLibrary::GetPlayerID())
	{
		PlayerTarget = UGolbalBPFunctionLibrary::GetActorByID(TargetId);

		if (IsValid(PlayerTarget) && (PlayerTarget->GetActorLocation() - SearchCenter).Size() / 100.f < SearchRange && !IsValid((Cast<APlayerCharacter>(PlayerTarget))))
		{
			TargetList.Add(PlayerTarget);
		}
	}

	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerCharacter) || PlayerCharacter->GetSelfEntity() == 0)
	{
		return nullptr;
	}
	//获取附近所有目标
	TArray<AActor*> SearchList;

	if (FVector::ZeroVector == SearchCenter)
	{
		SearchList = UGolbalBPFunctionLibrary::GetActorsInRange(SearchClass, SearchRange * 100.0f);
	}
	else
	{
		SearchList = UGolbalBPFunctionLibrary::GetActorsInRange(SearchClass, SearchRange * 100.0f, SearchCenter);
	}

	//判断列表有没有重复
	for (auto TargetActor : TargetList)
	{
		///<自动战斗只能以可以攻击的怪物为目标，不能以玩家为目标
		if (IsValid(TargetActor) && SearchList.Contains(TargetActor) && (!IsValid(Cast<APlayerCharacter>(TargetActor))))
		{
			SearchList.Remove(TargetActor);
		}
	}

	//将搜索到的目标添加到目标列表里
	TargetList.Append(SearchList);

	TArray<AActor*> CanbeAtkActorList;
	for (auto TargetActor : TargetList)
	{
		AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);
		UMonsterOwnerInterface* MonsterOwnerInterface = Cast<UMonsterOwnerInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("MonsterOwnerInterface"), TargetCharacter->GetSelfEntity()->ID()));
		//判断目标是否可以被选为目标 玩家是否可寻路过去的目标
		if (IsValid(TargetCharacter) &&
			IsValid(PlayerCharacter) &&
			!MaskActors.Contains(TargetCharacter) &&
			IsRelationshipOk(PlayerCharacter, TargetActor, CombatRelation) &&
			!IsTargetHideInGame(PlayerCharacter, TargetCharacter) &&
			!IsEntityBeMask(TargetCharacter->EntityId) &&
			!IsTargetClassBeMask(MaskClass, TargetCharacter) &&
			!IsTargetStateBeMask(MaskState, TargetCharacter) &&
			!IsTargetFlagBeMask(MaskFlags, TargetCharacter) &&
			UGolbalBPFunctionLibrary::FindPathToLocation(TargetCharacter->GetActorLocation()) &&
			((MonsterOwnerInterface && (!MonsterOwnerInterface->hasOwner() || MonsterOwnerInterface->PlayerIsOwner()))|| (MonsterOwnerInterface ==nullptr)))
		{
			CanbeAtkActorList.Add(TargetActor);
			//return TargetActor;
		}
	}

	//排序，在战斗列表中优先级>距离优先级
	if (CanbeAtkActorList.Num())
	{
		CanbeAtkActorList.Sort([SearchCenter](AActor& First, const AActor& Second)->bool
		{
			return (First.GetActorLocation() - SearchCenter).Size() < (Second.GetActorLocation() - SearchCenter).Size();
		});
		///<可被攻击目标列表中是否有当前玩家目标
		if (CanbeAtkActorList.Contains(PlayerTarget))
		{
			return PlayerTarget;
		}

		///<战斗列表
		TMap<int32, int32> EnemyList;
		URoleInterface* RoleInterface = Cast<URoleInterface>(PlayerCharacter->GetEntityInterface_Cache().GameObjectInterface);
		if (RoleInterface)
		{
			EnemyList = RoleInterface->GetEnemyList();
		}
		for (auto TargetActor : CanbeAtkActorList)
		{
			AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);
			if (IsValid(TargetCharacter) && TargetCharacter->GetSelfEntity() != nullptr&& EnemyList.Contains(TargetCharacter->GetSelfEntity()->ID()))
			{
				return TargetActor;
			}
		}
		if (bReturnNotInEnemyList)
		{
			return CanbeAtkActorList[0];
		}
		
	}
	return nullptr;
}

bool UAtkStateMar::IsTargetOKOfAutoAtt(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState, const TArray<ENTITY_FLAG>& MaskFlags, AActor* TargetActor, bool IsCheckPlayerTarget)
{
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	int32 TargetId = UGolbalBPFunctionLibrary::GetTargetEntityID();
	AActor* PlayerTarget;

	//判断是否为当前玩家
	if (IsCheckPlayerTarget && TargetId != UGolbalBPFunctionLibrary::GetPlayerID())
	{
		PlayerTarget = UGolbalBPFunctionLibrary::GetActorByID(TargetId);
		if (IsValid(TargetCharacter) && IsValid(PlayerTarget) && (TargetCharacter != PlayerTarget))
		{
			return false;
		}
	}
	//判断目标是否可以被选为目标 自动战斗只能以可以攻击的怪物为目标，不能以玩家为目标
	if (IsValid(TargetCharacter) &&
		IsValid(PlayerCharacter) &&
		(!IsValid(Cast<APlayerCharacter>(TargetCharacter)))&&
		(TargetCharacter->GetSelfEntity() != nullptr) &&
		IsRelationshipOk(PlayerCharacter, TargetActor, CombatRelation) &&
		!IsTargetHideInGame(PlayerCharacter, TargetCharacter) &&
		!IsEntityBeMask(TargetCharacter->EntityId) &&
		!IsTargetClassBeMask(MaskClass, TargetCharacter) &&
		!IsTargetStateBeMask(MaskState, TargetCharacter) &&
		!IsTargetFlagBeMask(MaskFlags, TargetCharacter) &&
		UGolbalBPFunctionLibrary::FindPathToLocation(TargetCharacter->GetActorLocation())
		)
	{
		UMonsterOwnerInterface* MonsterOwnerInterface = Cast<UMonsterOwnerInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("MonsterOwnerInterface"), TargetCharacter->GetSelfEntity()->ID()));
		if (MonsterOwnerInterface)
		{
			if (!MonsterOwnerInterface->hasOwner() || MonsterOwnerInterface->PlayerIsOwner())
			{
				return true;
			}
		}
	}

	return false;
}

AActor* UAtkStateMar::SearchTargetOfChaoFeng(UClass* SearchClass, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
	const TArray<ENTITY_FLAG>& MaskFlags, float SearchRange, FVector SearchCenter)
{
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	KBEngine::Entity* Entity = PlayerCharacter->GetSelfEntity();
	if (Entity != nullptr)
	{
		int32 TauntID = Entity->GetDefinedProperty(TEXT("TauntID")).GetValue<int32>();
		AActor* PlayerTarget = UGolbalBPFunctionLibrary::GetActorByID(TauntID);

		if (IsTargetOKOfChaoFeng(SearchClass, MaskClass, MaskState, MaskFlags, SearchRange, PlayerTarget))
		{
			return PlayerTarget;
		}
	}
	return nullptr;
}

bool UAtkStateMar::IsTargetOKOfChaoFeng(UClass* SearchClass, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState, const TArray<ENTITY_FLAG>& MaskFlags, float SearchRange, AActor* TargetActor)
{
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	KBEngine::Entity* Entity = PlayerCharacter->GetSelfEntity();
	//判断目标是否可以被选为目标 
	if (IsValid(TargetCharacter) &&
		IsValid(PlayerCharacter) &&
		(Entity != nullptr) &&
		(TargetCharacter->GetSelfEntity() != nullptr) &&
		!IsTargetHideInGame(PlayerCharacter,TargetCharacter) &&
		!IsEntityBeMask(TargetCharacter->EntityId) &&
		!IsTargetClassBeMask(MaskClass, TargetCharacter) &&
		!IsTargetStateBeMask(MaskState, TargetCharacter) &&
		!IsTargetFlagBeMask(MaskFlags, TargetCharacter) &&
		UGolbalBPFunctionLibrary::FindPathToLocation(TargetCharacter->GetActorLocation()) &&
		(UGolbalBPFunctionLibrary::GetActorDistance(TargetCharacter, PlayerCharacter) < SearchRange * 100)
		)
	{
		int32 TauntID = Entity->GetDefinedProperty(TEXT("TauntID")).GetValue<int32>();
		if (TauntID > 0 && (TargetCharacter->GetSelfEntity()->ID() == TauntID))
		{
			return true;
		}
	}
	return false;
}

void UAtkStateMar::MoveToTarget(AActor* Target, float TraceRange, FMoveToDelegate TraceCallback)
{
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		//移动
		PlayerController->TraceTargetActorAtClient(Target, TraceRange, FTraceCallback::CreateLambda([TraceCallback](bool IsSuccess)
		{
			TraceCallback.ExecuteIfBound(IsSuccess);
		}));
	}

}

void UAtkStateMar::MoveToPos(FVector TargetPos, float TraceRange, FMoveToDelegate TraceCallback)
{
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		//移动
		PlayerController->TraceTargetPostion(TargetPos, TraceRange, FTraceCallback::CreateLambda([TraceCallback](bool IsSuccess)
		{
			TraceCallback.ExecuteIfBound(IsSuccess);
		}));
	}
}

bool UAtkStateMar::UseSkill(AServerCharacter* UseCharacter, int32 SkillID, int32 TargetID, FUseSkillForTargetDelegate OnUseSkill)
{
	if (!IsValid(UseCharacter))return false;
	
	USkillInterface* SkillInterface = UseCharacter->GetEntityInterface_Cache().SkillInterface;

	if (IsValid(SkillInterface))
	{
		//使用技能，设置状态，执行回调
		SkillInterface->RealUseSkill(SkillID, TargetID, OnUseSkill);

		return true;
	}
	return false;
}

void UAtkStateMar::CheakUpDropBoxList(AActor* DropBox, TArray<UItemBase*>& CanPickUpItemList)
{
	ADropBoxCharacter* _DropBox = Cast<ADropBoxCharacter>(DropBox);

	if (!IsValid(_DropBox))
	{
		return;
	}

	AddMaskEntityID(_DropBox->EntityId);

	CanPickUpItemList.Empty();

	for (auto _item : _DropBox->GetBoxItemList())
	{
		//判断是否为装备
		if (_item->IsEquip())
		{
			CheakUpEquip(_item, CanPickUpItemList);

			continue;
		}

		//判断是否为任务物品
		if (_item->isQuest())
		{
			if (IsHasPickupType(EAutomaticPickupType::QuestType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}

		//判断是否为晶核
		if (_item->isSpar())
		{
			if (IsHasPickupType(EAutomaticPickupType::SparType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}

		//判断是否为杂物
		if (20001 == _item->ItemType)
		{
			if (IsHasPickupType(EAutomaticPickupType::DebrisType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}

		//判断是否为药品
		if (20002 == _item->ItemType ||
			20003 == _item->ItemType ||
			20004 == _item->ItemType ||
			20005 == _item->ItemType)
		{
			if (IsHasPickupType(EAutomaticPickupType::DrugType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}

		//判断是否为材料
		if (20009 == _item->ItemType)
		{
			if (IsHasPickupType(EAutomaticPickupType::MaterialType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}

		//判断是否为卷轴
		if (20010 == _item->ItemType)
		{
			if (IsHasPickupType(EAutomaticPickupType::ReelType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}

		//判断是否为符咒
		if (20011 == _item->ItemType)
		{
			if (IsHasPickupType(EAutomaticPickupType::SpellType))
			{
				CanPickUpItemList.Add(_item);
			}

			continue;
		}
	}
}

bool UAtkStateMar::UseItem(int32 ID, AServerCharacter* UseCharacter,int32 &ItemUseMsg)
{
	if (!IsValid(UseCharacter))
	{
		return false;
	}

	//获取玩家的背包
	URoleKitBagInterface* KitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));

	if (!IsValid(KitBagInterface))
	{
		CS3_Warning(TEXT("UAtkStateMar::UseItem --- KitBagInterface Is Null!"));
		return false;
	}

	//获取物品
	TArray<UItemBase*> ItemPtrs = KitBagInterface->GetItemsByItemID(ID);

	UItemBase* ItemPtr = nullptr;

	if (ItemPtrs.Num() > 0)
	{
		ItemPtr = ItemPtrs[0];
	}
	else
	{
		ItemUseMsg = 5309;
		CS3_Warning(TEXT("UAtkStateMar::UseItem Don't Find This Item!"));
		return false;
	}

	UItemUse* ItemUsePtr = Cast<UItemUse>(ItemPtr);

	//判断能否使用物品
	if (IsValid(ItemUsePtr))
	{
		//判断物品是否符合使用的条件
		ItemUseMsg = ItemUsePtr->UseQuery(UseCharacter);
		if (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG ==	ItemUseMsg)
		{
			KitBagInterface->RPC_uesItemByShortcutBar(ItemUsePtr->ItemID, UGolbalBPFunctionLibrary::GetTargetEntityID());
			return true;
		}
	}

	return false;
}

void UAtkStateMar::AutoRevive()
{
	AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Player) || !Player->IsState(ENTITY_STATE::EntityStateDead))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAtkStateMar::AutoRevive : Player!"));
		return;
	}

	URoleReviveInterface* ReviveInterface = Cast<URoleReviveInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleReviveInterface")));

	if (IsValid(ReviveInterface))
	{
		int32 Amount = 0;
		int32 NeedAmount = 1;
		int32 reviveByCostItemNumber = 0;
		int32 reviveByCostMoneyNumber = 0;
		int64 money = 0; 
		int64 bindMoney = 0;
		int32 NeedMoney = 1;
		FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_REVIVE_TYPE")));
		TArray<FString> ReviveList = UGolbalBPFunctionLibrary::SplitString(SpaceScriptID);
		KBEngine::Entity* SelfEntity = Player->GetSelfEntity();
		if (SelfEntity)
		{
			reviveByCostItemNumber = SelfEntity->GetDefinedProperty(TEXT("reviveByCostItemNumber")).GetValue<int32>() + 1;
			bindMoney = SelfEntity->GetDefinedProperty(TEXT("bindMoney")).GetValue<int64>();
			money = SelfEntity->GetDefinedProperty(TEXT("money")).GetValue<int64>();
			reviveByCostMoneyNumber = SelfEntity->GetDefinedProperty(TEXT("reviveByCostMoneyNumber")).GetValue<int32>() + 1;
		}
		
		//int32 id = SelfEntity->ID();
		//获取行为interface
		URoleKitBagInterface* RoleKitBag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
		if (IsValid(RoleKitBag))
			Amount = RoleKitBag->GetAmountByItemID(205010001, FIND_BINDTYPE_ENUM::INGOREBIND);
	
		NeedAmount = ReviveInterface->GetReviveCostByOriginType(REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_ITEM, reviveByCostItemNumber);
		NeedMoney = ReviveInterface->GetReviveCostByOriginType(REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_MONEY, reviveByCostMoneyNumber);

		//是否超过死亡深度，摔下悬崖（为true）不能原地复活
		bool IsPlayerUnderArea = UUECS3GameInstance::Instance->MapManager->IsPlayerUnderArea();

		/*归命符箓足够时*/
		if (ReviveList.Contains(INT_TO_FSTRING((int32)REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_ITEM)) && !IsPlayerUnderArea && Amount != 0 && Amount >= NeedAmount)
		{
			ReviveCD = FMath::CeilToInt(UGolbalBPFunctionLibrary::GetPlayerPropertyFloat(TEXT("remainUseItemTime")));
			ReviveCD = FMath::Max(ReviveCD, FMath::CeilToInt(AUTO_REVIVE_DELAY_TIME));
			ReviveCD = ReviveCD + RESURRECTION_PANEL_OPEN_TIME;//要加上复活框延迟弹出的时间，不然跟界面上显示的时间不匹配
			if (ReviveCD > 0)
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ReviveCDTimerHandle, this, &UAtkStateMar::ReviveCDTimerByCostItem, 1.0f, true);
			}
			else
			{
				ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_ITEM);
				this->OnReviveOnOrigin.Broadcast(true);
			}
		}
		//金钱复活
		else if (ReviveList.Contains(INT_TO_FSTRING((int32)REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_MONEY)) && !IsPlayerUnderArea && ((money != 0 && money >= NeedMoney) || (bindMoney > 0 && bindMoney >= NeedMoney)))
		{
			ReviveCD = FMath::CeilToInt(UGolbalBPFunctionLibrary::GetPlayerPropertyFloat(TEXT("remainUseMoneyTime")));
			ReviveCD = FMath::Max(ReviveCD, FMath::CeilToInt(AUTO_REVIVE_DELAY_TIME));
			ReviveCD = ReviveCD + RESURRECTION_PANEL_OPEN_TIME;//要加上复活框延迟弹出的时间，不然跟界面上显示的时间不匹配
			if (ReviveCD > 0)
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ReviveCDTimerHandle, this, &UAtkStateMar::ReviveCDTimerByCostMoney, 1.0f, true);
			}
			else
			{
				ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_MONEY);
				this->OnReviveOnOrigin.Broadcast(true);
			}
		}
		else if(ReviveList.Contains(INT_TO_FSTRING((int32)REVIVE_TYPE::REVIVE_ON_RETURN_POINT)))
		{
			ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_RETURN_POINT);
			SwitchAutoFight(false, EBreakAutomaticType::DeathBreakType);
		}
		else if (ReviveList.Contains(INT_TO_FSTRING((int32)REVIVE_TYPE::REVIVE_ON_SPACE_COPY)))
		{
			ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_SPACE_COPY);
			SwitchAutoFight(false, EBreakAutomaticType::DeathBreakType);
		}
		else if(ReviveList.Contains(INT_TO_FSTRING((int32)REVIVE_TYPE::REVIVE_ON_CITY)))
		{
			ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_CITY);
			SwitchAutoFight(false, EBreakAutomaticType::DeathBreakType);
		}
	}
}

void UAtkStateMar::AddMaskEntityID(int32 EntityID)
{
	if (MaskEntityID.Num() >= 30)
	{
		//删除20个
		MaskEntityID.Empty(10);
	}

	//已经存在就不需要添加
	if (IsEntityBeMask(EntityID))
	{
		return;
	}

	MaskEntityID.Add(EntityID);
}


bool UAtkStateMar::IsEntityBeMask(int32 EntityID)
{
	return MaskEntityID.Contains(EntityID);
}

void UAtkStateMar::SetCanPickUpType(TArray<EAutomaticPickupType> _CanPickupType)
{
	CanPickupType.Empty();

	CanPickupType = _CanPickupType;
}

int32 UAtkStateMar::AddFlyForce(int Dire, float ForceSpeed, float ForceTime)
{
	UGlidingState* GlidingState = Cast<UGlidingState>(CurAtkState);

	if (IsValid(GlidingState))
	{
		return GlidingState->AddFlyForce(Dire, ForceSpeed, ForceTime);
	}
	CS3_Warning(TEXT("UAtkStateMar::AddFlyForce: --- CurAtkState Is Not GlidingState!"));
	return -1;
}

bool UAtkStateMar::IsTargetHideInGame(AServerCharacter* PlayerCharacter, AServerCharacter* TargetCharacter)
{
	UStateInterface * StateInterface = TargetCharacter->GetEntityInterface_Cache().StateInterface;
	if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIDE))
	{
		if (TargetCharacter->QueryRelation(PlayerCharacter) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
		{
			return true;
		}
	}
	return false;
}

float UAtkStateMar::GetBaGuaZhenModeValue()
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_BAGUAZHEN) && IsValid(CurAtkState) && IsValid(Cast<UBaGuaZhenMode>(CurAtkState)))
	{
		return Cast<UBaGuaZhenMode>(CurAtkState)->GetScaleValue();
	}
	return 0.0f;
}

void UAtkStateMar::SetBaGuaZhenModeCanMove(bool InCanMove)
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_BAGUAZHEN) && IsValid(CurAtkState) && IsValid(Cast<UBaGuaZhenMode>(CurAtkState)))
	{
		return Cast<UBaGuaZhenMode>(CurAtkState)->SetCanMove(InCanMove);
	}
}

bool UAtkStateMar::GetBaGuaZhenModeCanMove()
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_BAGUAZHEN) && IsValid(CurAtkState) && IsValid(Cast<UBaGuaZhenMode>(CurAtkState)))
	{
		return Cast<UBaGuaZhenMode>(CurAtkState)->IsCanMove();
	}
	return false;
}

bool UAtkStateMar::IsTargetClassBeMask(const TArray<UClass*>& MaskClasses, AActor* TargetActor)
{
	//如果目标是无效目标则认为他的类型被屏蔽了
	if (!IsValid(TargetActor))
	{
		return true;
	}

	for (auto Parentclass : MaskClasses)
	{
		//判断当前目标的种类被屏蔽了么？
		if (TargetActor->GetClass()->IsChildOf(Parentclass))
		{
			return true;
		}
	}

	return false;
}

bool UAtkStateMar::IsTargetStateBeMask(const TArray<ENTITY_STATE>& MaskStates, AActor* TargetActor)
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(TargetActor);

	//如果目标是无效目标则认为他当前的状态无法被选择为目标
	if (!IsValid(ServerActor))
	{
		return true;
	}

	for (auto TestState : MaskStates)
	{
		//判断当前目标的状态是否是可以被选择为目标的
		if (ServerActor->IsState(TestState))
		{
			return true;
		}
	}

	return false;
}

bool UAtkStateMar::IsTargetFlagBeMask(const TArray<ENTITY_FLAG>& MaskFlags, AActor* TargetActor)
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(TargetActor);

	//如果目标是无效目标则认为他当前的状态无法被选择为目标
	if (!IsValid(ServerActor))
	{
		return true;
	}

	for (auto TestFlag : MaskFlags)
	{
		//判断当前目标的状态是否是可以被选择为目标的
		if (ServerActor->HasFlag(TestFlag))
		{
			return true;
		}
	}

	return false;
}

void UAtkStateMar::CheakUpEquip(UItemBase* _Item, TArray<UItemBase*>& CanPickUpItemList)
{
	switch (_Item->Quality)
	{
	case (int32)QUALITY::QUALITY_WHITE:
		if (IsHasPickupType(EAutomaticPickupType::WhiteType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_BLUE:
		if (IsHasPickupType(EAutomaticPickupType::BlueType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_GOLD:
		if (IsHasPickupType(EAutomaticPickupType::GoldType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_PINK:
		if (IsHasPickupType(EAutomaticPickupType::PinkType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_GREEN:
		if (IsHasPickupType(EAutomaticPickupType::GreenType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_GREEN_TIAN:
		if (IsHasPickupType(EAutomaticPickupType::GreenTianType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_GREEN_SHENG:
		if (IsHasPickupType(EAutomaticPickupType::GreenShengType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	case (int32)QUALITY::QUALITY_GREEN_SHEN:
		if (IsHasPickupType(EAutomaticPickupType::GreenShenType))
		{
			CanPickUpItemList.Add(_Item);
		}
		break;
	default:
		break;
	}
}

bool UAtkStateMar::IsHasPickupType(EAutomaticPickupType ItemType)
{
	return CanPickupType.Contains(ItemType);
}

bool UAtkStateMar::IsRelationshipOk(AActor* Character1, AActor* Character2, COMBAT_RELATION CombatRelation)
{
	if (COMBAT_RELATION::COMBAT_RELATION_DEFAULT == CombatRelation)
	{
		return true;
	}

	AServerCharacter* SearchCharacter = Cast<AServerCharacter>(Character1);
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(Character2);

	if (IsValid(SearchCharacter) && IsValid(TargetCharacter))
	{
		return SearchCharacter->QueryRelation(TargetCharacter) == CombatRelation;
	}

	return false;
}

void UAtkStateMar::ReviveCDTimerByCostItem()
{
	ReviveCD = ReviveCD - 1;
	if (ReviveCD <= 0)
	{
		URoleReviveInterface* ReviveInterface = Cast<URoleReviveInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleReviveInterface")));

		if (IsValid(ReviveInterface))
		{
			ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_ITEM);
			this->OnReviveOnOrigin.Broadcast(true);
		}
		//清除定时器
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ReviveCDTimerHandle);
		}
	}
}

void UAtkStateMar::ReviveCDTimerByCostMoney()
{
	ReviveCD = ReviveCD - 1;
	if (ReviveCD <= 0)
	{
		URoleReviveInterface* ReviveInterface = Cast<URoleReviveInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleReviveInterface")));

		if (IsValid(ReviveInterface))
		{
			ReviveInterface->Revive(REVIVE_TYPE::REVIVE_ON_ORIGIN_BY_COST_MONEY);
			this->OnReviveOnOrigin.Broadcast(true);
		}
		//清除定时器
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ReviveCDTimerHandle);
		}
	}
}

#pragma endregion

bool UAtkStateMar::AddAttackState(const EATTACT_STATE AttackState)
{
	//获取这个状态
	UAtkStateBase* WantAddState = FindAtkStateByStateID(AttackState);

	//判断有效性
	if (!IsValid(WantAddState))
	{
		return false;
	}

	//判断是否已经有这一个状态了
	if (!IsHaveState(AttackState))
	{
		//添加状态
		ActivateState.Add(WantAddState);
	}

	//判断是否能激活
	if (CheakCanActivate(WantAddState))
	{
		if (IsValid(CurAtkState) && WantAddState != CurAtkState)
		{
			OldState = CurAtkState->GetAttState();
			if (!CurAtkState->GetIsleaving())
			{
				CurAtkState->Leave(CurStateLeaveParameters);
				if (CurAtkState->GetAttState()== EATTACT_STATE::NAVIGATE_MOVE)
				{
					ActivateState.Remove(CurAtkState);//移除此状态从激活列表
				}
			}
		}
		return true;
	}
	else
	{
		return false;
	}
}

bool UAtkStateMar::RemoveAttackState(const EATTACT_STATE AttackState, TArray<FVariant> Parameters)
{
	//判断是否有这一个状态了
	if (!IsHaveState(AttackState))
	{
		return false;
	}

	//获取这个状态
	UAtkStateBase* WantRemState = FindAtkStateByStateID(AttackState);

	//判断有效性
	if (IsValid(WantRemState))
	{
		//判断当前状态
		if (CurAtkState == WantRemState )
		{		
			if (!CurAtkState->GetIsleaving())
			{
				WantRemState->Leave(Parameters);
				CurAtkState = nullptr;
				OldState = WantRemState->GetAttState();
				ActivateState.Remove(WantRemState);//移除此状态从激活列表
				CheakAllActiveState();//检查其他所有的状态
			}			
		}
		else
		{
			ActivateState.Remove(WantRemState);//移除此状态从激活列表
			CheakAllActiveState();//检查其他所有的状态
		}	

		return true;
	}

	return false;
}

bool UAtkStateMar::IsHaveState(const EATTACT_STATE AttackState)
{
	for (auto AtkState : ActivateState)
	{
		if (AttackState == AtkState->GetAttState())
		{
			return true;
		}
	}

	return false;
}

FString UAtkStateMar::GetShootModeState()
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_SHOOT))
	{
		UShootMode* ShootMode = Cast<UShootMode>(CurAtkState);
		if (IsValid(ShootMode))
		{
			return ShootMode->GetStateType();
		}		
	}
	return TEXT("");
}

void UAtkStateMar::SetShootModeOtherValue(FString OtherValue)
{
	if (IsHaveState(EATTACT_STATE::BEHAVIOR_SHOOT))
	{
		UShootMode* ShootMode = Cast<UShootMode>(CurAtkState);
		if (IsValid(ShootMode))
		{
			return ShootMode->SetOtherValue(OtherValue);
		}
	}
}
UAtkStateBase* UAtkStateMar::FindAtkStateByStateID(const EATTACT_STATE AttackState)
{
	for (auto AtkState : AllState)
	{
		if (IsValid(AtkState) && (AttackState == AtkState->GetAttState()))
		{
			return AtkState;
		}
	}

	return nullptr;
}

void UAtkStateMar::CheakAllActiveState()
{
	for (auto AtkState : ActivateState)
	{
		if (CurAtkState != AtkState && CheakCanActivate(AtkState))//判断能否激活
		{
			AtkState->Enter();
			ActivateFuntion(AtkState->GetAttState());
		}
	}
}

void UAtkStateMar::ActivateFuntion(const EATTACT_STATE AttackState)
{
	ACS3PlayerController* PlayerCon = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (CurAtkState == FindAtkStateByStateID(AttackState))
	{
		if (IsValid(PlayerCon))
		{
			PlayerCon->OnBehaviorChange(CurAtkState->GetAttState(), OldState);
		}

		return;
	}

	CurAtkState = FindAtkStateByStateID(AttackState);

	switch (AttackState)
	{
	case EATTACT_STATE::NULL_ATT:
		OnNullAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::CONTINUITY_ATT:
		OnContinuityAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::AUTO_ATT:
		OnAutoFight.ExecuteIfBound();
		break;
	case EATTACT_STATE::AUTO_ONCE_ATT:
		OnAutoOnceAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::SKILL_ONCE_ATT:
		OnSkillOnceAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::AUTO_HOMING_SPELL_ATT:
		OnHomingSpellAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::HALF_HOMING_SPELL_ATT:
		OnHalfHomingSpellAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::AUTO_FIGHT_IN_STORY:
		OnFightInStoryAtt.ExecuteIfBound();
		break;
	case EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL:
		OnFightInXinMo.ExecuteIfBound(/*ExcludeList, ActForbids*/);
		break;
	case EATTACT_STATE::ARDER_FISH_MODE:
		OnArderFishMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::ARDER_JINGSU_MODE:
		OnArderJingsuMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_CONFUSION:
		OnConfusionMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_GLIDING:
		OnGlidingMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_SHIELD:
		OnPutOnShieldMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY:
		OnFlyDeliveryMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::NAVIGATE_MOVE:
		OnNavigateMoveMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_HEHUA:
		OnHehuaMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_LEIZHEN:
		OnLeiZhenMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_SHOOT:
		OnShootMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_CHAOFENG:
		OnChaoFengMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_SHENFENGMIJING:
		OnShenFengMiJingMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_FALL:
		OnFallMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_BAGUAZHEN:
		OnBaGuaZhenMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_FEISHENG:
		OnFeiShengMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_MIJING:
		OnArderMiJingMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_BATTERY:
		OnArderBatteryMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_GHOSTEYE:
		OnGhostEyeMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_TRAINSOLDIER:
		OnTrainSoldierMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_EQUIPBUILD:
		OnEquipBuildMode.ExecuteIfBound();
		break;
	case EATTACT_STATE::BEHAVIOR_MOVEVEHICLE:
		OnMoveVehicleMode.ExecuteIfBound();
		break;
	default:
		break;
	}

	if (IsValid(PlayerCon))
	{
		PlayerCon->OnBehaviorChange(CurAtkState->GetAttState(), OldState);
	}
}

bool UAtkStateMar::CheakCanActivate(UAtkStateBase* WantsActivate)
{
	if (!IsValid(WantsActivate))
	{
		return false;
	}

	if (!IsValid(CurAtkState))
	{
		for (auto _AtkState : ActivateState)
		{
			//如果有模式的优先级大于此模式则返回false
			if (_AtkState->GetPriority() > WantsActivate->GetPriority())
			{
				return false;
			}
		}

		return true;
	}

	if (EATTACT_STATE::NULL_ATT == WantsActivate->GetAttState())
	{
		return true;
	}

	if (WantsActivate->GetPriority() >= CurAtkState->GetPriority())
	{
		for (auto _AtkState : ActivateState)
		{
			//如果有模式的优先级大于此模式则返回false
			if (_AtkState->GetPriority() > WantsActivate->GetPriority())
			{
				return false;
			}
		}

		return true;
	}

	return false;
}

CONTROL_COMPILE_OPTIMIZE_END
