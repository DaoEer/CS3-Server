
#include "CSOLPersonality.h"
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/UIDataDefine.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include "Manager/LoginManager.h"
#include "CS3Base/UIManager.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/BaseWindow.h"
#include "Manager/MessageManager.h"
#include "Manager/AudioManager.h"


void CSOLPersonality::OnSetSpaceData(uint32 spaceID, const FString &key, const FString &value)
{
	CS3_Warning(TEXT("CSOLPersonality::OnSetSpaceData: spaceID: %u, key: %s, value: %s"), spaceID, *key, *value);	
	URoleSpaceInterface * Interface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), 0));
	if (IsValid(Interface))
	{
		Interface->OnSetSpaceData(spaceID, key, value);
	}
}

void CSOLPersonality::OnDelSpaceData(uint32 spaceID, const FString &key)
{
	CS3_Warning(TEXT("CSOLPersonality::OnDelSpaceData: spaceID: %u, key: %s"), spaceID, *key);
}

void CSOLPersonality::OnAddSpaceGeometryMapping(uint32 spaceID, const FString &respath)
{
	CS3_Warning(TEXT("CSOLPersonality::OnAddSpaceGeometryMapping: spaceID: %u, key: %s"), spaceID, *respath);
}

void CSOLPersonality::OnDisconnect()
{
	CS3_Warning(TEXT("CSOLPersonality::OnDisconnect: "));

	if (IsValid(UUECS3GameInstance::Instance->LoginManager))
	{
		UUECS3GameInstance::Instance->LoginManager->OnDisconnect();
	}
}

void CSOLPersonality::OnLoginFailed(int32 errCode, const FString& errName, const FString& errDesc, const TArray<uint8>& serverDatas)
{
	CS3_Warning(TEXT("CSOLPersonality::OnLoginFailed: code: %d, name: %s, desc:%s "), errCode, *errName, *errDesc);
	UDialogMessage* msg = NewObject<UDialogMessage>();
	msg->Message = errDesc;
	
	// 这个错误ID特殊处理一下
	// CST-2265 游戏功能——封锁账号功能的支持
	// 上述事务中，需要在相应的消息提示中增加一个截止时间，而此截止时间只能通过额外参数进行传递
	FString arg;
	if (errCode == 27)
	{
		auto data = std::string((const char *)&serverDatas[0], serverDatas.Num());
		arg = STDSTRING_TO_FSTRING(data);
	}
	//播放错误音效1
	if (IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		UUECS3GameInstance::Instance->AudioManager->PlaySoundUI(TEXT("other010109"));
	}
	
	//登录失败报错
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(4000 + errCode, arg, FBtnClick::CreateLambda([](RT_BTN_TYPE RtType)
	{
		//登录失败报错的回调函数
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UBaseWindow* LoginWin = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("Login"));
			if (IsValid(LoginWin))
			{
				LoginWin->OnFailedLogin();
			}
		}
	}));
	
}