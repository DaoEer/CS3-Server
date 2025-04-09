// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleRelationInterface.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Manager/MessageManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CS3Debug.h"
#include "GameData/ConstData.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleRelationInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(relation_initRelationCatalog, &URoleRelationInterface::relation_initRelationCatalog,  const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleRelationInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleRelationInterface::URoleRelationInterface()
{
	const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	if (GameInstance &&
		GameInstance->LocalDataSaveManager &&
		GameInstance->LocalDataSaveManager->LocalUserSettingData
		)
	{
		SetRelationNotice(GameInstance->LocalDataSaveManager->LocalUserSettingData->GetIsShowOnlineRemind());
	}
}

void URoleRelationInterface::relation_sendRelationData_Implementation(const FString& RelationUID, const FString& Name, const FString& AliasName, const FString& DBID, const int32& PlayerID, const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace)
{
	FRelationData rData;
	rData.relationUID = RelationUID;
	rData.playName = Name;
	rData.aliasName = AliasName;
	rData.playerDBID = DBID;
	rData.playerID = PlayerID;
	rData.profession = Profession;
	rData.Camp = Camp;
	rData.level = Level;
	rData.relationShip = RelationShip;
	rData.tongName = TongName;
	rData.localSpace = LocalSpace;
	RelationDict.Add(rData.relationUID, rData);
}

void URoleRelationInterface::relation_onNoticePlayerLogin_Implementation(const FString& RelationUID, const int32& PlayerID)
{
	if (RelationDict.Contains(RelationUID))
	{
		RelationDict[RelationUID].playerID = PlayerID;
		if (IsNoticeFriend)
		{
			if (HasRelationShip(RelationDict[RelationUID].relationShip, RELATION_SHIP::ROLE_RELATION_FRIEND))
			{
				if (UUECS3GameInstance::Instance)
				{
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(1144, RelationDict[RelationUID].playName);
				}
			}
			else if (HasRelationShip(RelationDict[RelationUID].relationShip, RELATION_SHIP::ROLE_RELATION_FOE))
			{
				if (UUECS3GameInstance::Instance)
				{
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(1145, RelationDict[RelationUID].playName);
				}
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("Can not find relationUID(%s)"), *RelationUID);
	}
}

void URoleRelationInterface::relation_onNoticePlayerLogout_Implementation(const FString& RelationUID, const int32& level, const FString& locaSpace)
{
	if (RelationDict.Contains(RelationUID))
	{
		RelationDict[RelationUID].playerID = 0;
		RelationDict[RelationUID].level = level;
		RelationDict[RelationUID].localSpace = locaSpace;
	}
	else
	{
		CS3_Warning(TEXT("Can not find relationUID(%s)"), *RelationUID);
	}
}

void URoleRelationInterface::OnInitRelationDataCompleted_Implementation()
{

}

FRelationData URoleRelationInterface::GetRelationDataByUID(const FString& UID, int32& Index)
{
	if (RelationDict.Contains(UID))
	{
		Index = 1;
		return RelationDict[UID];
	}
	else
	{
		CS3_Warning(TEXT("Can not find relationUID(%s)"), *UID);
		FRelationData F;
		Index = -1;
		return F;
	}
}

FRelationData URoleRelationInterface::GetRelationDataByPlayerDBID(const FString& PlayerDBID, int32& Index)
{
	for (auto It = RelationDict.CreateConstIterator(); It; ++It)
	{
		if (It.Value().playerDBID == PlayerDBID)
		{
			Index = 1;
			return It.Value();
		}
		 
	}
	Index = -1;
	FRelationData F;
	return F;
}

FRelationData URoleRelationInterface::GetRelationDataByPlayerName(const FString& PlayerName, int32& Index)
{
	for (auto It = RelationDict.CreateConstIterator(); It; ++It)
	{
		if (It.Value().playName == PlayerName)
		{
			Index = 1;
			return It.Value();
		}

	}
	Index = -1;
	FRelationData F;
	return F;
}

FRelationCatalogData URoleRelationInterface::GetRelationCatalogByindex(int32 CataIndex, int32& Index)
{
	for (auto It : RelationCatelogs)
	{
		if (It.relationIndex == CataIndex)
		{
			Index = 1;
			return It;
		}
	}
	Index = -1;
	FRelationCatalogData F;
	return F;
}

void URoleRelationInterface::GetRelationCatalogNum(int32 CataIndex, int32& OnlineNum, int32& TotalNum)
{
	OnlineNum = 0;
	TotalNum = 0;
	for (auto It = RelationCatelogs.CreateConstIterator(); It; ++It)
	{
		if (It->relationIndex == CataIndex)
		{
			TotalNum = It->relationUIDs.Num();
			for (auto uid : It->relationUIDs)
			{
				if (RelationDict.Contains(uid) && RelationDict[uid].playerID != 0)
				{
					OnlineNum += 1;
				}
			}
		}
	}
}

TArray<FRelationCatalogData> URoleRelationInterface::SearchRelationByName(int32 CataIndex, const FString& SearchStr)
{
	TArray<FRelationCatalogData> Catalogs;
	for (auto Rc : RelationCatelogs)
	{
		/// 好友分组，则加上自定义分组
		if (CataIndex == RELATION_CATALOG_TYPE_FRIEND_LIST && Rc.relationIndex < RELATION_CATALOG_TYPE_FRIEND_LIST)
		{
			continue;
		}
		if (CataIndex != RELATION_CATALOG_TYPE_FRIEND_LIST && CataIndex != Rc.relationIndex)
		{
			continue;
		}
		FRelationCatalogData RCD;
		RCD.relationIndex = Rc.relationIndex;
		RCD.relationName = Rc.relationName;
		for (auto uid : Rc.relationUIDs)
		{
			if (RelationDict.Contains(uid))
			{
				if (RelationDict[uid].aliasName.Contains(SearchStr) || RelationDict[uid].playName.Contains(SearchStr) || INT_TO_FSTRING(RelationDict[uid].level).Contains(SearchStr))
				{
					RCD.relationUIDs.Add(uid);
				}
			}
		}
		Catalogs.Add(RCD);
	}
	return Catalogs; 
}

bool URoleRelationInterface::GetRelationIndexByRelationName(const FString& RelationName, int32& CataIndex)
{
	for (auto It = RelationCatelogs.CreateConstIterator(); It; ++It)
	{
		if (It->relationName == RelationName)
		{
			CataIndex = It->relationIndex;
			return true;
		}
	}
	CataIndex = -3;
	return false;
}

TArray<int32> URoleRelationInterface::GetAllRelationCatalogIndex(TArray<FString>& RelationNameList)
{
	TArray<int32> indexList;
	RelationCatelogs.Sort([](const FRelationCatalogData& A, const FRelationCatalogData& B) { return A.relationIndex < B.relationIndex; });
	for (auto It = RelationCatelogs.CreateConstIterator(); It ; ++It)
	{
		if (It->relationIndex >= 0)
		{
			indexList.Add(It->relationIndex);
			RelationNameList.Add(It->relationName);
		}

	}
	return indexList;
	
}

bool URoleRelationInterface::HasRelationShip(int32 RelationShip, RELATION_SHIP Digit)
{
	uint16 RelationMask = uint16(1) << uint16(Digit);
	if (RelationShip & RelationMask)
	{
		return true;
	}
	return false;
}

bool URoleRelationInterface::HasRelationShipByEntityID(int32 inEntityID, RELATION_SHIP Digit)
{
	for (auto It = RelationDict.CreateConstIterator(); It ; ++It)
	{
		if (It.Value().playerID == inEntityID)
		{
			uint16 RelationMask = uint16(1) << uint16(Digit);
			if (It.Value().relationShip & RelationMask)
			{
				return true;
			}
		}
	}
	return false;
}

bool URoleRelationInterface::HasRelationShipByName(const FString& PlayerName, RELATION_SHIP Digit)
{
	for (auto It = RelationDict.CreateConstIterator(); It; ++It)
	{
		if (PlayerName.Equals(It.Value().playName))
		{
			uint16 RelationMask = uint16(1) << uint16(Digit);
			if (It.Value().relationShip & RelationMask)
			{
				return true;
			}
		}
	}
	return false;
}

void URoleRelationInterface::RequestPlayerInfo(const FString& Name)
{
	if (Name.IsEmpty())return;
	KBEngine::FVariantArray args;
	args.Add(Name);
	BaseCall(TEXT("requestPlayerInfo"), args);
}

void URoleRelationInterface::relation_requestPlayerInfo_Implementation(const FString& Name, const int32& Level, const int32& Camp, const int32& Profession)
{

}

void URoleRelationInterface::AddFriend(const FString& Name)
{
	if (Name.IsEmpty())return;
	if (Name.Equals(UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityID, TEXT("playerName"))))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1102);
		return;
	}

	if (HasRelationShipByName(Name, RELATION_SHIP::ROLE_RELATION_FOE))
	{
		TWeakObjectPtr<URoleRelationInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1152, Name, FBtnClick::CreateLambda([DelayThisPtr,Name](RT_BTN_TYPE RType)
		{
			if (DelayThisPtr.IsValid() && RType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				args.Add(Name);
				DelayThisPtr->BaseCall(TEXT("addFriend"), args);
			}
		}));
		return;
	}

	if (HasRelationShipByName(Name, RELATION_SHIP::ROLE_RELATION_BLACKLIST))
	{
		TWeakObjectPtr<URoleRelationInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1153, Name, FBtnClick::CreateLambda([DelayThisPtr, Name](RT_BTN_TYPE RType)
		{
			if (DelayThisPtr.IsValid() && RType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				args.Add(Name);
				DelayThisPtr->BaseCall(TEXT("addFriend"), args);
			}
		}));
		return;
	}
	
	KBEngine::FVariantArray args;
	args.Add(Name);
	BaseCall(TEXT("addFriend"), args);
	
	
}

void URoleRelationInterface::relation_addFriendRelation_Implementation(const FString& RelationUID, const int32& PlayerID, const FString& Name, const FString& DBID, const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace)
{
	UGolbalBPFunctionLibrary::StatusMessage(1128, TEXT(""));
	AddRelation_(RelationUID, Name, DBID, PlayerID, RelationShip, Profession, Level, Camp, TongName, LocalSpace);
	relation_addCatelogsMember(RELATION_CATALOG_TYPE_FRIEND_LIST, RelationUID);				// 添加默认好友分组
}

void URoleRelationInterface::RemoveFriend(const FString& RelationUID)
{
	KBEngine::FVariantArray args;
	args.Add(RelationUID);
	BaseCall(TEXT("removeFriend"), args);
}

void URoleRelationInterface::relation_removeFriend_Implementation(const FString& RelationUID)
{
	RemoveRelation_(RelationUID, RELATION_SHIP::ROLE_RELATION_FRIEND);
	for (auto catelog : RelationCatelogs)
	{
		if (catelog.relationUIDs.Contains(RelationUID))
		{
			if (catelog.relationIndex != RELATION_CATALOG_TYPE_FOE_LIST && catelog.relationIndex != RELATION_CATALOG_TYPE_BLEACK_LIST &&
				catelog.relationIndex != RELATION_CATALOG_TYPE_LASTTIME_LIST )
			{
				relation_removeCatelogsMember(catelog.relationIndex, RelationUID);
				break;
			}
			
		}
	}
	
}

void URoleRelationInterface::ReceiveInviteToFriend_Implementation(const int32& InviterID, const FString& InviterName)
{
	RelationFriendInviteList.Add(InviterName);
}

void URoleRelationInterface::ReplyInvitedToFriend(bool IsAccept, FString InviterName)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleRelationInterface::ReplyInvitedToFriend : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(uint8(IsAccept));
	args.Add(InviterName);
	this->GetEntity()->BaseCall(TEXT("replyInvitedToFriend"), args);
}

void URoleRelationInterface::DeleteFriendInvite(const FString& Name)
{
	RelationFriendInviteList.Remove(Name);
}

void URoleRelationInterface::relation_addRecentContacts_Implementation(const FString& RelationUID)
{
	if (RelationDict.Contains(RelationUID))
	{
		RelationDict[RelationUID].relationShip |= (uint16(1) << uint16(RELATION_SHIP::ROLE_RELATION_LAST_CHAT));
		relation_addCatelogsMember(RELATION_CATALOG_TYPE_LASTTIME_LIST, RelationUID);
	}
	else
	{
		CS3_Warning(TEXT("Can not find relationUID(%s)"), *RelationUID);
	}
}

void URoleRelationInterface::relation_addRecentContactsDatas_Implementation(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace)
{
	AddRelation_(RelationUID, Name, DBID, PlayerID, RelationShip, Profession, Level, Camp, TongName, LocalSpace);

	relation_addCatelogsMember(RELATION_CATALOG_TYPE_LASTTIME_LIST, RelationUID);
}

void URoleRelationInterface::RemoveRecentContacts(const FString& RelationUID)
{
	KBEngine::FVariantArray args;
	args.Add(RelationUID);
	BaseCall(TEXT("removeRecentContacts"), args);
}

void URoleRelationInterface::RemoveAllRecentContacts()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("removeAllRecentContacts"), args);
}

void URoleRelationInterface::relation_removeRecentContacts_Implementation(const FString& RelationUID)
{
	RemoveRelation_(RelationUID, RELATION_SHIP::ROLE_RELATION_LAST_CHAT);
	relation_removeCatelogsMember(RELATION_CATALOG_TYPE_LASTTIME_LIST, RelationUID);
}

void URoleRelationInterface::relation_initRelationCatalog(const FVariant& data)
{
	RelationCatelogs.Empty();
	RELATION_CATALOG_DATA CataLogData = RELATION_CATALOG_DATA(data);
	for (auto d : CataLogData.RelationCatalogDatas)
	{
		FRelationCatalogData RC;
		RC.relationIndex = d.relationIndex;
		RC.relationName = d.catalogName;
		for (auto uid : d.catalogList)
		{
			char uidTemp[21];
			sprintf_s(uidTemp, "%llu", uid);
			RC.relationUIDs.Add(uidTemp);
		}
		RelationCatelogs.Add(RC);
	}
}

void URoleRelationInterface::AddRelationCatalog(const FString & CatalogName)
{
	KBEngine::FVariantArray args;
	args.Add(CatalogName);
	BaseCall(TEXT("addRelationCatalog"), args);
}

void URoleRelationInterface::relation_addRelationCatalog_Implementation(const int32& index, const FString& CatalogName)
{
	FRelationCatalogData Rc;
	Rc.relationIndex = index;
	Rc.relationName = CatalogName;
	RelationCatelogs.Add(Rc);
}

void URoleRelationInterface::DelRelationCatalog(const int32& index)
{
	if (index > 1)
	{
		KBEngine::FVariantArray args;
		args.Add(index);
		BaseCall(TEXT("delRelationCatalog"), args);
	}
}

void URoleRelationInterface::relation_delRelationCatalog_Implementation(const int32& index)
{
	for (auto it : RelationCatelogs)
	{
		if (it.relationIndex == index)
		{
			RelationCatelogs.Remove(it);
			return;
		}
	}

}

void URoleRelationInterface::relation_addCatelogsMember_Implementation(const int32& index, const FString& relationUID)
{
	for (auto& RC : RelationCatelogs)
	{
		if (RC.relationIndex == index)
		{
			RC.relationUIDs.AddUnique(relationUID);
			return;
		}
	}
	CS3_Warning(TEXT("Add catelog(relationUID:%s) err! Cannot find index(%d)!!"), *relationUID, index);
}

void URoleRelationInterface::relation_removeCatelogsMember_Implementation(const int32& index, const FString& relationUID)
{
	for (auto& RC : RelationCatelogs)
	{
		if (RC.relationIndex == index)
		{
			if (RC.relationUIDs.Contains(relationUID))
			{
				RC.relationUIDs.Remove(relationUID);
				return;
			}
			else
			{
				CS3_Warning(TEXT("Remove Catelog err!cannot find relationUID(%s)"), *relationUID);
			}
			return;
		}
	}
	CS3_Warning(TEXT("Remove catelog(relationUID:%s) err! Cannot find index(%d)!!"), *relationUID, index);
}

void URoleRelationInterface::RenameRelationCatalog(const int32& index, const FString& CatalogName)
{
	KBEngine::FVariantArray args;
	args.Add(index);
	args.Add(CatalogName);
	BaseCall(TEXT("renameRelationCatalog"), args);

	relation_renameRelationCatalog(index, CatalogName);
}

void URoleRelationInterface::relation_renameRelationCatalog_Implementation(const int32& index, const FString& CatalogName)
{
	for (auto& it : RelationCatelogs)
	{
		if (it.relationIndex == index)
		{
			it.relationName = CatalogName;
			return;
		}
	}
}

void URoleRelationInterface::MoveToOtherCatalog(const int32& OldIndex, const int32& NewIndex, const FString& RelationUID)
{
	KBEngine::FVariantArray args;
	args.Add(OldIndex);
	args.Add(NewIndex);
	args.Add(RelationUID);
	BaseCall(TEXT("moveRelationItemToCatalog"), args);

	//relation_moveToOtherCatalog(OldIndex, NewIndex, RelationUID);
}

void URoleRelationInterface::relation_moveToOtherCatalog_Implementation(const int32& OldIndex, const int32& NewIndex, const FString& RelationUID)
{
	relation_removeCatelogsMember(OldIndex, RelationUID);
	relation_addCatelogsMember(NewIndex, RelationUID);
}

void URoleRelationInterface::SetAliasName(const FString& RelationUID, const FString& AliasName)
{
	if (RelationDict.Contains(RelationUID))
	{
		int32 relationShip = RelationDict[RelationUID].relationShip;
		if (HasRelationShip(relationShip,RELATION_SHIP::ROLE_RELATION_FRIEND) || HasRelationShip(relationShip,RELATION_SHIP::ROLE_RELATION_BLACKLIST))
		{
			KBEngine::FVariantArray args;
			args.Add(RelationUID);
			args.Add(AliasName);
			BaseCall(TEXT("setRelationRemarkName"), args);

			RelationDict[RelationUID].aliasName = AliasName;
			relation_setAliasName(RelationUID, AliasName);
		}
	}
	
}

void URoleRelationInterface::relation_setAliasName_Implementation(const FString& RelationUID, const FString& AliasName)
{
	if (RelationDict.Contains(RelationUID))
	{
		RelationDict[RelationUID].aliasName = AliasName;
	}
}

void URoleRelationInterface::SetRelationNotice(bool IsNotice)
{
	IsNoticeFriend = IsNotice;
}

void URoleRelationInterface::OnSetRelationNotice_Implementation(const int32& IsNotice)
{
	if (IsNotice == 0)
	{
		IsNoticeFriend = false;
	}
	else
	{
		IsNoticeFriend = true;
	}
	
}

void URoleRelationInterface::AddBlacklist(const FString& Name)
{
	KBEngine::FVariantArray args;
	args.Add(Name);
	BaseCall(TEXT("addBlacklist"), args);
}

void URoleRelationInterface::relation_addBlacklistRelation_Implementation(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace)
{
	AddRelation_(RelationUID, Name, DBID, PlayerID, RelationShip, Profession, Level, Camp, TongName, LocalSpace);
	relation_addCatelogsMember(RELATION_CATALOG_TYPE_BLEACK_LIST, RelationUID);
}

void URoleRelationInterface::RemoveBlacklist(const FString& RelationUID)
{
	KBEngine::FVariantArray args;
	args.Add(RelationUID);
	BaseCall(TEXT("removeBlacklist"), args);
}

void URoleRelationInterface::relation_removeBlackList_Implementation(const FString& RelationUID)
{
	RemoveRelation_(RelationUID, RELATION_SHIP::ROLE_RELATION_BLACKLIST);
	relation_removeCatelogsMember(RELATION_CATALOG_TYPE_BLEACK_LIST, RelationUID);
}

void URoleRelationInterface::AddFoe(const FString& Name)
{
	KBEngine::FVariantArray args;
	args.Add(Name);
	BaseCall(TEXT("addFoe"), args);
}

void URoleRelationInterface::relation_addFoeRelation_Implementation(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace)
{
	AddRelation_(RelationUID, Name, DBID, PlayerID, RelationShip, Profession, Level, Camp, TongName, LocalSpace);
	relation_addCatelogsMember(RELATION_CATALOG_TYPE_FOE_LIST, RelationUID);
}

void URoleRelationInterface::RemoveFoe(const FString& RelationUID)
{
	KBEngine::FVariantArray args;
	args.Add(RelationUID);
	BaseCall(TEXT("removeFoe"), args);
}

void URoleRelationInterface::relation_removeFoe_Implementation(const FString& RelationUID)
{
	RemoveRelation_(RelationUID, RELATION_SHIP::ROLE_RELATION_FOE);
	relation_removeCatelogsMember(RELATION_CATALOG_TYPE_FOE_LIST, RelationUID);
}

FRelationGroupData URoleRelationInterface::GetRelationGroupByUID(const int32& GroupIndex, int32& Index)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		Index = 1;
		return RelationGroupDict[GroupIndex];
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
	Index = -1;
	FRelationGroupData F;
	return F;
}

FRelationGroupMember URoleRelationInterface::GetRelationGroupMemberByUIDAndName(const int32& GroupUID, const FString& PlayerName, int32& Index)
{
	if (RelationGroupDict.Contains(GroupUID))
	{
		for (auto member : RelationGroupDict[GroupUID].groupMembers)
		{
			if (member.playerName == PlayerName)
			{
				Index = 1;
				return member;
			}
		}
		CS3_Warning(TEXT("Cannot find Group(%d) member(%s)!!"), GroupUID,*PlayerName);
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupUID);
	}
	Index = -1;
	FRelationGroupMember F;
	return F;
}

void URoleRelationInterface::CreateGroup(const FString GroupName, const bool IsAllowJoin, const FString& PassWord)
{
	KBEngine::FVariantArray args;
	args.Add(GroupName);
	args.Add((int32)IsAllowJoin);
	args.Add(PassWord);
	BaseCall(TEXT("createGroup"), args);
}

void URoleRelationInterface::DeleteGroup(const int32& GroupIndex)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	BaseCall(TEXT("deleteGroup"), args);
}

void URoleRelationInterface::InvitedToGroup(const int32& GroupIndex, const FString& PlayerName)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add(PlayerName);
	BaseCall(TEXT("invitedToGroup"), args);
}

void URoleRelationInterface::relation_receiverGroup_Implementation(const int32& GroupIndex, const FString& GroupName, const FString& EndTime, const FString& CreaterName, const FString& PassWord, const int32& IsAllowJoin, const TArray<FString>& BlackList)
{
	FRelationGroupData Group;
	Group.groupUID = GroupIndex;
	Group.leaterName = CreaterName;
	Group.groupName = GroupName;
	Group.endTime = EndTime;
	Group.canJoin = false;
	if (IsAllowJoin > 0)
	{
		Group.canJoin = true;
	}
	Group.passWord = PassWord;
	Group.blackList = BlackList;
	RelationGroupDict.Add(GroupIndex, Group);
}

void URoleRelationInterface::relation_receiverGroupInfo_Implementation(const int32& GroupIndex, const FString& PlayerName, const int32& Profession, const int32& level, const int32& Camp, const int32& IsOnline)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		FRelationGroupMember member;
		member.playerName = PlayerName;
		member.profession = Profession;
		member.level = level;
		member.camp = Camp;
		member.isOnline = false;
		if (IsOnline > 0)
		{
			member.isOnline = true;
		}

		RelationGroupDict[GroupIndex].groupMembers.Add(member);
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::RequestEnterGroupByPassword(const int32& GroupIndex, const FString& PassWord)
{

}

void URoleRelationInterface::ActiveLeaveGroup(const int32& GroupIndex)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	BaseCall(TEXT("activeLeaveGroup"), args);
}

void URoleRelationInterface::PassiveLeaveGroup(const int32& GroupIndex, const FString& PlayerName)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add(PlayerName);
	BaseCall(TEXT("passiveLeaveGroup"), args);
}

void URoleRelationInterface::relation_onPlayerRemoveGroup_Implementation(const int32& GroupIndex, const FString& PlayerName)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		for (auto member : RelationGroupDict[GroupIndex].groupMembers)
		{
			if (member.playerName == PlayerName)
			{
				RelationGroupDict[GroupIndex].groupMembers.Remove(member);
				return;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::relation_onDelectGroup_Implementation(const int32& GroupIndex)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		RelationGroupDict.Remove(GroupIndex);
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::ChangeGroupLeater(const int32& GroupIndex, const FString & PlayerName)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add(PlayerName);
	BaseCall(TEXT("changeGroupLeater"), args);
}

void URoleRelationInterface::relation_changeGroupLeater_Implementation(const int32& GroupIndex, const FString& PlayerName)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		RelationGroupDict[GroupIndex].leaterName = PlayerName;
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::AddEndTime(const int32& GroupIndex, const GROUP_END_TYPE & EndTime)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add((int32)EndTime);
	BaseCall(TEXT("addEndTime"), args);
}

void URoleRelationInterface::relation_addEndTime_Implementation(const int32& GroupIndex, const FString& EndTime)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		RelationGroupDict[GroupIndex].endTime = EndTime;
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::AddGroupBlackList(const int32& GroupIndex, const FString& PlayerName)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add(PlayerName);
	BaseCall(TEXT("addGroupBlackList"), args);
}

void URoleRelationInterface::relation_addGroupBlackList_Implementation(const int32& GroupIndex, const FString& PlayerName)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		RelationGroupDict[GroupIndex].blackList.AddUnique(PlayerName);
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::DelGroupBlackList(const int32& GroupIndex, const FString& PlayerName)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add(PlayerName);
	BaseCall(TEXT("delGroupBlackList"), args);
}

void URoleRelationInterface::relation_delGroupBlackList_Implementation(const int32& GroupIndex, const FString& PlayerName)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		if (RelationGroupDict[GroupIndex].blackList.Contains(PlayerName))
		{
			RelationGroupDict[GroupIndex].blackList.Remove(PlayerName);
		}
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::updateGroupInfo(const int32& GroupIndex, const FString& GroupName, const bool IsAllowJoin, const FString& PassWord)
{
	KBEngine::FVariantArray args;
	args.Add(GroupIndex);
	args.Add(GroupName);
	args.Add((int32)IsAllowJoin);
	args.Add(PassWord);
	BaseCall(TEXT("updateGroupInfo"), args);
}

void URoleRelationInterface::relation_updateGroupInfo_Implementation(const int32& GroupIndex, const FString& GroupName, const int32& IsAllowJoin, const FString& PassWord)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		RelationGroupDict[GroupIndex].groupName = GroupName;
		RelationGroupDict[GroupIndex].canJoin = true;
		if (IsAllowJoin == 0)
		{
			RelationGroupDict[GroupIndex].canJoin = false;

		}
		RelationGroupDict[GroupIndex].passWord = PassWord;
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::relation_onNoticePlayerOnLine_Implementation(const int32& GroupIndex, const FString& PlayerName, const int32& level)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		for (auto member : RelationGroupDict[GroupIndex].groupMembers)
		{
			if (member.playerName == PlayerName)
			{
				member.isOnline = true;
				member.level = level;
				return;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::relation_onPlayerOffLine_Implementation(const int32& GroupIndex, const FString& PlayerName)
{
	if (RelationGroupDict.Contains(GroupIndex))
	{
		for (auto member : RelationGroupDict[GroupIndex].groupMembers)
		{
			if (member.playerName == PlayerName)
			{
				member.isOnline = false;
				return;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("Cannot find Group(%d)!!"), GroupIndex);
	}
}

void URoleRelationInterface::relation_recommendGroup_Implementation(FString& JsonStr)
{
	auto JsonDatas = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObjectArray(this, TEXT("ROOT"));
	for (auto JsonData : JsonDatas)
	{
		FRelationGroupSimple Group;
		Group.groupUID = FSTRING_TO_INT(JsonData->GetString(TEXT("uid")));
		Group.groupName = JsonData->GetString(TEXT("groupName"));
		Group.groupNum = FSTRING_TO_INT(JsonData->GetString(TEXT("nums")));

		RelationRecommendGroup.Add(Group);
	}

}

void URoleRelationInterface::InitBlueCB()
{
	ArrBlueFunc.Add("relation_initRelationCatalog");
	ArrBlueFunc.Add("relation_addRelationCatalog");
	ArrBlueFunc.Add("relation_delRelationCatalog");
	ArrBlueFunc.Add("relation_sendRelationData");
	ArrBlueFunc.Add("OnInitRelationDataCompleted");
	ArrBlueFunc.Add("relation_onNoticePlayerLogin");
	ArrBlueFunc.Add("relation_onNoticePlayerLogout");
	ArrBlueFunc.Add("relation_requestPlayerInfo");
	ArrBlueFunc.Add("relation_addFriendRelation");
	ArrBlueFunc.Add("relation_removeFriend");
	ArrBlueFunc.Add("relation_addFoeRelation");
	ArrBlueFunc.Add("relation_removeFoe");
	ArrBlueFunc.Add("relation_addBlacklistRelation");
	ArrBlueFunc.Add("relation_removeBlackList");
	ArrBlueFunc.Add("relation_addRecentContacts");
	ArrBlueFunc.Add("relation_addRecentContactsDatas");
	ArrBlueFunc.Add("relation_removeRecentContacts");
	ArrBlueFunc.Add("relation_receiverGroup");
	ArrBlueFunc.Add("relation_receiverGroupInfo");
	ArrBlueFunc.Add("relation_onNoticePlayerOnLine");
	ArrBlueFunc.Add("relation_onPlayerOffLine");
	ArrBlueFunc.Add("relation_onPlayerRemoveGroup");
	ArrBlueFunc.Add("relation_onDelectGroup");
	ArrBlueFunc.Add("relation_changeGroupLeater");
	ArrBlueFunc.Add("relation_addEndTime");
	ArrBlueFunc.Add("relation_addGroupBlackList");
	ArrBlueFunc.Add("relation_delGroupBlackList");
	ArrBlueFunc.Add("relation_recommendGroup");
	ArrBlueFunc.Add("OpenGroupPassWordWidget");
	ArrBlueFunc.Add("OnSetRelationNotice");
	ArrBlueFunc.Add("ReceiveInviteToFriend");
	ArrBlueFunc.Add("relation_moveToOtherCatalog");
	Supper::InitBlueCB();
}

void URoleRelationInterface::AddRelation_(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace)
{
	FRelationData rData;
	rData.relationUID = RelationUID;
	rData.playName = Name;
	rData.playerDBID = DBID;
	rData.playerID = PlayerID;
	rData.profession = Profession;
	rData.Camp = Camp;
	rData.level = Level;
	rData.relationShip = RelationShip;
	rData.tongName = TongName;
	rData.localSpace = LocalSpace;

	RelationDict.Add(RelationUID, rData);
}

void URoleRelationInterface::RemoveRelation_(const FString& RelationUID, RELATION_SHIP relation)
{
	if (RelationDict.Contains(RelationUID))
	{
		RelationDict[RelationUID].relationShip &= ~(uint16(1) << uint16(relation));
		if (RelationDict[RelationUID].relationShip == 0)
		{
			RelationDict.Remove(RelationUID);
		}
	}
	else
	{
		CS3_Warning(TEXT("Can not find relationUID(%s)"), *RelationUID);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
