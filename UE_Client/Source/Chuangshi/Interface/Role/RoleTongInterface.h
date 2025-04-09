// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/TongClass.h"
#include "GameData/TongData.h"
#include "Util/CS3Debug.h"
#include "GameData/BHZBData.h"
#include "RoleTongInterface.generated.h"

/*
* 文件名称：RoleTongInterface.h
* 功能说明：帮会接口类
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018/1/26
*/

CONTROL_COMPILE_OPTIMIZE_START




UCLASS(BlueprintType)
class CHUANGSHI_API URoleTongInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleTongInterface();
	~URoleTongInterface() {};
	static FString GetName() { return TEXT("RoleTongInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTongInterface.BP_RoleTongInterface_C'"); } //获取蓝图对象路径

	///< 向服务器请求所有帮会数据，如果返回为True,则表明客户端已向服务器请求过。可直接访问数据
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool RequireAllTong();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnReceiveAllTong();
		void CLIENT_OnReceiveAllTong(const FVariant& Variant);
	///< 帮会搜索（根据帮会名搜索）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongJoinData> SearchJoinListByName(const FString& tongName);
	///< 帮会筛选（是否显示已满帮派）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongJoinData> SearchJoinListByIsFull(const bool isFull);

	///< 判断玩家自己是否已经加入帮会
	UFUNCTION(BlueprintPure, Category = "RoleTongInterface")
		bool hasTong();
	///< 判断玩家是否在本帮派中
	UFUNCTION(BlueprintPure, Category = "RoleTongInterface")
		bool IsInSameTong(const int32& entityID_);

	//创建帮会
	UFUNCTION(BlueprintCallable)
		void CreateTong(const FString& tongName);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnJoinTong();

	///< 玩家申请加入帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void TongReqJoin(const FString& tongDBID);
	///< 收到其他玩家加入帮会申请
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnOtherReqJoinTong(const FString& playerDBID, const FString& playerName, const int32& level, const int32& profession);

	///< 玩家取消 申请加入帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void CancelJoinTong(const FString& tongDBID);
	///< 收到其他玩家取消 加入帮会申请
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnOtherCancelJoinTong(const FString& playerDBID);
	///< 通过角色DBID移除未读申请列表（申请者主动取消的时候会移除）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RemoveNoReadApplicantList(const FString& playerDBID);
	///< 清空未读申请列表（申请列表界面打开的时候会清空）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void ClearNoReadApplicantList();
	///< 判断是否有未读申请消息
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool HasNoReadApplicant();
	///< 收到通知移除某个申请加入的成员
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnRemoveApplyJoinTongMember(const FString& playerDBID);

	///< 设置玩家上下线提示
	UFUNCTION(BlueprintCallable)
		void SetNoticeLine(bool bNotice) { isNotice = bNotice; };

	///< 玩家请求 其他玩家申请加入帮会的 列表（只有在打开申请列表界面的时候去请求，不做实时更新）（废弃）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RequestPlayerJoin();
	/**
	*Define method													
	*BlueprintNativeEvent,请求 帮会申请加入列表（废弃）
	*
	*@param DBIDList - 所有申请者的DBID列表
	*@param nameList - 所有申请者的名字列表
	*@param levelList - 所有申请者的等级列表
	*@param proList - 所有申请者的职业列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnRequestJoinList(const TArray<FString>& DBIDList, const TArray<FString>& nameList, const TArray<int32>& levelList, const TArray<int32>& proList);

	/**
	*Define method
	*BlueprintNativeEvent,申请者收到被拒绝加入帮会
	*
	*@param TongDBID - 帮会DBID
	*@param tongName - 帮会名字
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnRefuseJoinTong(const FString& TongDBID, const FString& tongName);
	//申请者收到申请加入帮会失败的事件
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnApplyJoinTongFailed(const FString& TongDBID);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnApplyJoinTongSuccess(const FString& TongDBID);

	///< 帮中拥有权限成员回复申请加入帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void ReplyJoinTong(const FString& playerDBID, bool canJoin);
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void ReplyAllJoinTong(bool canJoin);

	///< 邀请加入帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void InviteJoinTong(const int32& targetID_);
	///< 远程邀请加入帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RemoteTongInviteJoin(const FString& targetName);

	///< 传送到帮会领地
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void GotoTongSpace();

	///< 成员上下线
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnMemberOnline(const FString& dbid, const int32& id);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnMemberOffline(const FString& dbid, const int32& level, const FString& birthSpace, const FString& offTime);

	///< 成员搜索（根据帮会成员名搜索）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<UTongMember*> SearchTongMemberByName(const FString& name);
	///< 成员筛选（是否显示离线帮众，isOnline为False，显示离线帮众）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<UTongMember*> SearchTongMemberByLine(const bool isOnline);
	
	///< 更新帮会数据（玩家入帮的时候和上线的时候通知）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void onUpdateTongDatas();
	void UpdateTongDatas(const FVariant& JsonStr);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnInitTongApplyList(const TArray<FString>& joinTongList);


	///< 更新帮会成员数据（1、玩家入帮的时候会收到所有帮会成员信息，2、帮会成员收到新入帮的玩家信息）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void UpdateTongMember( );
		void CLIENT_UpdateTongMember(const FVariant& JsonStr);

	///< 有权限的玩家请求服务器踢人
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void KickTongMember(const FString& targetDBID);
	/**
	*Define method
	*BlueprintNativeEvent,所有帮会成员收到踢人的消息回调通知（包括被踢者）
	*
	*@param kickerDBID - 踢人DBID
	*@param beKickerDBID - 被踢者DBID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnKickTongMember(const FString& kickerDBID, const FString& beKickerDBID);

	///< 玩家请求退出帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void QuitTong();

	/**
	*Define method
	*BlueprintNativeEvent,帮会成员收到某某退出帮会消息回调通知（服务器是先做退出处理再删除数据，所以包括退出的玩家）
	*
	*@param playerDBID - 退出帮会的玩家的DBID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnQuitTong(const FString& playerDBID);

	///< 解散帮会
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void DismissTong();

	///< 离开帮会回调（包括被踢出帮会、主动退出帮会及解散帮会）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnLeaveTong();

	///< 更新帮会成员数据（1、玩家入帮的时候会收到所有帮会成员信息，2、帮会成员收到新入帮的玩家信息）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void UpdateTongMemberInfo(const FString& playerDBID, const int32& level, const FString& birthSpace, const int32& soldierAmount, const int32& militaryRank);

	// ==========================更改帮会属性=======================================================
	///< 设置帮会职位称号
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetTitleName(int32 titleType, const FString& name);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetTitleName(const int32& titleType, const FString& name);
	///< 设置帮会职位称号失败通知（失败之后需重置界面）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetTitleNameFailed();

	///< 任免职务
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetTongTitle(const FString& playerDBID, const int32& titleTypee);
	///< 服务器回调通知设置职务（转让帮主也会调这个方法）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetTongTitle(const FString& playerDBID, const int32 titleType);
	///< 获取帮会某职称成员数量
	UFUNCTION(BlueprintPure, Category = "RoleTongInterface")
		int32 GetMemberNumByTitle(int32 titleType);


	///< 转让帮主
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void deMiseLeader(const FString& playerDBID);
	///< 帮会帮主改变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnLeaderChange(const FString& playerDBID);

	///< 玩家帮会资金改变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnTongMoneyChange(const int32& tongMoney);
	///< 玩家帮会活跃度改变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnActivityChange(const int32& Activity);
	///< 玩家帮会成长度改变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnGrowChange(const int32& Grow);

	///< 帮会成员帮贡（剩余帮贡、周帮贡、累计帮贡都会相应改变）改变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnContributionChange(const FString& dbid, const int32& contribute);
	///< 帮会成员帮会经验变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void onTongMemberExpChange(const FString& dbid, const int32& exp);

	/**
	*BlueprintCallable,请求服务器设置帮会权限
	*
	*@param titleType - 帮会职称
	*@param gradeList - 可操作权限并勾选的(不包括系统权限）)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetGrade(const TONG_TITLE_TYPE titleType, const TArray<TONG_GRADE_TYPE>& gradeList);

	/**
	*Define method
	*BlueprintNativeEvent,服务器设置帮会权限回调通知客户端
	*
	*@param titleType - 帮会职称
	*@param grades - titleType这个职位下，所有可操作的权限（包括系统权限）按位运算的结果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetGrade(const int32& titleType, const int32& grades);
	///<设置权限失败通知（权限设置失败后需重置权限管理界面）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetGradeFailed();

	///<帮会屏蔽列表改变
		void OnTongBlocklistChange(const TArray<FVariant>& BlockList);

	///< 捐献金钱
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void DonateMoney(const int64& money);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnDonateMoney(const int64& money);
	///< 获取有效的捐献输入金额，捐献金钱最少是1最大不超过玩家身上的金钱（单位金币）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		FString GetValidInputDonateMoney(const FString& InputMoney);

	///< 设置帮会公告
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetAffiche(const FString& affiche);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetAffiche(const FString& affiche);

	///< 设置招募公告
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetRecruitAffiche(const FString& affiche);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetRecruitAffiche(const FString& affiche);

	///< 禁言
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetGag(const FString& dbid, const int32& isGag);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnSetGag(const FString& dbid, const int32& isGag);

	//帮会分配方式
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetTongAllocation(const TONG_PICKUP_TYPE& allocation);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void onSetTongAllocation(const uint8& allocation);
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetTongBHLDAllocation(const TONG_PICKUP_TYPE& allocation);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void onSetTongBHLDAllocation(const uint8& allocation);

	///< 帮会签到
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void TongSign();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnTongSign();
	///< 0点服务器通知更新签到状态及领取俸禄状态
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void onDawnArrive();

	///< 领取俸禄
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void GetSalary();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnGetSalaryFail();

	///< 判断玩家自己是否有某某权限
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool HasGradeTong(TONG_GRADE_TYPE GradeType);			
	///< 判断某某职称是否有某某权限
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool HasGradeByTitle(TONG_TITLE_TYPE titleID, TONG_GRADE_TYPE GradeType);	
	///< 判断某职称下的某权限是不是系统权限
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool IsSysGrade(const TONG_TITLE_TYPE& titleID, const TONG_GRADE_TYPE& GradeType);
	///< 判断某职称下的某权限是不是可操作权限
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool IsDefGrade(const TONG_TITLE_TYPE& titleID, const TONG_GRADE_TYPE& GradeType);
	///< 判断某职称下的某权限是不是禁止权限
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool IsFobGrade(const TONG_TITLE_TYPE& titleID, const TONG_GRADE_TYPE& GradeType);

	///< 获取建筑相关提示
	///< 获取帮会建筑升级需要的金钱
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		int32 GetMoneyByBuildLevel(uint8 BuildLevel, TONG_BUILD_TYPE BuildType);
	///< 获取帮会建筑升级需要的成长度
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		int32 GetGrowByBuildLevel(uint8 BuildLevel, TONG_BUILD_TYPE BuildType);
	///< 根据帮会建筑等级及类型获取帮会建筑升级效果
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		FString GetEffectByBuildLevel(uint8 BuildLevel, TONG_BUILD_TYPE BuildType);

	///< 建筑升级
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void UpgrowBuild(TONG_BUILD_TYPE BuildType);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnUpgrowBuild(int32 BuildType, int32 level);
	///< 议事大厅升级，更新人数上限
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnConferenceHallLevelChange(int32 LimitNum);

	///< 帮会升级
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void UpgrowTong();
	///< 帮会等级、以及下一级升级需要的活跃度
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnUpgrowTong(const int32& level, const int32& upGradeActivity);

	///< 帮会技能研发
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void ResearchTongSkill(const int32& skillID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnResearchTongSkill(const int32& skillID);
	///< 暂停帮会技能研发
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void PauseTongSkill(const int32& skillID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnPauseTongSkill(const int32& skillID);
	///< 帮会技能研发进度改变通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnTongSkillProgressChange(const int32& Progress);
	///< 帮会技能研发完成通知
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnFinishResearchSkill(const int32& skillID);
	///< 学习研发的技能
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void StudyTongSkill(const int32& skillID);
	///学习技能完成回调
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnFinishLearnSkill(const int32& skillID);
	/**
	*BlueprintCallable,获取帮会技能研发界面显示的数据
	*
	*@return TArray<int32>& state 当前技能研发状态（state:0 ---正在研发；state:1 ---暂停研发；state:2  ---未研发）
	*@return TArray<int32>& playerLevel 玩家学习这个技能的等级（playerLevel=0代表未学习）
	*@return TArray<FTongSkillDATA>  技能研发数据结构体数组
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongSkillDATA> GetAllResearchSkills(TArray<int32>& state,TArray<int32>& playerLevel);
	///< 根据技能ID获取当前研发技能数据
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		FTongSkillDATA GetResearchSkillData(const int32& curSkillID);
	///< 获取当前研发技能的最大等级和玩家学习到等级
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void GetResearchSkillLevelRelevant(const int32& SkillID, int32& CurLevel, int32& MaxLevel);

	///< 帮会事件
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool RequireTongEvent();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnRequireTongEvent();
	void CLIENT_OnRequireTongEvent(const FVariant& TongEvent);
	
	/**
	*BlueprintCallable,根据帮会事件设置类型获取帮会事件
	*
	*@param classType - 帮会事件设置类型勾选的列表
	*@param time - 界面组合框选中的时间筛选索引（0：只显示今日；1：显示一周；2：显示一月；3：显示所有；）
	*@param isShowOnlyMe - 是否只显示与我相关
	*
	*@return TArray<FTongEventDATA> 帮会事件数据列表
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongEventDATA> GetTongEventByClassType(const TArray<TONG_EVENT_SET_TYPE> classType, const int32 time, const bool isShowOnlyMe);
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongStoreEventData> GetTongStoreEventByType(const TONG_STORE_EVENT_TYPE type, bool getAll);

	///< 帮会仓库事件
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RequireTongStoreEvent();
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnRequireTongStoreEvent( );
	void CLIENT_OnRequireTongStoreEvent(const FVariant& TongEvent);

	///< 帮会仓库相关操作
	/// 帮会仓库，参数1：帮会仓库容量（格子数量）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OpenTongStore(const int32& NPCID, const int32& tongStoreCapacity);
	/// 右键保存srcOrder到帮会仓库（bagID:0-第一个包裹，1-第二个包裹...）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RequestSaveTongItem(const int32& srcOrder, const int32& bagID);
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RequestTakeTongItem(const int32& srcOrder);
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SortTongStoreItem(const int32& bagID);
	///打开神兽界面
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OpenTongNagualUI();
	///更换神兽
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RequestChangeNagual(int32	nagualType);
	///切换神兽成功回调
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnChangeNagualCB(const uint8& result);
	///
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void UpdateNagualType(const int32& nagualType);

	///帮会名改变
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void OnRep_tongName();

	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnTongNameChange();
	
	//收到帮会邀请
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void ReceiveInviteJoinTong(const FString& inviterName, const int32& inviterID, const FString& tongName, const FString& tongDBID);

	//回复帮会邀请
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void ReplyInviteTong(bool IsAccept, int32 InviterID, FString TongDBID);

	//删除帮会邀请数据
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void DeleteTongInvite(FTongInviteData TongInviteData);

	///< 清除玩家帮会信息
	void ClearTongInfo();
	virtual void onEnterWorld();
	virtual void onLeaveWorld(); ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void InitBlueCB() override;

#pragma region 帮会争霸相关
	/// 准备报名帮会争霸成员
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void ReadyToSignUpBHZBMember(TArray<FBHZBSIGNMEMBERDATA> signUpMemberDatas);
	/// 确认报名帮会成员回调
	void OnSureSignUpBHZBMember(const FVariant& Var);
	/// 设置帮会争霸报名成员队伍状态
	void SetbhzbSignUpMembersIsActive(int32 groupID, uint8 isActive, int32 pointIndex);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBarracksInterface")
		void BPOnSureSignUpBHZBMember();

	/// 增加帮会争霸候选人
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool AddCandidateToBHZB(FString MemberDBID, int32 TeamGroupID, bool IsCaptain);
	/// 移除帮会争霸候选人
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool RemoveCandidateFromBHZB(FString MemberDBID);
	/// 选取或取消帮会争霸候选人
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SetIsSeletedCandidateToBHZB(FString MemberDBID, int32 TeamGroupID, bool isCaptain);
	/// 争霸候选人是否被选取
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		bool IsCandidateSelected(FString MemberDBID);

	void ClearAllTongSignMemberData();

	///< 发起掠夺战
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void SignUpTongPlunder(const FString& targetTongDBID);
	///< 添加参战成员
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void PlunderAddMember(const FString& playerDBID);
	///< 改变参战人员
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void PlunderRemoveMember(const FString& PlayerDBID);

	///< 添加参战成员改变
		void OnPlunderMemberChange(const TArray<FVariant>& MemberDBIDList);

	///< 打开掠夺战帮会列表界面
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTongInterface")
		void OnOpenPlunderTongListWnd();
	void OpenPlunderTongListWnd(const FVariant& TongInfos);

	///< 获取帮会掠夺战参赛人员信息
	UFUNCTION(BlueprintPure, Category = "RoleTongInterface")
		TArray<UTongMember*> GetPlunderMemberInfo();

	///< 帮会搜索（根据帮会名搜索）
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongJoinData> SearchPlunderListByName(const FString& tongName);
	
	///< 帮会掠夺列表
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		TArray<FTongJoinData> GetPlunderTongDatas(int32 Camp);

	///< 帮会掠夺列表 帮会数据
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		FTongJoinData GetPlunderTongDataByTongDBID(FString TongDBID, bool& IsSuccess);

	/// 加入屏蔽列表
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void AddTongBlockList(const FString& memberDBID);
	/// 移除屏蔽列表
	UFUNCTION(BlueprintCallable, Category = "RoleTongInterface")
		void RemoveTongBlockList(const FString& memberDBID);

#pragma endregion

private:
	void Tong_BaseCall(const FString& name, KBEngine::FVariantArray& args);
	void Tong_CellCall(const FString& name, KBEngine::FVariantArray& args);
	
	void InitTongGrade(bool isPlayer);
	void InitTongBuildLevel();
	void InitTongSkill();

	int32 GetPlayerTongResSkillLevel(TArray<int32> SkillList);
	
	FORCEINLINE TArray<FString> ChangeEventTypeToStr(TONG_EVENT_TYPE& EventType, TArray<FString> Params);
public:
	///<玩家帮会数据
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		UTongObject* Tong;
	///<所有帮会数据
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TMap<FString, FTongJoinData> TongDatas;

	///<申请者列表
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FPlayerJoinData> ApplicantDataList;

	///<未读申请者DBID列表
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FString> NoReadApplicantList;

	///<玩家已经申请入帮的帮会DBID列表
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FString> TongApplyList;

	///<帮会事件
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FTongEventDATA> TongEventList;
	///<帮会仓库事件
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FTongStoreEventData> TongStoreEventList;

	///<帮会仓库包裹开启的格子数量
	UPROPERTY(BlueprintReadOnly)
		int32 OpenGridCapacity;

	///<帮会仓库包裹默认能够解锁的的格子数量
	UPROPERTY(BlueprintReadOnly)
		int32 CanUnLockGridCapacity = 0;

	///<帮会邀请
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FTongInviteData> TongInviteList;
	///帮会争霸参与成员数据
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TMap<int32, FBHZBSIGNMEMBERDATA> JoinBHZBMemberDatas;
	///帮会争霸候选人列表
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TArray<FBHZBCandidate> BHZBCandidates;
	UPROPERTY(BlueprintReadOnly, Category = "RoleTongInterface")
		TMap<FString, FTongJoinData> PlunderTongDatas;

private:
				
	//FDateTime RequitJoinTime;							// 请求服务器帮会数据 时间
	//FDateTime RequitEventTime;							// 请求服务器帮会事件 时间

	TArray<TArray<int32>> TongSkillList;				// 帮会技能ID数据[[技能ID，技能ID..],[技能ID，技能ID..]]
	TMap<int32, FTongSkillDATA*> TongSkillDatas;			// 帮会技能数据

	///<帮会建筑升级数据
	TMap<uint8, TMap<TONG_BUILD_TYPE, FTongUpGradeData>> TongBuildUpGrade;

	TMap<TONG_TITLE_TYPE, int32> SysGrades;				// 系统权限（不可操作，默认勾选）
	TMap<TONG_TITLE_TYPE, int32> DefaultGrades;			// 可操作权限（可操作权限，是不是勾选要根据HasGradeByTitle判断）
	TMap<TONG_TITLE_TYPE, int32> ForbidGrades;			// 禁止权限（不可操作，默认不勾选）

	bool isNotice;										// 玩家上下线提示

	TArray<FString> PlunderMembers; //帮会掠夺战参赛成员列表, dbid
};

CONTROL_COMPILE_OPTIMIZE_END
