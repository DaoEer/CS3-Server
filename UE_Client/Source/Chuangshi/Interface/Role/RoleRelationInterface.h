// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/RelationData.h"
#include "GameData/RelationGroupData.h"
#include "GameData/RelationGroupMember.h"
#include "RoleRelationInterface.generated.h"

/*
* 文件名称：RoleRelationInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

/**
 * 玩家关系接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleRelationInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleRelationInterface();

	static FString GetName() { return TEXT("RoleRelationInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleRelationInterface.BP_RoleRelationInterface_C'"); } //获取蓝图对象路径


	/// 上线同步关系数据
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_sendRelationData(const FString& RelationUID, const FString& Name, const FString& AliasName, const FString& DBID, const int32& PlayerID, 
			const int32& RelationShip, const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace);
	/// 完成上线同步数据
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void OnInitRelationDataCompleted();

	///< 设置玩家上下线提示
	UFUNCTION(BlueprintCallable)
		void SetNoticeLine(bool bNotice) { IsNoticeFriend = bNotice; };

	/// 玩家上下线
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_onNoticePlayerLogin(const FString& RelationUID, const int32& PlayerID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_onNoticePlayerLogout(const FString& RelationUID, const int32& level, const FString& locaSpace);

	/// 通过关系UID获取关系数据，没找到Index返回-1
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		FRelationData GetRelationDataByUID(const FString& UID, int32& Index);
	
	///根据分组索引（仇人-2、黑名单-1、最近联系人0、好友1、自定义分组2-6）获得分组数据，没找到Index返回-1
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		FRelationCatalogData GetRelationCatalogByindex(int32 CataIndex, int32& Index);

	/// 获取各个分组的在线/总人数
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void GetRelationCatalogNum(int32 CataIndex, int32& OnlineNum, int32& TotalNum);

	/// 搜索分组,（CataIndex：好友分页传1，仇人分页传-2，黑名单分页传-1；SearchStr：搜索文本）， { CataIndex : [ relationUID,...] }
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		TArray<FRelationCatalogData> SearchRelationByName(int32 CataIndex, const FString& SearchStr);

	/// 通过玩家DBID获得玩家关系数据，没找到Index返回-1
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		FRelationData GetRelationDataByPlayerDBID(const FString& PlayerDBID, int32& Index);
	/// 通过玩家PlayerName获得玩家关系数据，没找到Index返回-1
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		FRelationData GetRelationDataByPlayerName(const FString& PlayerName, int32& Index);
	/// 通过分组名获取分组索引,没找到返回False
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		bool GetRelationIndexByRelationName(const FString& RelationName, int32& CataIndex);

	///获取所有关系分组索引及名字,索引要排序输出（名字顺序也要和索引对应），排序：最近联系人>好友>自定义分组（按顺序排）
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		TArray<int32> GetAllRelationCatalogIndex(TArray<FString>& RelationNameList);

	/**
	*判断当前RelationShip是否具有某种关系
	*
	*@param RelationShip 需要判断的关系值
	*@param Digit 关系
	*
	*@return bool，RelationShip具有某种关系g返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface")
		bool HasRelationShip(int32 RelationShip, RELATION_SHIP Digit);
	/// 跟某个 entity是否有 某种关系
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface")
		bool HasRelationShipByEntityID(int32 inEntityID, RELATION_SHIP Digit);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface")
		bool HasRelationShipByName(const FString& PlayerName, RELATION_SHIP Digit);

	/// 好友
	// 向服务器请求玩家信息
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RequestPlayerInfo(const FString& Name);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_requestPlayerInfo(const FString& Name, const int32& Level, const int32& Camp, const int32& Profession);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void AddFriend(const FString& Name);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addFriendRelation(const FString& RelationUID, const int32& PlayerID, const FString& Name, const FString& DBID, const int32& RelationShip,
			const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RemoveFriend(const FString& RelationUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_removeFriend(const FString& RelationUID);
	
	///好友申请
	//收到好友申请
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface")
		void ReceiveInviteToFriend(const int32& InviterID, const FString& InviterName);
	//回复好友申请
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface")
		void ReplyInvitedToFriend(bool IsAccept, FString InviterName);
	//删除好友申请数据
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface")
		void DeleteFriendInvite(const FString& Name);

	/// 最近联系人
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addRecentContacts(const FString& RelationUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addRecentContactsDatas(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip,
			const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RemoveRecentContacts(const FString& RelationUID);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RemoveAllRecentContacts();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_removeRecentContacts(const FString& RelationUID);

	/// 分组
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_initRelationCatalog(const FVariant& data);
	/// 增加分组
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void AddRelationCatalog(const FString& CatalogName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addRelationCatalog(const int32& index, const FString& CatalogName);
	/// 删除分组
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void DelRelationCatalog(const int32& index);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_delRelationCatalog(const int32& index);
	/// 添加（删除分组里成员）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addCatelogsMember(const int32& index, const FString& relationUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_removeCatelogsMember(const int32& index, const FString& relationUID);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RenameRelationCatalog(const int32& index, const FString& CatalogName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_renameRelationCatalog(const int32& index, const FString& CatalogName);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void MoveToOtherCatalog(const int32& OldIndex, const int32& NewIndex, const FString& RelationUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_moveToOtherCatalog(const int32& OldIndex, const int32& NewIndex, const FString& RelationUID);

	/// 设置备注名
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void SetAliasName(const FString& RelationUID, const FString& AliasName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_setAliasName(const FString& RelationUID, const FString& AliasName);

	/// 朋友上线是否通知
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void SetRelationNotice(bool IsNotice);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void OnSetRelationNotice(const int32& IsNotice);

	/// 黑名单
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void AddBlacklist(const FString& Name);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addBlacklistRelation(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip,
			const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RemoveBlacklist(const FString& RelationUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_removeBlackList(const FString& RelationUID);

	/// 不友好
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void AddFoe(const FString& Name);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addFoeRelation(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip,
			const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Relation")
		void RemoveFoe(const FString& RelationUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_removeFoe(const FString& RelationUID);
	
	/// 讨论组=====暂时屏蔽
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		FRelationGroupData GetRelationGroupByUID(const int32& GroupIndex, int32& Index);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		FRelationGroupMember GetRelationGroupMemberByUIDAndName(const int32& GroupUID, const FString& PlayerName, int32& Index);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void CreateGroup(const FString GroupName, const bool IsAllowJoin, const FString& PassWord);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void DeleteGroup(const int32& GroupIndex);
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void InvitedToGroup(const int32& GroupIndex, const FString& PlayerName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Group")
		void relation_receiverGroup(const int32& GroupIndex, const FString& GroupName, const FString& EndTime, const FString& CreaterName, const FString& PassWord, const int32& IsAllowJoin, const TArray<FString>& BlackList);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Group")
		void relation_receiverGroupInfo(const int32& GroupIndex, const FString& PlayerName, const int32& Profession, const int32& level, const int32& Camp, const int32& IsOnline);
	/// 密码进入讨论组
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void RequestEnterGroupByPassword(const int32& GroupIndex, const FString& PassWord);
	/// 玩家主动离开讨论组
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void ActiveLeaveGroup(const int32& GroupIndex);
	/// 玩家被请离讨论组
	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void PassiveLeaveGroup(const int32& GroupIndex, const FString& PlayerName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_onPlayerRemoveGroup(const int32& GroupIndex, const FString& PlayerName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_onDelectGroup(const int32& GroupIndex);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void ChangeGroupLeater(const int32& GroupIndex, const FString & PlayerName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_changeGroupLeater(const int32& GroupIndex, const FString& PlayerName);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void AddEndTime(const int32& GroupIndex, const GROUP_END_TYPE & EndTime);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addEndTime(const int32& GroupIndex, const FString& EndTime);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void AddGroupBlackList(const int32& GroupIndex, const FString& PlayerName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_addGroupBlackList(const int32& GroupIndex, const FString& PlayerName);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void DelGroupBlackList(const int32& GroupIndex, const FString& PlayerName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_delGroupBlackList(const int32& GroupIndex, const FString& PlayerName);

	UFUNCTION(BlueprintCallable, Category = "RoleRelationInterface|Group")
		void updateGroupInfo(const int32& GroupIndex, const FString& GroupName, const bool IsAllowJoin, const FString& PassWord);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_updateGroupInfo(const int32& GroupIndex, const FString& GroupName, const int32& IsAllowJoin, const FString& PassWord);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_onNoticePlayerOnLine(const int32& GroupIndex, const FString& PlayerName, const int32& level);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_onPlayerOffLine(const int32& GroupIndex, const FString& PlayerName);

	/// 推荐讨论组数据
	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface|Relation")
		void relation_recommendGroup(FString& JsonStr);

	virtual void InitBlueCB() override;

private:
	void AddRelation_(const FString& RelationUID, const FString& Name, const FString& DBID, const int32& PlayerID, const int32& RelationShip,
		const int32& Profession, const int32& Level, const int32& Camp, const FString& TongName, const FString& LocalSpace);
	void RemoveRelation_(const FString& RelationUID, RELATION_SHIP relation);


public:
	///好友上线是否通知
	UPROPERTY(BlueprintReadOnly, Category = "RoleRelationInterface|Relation")
		bool IsNoticeFriend = true;
	///关系列表{ relationUID : relationData,.... }
	UPROPERTY(BlueprintReadOnly, Category = "RoleRelationInterface|Relation")
		TMap<FString,FRelationData> RelationDict;
	///分组数据
	UPROPERTY(BlueprintReadOnly, Category = "RoleRelationInterface|Relation")
		TArray<FRelationCatalogData> RelationCatelogs;

	///讨论组{ groupUID : groupData,.... }
	UPROPERTY(BlueprintReadOnly, Category = "RoleRelationInterface|Group")
		TMap<int32, FRelationGroupData> RelationGroupDict;
	///推荐讨论群
	UPROPERTY(BlueprintReadOnly, Category = "RoleRelationInterface|Group")
		TArray<FRelationGroupSimple> RelationRecommendGroup;
	///好友邀请数据
	UPROPERTY(BlueprintReadOnly, Category = "RoleRelationInterface")
		TArray<FString> RelationFriendInviteList;
};
