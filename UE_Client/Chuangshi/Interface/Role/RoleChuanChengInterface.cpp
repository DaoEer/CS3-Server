#include "RoleChuanChengInterface.h"
#include "KBEngine.h"
#include "RoleKitBagInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "Manager/SkillManager.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/UIManager.h"
#include "GameData/Item/ItemFactory.h"
#include "Manager/MessageManager.h"

CONTROL_COMPILE_OPTIMIZE_START
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleChuanChengInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnUnlockChuanChengSkillBar, &URoleChuanChengInterface::OnUnlockChuanChengSkillBar, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateChuanChengSkillBar, &URoleChuanChengInterface::UpdateChuanChengSkillBar, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleChuanChengInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	

URoleChuanChengInterface::URoleChuanChengInterface()
{

}


URoleChuanChengInterface::~URoleChuanChengInterface()
{

}

void URoleChuanChengInterface::onEnterWorld()
{
	Init();
	Super::onEnterWorld();
}

void URoleChuanChengInterface::onLeaveWorld()
{
	ClearAllData();
	Super::onLeaveWorld();
}

void URoleChuanChengInterface::Init()
{
	
}

void URoleChuanChengInterface::ClearAllData()
{
	
}

void URoleChuanChengInterface::OnUnlockChuanChengSkillBar(const int32 & index)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUnlockChuanChengSkillBarEvent.Broadcast(index);
	}
}

void URoleChuanChengInterface::UpdateChuanChengSkillBar(const FVariant & data)
{
	FCHUANCHENG_SKILL_BAR_DATA *Temp = new FCHUANCHENG_SKILL_BAR_DATA(data);
	if (ChuanChengSkillBarData.Contains(Temp->id))
	{
		ChuanChengSkillBarData.Remove(Temp->id);
	}
	ChuanChengSkillBarData.Add(Temp->id, *Temp);

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateChuanChengSkillBarEvent.Broadcast(Temp->id);
	}
}

void URoleChuanChengInterface::GetChuanChengSkillBarData(int32 id, uint8 & isLock, int32 & skillID)
{
	isLock = 1;//Ëø×¡
	skillID = 0;
	if (ChuanChengSkillBarData.Contains(id))
	{
		isLock = ChuanChengSkillBarData[id].isLock;
		skillID = ChuanChengSkillBarData[id].skillID;
	}
}

bool URoleChuanChengInterface::IsLoadChuanChengSkill(int32 SkillID)
{
	for (TPair<int32, FCHUANCHENG_SKILL_BAR_DATA>& SkillData : ChuanChengSkillBarData)
	{
		if (UUECS3GameInstance::Instance->SkillManager->IsSameSkill(SkillData.Value.skillID, SkillID))
		{
			return true;
		}
	}
	return false;
}

TArray<int32> URoleChuanChengInterface::GetSortChuanChengSkillList()
{
	TArray<int32> NewChuanChengSkillList;
	TArray<int32> PlayerSkillList = UUECS3GameInstance::Instance->SkillManager->GetPlayerSkillIdList();
	for (auto SkillID : PlayerSkillList)
	{
		if (UUECS3GameInstance::Instance->SkillManager->IsChuanChengSkill(SkillID))
		{
			NewChuanChengSkillList.Add(SkillID);
		}
	}
	NewChuanChengSkillList.Sort([](const int32& SkillIDA, const int32& SkillIDB)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			int32 IndexA = UUECS3GameInstance::Instance->SkillManager->GetChuanChengSkillTreeCfgBySkillID(SkillIDA).Index;
			int32 IndexB = UUECS3GameInstance::Instance->SkillManager->GetChuanChengSkillTreeCfgBySkillID(SkillIDB).Index;
			return IndexA < IndexB;
		}
		return true;
	});
	return NewChuanChengSkillList;
}

TArray<int32> URoleChuanChengInterface::GetLoadChuanChengSkillList()
{
	TArray<int32> SkillIDs;
	for (int32 Index = 0; Index < 4; Index++)
	{
		if (ChuanChengSkillBarData.Contains(Index))
		{
			int32 SkillID = ChuanChengSkillBarData[Index].skillID;
			if (SkillID != 0)
			{
				SkillIDs.Add(SkillID);
			}
		}
	}
	return SkillIDs;
}

void URoleChuanChengInterface::RPC_RequestFitChuanChengSkill(int32 skillID, int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChuanChengInterface::RPC_RequestFitChuanChengSkill : entity!"));
		return;
	};

	KBEngine::FVariantArray Args;
	Args.Add(skillID);
	Args.Add(index);
	entity->CellCall(TEXT("requestFitChuanChengSkill"), Args);
}
void URoleChuanChengInterface::RPC_RequestUnloadChuanChengSkill(int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChuanChengInterface::RPC_RequestUnloadChuanChengSkill : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(index);
	entity->CellCall(TEXT("requestUnloadChuanChengSkill"), Args);
}

void URoleChuanChengInterface::RPC_RequestUnlockChuanChengSkillBar(int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChuanChengInterface::RPC_RequestUnlockChuanChengSkillBar : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(index);
	entity->CellCall(TEXT("requestUnlockChuanChengSkillBar"), Args);
}

void URoleChuanChengInterface::RPC_RequestChuanChengSkillUpgrade(int32 skillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChuanChengInterface::RPC_RequestChuanChengSkillUpgrade : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(skillID);
	entity->CellCall(TEXT("requestChuanChengSkillUpgrade"), Args);
}

CONTROL_COMPILE_OPTIMIZE_END