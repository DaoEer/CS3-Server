
#include "Account.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"
#include "Manager/LoginManager.h"
#include "Manager/MessageManager.h"
#include "GameDevelop/CS3GameInstance.h"

KBE_BEGIN_ENTITY_METHOD_MAP(Account, Supper)
	DECLARE_REMOTE_METHOD(RequestInitRolesCB, &Account::RequestInitRolesCB, const FVariant&)
	DECLARE_REMOTE_METHOD(AddRoleCB, &Account::AddRoleCB, const FVariant&)
	DECLARE_REMOTE_METHOD(DeleteRoleCB, &Account::DeleteRoleCB, uint64)
	DECLARE_REMOTE_METHOD(AccountCreateCB, &Account::AccountCreateCB)
	DECLARE_REMOTE_METHOD(TimeSynchronization, &Account::TimeSynchronization, FString&)
	DECLARE_REMOTE_METHOD(OnStatusMessageCB,&Account::OnStatusMessageCB,const int32&,const FString&)
	DECLARE_REMOTE_METHOD(CreateRoleCallback, &Account::CreateRoleCallback)
	DECLARE_REMOTE_METHOD(ReceiveWattingInfo, &Account::ReceiveWattingInfo, const int32&, const float&, const int32&)
	DECLARE_REMOTE_METHOD(OnCancelLoginQueue, &Account::OnCancelLoginQueue, const int32&)
	DECLARE_REMOTE_METHOD(SetAccountInfo, &Account::SetAccountInfo, const FVariant&)
	DECLARE_REMOTE_METHOD(GameTimeHasUsedUp, &Account::GameTimeHasUsedUp)
	DECLARE_REMOTE_METHOD(RoleFrozenNotification, &Account::RoleFrozenNotification, const FString&)
	DECLARE_REMOTE_METHOD(onActivationKeyResult, &Account::onActivationKeyResult, const int8&)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(Account, Supper)
	DECLARE_PROPERTY_CHANGED_NOTIFY(vector2Value, &Account::set_vector2Value, FVector2D)
	DECLARE_PROPERTY_CHANGED_NOTIFY(vectorValue, &Account::set_vector3Value, FVector)
KBE_END_ENTITY_PROPERTY_MAP()

CONTROL_COMPILE_OPTIMIZE_START

Account::Account()
{
	
}


Account::~Account()
{
}


void Account::RequestInitRolesCB(const FVariant& val)
{
	AliasRoleInfoTmap inst;
	AliasRoleInfoTmap::CreateFromVariant(val, inst);
	CS3_Warning(TEXT("Account::RequestInitRolesCB: %s"), *inst.ToString());
	UUECS3GameInstance::Instance->LoginManager->SetLoginStage(ELoginStage::StageAccountLogin);
	//更新角色选择界面并创建角色模型
	UUECS3GameInstance::Instance->LoginManager->OnLoginSucceed(inst);
}

void Account::AccountCreateCB()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("requestInitRoles"), args);
}

void Account::SetAccountInfo(const FVariant& val)
{
	AliasAccountInfo AccountInfoInst;
	AliasAccountInfo::CreateFromVariant(val, AccountInfoInst);
	int32 GameTimeBalance = AccountInfoInst.GameTimeBalance;
	FString LastLoginTime = AccountInfoInst.LastLoginTime;
	FString LoginTime = AccountInfoInst.LoginTime;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->LoginManager))
	{
		UUECS3GameInstance::Instance->LoginManager->SetLoginAccountInfo(GameTimeBalance, LastLoginTime, LoginTime);
	}
}

void Account::GameTimeHasUsedUp()
{
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(5594);
	EntityCallEnable(true);
}

void Account::TimeSynchronization(FString& ServerTime)
{
	if (UUECS3GameInstance::Instance)
	{
		UUECS3GameInstance::Instance->TimeSynchronization(ServerTime);
	}
	else
	{
		CS3_Warning(TEXT("time synch err!!UUECS3GameInstance::Instance == nullptr "));
	}
}

void Account::AddRole(FString playerName, int32 profession, int32 camp, int32 gender)
{
	KBEngine::FVariantArray args;
	args.Add(playerName);
	args.Add(profession);
	args.Add(camp);
	args.Add(gender);
	BaseCall(TEXT("createRole"), args);
}
void Account::AddRoleCB(const FVariant& val)
{
	AliasRoleInfo inst;
	AliasRoleInfo::CreateFromVariant(val, inst);
	CS3_Warning(TEXT("Account::AddRoleCB: %s"), *inst.ToString());
	UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor->AddRoleInfo(inst);
	//UUECS3GameInstance::Instance->LoginManager->OnCreateRoleSuccess(INT64_TO_FSTRING(inst.DBid));
	UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor->OnAddAccount(inst.DBid);
}

void Account::DeleteRole(uint64 dbid)
{
	KBEngine::FVariantArray args;
	args.Add(dbid);
	CS3_Warning(TEXT("Account::DeleteRole: %d"), dbid);
	BaseCall(TEXT("deleteRole"), args);
}
void Account::DeleteRoleCB(uint64 dbid)
{
	//dbid = (int32)dbid;
	CS3_Warning(TEXT("Account::DeleteRoleCB: %d"), dbid);
	UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor->DelRoleInfo(dbid);
	UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor->OnDelAccount(dbid);
}

void Account::EnterGame(uint64 dbid)
{
	FString MacAddr = FGenericPlatformMisc::GetMacAddressString();
	KBEngine::FVariantArray args;
	args.Add(dbid);
	args.Add(MacAddr);
	CS3_Warning(TEXT("Account::EnterGame: %d"), dbid);
	BaseCall(TEXT("login"), args);
	EntityCallEnable(false); //关闭account继续给服务器发送消息的通道
}

void Account::Logoff()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("logoff"), args);
}

void Account::RoleFrozenNotification(const FString& EndTime)
{
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(5852, EndTime, FBtnClick::CreateLambda([](RT_BTN_TYPE RtType) {}));
	EntityCallEnable(true);
}

void Account::OnStatusMessageCB(const int32& statusID, const FString& args)
{
	//根据传入的ID以及参数，取出提示消息并填充参数进行界面输出
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(statusID, args);
	/*FString messageInfo = UUECS3GameInstance::Instance->StatusMessageManager->getStatusMessage(statusID, args);
	UUECS3GameInstance::Instance->ShowMessageBox(messageInfo);*/
}

void Account::ReceiveWattingInfo(const int32& rank, const float& time, const int32& count)
{
	UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor->ReceiveWattingInfo(rank, time, count);
	EntityCallEnable(true); //因玩家进入排队状态所以开启account继续给服务器发送消息的通道
}

void Account::set_vector2Value(const FVector2D &nv, const FVector2D &ov)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Account::set_vector2Value(), new value (%f, %f), old value (%f, %f)"), nv.X, nv.Y, ov.X, ov.Y);
}

void Account::set_vector3Value(const FVector &nv, const FVector &ov)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Account::set_vector3Value(), new value (%f, %f, %f), old value (%f, %f, %f)"), nv.X, nv.Y, nv.Z, ov.X, ov.Y, ov.Z);
}

void Account::CreateRoleCallback()
{
	UUECS3GameInstance::Instance->LoginManager->OnCreateRoleCallback();
}

void Account::setModifyFaceData(FaceInfoList& faceinfolist, FaceStyle& facestyleinfo, ModelList& modelList)
{
	KBEngine::FVariantMap faceModel, faceStyle,modellist;
	//KBEngine::FVariantMap faceStyle;
	KBEngine::FVariantArray args;
	faceinfolist.ToFVariantMap(faceModel);
	facestyleinfo.ToFVariantMap(faceStyle);
	modelList.ToFVariantMap(modellist);
	args.Add(faceModel);
	args.Add(faceStyle);
	args.Add(modellist);
	BaseCall(TEXT("modifyFace"), args);

}

void Account::RequestActivationKey(const FString& key, const FString& playerName)
{
	KBEngine::FVariantArray args;
	args.Add(key);
	args.Add(playerName);
	BaseCall("requestActivationKey", args);
}

void Account::onActivationKeyResult(const int8& result)
{
	if (result == 1)
	{
		UUECS3GameInstance::Instance->GEventManager->OnExchangeGiftSuccesd.Broadcast();
	}
}

void Account::CancelLoginQueue()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("reqCancelLoginQueue"), args);
}

void Account::OnCancelLoginQueue(const int32& isInQueue)
{
	UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor->OnCancelLoginQueue(isInQueue);
}

CONTROL_COMPILE_OPTIMIZE_END
