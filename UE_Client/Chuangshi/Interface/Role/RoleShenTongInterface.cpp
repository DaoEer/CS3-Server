#include "RoleShenTongInterface.h"
#include "KBEngine.h"
#include "RoleKitBagInterface.h"
#include "GameData/Item/ItemShenTongSkill.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "Manager/SkillManager.h"
#include "Util/ConvertUtil.h"

CONTROL_COMPILE_OPTIMIZE_START
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleShenTongInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateShenTongSKill, &URoleShenTongInterface::UpdateShenTongSKill, const int32&, const int32&, const uint8)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleShenTongInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	

URoleShenTongInterface::URoleShenTongInterface()
{

}


URoleShenTongInterface::~URoleShenTongInterface()
{

}

void URoleShenTongInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_rquestComminution");
	ArrBlueFunc.Add("CLIENT_UpdateShenTongDynamic");
	Supper::InitBlueCB();
}

void URoleShenTongInterface::RPC_RquestComminution(const FString & Suid, const FString & ItemList)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShenTongInterface::RPC_RquestComminution : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Suid);
	args.Add(ItemList);
	entity->CellCall(TEXT("CELL_rquestComminution"), args);
}

void URoleShenTongInterface::CLIENT_rquestComminution_Implementation(const int32& npcID)
{

}

void URoleShenTongInterface::CLIENT_UpdateShenTongDynamic_Implementation(const FString & Suid, const int32& SkillID, const int32& Level, const int32& PreExp, const int32& ReduceUseLevel, const uint8& isComminution)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShenTongInterface::CLIENT_UpdateShenTongDynamic : kitbatInst!"));
		return;
	}
	UItemShenTongSkill* Item = Cast<UItemShenTongSkill>(kitbatInst->FindItemByUID(Suid));
	if (Item)
	{
		Item->SetDynamicData(SkillID, Level, PreExp, ReduceUseLevel, isComminution);
	}
	OnUpdateShenTongDynamic(Suid);
}

void URoleShenTongInterface::UpdateShenTongSKill(const int32 & SkillID, const int32 & Times, const uint8 isAdd)
{
	///当可用次数为0时，移除改技能
	if (Times == 0)
	{
		if (ShenTongSkills.Contains(SkillID))
		{
			ShenTongSkills.Remove(SkillID);
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
			{
				UUECS3GameInstance::Instance->GEventManager->OnRemoveShenTongSKillEvent.Broadcast(SkillID);
			}
		}
		return;
	}

	if (ShenTongSkills.Contains(SkillID))
	{
		ShenTongSkills[SkillID] = Times;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnUpdateShenTongSKillEvent.Broadcast(SkillID, Times);
		}
	}
	else
	{
		ShenTongSkills.Add(SkillID, Times);
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			if(isAdd!=0)
			{ UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("SkillUpgraded")); }			
			UUECS3GameInstance::Instance->GEventManager->OnAddShenTongSKillEvent.Broadcast(SkillID);
		}
	}
	
}

TMap<int32, int32> URoleShenTongInterface::GetShenTongSKills()
{
	return ShenTongSkills;
}

TArray<int32> URoleShenTongInterface::GetShenTongSKillIDs()
{
	TArray<int32> NewShenTongSkillList;
	for (TPair<int32, int32>& Skill : ShenTongSkills)
	{
		NewShenTongSkillList.Add(Skill.Key);
	}
	return NewShenTongSkillList;
}

TArray<int32> URoleShenTongInterface::GetShenTongSKillsSortByIndex()
{
	TArray<int32> NewShenTongSkillList = GetShenTongSKillIDs();
	TWeakObjectPtr<URoleShenTongInterface> DelayThisPtr(this);
	NewShenTongSkillList.Sort([DelayThisPtr](const int32& SkillIDA, const int32& SkillIDB)
	{
		if (DelayThisPtr.IsValid())
		{
			int32 IndexA = DelayThisPtr->GetShenTongSKillCfgBySkillID(SkillIDA).Index;
			int32 IndexB = DelayThisPtr->GetShenTongSKillCfgBySkillID(SkillIDB).Index;
			return IndexA < IndexB;
		}
		return true;
	});
	return NewShenTongSkillList;
}

TArray<int32> URoleShenTongInterface::GetShenTongSKillsSortByLevel()
{
	TArray<int32> NewShenTongSkillList = GetShenTongSKillIDs();
	NewShenTongSkillList.Sort([](const int32& SkillIDA, const int32& SkillIDB)
	{
		USkillData* SkillDataA = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillIDA);
		USkillData* SkillDataB = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillIDB);
		if (!IsValid(SkillDataA) || !IsValid(SkillDataA))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleShenTongInterface::GetShenTongSKillsSortByLevel : SkillData!"));
			return true;
		}
		int32 SkillLevelA = SkillDataA->GetSkillLevel();
		int32 SkillLevelB = SkillDataB->GetSkillLevel();
		if (SkillLevelA == SkillLevelB)
		{
			//等级相同，按技能名字排
			TArray<FString> SplitArrayA = UGolbalBPFunctionLibrary::SplitString(SkillDataA->GetSkillName(), false, "·");
			FString NameA = SplitArrayA[0];
			TArray<FString> SplitArrayB = UGolbalBPFunctionLibrary::SplitString(SkillDataB->GetSkillName(), false, "·");
			FString NameB = SplitArrayB[0];
			return NameA > NameB;
		}
		return SkillLevelA > SkillLevelB;
	});
	return NewShenTongSkillList;
}

TArray<int32> URoleShenTongInterface::GetShenTongSKillsSortByRemainTimes()
{
	TArray<int32> NewShenTongSkillList = GetShenTongSKillIDs();
	TWeakObjectPtr<URoleShenTongInterface> DelayThisPtr(this);
	NewShenTongSkillList.Sort([DelayThisPtr](const int32& SkillIDA, const int32& SkillIDB)
	{
		if (DelayThisPtr.IsValid())
		{
			int32 TimesA = DelayThisPtr->GetShenTongSKillTimes(SkillIDA);
			int32 TimesB = DelayThisPtr->GetShenTongSKillTimes(SkillIDB);
			if (TimesA == TimesB)
			{
				//等级相同，按技能名字排
				USkillData* SkillDataA = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillIDA);
				USkillData* SkillDataB = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillIDB);
				if (!IsValid(SkillDataA) || !IsValid(SkillDataA))
				{
					CS3_Warning(TEXT("-->Null Pointer error:URoleShenTongInterface::GetShenTongSKillsSortByRemainTimes : SkillData!"));
					return true;
				}
				FString SkillNameA = SkillDataA->GetSkillName();
				FString SkillNameB = SkillDataB->GetSkillName();
				TArray<FString> SplitArrayA = UGolbalBPFunctionLibrary::SplitString(SkillNameA, false, "·");
				FString NameA = SplitArrayA[0];
				TArray<FString> SplitArrayB = UGolbalBPFunctionLibrary::SplitString(SkillNameB, false, "·");
				FString NameB = SplitArrayB[0];
				//名字相同则按等级排
				if (NameA.Equals(NameB))
				{
					int32 SkillLevelA = SkillDataA->GetSkillLevel();
					int32 SkillLevelB = SkillDataB->GetSkillLevel();
					return SkillLevelA > SkillLevelB;
				}
				return NameA > NameB;
			}
			return TimesA > TimesB;
		}
		return true;
	});
	return NewShenTongSkillList;
}

int32 URoleShenTongInterface::GetShenTongSKillTimes(const int32 & SkillID)
{
	if (ShenTongSkills.Contains(SkillID))
	{
		return ShenTongSkills[SkillID];
	}
	return 0;
}

FSKILL_SHEN_TONG_TREE_CONFIG URoleShenTongInterface::GetShenTongSKillCfgBySkillID(int32 SkillID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ShenTongSkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SHENTONGSKILLTREE_DATA);
		if (IsValid(ShenTongSkillConfig))
		{
			FName Row = FSTRING_TO_FNAME(INT_TO_FSTRING(SkillID));
			const FSKILL_SHEN_TONG_TREE_CONFIG* TempData = ShenTongSkillConfig->GetRow<FSKILL_SHEN_TONG_TREE_CONFIG>(Row);
			if (TempData)
			{
				FSKILL_SHEN_TONG_TREE_CONFIG* Data = const_cast<FSKILL_SHEN_TONG_TREE_CONFIG*>(TempData);
				if (Data)
				{
					return *Data;
				}
			}
		}
	}
	return FSKILL_SHEN_TONG_TREE_CONFIG();
}

FSKILL_SHEN_TONG_TREE_CONFIG URoleShenTongInterface::GetPetShenTongSKillCfgBySkillID(int32 SkillID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ShenTongSkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET_SHENTONG_SKILL_TREE_DATA);
		if (IsValid(ShenTongSkillConfig))
		{
			FName Row = FSTRING_TO_FNAME(INT_TO_FSTRING(SkillID));
			const FSKILL_SHEN_TONG_TREE_CONFIG* TempData = ShenTongSkillConfig->GetRow<FSKILL_SHEN_TONG_TREE_CONFIG>(Row);
			if (TempData)
			{
				FSKILL_SHEN_TONG_TREE_CONFIG* Data = const_cast<FSKILL_SHEN_TONG_TREE_CONFIG*>(TempData);
				if (Data)
				{
					return *Data;
				}
			}
		}
	}
	return FSKILL_SHEN_TONG_TREE_CONFIG();
}

void URoleShenTongInterface::RPC_LearnPetShenTongSkill(FString PetUid, FString ItemUid)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShenTongInterface::RPC_LearnPetShenTongSkill : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(PetUid);
	args.Add(ItemUid);
	entity->CellCall(TEXT("learnPetShenTongSkill"), args);
}

void URoleShenTongInterface::RPC_DelPetShenTongSkill(FString PetUid, int32 SkillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleShenTongInterface::RPC_DelPetShenTongSkill : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(PetUid);
	args.Add(SkillID);
	entity->CellCall(TEXT("delPetShenTongSkill"), args);
}

CONTROL_COMPILE_OPTIMIZE_END