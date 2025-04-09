
#include "SkillManager.h"
#include "ResourceManager.h"
#include "Util/ConvertUtil.h"
#include "GameData/Skill/SkillTableData.h"
#include "GameData/Skill/PassiveSkillTableData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/SkillInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameData/Item/ItemUse.h"
#include "GameData/ConstData.h"
#include"Chuangshi.h"
#include "Component/Role/JumpComponent.h"
#include "CustomTimerManager.h"
#include "Skill//SkillLoader.h"
#include "GameData/EntityProperty/CombatDamagerLoader.h"
#include "CS3Base/GameObject.h"

#if WITH_EDITOR
#include "Editor.h"
#endif
#include "Interface/Role/RoleInterface.h"
#include "Util/CS3Debug.h"
#include "GameData/Skill/SkillUIData.h"

CONTROL_COMPILE_OPTIMIZE_START

USkillManager::USkillManager()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
	{
		UUECS3GameInstance::Instance->SkillLoader->loadAllSkill();
	}
	UCombatDamagerLoader::GetInstance()->loadAllData();
	SetSkillLearnTableDatas();
	InitChuanChengSkillLearnTableDatas();
	InitPetSkillLearnTableDatas();
	
	ForbidJumpSkillIDs.Empty();
}

USkillManager::~USkillManager()
{

}

USkillManager* USkillManager::GetInstance()
{
	cs3_checkNoReentry();

	return (USkillManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SkillManager")));
}
void USkillManager::UpdateSelfSkillData(int32 SkillId, bool IsAddSkill)
{
	if (IsAddSkill)
	{
		PlayerSkillIdList.RemoveAll([this, SkillId](int32 & skillID) { return IsSameSkill(skillID, SkillId); });
		AddTotalSkillData(SkillId);
		PlayerSkillIdList.Add(SkillId);
		CheckJumpMaxCount(SkillId);
		SetSkillTreeData(SkillId);
		SetPassiveListData(SkillId);
		if (LearnSkillIDs.Contains(SkillId))
		{
			RemoveSkillLearnDataByID(SkillId);
		}
	}
	else
	{
		if (PlayerSkillIdList.Contains(SkillId))
		{
			PlayerSkillIdList.Remove(SkillId);
		}
		RemoveSkillTreeDataByID(SkillId);
		RemovePassiveListDataByID(SkillId);
		if (LearnSkillIDs.Contains(SkillId))
		{
			AddSkillLearnDataByID(SkillId);
		}
	}
}



void USkillManager::InitActPetSkills(TArray<int32> SkillIds)
{
	VPetSkillIdList = SkillIds;
	for (int32 skillID : SkillIds)
	{
		AddTotalSkillData(skillID);
	}
}

void USkillManager::RemoveActPetSkills()
{
	VPetSkillIdList.Empty();
}
void USkillManager::onEnterWorld()
{
#if WITH_EDITOR
	if (GEditor)
	{
		GEditor->GetEditorSubsystem<UImportSubsystem>()->OnAssetReimport.AddUObject(this, &USkillManager::UpdateSkillTable);
	}
#endif
	InitActionSkillData();
}

void USkillManager::onLeaveWorld()
{
	RemoveActPetSkills();
	PlayerSkillIdList.Empty();
	totalSkillData.Empty();
	SkillLearnDatas.Empty();
	SkillTreeUIDatas.Empty();
	SkillPassiveTreeDatas.Empty();
	ActionSkillDatas.Empty();
	ForbidJumpSkillIDs.Empty();
	TeacherID = 0;
}


void USkillManager::UpdateSkillCoolDown(TMap<int32, FSKILL_UPDATE_COOL_DOWN> UpdateSkillCdList)
{
	for (auto CD: UpdateSkillCdList)
	{
		if (AttrCooldowns.Contains(CD.Key))
		{
			StopCdTime(CD.Key);
			AttrCooldowns[CD.Key] = CD.Value;
		}
		else
		{
			AttrCooldowns.Add(CD.Key, CD.Value);
		}
		StartCdTime(CD.Key, AttrCooldowns[CD.Key].RemainingTime);
	}
	TArray<USkillData*> skillList;
	UCS3EntityInterface* baseinterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
	if (IsValid(baseinterface))
	{
		URoleKitBagInterface* kbinterface = Cast<URoleKitBagInterface>(baseinterface);
		if (IsValid(kbinterface))
		{
			skillList.Append(kbinterface->GetItemSkillDataList());
		}
	}
	for (auto skillData : totalSkillData)
	{
		skillList.Add(skillData.Value);
	}
	for (USkillData* SkillData : skillList)
	{
		if (!IsValid(SkillData) || !SkillData->IsSkillDataValid())
		{
			CS3_Warning(TEXT("-->Null Pointer error:UQuestEntityVisibleManager::UpdateAroundQuestEntityVisible : SkillData||SkillData->IsSkillDataValid()!"));
			continue;
		}
		TArray<FSKILL_COOL_DOWN> CasterCoolDownList = SkillData->GetCasterCoolDown();
		bool isShowCD = false;
		for (FSKILL_COOL_DOWN CoolDown : CasterCoolDownList)
		{
			if (UpdateSkillCdList.Contains(CoolDown.CooldownId))
				isShowCD = true;			
		}
		if (!isShowCD)
		{
			continue;
		}
		float _RemainTime = -1.0;
		float _PersistTime = -1.0;
		for (FSKILL_COOL_DOWN CoolDown : CasterCoolDownList)
		{
			if (AttrCooldowns.Contains(CoolDown.CooldownId))
			{
				FSKILL_UPDATE_COOL_DOWN UpdateCdData = AttrCooldowns[CoolDown.CooldownId];
				float RemainingTime = 0.0;
				if (AttrCooldowns[CoolDown.CooldownId].RemainingTime <= 0.0)
				{
					AttrCooldowns.Remove(CoolDown.CooldownId);

				}
				else 
				{
					RemainingTime = GetRemainingTime(CoolDown.CooldownId);
				}

				if (_RemainTime < RemainingTime || (FMath::IsNearlyEqual(_RemainTime, RemainingTime) && _PersistTime < UpdateCdData.PersistTime))
				{
					_RemainTime = RemainingTime;
					_PersistTime = UpdateCdData.PersistTime;
				}
			}

		}
		if (_RemainTime >= 0.0)
		{
			SkillData->StartCdTime(_RemainTime);
			SkillData->SetPersistTime(_PersistTime);
			UCS3EntityInterface* skillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
			Cast<USkillInterface>(skillInterface)->OnSetCooldown(FSTRING_TO_INT(SkillData->GetID().ToString()), _RemainTime, _PersistTime);
			UCS3EntityInterface* kitbagInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"));
			Cast<URoleKitBagInterface>(kitbagInterface)->OnSetCooldown(FSTRING_TO_INT(SkillData->GetID().ToString()), _RemainTime, _PersistTime);
		}
	}
}


void USkillManager::StartCdTime(int32 CDID,float TimeRemaining)
{
	if (TimeRemaining <= 0.1f)
		return;
	FTimerHandle TempTimerHandle;
	TWeakObjectPtr<USkillManager> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TempTimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr, CDID]()
	{
		if (DelayThisPtr.IsValid())
		{
			USkillManager* ThisPtr = DelayThisPtr.Get();
			if (ThisPtr->CdTimerHandle.Contains(CDID))
			{
				ThisPtr->CdTimerHandle.Remove(CDID);
			}
		}
	}), TimeRemaining, false);

	if (CdTimerHandle.Contains(CDID))
	{
		CdTimerHandle[CDID] = TempTimerHandle;
	}
	else
	{
		CdTimerHandle.Add(CDID, TempTimerHandle);
	}
	
}

float USkillManager::GetRemainingTime(int32 CDID)
{
	if (CdTimerHandle.Contains(CDID))
	{
		return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(CdTimerHandle[CDID]);
	}
	else
	{
		return -1.f;
	}
}

const FSKILL_TABLE_DATA* USkillManager::GetSkillTableDataById(FString SkillId) const
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* SkillConfigTest = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SKILL_TEST);
		const FSKILL_TABLE_DATA* _SkillTestTableData = SkillConfigTest->GetRow<FSKILL_TABLE_DATA>(SkillId);
		if (_SkillTestTableData)
		{
			return _SkillTestTableData;
		}
		else
		{
			const UConfigTable* SkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SKILL);
			const FSKILL_TABLE_DATA* _SkillTableData = SkillConfig->GetRow<FSKILL_TABLE_DATA>(SkillId);
			if (_SkillTableData)
			{
				return _SkillTableData;
			}
		}
	}

	return nullptr;
}

TArray<FName> USkillManager::GetRowNamesFromSkillCfg()
{
	TArray<FName> RowNames;
	
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* SkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SKILL);
		RowNames = SkillConfig->GetRowNames();

		const UConfigTable* SkillConfigTest = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SKILL_TEST);
		for (auto RowName : SkillConfigTest->GetRowNames())
		{
			if (!RowNames.Contains(RowName))
			{
				RowNames.Add(RowName);
			}
		}
	}

	return RowNames;
}

void USkillManager::StopCdTime(int32 CDID)
{

	if (CdTimerHandle.Contains(CDID) && CdTimerHandle[CDID].IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CdTimerHandle[CDID]);
	}
}

void USkillManager::ClearSkillCoolDown()
{
	for (auto SkillData : totalSkillData)
	{
		if (SkillData.Value)
		{
			SkillData.Value->StopCdTime();
			UCS3EntityInterface* skillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
			Cast<USkillInterface>(skillInterface)->OnSetCooldown(FSTRING_TO_INT(SkillData.Value->GetID().ToString()), 0.0f, 0.0f);
		}	
	}
	UCS3EntityInterface* kitbagInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"));
	for (auto item : Cast<URoleKitBagInterface>(kitbagInterface)->FKB_ItemList)
	{
		if (item->SkillID != 0)
		{
			UItemUse* ItemUse = Cast<UItemUse>(item);
			if (IsValid(ItemUse))
			{
				ItemUse->StopCdTime();
				Cast<URoleKitBagInterface>(kitbagInterface)->OnSetCooldown(item->SkillID, 0.0f, 0.0f);
			}	
		}
	}
	//清空CD数据
	for (TPair<int32, FSKILL_UPDATE_COOL_DOWN>& CDData : AttrCooldowns)
	{
		StopCdTime(CDData.Key);
	}
	AttrCooldowns.Empty();
}

USkillData* USkillManager::GetSkillDataById(int32 SkillId)
{
	if (totalSkillData.Contains(SkillId))
	{
		return totalSkillData.FindRef(SkillId);
	}
	return CreateSkillDataById(SkillId);
}

USkillData* USkillManager::CreateSkillDataById(int32 SkillId)
{
	USkillData* SkillData = nullptr;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	
	const FSKILL_TABLE_DATA* _SkillTableData = GetSkillTableDataById(INT_TO_FSTRING(SkillId));

	const FSKILL_TABLE_DATA* SkillTableData = _SkillTableData;
	if (SkillTableData)
	{
		SkillData = USkillData::CreateSkillData(SkillTableData);
	}
	else
	{
		const UConfigTable* PassiveSkillConfig =  CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PASSIVE_SKILL);
		const FPASSIVE_SKILL_TABLE_DATA* PassiveSkillTableData = PassiveSkillConfig->GetRow<FPASSIVE_SKILL_TABLE_DATA>(INT_TO_FSTRING(SkillId));
		if (PassiveSkillTableData)
		{
			SkillData = USkillData::CreatePassiveSkillData(PassiveSkillTableData);
		}
	}
	return SkillData;
}

UTexture2D* USkillManager::GetIconBySkillID(int32 SkillId)
{
	if (totalSkillData.Contains(SkillId))
	{
		return totalSkillData.FindRef(SkillId)->GetIcon();
	}
	const FSKILL_TABLE_DATA* SkillTableData = GetSkillTableDataById(INT_TO_FSTRING(SkillId));
	if (SkillTableData)
	{
		TSoftObjectPtr<UTexture2D> TextureIcon = SkillTableData->SkillIcon;;

		if (IsValid(TextureIcon.Get()))
		{
			return TextureIcon.Get();
		}

		if (TextureIcon.ToSoftObjectPath().IsValid())
		{
			UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(TextureIcon.ToSoftObjectPath());
		}

		return TextureIcon.Get();
	}

	const UConfigTable* PTextureTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PASSIVE_SKILL);
	const FPASSIVE_SKILL_TABLE_DATA* PassiveSkillTableData = PTextureTable->GetRow<FPASSIVE_SKILL_TABLE_DATA>(INT_TO_FSTRING(SkillId));
	if (PassiveSkillTableData)
	{
		TSoftObjectPtr<UTexture2D> PTextureIcon = PassiveSkillTableData->SkillIcon;;

		if (IsValid(PTextureIcon.Get()))
		{
			return PTextureIcon.Get();
		}

		if (PTextureIcon.ToSoftObjectPath().IsValid())
		{
			UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(PTextureIcon.ToSoftObjectPath());
		}

		return PTextureIcon.Get();
	}
	return nullptr;
}

void USkillManager::AddTotalSkillData(int32 SkillId)
{
	if (!totalSkillData.Contains(SkillId))
	{
		USkillData* skillData = CreateSkillDataById(SkillId);
		if (skillData)
		{
			totalSkillData.Add(SkillId, skillData);
		}
	}
}

void USkillManager::RemoveTotalSkillData(int32 SkillId)
{
	if (totalSkillData.Contains(SkillId))
	{
		//不是玩家身上的技能才删除
		if (!PlayerSkillIdList.Contains(SkillId))
		{
			totalSkillData[SkillId] = nullptr;
			totalSkillData.Remove(SkillId);
			StopCdTime(SkillId);
		}
	}
}

void USkillManager::CheckJumpMaxCount(int32 SkillId)
{
	APlayerCharacter* PlayerCharacter = nullptr;
	if (SkillId == TWO_SECTION_JUMP_SKILLID || SkillId == THREE_SECTION_JUMP_SKILLID)
	{
		PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (PlayerCharacter)
		{
			PlayerCharacter->JumpComponent->SetJumpMaxCountBySkill();
		}
	}
}

TArray<int32> USkillManager::GetPlayerSkillIdList()
{
	return PlayerSkillIdList;
}

TArray<USkillData*> USkillManager::GetPlayerDataSkillList()
{
	TArray<USkillData*> PlayerSkillDataList;
	for (int32 playerSkillID:PlayerSkillIdList)
	{
		USkillData* skillData = GetSkillDataById(playerSkillID);
		if (skillData)
		{
			PlayerSkillDataList.Add(skillData);
		}
	}
	return PlayerSkillDataList;
}

void USkillManager::SetForbidJumpSkillIDs(TArray<int32> SkillIDs)
{
	ForbidJumpSkillIDs = SkillIDs;
}

TArray<int32> USkillManager::GetForbidJumpSkillIDs()
{
	return ForbidJumpSkillIDs;
}

TArray<USkillData*> USkillManager::GetPetDataSkillList()
{
	TArray<USkillData*> VPetSkillDataList;
	for (int32 skillID : VPetSkillIdList)
	{
		USkillData* skillData = GetSkillDataById(skillID);
		if (skillData)
		{
			VPetSkillDataList.Add(skillData);
		}
	}
	return VPetSkillDataList;
}

void USkillManager::IsLearnedSkill(int32 SkillId, bool& isLearned, int32& PlayerSkillID)
{
	isLearned = false;
	for (auto id : PlayerSkillIdList)
	{
		if (IsSameSkill(SkillId, id))
		{
			isLearned = true;
			PlayerSkillID = id;
			return;
		}
	}
}

void USkillManager::IsInTeachSkillCfg(int32 SkillId, bool& isIn)
{
	isIn = false;
	KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player();
	if (!Player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillManager::IsInTeachSkillCfg : Player!"));
		return;
	}
	int32 Profession = Player->GetDefinedProperty(TEXT("profession")).GetValue<int32>();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* SkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SKILLTEACHER_DATA);
	TArray<FSKILLTEACHER_DATA*> TeacherTableDatas;
	SkillConfig->GetAllRows(TeacherTableDatas);
	for (auto TeacherTableData : TeacherTableDatas)
	{
		if (TeacherTableData->npcId != TeacherID)
		{
			continue;
		}
		if (TeacherTableData->Class != Profession)
		{
			continue;
		}
		if (SkillId/1000 == TeacherTableData->skillID/1000)
		{
			isIn = true;
			return;
		}
	}
}

void USkillManager::InitSkillTreeData()
{
	KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player();
	if (!Player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillManager::InitSkillTreeData : Player!"));
		return;
	}
	int32 Profession = Player->GetDefinedProperty(TEXT("profession")).GetValue<int32>();
	SkillTreeUIDatas.Empty();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SKILLTREE_DATA);
	TArray<FSKILLTREE_INFO*> TableDatas;
	ConfigTable->GetAllRows(TableDatas);
	for (auto TableData : TableDatas)
	{
		if (!TableData->Class.Contains(Profession))
		{
			continue;
		}
		bool isLearned = false;
		int32 SkillID = FSTRING_TO_INT(TableData->skillID);
		this->IsLearnedSkill(SkillID, isLearned, SkillID);
		int32 Level = 0;
		UTexture2D* icon = GetIconBySkillID(SkillID);
		if(isLearned)
		{
			USkillData*SkillData = GetSkillDataById(SkillID);
			if (SkillData)
			{
				Level = SkillData->GetSkillLevel();
				icon = SkillData->GetIcon();
			}
		}
		FSKILLTREEUI_DATA SkillTreeUIData;
		SkillTreeUIData.skillID = INT_TO_FSTRING(SkillID);
		SkillTreeUIData.Type = TableData->type;
		SkillTreeUIData.RowIndex = TableData->rowIndex;
		SkillTreeUIData.ColIndex = TableData->colIndex;
		SkillTreeUIData.icon = icon;
		SkillTreeUIData.SkillLevel = Level;
		SkillTreeUIData.MaxSkillLevel = TableData->maxSkillLevel;
		SkillTreeUIData.QuickID = TableData->QuickID;
		SkillTreeUIDatas.Add(int32(SkillID / 1000), SkillTreeUIData);
	}
	IsInitSkillTree = true;
}

void USkillManager::SetSkillTreeData(int32 SkillId)
{
	if (!IsInitSkillTree)
	{
		return;
	}
	if (! SkillTreeUIDatas.Contains(int32(SkillId /1000))  )
	{
		return;
	}
	USkillData*SkillData = GetSkillDataById(SkillId);
	int32 Level = SkillData->GetSkillLevel();
	UTexture2D* icon = SkillData->GetIcon();
	FSKILLTREEUI_DATA SKillTreeTempData = SkillTreeUIDatas[int32(SkillId / 1000)];
	FSKILLTREEUI_DATA SkillTreeUIData;
	SkillTreeUIData.skillID = INT_TO_FSTRING(SkillId);
	SkillTreeUIData.Type = SKillTreeTempData.Type;
	SkillTreeUIData.RowIndex = SKillTreeTempData.RowIndex;
	SkillTreeUIData.ColIndex = SKillTreeTempData.ColIndex;
	SkillTreeUIData.icon = icon;
	SkillTreeUIData.SkillLevel = Level;
	SkillTreeUIData.MaxSkillLevel = SKillTreeTempData.MaxSkillLevel;
	SkillTreeUIData.QuickID = SKillTreeTempData.QuickID;
	SkillTreeUIDatas[int32(SkillId / 1000)] = SkillTreeUIData;

}
void USkillManager::RemoveSkillTreeDataByID(int32 SkillId)
{
	bool isLearned = false;
	int32 SkillID = SkillId;
	this->IsLearnedSkill(SkillID, isLearned, SkillID);
	if (isLearned)
		return;
	if (SkillTreeUIDatas.Contains(SkillId/1000))
	{
		SkillTreeUIDatas[SkillId / 1000].SkillLevel = 0;
		SkillTreeUIDatas[SkillId / 1000].skillID = INT_TO_FSTRING(SkillId / 1000 * 1000 + 1);
	}
}

void USkillManager::InitActionSkillData()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	for (auto RowName : GetRowNamesFromSkillCfg())
	{
		const FSKILL_TABLE_DATA* SkillTableData = GetSkillTableDataById(RowName.ToString());
		UObject* Result = LoadObject<UObject>(nullptr, *TSoftObjectPtr<UObject>(SkillTableData->SkillIcon).ToString());
		if (IsValid(Result))
		{
			FACTIONSKILL_DATA TempSkillData;
			FString SkillID = FNAME_TO_FSTRING(RowName);
			TempSkillData.skillID = SkillID;
			TempSkillData.actionName = SkillTableData->SkillName;
			
			TempSkillData.icon = nullptr;
			if (IsValid(SkillTableData->SkillIcon.Get()))
			{
				TempSkillData.icon = SkillTableData->SkillIcon.Get();
			}else {
				if (SkillTableData->SkillIcon.ToSoftObjectPath().IsValid())
				{
					UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(SkillTableData->SkillIcon.ToSoftObjectPath());
					TempSkillData.icon = SkillTableData->SkillIcon.Get();
				}
			}

			TempSkillData.description = SkillTableData->Description;
			ActionSkillDatas.Add(FSTRING_TO_INT(SkillID), TempSkillData);
		}
	}

}

TMap<int32, FSKILLLEARN_DATA> USkillManager::GetSkillLearnDatas()
{
	return SkillLearnDatas;
}

TArray<FSKILLLEARN_DATA> USkillManager::GetSortSkillLearnDatas(int32 type)//0为不可学习技能，1为可学习技能，2为全部技能
{
	TArray<FSKILLLEARN_DATA> LearnDatas;
	KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player();
	if (!Player)
	{
		return LearnDatas;
	}
	int16 level = Player->GetDefinedProperty(TEXT("level")).GetValue<int16>();
	
	int i = 0;
	for (auto it = SkillLearnDatas.CreateIterator(); it; ++it)
	{
		if( (type ==2 ) || ( ( level >= it.Value().ReqLevel ) == type))
		{
			LearnDatas.Add(it.Value()); 
		}
	}
	LearnDatas.Sort([](const FSKILLLEARN_DATA& A, const FSKILLLEARN_DATA& B){
		if  (A.ReqLevel != B.ReqLevel){
			return A.ReqLevel < B.ReqLevel; 
		}
		else
		{
			return A.ID < B.ID;
		}
	});
	return LearnDatas;
}
void USkillManager::InitSkillLearnDatasByTeacherID(int32 teacherID)
{
	if (this->TeacherID == teacherID)
	{
		return;
	}

	KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player();
	if (!Player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillManager::InitSkillLearnDatasByTeacherID : Player!"));
		return;
	}

	int32 Profession = Player->GetDefinedProperty(TEXT("profession")).GetValue<int32>();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* SkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SKILLTEACHER_DATA);
	TArray<FSKILLTEACHER_DATA*> TeacherTableDatas;
	SkillLearnDatas.Empty();
	LearnSkillIDs.Empty();
	SkillConfig->GetAllRows(TeacherTableDatas);
	for (auto TeacherTableData : TeacherTableDatas)
	{
		if (TeacherTableData->npcId != teacherID)
		{
			continue;
		}
		if (TeacherTableData->Class != Profession)
		{
			continue;
		}
		FSKILLLEARN_DATA TempLearnData = GetSkillLearnDataById(TeacherTableData->skillID);
		SkillLearnDatas.Add(FSTRING_TO_INT(TempLearnData.ID), TempLearnData);
		LearnSkillIDs.Add(FSTRING_TO_INT(TempLearnData.ID));
	}
	for (auto TempLearnSkillID : LearnSkillIDs)
	{
		for (auto skillID : PlayerSkillIdList)
		{
			if (IsSameSkill(TempLearnSkillID, skillID))
			{
				SkillLearnDatas.Remove(TempLearnSkillID);
			}
		}
	}
	this->TeacherID = teacherID;
}
void USkillManager::AddSkillLearnDataByID(int32 SkillId)
{
	bool isLearned = false;
	int32 SkillID = SkillId;
	this->IsLearnedSkill(SkillID, isLearned, SkillID);
	if (isLearned)
		return;
	bool isIn = false;
	this->IsInTeachSkillCfg(SkillId, isIn);
	if (!isIn)
		return;
	FSKILLLEARN_DATA TempLearnData = GetSkillLearnDataById(SkillId);
	if (SkillLearnDatas.Contains(SkillId) )
	{
		SkillLearnDatas[SkillId] = TempLearnData;
	}else {
		SkillLearnDatas.Add(SkillId, TempLearnData);
	}
}

void USkillManager::RemoveSkillLearnDataByID(int32 SkillId)
{
	if (SkillLearnDatas.Contains(SkillId))
	{
		SkillLearnDatas.Remove(SkillId);
	}
}

TMap<int32, FSKILLTREEUI_DATA> USkillManager::GetSkillTreeUIDatas()
{
	return SkillTreeUIDatas;
}


TArray<FSKILLTREEUI_DATA> USkillManager::GetSkillTreeUIDatasByType(int32 type)
{
	TArray<FSKILLTREEUI_DATA> tempSkillTreeDatas;
	for (auto SkillTreeUIData : SkillTreeUIDatas)
	{
		if (type == SkillTreeUIData.Value.Type)
		{
			tempSkillTreeDatas.Add(SkillTreeUIData.Value);
		}
	}
	return tempSkillTreeDatas;
}

FSKILLTREEUI_DATA USkillManager::GetSkillTreeUIDatasByID(int32 SkillID, bool& IsSuccess)
{
	for (auto SkillTreeUIData : SkillTreeUIDatas)
	{
		if (SkillID / 1000 == FSTRING_TO_INT(SkillTreeUIData.Value.skillID) / 1000)
		{
			IsSuccess = true;
			return SkillTreeUIData.Value;
		}
	}
	IsSuccess = false;
	return FSKILLTREEUI_DATA();
}

TMap<int32, FACTIONSKILL_DATA>  USkillManager::GetActionSKillDatas()
{
	return ActionSkillDatas;
}

void USkillManager::SetSkillLearnTableDatas()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		if (IsValid(CfgManager))
		{
			const UConfigTable* LearnSkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SKILLLEARN_DATA);

			if (IsValid(LearnSkillConfig))
			{
				TArray<FSKILLLEARN_DATA*> TableDatas;
				LearnSkillConfig->GetAllRows(TableDatas);
				for (auto TableData : TableDatas)
				{
					SkillLearnTableData.Add(FSTRING_TO_INT(TableData->ID), *TableData);
				}
			}
		}
	}
}


FSKILLLEARN_DATA USkillManager::GetSkillLearnDataById(int32 SkillId)
{
	if (SkillLearnTableData.Contains(SkillId))
	{
		return SkillLearnTableData[SkillId];
	}
	return FSKILLLEARN_DATA();
}

TArray<int32> USkillManager::GetMaxUpgrateSkillList(int32 SkillId, FString& SkillName, int32& MaxSkillLevel, int32& TotalRepPotential)
{
	TArray<int32> UpgrateSkillIds;
	int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
	FSKILLLEARN_DATA tempSkillLearnData = GetSkillLearnDataById(SkillId);//当前技能学习数据
	SkillName = tempSkillLearnData.UName;
	int32 tempNextLevelID = tempSkillLearnData.NextLevelID;//下一等级技能ID
	MaxSkillLevel = tempSkillLearnData.Level;
	if(tempNextLevelID == 0) return UpgrateSkillIds;//下一等级技能ID为0则当前技能已满级
	FSKILLLEARN_DATA tempNextSkillLearnData = GetSkillLearnDataById(tempNextLevelID);//下一等级技能学习数据
	TotalRepPotential += tempNextSkillLearnData.ReqPotential;
	while (PlayerLevel >= tempNextSkillLearnData.ReqLevel)
	{
		UpgrateSkillIds.Add(FSTRING_TO_INT(tempNextSkillLearnData.ID));
		MaxSkillLevel = tempNextSkillLearnData.Level;
		tempNextSkillLearnData = GetSkillLearnDataById(tempNextSkillLearnData.NextLevelID);
		TotalRepPotential += tempNextSkillLearnData.ReqPotential;
	}
	TotalRepPotential = TotalRepPotential - tempNextSkillLearnData.ReqPotential;//最后一次需要减一次，因为while里面已经加过一次判断不通过最后需要减去
	return UpgrateSkillIds;
}

bool USkillManager::CheckUpgradeCondition(int32 SkillID)
{
	FSKILLLEARN_DATA SkillLearnData = GetSkillLearnDataById(SkillID);
	//是否满级
	if (CheckUpgradeCondition_IsFullLevel(SkillLearnData.NextLevelID))
	{
		return false;
	}
	else
	{
		FSKILLLEARN_DATA NextSkillLearnData = GetSkillLearnDataById(SkillLearnData.NextLevelID);
		//等级
		if (!CheckUpgradeCondition_IsReachLevel(NextSkillLearnData.ReqLevel))
		{
			return false;
		}
		//技能书
		if (!CheckUpgradeCondition_IsReachMaterial(NextSkillLearnData.material_1, NextSkillLearnData.mNum_1))
		{
			return false;
		}
		if (!CheckUpgradeCondition_IsReachMaterial(NextSkillLearnData.material_2, NextSkillLearnData.mNum_2))
		{
			return false;
		}
		if (!CheckUpgradeCondition_IsReachMaterial(NextSkillLearnData.material_3, NextSkillLearnData.mNum_3))
		{
			return false;
		}
		//潜能
		if (!CheckUpgradeCondition_IsReachPotential(NextSkillLearnData.ReqPotential))
		{
			return false;
		}
		//金钱&绑定金钱
		if (!CheckUpgradeCondition_IsReachMoney(NextSkillLearnData.Money))
		{
			if(CheckUpgradeCondition_IsReachBindMoney(NextSkillLearnData.Money))
			{
				return true;
			}
			return false;
		}
		return true;
	}
}

bool USkillManager::CheckUpgradeCondition_IsFullLevel(int32 NextSkillID)
{
	if (NextSkillID == 0)
	{
		return true;
	}
	return false;
}

bool USkillManager::CheckUpgradeCondition_IsReachLevel(int32 ReqLevel)
{
	//等级
	int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
	if (PlayerLevel >= ReqLevel)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool USkillManager::CheckUpgradeCondition_IsReachMaterial(int32 ReqMaterialID, int32 ReqMaterialAmount)
{
	//技能书
	if (ReqMaterialID == 0)
	{
		//不需要技能书
		return true;
	}
	else
	{
		URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
		int32 Amount = RoleKitBagInterface->GetAmountByItemID(ReqMaterialID, FIND_BINDTYPE_ENUM::INGOREBIND);
		if (Amount >= ReqMaterialAmount)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
}

bool USkillManager::CheckUpgradeCondition_IsReachPotential(int32 ReqPotential)
{
	int32 PlayerPotential = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("potential"));
	if (PlayerPotential >= ReqPotential)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool USkillManager::CheckUpgradeCondition_IsReachBindMoney(int32 ReqMoney)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return false;

	URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (!IsValid(RoleInterface))
	{
		return false;
	}
	int64 PlayerBindMoney = RoleInterface->GetBindMoney();
	if (PlayerBindMoney >= ReqMoney)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool USkillManager::CheckUpgradeCondition_IsReachMoney(int32 ReqMoney)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return false;

	URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (!IsValid(RoleInterface))
	{
		return false;
	}
	int64 PlayerMoney = RoleInterface->GetMoney();
	int64 PlayerBindMoney = RoleInterface->GetBindMoney();
	if ((PlayerMoney + PlayerBindMoney) >= ReqMoney)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool USkillManager::CheckConditionSkillPosture(int32 SkillID)
{
	FSKILLLEARN_DATA LearnTableData = GetSkillLearnDataById(SkillID);
	const FSKILL_TABLE_DATA* SkillTableData = GetSkillTableDataById(INT_TO_FSTRING(SkillID));
	if (LearnTableData.SkillClass == 2 && SkillTableData)
	{
		USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;

		TArray<FSKILL_USE_CONDITION> CasterCondition = SkillTableData->CasterCondition;
		for (FSKILL_USE_CONDITION Condition : CasterCondition)
		{
			if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionSkillPosture)
			{
				TArray<FString> Postures =  UGolbalBPFunctionLibrary::SplitString(Condition.Param1, false, TEXT("|"));
				if (Postures.Contains(INT_TO_FSTRING(SkillInterface->skillPosture)))
				{
					return true;
				}
				else
				{
					return false;
				}
			}
		}
	}
	return true;
}

TArray<FSKILL_PASSIVE_TREE_DATA> USkillManager::GetLearnedPassiveSkillList()
{
	TArray<FSKILL_PASSIVE_TREE_DATA> SkillList;
	for (TPair<int32, FSKILL_PASSIVE_TREE_DATA> PassiveSkillData : SkillPassiveTreeDatas)
	{
		FSKILL_PASSIVE_TREE_DATA Data = PassiveSkillData.Value;
		bool isLearned = false;;
		int32 PlayerSkillID;
		UUECS3GameInstance::Instance->SkillManager->IsLearnedSkill(FSTRING_TO_INT(Data.skillID), isLearned, PlayerSkillID);
		if (isLearned)
		{
			SkillList.Add(Data);
		}
	}
	// 已激活>已学习的顺序排序
	SkillList.Sort([](const FSKILL_PASSIVE_TREE_DATA& A, const FSKILL_PASSIVE_TREE_DATA& B) {
		USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
		bool ActiveA = SkillInterface->CheckPassiveSkillActiveSate(FSTRING_TO_INT(A.skillID));
		bool ActiveB = SkillInterface->CheckPassiveSkillActiveSate(FSTRING_TO_INT(B.skillID));
		if (!ActiveA && ActiveB)
		{
			return false;
		} 
		else
		{
			//配置的顺序字段
			return A.Index < B.Index;
		}
	});
	return SkillList;
}

TArray<FSKILL_PASSIVE_TREE_DATA> USkillManager::GetAllPassiveSkillList(int32 PassiveSkillType)
{
	TArray<FSKILL_PASSIVE_TREE_DATA> SkillList;

	for (TPair<int32, FSKILL_PASSIVE_TREE_DATA> PassiveSkillData : SkillPassiveTreeDatas)
	{
		if (PassiveSkillData.Value.PassiveSkillType == PassiveSkillType)
		{
			SkillList.Add(PassiveSkillData.Value);
		}
	}

	// 已激活>已学习>未学习>技能ID的顺序排序
	SkillList.Sort([](const FSKILL_PASSIVE_TREE_DATA& A, const FSKILL_PASSIVE_TREE_DATA& B) {
		USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
		int32 SkillIDA = FSTRING_TO_INT(A.skillID);
		int32 SkillIDB = FSTRING_TO_INT(B.skillID);
		bool ActiveA = SkillInterface->CheckPassiveSkillActiveSate(SkillIDA);
		bool ActiveB = SkillInterface->CheckPassiveSkillActiveSate(SkillIDB);
		//激活
		if (!ActiveA && ActiveB)
		{
			return false;
		}
		else if (ActiveA && !ActiveB)
		{
			return true;
		}
		else if (ActiveA && ActiveB)
		{
			//配置的顺序字段
			return A.Index < B.Index;
		}
		else
		{
			//学习
			bool isLearnedA = false;;
			int32 PlayerSkillID;
			UUECS3GameInstance::Instance->SkillManager->IsLearnedSkill(SkillIDA, isLearnedA, PlayerSkillID);
			bool isLearnedB = false;;
			UUECS3GameInstance::Instance->SkillManager->IsLearnedSkill(SkillIDB, isLearnedB, PlayerSkillID);
			if (!isLearnedA && isLearnedB)
			{
				return false;
			}
			else if (isLearnedA && !isLearnedB)
			{
				return true;
			}
			else
			{
				//配置的顺序字段
				return A.Index < B.Index;
			}
		}
	});
	return SkillList;
}

TMap<int32, FSKILL_PASSIVE_TREE_DATA> USkillManager::GetPassiveSkillTreeDatas()
{
	return SkillPassiveTreeDatas;
}

FSKILL_PASSIVE_TREE_DATA USkillManager::GetPassiveSkillDataBySkillID(int32 SkillID)
{
	if (SkillPassiveTreeDatas.Contains(SkillID / 100))
	{
		return SkillPassiveTreeDatas[SkillID / 100];
	}
	return FSKILL_PASSIVE_TREE_DATA();
}

void USkillManager::InitSkillPassiveListData()
{
	KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player();
	if (!Player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillManager::InitSkillTreeData : Player!"));
		return;
	}
	int32 Profession = Player->GetDefinedProperty(TEXT("profession")).GetValue<int32>();
	SkillPassiveTreeDatas.Empty();
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PASSIVE_SKILL_TREE_DATA);
	TArray<FSKILL_PASSIVE_TREE_CONFIG*> TableDatas;
	ConfigTable->GetAllRows(TableDatas);
	for (auto TableData : TableDatas)
	{
		if (!TableData->Class.Contains(Profession))
		{
			continue;
		}
		bool isLearned = false;
		int32 SkillID = FSTRING_TO_INT(TableData->skillID);
		this->IsLearnedSkill(SkillID, isLearned, SkillID);
		int32 Level = 0;
		UTexture2D* icon = GetIconBySkillID(SkillID);
		if (isLearned)
		{
			USkillData*SkillData = GetSkillDataById(SkillID);
			if (SkillData)
			{
				Level = SkillData->GetSkillLevel();
				icon = SkillData->GetIcon();
			}
		}
		FSKILL_PASSIVE_TREE_DATA SkillTreeData;
		SkillTreeData.skillID = INT_TO_FSTRING(SkillID);
		SkillTreeData.icon = icon;
		SkillTreeData.SkillLevel = Level;
		SkillTreeData.MaxSkillLevel = TableData->MaxSkillLevel;
		SkillTreeData.PassiveSkillType = TableData->PassiveSkillType;
		SkillTreeData.Index = TableData->Index;
		SkillPassiveTreeDatas.Add(int32(SkillID / 100), SkillTreeData);
	}
}

void USkillManager::SetPassiveListData(int32 SkillID)
{
	if (!SkillPassiveTreeDatas.Contains(int32(SkillID / 100)))
	{
		return;
	}
	USkillData*SkillData = GetSkillDataById(SkillID);
	int32 Level = SkillData->GetSkillLevel();
	UTexture2D* icon = SkillData->GetIcon();
	FSKILL_PASSIVE_TREE_DATA SKillTreeTempData = SkillPassiveTreeDatas[int32(SkillID / 100)];
	FSKILL_PASSIVE_TREE_DATA TreeData;
	TreeData.skillID = INT_TO_FSTRING(SkillID);
	TreeData.icon = icon;
	TreeData.SkillLevel = Level;
	TreeData.MaxSkillLevel = SKillTreeTempData.MaxSkillLevel;
	TreeData.PassiveSkillType = SKillTreeTempData.PassiveSkillType;
	TreeData.Index = SKillTreeTempData.Index;
	SkillPassiveTreeDatas[int32(SkillID / 100)] = TreeData;
}

void USkillManager::RemovePassiveListDataByID(int32 SkillID)
{
	bool isLearned = false;
	int32 PlayerSkillID;
	this->IsLearnedSkill(SkillID, isLearned, PlayerSkillID);
	if (isLearned)
		return;
	if (SkillPassiveTreeDatas.Contains(SkillID / 100))
	{
		SkillPassiveTreeDatas[SkillID / 100].SkillLevel = 0;
		SkillPassiveTreeDatas[SkillID / 100].skillID = INT_TO_FSTRING(SkillID / 100 * 100 + 1);
	}
}

FSKILL_PASSIVE_LEARN_DATA USkillManager::GetPassiveSkillLearnDataById(int32 SkillId)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* LearnSkillConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PASSIVESKILL_LEARN_DATA);
		if (IsValid(LearnSkillConfig))
		{
			FName Row = FSTRING_TO_FNAME(INT_TO_FSTRING(SkillId));
			const FSKILL_PASSIVE_LEARN_DATA* TempLearnData = LearnSkillConfig->GetRow<FSKILL_PASSIVE_LEARN_DATA>(Row);
			if (TempLearnData)
			{
				FSKILL_PASSIVE_LEARN_DATA* Data = const_cast<FSKILL_PASSIVE_LEARN_DATA*>(TempLearnData);
				if (Data)
				{
					return *Data;
				}
			}
		}
	}
	return FSKILL_PASSIVE_LEARN_DATA();
}

bool USkillManager::CheckPassiveUpgradeCondition(int32 SkillID)
{
	FSKILL_PASSIVE_LEARN_DATA SkillLearnData = GetPassiveSkillLearnDataById(SkillID);
	//是否满级
	if (CheckUpgradeCondition_IsFullLevel(SkillLearnData.NextLevelID))
	{
		return false;
	}
	else
	{
		FSKILL_PASSIVE_LEARN_DATA NextSkillLearnData = GetPassiveSkillLearnDataById(SkillLearnData.NextLevelID);
		//等级
		if (!CheckUpgradeCondition_IsReachLevel(NextSkillLearnData.ReqLevel))
		{
			return false;
		}
		//材料
		if (!NextSkillLearnData.Material_1.IsEmpty())
		{
			TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(NextSkillLearnData.Material_1, false, "|");
			if (SplitArray.Num() >= 2)
			{
				if (!CheckUpgradeCondition_IsReachMaterial(FSTRING_TO_INT(SplitArray[0]), FSTRING_TO_INT(SplitArray[1])))
				{
					return false;
				}
			}
		}
		if (!NextSkillLearnData.Material_2.IsEmpty())
		{
			TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(NextSkillLearnData.Material_2, false, "|");
			if (SplitArray.Num() >= 2)
			{
				if (!CheckUpgradeCondition_IsReachMaterial(FSTRING_TO_INT(SplitArray[0]), FSTRING_TO_INT(SplitArray[1])))
				{
					return false;
				}
			}
		}
		if (!NextSkillLearnData.Material_3.IsEmpty())
		{
			TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(NextSkillLearnData.Material_3, false, "|");
			if (SplitArray.Num() >= 2)
			{
				if (!CheckUpgradeCondition_IsReachMaterial(FSTRING_TO_INT(SplitArray[0]), FSTRING_TO_INT(SplitArray[1])))
				{
					return false;
				}
			}
		}
		//潜能
		if (!CheckUpgradeCondition_IsReachPotential(NextSkillLearnData.ReqPotential))
		{
			return false;
		}
		//金钱
		if (!CheckUpgradeCondition_IsReachMoney(NextSkillLearnData.Money))
		{
			return false;
		}

		return true;
	}
}

FPASSIVESKILLBAR_DATA USkillManager::GetUnLockPassiveSkillSlotCost(int32 Index, bool& IsSuccess)
{
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PASSIVESKILLBAR_DATA);
	const FPASSIVESKILLBAR_DATA* data = table->GetRow<FPASSIVESKILLBAR_DATA>(INT_TO_FSTRING(Index));
	if (data)
	{
		IsSuccess = true;
		return *data;
	}
	IsSuccess = false;
	return FPASSIVESKILLBAR_DATA();
}

FSKILL_CHUANCHENG_TREE_CONFIG USkillManager::GetChuanChengSkillTreeCfgBySkillID(int32 SkillID)
{
	if (ChuanChengSkillTreeDatas.Contains(SkillID / 1000))
	{
		return ChuanChengSkillTreeDatas[SkillID / 1000];
	}
	return FSKILL_CHUANCHENG_TREE_CONFIG();
}

bool USkillManager::IsChuanChengSkill(int32 skillID)
{
	if (ChuanChengSkillTreeDatas.Contains(skillID / 1000))
	{
		return true;
	}
	return false;
}

void USkillManager::InitChuanChengSkillTreeTableDatas()
{
	KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player();
	if (!Player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillManager::InitChuanChengSkillTreeTableDatas : Player!"));
		return;
	}
	int32 Profession = Player->GetDefinedProperty(TEXT("profession")).GetValue<int32>();

	ChuanChengSkillTreeDatas.Empty();
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		return;
	}
	const UConfigTable* ChuanChengSkillTreeTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CHUANCHENG_SKILL_TREE_DATA);
	if (IsValid(ChuanChengSkillTreeTable))
	{
		for (auto RowName : ChuanChengSkillTreeTable->GetRowNames())
		{
			const FSKILL_CHUANCHENG_TREE_CONFIG* ConfigData = ChuanChengSkillTreeTable->GetRow<FSKILL_CHUANCHENG_TREE_CONFIG>(RowName);
			if (ConfigData)
			{
				if (!ConfigData->Class.Contains(Profession))
				{
					continue;
				}
				FSKILL_CHUANCHENG_TREE_CONFIG* Data = const_cast<FSKILL_CHUANCHENG_TREE_CONFIG*>(ConfigData);
				ChuanChengSkillTreeDatas.Add(ConfigData->skillID / 1000, *Data);
			}
		}
	}
}

FSKILL_CHUANCHENG_LEARN_DATA USkillManager::GetChuanChengSkillLearnDataById(int32 SkillId)
{
	if (ChuanChengSkillLearnTableData.Contains(SkillId))
	{
		return ChuanChengSkillLearnTableData[SkillId];
	}
	return FSKILL_CHUANCHENG_LEARN_DATA();
}

void USkillManager::InitChuanChengSkillLearnTableDatas()
{
	ChuanChengSkillLearnTableData.Empty();
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		return;
	}
	const UConfigTable* LearnSkillConfig = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CHUANCHENG_SKILL_LEARN_DATA);
	if (IsValid(LearnSkillConfig))
	{
		TArray<FSKILL_CHUANCHENG_LEARN_DATA*> TableDatas;
		LearnSkillConfig->GetAllRows(TableDatas);
		for (auto TableData : TableDatas)
		{
			ChuanChengSkillLearnTableData.Add(FSTRING_TO_INT(TableData->ID), *TableData);
		}
	}
}

FPET_SKILL_PASSIVE_LEARN_DATA USkillManager::GetPetSkillLearnDataById(int32 SkillId, bool& IsSuccess)
{
	if (PetSkillLearnTableData.Contains(SkillId))
	{
		IsSuccess = true;
		return PetSkillLearnTableData[SkillId];
	}
	IsSuccess = false;
	return FPET_SKILL_PASSIVE_LEARN_DATA();
}

void USkillManager::InitPetSkillLearnTableDatas()
{
	PetSkillLearnTableData.Empty();
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		return;
	}
	const UConfigTable* LearnSkillConfig = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET_SKILL_LEARN_DATA);
	if (IsValid(LearnSkillConfig))
	{
		TArray<FPET_SKILL_PASSIVE_LEARN_DATA*> TableDatas;
		LearnSkillConfig->GetAllRows(TableDatas);
		for (auto TableData : TableDatas)
		{
			PetSkillLearnTableData.Add(FSTRING_TO_INT(TableData->ID), *TableData);
		}
	}
}

void USkillManager::RefreshCDBySkillID(int32 SkillID)
{
	USkillData* SkillData = GetSkillDataById(SkillID);
	if (!IsValid(SkillData)) return;
	TMap<int32, FSKILL_UPDATE_COOL_DOWN> UpdateSkillCdList;
	TArray<FSKILL_COOL_DOWN> CasterCoolDownList = SkillData->GetCasterCoolDown();

	for (auto CasterCoolDown : CasterCoolDownList)
	{
		FSKILL_UPDATE_COOL_DOWN UpdateCoolDown = FSKILL_UPDATE_COOL_DOWN();
		UpdateCoolDown.CooldownId = CasterCoolDown.CooldownId;
		UpdateCoolDown.PersistTime = CasterCoolDown.CoolDownTime;
		UpdateCoolDown.RemainingTime = GetRemainingTime(CasterCoolDown.CooldownId);
		UpdateSkillCdList.Emplace(UpdateCoolDown.CooldownId, UpdateCoolDown);
	}
	UpdateSkillCoolDown(UpdateSkillCdList);
}

bool USkillManager::IsSameSkill(int32 SrcSkillID, int32 DestSkillID)
{
	USkillData* SrcSkillData = GetSkillDataById(SrcSkillID);
	USkillData* DestSkillData = GetSkillDataById(DestSkillID);
	if (IsValid(SrcSkillData) && IsValid(DestSkillData))
	{
		if (SrcSkillData->IsPassiveSkill() && DestSkillData->IsPassiveSkill())
		{
			return SrcSkillID / 100 == DestSkillID / 100;
		}
		else if (!SrcSkillData->IsPassiveSkill() && !DestSkillData->IsPassiveSkill())
		{
			return SrcSkillID / 1000 == DestSkillID / 1000;
		}
	}
	return false;
}

#if WITH_EDITOR
void USkillManager::UpdateSkillTable(UObject* Asset)
{
	if (Asset->GetName().Contains("SkillCfg"))
	{
		for (auto it = totalSkillData.CreateIterator(); it; ++it)
		{
			it.Value() = CreateSkillDataById(it.Key());
		}
	}
}
#endif

CONTROL_COMPILE_OPTIMIZE_END