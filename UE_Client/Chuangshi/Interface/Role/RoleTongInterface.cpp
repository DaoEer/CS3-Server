// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleTongInterface.h"
#include "GameData/ConstData.h"
#include "Actor/Player/PlayerCharacter.h"
#include "JsonFieldData.h"
#include "Interface/StatusMessageInterface.h"
#include "UnrealMathUtility.h"
#include "Manager/MessageManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/SkillManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include"Chuangshi.h"
#include "GameDevelop/CS3GameInstance.h"
#include "JsonFieldData.h"
#include "Dom/JsonValue.h"
#include "Entity/Alias.h"
#include "GameData/TongData.h"
#include "Manager/EventManager.h"
#include "CS3Base/UIManager.h"

CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTongInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateTongDatas, &URoleTongInterface::UpdateTongDatas, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnReceiveAllTong, &URoleTongInterface::CLIENT_OnReceiveAllTong, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpdateTongMember, &URoleTongInterface::CLIENT_UpdateTongMember, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequireTongEvent, &URoleTongInterface::CLIENT_OnRequireTongEvent, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequireTongStoreEvent, &URoleTongInterface::CLIENT_OnRequireTongStoreEvent, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnSureSignUpBHZBMember, &URoleTongInterface::OnSureSignUpBHZBMember, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SetbhzbSignUpMembersIsActive, &URoleTongInterface::SetbhzbSignUpMembersIsActive,int32,uint8,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRemoveApplyJoinTongMember, &URoleTongInterface::OnRemoveApplyJoinTongMember, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnPlunderMemberChange, &URoleTongInterface::OnPlunderMemberChange, const TArray<FVariant>&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenPlunderTongListWnd, &URoleTongInterface::OpenPlunderTongListWnd, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onSetTongAllocation, &URoleTongInterface::onSetTongAllocation, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onSetTongBHLDAllocation, &URoleTongInterface::onSetTongBHLDAllocation, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ClearAllTongSignMemberData, &URoleTongInterface::ClearAllTongSignMemberData)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnTongBlocklistChange, &URoleTongInterface::OnTongBlocklistChange, const TArray<FVariant>&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTongInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
	

URoleTongInterface::URoleTongInterface()
{
	const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	if (GameInstance &&
		GameInstance->LocalDataSaveManager &&
		GameInstance->LocalDataSaveManager->LocalUserSettingData
		)
	{
		SetNoticeLine(GameInstance->LocalDataSaveManager->LocalUserSettingData->GetIsShowOnlineRemind());
	}
}

bool URoleTongInterface::RequireAllTong()
{
	int32 level = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("level"));
	if (level < TONG_JOIN_MIX_LEVEL)
	{
		return false;
	}
	/*
	if (TongDatas.Num() != 0)
	{
		if ((FDateTime::Now() - RequitJoinTime).GetMinutes() <= REQUEST_TONG_JOIN_TIME)
		{
			return true;
		}
	}*/
	TArray<FString> args;
	UGolbalBPFunctionLibrary::BaseCall(EntityID, ("RequireTongInfo"), args);
	return false;
}

void URoleTongInterface::CLIENT_OnReceiveAllTong(const FVariant& Variant)
{
	///	RequitJoinTime = FDateTime::Now();
	TongDatas.Empty();
	JOIN_TONG_DATAS tempData = JOIN_TONG_DATAS(Variant);
	for (auto data : tempData.tongDatas)
	{
		FTongJoinData joinData;
		joinData.TongDBID = data.TongDBID;
		joinData.TongName = data.Name;
		joinData.TongLevel = data.Level;
		joinData.TongActivity = data.Activity;
		joinData.TongNum = data.TongNum;
		joinData.TotalNum = data.TotalNum;
		joinData.LeaderName = data.LeaderName;
		joinData.Money = FSTRING_TO_INT64(data.Money);
		joinData.RecruitAffiche = data.Recruit;
		joinData.TongLeague = data.League;
		joinData.OccupyCity = data.City;
		joinData.Shenshou = data.ShenShou;
		joinData.PersonTitle = data.PersonTitle;
		TongDatas.Add(joinData.TongDBID, joinData);
	}
	TongDatas.ValueSort([](const FTongJoinData& A, const FTongJoinData& B)->bool
	{
		if (A.TongLevel > B.TongLevel) return true;
		if (A.TongLevel < B.TongLevel) return false;
		if (A.TongNum > B.TongNum) return true;
		if (A.TongNum < B.TongNum) return false;
		if (A.TongDBID < B.TongDBID) return true;
		if (A.TongDBID > B.TongDBID) return false;
		return false;
	});
	OnReceiveAllTong();
}
void URoleTongInterface::OnReceiveAllTong_Implementation()
{

}

TArray<FTongJoinData> URoleTongInterface::SearchJoinListByName(const FString& tongName)
{
	TArray<FTongJoinData> searchList;
	for (auto It = TongDatas.CreateConstIterator(); It; ++It)
	{
		if (tongName.IsEmpty() || It.Value().TongName.Contains(tongName))
		{
			searchList.Add(It.Value());
		}
	}
	return searchList;
}

TArray<FTongJoinData> URoleTongInterface::SearchJoinListByIsFull(const bool isFull)
{
	TArray<FTongJoinData> searchList;
	for (auto It = TongDatas.CreateConstIterator(); It; ++It)
	{
		if (isFull)
		{
			searchList.Add(It.Value());
		} 
		else
		{
			if (It.Value().TongNum < It.Value().TotalNum)
			{
				searchList.Add(It.Value());
			}
		}
	}
	return searchList;
}

bool URoleTongInterface::hasTong()
{
	if (IsValid(Tong))
	{
		return true;
	}
	return false;
}

bool URoleTongInterface::IsInSameTong(const int32& entityID_)
{
	if (IsValid(Tong))
	{
		if (Tong->PlayerMember->id == entityID_)
		{
			return true;
		}
		for (auto IT = Tong->TongMembers.CreateConstIterator(); IT ; ++IT)
		{
			if (IT.Value()->id == entityID_)
			{
				return true;
			}
		}
	}
	return false;
}

void URoleTongInterface::CreateTong(const FString& tongName)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::CreateTong : GetEntity()!"));
		return;
	}
	if (IsValid(Tong))return;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("level")) < TONG_CREATE_MIX_LEVEL)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3140, "");
			return;
		}
		if (UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("jingjieLevel")) < TONG_CREATE_MIX_JINJIELEVEL)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3135, "");
			return;
		}
		KBEngine::FVariantArray args;
		args.Add(tongName);
		Tong_CellCall(TEXT("tongCreate"), args);
	}
}

void URoleTongInterface::OnJoinTong_Implementation()
{

}

void URoleTongInterface::TongReqJoin(const FString& tongDBID)
{
	if (TongApplyList.Contains(tongDBID)) return;

	if (IsValid(UUECS3GameInstance::Instance))
	{
		int32 level = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("level"));
		if (level < TONG_JOIN_MIX_LEVEL)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3101, TEXT(""));
			return;
		}
		if (TongApplyList.Num() >= APPLY_JOIN_MAX_LIST)
		{

			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3100, TEXT(""));
			return;
		}
	}
	
	TongApplyList.Add(tongDBID);
	KBEngine::FVariantArray args;
	args.Add(tongDBID);
	Tong_BaseCall(TEXT("tongReqJoin"), args);
}

void URoleTongInterface::OnOtherReqJoinTong_Implementation(const FString& playerDBID, const FString& playerName, const int32& level, const int32& profession)
{
	for (auto& data : ApplicantDataList)
	{
		if (data.DBID.Equals(playerDBID))return;
	}
	FPlayerJoinData joinData;
	joinData.DBID = playerDBID;
	joinData.name = playerName;
	joinData.level = level;
	joinData.profession = profession;
	ApplicantDataList.Add(joinData);
	NoReadApplicantList.Add(playerDBID);
}

void URoleTongInterface::CancelJoinTong(const FString& tongDBID)
{
	if (TongApplyList.Contains(tongDBID))
	{
		TongApplyList.Remove(tongDBID);
	}
	KBEngine::FVariantArray args;
	args.Add(tongDBID);
	Tong_BaseCall(TEXT("tongCancelJoin"), args);
}

void URoleTongInterface::RemoveNoReadApplicantList(const FString& playerDBID)
{
	if (NoReadApplicantList.Contains(playerDBID))
	{
		NoReadApplicantList.Remove(playerDBID);
	}
}

void URoleTongInterface::ClearNoReadApplicantList()
{
	NoReadApplicantList.Empty();
}

bool URoleTongInterface::HasNoReadApplicant()
{
	return NoReadApplicantList.Num() > 0;
}

void URoleTongInterface::OnOtherCancelJoinTong_Implementation(const FString& playerDBID)
{
	RemoveNoReadApplicantList(playerDBID);
	for (auto it = ApplicantDataList.CreateConstIterator(); it; ++it)
	{
		if (it->DBID.Equals(playerDBID))
		{
			ApplicantDataList.RemoveAt(it.GetIndex());
			break;
		}
	}
}

void URoleTongInterface::RequestPlayerJoin()
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_REQUEST))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(3108, "");
		return;
	}
	KBEngine::FVariantArray args;
	Tong_BaseCall(TEXT("requestJoinList"), args);
}

void URoleTongInterface::OnRequestJoinList_Implementation(const TArray<FString>& DBIDList, const TArray<FString>& nameList, const TArray<int32>& levelList, const TArray<int32>& proList)
{
	ApplicantDataList.Empty();
	auto num = DBIDList.Num();
	if (num == nameList.Num() && num == levelList.Num() && num == proList.Num())
	{
		for (auto It = DBIDList.CreateConstIterator(); It ; ++It)
		{
			int32 index = It.GetIndex();
			if (!DBIDList[index].IsEmpty())
			{
				FPlayerJoinData joinData;
				joinData.DBID = DBIDList[index];
				joinData.name = nameList[index];
				joinData.level = levelList[index];
				joinData.profession = proList[index];
				ApplicantDataList.Add(joinData);
			}	
		}

	}
}

void URoleTongInterface::OnRefuseJoinTong_Implementation(const FString& TongDBID, const FString& tongName)
{
	if (TongApplyList.Contains(TongDBID))
	{
		TongApplyList.Remove(TongDBID);
	}
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(3104, tongName);
}

void URoleTongInterface::OnApplyJoinTongFailed_Implementation(const FString& TongDBID)
{
	if (TongApplyList.Contains(TongDBID))
	{
		TongApplyList.Remove(TongDBID);
	}
}

void URoleTongInterface::OnApplyJoinTongSuccess_Implementation(const FString& TongDBID)
{

}

void URoleTongInterface::ReplyJoinTong(const FString& playerDBID, bool canJoin)
{
	for (auto it = ApplicantDataList.CreateConstIterator(); it; ++it)
	{
		if (it->DBID.Equals(playerDBID))
		{
			ApplicantDataList.RemoveAt(it.GetIndex());
			break;
		}
	}

	KBEngine::FVariantArray args;
	args.Add(playerDBID);
	args.Add(int32(canJoin));
	Tong_BaseCall(TEXT("replyJoinTong"), args);
}

void URoleTongInterface::ReplyAllJoinTong(bool canJoin)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::ReplyAllJoinTong : pKBEApp!"));
		return;
	}
	if (ApplicantDataList.Num() == 0)return;
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::ReplyAllJoinTong : player!"));
		return;
	}

	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("URoleStallInterface::ReplyAllJoinTong no this PlayerRole"));
		return;
	}
	ApplicantDataList.Empty();
	KBEngine::FVariantArray args;
	args.Add(int32(canJoin));
	player->BaseCall(TEXT("replyAllJoinTong"), args);
}

void URoleTongInterface::InviteJoinTong(const int32& targetID_)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		// 如果客户端可以获取目标ID，就检查
		if (UGolbalBPFunctionLibrary::FindEntity(targetID_) != nullptr)
		{
			if (UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("camp")) != UGolbalBPFunctionLibrary::GetIntPropertyValue(targetID_, TEXT("camp")))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3111, "");
				return;
			}
			if (UGolbalBPFunctionLibrary::GetIntPropertyValue(targetID_, TEXT("level")) < TONG_JOIN_MIX_LEVEL)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3101, "");
				return;
			}
		}
		
		if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_INVITE))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3108, "");
			return;
		}
	}
	KBEngine::FVariantArray args;
	args.Add(targetID_);
	Tong_CellCall("tongInviteJoin", args);
}

void URoleTongInterface::RemoteTongInviteJoin(const FString& targetName)
{
	KBEngine::FVariantArray args;
	args.Add(targetName);
	Tong_BaseCall("remoteTongInviteJoin", args);
}

void URoleTongInterface::GotoTongSpace()
{
	if (IsValid(Tong))
	{
		KBEngine::FVariantArray args;
		Tong_CellCall("gotoTongSpace", args);
	}
}

TArray<UTongMember*> URoleTongInterface::SearchTongMemberByName(const FString& name)
{
	TArray<UTongMember*> tempList;
	if (IsValid(Tong))
	{
		if (name.IsEmpty())
		{
			tempList.Add(Tong->PlayerMember);
			for (auto It = Tong->TongMembers.CreateConstIterator(); It; ++It)
			{
				tempList.Add(It.Value());
			}
		}
		else
		{
			if (Tong->PlayerMember->name.Contains(name))
			{
				tempList.Add(Tong->PlayerMember);
			}
			for (auto It = Tong->TongMembers.CreateConstIterator(); It; ++It)
			{
				if (It.Value()->name == name)
				{
					tempList.Add(It.Value());
				}
			}
		}
	}
	return tempList;
}

TArray<UTongMember*> URoleTongInterface::SearchTongMemberByLine(const bool isOnline)
{
	TArray<UTongMember*> tempList;
	if (IsValid(Tong))
	{
		tempList.Add(Tong->PlayerMember);
		for (auto It = Tong->TongMembers.CreateConstIterator(); It; ++It)
		{
			if (It.Value()->id != 0)
			{
				tempList.Add(It.Value());
			}
			else if (!isOnline)
			{
				tempList.Add(It.Value());
			}
		}
	}
	return tempList;
}

void URoleTongInterface::OnMemberOnline_Implementation(const FString& dbid, const int32& id)
{
	if (IsValid(Tong) && Tong->TongMembers.Contains(dbid))
	{
		auto member = Tong->TongMembers[dbid];
		member->id = id;
		
		if (isNotice && IsValid(UUECS3GameInstance::Instance))
		{
			FString tempStr = Tong->TongTitleNames[member->title] + "|" + member->name;
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3169, tempStr);
		}
	}
}

void URoleTongInterface::OnMemberOffline_Implementation(const FString& dbid, const int32& level, const FString& birthSpace, const FString& offTime)
{
	if (IsValid(Tong) && Tong->TongMembers.Contains(dbid))
	{
		UTongMember* member = Tong->TongMembers[dbid];
		member->id = 0;
		member->level = level;
		member->localSpace = birthSpace;
		member->offTime = offTime;
		Tong->calculOffTimeStr(member);
		if (isNotice && IsValid(UUECS3GameInstance::Instance))
		{
			FString tempStr = Tong->TongTitleNames[member->title] + "|" + member->name;
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3170, tempStr);
		}
		Tong->SortMember();
	}
}

void URoleTongInterface::UpdateTongDatas(const FVariant& JsonStr)
{
	TongApplyList.Empty();		///玩家加入帮会了需要把入帮申请列表清空
	if (!IsValid(Tong))
	{
		Tong = NewObject<UTongObject>();
	}
	Tong->initTongData(JsonStr);
	//InitTongGrade();
	InitTongBuildLevel();
	InitTongSkill();
	onUpdateTongDatas();
}
void URoleTongInterface::onUpdateTongDatas_Implementation()
{

}

void URoleTongInterface::OnInitTongApplyList_Implementation(const TArray<FString>& joinTongList)
{

	TongApplyList =  joinTongList;
}

void URoleTongInterface::CLIENT_UpdateTongMember(const FVariant& Variant)
{
	if (!IsValid(Tong))
	{
		Tong = NewObject<UTongObject>();
	}

	Tong->initMemberData(Variant, FTraceCallback::CreateLambda([this](bool isplayer)
	{
		this->InitTongGrade(true);
	}));
	UpdateTongMember();
}
void URoleTongInterface::UpdateTongMember_Implementation()
{

}
void URoleTongInterface::KickTongMember(const FString& targetDBID)
{
	KBEngine::FVariantArray args;
	args.Add(targetDBID);
	Tong_BaseCall("tongKickMember", args);
}

void URoleTongInterface::OnKickTongMember_Implementation(const FString& kickerDBID, const FString& beKickerDBID)
{
	if (IsValid(Tong))
	{
		Tong->OnKickTongMember(kickerDBID, beKickerDBID);
		if (Tong->PlayerMember && Tong->PlayerMember->DBID == beKickerDBID)	///玩家被踢出帮会服务器也会调OnLeaveTong，这里不处理清除数据也可以
		{
			ClearTongInfo();
		}
	}
	else
	{
		CS3_Warning(TEXT("Kick Member err!Tong is nullptu!"));
	}
}

void URoleTongInterface::QuitTong()
{
	if (IsValid(Tong) && UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->MessageManager)
	{
		//判断玩家是不是帮主
		if (Tong->PlayerMember->title == int32(TONG_TITLE_TYPE::TONG_TITLE_1))
		{
			//判断帮会是不是只有一个成员
			if (Tong->TongMembers.Num() > 1)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3117, "");
				return;
			}
			else
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3127, "", FBtnClick::CreateLambda([this](RT_BTN_TYPE RtType)
				{
					KBEngine::FVariantArray args;
					if (RtType == RT_BTN_TYPE::RT_OK) Tong_BaseCall("tongQuit", args);
				}));
			}

		}
		else
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3149, "", FBtnClick::CreateLambda([this](RT_BTN_TYPE RtType)
			{
				KBEngine::FVariantArray args;
				if (RtType == RT_BTN_TYPE::RT_OK) Tong_BaseCall("tongQuit", args);
			}));
		}
	}
}

void URoleTongInterface::OnQuitTong_Implementation(const FString& playerDBID)
{
	if (IsValid(Tong))
	{
		if (Tong->PlayerMember->DBID == playerDBID)		///玩家自己退出帮会也会走OnLeaveTong清除数据，这里不处理清除数据也可以
		{
			ClearTongInfo();
		}
		else if(Tong->TongMembers.Find(playerDBID))
		{
			if (UUECS3GameInstance::Instance)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3133, Tong->TongMembers[playerDBID]->name); ///“xxx退出了帮会”
			}
			Tong->TongMembers.Remove(playerDBID);
			Tong->TongNum -= 1;
		}
		else
		{
			CS3_Warning(TEXT("On quick tong err!Player is not in the Tong!"));
		}
	}
	else
	{
		CS3_Warning(TEXT("On quick tong err!Tong is nullptu!"));
	}
	
}

void URoleTongInterface::DismissTong()
{
	if (IsValid(Tong))
	{
		if (Tong->PlayerMember->title == int32(TONG_TITLE_TYPE::TONG_TITLE_1))
			{
				KBEngine::FVariantArray args;
				Tong_BaseCall("tongDismiss", args);
			}
	}
	else
	{
		CS3_Warning(TEXT("Dismiss tong err!Tong is nullptu!"));
	}
}

void URoleTongInterface::OnLeaveTong_Implementation()
{
	ClearTongInfo();
}

void URoleTongInterface::SetTitleName(int32 titleType, const FString& name)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::SetTitleName : Tong!"));
		return;
	}
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_RENAME))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	if (Tong->TongTitleNames.Contains(name))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3120, "");
		}
		OnSetTitleNameFailed();
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(titleType);
	args.Add(name);
	Tong_BaseCall("setTitleName", args);
}

void URoleTongInterface::OnSetTitleName_Implementation(const int32& titleType, const FString& name)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::OnSetTitleName_Implementation : Tong!"));
		return;
	}
	if (Tong->TongTitleNames.Num()>=titleType)
	{
		Tong->TongTitleNames.RemoveAt(titleType);
		Tong->TongTitleNames.Insert(name, titleType);
		
	}
}

void URoleTongInterface::OnSetTitleNameFailed_Implementation()
{

}

void URoleTongInterface::SetTongTitle(const FString& playerDBID, const int32& titleType)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_APPOINT))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(playerDBID);
	args.Add(titleType);
	Tong_BaseCall("setTitle", args);
}

void URoleTongInterface::OnSetTongTitle_Implementation(const FString& playerDBID, const int32 titleType)
{
	if (IsValid(Tong))
	{
		if (Tong->PlayerMember->DBID.Equals( playerDBID))
		{
			int32 hasOldRequestJoin(Tong->TongGrades[Tong->PlayerMember->title] & (1 << (int32)TONG_GRADE_TYPE::TONG_GRADE_REQUEST));
			Tong->PlayerMember->title = titleType;
			InitTongGrade(true);
			int32 hasNewRequestJoin(Tong->TongGrades[titleType] & (1 << (int32)TONG_GRADE_TYPE::TONG_GRADE_REQUEST));
			if (ApplicantDataList.Num() != 0)
			{
				if (hasOldRequestJoin != 0 && hasNewRequestJoin == 0)
				{
					for (int32 index = 0; index < ApplicantDataList.Num();index++)
					{
						if (ApplicantDataList.IsValidIndex(index))
						{
							OnOtherCancelJoinTong(ApplicantDataList[index].DBID);
						}
					}
				}
			}
		}
		else
		{
			if (Tong->TongMembers.Contains(playerDBID))
			{
				Tong->TongMembers[playerDBID]->title = titleType;
				Tong->SortMember();
			}
		}
	}
}

int32 URoleTongInterface::GetMemberNumByTitle(int32 titleType)
{
	int32 TempNum = 0;
	if (IsValid(Tong))
	{
		for (auto It = Tong->TongMembers.CreateConstIterator(); It; ++It)
		{
			if (It.Value()->title == titleType)
			{
				TempNum += 1;
			}
		}
		if (Tong->PlayerMember->title == titleType)
		{
			TempNum += 1;
		}
	}
	
	return TempNum;
}

void URoleTongInterface::deMiseLeader(const FString& playerDBID)
{
	if (IsValid(Tong))
	{
		// 只有帮主可以转让帮主
		if (Tong->TongLeaderDBID.Equals( Tong->PlayerMember->DBID))
		{
			//被转让的玩家的帮众等级必须达到3星帮众(TONG_TITLE= 5 # 3星帮众，等级越高Title越小)
			if (Tong->TongMembers.Contains(playerDBID) && Tong->TongMembers[playerDBID]->title > 5)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3165, "");
			}
			else
			{
				KBEngine::FVariantArray args;
				args.Add(playerDBID);
				Tong_BaseCall("deMiseLeader", args);
			}
		}
	}
}

void URoleTongInterface::OnLeaderChange_Implementation(const FString& playerDBID)
{
	if (IsValid(Tong))
	{
		Tong->TongLeaderDBID = playerDBID;
	}
}

void URoleTongInterface::OnTongMoneyChange_Implementation(const int32& tongMoney)
{
	if (IsValid(Tong))
	{
		Tong->TongMoney = tongMoney;
	}
}

void URoleTongInterface::OnActivityChange_Implementation(const int32& Activity)
{
	if (IsValid(Tong))
	{
		Tong->TongActivity = Activity;
	}
}

void URoleTongInterface::OnGrowChange_Implementation(const int32& Grow)
{
	if (IsValid(Tong))
	{
		Tong->TongGrowth = Grow;
	}
}

void URoleTongInterface::OnContributionChange_Implementation(const FString& dbid, const int32& contribute)
{
	if (IsValid(Tong))
	{
		if (Tong->PlayerMember->DBID.Equals( dbid))
		{
			if (contribute > Tong->PlayerMember->contribution)
			{
				int32 addCon = contribute - Tong->PlayerMember->contribution;
				Tong->PlayerMember->weekContribution += addCon;
				Tong->PlayerMember->totalContribution += addCon;
			}
			Tong->PlayerMember->contribution = contribute;
		}
		for (auto It = Tong->TongMembers.CreateConstIterator(); It; ++It)
		{
			if (It.Key() == dbid)
			{
				if (contribute > It.Value()->contribution)
				{
					int32 addCon = contribute - It.Value()->contribution;
					It.Value()->weekContribution += addCon;
					It.Value()->totalContribution += addCon;
				}
				It.Value()->contribution = contribute;
			}
		}
		
	}
}

void URoleTongInterface::onTongMemberExpChange_Implementation(const FString& dbid, const int32& exp)
{
	if (IsValid(Tong))
	{
		if (Tong->PlayerMember->DBID == dbid)
		{
			Tong->PlayerMember->exp = exp;
		}
		if (Tong->TongMembers.Contains(dbid))
		{
			Tong->TongMembers[dbid]->exp = exp;
		}
	}
}

void URoleTongInterface::SetGrade(const TONG_TITLE_TYPE titleType, const TArray<TONG_GRADE_TYPE>& gradeList)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_REQUEST))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		OnSetGradeFailed();
		return;
	}
	int32 grades(0);
	for (auto& grade : gradeList)
	{
		grades |= 1 << (uint8)grade;
	}
	KBEngine::FVariantArray args;
	args.Add(int(titleType));
	args.Add(grades);
	Tong_BaseCall("setGrade", args);
}

void URoleTongInterface::OnSetGrade_Implementation(const int32& titleType, const int32& grades)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::OnSetGrade_Implementation : Tong!"));
		return;
	}
	int32 oldGrade = Tong->TongGrades[titleType];
	Tong->TongGrades.Insert(grades, titleType);
	Tong->TongGrades.RemoveAt(titleType + 1);
	if (ApplicantDataList.Num() != 0)
	{
		int32 grade = 1 << (int32)TONG_GRADE_TYPE::TONG_GRADE_REQUEST;
		if (((oldGrade & grade) != 0) && ((grades & grade) == 0))
		{
			for (int32 index = 0; index < ApplicantDataList.Num(); index++)
			{
				if (ApplicantDataList.IsValidIndex(index))
				{
					OnOtherCancelJoinTong(ApplicantDataList[index].DBID);
				}
			}
		}
	}
}

void URoleTongInterface::OnSetGradeFailed_Implementation()
{

}

void URoleTongInterface::OnTongBlocklistChange(const TArray<FVariant>& BlockList)
{
	if (IsValid(Tong))
	{
		Tong->PlayerMember->Blocklist.Empty();
		for (auto DBID : BlockList)
		{
			Tong->PlayerMember->Blocklist.Add(DBID.GetValue<FString>());
		}
	}
}

void URoleTongInterface::DonateMoney(const int64& money)
{
	KBEngine::FVariantArray args;
	args.Add(INT64_TO_FSTRING(money));
	Tong_CellCall("donateMoney", args);
}

void URoleTongInterface::OnDonateMoney_Implementation(const int64& money)
{
	if (IsValid(Tong))
	{
		Tong->DonateMoney += money;
	}
}

FString URoleTongInterface::GetValidInputDonateMoney(const FString& InputMoney)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::GetValidInputDonateMoney : GetEntity()!"));
		return TEXT("1");
	}

	int64 playerMoneyValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 tempInputMoney = FSTRING_TO_INT64(InputMoney);
	if (playerMoneyValue > tempInputMoney) {
		return INT64_TO_FSTRING(FMath::Clamp<int64>(tempInputMoney, 0, 10000));
	}
	return INT64_TO_FSTRING(FMath::Clamp<int64>(playerMoneyValue, 0, 10000));
}

void URoleTongInterface::SetAffiche(const FString& affiche)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_NOTICE))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	FString TempAffiche = UGolbalBPFunctionLibrary::ReplaceLineBreak(affiche);
	KBEngine::FVariantArray args;
	args.Add(TempAffiche);
	Tong_BaseCall("setAffiche", args);
}

void URoleTongInterface::OnSetAffiche_Implementation(const FString& affiche)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::OnSetAffiche_Implementation : Tong!"));
		return;
	}
	Tong->TongAffiche = affiche;
}

void URoleTongInterface::SetRecruitAffiche(const FString& affiche)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_NOTICE))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	FString TempAffiche = UGolbalBPFunctionLibrary::ReplaceLineBreak(affiche);
	KBEngine::FVariantArray args;
	args.Add(TempAffiche);
	Tong_BaseCall("setRecruitAffiche", args);
}

void URoleTongInterface::OnSetRecruitAffiche_Implementation(const FString& affiche)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::OnSetRecruitAffiche_Implementation : Tong!"));
		return;
	}
	Tong->TongRecruitAffiche = affiche;
}

void URoleTongInterface::SetGag(const FString& dbid, const int32& isGag)
{
	if (IsValid(Tong) && Tong->TongMembers.Contains(dbid))
	{
		if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_SHUTUP))
		{
			if (UUECS3GameInstance::Instance)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
			}
		}
		else if(Tong->PlayerMember->title >= Tong->TongMembers[dbid]->title)
		{
			if (UUECS3GameInstance::Instance)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(3227, "");
			}
		} 
		else
		{
			KBEngine::FVariantArray args;
			args.Add(dbid);
			args.Add(isGag);
			Tong_BaseCall("setMemberGag", args);
		}
	}
}

void URoleTongInterface::OnSetGag_Implementation(const FString& dbid, const int32& isGag)
{
	if (IsValid(Tong) && Tong->TongMembers.Contains(dbid))
	{
		Tong->TongMembers[dbid]->isGag = isGag;
	}
}

void URoleTongInterface::TongSign()
{
	if (IsValid(Tong))
	{
		if (!Tong->isSign)
		{
			KBEngine::FVariantArray args;
			Tong_BaseCall("tongSign", args);
		}
	}
}

void URoleTongInterface::OnTongSign_Implementation()
{
	if (IsValid(Tong))
	{
		Tong->isSign = true;
		Tong->SignTime += 1;
	}
}

void URoleTongInterface::onDawnArrive_Implementation()
{
	if (IsValid(Tong))
	{
		Tong->isSign = false;
		Tong->isGetSalary = false;
	}
}

void URoleTongInterface::GetSalary()
{
	if (IsValid(Tong) && !Tong->isGetSalary)
	{
		Tong->isGetSalary = true;
		KBEngine::FVariantArray args;
		Tong_CellCall("getTongSalary", args);
	}
}

void URoleTongInterface::OnGetSalaryFail_Implementation()
{
	if (IsValid(Tong))
	{
		Tong->isGetSalary = false;
	}
}

bool URoleTongInterface::HasGradeTong(TONG_GRADE_TYPE GradeType)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::HasGradeTong : Tong!"));
		return false;
	}
	if (IsValid(Tong->PlayerMember) && Tong->TongGrades.Num() >= Tong->PlayerMember->title)
	{
		int32 grade = 1 << int32(GradeType);
		if (Tong->TongGrades[Tong->PlayerMember->title] & grade)
		{
			return true;
		}
		return false;
	}
	CS3_Warning(TEXT("IndexError: list index out of range!"));
	return false;
}

bool URoleTongInterface::HasGradeByTitle(TONG_TITLE_TYPE titleID, TONG_GRADE_TYPE GradeType)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::HasGradeByTitle : Tong!"));
		return false;
	}
	int32 grade = 1 << int32(GradeType);
	if (Tong->TongGrades[(int32)titleID] & grade)
	{
		return true;
	}
	return false;
}

bool URoleTongInterface::IsSysGrade(const TONG_TITLE_TYPE& titleID, const TONG_GRADE_TYPE& GradeType)
{
	if (SysGrades.Contains(titleID))
	{
		int32 sysGrade = SysGrades[titleID];
		int32 grade = 1 << (uint8)GradeType;
		if (sysGrade & grade)
		{
			return true;
		}
		return false;
	}
	CS3_Warning(TEXT("KeyError: %d"),(uint8)titleID);
	return false;
}

bool URoleTongInterface::IsDefGrade(const TONG_TITLE_TYPE& titleID, const TONG_GRADE_TYPE& GradeType)
{
	if (DefaultGrades.Contains(titleID))
	{
		int32 sysGrade = DefaultGrades[titleID];
		int32 grade = 1 << (uint8)GradeType;
		if (sysGrade & grade)
		{
			return true;
		}
		return false;
	}
	CS3_Warning(TEXT("KeyError: %d"), (uint8)titleID);
	return false;
}

bool URoleTongInterface::IsFobGrade(const TONG_TITLE_TYPE& titleID, const TONG_GRADE_TYPE& GradeType)
{
	if (ForbidGrades.Contains(titleID))
	{
		int32 sysGrade = ForbidGrades[titleID];
		int32 grade = 1 << (uint8)GradeType;
		if (sysGrade & grade)
		{
			return true;
		}
		return false;
	}
	CS3_Warning(TEXT("KeyError: %d"), (uint8)titleID);
	return false;
}

int32 URoleTongInterface::GetMoneyByBuildLevel(uint8 BuildLevel, TONG_BUILD_TYPE BuildType)
{
	if (TongBuildUpGrade.Contains(BuildLevel) && TongBuildUpGrade[BuildLevel].Contains(BuildType))
	{
		return TongBuildUpGrade[BuildLevel][BuildType].upGradeMoney;
	}
	return 0;
}

int32 URoleTongInterface::GetGrowByBuildLevel(uint8 BuildLevel, TONG_BUILD_TYPE BuildType)
{
	if (TongBuildUpGrade.Contains(BuildLevel) && TongBuildUpGrade[BuildLevel].Contains(BuildType))
	{
		return TongBuildUpGrade[BuildLevel][BuildType].upGradeGrow;
	}
	return 0;
}

FString URoleTongInterface::GetEffectByBuildLevel(uint8 BuildLevel, TONG_BUILD_TYPE BuildType)
{
	if (TongBuildUpGrade.Contains(BuildLevel) && TongBuildUpGrade[BuildLevel].Contains(BuildType))
	{
		return TongBuildUpGrade[BuildLevel][BuildType].effect;
	}
	return FString("");
}

void URoleTongInterface::UpgrowBuild(TONG_BUILD_TYPE BuildType)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_BUILDING))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)BuildType);
	Tong_BaseCall("upGrowTongBuild", args);
}

void URoleTongInterface::OnUpgrowBuild_Implementation(int32 BuildType, int32 level)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::OnUpgrowBuild_Implementation : Tong!"));
		return;
	}
	if (Tong->TongBuildLevel.Contains((TONG_BUILD_TYPE)BuildType))
	{
		Tong->TongBuildLevel[(TONG_BUILD_TYPE)BuildType] = level;
		FString msg(TONG_BUILD_NAMES[(TONG_BUILD_TYPE)BuildType] + "|" + INT_TO_FSTRING(level));
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5553, msg);

	}
}

void URoleTongInterface::OnConferenceHallLevelChange_Implementation(int32 LimitNum)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::OnUpgrowBuild_Implementation : Tong!"));
		return;
	}
	Tong->TongMaxNum = LimitNum;
}

void URoleTongInterface::UpgrowTong()
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_UPGRADE))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	KBEngine::FVariantArray args;
	Tong_BaseCall("upGrowTong", args);
}


void URoleTongInterface::OnUpgrowTong_Implementation(const int32& level, const int32& upGradeActivity)
{
	if (IsValid(Tong))
	{
		Tong->TongLevel = level;
		Tong->TongUpGradeActivity = upGradeActivity;
	}
}

void URoleTongInterface::ResearchTongSkill(const int32& skillID)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_DEVELOP))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(skillID);
	Tong_BaseCall("researchTongSkill", args);
}

void URoleTongInterface::OnResearchTongSkill_Implementation(const int32& skillID)
{
	if (IsValid(Tong))
	{
		int32 progress(0);
		for (auto& RSkill : Tong->PauseSkill)
		{
			if (RSkill.SkillID == skillID)
			{
				progress = RSkill.Progress;
				//CST-13790
				Tong->PauseSkill.RemoveSingleSwap(RSkill);
				break;
			}
		}
		Tong->CurResearSkill.SkillID = skillID;
		Tong->CurResearSkill.Progress = progress;
	}
}

void URoleTongInterface::PauseTongSkill(const int32& skillID)
{
	if (!HasGradeTong(TONG_GRADE_TYPE::TONG_GRADE_DEVELOP))
	{
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(3114, "");
		}
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(skillID);
	Tong_BaseCall("pauseTongSkill", args);
}

void URoleTongInterface::OnPauseTongSkill_Implementation(const int32& skillID)
{
	if (IsValid(Tong))
	{
		FResearchSkillDATA data;
		data.SkillID = Tong->CurResearSkill.SkillID;
		data.Progress = Tong->CurResearSkill.Progress;
		Tong->PauseSkill.Add(data);
		Tong->CurResearSkill.SkillID = 0;
		Tong->CurResearSkill.Progress = 0;

	}
}


void URoleTongInterface::OnTongSkillProgressChange_Implementation(const int32& Progress)
{
	if (IsValid(Tong))
	{
		Tong->CurResearSkill.Progress = Progress;
	}

}

void URoleTongInterface::OnFinishResearchSkill_Implementation(const int32& skillID)
{
	if (IsValid(Tong))
	{
		if ( Tong->CurResearSkill.SkillID == skillID )
		{
			Tong->CurResearSkill.SkillID = 0;
			Tong->CurResearSkill.Progress = 0;
			Tong->HasResearSkillList.Add(skillID);
			Tong->CurSkillLevelList.RemoveAll([skillID](int32 & SkillID) { return SkillID / 1000 == skillID / 1000; });
			Tong->CurSkillLevelList.Add(skillID);
		}
		else
		{
			Tong->HasResearSkillList.Add(skillID);
			Tong->CurSkillLevelList.RemoveAll([skillID](int32 & SkillID) { return SkillID / 1000 == skillID / 1000; });
			Tong->CurSkillLevelList.Add(skillID);
			CS3_Warning(TEXT("Finish research skill err!skill ID is diff"));
		}
	}
}

void URoleTongInterface::OnFinishLearnSkill_Implementation(const int32& skillID) 
{
}

void URoleTongInterface::StudyTongSkill(const int32& skillID)
{
	if (UUECS3GameInstance::Instance)
	{
		TArray<int32> playerSkillList = UUECS3GameInstance::Instance->SkillManager->GetPlayerSkillIdList();
		for (auto& skillList : TongSkillList)
		{
			if (skillList.Contains(skillID))
			{
				for (auto id : skillList)
				{
					if (playerSkillList.Contains(id))
					{
						int32 nextSkill = TongSkillDatas[id]->NextSkill;
						if (nextSkill)
						{
							KBEngine::FVariantArray args;
							args.Add(nextSkill);
							Tong_CellCall("startStudyTongSkill", args);
						}
						return;
					}
				}
				int32 skill = skillList[0];
				KBEngine::FVariantArray args;
				args.Add(skill);
				Tong_CellCall("startStudyTongSkill", args);
			}
		}
	}
	
}

TArray<FTongSkillDATA> URoleTongInterface::GetAllResearchSkills(TArray<int32>& state, TArray<int32>& playerLevel)
{
	TArray<FTongSkillDATA> datas;
	if (UUECS3GameInstance::Instance && IsValid(Tong))
	{
		
		for (auto& skillList : TongSkillList)
		{
			bool isAdd = false;
			for (auto id : skillList)
			{
				if (Tong->CurResearSkill.SkillID == id)
				{
					isAdd = true;
					datas.Add(*TongSkillDatas[id]);
					state.Add(0);
					playerLevel.Add(GetPlayerTongResSkillLevel(skillList));
					break;
				}

				for (auto PRS : Tong->PauseSkill)
				{
					if (PRS.SkillID == id)
					{
						isAdd = true;
						datas.Add(*TongSkillDatas[id]);
						state.Add(1);
						playerLevel.Add(GetPlayerTongResSkillLevel(skillList));
						break;
					}
				}

			}
			if (!isAdd)
			{
				for (int32 skillID : Tong->CurSkillLevelList)
				{
					if (skillList.Contains(skillID))
					{
						isAdd = true;
						datas.Add(*TongSkillDatas[skillID]);
						state.Add(3);
						playerLevel.Add(GetPlayerTongResSkillLevel(skillList));
						break;
					}
				}
				if (!isAdd)
				{
					datas.Add(*TongSkillDatas[skillList[0]]);
					state.Add(2);
					playerLevel.Add(0);
				}
			}
		}
	}

	return datas;
}

FTongSkillDATA URoleTongInterface::GetResearchSkillData(const int32& curSkillID)
{
	if (TongSkillDatas.Contains(curSkillID))
	{
		return *TongSkillDatas[curSkillID];
	}
	FTongSkillDATA emptyData;
	return emptyData;
}

void URoleTongInterface::GetResearchSkillLevelRelevant(const int32& SkillID, int32& CurLevel, int32& MaxLevel)
{
	if (UUECS3GameInstance::Instance)
	{
		TArray<int32> playerSkillList = UUECS3GameInstance::Instance->SkillManager->GetPlayerSkillIdList();
		for (auto& skillList : TongSkillList)
		{
			if (skillList.Contains(SkillID))
			{
				MaxLevel = TongSkillDatas[skillList[skillList.Num()-1]]->Level;
				for (auto id : skillList)
				{
					if (playerSkillList.Contains(id))
					{
						CurLevel = TongSkillDatas[id]->Level;
						return;
					}
				}
			}
		}
	}
}

bool URoleTongInterface::RequireTongEvent()
{
	/*
	if (TongEventList.Num() != 0)
	{
		if ((FDateTime::Now() - RequitEventTime).GetMinutes() < REQUEST_TONG_EVENT_TIME)
		{
			return true;
		}
		
	}*/
	KBEngine::FVariantArray args;
	Tong_BaseCall("requestTongEvent", args);
	return false;
}

void URoleTongInterface::CLIENT_OnRequireTongEvent(const FVariant& TongEvent)
{
	TongEventList.Empty();
	TONG_EVENT_DATAS tempData = TONG_EVENT_DATAS(TongEvent);
	for (auto& data : tempData.eventDatas)
	{
		FTongEventDATA eventData;
		eventData.Time = UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime( data.time );
		eventData.EventType = data.type;
		TArray<FString> Params = data.param;
		UCfgManager* cfgMgr = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_EVENT_DATA);
		if (IsValid(table))
		{
			TArray<FTongEventMapping*> EventData;
			table->GetAllRows(EventData);
			for (FTongEventMapping* TE : EventData)
			{
				if (int32(TE->EventType)==eventData.EventType)
				{
					eventData.ClassEventType = TE->ClassEventType;
					for (FString es : TE->EventStr)
					{
						for (auto It = Params.CreateConstIterator(); It; ++It )
						{
							int32 index = It.GetIndex();
							if (eventData.EventType == 13 && index == 0)
							{
								FString temp;
								if (FSTRING_TO_INT(*It) == 0)temp = TEXT("议事大厅");
								else if (FSTRING_TO_INT(*It) == 1)temp = TEXT("神兽殿");
								else if (FSTRING_TO_INT(*It) == 2)temp = TEXT("仓库");
								else if (FSTRING_TO_INT(*It) == 3)temp = TEXT("铁匠铺");
								else if (FSTRING_TO_INT(*It) == 4)temp = TEXT("商店");
								else if (FSTRING_TO_INT(*It) == 5)temp = TEXT("研究院");
								es = es.Replace(TEXT("[0]"), *temp);
							}
							else
							{
								if (Params[index].IsNumeric())
								{
									es = es.Replace(*FString("[" + INT_TO_FSTRING(index) + "]"), *INT_TO_FSTRING(FSTRING_TO_INT(*It)));
								}
								else
								{
									es = es.Replace(*FString("[" + INT_TO_FSTRING(index) + "]"), *Params[index]);
								}
								
							}
							
						}
						eventData.EventStr.Add(es);
					}
				}
			}
		}
		TongEventList.Add(eventData);
	}
	OnRequireTongEvent();
}
void URoleTongInterface::OnRequireTongEvent_Implementation( )
{

}
TArray<FTongEventDATA> URoleTongInterface::GetTongEventByClassType(const TArray<TONG_EVENT_SET_TYPE> classType, const int32 time, const bool isShowOnlyMe)
{
	TArray<FTongEventDATA> Datas,temp;
	for (auto It : classType)
	{
		for (auto eventData : TongEventList)
		{
			if (eventData.ClassEventType == It)
			{
				temp.Add(eventData);
			}
		}
	}
	
	if (isShowOnlyMe)
	{
		FString name = UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityID, TEXT("playerName"));
		for (auto& event_ : temp)
		{
			for (auto eStr : event_.EventStr)
			{
				if (eStr.Contains(name))
				{
					Datas.Add(event_);
					break;
				}
			}
		}
	}
	else
	{
		Datas = temp;
	}
	temp = Datas;
	Datas.Empty();

	for (auto& event_ : temp)
	{
		FDateTime DNow = FDateTime::Now();
		FDateTime DayT = event_.Time;
		if (time == 0 && DayT.GetDayOfYear() == DNow.GetDayOfYear())			// 只显示今日
		{
			Datas.Add(event_);
		}
		else if (time == 1 && DNow.GetDayOfYear() - DayT.GetDayOfYear() <= 7)	// 显示一周
		{
			Datas.Add(event_);
		}
		else if (time == 2 && DNow.GetDayOfYear() - DayT.GetDayOfYear() <= 30)	// 显示一月
		{
			Datas.Add(event_);
		}
		else if(time == 3)														// 显示全部
		{
			Datas.Add(event_);
		}
	}
	Datas.Sort([](const FTongEventDATA& A, const FTongEventDATA& B) { return A.Time < B.Time; });
	return Datas;
}

void URoleTongInterface::RequireTongStoreEvent()
{
	KBEngine::FVariantArray args;
	Tong_BaseCall("requestTongStoreEvent", args);
}


void URoleTongInterface::CLIENT_OnRequireTongStoreEvent(const FVariant& TongEvent)
{
	TongStoreEventList.Empty();
	TONG_EVENT_DATAS tempData = TONG_EVENT_DATAS(TongEvent);
	for (auto data : tempData.eventDatas)
	{
		FTongStoreEventData eventData;
		eventData.Time = UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime( data.time );
		eventData.EventType = data.type;
		TArray<FString> Params = data.param;

		UCfgManager* cfgMgr = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_STORE_EVENT_DATA);
		if (IsValid(table))
		{
			TArray<FTongStoreEventMapping*> EventData;
			table->GetAllRows(EventData);
			for (FTongStoreEventMapping* TSE : EventData)
			{
				if (int32(TSE->EventType) == eventData.EventType)
				{
					for (FString es : TSE->EventStr)
					{
						for (auto It = Params.CreateConstIterator(); It; ++It)
						{
							int32 index = It.GetIndex();
							if (Params[index].IsNumeric())
							{
								es = es.Replace(*FString("[" + INT_TO_FSTRING(index) + "]"), *INT_TO_FSTRING(FSTRING_TO_INT(*It)));
							}
							else
							{
								es = es.Replace(*FString("[" + INT_TO_FSTRING(index) + "]"), *Params[index]);
							}
						}
						eventData.EventStr.Add(es);
					}
				}
			}
		}
		TongStoreEventList.Add(eventData);
	}
	OnRequireTongStoreEvent();
}

void URoleTongInterface::OnRequireTongStoreEvent_Implementation( )
{

}
TArray<FTongStoreEventData> URoleTongInterface::GetTongStoreEventByType(const TONG_STORE_EVENT_TYPE type,bool getAll)
{
	TArray<FTongStoreEventData> datas;
	if (getAll)
	{
		datas = TongStoreEventList;
		datas.Sort([](const FTongStoreEventData& A, const FTongStoreEventData& B) { return A.Time > B.Time; });
		return datas;
	}
	else
	{
		for (auto e : TongStoreEventList)
		{
			if (e.EventType == int32(type))
			{
				datas.Add(e);
			}
		}
		datas.Sort([](const FTongStoreEventData& A, const FTongStoreEventData& B) { return A.Time > B.Time; });
		return datas;
	}
}

void URoleTongInterface::OpenTongStore_Implementation(const int32& NPCID, const int32& tongStoreCapacity)
{
	OpenGridCapacity = tongStoreCapacity;
}

void URoleTongInterface::RequestSaveTongItem(const int32& srcOrder, const int32& bagID)
{
	KBEngine::FVariantArray args;
	args.Add(srcOrder);
	args.Add(bagID);
	Tong_CellCall("CELL_requestSaveTongItem", args);
}


void URoleTongInterface::RequestTakeTongItem(const int32& srcOrder)
{
	KBEngine::FVariantArray args;
	args.Add(srcOrder);
	Tong_CellCall("CELL_requestTakeTongItem", args);
}

void URoleTongInterface::SortTongStoreItem(const int32& bagID)
{
	KBEngine::FVariantArray args;
	args.Add(bagID);
	Tong_CellCall("sortTongStoreItem", args);
}

void URoleTongInterface::OnRep_tongName()
{
	OnTongNameChange();
}

void URoleTongInterface::OnTongNameChange_Implementation()
{

}

void URoleTongInterface::ReceiveInviteJoinTong_Implementation(const FString& inviterName, const int32& inviterID, const FString& tongName, const FString& tongDBID)
{
	FTongInviteData TongInviteData;
	TongInviteData.InviterName = inviterName;
	TongInviteData.InviterEntityID = inviterID;
	TongInviteData.TongName = tongName;
	TongInviteData.TongDBID = tongDBID;
	TongInviteList.Add(TongInviteData);
}

void URoleTongInterface::ReplyInviteTong(bool IsAccept, int32 InviterID, FString TongDBID)
{
	KBEngine::FVariantArray args;
	args.Add(uint8(IsAccept));
	args.Add(InviterID);
	args.Add(TongDBID);
	Tong_BaseCall("replyInviteTong", args);
}

void URoleTongInterface::DeleteTongInvite(FTongInviteData TongInviteData)
{
	TongInviteList.Remove(TongInviteData);
}

void URoleTongInterface::ClearTongInfo()
{
	TongDatas.Empty();
	ApplicantDataList.Empty();
	NoReadApplicantList.Empty();
	TongApplyList.Empty();
	TongEventList.Empty();
	TongStoreEventList.Empty();
	TongSkillList.Empty();
	TongSkillDatas.Empty();
	TongBuildUpGrade.Empty();
	BHZBCandidates.Empty();
	Tong = nullptr;
}

void URoleTongInterface::onEnterWorld()
{
	Super::onEnterWorld();
}

void URoleTongInterface::onLeaveWorld()
{
	ClearTongInfo();
	Super::onLeaveWorld();
}

void URoleTongInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnRequestJoinList");
	ArrBlueFunc.Add("OnOtherReqJoinTong");
	ArrBlueFunc.Add("OnOtherCancelJoinTong");
	ArrBlueFunc.Add("OnRefuseJoinTong");
	ArrBlueFunc.Add("OnApplyJoinTongFailed");
	ArrBlueFunc.Add("OnApplyJoinTongSuccess");
	ArrBlueFunc.Add("UpdateTongDatas");
	ArrBlueFunc.Add("CLIENT_UpdateTongMember");
	ArrBlueFunc.Add("CLIENT_OnReceiveAllTong");
	ArrBlueFunc.Add("OnRequireJoinTong");
	ArrBlueFunc.Add("OnCancelJoinTong");
	ArrBlueFunc.Add("OnSetTitleName");
	ArrBlueFunc.Add("OnSetTitleNameFailed");
	ArrBlueFunc.Add("OnSetTongTitle"); 
	ArrBlueFunc.Add("OnSetGrade");
	ArrBlueFunc.Add("OnInitTongApplyList");
	
	ArrBlueFunc.Add("OnSetGradeFailed");
	ArrBlueFunc.Add("OnSetAffiche");
	ArrBlueFunc.Add("OnSetRecruitAffiche");
	ArrBlueFunc.Add("OnTongMoneyChange");
	ArrBlueFunc.Add("OnActivityChange");
	ArrBlueFunc.Add("OnLeaderChange");
	ArrBlueFunc.Add("OnGrowChange");
	ArrBlueFunc.Add("OnUpgrowBuild");
	ArrBlueFunc.Add("OnConferenceHallLevelChange");
	ArrBlueFunc.Add("OnDonateMoney");
	ArrBlueFunc.Add("OnLeaveTong");
	ArrBlueFunc.Add("OnKickTongMember");
	ArrBlueFunc.Add("OnQuitTong");
	ArrBlueFunc.Add("OnResearchTongSkill");
	ArrBlueFunc.Add("OnPauseTongSkill");
	ArrBlueFunc.Add("OnTongSkillProgressChange");
	ArrBlueFunc.Add("OnFinishResearchSkill");
	ArrBlueFunc.Add("OnFinishLearnSkill");
	ArrBlueFunc.Add("CLIENT_OnRequireTongEvent");
	ArrBlueFunc.Add("CLIENT_OnRequireTongStoreEvent");
	ArrBlueFunc.Add("OnMemberOnline");
	ArrBlueFunc.Add("OnMemberOffline");
	ArrBlueFunc.Add("OnSetGag");
	ArrBlueFunc.Add("OnContributionChange");
	ArrBlueFunc.Add("onTongMemberExpChange");
	ArrBlueFunc.Add("OnTongSign");
	ArrBlueFunc.Add("onDawnArrive");
	ArrBlueFunc.Add("OnGetSalaryFail");
	ArrBlueFunc.Add("OnJoinTong");
	ArrBlueFunc.Add("OnUpgrowTong");
	ArrBlueFunc.Add("OpenTongStore");
	ArrBlueFunc.Add("UpdateTongMemberInfo");
	ArrBlueFunc.Add("OnChangeNagualCB");
	ArrBlueFunc.Add("OpenTongNagualUI");
	ArrBlueFunc.Add("UpdateNagualType");
	ArrBlueFunc.Add("ReceiveInviteJoinTong");
	ArrBlueFunc.Add("OnSureSignUpBHZBMember");
	Supper::InitBlueCB();
}

void URoleTongInterface::ReadyToSignUpBHZBMember(TArray<FBHZBSIGNMEMBERDATA> signUpMemberDatas)
{
	if (!IsValid(Tong))
	{
		return;
	}
	int32 title = Tong->PlayerMember->title;
	if ((title == int32(TONG_TITLE_TYPE::TONG_TITLE_1))||(title == int32(TONG_TITLE_TYPE::TONG_TITLE_3)))
	{
		KBEngine::FVariantArray args;
		KBEngine::FVariantArray members;
		for (auto member : signUpMemberDatas)
		{
			FBHZB_SIGN_MEMBER_DATA tempMember;
			tempMember.signID = member.SignID;
			tempMember.groupID = member.GroupID;
			tempMember.captainDBID = member.CaptainDBID;
			tempMember.memberDBIDs = member.MemberDBIDs;
			tempMember.isActive = member.IsActive;
			tempMember.pointIndex = member.PointIndex;
			KBEngine::FVariantMap memberMap;
			tempMember.ToFVariantMap(memberMap);
			members.Add(FVariant(memberMap));
		}
		args.Add(members);
		Tong_CellCall("readyToSignUpBHZBMember", args);
	}
}

void URoleTongInterface::OnSureSignUpBHZBMember(const FVariant& Var)
{
	JoinBHZBMemberDatas.Empty();
	KBEngine::FVariantArray BHZBMemberDatas = Var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : BHZBMemberDatas)
	{
		FBHZB_SIGN_MEMBER_DATA BHZBMemberData = FBHZB_SIGN_MEMBER_DATA(data);
		FBHZBSIGNMEMBERDATA TempBHZBMemberData;
		TempBHZBMemberData.SignID = BHZBMemberData.signID;
		TempBHZBMemberData.CaptainDBID = BHZBMemberData.captainDBID;
		TempBHZBMemberData.GroupID = BHZBMemberData.groupID;
		TempBHZBMemberData.MemberDBIDs = BHZBMemberData.memberDBIDs;
		TempBHZBMemberData.IsActive = BHZBMemberData.isActive > 0 ? true : false;
		TempBHZBMemberData.PointIndex = BHZBMemberData.pointIndex;
		if (JoinBHZBMemberDatas.Contains(TempBHZBMemberData.GroupID))
		{
			JoinBHZBMemberDatas.Remove(TempBHZBMemberData.GroupID);
		}
		JoinBHZBMemberDatas.Add(TempBHZBMemberData.GroupID, TempBHZBMemberData);
	}
	for (auto It = JoinBHZBMemberDatas.CreateConstIterator(); It; ++It)
	{
	        TArray<FString> CandidateDBIDs;
		CandidateDBIDs.Empty();
		int32 TeamGroupID = It.Key();
		FBHZBSIGNMEMBERDATA BHZBmemberData = It.Value();
		FString CaptainDBID = BHZBmemberData.CaptainDBID;
		TArray<FString> MemberDBIDs = BHZBmemberData.MemberDBIDs;
		AddCandidateToBHZB(CaptainDBID, TeamGroupID, true);
		for (FString MemberDBID : MemberDBIDs)
		{
		      AddCandidateToBHZB(MemberDBID, TeamGroupID, false);
		}

	}
	BPOnSureSignUpBHZBMember();
	
}

void URoleTongInterface::SetbhzbSignUpMembersIsActive(int32 groupID, uint8 isActive, int32 pointIndex)
{
	if (JoinBHZBMemberDatas.Contains(groupID))
	{
		JoinBHZBMemberDatas[groupID].IsActive = isActive > 0 ? true : false;
		JoinBHZBMemberDatas[groupID].PointIndex = pointIndex;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnSetbhzbSignUpMembersIsActive.Broadcast(groupID, bool(isActive), pointIndex);
		}
	}
}

bool URoleTongInterface::AddCandidateToBHZB(FString MemberDBID, int32 TeamGroupID, bool IsCaptain )
{
	bool IsAddSuccess = false;
	if (!IsValid(Tong))
	{
		return false;
	}
	bool IsInCandates = false;
	for (FBHZBCandidate& BHZBCandidate: BHZBCandidates)
	{
		if (BHZBCandidate.CandidateDBID == MemberDBID)
		{
			IsInCandates = true;
			BHZBCandidate.TeamGroupID = TeamGroupID;
			BHZBCandidate.IsCaptain = IsCaptain;
			break;
		}
	}
	if (!IsInCandates)
	{
		UTongMember* tongMember = nullptr;
		if (Tong->TongMembers.Contains(MemberDBID))
		{
			tongMember = Tong->TongMembers[MemberDBID];
		}
		else if (Tong->PlayerMember->DBID.Equals(MemberDBID))
		{
			tongMember = Tong->PlayerMember;
		}
		if (IsValid(tongMember))
		{
			if ((tongMember->MilitaryRank >= 4) && (tongMember->SoldierAmount >= 200))
			{
				FBHZBCandidate LocalCandidate;
				LocalCandidate.CandidateDBID = MemberDBID;
				LocalCandidate.CandidateName = tongMember->name;
				LocalCandidate.SoldierAmount = tongMember->SoldierAmount;
				LocalCandidate.TeamGroupID = TeamGroupID;
				LocalCandidate.IsCaptain = IsCaptain;
				BHZBCandidates.Add(LocalCandidate);
				IsAddSuccess = true;
			}
		}
		if (IsAddSuccess)
		{
			BHZBCandidates.Sort([](const FBHZBCandidate& A, const FBHZBCandidate& B) { return A.SoldierAmount > B.SoldierAmount; });
		}
	}
	return IsAddSuccess;
}

bool URoleTongInterface::RemoveCandidateFromBHZB(FString MemberDBID)
{
	bool isCanRemove = false;
	FBHZBCandidate LocalBHZBCandidate;
	for (FBHZBCandidate& BHZBCandidate: BHZBCandidates)
	{
		if (BHZBCandidate.CandidateDBID == MemberDBID)
		{
			LocalBHZBCandidate = BHZBCandidate;
			isCanRemove = true;
			break;
		}
	}
	if (isCanRemove)
	{
		BHZBCandidates.Remove(LocalBHZBCandidate);
		BHZBCandidates.Sort([](const FBHZBCandidate& A, const FBHZBCandidate& B) { return A.SoldierAmount > B.SoldierAmount; });
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnRemoveCandidateFromBHZB.Broadcast(MemberDBID);
		}
	}
	return isCanRemove;
}

void URoleTongInterface::SetIsSeletedCandidateToBHZB(FString MemberDBID, int32 TeamGroupID, bool IsCaptain)
{
	for (FBHZBCandidate& BHZBCandidate : BHZBCandidates)
	{
		if (BHZBCandidate.CandidateDBID == MemberDBID)
		{
			BHZBCandidate.TeamGroupID = TeamGroupID;
			BHZBCandidate.IsCaptain = IsCaptain;
		}
	}
}

bool URoleTongInterface::IsCandidateSelected(FString MemberDBID)
{
	bool IsSelected = false;
	for (FBHZBCandidate& BHZBCandidate: BHZBCandidates)
	{
		if (BHZBCandidate.CandidateDBID == MemberDBID)
		{
			IsSelected = BHZBCandidate.TeamGroupID > 0 ? true : false;;
			break;
		}	
	}
	return IsSelected;
}

void URoleTongInterface::ClearAllTongSignMemberData()
{
	JoinBHZBMemberDatas.Empty();
	BHZBCandidates.Empty();
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnClearAllTongSignMemberData.Broadcast();
	}
}

void URoleTongInterface::SignUpTongPlunder(const FString& targetTongDBID)
{
	KBEngine::FVariantArray args;
	args.Add(targetTongDBID);
	Tong_BaseCall(TEXT("signUpTongPlunder"), args);
}

void URoleTongInterface::PlunderAddMember(const FString& playerDBID)
{
	KBEngine::FVariantArray args;
	args.Add(playerDBID);
	Tong_BaseCall(TEXT("plunderAddMember"), args);
}

void URoleTongInterface::PlunderRemoveMember(const FString&PlayerDBID)
{
	KBEngine::FVariantArray args;
	args.Add(PlayerDBID);
	Tong_BaseCall(TEXT("plunderRemoveMember"), args);
}

void URoleTongInterface::OnPlunderMemberChange(const TArray<FVariant>& MemberDBIDList)
{
	PlunderMembers.Empty();
	for (auto DBID: MemberDBIDList)
	{
		PlunderMembers.Add(DBID.GetValue<FString>());
	}

	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnPlunderMemberChange.Broadcast();
	}
}

void URoleTongInterface::OpenPlunderTongListWnd(const FVariant& TongInfos)
{
	PlunderTongDatas.Empty();
	JOIN_TONG_DATAS tempData = JOIN_TONG_DATAS(TongInfos);
	for (auto data : tempData.tongDatas)
	{
		FTongJoinData joinData;
		joinData.TongDBID = data.TongDBID;
		joinData.TongName = data.Name;
		joinData.TongLevel = data.Level;
		joinData.TongActivity = data.Activity;
		joinData.TongNum = data.TongNum;
		joinData.TotalNum = data.TotalNum;
		joinData.LeaderName = data.LeaderName;
		joinData.Money = FSTRING_TO_INT64(data.Money);
		joinData.RecruitAffiche = data.Recruit;
		joinData.TongLeague = data.League;
		joinData.OccupyCity = data.City;
		joinData.Shenshou = data.ShenShou;
		PlunderTongDatas.Add(joinData.TongDBID, joinData);
	}
	PlunderTongDatas.ValueSort([](const FTongJoinData& A, const FTongJoinData& B)->bool
	{
		if (A.TongLevel > B.TongLevel) return true;
		if (A.TongLevel < B.TongLevel) return false;
		if (A.TongNum > B.TongNum) return true;
		if (A.TongNum < B.TongNum) return false;
		if (A.TongDBID < B.TongDBID) return true;
		if (A.TongDBID > B.TongDBID) return false;
		return false;
	});

	OnOpenPlunderTongListWnd();
}

TArray<UTongMember*> URoleTongInterface::GetPlunderMemberInfo()
{
	TArray<UTongMember*> TempList;
	if (PlunderMembers.Contains(Tong->PlayerMember->DBID))
	{
		TempList.Add(Tong->PlayerMember);
	}
	if (IsValid(Tong))
	{
		for (auto IT = Tong->TongMembers.CreateConstIterator(); IT; ++IT)
		{
			if (PlunderMembers.Contains(IT.Value()->DBID))
			{
				TempList.Add(IT.Value());
			}
		}
	}
	return TempList;
}

TArray<FTongJoinData> URoleTongInterface::SearchPlunderListByName(const FString& tongName)
{
	TArray<FTongJoinData> searchList;
	for (auto It = PlunderTongDatas.CreateConstIterator(); It; ++It)
	{
		if (tongName.IsEmpty() || It.Value().TongName.Contains(tongName))
		{
			searchList.Add(It.Value());
		}
	}
	return searchList;
}

TArray<FTongJoinData> URoleTongInterface::GetPlunderTongDatas(int32 Camp)
{
	TArray<FTongJoinData> TempData;
	for (auto It = PlunderTongDatas.CreateConstIterator(); It; ++It)
	{
		TempData.Add(It.Value());
	}
	return TempData;
}

FTongJoinData URoleTongInterface::GetPlunderTongDataByTongDBID(FString TongDBID, bool& IsSuccess)
{
	for (auto It = PlunderTongDatas.CreateConstIterator(); It; ++It)
	{
		if (It.Value().TongDBID == TongDBID)
		{
			IsSuccess = true;
			return It.Value();
		}
	}
	IsSuccess = false;
	return FTongJoinData();
}

void URoleTongInterface::OnOpenPlunderTongListWnd_Implementation()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TongPlunderList"));
	}
}

void URoleTongInterface::Tong_BaseCall(const FString& name, KBEngine::FVariantArray& args)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::Tong_BaseCall : pKBEApp!"));
		return;
	}
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UURoleTongInterface::Tong_BaseCall : player!"));
		return;
	}

	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UURoleTongInterface::Tong_BaseCall : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	player->BaseCall(name, args);
}

void URoleTongInterface::Tong_CellCall(const FString& name, KBEngine::FVariantArray& args)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::Tong_CellCall : pKBEApp!"));
		return;
	}
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::Tong_CellCall : player!"));
		return;
	}

	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::Tong_CellCall : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	player->CellCall(name, args);
}

void URoleTongInterface::InitTongGrade(bool isPlayer)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::InitTongGrade : Tong!"));
		return;
	}
	SysGrades.Empty();
	DefaultGrades.Empty();
	ForbidGrades.Empty();
	UCfgManager* cfgMgr = UUECS3GameInstance::Instance->CfgManager;
	
	const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_GRADE_DATA);
	if (table)
	{
		int32 titleID = Tong->PlayerMember->title;
		TArray<FTongGradeDATA*> TongGradeList;
		table->GetAllRows(TongGradeList);
		for (FTongGradeDATA* tongGrade : TongGradeList)
		{
			if (titleID == (uint8)tongGrade->TongType)
			{
				int32 sysGrade(0);
				for (auto g : tongGrade->TONG_SYSTEM_GRADE)
				{
					sysGrade |= (1 << (uint8)g);
				}
				SysGrades.Add(tongGrade->uiTongType, sysGrade);

				int32 defGrade(0);
				for (auto g : tongGrade->TONG_DEFAULT_GRADE)
				{
					defGrade |= (1 << (uint8)g);
				}
				DefaultGrades.Add(tongGrade->uiTongType, defGrade);

				int32 fobGrade(0);
				for (auto g : tongGrade->TONG_FORBID_GRADE)
				{
					fobGrade |= (1 << (uint8)g);
				}
				ForbidGrades.Add(tongGrade->uiTongType, fobGrade);
			}
		}
	}
}

void URoleTongInterface::InitTongBuildLevel()
{
	if (TongBuildUpGrade.Num() == 0)
	{
		UCfgManager* cfgMgr = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_BUILD_LEVEL_DATA);
		if (IsValid(table))
		{
			TArray<FTongBuildLevelDATA*> buildDatas;
			table->GetAllRows(buildDatas);
			for (FTongBuildLevelDATA* build : buildDatas)
			{
				uint8 level = build->level;
				TongBuildUpGrade.Add(level, build->upGradeData);
			}
		}
	}
}

void URoleTongInterface::InitTongSkill()
{
	UCfgManager* cfgMgr = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_SKILL_DATA);
	if (IsValid(table))
	{
		TArray<FTongSkillDATA*> skillData;
		table->GetAllRows(skillData);

		TArray<int32> tempList;
		for (FTongSkillDATA* skill : skillData)
		{
			if (skill->Level == 1)
			{
				TArray<int32> SkillList;
				SkillList.Add(skill->SkillID);
				TongSkillList.Add(SkillList);
				TongSkillDatas.Add(skill->SkillID, skill);
			}
			else
			{
				if (TongSkillList.Num())
				{
					TArray<int32> lastSkillList = TongSkillList[TongSkillList.Num() - 1];
					int32 lastSkillID = lastSkillList[lastSkillList.Num() - 1];
					if (TongSkillDatas[lastSkillID]->NextSkill == skill->SkillID)
					{
						TongSkillList[TongSkillList.Num() - 1].Add(skill->SkillID);
						TongSkillDatas.Add(skill->SkillID, skill);
					}
				}
				
			}
		}
	}

}

int32 URoleTongInterface::GetPlayerTongResSkillLevel(TArray<int32> SkillList)
{
	TArray<int32> playerSkillList = UUECS3GameInstance::Instance->SkillManager->GetPlayerSkillIdList();
	for (auto id : SkillList)
	{
		if (playerSkillList.Contains(id))
		{
			return TongSkillDatas[id]->Level;
		}
	}
	return 0;
}

void URoleTongInterface::UpdateTongMemberInfo_Implementation(const FString& playerDBID, const int32& level, const FString& birthSpace, const int32& soldierAmount, const int32& militaryRank)
{
	if (IsValid(Tong))
	{
		if (Tong->TongMembers.Contains(playerDBID))
		{
			UTongMember* member = Tong->TongMembers[playerDBID];
			member->level = level;
			member->localSpace = birthSpace;
			member->SoldierAmount = soldierAmount;
			member->MilitaryRank = militaryRank;
		}
		else if (Tong->PlayerMember->DBID.Equals(playerDBID))
		{
			Tong->PlayerMember->level = level;
			Tong->PlayerMember->localSpace = birthSpace;
			Tong->PlayerMember->SoldierAmount = soldierAmount;
			Tong->PlayerMember->MilitaryRank = militaryRank;
		}
	}
}

void URoleTongInterface::RequestChangeNagual(int32	nagualType)
{
	KBEngine::FVariantArray args;
	args.Add(nagualType);
	Tong_BaseCall(TEXT("changeNagual"), args);
}

void URoleTongInterface::OnChangeNagualCB_Implementation(const uint8& result)
{
}

void URoleTongInterface::OpenTongNagualUI_Implementation()
{
}

void URoleTongInterface::UpdateNagualType_Implementation(const int32& nagualType)
{
	Tong->ShenShou = nagualType;
}

void URoleTongInterface::OnRemoveApplyJoinTongMember_Implementation(const FString& playerDBID)
{
	RemoveNoReadApplicantList(playerDBID);

	for (auto it = ApplicantDataList.CreateConstIterator(); it; ++it)
	{
		if (it->DBID.Equals(playerDBID))
		{
			ApplicantDataList.RemoveAt(it.GetIndex());
			break;
		}
	}
}

void URoleTongInterface::SetTongAllocation(const TONG_PICKUP_TYPE& allocation)
{
	if (IsValid(Tong))
	{
		if (Tong->allocation == allocation)
			return;

		int32 title = Tong->PlayerMember->title;
		if ((title == int32(TONG_TITLE_TYPE::TONG_TITLE_1)) || (title == int32(TONG_TITLE_TYPE::TONG_TITLE_3)))
		{
			KBEngine::FVariantArray args;
			args.Add((uint8)allocation);
			Tong_CellCall("reqSetTongAllocation", args);
		}
	}
}

void URoleTongInterface::onSetTongAllocation_Implementation(const uint8& allocation)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::onSetTongAllocation : Tong!"));
		return;
	}
	Tong->allocation = (TONG_PICKUP_TYPE)allocation;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnSetTongBattleAllocation.Broadcast(Tong->allocation);
	}
}

void URoleTongInterface::SetTongBHLDAllocation(const TONG_PICKUP_TYPE& allocation)
{
	if (IsValid(Tong))
	{
		if (Tong->BHLDAllocation == allocation)
			return;

		int32 title = Tong->PlayerMember->title;
		if ((title == int32(TONG_TITLE_TYPE::TONG_TITLE_1)) || (title == int32(TONG_TITLE_TYPE::TONG_TITLE_3)))
		{
			KBEngine::FVariantArray args;
			args.Add((uint8)allocation);
			Tong_CellCall("reqSetTongBHLDAllocation", args);
		}
	}
}

void URoleTongInterface::onSetTongBHLDAllocation_Implementation(const uint8& allocation)
{
	if (!IsValid(Tong))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTongInterface::onSetTongBHLDAllocation : Tong!"));
		return;
	}
	Tong->BHLDAllocation = (TONG_PICKUP_TYPE)allocation;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnSetTongPlunderAllocation.Broadcast(Tong->BHLDAllocation);
	}
}


void URoleTongInterface::AddTongBlockList(const FString & memberDBID)
{
	KBEngine::FVariantArray args;
	args.Add(memberDBID);
	Tong_CellCall(TEXT("addTongBlockList"), args);

}

void URoleTongInterface::RemoveTongBlockList(const FString & memberDBID)
{
	KBEngine::FVariantArray args;
	args.Add(memberDBID);
	Tong_CellCall(TEXT("removeTongBlockList"), args);
}


CONTROL_COMPILE_OPTIMIZE_END