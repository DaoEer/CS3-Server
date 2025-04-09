// Fill out your copyright notice in the Description page of Project Settings.


#include "StatusMessageInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/MessageManager.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UStatusMessageInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UStatusMessageInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
UStatusMessageInterface::UStatusMessageInterface()
{

}

UStatusMessageInterface::~UStatusMessageInterface()
{

}

void UStatusMessageInterface::statusMessage_Implementation(const int32& statusID, const FString& args)
{
	//根据传入的ID以及参数，取出提示消息并填充参数进行界面输出
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(statusID, args);
}


void UStatusMessageInterface::HideStatusMessage_Implementation(const int32& statusID)
{
	//根据传入的ID 隐藏消息
	UUECS3GameInstance::Instance->MessageManager->HideMessage(statusID);
}

void UStatusMessageInterface::inquireMessage_Implementation(const int32 & statusID, const FString & args, const int32 Key, const FString& Compotent)
{
	//服务器与客户端交互，用于点击按钮自动回应服务器的消息，不需要客户端点击按钮绑定事件通知
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(statusID, args, nullptr, Key, Compotent);
}

FString UStatusMessageInterface::GetReplaceMessage(const FString& replaceMessage, const FString args /*= TEXT("")*/, FString SplitChar /*= TEXT("|")*/)
{
	//把提示信息中的参数用传入的参数进行填充
	FString MsgArgs = args;
	TArray<FStringFormatArg> ArgsArray;
	FString left, right;
	bool result = true;
	while (!MsgArgs.IsEmpty())
	{
		result = MsgArgs.Split(SplitChar, &left, &right, ESearchCase::Type::CaseSensitive);
		if (result)
		{
			MsgArgs = right;
			ArgsArray.Add(left);
		}
		else
		{
			ArgsArray.Add(MsgArgs);
			MsgArgs = TEXT("");
		}
	}
	FString infoMessage;
	if (ArgsArray.Num() > 0)
		infoMessage = FString::Format(*replaceMessage, ArgsArray);
	else
		infoMessage = replaceMessage;
	return infoMessage;
}

void UStatusMessageInterface::RPC_Base_replyMessage(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStatusMessageInterface::RPC_Base_replyMessage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->BaseCall(TEXT("replyMessage"), args);
}

void UStatusMessageInterface::RPC_Cell_replyMessage(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStatusMessageInterface::RPC_Cell_replyMessage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("replyMessage"), args);
}


void UStatusMessageInterface::InitBlueCB()
{
	ArrBlueFunc.Add("statusMessage"); 
	ArrBlueFunc.Add("HideStatusMessage");
	ArrBlueFunc.Add("inquireMessage");
	ArrBlueFunc.Add("ShowCountDown");
	ArrBlueFunc.Add("ShowSpaceCopyIntroduction");
	Supper::InitBlueCB();
}
