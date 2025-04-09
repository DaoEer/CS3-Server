
#include "SkillData.h"
#include "Util/ConvertUtil.h"
#include "Manager/ResourceManager.h"
#include "Manager/CustomTimerManager.h"
#include "GameData/ConstDataBP.h"
#include "Util/CS3Debug.h"
#include "../Item/ItemFactory.h"
#include "../Item/CS3ItemData.h"

CONTROL_COMPILE_OPTIMIZE_START
USkillData* USkillData::CreateSkillData(const FSKILL_TABLE_DATA* TableData)
{
	USkillData* SkillData = NewObject<USkillData>();
	SkillData->SkillTableData = TableData;
	return SkillData;
}

USkillData * USkillData::CreatePassiveSkillData(const FPASSIVE_SKILL_TABLE_DATA * TableData)
{
	USkillData* SkillData = NewObject<USkillData>();
	SkillData->PassiveSkillTableData = TableData;
	return SkillData;
}

FSKILL_USE_RESULT USkillData::GetCasterResult()
{
	FSKILL_USE_RESULT CasterResult;
	if (SkillTableData!=nullptr)
	{
		CasterResult.CasterCastEffectId = SkillTableData->CasterCastEffectId;
		CasterResult.TargetCastEffectId = SkillTableData->TargetCastEffectId;
		CasterResult.CasterCastSoundId = SkillTableData->CasterCastSoundId;
		CasterResult.TargetCastSoundId = SkillTableData->TargetCastSoundId;
		CasterResult.SkillName = SkillTableData->SkillName;
		CasterResult.IsPromptSkillName = SkillTableData->IsPromptSkillName;
	}
	return CasterResult;
}

bool USkillData::IsInstantSkill()
{
	
	return SkillTableData->SkillType == ENUM_SKILL_CLASS_TYPE::InstantSkill;
}

bool USkillData::IsPassiveSkill()
{
	return PassiveSkillTableData != nullptr;
}

bool USkillData::IsCoolDowning()
{
	return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(CdTimerHandle) > 0;
}

void USkillData::StartCdTime(float TimeRemaining)
{
	if (IsCoolDowning())
	{
		StopCdTime();
	}

	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CdTimerHandle,this,&USkillData::StopCdTime, TimeRemaining, false);
}

void USkillData::StopCdTime()
{
	if (CdTimerHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CdTimerHandle);
	}
}

int32 USkillData::GetRemainingTime()
{
	return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(CdTimerHandle);
}

void USkillData::SetPersistTime(float PersistTime)
{
	CDPersistTime = PersistTime;
}

float USkillData::GetPersistTime()
{
	return CDPersistTime;
}

ENUM_CAST_TARGET_TYPE USkillData::GetTargetType()
{
	return SkillTableData->TargetType;
}

ENUM_SKILL_ASSIST_TARGET_TYPE USkillData::GetAssistTargetType()
{
	return SkillTableData->AssistTargetType;
}

TArray<FSKILL_REQUIRE> USkillData::GetCasterRequireList()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->CasterRequireDefine;
	}
	else
	{
		return SkillTableData->CasterRequireDefine;
	}
}

TArray<FSKILL_USE_CONDITION> USkillData::GetCasterCondition()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->CasterCondition;
	}
	else
	{
		return SkillTableData->CasterCondition;
	}
}

TArray<TArray<FSKILL_USE_CONDITION>> USkillData::GetTargetCondition()
{
	TArray<TArray<FSKILL_USE_CONDITION>> Conditions;
	if (IsPassiveSkill())
	{
		for (FPASSIVE_SKILL_HIT HitData : PassiveSkillTableData->HitList)
		{
			Conditions.Add(HitData.ReceiverCondition);
		}
	}
	else
	{
		for (FSKILL_HIT HitData : SkillTableData->HitList)
		{
			Conditions.Add(HitData.ReceiverCondition);
		}
	}
	return Conditions;
}

const FSKILL_ASSIST_EFFECT& USkillData::GetAssistEffect()
{
	return SkillTableData->AssistEffect;
}

float USkillData::GetRangeMax()
{
	//如果配置的CastRangeMax为0则表示默认最大施法距离，并非施法距离为0的意思
	if ( FMath::IsNearlyZero(SkillTableData->CastRangeMax))
		return SKILL_CAST_RANGE_MAX;
	return SkillTableData->CastRangeMax;
}

bool USkillData::GetTurnToTarget()
{
	return SkillTableData->IsTurnToTarget;
}

FName USkillData::GetID()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->RowName;
	}
	else
	{
		return SkillTableData->RowName;
	}
}

TArray<FSKILL_COOL_DOWN> USkillData::GetCasterCoolDown()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->CasterCoolDown;
	}
	else
	{
		return SkillTableData->CasterCoolDown;
	}
}

UTexture2D* USkillData::GetIcon()
{
	if (IsPassiveSkill())
	{
		TSoftObjectPtr<UTexture2D> TextureIcon = PassiveSkillTableData->SkillIcon;;

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
	else
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
}

FString USkillData::GetDescription()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->Description;
	}
	else
	{
		return SkillTableData->Description;
	}
}

FString USkillData::GetCasterRequireDescribe()
{
	FString CasterRequireDescribe;
	if (IsPassiveSkill())
	{
		CasterRequireDescribe =  PassiveSkillTableData->CasterRequireDescribe;
	}
	else
	{
		CasterRequireDescribe = SkillTableData->CasterRequireDescribe;
	}

	//优先描述配置（格式：消耗类型|消耗数量|消耗道具ID）
	if (!CasterRequireDescribe.Equals(TEXT("")))
	{
		TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(CasterRequireDescribe, false, "|");
		if (SplitArray.Num() >= 2)
		{
			int32 RequireType = FSTRING_TO_INT(SplitArray[0]);
			FString RequireID;
			switch (RequireType)
			{
			case 1:
			{
				RequireID = TEXT("RequireMp");
				break;
			}
			case 2:
			{
				RequireID = TEXT("RequireHp");
				break;
			}
			case 3:
			{
				RequireID = TEXT("RequireGangQi");
				break;
			}
			case 4:
			{
				if (SplitArray.Num() >= 3)
				{
					const FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(FSTRING_TO_INT(SplitArray[2]));
					return SplitArray[1] + TEXT(" ") + ItemData.ItemName;
				}
				return UGolbalBPFunctionLibrary::GetChinese(TEXT("Wu"));
			}
			default:
				return UGolbalBPFunctionLibrary::GetChinese(TEXT("Wu"));
			}
			return SplitArray[1] + TEXT(" ") + UGolbalBPFunctionLibrary::GetChinese(RequireID);
		}
		return CasterRequireDescribe;
	}
	else
	{
		//如果没有配置描述，则获取消耗配置 第一个消耗
		TArray<FSKILL_REQUIRE> RequireList = GetCasterRequireList();
		if (RequireList.Num() > 0)
		{
			FSKILL_REQUIRE Require = RequireList[0];
			FString RequireID;
			switch (Require.Type)
			{
			case ENUM_SKILL_REQUIRE_TYPE::RequireMp:
			{
				RequireID = TEXT("RequireMp");
				break;
			}
			case ENUM_SKILL_REQUIRE_TYPE::RequireHp:
			{
				RequireID = TEXT("RequireHp");
				break;
			}
			case ENUM_SKILL_REQUIRE_TYPE::RequireGangQi:
			{
				RequireID = TEXT("RequireGangQi");
				break;
			}
			case ENUM_SKILL_REQUIRE_TYPE::RequireCostItem:
			{
				const FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(FSTRING_TO_INT(Require.Param1));
				return Require.Param2 + TEXT(" ") + ItemData.ItemName;
			}
			default:
				return UGolbalBPFunctionLibrary::GetChinese(TEXT("Wu"));
			}
			return Require.Param1 + TEXT(" ") + UGolbalBPFunctionLibrary::GetChinese(RequireID);
		}
	}
	return UGolbalBPFunctionLibrary::GetChinese(TEXT("Wu"));
}

FString USkillData::GetCasterCoolDownDescribe()
{
	FString CasterCoolDownDescribe;
	if (IsPassiveSkill())
	{
		CasterCoolDownDescribe = PassiveSkillTableData->CasterCoolDownDescribe;
	}
	else
	{
		CasterCoolDownDescribe = SkillTableData->CasterCoolDownDescribe;
	}
	
	//优先描述配置
	if (!CasterCoolDownDescribe.Equals(TEXT("")))
	{
		return CasterCoolDownDescribe + TEXT(" ") + UGolbalBPFunctionLibrary::GetChinese(TEXT("Second"));
	}
	else
	{
		//如果没有配置描述，则获取冷却配置 第一个冷却
		TArray<FSKILL_COOL_DOWN> CoolDownList = GetCasterCoolDown();
		if (CoolDownList.Num() > 0)
		{
			FSKILL_COOL_DOWN CoolDown = CoolDownList[0];
			return INT_TO_FSTRING(FMath::CeilToInt(CoolDown.CoolDownTime)) + TEXT(" ") + UGolbalBPFunctionLibrary::GetChinese(TEXT("Second"));
		}
	}
	return UGolbalBPFunctionLibrary::GetChinese(TEXT("Wu"));
}

ENUM_SKILL_CLASS_TYPE USkillData::GetSkillType()
{
	return SkillTableData->SkillType;
}

FString USkillData::GetSkillName()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->SkillName;
	}
	else
	{
		return SkillTableData->SkillName;
	}
}

int32 USkillData::GetSkillLevel()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->SkillLevel;
	}
	else
	{
		return SkillTableData->SkillLevel;
	}
}

int32 USkillData::GetSkillQuality()
{
	if (IsPassiveSkill())
	{
		return PassiveSkillTableData->Quality;
	}
	else
	{
		return SkillTableData->Quality;
	}
}

ACTION_FLAG USkillData::GetCasterActForbid()
{
	return SkillTableData->CasterActForbid;
}

ACTION_FLAG USkillData::GetTargetActForbid()
{
	return SkillTableData->TargetActForbid;
}

bool USkillData::IsSkillDataValid()
{
	if (nullptr == SkillTableData && nullptr == PassiveSkillTableData)
	{
		return false;
	}

	if (nullptr != SkillTableData && !SkillTableData->CasterCoolDown.IsValidIndex(0))
	{
		return false;
	}

	if (nullptr != PassiveSkillTableData && !PassiveSkillTableData->CasterCoolDown.IsValidIndex(0))
	{
		return false;
	}

	return true;
}

void USkillData::BeginDestroy()
{
	Super::BeginDestroy();
}

bool USkillData::CanInitiaiveInterrupt()
{
	bool _CanInterrupt = false;
	for (auto _TempEvent : SkillTableData->CasterInterruptSkillEvent)
	{
		if (_TempEvent.EventType == ENUM_SKILL_EVENT::InitiaiveStopSkillEvent)
		{
			_CanInterrupt = true;
		}
	}
	return _CanInterrupt;
	
}
CONTROL_COMPILE_OPTIMIZE_END
