#include "RoleCrossServiceInterface.h"
#include "JsonFieldData.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/LoginManager.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/CS3EntityInterface.h"
#include "CS3Base/CS3InterfaceDeclare.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/UIManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleCrossServiceInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestCrossServiceResult, &URoleCrossServiceInterface::CLIENT_OnRequestCrossServiceResult, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestReturnServerResult, &URoleCrossServiceInterface::CLIENT_OnRequestReturnServerResult, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRoleReEnterWorld, &URoleCrossServiceInterface::OnRoleReEnterWorld)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleCrossServiceInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleCrossServiceInterface::URoleCrossServiceInterface()
{
}


URoleCrossServiceInterface::~URoleCrossServiceInterface()
{
}

void URoleCrossServiceInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnRequestCrossServiceResult");
	ArrBlueFunc.Add("CLIENT_OnRequestReturnServerResult");
	ArrBlueFunc.Add("OnRoleReEnterWorld");

	Supper::InitBlueCB();
}

bool URoleCrossServiceInterface::Check(FSERVER_DATA CurrServerData, FSERVER_DATA TargetServerData)
{
	if (CurrServerData.ServerName == "" || CurrServerData.ServerName.ToString().Equals(TargetServerData.ServerName.ToString()))
	{
		return false;
	}
	else if (TargetServerData.ServerState == FSERVER_STATE::MAINTENANCE)
	{
		return false;
	}

	return true;
}

void URoleCrossServiceInterface::BeforeCrossService()
{

}

void URoleCrossServiceInterface::BeforeReturnServer()
{

}

void URoleCrossServiceInterface::RPC_RequestCrossService(FString TargetServerName)
{
	FName CurrServerName = UUECS3GameInstance::Instance->LoginManager->GetCurrServerName();
	FSERVER_DATA CurrServerData = UUECS3GameInstance::Instance->LoginManager->GetServerData(CurrServerName);
	FSERVER_DATA TargetServerData = UUECS3GameInstance::Instance->LoginManager->GetServerData(*TargetServerName);

	if (Check(CurrServerData, TargetServerData))
	{
		KBEngine::Entity* Entity = GetEntity();
		if (Entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleCrossServiceInterface::RPC_RequestCrossService: entity!"));
			return;
		}

		KBEngine::FVariantArray Args;
		Args.Add(CurrServerData.ServerKey);
		Args.Add(TargetServerData.ServerKey);

		Entity->BaseCall(TEXT("requestCrossService"), Args);
	}
}

void URoleCrossServiceInterface::CLIENT_OnRequestCrossServiceResult(const FString& Result)
{

	UJsonFieldData* JsonObject = UJsonFieldData::Create(this);
	auto ResultStr = JsonObject->FromString(Result);
	auto RootObject = ResultStr->GetObject(TEXT("ROOT"));
	FString ResultValue = RootObject->GetString(TEXT("result"));
	int8 ResultCode = _tstoi(*RootObject->GetString(TEXT("result_code")));
	if (ResultValue.Equals("SUCCESS"))
	{
		KBEngine::Entity* Entity = GetEntity();
		if (Entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleCrossServiceInterface::CLIENT_OnRequestCrossServiceResult: entity!"));
			return;
		}

		BeforeCrossService();

		KBEngine::FVariantArray Args;
		Entity->BaseCall(TEXT("startCrossService"), Args);
	}
	else
	{
		CS3_Warning(TEXT("URoleCrossServiceInterface::CLIENT_OnRequestCrossServiceResult: request cross service failed: %d"), ResultCode);
	}
}

void URoleCrossServiceInterface::RPC_RequestReturnServer()
{
	KBEngine::Entity* Entity = GetEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleCrossServiceInterface::RPC_RequestReturnServer: entity!"));
		return;
	}

	KBEngine::FVariantArray Args;

	Entity->BaseCall(TEXT("requestReturnServer"), Args);
}

void URoleCrossServiceInterface::CLIENT_OnRequestReturnServerResult(const FString& Result)
{
	UJsonFieldData* JsonObject = UJsonFieldData::Create(this);
	auto ResultStr = JsonObject->FromString(Result);
	auto RootObject = ResultStr->GetObject(TEXT("ROOT"));
	FString ResultValue = RootObject->GetString(TEXT("result"));
	int8 ResultCode = _tstoi(*RootObject->GetString(TEXT("result_code")));
	if (ResultValue.Equals("SUCCESS"))
	{
		KBEngine::Entity* Entity = GetEntity();
		if (Entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleCrossServiceInterface::CLIENT_OnRequestReturnServerResult: entity!"));
			return;
		}

		BeforeReturnServer();

		KBEngine::FVariantArray Args;
		Entity->BaseCall(TEXT("startReturnServer"), Args);
	}
	else
	{
		CS3_Warning(TEXT("URoleCrossServiceInterface::CLIENT_OnRequestReturnServerResult: request return server failed: %d"), ResultCode);
	}
}

void URoleCrossServiceInterface::OnRoleReEnterWorld()
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OnRoleEnterWorld();
	}
}
