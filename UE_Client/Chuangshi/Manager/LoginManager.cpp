// Fill out your copyright notice in the Description page of Project Settings.


#include "Manager/LoginManager.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"
#include "../Entity/Account/Account.h"
#include "../Entity/Role/CS3Role.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../Actor/ServerCharacter.h"
#include "../Actor/Player/LoginCharacter.h"
#include "LoaderManager.h"
#include "ResourceManager.h"
#include "CS3Base/UIManager.h"
#include "LevelManager.h"
#include "Chuangshi.h"
#include "GameStatus.h"
#include "LocalDataSaveManager.h"
#include "GameStatus.h"
#include "AutoTest/AutoTestManager.h"
#include "MediaPlayerManager.h"
#include "Level/LoginSelectLevel.h"
#include "GameData/CS3HttpRequest.h"
#include "GameData/GameDefault.h"

#include "AllowWindowsPlatformTypes.h"
//#include <wtypes.h>
#include <winbase.h>
#include "HideWindowsPlatformTypes.h"
#include "Util/ConvertUtil.h"
#include "Entity/Alias.h"
#include "JsonFieldData.h"
#include "JsonReader.h"
#include "JsonObject.h"
#include "JsonSerializer.h"
#include "CfgManager.h"
#include "GameData/GameDefault.h"
#include "PlatformFilemanager.h"
#include "GenericPlatformFile.h"

CONTROL_COMPILE_OPTIMIZE_START

ULoginManager::ULoginManager()
{
	bIsFirstEnterWorld = true;
}

ULoginManager::~ULoginManager()
{

}

ULoginManager* ULoginManager::GetInstance()
{
	cs3_checkNoReentry();

	return (ULoginManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_LoginManager")));
}

void ULoginManager::BeginDestroy()
{
	Super::BeginDestroy();
}

void ULoginManager::Init()
{
	RequestServerRecordData();
	if (UUECS3GameInstance::Instance->GameDefault->IsChangeServer)
	{
		RequestServerListData();
	}
}

void ULoginManager::CS3Login(FString ServerName, FString server, FString account, FString password, FString szMsg, bool IsSaveAccount/* = true*/)
{
	if (currLoginStage== ELoginStage::StageTryLogin)return;
	//设置登录状态
	SetLoginStage(ELoginStage::StageTryLogin);
	//设置当前账号和服务器
	CurrAccountName = account;
	ChangeServer(FSTRING_TO_FNAME(ServerName));
	if (IsSaveAccount)
	{
		//增加登录记录（包含更新是否记录账号）
		AddServerRecord(CurrAccountName, CurrServerName, server);
	}
	else
	{
		//更新是否记录账号
		UpdateIsSaveAccountDataToFile(IsSaveAccount);
	}
	//请求服务器
	TArray<uint8> datasist;
	datasist.SetNum(szMsg.Len());
	memcpy(datasist.GetData(), TCHAR_TO_ANSI(*szMsg), szMsg.Len());
	NotifyServerLogin(server, account, password, datasist);
}

void ULoginManager::OnLoginBaseapp()
{
	///这个地方登录游戏
	if (GetRoleInfos().Num() > 0)
	{
		UGolbalBPFunctionLibrary::LevelManager()->TeleportSelectRoleLevel();
	}
	else
	{
		CurLevelScriptActor->PlayCG();
	}
}


void ULoginManager::CS3Logoff()
{
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player) 
	{ 
		CS3_Warning(TEXT("-->Null Pointer error:ULoginManager::CS3Logoff : player!"));
		return; 
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (pEntity_Player->IsPlayerAccount())
	{
		Account *account = (Account*)(pEntity_Player);
		account->Logoff();
	}
	else
	{
		CS3Role* role = (CS3Role*)(pEntity_Player);
		role->Logoff();
	}
}

void ULoginManager::CS3Logout()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT(" ------------UUECS3GameInstance::CS3Logout: -------------------- "));

	if (!UUECS3GameInstance::Instance)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ULoginManager::CS3Logout : UUECS3GameInstance::Instance!"));
		return;
	}

	if (UUECS3GameInstance::Instance->GameStatus && UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::InWorld))
	{
		KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
		if (entity != nullptr)
		{
			CS3Entity* pEntity_Player = (CS3Entity*)(entity);
			if (pEntity_Player->IsPlayerRole())
			{
				CS3Role *role = (CS3Role *)entity;
				role->Logout();
				///改变进入游戏的模式为选人进入
				UUECS3GameInstance::Instance->GameDefault->IsEnterGame = false;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT(" ------------UUECS3GameInstance::CS3Logout: current state is not in game"));
	}

	//停止自动化测试
	if (UUECS3GameInstance::Instance->AutoTestManager)
	{
		if (UUECS3GameInstance::Instance->AutoTestManager->bIsStartFMO && (!UUECS3GameInstance::Instance->GameDefault->bContinueHandleAT))
		{
			UUECS3GameInstance::Instance->AutoTestManager->StopFMO();
		}
	}
}

void ULoginManager::EnterGame(FString dbid)
{

	GEngine->RedrawViewports(false);
	CurrLoginDBID = dbid;
	KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
	if (entity != nullptr)
	{
		CS3Entity* pEntity_Player = (CS3Entity*)(entity);
		if (pEntity_Player->IsPlayerAccount())
		{
			Account *account = (Account *)entity;
			account->EnterGame(uint64(FSTRING_TO_INT64(dbid)));
		}
	}
}


void ULoginManager::OnDisconnect()
{	
	SetLoginStage(ELoginStage::StageNoLogin);
	bIsLoginStatus = false;
	//停止自动化测试
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->AutoTestManager)
	{
		if (UUECS3GameInstance::Instance->AutoTestManager->bIsStartFMO && (!UUECS3GameInstance::Instance->GameDefault->bContinueHandleAT))
		{
			UUECS3GameInstance::Instance->AutoTestManager->StopFMO();
		}
	}
	
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->GameStatus && !UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UUECS3GameInstance::Instance->GUIManager->HideVSWindows();
		}
		if (IsValid(UGolbalBPFunctionLibrary::LevelManager()))
		{
			UGolbalBPFunctionLibrary::LevelManager()->TeleportLoginLevel();
		}
	}
}

void ULoginManager::OnDisconnectLoad()
{
}

void ULoginManager::OnLoginSucceed(AliasRoleInfoTmap& inst)
{
	bIsLoginStatus = true;
	CurLevelScriptActor->UpdateSelectWndAndModel(inst);
	CS3_Warning(TEXT("LoginManager::OnLoginSucceed:-----------"));
}

void ULoginManager::SetRoleInfos(AliasRoleInfoTmap& inst)
{
	UUECS3GameInstance::Instance->LoginManager->roleInfos = inst.infos;
	CS3_Warning(TEXT("UUECS3GameInstance::SetRoleInfos: ------------"));
}

TArray<FROLEINFO> ULoginManager::GetRoleInfos()
{
	TArray<FROLEINFO> fRoleInfos;
	for (auto info : roleInfos)
	{
		char str[100];
		sprintf_s(str, "====%I64d", info.DBid);
		GEngine->AddOnScreenDebugMessage(-1, 1.0f, FColor::Blue, str);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------GetRoleInfos----%d,%s,%d--------------\n"), (int64)info.DBid, *(info.PlayerName), info.Level);
		FROLEINFO finfo;
		finfo.dbid = INT64_TO_FSTRING(info.DBid);
		finfo.playerName = info.PlayerName;
		finfo.level = (int32)info.Level;
		finfo.profession = info.Profession;
		finfo.camp = info.Camp;
		finfo.gender = info.Gender;
		finfo.offlineTime = INT64_TO_FSTRING(info.OfflineTime);
		//导入脸部骨骼数据
		for (FaceInfo facedatas : info.faceModel.infolist)
		{
			finfo.bonedatas.Add(facedatas.boneData);
			finfo.bonenames.Add(facedatas.boneName);
		}
		//导入脸部样式数据
		finfo.facestyledata.ChunZhuangIndex = info.faceStyle.ChunzhuangIndex;
		finfo.facestyledata.ChunZhuangShape = FSTRING_TO_FLOAT(info.faceStyle.ChunzhuangShape);
		finfo.facestyledata.HuXuIndex = info.faceStyle.HuXuIndex;
		finfo.facestyledata.LianWenIndex = info.faceStyle.LianWenIndex;
		finfo.facestyledata.MeiMaoIndex = info.faceStyle.MeiMaoIndex;
		finfo.facestyledata.MeiMaoShape = FSTRING_TO_FLOAT(info.faceStyle.MeiMaoShape);
		finfo.facestyledata.YanXianIndex = info.faceStyle.YanXianIndex;
		finfo.facestyledata.SaiHongIndex = info.faceStyle.SaiHongIndex;
		finfo.facestyledata.SaiHongShape = FSTRING_TO_FLOAT(info.faceStyle.SaiHongShape);
		finfo.facestyledata.YanYingIndex = info.faceStyle.YanYingIndex;
		finfo.facestyledata.YanYingShape = FSTRING_TO_FLOAT(info.faceStyle.YanYingShape);
		finfo.facestyledata.Brighjtness = FSTRING_TO_FLOAT(info.faceStyle.Brightness);
		finfo.facestyledata.ColorDepth = FSTRING_TO_FLOAT(info.faceStyle.ColorDepth);
		finfo.facestyledata.EyeIndex = info.faceStyle.EyeIndex;
		finfo.facestyledata.EyeScale = FSTRING_TO_FLOAT(info.faceStyle.EyeScale);

		fRoleInfos.Add(finfo);
	}
	return fRoleInfos;
}

bool ULoginManager::GetRoleInfo(const FString& dbid, FROLEINFO& roleInfo)
{
	TArray<FROLEINFO> RoleInfoArray = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos();
	FROLEINFO* pRoleInfo = RoleInfoArray.FindByPredicate([dbid](FROLEINFO info) { return info.dbid == dbid; });
	if (pRoleInfo)
	{
		roleInfo = *pRoleInfo;
		return true;
	}
	else
	{
		return false;
	}
}

AliasRoleInfo* ULoginManager::GetARoleInfo(const FString& PlayerName)
{
	for (AliasRoleInfo& info : roleInfos)
	{
		if (info.PlayerName == PlayerName)
		{
			return &info;
		}
	}
	return nullptr;
}


void ULoginManager::NotifyServerLogin(FString server, FString account, FString password, TArray<uint8> datas)
{
	KBEngine::KBEngineArgs *args = new KBEngine::KBEngineArgs();

	TArray<FString> ServerArray = UGolbalBPFunctionLibrary::SplitString(server, false, ":");
	if (ServerArray.Num() == 2)
	{
		args->host = ServerArray[0];
		args->port = FSTRING_TO_INT(ServerArray[1]);
	}
	else
	{
		args->host = server;
		args->port = 20013;
	}
	args->clientType = KBEngine::CLIENT_TYPE::CLIENT_TYPE_MINI;

	args->persistentDataPath = "Application.PersistentDataPath";

	args->syncPlayer = true;
	args->useAliasEntityID = true;
	args->isOnInitCallPropertysSetMethods = true;

	args->SEND_BUFFER_MAX = 32768;
	args->RECV_BUFFER_MAX = 262142;
	if (UUECS3GameInstance::pKBEApp)
	{
		delete UUECS3GameInstance::pKBEApp;
		UUECS3GameInstance::pKBEApp = nullptr;
	}
	UUECS3GameInstance::pKBEApp = new KBEngine::KBEngineApp(args);

	UUECS3GameInstance::pKBEApp->Login(account, password, datas);
}

void ULoginManager::OnTryLoginTimeOut()
{
	if (currLoginStage == ELoginStage::StageTryLogin)
	{
		SetLoginStage(ELoginStage::StageNoLogin);
	}
	if (TryLoginHander.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TryLoginHander);
	}
}

bool ULoginManager::SelectRole_Implementation(AActor* Role)
{
	return false;
}

void ULoginManager::SetLoginStage(ELoginStage inLoginStage)
{
	currLoginStage = inLoginStage;
	OnLoginStageChange(inLoginStage);
}

ELoginStage ULoginManager::GetLoginStage()
{
	return currLoginStage;
}

void ULoginManager::OnLoginStageChange(ELoginStage newLoginStage)
{
	if (newLoginStage == ELoginStage::StageTryLogin)
	{		
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TryLoginHander, this, &ULoginManager::OnTryLoginTimeOut, 5.0f, false);
	}
	else if (newLoginStage == ELoginStage::StageAccountLogin)
	{
		if (TryLoginHander.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TryLoginHander);
		}
	}
	else if (newLoginStage == ELoginStage::StageRoleLogin)
	{
		UGUIManager* GUIManager = UUECS3GameInstance::Instance->GUIManager;
		if (GUIManager)
		{
			GUIManager->PreCreateWindows();
		}

	}
	else if (newLoginStage == ELoginStage::StageNoLogin)
	{

	}
}

void ULoginManager::SetLoginAccountInfo(int32 BalanceVal, FString LastTime, FString Time) {

	GameTimeBalance = BalanceVal;
	LastLoginTime = LastTime;
	LoginTime = Time;
}

#pragma region	/** 服务器列表 */
TArray<FSERVER_DATA> ULoginManager::GetAllServerListData()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------LoginManager::GetAllServerListData--------"));
	TArray<FSERVER_DATA> ServerList;
	for (TPair<int32, TArray<FSERVER_DATA>> Datas : ServerListDatas)
	{
		for (FSERVER_DATA Data : Datas.Value)
		{
			ServerList.Add(Data);
		}
	}
	return ServerList;
}

TArray<FSERVER_DATA> ULoginManager::GetServerListData(int32 ServerType)
{
	TArray<FSERVER_DATA> ServerList;
	if (ServerListDatas.Contains(ServerType))
	{
		ServerList =  ServerListDatas[ServerType];
	}
	return ServerList;
}

FSERVER_DATA ULoginManager::GetServerData(FName ServerName)
{
	for (TPair<int32, TArray<FSERVER_DATA>> Datas : ServerListDatas)
	{
		for (FSERVER_DATA Data : Datas.Value)
		{
			if (Data.ServerName == ServerName)
			{
				return Data;
			}
		}
	}
	CS3_Warning(TEXT("-->ULoginManager::GetServerData(%s) is Empty!"), *(FNAME_TO_FSTRING(ServerName)));
	return FSERVER_DATA();
}

FString ULoginManager::GetLoginServerIP()
{
	if (UUECS3GameInstance::Instance->GameDefault->IsChangeServer && CheckServerListNum())
	{
		FSERVER_DATA ServerData = GetServerData(CurrServerName);
		if (ServerData.ServerIP.Num() > 0)
		{
			int32 rand = FMath::RandRange(0, (ServerData.ServerIP.Num() - 1));
			return ServerData.ServerIP[rand];
		}
	}
	return UGolbalBPFunctionLibrary::GetServerIP();
}

TArray<FSERVER_DATA> ULoginManager::GetRecommentServerData()
{
	TArray<FSERVER_DATA> ServerList;
	for (TPair<int32, TArray<FSERVER_DATA>>& DataList : ServerListDatas)
	{
		for (FSERVER_DATA Data : DataList.Value)
		{
			if (RecommentServerList.Contains(Data.ServerName))
			{
				ServerList.Add(Data);
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("LoginManager::GetRecommentServerData---------------"));
			}
		}
	}
	return ServerList;
}

TArray<FSERVER_DATA> ULoginManager::GetRecordServerData()
{
	TArray<FSERVER_DATA> ServerList;
	if (ServerRecordMap.Contains(InputAccountName))
	{
		TArray<FString> ServerKeyList = ServerRecordMap[InputAccountName];
		if (ServerKeyList.Num() > 0)
		{
			for (FString ServerKey : ServerKeyList)
			{
				bool IsSuccess = false;
				FSERVER_DATA ServerData = GetServerDataByKey(ServerKey, IsSuccess);
				if (IsSuccess)
				{
					ServerList.Add(ServerData);
				}
			}
		}
	}
	return ServerList;
}

bool ULoginManager::IsRecommentServer(FName ServerName)
{
	if (RecommentServerList.Contains(ServerName))
	{
		return true;
	}
	return false;
}

bool ULoginManager::IsNewServer(FName ServerName)
{
	
	if (NewServerList.Contains(ServerName))
	{
		CS3_Display(CS3DebugType::CL_Login, TEXT("LoginManager::IsNewServer---------"));
		return true;
	}
	return false;
}

void ULoginManager::ChangeServer(FName ServerName)
{
	CS3_Display(CS3DebugType::CL_Login, TEXT("LoginManager::ChangeServer-------"));
	CurrServerName = ServerName;
}

FName ULoginManager::GetCurrServerName()
{
	return CurrServerName;
}

void ULoginManager::RequestServerListData()
{
	RecommentServerList.Empty();
	NewServerList.Empty();

	int MAX_LENGTH = 128;
	wchar_t serveridlist[128] = { 0 };
	FString ProfilePath;
#if WITH_EDITOR
	ProfilePath = FPaths::ProjectSavedDir() + TEXT("Config/Windows/svrlist.ini");
#else
	ProfilePath = FPaths::ProjectSavedDir() + TEXT("Config/WindowsNoEditor/svrlist.ini");
#endif
	ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
	LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));
	GetPrivateProfileString(TEXT("serverlist"), TEXT("serveridlist"), TEXT(""), serveridlist, MAX_LENGTH, FilePath);
	FString serveridlistStr(serveridlist);

	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(serveridlistStr, false, "|");
	for (FString str : SplitArray)
	{
		AnalyzeServerData(TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(str)), FilePath);
	}
	
	RequestServerStateData();
}

void ULoginManager::AnalyzeServerData(LPCTSTR lpAppName, LPCTSTR lpFileName)
{
	int MAX_LENGTH = 128;
	wchar_t LocalServerName[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("name"), TEXT(""), LocalServerName, MAX_LENGTH, lpFileName);
	FString ServerNameStr(LocalServerName);

	TArray<FString> ServerIP = AnalyzeServerIPData(lpAppName, lpFileName);

	wchar_t LocalServerType[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("type"), TEXT(""), LocalServerType, MAX_LENGTH, lpFileName);
	FString LocalServerTypeStr(LocalServerType);

	wchar_t LocalRecomment[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("recommend"), TEXT(""), LocalRecomment, MAX_LENGTH, lpFileName);
	FString LocalRecommentStr(LocalRecomment);

	wchar_t LocalNewServer[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("newServer"), TEXT(""), LocalNewServer, MAX_LENGTH, lpFileName);
	FString LocalNewServerStr(LocalNewServer);

	FSERVER_DATA ServerData;
	ServerData.ServerKey = lpAppName;
	ServerData.ServerType = FSTRING_TO_INT(LocalServerTypeStr);
	ServerData.ServerName = FSTRING_TO_FNAME(ServerNameStr);
	ServerData.ServerIP = ServerIP;
	ServerData.ServerState = FSERVER_STATE::VERY_GOOD;
	ServerData.IsRecomment = LocalRecommentStr == TEXT("1") ? true : false;
	ServerData.IsNewServer = LocalNewServerStr == TEXT("1") ? true : false;
	if (ServerData.IsRecomment)
	{
		RecommentServerList.Add(ServerData.ServerName);
	}
	if (ServerData.IsNewServer)
	{
		NewServerList.Add(ServerData.ServerName);
	}
	if (!ServerListDatas.Contains(ServerData.ServerType))
	{
		ServerListDatas.Add(ServerData.ServerType, {});
	}
	ServerListDatas[ServerData.ServerType].Add(ServerData);
}

TArray<FString> ULoginManager::AnalyzeServerIPData(LPCTSTR lpAppName, LPCTSTR lpFileName)
{
	int MAX_LENGTH = 128;
	TArray<FString> ServerIP;

	wchar_t loginlist[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("loginlist"), TEXT(""), loginlist, MAX_LENGTH, lpFileName);
	FString loginlistStr(loginlist);
	
	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(loginlistStr, false, "|");
	for (FString str : SplitArray)
	{
		wchar_t lpString[128] = { 0 };
		GetPrivateProfileString(lpAppName, TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(str)), TEXT(""), lpString, MAX_LENGTH, lpFileName);
		FString IPStr(lpString);
		ServerIP.Add(IPStr);
	}
	return ServerIP;
}

void ULoginManager::RequestServerStateData()
{
	FString URL = UUECS3GameInstance::Instance->GameDefault->ServerStateHostAndPort + TEXT("/serverStatus");
	//FString URL = TEXT("http://172.16.6.47:8080/serverStatus");
	HttpRequest = UCS3HttpRequest::GetHttpRequest(URL);
	HttpRequest->OnSuccess.AddDynamic(this, &ULoginManager::OnRequestServerStateDataSuccess);
	HttpRequest->OnFail.AddDynamic(this, &ULoginManager::OnRequestServerStateDataFail);
}

void ULoginManager::OnRequestServerStateDataSuccess(FString JsonString)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("RequestServerListData*********| %s |******* "), *JsonString);
	TArray<FSERVER_STATE_DATA> StateList;

	TSharedRef<TJsonReader<TCHAR>> JsonReader = TJsonReaderFactory<TCHAR>::Create(JsonString);
	TArray< TSharedPtr<FJsonValue> > Array;
	if (FJsonSerializer::Deserialize(JsonReader, Array))
	{
		for (auto dict : Array)
		{
			auto data = dict->AsObject();
			FSERVER_STATE_DATA StateData;
			StateData.ServerName = FSTRING_TO_FNAME(data->GetStringField(TEXT("ServerName")));
			bool ServerOpenState = data->GetBoolField(TEXT("ServerState"));
			if (ServerOpenState)
			{
				int32 RoleNum = data->GetIntegerField(TEXT("RoleNum"));
				int32 RoleMax = data->GetIntegerField(TEXT("RoleMax"));
				float Percent = (RoleMax == 0) ? 0 : (RoleNum / RoleMax);
				//爆满
				if (Percent > 0.5)
				{
					StateData.ServerState = FSERVER_STATE::FULL;
				}
				//繁忙
				else if (Percent >= 0.3)
				{
					StateData.ServerState = FSERVER_STATE::BUSY;
				}
				//良好
				else if (Percent >= 0.1)
				{
					StateData.ServerState = FSERVER_STATE::GOOD;
				}
				//极佳
				else
				{
					StateData.ServerState = FSERVER_STATE::VERY_GOOD;
				}
			}
			//服务器未开启
			else
			{
				//维护
				StateData.ServerState = FSERVER_STATE::MAINTENANCE;
			}
			StateList.Add(StateData);
		}
	}
	//更新状态
	if (StateList.Num() > 0)
	{
		for (TPair<int32, TArray<FSERVER_DATA>>& Datas : ServerListDatas)
		{
			for (FSERVER_DATA& Data : Datas.Value)
			{
				for (FSERVER_STATE_DATA ServerStateData : StateList)
				{
					if (Data.ServerName == ServerStateData.ServerName)
					{
						Data.ServerState = ServerStateData.ServerState;
						StateList.Remove(ServerStateData);
						break;
					}
				}
			}
		}
	}
}

void ULoginManager::OnRequestServerStateDataFail(FString JsonString)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ULoginManager::OnRequestServerStateDataFail,serverStatus Request Fail!!!!!!!!!"));
}

void ULoginManager::RequestServerRecordData()
{
	ServerRecordMap.Empty();
	RecordAccountList.Empty();

	int MAX_LENGTH = 128;
	wchar_t recordAccountlist[128] = { 0 };
	FString ProfilePath = GetLauncherRecordProfilePath();
	ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
	LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));

	GetPrivateProfileString(TEXT("Account"), TEXT("RecordAccount"), TEXT(""), recordAccountlist, MAX_LENGTH, FilePath);
	FString recordAccountlistStr(recordAccountlist);

	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(recordAccountlistStr, false, "|");
	for (FString str : SplitArray)
	{
		RecordAccountList.Add(str);
		FString lpAppNameStr = TEXT("AccountRecord_") + str;
		AnalyzeServerRecordData(TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(lpAppNameStr)), FilePath);
	}
}

void ULoginManager::AnalyzeServerRecordData(LPCTSTR lpAppName, LPCTSTR lpFileName)
{
	int MAX_LENGTH = 128;
	wchar_t LocalServerKeyList[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("Server"), TEXT(""), LocalServerKeyList, MAX_LENGTH, lpFileName);
	FString ServerKeyStr(LocalServerKeyList);

	wchar_t LocalAccountName[128] = { 0 };
	GetPrivateProfileString(lpAppName, TEXT("Name"), TEXT(""), LocalAccountName, MAX_LENGTH, lpFileName);
	FString LocalAccountNameStr(LocalAccountName);

	if (!ServerRecordMap.Contains(LocalAccountNameStr))
	{
		ServerRecordMap.Add(LocalAccountNameStr, {});
	}
	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(LocalServerKeyList, false, "|");
	for (FString ServerKey : SplitArray)
	{
		ServerRecordMap[LocalAccountNameStr].Add(ServerKey);
	}
}

void ULoginManager::WriteServerRecordData(FString AccountName, FString RecordAccountStr, FString RecordServerStr)
{
	FString ProfilePath = GetLauncherRecordProfilePath();
	ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
	LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));

	WritePrivateProfileString(TEXT("Account"), TEXT("RecordAccount"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(RecordAccountStr)), FilePath);

	//可能存在没有服务器数据的情况（从来没有使用登录器登录过）
	if (!RecordServerStr.Equals(TEXT("")))
	{
		FString lpAppNameStr = TEXT("AccountRecord_") + AccountName;
		WritePrivateProfileString(TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(lpAppNameStr)), TEXT("Server"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(RecordServerStr)), FilePath);
		WritePrivateProfileString(TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(lpAppNameStr)), TEXT("Name"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(AccountName)), FilePath);
		//密码暂时空的
		WritePrivateProfileString(TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(lpAppNameStr)), TEXT("Password"), TEXT(""), FilePath);
	}

	//如果本地表中 记录账号 为false，则更新本地表 记录账号 值
	int MAX_LENGTH = 128;
	wchar_t LocalIsSaveAccount[128] = { 0 };
	GetPrivateProfileString(TEXT("LauncherSetting"), TEXT("SaveAccount"), TEXT(""), LocalIsSaveAccount, MAX_LENGTH, FilePath);
	FString LocalIsSaveAccountStr(LocalIsSaveAccount);
	FString NewIsSaveAccountStr = TEXT("true");
	if (!LocalIsSaveAccountStr.Equals(NewIsSaveAccountStr))
	{
		WritePrivateProfileString(TEXT("LauncherSetting"), TEXT("SaveAccount"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(NewIsSaveAccountStr)), FilePath);
	}
}

void ULoginManager::UpdateServerRecordDataToFile(FString AccountName)
{
	FString RecordAccountStr = TEXT("");
	for (int32 i = 0; i < RecordAccountList.Num(); i++)
	{
		if (i == 0)
		{
			RecordAccountStr = RecordAccountList[i];
		}
		else
		{
			RecordAccountStr = RecordAccountStr + TEXT("|") + RecordAccountList[i];
		}
	}

	FString RecordServerStr = TEXT("");
	if (ServerRecordMap.Contains(AccountName))
	{
		TArray<FString> ServerList = ServerRecordMap[AccountName];
		for (int32 i = 0; i < ServerList.Num(); i++)
		{
			if (i == 0)
			{
				RecordServerStr = ServerList[i];
			}
			else
			{
				RecordServerStr = RecordServerStr + TEXT("|") + ServerList[i];
			}
		}
	}

	FString ProfilePath = GetLauncherRecordProfilePath();
	if (!FPaths::FileExists(ProfilePath))
	{
		IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
		IFileHandle* FileHandle = PlatformFile.OpenWrite(FSTRING_TO_TCHAR(ProfilePath));
		if (FileHandle)
		{
			delete FileHandle;
		}
	}
	WriteServerRecordData(AccountName, RecordAccountStr, RecordServerStr);
}

void ULoginManager::AddServerRecord(FString AccountName, FName ServerName, FString ServerIP)
{
	if (AccountName.Equals(TEXT("")))
	{
		return;
	}
	//已经有，则删掉，在加在最新
	if (RecordAccountList.Num() > 0 && RecordAccountList.Contains(AccountName))
	{
		RecordAccountList.Remove(AccountName);
	}
	//只保存5条账号记录
	if (RecordAccountList.Num() >= 5)
	{
		RecordAccountList.RemoveAt(RecordAccountList.Num() - 1);
	}
	RecordAccountList.Insert(AccountName, 0);

	FSERVER_DATA ServerData = GetServerData(ServerName);
	//可能存在没有服务器数据的情况（从来没有使用登录器登录过），ServerKey为空
	if (!ServerData.ServerKey.Equals(TEXT("")))
	{
		if (!ServerRecordMap.Contains(AccountName))
		{
			ServerRecordMap.Add(AccountName, {});
		}
		//已经有，则删掉，在加在最新
		if (ServerRecordMap[AccountName].Num() > 0 && ServerRecordMap[AccountName].Contains(ServerData.ServerKey))
		{
			ServerRecordMap[AccountName].Remove(ServerData.ServerKey);
		}
		//只保存3条服务器记录
		if (ServerRecordMap[AccountName].Num() >= 3)
		{
			ServerRecordMap[AccountName].RemoveAt(ServerRecordMap[AccountName].Num() - 1);
		}
		ServerRecordMap[AccountName].Insert(ServerData.ServerKey, 0);
	}

	UpdateServerRecordDataToFile(AccountName);

	//保存当前账号和ServerIP到LocalData本地表
	if (IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager->LocalData))
	{
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalData->UpdateLoginDataToFile(ServerIP, AccountName);
	}
}

void ULoginManager::WriteIsSaveAccountData(FString NewIsSaveAccount)
{
	FString ProfilePath = GetLauncherRecordProfilePath();
	ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
	LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));

	//如果本地表中 记录账号 为false，则更新本地表 记录账号 值
	int MAX_LENGTH = 128;
	wchar_t LocalIsSaveAccount[128] = { 0 };
	GetPrivateProfileString(TEXT("LauncherSetting"), TEXT("SaveAccount"), TEXT(""), LocalIsSaveAccount, MAX_LENGTH, FilePath);
	FString LocalIsSaveAccountStr(LocalIsSaveAccount);
	if (!LocalIsSaveAccountStr.Equals(NewIsSaveAccount))
	{
		WritePrivateProfileString(TEXT("LauncherSetting"), TEXT("SaveAccount"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(NewIsSaveAccount)), FilePath);
	}
}

void ULoginManager::UpdateIsSaveAccountDataToFile(bool IsSaveAccount)
{
	FString NewIsSaveAccountStr = IsSaveAccount == true ? TEXT("true") : TEXT("false");

	FString ProfilePath = GetLauncherRecordProfilePath();
	if (!FPaths::FileExists(ProfilePath))
	{
		IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
		IFileHandle* FileHandle = PlatformFile.OpenWrite(FSTRING_TO_TCHAR(ProfilePath));
		if (FileHandle)
		{
			delete FileHandle;
		}
	}
	WriteIsSaveAccountData(NewIsSaveAccountStr);
}

FString ULoginManager::GetLauncherRecordProfilePath()
{
#if WITH_EDITOR
	return FPaths::ProjectSavedDir() + TEXT("Config/Windows/launcherRecord.ini");
#else
	return FPaths::ProjectSavedDir() + TEXT("Config/WindowsNoEditor/launcherRecord.ini");
#endif
}

void ULoginManager::InitCurrServer()
{
 	if (ServerRecordMap.Contains(InputAccountName))
	{
		TArray<FString> ServerKeyList = ServerRecordMap[InputAccountName];
		//上次登录的
		if (ServerKeyList.Num() > 0)
		{
			//上次登录的
			bool IsSuccess = false;
			FSERVER_DATA ServerData = GetServerDataByKey(ServerKeyList[0], IsSuccess);
			if (IsSuccess)
			{
				ChangeServer(ServerData.ServerName);
			}
		}
	}
	//如果从没有登录过
	else
	{
		if (RecommentServerListData.Num() > 0)
		{
			//如果有推荐的服务器，则默认第一个推荐
			ChangeServer(RecommentServerListData[0].ServerName);
		}
		else
		{
			//如果没有推荐的，则默认第一个服务器
			for (TPair<int32, TArray<FSERVER_DATA>>& Datas : ServerListDatas)
			{
				if (Datas.Value.Num() > 0)
				{
					ChangeServer(Datas.Value[0].ServerName);
					break;
				}
			}
		}
	}
}

void ULoginManager::ChangeInputAccountName(FString InAccountName)
{
	InputAccountName = InAccountName;
}

FSERVER_DATA ULoginManager::GetServerDataByKey(FString ServerKey, bool& IsSuccess)
{
	for (TPair<int32, TArray<FSERVER_DATA>>& Datas : ServerListDatas)
	{
		for (FSERVER_DATA& Data : Datas.Value)
		{
			if (Data.ServerKey == ServerKey)
			{
				IsSuccess = true;
				return Data;
			}
		}
	}
	CS3_Warning(TEXT("-->ULoginManager::GetServerDataByKey(%s) is Empty!"), *ServerKey);
	IsSuccess = false;
	return FSERVER_DATA();
}

bool ULoginManager::CheckServerListNum()
{
	if (ServerListDatas.Num() > 0)
	{
		return true;
	}
	return false;
}

bool ULoginManager::IsSaveAccount()
{
	FString ProfilePath = GetLauncherRecordProfilePath();
	if (FPaths::FileExists(ProfilePath))
	{
		ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
		LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));

		int MAX_LENGTH = 128;
		wchar_t LocalIsSaveAccount[128] = { 0 };
		GetPrivateProfileString(TEXT("LauncherSetting"), TEXT("SaveAccount"), TEXT(""), LocalIsSaveAccount, MAX_LENGTH, FilePath);
		FString LocalIsSaveAccountStr(LocalIsSaveAccount);

		if (LocalIsSaveAccountStr.Equals(TEXT("true")))
		{
			return true;
		}
		return false;
	}
	return true;
}

#pragma endregion

void ULoginManager::CS3CancelLoginQueue()
{
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ULoginManager::CS3CancelLoginQueue : player!"));
		return;
	}

	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (pEntity_Player->IsPlayerAccount())
	{
		Account *account = (Account*)(pEntity_Player);
		account->CancelLoginQueue();
	}
	else
	{
		CS3_Warning(TEXT("-->Null Pointer error:ULoginManager::CS3CancelLoginQueue : is role!"));
		return;
	}
}

CONTROL_COMPILE_OPTIMIZE_END