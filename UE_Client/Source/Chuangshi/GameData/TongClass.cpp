#pragma once


#include "TongClass.h"
#include "Dom/JsonObject.h"
#include "JsonFieldData.h"
#include "Manager/MessageManager.h"
#include "Interface/Role/RoleTongInterface.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CfgManager.h"


UTongMember* UTongObject::GetMemberByDBID(const FString PlayerDBID)
{
	if (TongMembers.Contains(PlayerDBID))
	{
		return TongMembers[PlayerDBID];
	}
	return nullptr;
}

TArray<UTongMember*> UTongObject::GetMembersBySoldierData(const TArray<FString> removeMemberDIBDs,const int32& soldierAmount, const int32& militaryRank)
{
	TArray<UTongMember*> tempMembers;
	for (auto It = TongMembers.CreateConstIterator();It;++It)
	{
		if (!removeMemberDIBDs.Contains(It.Value()->DBID) && It.Value()->SoldierAmount >= soldierAmount && It.Value()->MilitaryRank >= militaryRank)
		{
			tempMembers.Add(It.Value());
		}
	}
	tempMembers.Sort([](const UTongMember& member1, const UTongMember& member2) { return member1.SoldierAmount > member2.SoldierAmount; });
	return tempMembers;
}

void UTongObject::initTongData(const FVariant& JsonData)
{
	FCLINE_TONG_DATAS tempData = FCLINE_TONG_DATAS( JsonData );
	TongDBID = tempData.TongDBID;
	TongLeaderDBID = tempData.TongLeader;
	TongName = tempData.TongName;
	TongLevel = tempData.level;
	TongMoney = FSTRING_TO_INT64(tempData.TongMoney);
	TongAffiche = tempData.TongAffiche;
	TongActivity = tempData.TongActivity;
	TongUpGradeActivity = tempData.UpGradeActivity;
	MinActivity = tempData.MinActivity;
	TongGrowth = tempData.TongGrow;
	TongMaxNum = tempData.TotalNum;
	TongLeague = tempData.League;
	TongCity = tempData.City;
	ShenShou = tempData.ShenShou;
	isSign = bool(tempData.Sign);
	SignTime = tempData.signTime;
	DonateMoney = tempData.donateMoney;
	isGetSalary = (tempData.Salary == 1);
	TongRecruitAffiche = tempData.TongRecruitAffiche;
	allocation = (TONG_PICKUP_TYPE)tempData.Allocation;
	BHLDAllocation = (TONG_PICKUP_TYPE)tempData.BHLDAllocation;
	for (auto Name : tempData.TitleNames)
	{
		TongTitleNames.Add(Name);
	}

	for (auto Grade : tempData.TongGrades)
	{
		TongGrades.Add(Grade);
	}
	for (int32 index = 0; index < tempData.TongBuild.Num(); index++)
	{
		if ((int32)TONG_BUILD_TYPE::TONG_BUILDING_TYPE_MAX > index)
		{
			TongBuildLevel.Add(TONG_BUILD_TYPE(index), tempData.TongBuild[index]);
		}
	}

	CurResearSkill.SkillID = tempData.TongSkill.ResearchSkill.skillID;
	CurResearSkill.Progress = tempData.TongSkill.ResearchSkill.progress;

	for (auto skill : tempData.TongSkill.PauseSkill)
	{
		FResearchSkillDATA pSkill;
		pSkill.SkillID = skill.skillID;
		pSkill.Progress = skill.progress;
		PauseSkill.Add(pSkill);
	}

	for (auto skill : tempData.TongSkill.SkillList)
	{
		HasResearSkillList.Add(skill);
	}

	for (auto level : tempData.TongSkill.SkillLevelList)
	{
		CurSkillLevelList.Add( level );
	}
}

void UTongObject::initMemberData(const FVariant& JsonData, FTraceCallback TraceCallback)
{
	UTongMember* member = NewObject<UTongMember>();
	CLENT_TONG_MEMBER_DATA tempData = CLENT_TONG_MEMBER_DATA( JsonData );
	member->name = tempData.name;
	member->DBID = tempData.DBID;
	member->id = tempData.id;
	member->level = tempData.level;
	member->profession = tempData.profession;
	member->title = tempData.title;
	member->exp = tempData.exp;
	member->weekContribution = tempData.weekContribution;
	member->contribution = tempData.contribution;
	member->totalContribution = tempData.totalContribution;
	member->localSpace = tempData.localSpace;
	member->offTime = tempData.offLineTime;
	member->isGag = tempData.isGag;
	member->SoldierAmount = tempData.soldierAmount;
	member->MilitaryRank = tempData.militaryRank;
	member->Blocklist = tempData.tongBlocklist;
	calculOffTimeStr(member);

	if (auto playerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity())
	{
		if (playerEntity->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>() == FSTRING_TO_INT64(member->DBID))
		{
			PlayerMember = member;
			TraceCallback.ExecuteIfBound(true);

		}
		else
		{
			TongMembers.Add(member->DBID, member);
		}
	}
		
	TongNum = TongMembers.Num() + 1;			// 加玩家自己
	SortMember();
}

void UTongObject::OnKickTongMember(const FString& kickerDBID, const FString& beKickerDBID)
{
	if (PlayerMember->DBID == kickerDBID)
	{
		if (TongMembers.Contains(beKickerDBID))
		{
			UTongMember* member = TongMembers[beKickerDBID];
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3115, member->name);
			}
			TongMembers.Remove(beKickerDBID);
			TongNum -= 1;
		}
	}
	else if (PlayerMember->DBID == beKickerDBID)
	{
		if (TongMembers.Contains(kickerDBID))
		{
			auto member = TongMembers[kickerDBID];
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3116, member->name);
			}
		}
	}
	else
	{
		auto kicker = TongMembers[kickerDBID];
		auto beKicker = TongMembers[beKickerDBID];
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3126, kicker->name + "|" + beKicker->name);
		}
		TongMembers.Remove(beKickerDBID);
		TongNum -= 1;
	}
}

void UTongObject::SortMember()
{
	TongMembers.ValueSort([](const UTongMember& A, const UTongMember& B)
	{
		if (A.title < B.title)return true;
		if (A.title > B.title)return false;
		if (A.level > B.level)return true;
		if (A.level < B.level)return false;
		if (A.exp > B.exp)return true;
		if (A.exp < B.exp)return false;
		if (A.id > B.id)return true;
		if (A.id < B.id)return false;
		return false;
	});
}

void UTongObject::calculOffTimeStr(UTongMember* member)
{
	FTimespan dstTime = FDateTime::Now() - UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime(member->offTime);
	int32 day = dstTime.GetDays();
	if (day)
	{
		int32 mount = day / 30;
		int32 week = day / 7;
		if (mount)
		{
			member->offLineTime = TEXT("1月前");
			return;
		}
		else if (week)
		{
			member->offLineTime = TEXT("1周前");
			return;
		}
		else
		{
			member->offLineTime = TEXT("1天前");
			return;
		}
	}
	int32 hour = dstTime.GetHours();
	if (hour == 0)
	{
		hour = 1;
	}
	member->offLineTime = INT_TO_FSTRING(hour) + TEXT("小时前");
}

bool UTongObject::isTongMoneyLow()
{
	auto CostTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_LEVEL_DATA);
	const FTongLevelData* CostData = CostTable->GetRow<FTongLevelData>(FSTRING_TO_FNAME(INT_TO_FSTRING(this->TongLevel)));
	if(CostData != nullptr) return this->TongMoney < CostData->lowMoney;
	return false;
}

int32 UTongObject::getDayExtraDeductActivity()
{
	auto CostTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_LEVEL_DATA);
	const FTongLevelData* CostData = CostTable->GetRow<FTongLevelData>(FSTRING_TO_FNAME(INT_TO_FSTRING(this->TongLevel)));
	if (CostData != nullptr)
	{
		if (this->TongMoney < CostData->lowMoney)
		{
			return (int32)(CostData->perActivity * CostData->perActivityForLowMoney / 100);
		}
	}
	return 0;
}

