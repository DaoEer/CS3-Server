// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "GameFramework/SaveGame.h"
#include "Entity/Alias.h"
#include "GameData/RoleInfo.h"
#include "GameData/CS3Object.h"
#include "GameData/GameDefine.h"
#include "Level/CS3LevelScriptActor.h"
#include "GameData/ServerListData.h"
#include "AllowWindowsPlatformTypes.h"
#include <wtypes.h>
#include "HideWindowsPlatformTypes.h"
#include "GameData/CS3HttpRequest.h"
#include "LoginManager.generated.h"

/*
* 文件名称：LoginManager.h
* 功能说明：
* 文件作者：yikun
* 目前维护：wuxiaoou
* 创建时间：2016-09-07
*/
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FBeginPlayCGDelegate);
/**
 * 登陆管理器类
 */

UCLASS(Blueprintable)
class CHUANGSHI_API ULoginManager : public UCS3Object
{
	GENERATED_BODY()
public:
	ULoginManager();
	~ULoginManager();

	static ULoginManager* GetInstance();

	virtual void BeginDestroy()override;

	void Init();
	/**
	*BlueprintCallable，账号登陆
	*
	*@param server 服务器
	*@param account 账号
	*@param password 密码
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void CS3Login(FString ServerName,  FString server, FString account, FString password, FString szMsg, bool IsSaveAccount = true);

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void OnLoginBaseapp();

	/**
	*BlueprintCallable，进入游戏
	*
	*@param dbid 玩家DBID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void EnterGame(FString dbid);


	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void OnDisconnect();///<失去服务器连接

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void OnDisconnectLoad(); ///<改为登录状态

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void CS3Logoff();///<BlueprintCallable,客户端从游戏状态返回到登陆界面/直接退出

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void CS3Logout();///<BlueprintCallable,客户端从游戏状态返回到角色选择

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void CS3CancelLoginQueue();///<BlueprintCallable,客户端取消登录排队

		///<登录成功
	void OnLoginSucceed(AliasRoleInfoTmap& inst);


	///获取当前是否是登录状态
	bool GetIsLoginStatus() { return bIsLoginStatus; };


	/**
	*BlueprintImplementableEvent,创建角色回调，不管成不成功
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "LoginManager")
		void OnCreateRoleCallback();

	/**
	*设置玩家信息表
	*
	*@param inst 服务器传过来的玩家信息列表
	*
	*@return 无
	*/
	void SetRoleInfos(AliasRoleInfoTmap& inst);

	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		TArray<FROLEINFO> GetRoleInfos();///<BlueprintCallable，获取玩家信息

	/**
	*BlueprintCallable，获取玩家数据
	*
	*@param dbid 玩家DBID
	*@param roleInfo 玩家信息数据
	*
	*@return bool 获取玩家数据成功返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		bool GetRoleInfo(const FString& dbid, FROLEINFO& roleInfo);

	/**
	*根据PlayerName获取AliasRoleInfo
	*
	*@param PlayerName 玩家名字
	*
	*@return AliasRoleInfo* 玩家信息
	*/
	AliasRoleInfo* GetARoleInfo(const FString& PlayerName);

	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "LoginManager")
		bool SelectRole(AActor* Role);///<切换角色
private:
	void NotifyServerLogin(FString server, FString account, FString password, TArray<uint8> datas);///<通知服务器账号登陆
	void OnTryLoginTimeOut();///<尝试登录阶段超时
public:
	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		FString CurrAccountName;	//当前登录的角色的账号名

	UPROPERTY(BlueprintReadWrite, Category = "LoginManager")
		ACS3LevelScriptActor *CurLevelScriptActor;	//当前关卡Actor

	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		FString CurrLoginDBID; //当前准备进入游戏的角色的DBID
	
	bool bIsFirstEnterWorld; //玩家是不否是首次进入当前游戏地图，用于判断登录后第一次进入游戏，区别于传送地图

	TArray<AliasRoleInfo> roleInfos;///<玩家信息列表

	UPROPERTY(BlueprintAssignable)
		FBeginPlayCGDelegate OnBeginPlayCGDelegate;

	void SetLoginStage(ELoginStage inLoginStage);
	ELoginStage GetLoginStage();
	void OnLoginStageChange(ELoginStage newLoginStage);
	//设置账号剩余时间，上次登录时间和本次登录时间
	void SetLoginAccountInfo(int32 BalanceVal, FString LastTime, FString Time);

private:
	
	bool bIsLoginStatus = false;	///<是否登录状态
	ELoginStage currLoginStage = ELoginStage::StageNoLogin;
	FTimerHandle TryLoginHander;///<尝试登录阶段定时器

#pragma region	/** 服务器列表 */
public:
	/**
	*BlueprintCallable,获取服务器列表所有数据
	*
	*@return 服务器列表所有数据
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		TArray<FSERVER_DATA> GetAllServerListData();

	/**
	*BlueprintCallable,根据类型获取服务器列表数据
	*
	*@param ServerType 服务器类型，0盘古，1罗睺，2仙魔
	*
	*@return 服务器列表数据
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		TArray<FSERVER_DATA> GetServerListData(int32 ServerType);
	/**
	*BlueprintCallable,根据服务器名称获取服务器数据
	*
	*@param ServerName 服务器名称
	*
	*@return 服务器数据
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		FSERVER_DATA GetServerData(FName ServerName);
	/**
	*BlueprintCallable,获取服务器IP（端口随机），只用于登录界面登录时使用
	*
	*@return 服务器IP
	*/
	UFUNCTION(BlueprintPure, Category = "LoginManager")
		FString GetLoginServerIP();
	/**
	*BlueprintCallable,获取推荐服务器列表数据
	*
	*@return 推荐服务器列表数据
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		TArray<FSERVER_DATA> GetRecommentServerData();
	/**
	*BlueprintCallable,获取服务器记录列表数据
	*
	*@return 推荐服务器记录列表数据
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		TArray<FSERVER_DATA> GetRecordServerData();
	/**
	*BlueprintCallable,是否是推荐服务器
	*
	*@param ServerName 服务器名称
	*
	*@return 是否是推荐服务器
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		bool IsRecommentServer(FName ServerName);

	/**
	*BlueprintCallable,是否是新服务器
	*
	*@param ServerName 服务器名称
	*
	*@return 是否是新服务器
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		bool IsNewServer(FName ServerName);

	/**
	*BlueprintCallable,更换服务器
	*
	*@param ServerName 服务器名称
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void ChangeServer(FName ServerName);

	/**
	*BlueprintCallable,获取当前服务器名称
	*
	*@return 当前服务器名称
	*/
	UFUNCTION(BlueprintPure, Category = "LoginManager")
		FName GetCurrServerName();

	/**
	*初始化当前服务器
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void InitCurrServer();
	
	/**
	*改变当前输入的账户名（界面输入）
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		void ChangeInputAccountName(FString InAccountName);

	/**
	*根据ServerKey获取服务器数据
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginManager")
		FSERVER_DATA GetServerDataByKey(FString ServerKey, bool& IsSuccess);

	/**
	*是否有服务器列表数据
	*flase代表没有svrlist.ini文件或者文件没有配置数据（从来没有用登录器运行过是没有svrlist.ini文件的）
	*/
	UFUNCTION(BlueprintPure, Category = "LoginManager")
		bool CheckServerListNum();

	/**
	*获取是否记录账号
	*/
	UFUNCTION(BlueprintPure, Category = "LoginManager")
		bool IsSaveAccount();

private:
	/**
	*从文件读取服务器列表数据
	*/
	void RequestServerListData();
	/**
	*解析服务器列表数据文件
	*/
	void AnalyzeServerData(LPCTSTR lpAppName, LPCTSTR lpFileName);
	/**
	*解析ServerIP数据
	*/
	TArray<FString> AnalyzeServerIPData(LPCTSTR lpAppName, LPCTSTR lpFileName);
	/**
	*从文件读取服务器状态数据
	*/
	void RequestServerStateData();
	/**
	*读取成功
	*/
	UFUNCTION()
	void OnRequestServerStateDataSuccess(FString JsonString);
	/**
	*读取失败
	*/
	UFUNCTION()
	void OnRequestServerStateDataFail(FString JsonString);
	/**
	*从文件读取历史登录服务器数据
	*/
	void RequestServerRecordData();
	/**
	*解析历史登录服务器文件
	*/
	void AnalyzeServerRecordData(LPCTSTR lpAppName, LPCTSTR lpFileName);
	/**
	*写入历史登录服务器数据表
	*/
	void WriteServerRecordData(FString AccountName, FString RecordAccountStr, FString RecordServerStr);
	/**
	*更新历史登录服务器数据表
	*/
	void UpdateServerRecordDataToFile(FString AccountName);
	/**
	*增加历史登录服务器记录
	*/
	void AddServerRecord(FString AccountName, FName ServerName, FString ServerIP);

	/**
	*写入 是否记录账号数据 到本地数据表
	*/
	void WriteIsSaveAccountData(FString NewIsSaveAccount);
	/**
	*更新 是否记录账号数据
	*/
	void UpdateIsSaveAccountDataToFile(bool IsSaveAccount);

	/**
	*获取登录数据本地表文件路径
	*/
	FString GetLauncherRecordProfilePath();

public:
	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		FName CurrServerName;
	//游戏剩余时间
	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		int32 GameTimeBalance;
	//上次登录时间
	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		FString LastLoginTime;
	//本次登录时间
	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		FString LoginTime;

public:
	//当前输入的账户名（保存的登录界面输入）
	UPROPERTY(BlueprintReadOnly, Category = "LoginManager")
		FString InputAccountName;

private:
	UCS3HttpRequest* HttpRequest;

	TMap<int32, TArray<FSERVER_DATA>> ServerListDatas;//服务器数据，int32为服务器类型
	TArray<FSERVER_DATA> RecommentServerListData;
	TArray<FString> RecordAccountList;//账号记录列表，最新登录的在第一个
	TMap<FString, TArray<FString>> ServerRecordMap;//key:账号 Value:服务器key列表（最新登录的在第一个）

	TArray<FName> RecommentServerList;
	TArray<FName> NewServerList;

#pragma endregion
};
