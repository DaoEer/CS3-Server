// Fill out your copyright notice in the Description page of Project Settings.
#include "StateInterface.h"
//CS3数据
#include "GameData/TutorialData.h"
#include "GameData/GameDeFine.h"
#include "GameData/EffectEmitterData.h"
//CS3
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/CS3Entity.h"
#include "Actor/ServerCharacter.h"
#include "StateMachine/RoleStateMachine.h"
#include "Manager/ParticleManager.h"
#include "Manager/TutorialManager.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/EnumCsvDefine.h"
#include "Manager/CfgManager.h"
#include "CS3Base/GameObject.h"
CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UStateInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UStateInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
void UStateInterface::onEnterWorld()
{
	InitStateMachine();
	Supper::onEnterWorld();
}

void UStateInterface::InitStateMachine()
{
	if (!RoleStateMachine)
	{
		RoleStateMachine = NewObject<URoleStateMachine>();
		RoleStateMachine->InitStateMap(this->GetEntity());
		RoleStateMachine->InitEffectStateMap();
		RoleStateMachine->InitJumpStateMap();
		RoleStateMachine->InitClimbLadderStateMap();
		EffectStates.SetNum((int32)EFFECT_STATE::EFFECT_STATE_NULL);
	}
}

void UStateInterface::OnStateChanged(const int32& NewState, const int32& OldState)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStateInterface::OnStateChanged : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----Entity ID = %d, change state from %d to %d"), EntityID, OldState, NewState);
	//InitStateMachine();

	ENTITY_STATE ReceiveNewState = (ENTITY_STATE)NewState;
	ENTITY_STATE ReceiveOldState = (ENTITY_STATE)OldState;
	RoleStateMachine->UpdateState(ReceiveNewState);

	//玩家死亡状态触发
	if ((EntityID == UGolbalBPFunctionLibrary::GetPlayerID()) && (ReceiveNewState == ENTITY_STATE::EntityStateDead))
	{
		UGolbalBPFunctionLibrary::TutorialManager()->OnTrigger(ETUTORIALTRIGGERTYPE::DeathTrigger, TEXT(""), TEXT(""));
	}
}

void UStateInterface::OnRep_state()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStateInterface::OnRep_state : GetEntity()!"));
		return;
	}
	int32 oldState;
	oldState = CurrentState;
	CurrentState = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("state"));
	OnStateChanged(CurrentState, oldState);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UStateInterface::OnRep_state------------oldState[%i]-->newState[%i]"),oldState,CurrentState);
}

void UStateInterface::OnEffectStateChanged(const int32& NewEffectState, const int32& OldEffectState)
{
	UpdatePriorityEffectState(NewEffectState, OldEffectState);
	UpdateUnPriorityEffectState(NewEffectState, OldEffectState);

	//更新效果光效
	UpdataEffectByEffectState();
}

void UStateInterface::UpdatePriorityEffectState(const int32 & NewEffectState, const int32 & OldEffectState)
{
	TArray<EFFECT_STATE> ShowEffectState;
	GetEffectStateSortList(ShowEffectState);
	EFFECT_STATE CurState = EFFECT_STATE::EFFECT_STATE_NULL;
	bool IsAddEffect = false;//通知更新的状态是：添加or删除

	/*FString AllStateValueBefor = "";
	for (int32 SatateValue : EffectStates)
	{
		AllStateValueBefor += INT_TO_FSTRING(SatateValue);
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("STATE Entity=%d  addBefor [EffectStates= (%s)]"), EntityID, *AllStateValueBefor);*/

	for (auto IT : ShowEffectState)
	{
		uint32 EffectStateValue = uint32(1) << uint32(IT);
		CurState = IT;
		if ((EffectStateValue & NewEffectState) != 0 && (EffectStateValue & OldEffectState) == 0)
		{
			EffectStates[int32(IT)] = 1;
			IsAddEffect = true;
			break;
		}
		if ((EffectStateValue & NewEffectState) == 0 && (EffectStateValue & OldEffectState) != 0)
		{
			EffectStates[int32(IT)] = 0;
			IsAddEffect = false;
			break;
		}
	}

	/*FString AllStateValueEnd = "";
	for (int32 SatateValue : EffectStates)
	{
		AllStateValueEnd += INT_TO_FSTRING(SatateValue);
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("STATE Entity=%d  addEnd [EffectStates= (%s)]"), EntityID, *AllStateValueEnd);*/

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("STATE Entity=%d  [AddEffect=%d,  (CurState=%d),   new=%d,  old=%d]"),
		EntityID, IsAddEffect ? 1 : 0, (int32)CurState, NewEffectState, OldEffectState);

	if (!IsAddEffect)
		RoleStateMachine->OnDelEffectState(CurState);
	///检测是否有其他效果状态
	///条件：[本次此操作为删除 或者 本次新添加的状态]
	///注意：本次新加的状态是1，但有优先级顺序不一定能成功添加效果(OnAddEffectState()) 
	for (int32 i = 0; i < ShowEffectState.Num(); i++)
	{
		EFFECT_STATE FindState = ShowEffectState[i];
		if (EffectStates[(int32)FindState] == 1)
		{
			if (!IsAddEffect || (IsAddEffect && CurState == FindState))
				RoleStateMachine->OnAddEffectState(FindState);
			break;
		}
	}
}

void UStateInterface::UpdateUnPriorityEffectState(const int32 & NewEffectState, const int32 & OldEffectState)
{
	TArray<EFFECT_STATE> ShowEffectState;
	ShowEffectState.Add(EFFECT_STATE::EFFECT_STATE_HIDE);

	for (auto IT : ShowEffectState)
	{
		uint32 EffectStateValue = uint32(1) << uint32(IT);
		if ((EffectStateValue & NewEffectState) != 0 && (EffectStateValue & OldEffectState) == 0)
		{
			RoleStateMachine->OnAddEffectState(IT);
		}
		else if ((EffectStateValue & NewEffectState) == 0 && (EffectStateValue & OldEffectState) != 0)
		{
			RoleStateMachine->OnDelEffectState(IT);
		}
	}
}

void UStateInterface::OnRep_effectState_Implementation()
{
	if (!GetActor())
		return;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("add effect succeed!"));
	int32 oldEffectState;
	oldEffectState = CurrentEffectState;
	CurrentEffectState = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("effectState"));
	if (!RoleStateMachine)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStateInterface::OnRep_effectState : RoleStateMachine!"));
		return;
	}
	OnEffectStateChanged(CurrentEffectState, oldEffectState);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UStateInterface::OnRep_effectState------------oldEffectState[%i]-->CurrentEffectState[%i]"), oldEffectState, CurrentEffectState);
}

bool UStateInterface::IsActionForbid(const ACTION_FLAG& actionFlag)
{
	uint32 actionFlagValue = uint32(1) << uint32(actionFlag);
	uint32 actForbid = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("actForbid"));
	return (actForbid & actionFlagValue) != 0;
}

bool UStateInterface::HasEffectState(const EFFECT_STATE EffectState)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStateInterface::HasEffectState : GetEntity()!"));
		return false;
	}
	uint32 EffectStateValue = uint32(1) << uint32(EffectState);
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("=============GetEntity=%d,    EntityID=%d"), GetEntity()->ID(), EntityID);
	uint32 Effect_State = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("effectState"));
	return (Effect_State & EffectStateValue) != 0;
}
bool UStateInterface::IsHasEffectStates()
{
	if (HasEffectState(EFFECT_STATE::EFFECT_STATE_SLEEP) || HasEffectState(EFFECT_STATE::EFFECT_STATE_DIZZY) || 
		HasEffectState(EFFECT_STATE::EFFECT_STATE_HIT_BACK)||HasEffectState(EFFECT_STATE::EFFECT_STATE_WIND))
	{
		return true;
	}
	else
	{
		return false; 
	}

}

void UStateInterface::GetCurEffectState(EFFECT_STATE& EffectState)
{
	if (!RoleStateMachine)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStateInterface::GetCurEffectState : RoleStateMachine!"));
		return;
	}
	TArray<EFFECT_STATE> ShowEffectState;
	GetEffectStateSortList(ShowEffectState);
	for (int32 i = 0; i < ShowEffectState.Num(); i++)
	{
		EFFECT_STATE FindState = ShowEffectState[i];
		if (EffectStates[(int32)FindState] == 1)
		{
			EffectState = FindState;
			break;
		}
	}
}


void UStateInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}

void UStateInterface::UpdataEffectByEffectState()
{
	//获取配置数据
	auto EffectStateTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_EFFECTSTATE_EFFECT);
	
	TArray<FEffectState_Effect_DATA*> AllRows; 
	EffectStateTable->GetAllRows(AllRows);

	//检查光效是否有效
	for (TMap<EFFECT_STATE, FStateParticles>::TIterator TBegin = CurEffectMap.CreateIterator(); TBegin; ++TBegin)
	{
		bool isValid = true;
		for (auto EffectUID : TBegin->Value.EffectUIDList)
		{
			if (!UUECS3GameInstance::Instance->ParticleManager->CheckEffectValidByUID(EffectUID))
			{
				isValid = false;
				break;
			}	
		}
		if (isValid && !TBegin->Value.EffectUIDList.Num())
		{
			isValid = false;
		}
		if (!isValid)
		{
			TBegin.RemoveCurrent();
		}
	}
	
	for (auto TableValue : AllRows)
	{
		//判断此状态光效已经激活
		if (CurEffectMap.Contains(TableValue->EffectStateData))
		{
			//判断此状态是否激活
			if (HasEffectState(TableValue->EffectStateData))
			{
				continue;
			}
			else
			{
				//移除光效
				for (auto EffectUID : CurEffectMap[TableValue->EffectStateData].EffectUIDList)
				{
					UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID);
				}
				CurEffectMap.Remove(TableValue->EffectStateData);
			}
		}
		else
		{
			//判断此状态是否激活
			if (HasEffectState(TableValue->EffectStateData))
			{
				UParticleManager* ParticleManager = UGolbalBPFunctionLibrary::ParticleManager();
				if (IsValid(ParticleManager))
				{
					FStateParticles NewStateParticles;
					CurEffectMap.Add(TableValue->EffectStateData, NewStateParticles);

					//添加光效
					for (auto _EffectID : TableValue->EffectIDs)
					{
						int32 EffectUID = ParticleManager->PlayParticle(_EffectID, 0.0f, GetActor(), GetActor());
						if (CurEffectMap.Contains(TableValue->EffectStateData))
						{
							CurEffectMap[TableValue->EffectStateData].EffectUIDList.Add(EffectUID);
						}
					}
				}
			}
		}
	}
}

void UStateInterface::GetEffectStateSortList(TArray<EFFECT_STATE> &StateDatas)
{
	//此顺序是按效果状态优先级添加，慎改之
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_SLEEP);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_DIZZY);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_CONFUSION);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_INVINCIBLE);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_HIT_BACK);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_FIX);
	StateDatas.Add(EFFECT_STATE::EFFECT_STATE_FREEZE);
}

CONTROL_COMPILE_OPTIMIZE_END
