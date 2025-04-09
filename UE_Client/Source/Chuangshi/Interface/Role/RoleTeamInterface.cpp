// Fill out your copyright notice in the Description page of Project Settings.
#include "RoleTeamInterface.h"

#include "JsonObject.h"

#include "KBEngine.h"
#include "Entity/Alias.h"

#include "GameData/ConstDataBP.h"

#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/ConvertUtil.h"
#include "Manager/MessageManager.h"
#include "Manager/BuffManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/CS3Debug.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"


CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTeamInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnUpdateMemeberPos, &URoleTeamInterface::CLIENT_OnUpdateMemeberPos, const FVariant& )
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTeamInterface, Supper)
//CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP, &URoleTeamInterface::Set_HP, int32)
CS3_END_INTERFACE_PROPERTY_MAP()


URoleTeamInterface::URoleTeamInterface()
{
}

URoleTeamInterface::~URoleTeamInterface()
{
}

void URoleTeamInterface::BeginDestroy()
{
	Super::BeginDestroy();
}

bool URoleTeamInterface::CheckInTeam(int32 PlayerEntityID)
{
	APlayerCharacter* TempPlayer = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(PlayerEntityID));
	if (TempPlayer)
	{
		return TempPlayer->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_TEAMMING);
	}
	return false;
}

bool URoleTeamInterface::IsTeammate(int32 TargetID) 
{
	for (FTeamMemberData i : Members) 
	{
		if (i.EntityID == TargetID) 
		{
			return true;
		}
	}
	return false;
}

void URoleTeamInterface::teamInviteFC(const int32 targetPlayerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::teamInviteFC : GetEntity()!"));
		return;
	}

	int32 targetFlag = UGolbalBPFunctionLibrary::GetIntPropertyValue(targetPlayerID, TEXT("forbidTeamInvite"));
	if (targetFlag == 1)
	{
		UGolbalBPFunctionLibrary::StatusMessage(2138, TEXT(""));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetPlayerID);
	this->GetEntity()->CellCall(TEXT("teamInviteFC"), args);
}

void URoleTeamInterface::requestJoinTeamNear(const int32 targetPlayerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::requestJoinTeamNear : GetEntity()!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(targetPlayerID);
	this->GetEntity()->CellCall(TEXT("requestJoinTeamNear"), args);
}

void URoleTeamInterface::changeCaptainFC(const int32 newCaptainID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::changeCaptainFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(newCaptainID);
	this->GetEntity()->CellCall(TEXT("changeCaptainFC"), args);
}

void URoleTeamInterface::remoteTeamInviteFC(const FString& targetPlayerName)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::remoteTeamInviteFC : GetEntity()!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(targetPlayerName);
	this->GetEntity()->CellCall(TEXT("remoteTeamInviteFC"), args);
}

void URoleTeamInterface::replyTeamInviteByFC(const int32 isAgree, const int32 answerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::replyTeamInviteByFC: GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(isAgree);
	args.Add(answerID);
	this->GetEntity()->CellCall(TEXT("replyTeamInviteByFC"), args);
}

void URoleTeamInterface::ReplyTeammateInviteFC(const int32 targetID, const FString targetName, const int32 teammateID, uint8 isAgree)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::ReplyTeammateInviteFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetID);
	args.Add(targetName);
	args.Add(teammateID);
	args.Add(isAgree);
	this->GetEntity()->CellCall(TEXT("replyTeammateInvite"), args);
}

void URoleTeamInterface::replyPlayerJoinTeamFC(const int32 isAgree, const int32 RequesterID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::replyPlayerJoinTeamFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(isAgree);
	args.Add(RequesterID);
	this->GetEntity()->CellCall(TEXT("replyPlayerJoinTeamFC"), args);
}

void URoleTeamInterface::DisbandTeamFC()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::DisbandTeamFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("disbandTeamFC"), args);
}

void URoleTeamInterface::LeaveTeamFC(const int32 leavePlayerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::LeaveTeamFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(leavePlayerID);
	this->GetEntity()->CellCall(TEXT("leaveTeamFC"), args);
}

void URoleTeamInterface::RequestTeammateInfoFC(const int32 TeammateID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::RequestTeammateInfoFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(TeammateID);
	this->GetEntity()->CellCall(TEXT("requestTeammateInfoFC"), args);
}

void URoleTeamInterface::SetAllocationFC(const int32 allocation)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::SetAllocationFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(allocation);
	this->GetEntity()->CellCall(TEXT("setAllocationFC"), args);
}

void URoleTeamInterface::SetQualityFC(const int32 quality)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::SetQualityFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(quality);
	this->GetEntity()->CellCall(TEXT("setQualityFC"), args);
}

void URoleTeamInterface::setForbidTeamInviteFC(const uint8 isForbid)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::setForbidTeamInviteFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(isForbid);
	this->GetEntity()->CellCall(TEXT("setForbidTeamInviteFC"), args);
}

void URoleTeamInterface::requestAddTeamSignFC(const int32 targetID, const int32 SignType)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::requestAddTeamSignFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetID);
	args.Add(SignType);
	this->GetEntity()->CellCall(TEXT("requestAddTeamSignFC"), args);
}

void URoleTeamInterface::requestLeadTeamFollowFC()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::requestLeadTeamFollowFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("requestLeadTeamFollowFC"), args);
}

void URoleTeamInterface::cancelLeadTeamFollowFC()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::cancelLeadTeamFollowFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("cancelLeadTeamFollowFC"), args);
}

void URoleTeamInterface::requestNormalFollowFC(const int32 targetID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::requestNormalFollowFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetID);
	this->GetEntity()->CellCall(TEXT("requestNormalFollowFC"), args);
}

void URoleTeamInterface::cancelNormalFollowFC()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::cancelNormalFollowFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("cancelNormalFollowFC"), args);
}

void URoleTeamInterface::requestRoleTeamSpellBoxFollow(const int32 targetID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::requestRoleTeamSpellBoxFollow : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetID);
	this->GetEntity()->CellCall(TEXT("requestRoleTeamSpellBoxFollow"), args);
}

void URoleTeamInterface::TeamInviteByTeammate_Implementation(const int32 targetID, const FString& targetName, const int32 targetCamp, const int32 targetProfession, const int32 targetLevel, const FString& teammateName, const int32 teammateID)
{
	FTeamMsgData MsgData;
	MsgData.ID = targetID;
	MsgData.Name = targetName;
	MsgData.Camp = targetCamp;
	MsgData.Profession = targetProfession;
	MsgData.Level = targetLevel;
	MsgData.IsInvite = true;
	MsgData.TeammateID = teammateID;
	MsgData.TeammateName = teammateName;
	MsgData.IsFastTeamApply = false;
	TeamInviteList.Add(MsgData);
}

void URoleTeamInterface::OnTeamInviteBy_Implementation(const int32 inviterID, const FString& inviterName, const int32 inviterCamp, const int32 inviterProfession, const int32 inviterLevel)
{
	FTeamMsgData MsgData;
	MsgData.ID = inviterID;
	MsgData.Name = inviterName;
	MsgData.Camp = inviterCamp;
	MsgData.Profession = inviterProfession;
	MsgData.Level = inviterLevel;
	MsgData.IsInvite = true;
	MsgData.TeammateID = 0;
	MsgData.TeammateName = TEXT("");
	MsgData.IsFastTeamApply = false;
	TeamInviteList.Add(MsgData);
}

void URoleTeamInterface::OnTeamMemberAddBuff_Implementation(const int32 MemberID, const int32 BuffIndex, const int32 BuffID, const float BuffTotalTime, const float BuffHoldTime)
{
	if (UUECS3GameInstance::Instance)
	{
		TWeakObjectPtr<URoleTeamInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->BuffManager->AsyncLoadBuffAsset(FStreamableDelegate::CreateLambda([DelayThisPtr, BuffIndex, BuffID, BuffTotalTime, BuffHoldTime, MemberID]()
		{
			if (DelayThisPtr.IsValid())
			{
				URoleTeamInterface* DelayThis = DelayThisPtr.Get();
				FBuffUIData UIData = UUECS3GameInstance::Instance->BuffManager->CreateBuffUIData(BuffIndex, BuffID, BuffTotalTime, BuffHoldTime, 1);
				DelayThis->OnTeamMemberAddBuffBP(MemberID, UIData);
			}
		}), BuffID);
	}
}

void URoleTeamInterface::OnTeamMemberRemoveBuff_Implementation(const int32 MemberID, const int32 BuffIndex)
{

}

void URoleTeamInterface::OnTeamMemberResetBuffTime_Implementation(const int32 MemberID, const int32 BuffIndex, const float BuffHoldTime)
{

}

void URoleTeamInterface::modifyAllocation_Implementation(const int32 allocation)
{
	Allocation = TEAM_PICKUP_TYPE(allocation);
}

void URoleTeamInterface::modifyQuality_Implementation(const int32 Quality)
{

}

void URoleTeamInterface::teamInfoNotifyOnJoin_Implementation(const int32 captainID, const int32 teamID, const int32 allocation, const int32 quality, const int32 signerID, const TArray<int32>& teamSignKeys, const TArray<int32>& teamSignValues)
{
	Team_ID = teamID;
	Captain_ID = captainID;
	Allocation = TEAM_PICKUP_TYPE(allocation);
	for (auto i = teamSignKeys.CreateConstIterator(); i; ++i)
	{
		int32 index = i.GetIndex();
		TeamSignData.Add(teamSignKeys[index],teamSignValues[index]);
	}
	teamInfoNotifyOnJoinBP(captainID, teamID);
	if (MemberDataFarTimer.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberDataFarTimer);
		}
	}
	if (MemberDataNearTimer.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberDataNearTimer);
		}
	}
	if (MemberSynPosTimer.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberSynPosTimer);
		}
	}
	UpdateMemberPos();
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(MemberDataFarTimer, this, &URoleTeamInterface::UpdateMemberDataFar, 5.0f, true);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(MemberDataNearTimer, this, &URoleTeamInterface::UpdateMemberDataNear, 0.5f, true);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(MemberSynPosTimer, this, &URoleTeamInterface::UpdateMemberPos, 3.0f, true);
	}
}

void URoleTeamInterface::teammateInfoNotify_Implementation(const int32 PlayerID, const int32 Level, const int32 HP, const int32 HP_Max, const int32 MP, const int32 MP_Max, const FString& SpaceScriptID, const int32& LineNumber)
{
	//if (PlayerID == EntityID) return; //是自己
	for (int i = 0; i < Members.Num(); i++)
	{
		if (PlayerID == Members[i].EntityID)
		{

			Members[i].Level = Level;
			Members[i].HP = HP;
			Members[i].HPMax = HP_Max;
			Members[i].MP = MP;
			Members[i].MPMax = MP_Max;
			Members[i].SpaceScriptID = SpaceScriptID;
			Members[i].LineNumber = LineNumber;
			OnTeammateInfoNotify(Members[i]);
		}
	}
}

void URoleTeamInterface::leaveTeamNotify_Implementation(const int32 leavePlayerID, const uint8 isMyself)
{

	if (isMyself!=0)///自己离队
	{
		Team_ID = 0;
		Captain_ID = 0;
		Allocation = TEAM_PICKUP_TYPE::TEAM_PICKUP_TYPE_NONE;
		Members.Empty();

		TeamSignData.Empty();
		TeamPosMap.Empty();
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberSynPosTimer);
		}
	}
	else 
	{
		for (int i = 0; i < Members.Num(); i++)
		{
			if (Members[i].EntityID == leavePlayerID)
			{
				Members.RemoveAt(i);
			}
		}
		if (TeamSignData.Contains(leavePlayerID))
		{
			TeamSignData.Remove(leavePlayerID);
		}
	}
	bool _isMyself = isMyself == 1 ? true : false;
	leaveTeamNotifyBP(leavePlayerID, _isMyself);
}

void URoleTeamInterface::disbandTeamNotify_Implementation()
{
	Team_ID = 0;
	Captain_ID = 0;
	Allocation = TEAM_PICKUP_TYPE::TEAM_PICKUP_TYPE_NONE;
	Members.Empty();

	TeamSignData.Empty();
	TeamPosMap.Empty();
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberSynPosTimer);
	}
}

void URoleTeamInterface::changeCaptainNotify_Implementation(const int32 captainID)
{
	Captain_ID = captainID;
}

void URoleTeamInterface::logoutNotify_Implementation(const int32 logoutEntitiyID)
{
	if (Members.Num() <= 0)return;
	for (int i = 0; i < Members.Num(); i++)
	{
		if (Members[i].EntityID == logoutEntitiyID)
		{
			Members[i].OnLineState = false;
			break;
		}
	}
}

void URoleTeamInterface::onRejoinTeam_Implementation(const int32 oldEntitiyID, const int32 newEntitiyID)
{
	if (Members.Num() <= 0)return;
	UpdateMemberDataByReJoinTeam(oldEntitiyID, newEntitiyID);
	UpdateTeamSignDataByReJoinTeam(oldEntitiyID, newEntitiyID);
}

bool URoleTeamInterface::IsAllMemberSameLineNumber()
{
	int32 TempLineNumber = 0;
	for (auto Member: Members)
	{
		if (Member.EntityID == Captain_ID)
		{
			TempLineNumber = Member.LineNumber;
			break;
		}
	}

	for (auto Member : Members)
	{
		if (Member.LineNumber != TempLineNumber)
		{
			return false;
		}
	}

	return true;
}

void URoleTeamInterface::UpdateMemberDataByReJoinTeam(int32 oldEntitiyID, int32 newEntitiyID)
{
	for (int i = 0; i < Members.Num(); i++)
	{
		if (Members[i].EntityID == oldEntitiyID)
		{
			Members[i].OnLineState = true;
			Members[i].EntityID = newEntitiyID;
			break;
		}
	}
}
void URoleTeamInterface::UpdateTeamSignDataByReJoinTeam(int32 oldEntitiyID, int32 newEntitiyID)
{
	if (TeamSignData.Contains(oldEntitiyID))
	{
		int32 SignNumber = TeamSignData.FindRef(oldEntitiyID);
		TeamSignData.Remove(oldEntitiyID);
		TeamSignData.Add(newEntitiyID, SignNumber);
	}
}

void URoleTeamInterface::addTeamMember_Implementation(const FString& newMemberDBID, const int32 newMemberID, const FString& newMemberName, const int32 newMemberProfession, const int32 isOnline, const int32 newMemberLevel)
{
	FTeamMemberData pMem = FTeamMemberData();
	pMem.PlayerDBID = newMemberDBID;
	pMem.EntityID = newMemberID;
	pMem.PlayerName = newMemberName;
	pMem.Profession = newMemberProfession;
	pMem.Level = newMemberLevel;
	pMem.OnLineState = isOnline;
	pMem.Camp = 1;
	pMem.Gender = 1;
	pMem.HP = 0;
	pMem.HPMax = 0;
	pMem.MP = 0;
	pMem.MPMax = 0;
	pMem.SpaceScriptID = TEXT("");
	pMem.LineNumber = 0;
	Members.Add(pMem);
	addTeamMemberBP(pMem);
}

void URoleTeamInterface::OnReceiveJoinTeamRequest_Implementation(const int32 requesterID, const FString& roleName, const int32 camp, const int32 profession, const int32 level)
{
	FTeamMsgData MsgData;
	MsgData.ID = requesterID;
	MsgData.Name = roleName;
	MsgData.Camp = camp;
	MsgData.Profession = profession;
	MsgData.Level = level;
	MsgData.IsInvite = false;
	MsgData.TeammateID = 0;
	MsgData.TeammateName = TEXT("");
	MsgData.IsFastTeamApply = false;
	TeamInviteList.Add(MsgData);
}

void URoleTeamInterface::UpdateMemberDataFar()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::UpdateMemberDataFar : GetEntity()!"));
		return;
	}
	if (Captain_ID == 0)
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberDataFarTimer);
		}
		MemberDataFarTimer = FTimerHandle();
		return;
	}
	for (auto Member : Members)
	{
		if (Member.OnLineState == 0) continue;
		int32 PlayerID = Member.EntityID;
		KBEngine::Entity* Player = UGolbalBPFunctionLibrary::FindEntity(PlayerID);
		if (Player != nullptr) continue;
		KBEngine::FVariantArray Args;
		Args.Add(PlayerID);
		GetEntity()->CellCall(TEXT("requestTeammateInfoFC"), Args);
	}
}

void URoleTeamInterface::UpdateMemberDataNear()
{
	if (Captain_ID == 0)
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberDataNearTimer);
		}
		MemberDataNearTimer = FTimerHandle();
		return;
	}
	for (auto Member : Members)
	{
		int32 PlayerID = Member.EntityID;
		KBEngine::Entity* Player = UGolbalBPFunctionLibrary::FindEntity(PlayerID);
		if (Player == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::UpdateMemberDataNear : GetEntity()!"));
			continue;
		}
		int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerID, TEXT("level"));
		int32 PlayerHP = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerID, TEXT("HP"));
		int32 PlayerHP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerID, TEXT("HP_Max"));
		int32 PlayerMP = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerID, TEXT("MP"));
		int32 PlayerMP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerID, TEXT("MP_Max"));
		FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID"));
		int32 spaceType = FSTRING_TO_INT(UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_TYPE")));
		int32 LineNumber = 0;
		if (spaceType == int32(ENUM_SPACE_TYPE::SPACE_TYPE_MULTILINE))
		{
			LineNumber = FSTRING_TO_INT(UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_DATA_LINE_NUMBER")));
		}
		teammateInfoNotify(PlayerID, PlayerLevel, PlayerHP, PlayerHP_Max, PlayerMP, PlayerMP_Max, SpaceScriptID,LineNumber);
	}
}

void URoleTeamInterface::UpdateMemberPos()
{
	if (Captain_ID == 0)
	{
		TeamPosMap.Empty();
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MemberSynPosTimer);
		}
	}
	TArray<int32> needToUpdateIDs;
	for (auto member:Members)
	{
		KBEngine::Entity* player = UGolbalBPFunctionLibrary::FindEntity(member.EntityID);
		if (player == nullptr)
		{
			needToUpdateIDs.Add(member.EntityID);
		}
		else
		{
			APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(player->Actor());
			if (!IsValid(RoleCharacter))
			{
				CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::UpdateMemberPos : RoleCharacter!"));
				continue;
			}
			FString playerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(member.EntityID, "playerName");
			AddTeamPosMap(member.EntityID, RoleCharacter->GetActorLocation(), playerName);
		}
	}
	if (needToUpdateIDs.Num() > 0)
	{
		if (GetEntity() == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::UpdateMemberPos: GetEntity()!"));
			return;
		}
		KBEngine::FVariantArray Args;
		Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(needToUpdateIDs));
		GetEntity()->CellCall(TEXT("CELL_updateMembersPos"), Args);
	}
}

void URoleTeamInterface::AddTeamSignCB_Implementation(const int32 TargetID, const int32 SignNumber)
{
	if (TeamSignData.Contains(TargetID))
	{
		///entity改标记
		TeamSignData.Remove(TargetID);
	}
	TeamSignData.Add(TargetID, SignNumber);
	///entity加标记
}

void URoleTeamInterface::ClearTeamSign() 
{
	TeamSignData.Empty();
}

bool URoleTeamInterface::HasTeam()
{
	return Team_ID != 0;
}

bool URoleTeamInterface::IsTeamFollowing()
{
	return TeamFollowTarget != 0;
}

void URoleTeamInterface::StartTeamFollow_Implementation(const int32 captainID)
{
	TeamFollowTarget = captainID;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TeamFollowTimer, this, 
			&URoleTeamInterface::DetectTeamFollow, TEAM_FOLLOW_DETECT_TICK, true);
	}
}

void URoleTeamInterface::StopTeamFollow_Implementation()
{
	TeamFollowTarget = 0;
	if (TeamFollowTimer.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TeamFollowTimer);
		}
	}
}

void URoleTeamInterface::FollowNewCaptain_Implementation(const int32 newCaptainID)
{
	StopTeamFollow();
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->StopMove();
	}

	TeamFollowTarget = newCaptainID;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TeamFollowTimer, this, 
			&URoleTeamInterface::DetectTeamFollow, TEAM_FOLLOW_DETECT_TICK, true);
	}
}

void URoleTeamInterface::DetectTeamFollow()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::DetectTeamFollow : GetEntity()!"));
		return;
	}
	///记录不合法的开始时间
	if (TeamFollowWaitTime == FDateTime::MinValue())
	{
		TeamFollowWaitTime = FDateTime::UtcNow();
	}

	///找不到目标entity
	CS3Entity* TargetEntity = static_cast<CS3Entity*>(UUECS3GameInstance::Instance->pKBEApp->FindEntity(TeamFollowTarget));
	if (!TargetEntity || !TeamFollowWaitTimeCheck())
	{
		CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON::REASON_ENTITY_INVALID);
		return;
	}

	///找不到actor
	AActor* SelfActor = this->GetEntity()->Actor();
	AActor* TargetActor = TargetEntity->Actor();
	if (!SelfActor || !TargetActor)
	{
		if (!TeamFollowWaitTimeCheck())
		{
			CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON::REASON_ENTITY_INVALID);
			return;
		}
	}

	///距离太远，直接取消跟随
	if (UGolbalBPFunctionLibrary::GetActorDistance(SelfActor, TargetActor) > TEAM_FOLLOW_DISTANCE * 100.0f)
	{
		CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON::REASON_TO_FAR_TO_LEADER);
		return;
	}

	///在保持范围内
	if (UGolbalBPFunctionLibrary::GetActorDistance(SelfActor, TargetActor) < TEAM_FOLLOW_KEEP_DISTANCE * 100.0f)
	{
		TeamFollowWaitTime = FDateTime::MinValue(); ///合法则重置，否则会累计
		return;
	}

	///找不到PlayerController
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!PlayerController || !TeamFollowWaitTimeCheck())
	{
		CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON::REASON_ENTITY_INVALID);
		return;
	}

	///正在追踪
	if (PlayerController->GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_TEAM_FOLLOW)
	{
		TeamFollowWaitTime = FDateTime::MinValue(); ///合法则重置，否则会累计
		return;
	}

	///追踪
	PlayerController->TeamFollowTraceTarget(TargetActor, TEAM_FOLLOW_KEEP_DISTANCE, FTraceCallback::CreateLambda([this](bool IsSuccess)
	{
		if (!IsSuccess) ///卡住了
		{
			if (!TeamFollowWaitTimeCheck())
			{
				CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON::REASON_ENTITY_INVALID);
				return;
			}
		}
		else
		{
			TeamFollowWaitTime = FDateTime::MinValue(); ///合法则重置，否则会累计
			return;
		}
	}));

}

bool URoleTeamInterface::TeamFollowWaitTimeCheck()
{
	if (FDateTime::UtcNow() - TeamFollowWaitTime > TEAM_FOLLOW_WAIT_TIME * 10000000)
	{
		return false;
	}
	return true;
}

void URoleTeamInterface::CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON CancelReason)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CancelTeamFollowForce : GetEntity()!"));
		return;
	}
	StopTeamFollow();	///先停掉timer，否则可能会多次通知服务器
	KBEngine::FVariantArray args;
	args.Add(uint8(CancelReason));
	this->GetEntity()->CellCall(TEXT("cancelTeamFollowFC"), args);
}

void URoleTeamInterface::RoleTeamSpellBoxFollow_Implementation(int32 TargetID, float TotalTime)
{
	TeleportTargetID = TargetID;
}

bool URoleTeamInterface::IsNormalFollowing()
{
	return NormalFollowTarget != 0;
}

void URoleTeamInterface::StartNormalFollow_Implementation(const int32 targetID)
{
	NormalFollowTarget = targetID;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(NormalFollowTimer, this, 
			&URoleTeamInterface::DetectNormalFollow, TEAM_FOLLOW_DETECT_TICK, true);
	}
}

void URoleTeamInterface::StopNormalFollow_Implementation()
{
	NormalFollowTarget = 0;
	if (NormalFollowTimer.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(NormalFollowTimer);
		}
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->StopMove();   
	}
}

void URoleTeamInterface::CancelNormalFollowForce()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CancelNormalFollowForce : GetEntity()!"));
		return;
	}
	StopNormalFollow();	///先停掉timer，否则可能会多次通知服务器
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("cancelNormalFollowFC"), args);
}

void URoleTeamInterface::DetectNormalFollow()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::DetectNormalFollow : GetEntity()!"));
		return;
	}
	///记录不合法的开始时间
	if (NormalFollowWaitTime == FDateTime::MinValue())
	{
		NormalFollowWaitTime = FDateTime::UtcNow();
	}

	///找不到目标entity
	CS3Entity* TargetEntity = static_cast<CS3Entity*>(UUECS3GameInstance::Instance->pKBEApp->FindEntity(NormalFollowTarget));
	if (!TargetEntity)
	{
		if (!NormalFollowWaitTimeCheck())
		{
			CancelNormalFollowForce();
		}
		return;
	}

	///找不到actor
	AActor* SelfActor = this->GetEntity()->Actor();
	AActor* TargetActor = TargetEntity->Actor();
	if (!SelfActor || !TargetActor)
	{
		if (!NormalFollowWaitTimeCheck())
		{
			CancelNormalFollowForce();
		}
		return;
	}

	///找不到PlayerController
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!PlayerController)
	{
		if (!NormalFollowWaitTimeCheck())
		{
			CancelNormalFollowForce();
		}
		return;
	}
	
	float SelfToTargetDistance;
	APlayerCharacter* TargetCharacter = Cast<APlayerCharacter>(TargetActor);
	if (TargetCharacter && TargetCharacter->GetMovementComponent()->IsFalling())
	{
		SelfToTargetDistance = UGolbalBPFunctionLibrary::GetActorDistanceByJump(SelfActor, TargetActor);
	}
	else
	{
		SelfToTargetDistance = UGolbalBPFunctionLibrary::GetActorDistance(SelfActor, TargetActor);
	}
	
	///距离太远，直接取消跟随
	if (SelfToTargetDistance > TEAM_FOLLOW_DISTANCE * 100.0f)
	{
		CancelNormalFollowForce();
		return;
	}

	///在保持范围内 
	if (SelfToTargetDistance < TEAM_FOLLOW_KEEP_DISTANCE * 100.0f)
	{
		NormalFollowWaitTime = FDateTime::MinValue(); ///合法则重置，否则会累计
		return;
	}

	///正在追踪 
	if (PlayerController->GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_TEAM_FOLLOW)
	{
		NormalFollowWaitTime = FDateTime::MinValue(); ///合法则重置，否则会累计
		///这里不能return，因为超过与队长的距离后，也是跟随状态，但又不会向队长移动，就会卡死在这里
	}

	///追踪
	PlayerController->TeamFollowTraceTarget(TargetActor, TEAM_FOLLOW_KEEP_DISTANCE, FTraceCallback::CreateLambda([this](bool IsSuccess)
	{
		if (!IsSuccess) ///卡住了
		{
			if (!NormalFollowWaitTimeCheck())
			{
				CancelNormalFollowForce();
			}
		}
		else
		{
			NormalFollowWaitTime = FDateTime::MinValue(); ///合法则重置，否则会累计
		}
	}));
}

bool URoleTeamInterface::NormalFollowWaitTimeCheck()
{
	if (FDateTime::UtcNow() - NormalFollowWaitTime > TEAM_FOLLOW_WAIT_TIME * 10000000)
	{
		return false;
	}
	return true;
}

bool URoleTeamInterface::IsTeamMemberFull()
{
	return Members.Num() >= 5;
}

void URoleTeamInterface::ShareBigMapCustomMarkerToTeam(const FString& LevelName, const FVector Position, const int32 MarkerType)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::ShareBigMapCustomMarkerToTeam : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(LevelName);
	args.Add(Position);
	args.Add(MarkerType);
	this->GetEntity()->CellCall(TEXT("shareBigMapCustomMarker"), args);
}

void URoleTeamInterface::onMemberShareBigMapCustomMarker(const FString& MemberName, const FString& LevelName, const FVector Position, const int32 MarkerType)
{
	onMemberShareBigMapCustomMarkerBP(MemberName, LevelName, Position, MarkerType);
}

int32 URoleTeamInterface::GetMemberIndexOnFaBaoByEntityID(int32 memberID)
{
	if (Captain_ID == memberID)
	{
		return 0;
	}
	int32 CaptainIndex = -1;
	int32 memberIndex = -1;
	for (int i = 0; i < Members.Num(); i++)
	{
		if (Members[i].EntityID == Captain_ID)
		{
			CaptainIndex = i;
		}
		if (Members[i].EntityID == memberID)
		{
			memberIndex = i;
		}
	}
	if (CaptainIndex > memberIndex)
	{
		return memberIndex + 1;
	}
	return memberIndex;
}

void URoleTeamInterface::RemoveTeamSigner_Implementation(int32 TargetID)
{
	if (TeamSignData.Contains(TargetID))
	{
		TeamSignData.Remove(TargetID);
	}
}

void URoleTeamInterface::AddTeamPosMap(int32 entityID, FVector position, FString playerName)
{
	if (TeamPosMap.Contains(entityID))
	{
		TeamPosMap[entityID].position = position;
	}
	else
	{
		FBigmapActInfo Bmap;
		Bmap.objectID = entityID;
		Bmap.position = position;
		Bmap.playerName = playerName;
		TeamPosMap.Add(entityID, Bmap);
	}
}

void URoleTeamInterface::CLIENT_OnUpdateMemeberPos(const FVariant& BIGMAP_SHOW_INFO_1 )
{
	FBIGMAP_SHOW_INFO* info = new FBIGMAP_SHOW_INFO(BIGMAP_SHOW_INFO_1);
	AddTeamPosMap(info->objectID1, info->position2, info->name3);
}


void URoleTeamInterface::CELL_CallAllTeamMemberToCaptainLineNumber()
{
	TArray<int32> needToCallIDs;
	for (auto member : Members)
	{
		KBEngine::Entity* player = UGolbalBPFunctionLibrary::FindEntity(member.EntityID);
		if (player == nullptr)
		{
			needToCallIDs.Add(member.EntityID);
		}
	}
	if (needToCallIDs.Num() > 0)
	{
		if (GetEntity() == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CELL_CallAllTeamMemberToCaptainLineNumber : GetEntity()!"));
			return;
		}
		KBEngine::FVariantArray Args;
		Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(needToCallIDs));
		GetEntity()->CellCall(TEXT("CELL_callAllTeamMemberToCaptainLineNumber"), Args);
	}
}

void URoleTeamInterface::FastTeamOnMatchSuccess_Implementation()
{
}

void URoleTeamInterface::CLIENT_OnStartTeamSearch_Implementation(const FString& spaceName)
{

}
void URoleTeamInterface::CLIENT_OnFastTeamCancelMatch_Implementation()
{
	SetFastTeamSettingDefaultData();
}

void URoleTeamInterface::CLIENT_teamByApply_Implementation(const int32 applyID, const FString& applyName, const int32 applyCamp, const int32 applyProfession, const int32 applyLevel)
{
	FTeamMsgData MsgData;
	MsgData.ID = applyID;
	MsgData.Name = applyName;
	MsgData.Camp = applyCamp;
	MsgData.Profession = applyProfession;
	MsgData.Level = applyLevel;
	MsgData.TeammateName = TEXT("");
	MsgData.TeammateID = 0;
	MsgData.IsInvite = false;
	MsgData.TeammateID = 0;
	MsgData.TeammateName = TEXT("");
	MsgData.IsFastTeamApply = true;
	TeamInviteList.Add(MsgData);
}

void URoleTeamInterface::CELL_ReplyTeamApplyFastTeam(int32 agree, int32 applyID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CELL_ReplyTeamApplyFastTeam : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(agree);
	args.Add(applyID);
	GetEntity()->CellCall(TEXT("CELL_replyTeamApplyFastTeam"), args);
}

void URoleTeamInterface::CELL_ApplyJoinFastTeam(FString playerName)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CELL_ApplyJoinFastTeam : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(playerName);
	GetEntity()->CellCall(TEXT("CELL_applyJoinFastTeam"), args);
}

void URoleTeamInterface::CELL_CallMemberEnterSpaceCopy(int32 targetID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CELL_CallMemberEnterSpaceCopy : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(targetID);
	GetEntity()->CellCall(TEXT("CELL_callMemberEnterSpaceCopy"), args);
}

void URoleTeamInterface::FastTeamRequestGotoBunchSpace()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CELL_CallMemberEnterSpaceCopy : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(BunchSpaceScriptID);
	args.Add(NPCScriptID);
	args.Add(NPCID);
	args.Add(TalkKey);
	GetEntity()->CellCall(TEXT("fastTeamRequestGotoBunchSpace"), args);
}

void URoleTeamInterface::CLIENT_OnSetTeamSearchTime_Implementation(const int32 & calcMatchTime)
{
}

void URoleTeamInterface::CELL_teamAssembled(const FString& spaceScriptID, FVector position)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::CELL_teamAssembled : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(spaceScriptID);
	args.Add(position);
	GetEntity()->CellCall(TEXT("CELL_teamAssembled"), args);
}

void URoleTeamInterface::CLIENT_OpenFastTeamWin_Implementation(const FString& bunchSpaceScriptID,const int32 & reqLevel, const int32& isMatchFastTeam, const FString& ScriptID, const int32& ID, const FString& Key)
{
	SpaceCopyLevel = reqLevel;
	BunchSpaceScriptID = bunchSpaceScriptID;
	NPCScriptID = ScriptID;
	NPCID = ID;
	TalkKey = Key;
	SetFastTeamSettingDefaultData();
}

void URoleTeamInterface::RequestFastTeam()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::RequestFastTeam : GetEntity()!"));
		return;
	}
	FFastTeamSetData teamSetData = GetFastTeamSettingData();
	KBEngine::FVariantArray args;
	args.Add(teamSetData.Camp);
	args.Add(teamSetData.Profession);
	args.Add(teamSetData.MinLevel);
	args.Add(teamSetData.MaxLevel);
	args.Add(teamSetData.ChatType);
	args.Add(BunchSpaceScriptID);
	args.Add(NPCScriptID);
	args.Add(NPCID);
	args.Add(TalkKey);
	GetEntity()->CellCall(TEXT("requestFastTeam"), args);
}

void URoleTeamInterface::RequestCancelFastTeamMatch()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::RequestCancelFastTeamMatch : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->BaseCall(TEXT("requestCancelFastTeamMatch"), args);
}

void URoleTeamInterface::SetFastTeamSettingData(FFastTeamSetData SettingData)
{
	FastTeamSetData = SettingData;
}

void URoleTeamInterface::SetFastTeamSettingDefaultData()
{
	FastTeamSetData.Camp = -1;
	FastTeamSetData.Profession = -1;
	FastTeamSetData.MinLevel = SpaceCopyLevel;
	FastTeamSetData.MaxLevel = 100;
	FastTeamSetData.ChatType = 2;
}

FFastTeamSetData URoleTeamInterface::GetFastTeamSettingData()
{
	return FastTeamSetData;
}

void URoleTeamInterface::BASE_setFastTeamData()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeamInterface::BASE_setFastTeamData : GetEntity()!"));
		return;
	}
	FFastTeamSetData teamSetData = GetFastTeamSettingData();
	KBEngine::FVariantArray args;
	args.Add(teamSetData.Camp);
	args.Add(teamSetData.Profession);
	args.Add(teamSetData.MinLevel);
	args.Add(teamSetData.MaxLevel);
	args.Add(teamSetData.ChatType);
	GetEntity()->BaseCall(TEXT("BASE_setFastTeamData"), args);
}

void URoleTeamInterface::CLIENT_onTeamAssembled_Implementation(const FString& spaceScriptID, FVector position)
{
	AssembledSpaceScriptID = spaceScriptID;
	AssembledPosition = position;
}
FTeamMemberData URoleTeamInterface::GetMemberData(const int32 & targetID)
{
	for (auto member : Members)
	{
		if (member.EntityID == targetID)
		{
			return member;
		}
	}
	FTeamMemberData tempTeamMember;
	return tempTeamMember;
}
void URoleTeamInterface::InitBlueCB()
{
	ArrBlueFunc.Add("addTeamMember");
	ArrBlueFunc.Add("TeamInviteByTeammate");
	ArrBlueFunc.Add("OnTeamInviteBy");
	ArrBlueFunc.Add("teamInfoNotifyOnJoin");
	ArrBlueFunc.Add("leaveTeamNotify");
	ArrBlueFunc.Add("disbandTeamNotify");
	ArrBlueFunc.Add("changeCaptainNotify");
	ArrBlueFunc.Add("changeTeamSignerNotify");
	ArrBlueFunc.Add("logoutNotify");
	ArrBlueFunc.Add("onRejoinTeam");
	ArrBlueFunc.Add("teammateInfoNotify");
	ArrBlueFunc.Add("OnReceiveJoinTeamRequest");
	ArrBlueFunc.Add("onSendTeamMSG");
	ArrBlueFunc.Add("modifyAllocation");
	ArrBlueFunc.Add("modifyQuality");
	ArrBlueFunc.Add("OnTeamMemberAddBuff");
	ArrBlueFunc.Add("OnTeamMemberRemoveBuff");
	ArrBlueFunc.Add("OnTeamMemberResetBuffTime");
	ArrBlueFunc.Add("AddTeamSignCB");
	ArrBlueFunc.Add("StartTeamFollow");
	ArrBlueFunc.Add("StopTeamFollow");
	ArrBlueFunc.Add("FollowNewCaptain");
	ArrBlueFunc.Add("StartNormalFollow");
	ArrBlueFunc.Add("StopNormalFollow");
	ArrBlueFunc.Add("RoleTeamSpellBoxFollow");
	ArrBlueFunc.Add("onMemberShareBigMapCustomMarker");
	ArrBlueFunc.Add("RemoveTeamSigner");
	ArrBlueFunc.Add("CLIENT_OnStartTeamSearch");
	ArrBlueFunc.Add("CLIENT_OnFastTeamCancelMatch");
	ArrBlueFunc.Add("CLIENT_teamByApply");
	ArrBlueFunc.Add("CLIENT_onTeamAssembled");
	ArrBlueFunc.Add("CLIENT_OpenFastTeamWin");
	ArrBlueFunc.Add("CLIENT_OnSetTeamSearchTime");
	ArrBlueFunc.Add("FastTeamOnMatchSuccess");
	Supper::InitBlueCB();
}

void URoleTeamInterface::DeleteTeamInvite(int32 PlayerEntityID)
{
	for (FTeamMsgData Data : TeamInviteList)
	{
		if (Data.ID == PlayerEntityID)
		{
			TeamInviteList.Remove(Data);
			return;
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END
