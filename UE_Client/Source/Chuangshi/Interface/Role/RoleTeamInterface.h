// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CS3Base/CS3EntityInterface.h"
#include "CS3Base/CS3InterfaceDeclare.h"
#include "GameData/CsvTableRowBase.h"
#include "GameData/TeamMemberData.h"
#include "GameData/BigmapActInfo.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/BuffData.h"
#include "GameData/CsvTableRowBase.h"
#include "Entity/Alias.h"
#include "RoleTeamInterface.generated.h"

/*
* 文件名称：RoleTeamInterface.h
* 功能说明：角色组队接口类
* 文件作者：ouyangminzhen
* 目前维护：yikun
* 创建时间：2016-10-26
*/

#pragma region 结构体
/**
* 快速组队设置界面数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFastTeamSetData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//阵营（-1:不限，1:仙道，2:魔道）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = -1;
	//职业（-1:不限）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Profession = -1;
	//设置的最低等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MinLevel = 1;
	//设置的最高等级限制
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxLevel = 100;
	//聊天频道（0:附近，1:地图，2:世界，7:帮会，9:宗门，10:阵营）默认世界频道
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ChatType = 2;
};

/**
* 组队消息数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTeamMsgData
{
	GENERATED_USTRUCT_BODY()
public:
	//EntityID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
	//阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp;
	//职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Profession;
	//等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level;
	//是否是组队邀请
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsInvite;
	//队友ID（队员邀请其他玩家入队才需要设置这个数据）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TeammateID;
	//队友名字（队员邀请其他玩家入队才需要设置这个数据）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TeammateName;
	//是否是快速组队申请
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsFastTeamApply;

	FORCEINLINE bool operator==(const FTeamMsgData& Other) const
	{
		if (this->ID == Other.ID)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};
#pragma endregion

UCLASS( )
class CHUANGSHI_API URoleTeamInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;


CS3_DECLARE_INTERFACE_MAP()

public:
	URoleTeamInterface();
	~URoleTeamInterface();
	static FString GetName() { return TEXT("RoleTeamInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTeamInterface.BP_RoleTeamInterface_C'"); } //获取蓝图对象路径

	virtual void BeginDestroy()override;
	
	///检查是否有队伍
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		bool CheckInTeam(int32 PlayerEntityID);

	///判断是不是队友
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		bool IsTeammate(int32 TargetID);
	
	/**
	*BlueprintCallable,邀请某人入队
	*
	*@param targetPlayerID 对方ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void teamInviteFC(const int32 targetPlayerID);

	/**
	*BlueprintCallable,玩家申请加入队伍
	*
	*@param targetPlayerID 对方ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void requestJoinTeamNear(const int32 targetPlayerID);

	/**
	*BlueprintCallable,请求更换队长
	*
	*@param newCaptainID 新队长ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void changeCaptainFC(const int32 newCaptainID);

	/**
	*BlueprintCallable,客户端向服务器发送请求，远程邀请某玩家组队
	*
	*@param targetPlayerName 想要邀请的玩家的名字
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void remoteTeamInviteFC(const FString& targetPlayerName);

	/**
	*BlueprintCallable,被邀请者答复组队邀请
	*
	*@param isAgree 同意还是不同意
	*@param answerID 邀请者的ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void replyTeamInviteByFC(const int32 isAgree, const int32 answerID);

	/**
	*BlueprintCallable,队长答复队员邀请其他玩家入队
	*
	*@param targetID 目标玩家（即被邀请者）的ID
	*@param targetName 目标玩家（即被邀请者）的名字
	*@param teammateID 队员ID
	*@param isAgree 同意还是不同意
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void ReplyTeammateInviteFC(const int32 targetID, const FString targetName, const int32 teammateID, uint8 isAgree);

	/**
	*BlueprintCallable,队长回复玩家的远程加队申请：同意还是不同意
	*
	*@param isAgree 同意还是不同意
	*@param RequesterID 被通知的玩家的entityID即申请者的ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void replyPlayerJoinTeamFC(const int32 isAgree, const int32 RequesterID);

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void DisbandTeamFC();///<BlueprintCallable,请求解散队伍

	/**
	*BlueprintCallable,请求离开队伍
	*
	*@param levelPlayerID 离开者EntitiyID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void LeaveTeamFC(const int32 leavePlayerID);

	/**
	*Define method
	*BlueprintCallable,申请获取队伍中某个队伍成员的数据
	*
	*@param TeammateID 某个队伍成员ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void RequestTeammateInfoFC(const int32 TeammateID);

	/**
	*BlueprintCallable,请求修改队伍物品分配模式
	*
	*@param allocation 分配模式（1：自由拾取；2：队伍拾取；3：队长分配；4：竞拍）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void SetAllocationFC(const int32 allocation);

	/**
	*BlueprintCallable,请求修改队伍物品分配品质标准
	*
	*@param quality 物品品质标准（5：绿；2：蓝；4：粉；3：金；）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void SetQualityFC(const int32 quality);

	/**
	*BlueprintCallable,玩家设置拒绝申请通知服务器
	*
	*@param isForbid 是否拒绝申请
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void setForbidTeamInviteFC(const uint8 isForbid);

	/**
	*BlueprintCallable,请求增加队伍标记（拥有标记权的玩家点队友头像菜单->标记为->某某图标）
	*
	*@param EntityID 被标记队友的EntityID
	*@param SignType 标记编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void requestAddTeamSignFC(const int32 targetID, const int32 SignType);

	/**
	*BlueprintCallable,队长发起组队跟随
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void requestLeadTeamFollowFC();

	/**
	*BlueprintCallable,队长取消组队跟随
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void cancelLeadTeamFollowFC();

	/**
	*BlueprintCallable,发起普通跟随
	*
	*@param targetID 目标ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void requestNormalFollowFC(const int32 targetID);

	/**
	*BlueprintCallable,取消普通跟随
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void cancelNormalFollowFC();

	/**
	*BlueprintCallable,玩家请求把自己传送到目标队友（使用集合石的玩家）身边
	*
	*@param targetID 目标ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void requestRoleTeamSpellBoxFollow(const int32 targetID);

	/**
	*BlueprintImplementableEvent,收到通知，被某人邀请
	*
	*@param inviterID 邀请者的id
	*@param inviterName 邀请者的名字
	*@param inviterCamp 邀请者的阵营
	*@param inviterProfession 邀请者的职业
	*@param inviterLevel 邀请者的等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void OnTeamInviteBy(const int32 inviterID, const FString& inviterName, const int32 inviterCamp, const int32 inviterProfession, const int32 inviterLevel);

	/**
	*BlueprintImplementableEvent,队长收到通知，队员邀请其他玩家入队
	*
	*@param targetID 被邀请者的ID
	*@param targetName 被邀请者的名字
	*@param targetCamp 被邀请者的阵营
	*@param targetProfession 被邀请者的职业
	*@param targetLevel 被邀请者的等级
	*@param teammateName 邀请者（即队员）的名字
	*@param teammateID 邀请者（即队员）的ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void TeamInviteByTeammate(const int32 targetID, const FString& targetName, const int32 targetCamp, const int32 targetProfession, const int32 targetLevel, const FString& teammateName, const int32 teammateID);

	/**
	*Define method
	*BlueprintNativeEvent,入队时通知队伍信息
	*
	*@param captainID 队长ID
	*@param teamID 队伍ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void teamInfoNotifyOnJoin(const int32 captainID, const int32 teamID, const int32 allocation, const int32 quality, const int32 signerID, const TArray<int32>& teamSignKeys, const TArray<int32>& teamSignValues);

	/**
	*BlueprintImplementableEvent,入队时通知队伍信息
	*
	*@param captainID 队长ID
	*@param teamID 队伍ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleTeamInterface")
		void teamInfoNotifyOnJoinBP(const int32 captainID, const int32 teamID);

	/**
	*Define method
	*BlueprintNativeEvent,队友信息信息发生变化通知
	*
	*@param PlayerID 玩家ID
	*@param Level 玩家等级
	*@param HP 玩家血量
	*@param HP_Max 玩家最大血量
	*@param MP 玩家法力值
	*@param MP_Max 玩家最大法力值
	*@param SpaceScriptID 玩家当前地图ID
	*@param LineNumber 玩家当前大地图分线 其他地图为0
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void teammateInfoNotify(const int32 PlayerID, const int32 Level, const int32 HP, const int32 HP_Max, const int32 MP, const int32 MP_Max, const FString& SpaceScriptID,const int32& LineNumber);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleTeamInterface")
		void OnTeammateInfoNotify(const FTeamMemberData& MemberData);

	/**
	*Define method
	*BlueprintNativeEvent,通知客户端修改队伍物品分配模式
	*
	*@param Allocation 分配模式(1：自由拾取；2：队伍拾取；3：队长分配)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void modifyAllocation(const int32 allocation);

	/**
	*Define method
	*BlueprintNativeEvent,通知客户端修改队伍物品分配品质标准
	*
	*@param Quality 物品品质标准（5：绿；2：蓝；4：粉；3：金；）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void modifyQuality(const int32 Quality);

	/**
	*Define method
	*BlueprintNativeEvent,添加buff回调
	*
	*@param MemberID 添加buff的队员的ID
	*@param BuffIndex buff索引
	*@param BuffID buffID
	*@param BuffTotalTime buff总共时间
	*@param BuffHoldTime buff持续时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void OnTeamMemberAddBuff(const int32 MemberID, const int32 BuffIndex, const int32 BuffID, const float BuffTotalTime, const float BuffHoldTime );
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleTeamInterface")
		void OnTeamMemberAddBuffBP(const int32& MemberID, FBuffUIData BuffUIData);
	
	/**
	*Define method
	*BlueprintNativeEvent,删除buff回调
	*
	*@param MemberID 删除buff的队员的ID
	*@param BuffIndex buff索引
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void OnTeamMemberRemoveBuff(const int32 MemberID, const int32 BuffIndex);

	/**
	*Define method
	*BlueprintNativeEvent,重置buff持续时间回调
	*
	*@param MemberID 重置buff时间的队员的ID
	*@param BuffIndex buff索引
	*@param BuffHoldTime buff持续时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void OnTeamMemberResetBuffTime(const int32 MemberID, const int32 BuffIndex, const float BuffHoldTime);

	/**
	*Define method
	*BlueprintNativeEvent,通知离队信息
	*
	*@param leavePlayerID 离队者id
	*@param isMyself 是否为自己离队
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void leaveTeamNotify(const int32 leavePlayerID, const uint8 isMyself);

	/**
	*BlueprintImplementableEvent,通知离队信息
	*
	*@param leavePlayerID 离队者id
	*@param isMyself 是否为自己离队
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleTeamInterface")
		void leaveTeamNotifyBP(const int32 leavePlayerID, const bool isMyself);

	/**
	*Define method
	*BlueprintNativeEvent,队伍解散了通知客户端
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void disbandTeamNotify();

	/**
	*BlueprintNativeEvent,通知队长变更信息
	*
	*@param captainID 队长id
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void changeCaptainNotify(const int32 captainID);

	/**
	*Define method
	*BlueprintNativeEvent,通知有玩家离线
	*
	*@param logoutEntitiyID 离线玩家的id
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void logoutNotify(const int32 logoutEntitiyID);

	/**
	*Define method
	*BlueprintNativeEvent,玩家归队通知
	*
	*@param oldEntitiyID 归队玩家旧的id
	*@param newEntitiyID 归队玩家目前的id
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void onRejoinTeam(const int32 oldEntitiyID, const int32 newEntitiyID);

	/**
	*Define method
	*BlueprintImplementableEvent,有人申请加入自己的队伍
	*
	*@param requesterID 申请者ID
	*@param roleName 申请者名字
	*@param camp 申请者阵营
	*@param profession 申请者职业
	*@param level 申请者等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void OnReceiveJoinTeamRequest(const int32 requesterID, const FString& roleName, const int32 camp, const int32 profession, const int32 level );

	/**
	*Define method
	*BlueprintNativeEvent,队员入队通知
	*
	*@param newMemberDBID - 新队员的DBID
	*@param newMemberID - 新队员的ID
	*@param newMemberName - 新队员的名字
	*@param newMemberProfession - 新队员的职业
	*@param isOnline - 新队员是否在线
	*@param newMemberLevel - 新队员等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void addTeamMember(const FString& newMemberDBID, const int32 newMemberID, const FString& newMemberName, const int32 newMemberProfession, const int32 isOnline, const int32 newMemberLevel);
	
	/**
	*BlueprintImplementableEvent,队员入队通知
	*
	*@param newMemberDBID - 新队员的DBID
	*@param newMemberID - 新队员的ID
	*@param newMemberName - 新队员的名字
	*@param newMemberProfession - 新队员的职业
	*@param isOnline - 新队员是否在线
	*@param newMemberLevel - 新队员等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleTeamInterface")
		void addTeamMemberBP(const FTeamMemberData& MemberData);

	void UpdateMemberDataFar();
	void UpdateMemberDataNear();
	void UpdateMemberPos();

	/**
	*Define method
	*BlueprintNativeEvent,打标记服务器端回调
	*
	*@param EntityID - 目标entity id
	*@param SignNumber - 标记编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void AddTeamSignCB(const int32 TargetID, const int32 SignNumber);

	///清除所有队伍标记
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void ClearTeamSign();

	///判断玩家有没有队伍？
	UFUNCTION(BlueprintPure, Category = "RoleTeamInterface")
		bool HasTeam();

	///在组队跟随中？
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		bool IsTeamFollowing();
	
	///开始组队跟随
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void StartTeamFollow(const int32 captainID);

	///结束组队跟随
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void StopTeamFollow();

	///跟随新队长
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void FollowNewCaptain(const int32 newCaptainID);

	///组队跟随tick
	void DetectTeamFollow();

	///检测组队跟随不合法时间是否超时
	bool TeamFollowWaitTimeCheck();
	
	/**
	*BlueprintCallable,队员取消组队跟随
	*
	*@param CancelReason 原因类型（1、不合法（找不到目标或者卡住）；2、离领导者太远；3、主动取消；4、状态限制（如死亡、被定身等））
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
	void CancelTeamFollowForce(TEAM_FOLLOW_FAILURE_REASON CancelReason);

	/**
	*Define method
	*BlueprintNativeEvent,把同地图其它队友传送到使用场景物件的玩家身边（同地图所有队友客户端收到消息）
	*
	*@param TargetID - 使用场景物件的玩家ID
	*@param TotalTime - 技能读条总时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
	void RoleTeamSpellBoxFollow(int32 TargetID, float TotalTime);

	//---------------------------普通跟随---------------------------------
	///在普通跟随中？
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		bool IsNormalFollowing();

	///开始普通跟随
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void StartNormalFollow(const int32 targetID);

	///结束普通跟随
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void StopNormalFollow(); 

	///强制取消普通跟随
	void CancelNormalFollowForce();

	///普通跟随tick
	void DetectNormalFollow();

	///检测普通跟随不合法时间是否超时
	bool NormalFollowWaitTimeCheck();
	//---------------------------普通跟随---------------------------------

	///队员是否已经满了
	UFUNCTION(BlueprintPure, Category = "RoleTeamInterface")
		bool IsTeamMemberFull();

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void ShareBigMapCustomMarkerToTeam(const FString& LevelName, const FVector Position, const int32 MarkerType);

	///队友分享大地图标记的回调
	UFUNCTION(BlueprintCallable, Category = "cs3|Entity")
		void onMemberShareBigMapCustomMarker(const FString& MemberName, const FString& LevelName, const FVector Position, const int32 MarkerType);
	
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|Entity")
		void onMemberShareBigMapCustomMarkerBP(const FString& MemberName, const FString& LevelName, const FVector Position, const int32 MarkerType);

	/**
	*BlueprintCallable,获得队员在法宝上的索引
	*
	*@param memberID 队员EntityID
	*
	*@return 索引
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		int32 GetMemberIndexOnFaBaoByEntityID(int32 memberID);

	/**
	*Define method
	*BlueprintNativeEvent,队长移交后,新的队长如果有标记的需要移除标记
	*
	*@param TargetID - 新队长ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void RemoveTeamSigner(int32 TargetID);

	void AddTeamPosMap(int32 entityID, FVector position, FString playerName);

	void CLIENT_OnUpdateMemeberPos( const FVariant& BIGMAP_SHOW_INFO_1 );

	/**
	*BlueprintCallable,召唤全队同线
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
	void CELL_CallAllTeamMemberToCaptainLineNumber();
#pragma region 快速组队相关
	/**
	*Define method
	*BlueprintNativeEvent,通知客户端已开始快速组队
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void CLIENT_OnStartTeamSearch( const FString& spaceName );

	/**
	*Define method
	*BlueprintNativeEvent,取消快速组队
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void CLIENT_OnFastTeamCancelMatch();

	/**
	*Define method
	*BlueprintNativeEvent,匹配成功
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void FastTeamOnMatchSuccess();

	/**
	*BlueprintNativeEvent,收到通知，被某人申请
	*
	*@param applyID 申请者的id
	*@param applyName 申请者的名字
	*@param applyCamp 申请者的阵营
	*@param applyProfession 申请者的职业
	*@param applyLevel 申请者的等级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void CLIENT_teamByApply(const int32 applyID, const FString& applyName, const int32 applyCamp, const int32 applyProfession, const int32 applyLevel);
	
	/**
	*BlueprintCallable,答复快速组队的申请
	*
	*@param agree 是否同意加入
	*@param applyID 申请者的EntitiyID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void CELL_ReplyTeamApplyFastTeam(int32 agree, int32 applyID);
	/**
	*BlueprintNativeEvent 打开快速组队面板
	*@param	reqLevel 等级要求
	*
	*return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
	void CLIENT_OpenFastTeamWin(const FString& bunchSpaceScriptID,const int32& reqLevel,const int32& isMatchFastTeam, const FString& ScriptID, const int32& ID, const FString& Key);

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void RequestFastTeam();

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void RequestCancelFastTeamMatch();

	//设置快速组队设置面板数据
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void SetFastTeamSettingData(FFastTeamSetData SettingData);
	//设置快速组队面板默认数据
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void SetFastTeamSettingDefaultData();
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		FFastTeamSetData GetFastTeamSettingData();

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void BASE_setFastTeamData();

	/**
	*BlueprintCallable,申请加入别人快速组队
	*
	*@param playerName 玩家名称
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void CELL_ApplyJoinFastTeam(FString playerName);

	/**
	*BlueprintCallable,邀请成员进入副本
	*
	*@param applyID 申请者的EntitiyID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void CELL_CallMemberEnterSpaceCopy(int32 targetID);

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void FastTeamRequestGotoBunchSpace();

	/**
   *Define method
   *BlueprintNativeEvent,匹配时间
   *@return 无
   */
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void CLIENT_OnSetTeamSearchTime(const int32& calcMatchTime);

#pragma endregion
	/**
	*BlueprintCallable,请求服务器设置队伍集结点
	*
	*@param spaceScriptID 集结的地图ScriptID
	*@param	position 集结的坐标
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void CELL_teamAssembled(const FString& spaceScriptID, FVector position);

	/**
	*
	*@param spaceScriptID 集结的地图ScriptID
	*
	*@param	position 集结的坐标
	*
	*return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTeamInterface")
		void CLIENT_onTeamAssembled(const FString& spaceScriptID, FVector position);

	//判断所有成员是否同线
	UFUNCTION(BlueprintPure, Category = "RoleTeamInterface")
		bool IsAllMemberSameLineNumber();

	void UpdateMemberDataByReJoinTeam(int32 oldEntitiyID, int32 newEntitiyID);
	void UpdateTeamSignDataByReJoinTeam(int32 oldEntitiyID, int32 newEntitiyID);

	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
	FTeamMemberData GetMemberData(const int32& targetID);
	virtual void InitBlueCB() override;
	
	//删除组队申请数据
	UFUNCTION(BlueprintCallable, Category = "RoleTeamInterface")
		void DeleteTeamInvite(int32 PlayerEntityID);

public:
	///< 队伍ID	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TeamID")
		INT32 Team_ID;
	///< 队长entityID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CaptainID")
		INT32 Captain_ID;
	///< 队长entityID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Allocation")
		TEAM_PICKUP_TYPE Allocation;
	///< 队员列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Members")
		TArray<FTeamMemberData> Members;
	///< 队伍标记数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TeamSignData")
		TMap<int32, int32> TeamSignData;
	///< 组队跟随目标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TeamFollowTarget")
		int32 TeamFollowTarget;
	///< 普通跟随目标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NormalFollowTarget")
		int32 NormalFollowTarget;
	///< 传送目标ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TeleportTargetID")
		int32 TeleportTargetID;
	///< 拒绝组队邀请（0：没勾选拒绝，1：勾选了拒绝）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "forbidTeamInvite")
		int32 forbidTeamInvite;
	///< 队员位置数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TeamPosData")
		TMap<int32,FBigmapActInfo> TeamPosMap;

	///< 队员分线数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TeamLineNumberMap")
		TMap<int32, int32> TeamLineNumberMap;
	
	//集结的地图ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "AssembledSpaceID")
		FString AssembledSpaceScriptID;

	//集结的坐标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "AssembledPosition")
		FVector AssembledPosition;

	///< 快速组队副本最低等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SpaceCopyLevel")
		int32 SpaceCopyLevel;
	///< 快速组队副本串ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "BunchSpaceScriptID")
		FString BunchSpaceScriptID;
	///< 快速组队副本队伍最大人数
	///< 快速组队副本对话NPCScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NPCScriptID")
		FString NPCScriptID;
	///< 快速组队对话NPCID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NPCID")
		int32 NPCID;
	///< 快速组队进入副本的talkKey
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TalkKey")
		FString TalkKey;

	///组队申请数据
	UPROPERTY(BlueprintReadOnly, Category = "RoleTeamInterface")
		TArray<FTeamMsgData> TeamInviteList;

private:
	FTimerHandle MemberDataFarTimer;
	FTimerHandle MemberDataNearTimer;
	FTimerHandle TeamFollowTimer;///< 组队跟随侦测timer
	FDateTime TeamFollowWaitTime = FDateTime::MinValue();///< 记录组队跟随等待时间
	FTimerHandle NormalFollowTimer;///< 普通跟随侦测timer
	FDateTime NormalFollowWaitTime = FDateTime::MinValue();///< 记录普通跟随等待时间

	FTimerHandle MemberSynPosTimer; ///<队员位置数据的Timer 备注下：没有用MemberDataFarTimer这个Timer的原因；因为不在同一大地图的队友就不需要更新队友位置信息了,目前暂时已加在不同地图的队友也同步了下位置信息，后面可加入判断剔除
	FFastTeamSetData FastTeamSetData; ///<快速组队设置面板数据
};