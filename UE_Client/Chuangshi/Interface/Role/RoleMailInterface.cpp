
#include "RoleMailInterface.h"
#include "KBEngine.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "GameData/Item/ItemFactory.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/GameDeFine.h"
#include "Util/ConvertUtil.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleMailInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ReceiveMail, &URoleMailInterface::ReceiveMail, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ReceiveAllMail, &URoleMailInterface::ReceiveAllMail, const FVariantArray&,const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnMailDeleted, &URoleMailInterface::OnMailDeleted, const FVariantArray&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleMailInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleMailInterface::URoleMailInterface()
{

}

URoleMailInterface::~URoleMailInterface()
{

}

void URoleMailInterface::ReceiveMail(const FVariant& MailDataVar)
{

	FMailData mailData = AddOneMailData(MailDataVar);

	ReceiveMailBP(mailData.Id);
}

FMailData URoleMailInterface::AddOneMailData(const FVariant& MailDataVar)
{
	MAIL_DATA tempMailData = MAIL_DATA(MailDataVar);
	FMailData mailData;
	char charId[21];
	sprintf_s(charId, "%llu", tempMailData.id);
	mailData.Id = charId;
	mailData.Title = tempMailData.title;
	mailData.Content = tempMailData.content;
	mailData.Money = tempMailData.money;
	mailData.SenderName = tempMailData.senderName;
	mailData.ReceiverName = tempMailData.receiverName;
	mailData.IsTaken = tempMailData.isTaken;
	char charReceiveTime[21];
	sprintf_s(charReceiveTime, "%llu", tempMailData.receiveTime);
	mailData.ReceiveTime = charReceiveTime;
	mailData.RemainTime = tempMailData.remainTime;
	mailData.SenderType = MAIL_SEND_TYPE(tempMailData.senderType);
	mailData.IsRead = (tempMailData.isRead == 1);
	mailData.LingShi = tempMailData.lingshi;
	mailData.XianShi = tempMailData.xianshi;
	mailData.BindMoney = tempMailData.bindMoney;
	for (auto item : tempMailData.itemList)
	{
		int32 itemID = item.id;
		int32 amount = item.amount;
		int32 bindtype = item.bindType;
		char charUid[21];
		sprintf_s(charUid, "%llu", item.uid);
		FString uid = charUid;
		UItemBase* itembase = UItemFactory::GetItemByID(itemID);
		if (!IsValid(itembase))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::AddOneMailData : itembase!"));
			return mailData;
		}
		itembase->UID = uid;
		itembase->Amount = amount;
		itembase->BindType = bindtype;
		itembase->InitDynamicDataForJson(item.dynamicData);
		mailData.ItemList.Add(itembase);
	}

	MailMap.Add(mailData.Id, mailData);
	MailMap.ValueSort([](const FMailData& mailDataA, const FMailData& mailDataB) { return FSTRING_TO_INT64(mailDataA.ReceiveTime) > FSTRING_TO_INT64(mailDataB.ReceiveTime); });
	FTimerHandle tempTimer;
	TWeakObjectPtr<URoleMailInterface> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, tempTimer, FTimerDelegate::CreateLambda([DelayThisPtr, mailData]()
	{
		if (DelayThisPtr.IsValid())
		{
			URoleMailInterface* ThisPtr = DelayThisPtr.Get();
			if (ThisPtr->MailMap.Contains(mailData.Id))
			{
				ThisPtr->BASE_TimeToDelMail(mailData.Id);
			}
		}
	}), mailData.RemainTime, false);

	return mailData;
}

void URoleMailInterface::ReceiveMailBP_Implementation(const FString& mailId)
{

}


void URoleMailInterface::ReceiveAllMail(const FVariantArray& varRecordNames, const FVariantArray& AllMailData)
{
	TArray<FString> recordNames;
	for (auto VarRecordName : varRecordNames)
	{
		FString Name = VarRecordName.GetValue<FString>();
		recordNames.Add( Name );
	}
	if (recordNames.Num() == 1 && recordNames[0].IsEmpty())
	{
		for (auto variantData : AllMailData)
		{
			AddOneMailData(variantData);
		}
	}
	else 
	{
		RecordReceiceNames.Append(recordNames);
		for (auto variantData : AllMailData)
		{
			AddOneMailData(variantData);
		}
	}
	ReceiveAllMailBP();
}

void URoleMailInterface::ReceiveAllMailBP_Implementation()
{

}

void URoleMailInterface::OnMailDeleted(const FVariantArray&  mailids)
{
	TArray<FString> StrMailIDList;
	
	for (auto mailID: mailids)
	{

		FString strMailID = FString::FromInt( mailID.GetValue<int32>() );
		StrMailIDList.Add(strMailID);
		if (MailMap.Contains(strMailID))
		{
			MailMap.Remove(strMailID);
		}
		if (MailTimerDict.Contains(strMailID))
		{
			MailTimerDict.Remove(strMailID);
		}
	}

	OnMailDeletedBP(StrMailIDList);
}

void URoleMailInterface::OnMailDeletedBP_Implementation(const TArray<FString>& MailIDList)
{

}

void URoleMailInterface::CLIENT_ExtractMailSuccess_Implementation(const FString& MailID)
{
	if (MailMap.Contains(MailID))
	{
		MailMap[MailID].Money = 0;
		MailMap[MailID].ItemList.Empty();
	}
}

void URoleMailInterface::CLIENT_OpenMailWindow_Implementation()
{

}

void URoleMailInterface::AddMailByJsonData(const FString& jsonData)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(jsonData);
	auto temparray = returnvalue->GetObjectArray(this, TEXT("ROOT"));
	for (auto mailItem : temparray)
	{
		FMailData mailData;
		mailData.Id = mailItem->GetString(TEXT("id"));
		mailData.Title = mailItem->GetString(TEXT("title"));
		mailData.Content = mailItem->GetString(TEXT("content"));
		mailData.Money = FSTRING_TO_INT64(mailItem->GetString(TEXT("money")));
		mailData.SenderName = mailItem->GetString(TEXT("senderName"));
		mailData.ReceiverName = mailItem->GetString(TEXT("receiverName"));
		mailData.IsTaken = FSTRING_TO_INT(mailItem->GetString(TEXT("isTaken")));
		mailData.ReceiveTime = mailItem->GetString(TEXT("receiveTime"));
		mailData.RemainTime = FSTRING_TO_INT(mailItem->GetString(TEXT("remainTime")));
		mailData.SenderType = MAIL_SEND_TYPE(FSTRING_TO_INT(mailItem->GetString(TEXT("senderType"))));
		mailData.IsRead = FSTRING_TO_INT(mailItem->GetString(TEXT("isRead"))) ? true:false;
		mailData.LingShi = FSTRING_TO_INT(mailItem->GetString(TEXT("lingshi")));
		mailData.XianShi = FSTRING_TO_INT(mailItem->GetString(TEXT("xianshi")));
		FString itemListStr = mailItem->GetString(TEXT("itemList"));
		UJsonFieldData* tempItem = UJsonFieldData::Create(this);
		auto itemReturn = tempItem->FromString(itemListStr);
		auto itemArray = itemReturn->GetObjectArray(this, TEXT("ROOT"));
		for (auto item : itemArray)
		{
			int32 itemID = FSTRING_TO_INT(item->GetString(TEXT("id")));
			int32 amount = FSTRING_TO_INT(item->GetString(TEXT("amount")));
			int32 bindtype = FSTRING_TO_INT(item->GetString(TEXT("bindType")));
			FString uid = item->GetString(TEXT("uid"));
			UItemBase* itembase = UItemFactory::GetItemByID(itemID);
			if (!IsValid(itembase))
			{
				CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::AddMailByJsonData : itembase!"));
				return;
			}
			itembase->UID = uid;
			itembase->Amount = amount;
			itembase->BindType = bindtype;
			mailData.ItemList.Add(itembase);
		}
		MailMap.Add(mailData.Id,mailData);
		MailMap.ValueSort([](const FMailData& mailDataA, const FMailData& mailDataB) { return FSTRING_TO_INT64(mailDataA.ReceiveTime) > FSTRING_TO_INT64(mailDataB.ReceiveTime); });
		FTimerHandle tempTimer;
		TWeakObjectPtr<URoleMailInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, tempTimer, FTimerDelegate::CreateLambda([DelayThisPtr, mailData]()
		{
			if (DelayThisPtr.IsValid())
			{
				URoleMailInterface* ThisPtr = DelayThisPtr.Get();
				if (ThisPtr->MailMap.Contains(mailData.Id))
				{
					ThisPtr->BASE_TimeToDelMail(mailData.Id);
				}
			}
		}), mailData.RemainTime, false);
	}
}

void URoleMailInterface::BASE_TimeToDelMail(const FString& MailID)
{
	if (MailTimerDict.Contains(MailID))
	{
		MailTimerDict.Remove(MailID);
	}
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::BASE_TimeToDelMail : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(FVariant(MailID));
	GetEntity()->BaseCall(TEXT("BASE_timeToDelMail"), args);
}

void URoleMailInterface::BASE_RequestDeleteMail(TArray<FString> MailIDList)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::BASE_RequestDeleteMail : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	for (auto mailID : MailIDList)
	{
		if(mailID.Len())
			arr.Add(FCString::Atoi( *mailID) );
	}
	args.Add(FVariant(arr));
	GetEntity()->BaseCall(TEXT("mail_delete"), args);
}

void URoleMailInterface::BASE_RequestSendMail(FString receiverName, FString title, FString content)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::BASE_RequestSendMail : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	args.Add(FVariant(receiverName));
	args.Add(FVariant(title));
	args.Add(FVariant(content));
	GetEntity()->BaseCall(TEXT("BASE_mail_send"), args);
}

void URoleMailInterface::OnMailSendSuccess_Implementation()
{
}

void URoleMailInterface::CELL_RequestExtractMail(TArray<FString> MailIDList)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::CELL_RequestExtractMail : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	for (auto mailID : MailIDList)
	{
		arr.Add(FVariant(mailID));
	}
	args.Add(FVariant(arr));
	GetEntity()->CellCall(TEXT("CELL_extractMail"), args);
}

void URoleMailInterface::BASE_ReadedMailNotifyToSever(FString MailID)
{
	if (MailMap.Contains(MailID))
	{
		MailMap[MailID].IsRead = true;
	}
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMailInterface::BASE_ReadedMailNotifyToSever : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(FVariant(MailID));
	GetEntity()->BaseCall(TEXT("BASE_readedMailNotify"), args);
}

TArray<FMailData> URoleMailInterface::GetMailDataByMailSendType(MAIL_SEND_TYPE mailSendType)
{
	TArray<FMailData> mailDatas;
	for (auto mail:MailMap)
	{
		if (mail.Value.SenderType == mailSendType)
		{
			mailDatas.Add(mail.Value);
		}
	}
	return mailDatas;
}

FMailData URoleMailInterface::GetMailDataByMailID(FString mailID)
{
	if (MailMap.Contains(mailID))
	{
		return MailMap[mailID];
	}
	FMailData mailData;
	return mailData;
}

bool URoleMailInterface::IsMailDataNotRead(MAIL_SEND_TYPE mailSendType)
{
	TArray<FMailData> mailDatas = GetMailDataByMailSendType(mailSendType);
	for (auto mailData :mailDatas )
	{
		if (!mailData.IsRead)
		{
			return true;
		}
	}
	return false;
}

void URoleMailInterface::CLIENT_AddRecordReceiveName_Implementation(const FString& receiveName)
{
	RecordReceiceNames.Insert(receiveName, 0);
}

void URoleMailInterface::CLIENT_RemoveRecordReceiveName_Implementation(const FString& receiveName)
{
	if (RecordReceiceNames.Contains(receiveName))
	{
		RecordReceiceNames.Remove(receiveName);
	}
}

TArray<FString> URoleMailInterface::GetRecordReceiveNames()
{
	return RecordReceiceNames;
}

void URoleMailInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_ExtractMailSuccess");
	ArrBlueFunc.Add("CLIENT_OpenMailWindow");
	ArrBlueFunc.Add("CLIENT_AddRecordReceiveName");
	ArrBlueFunc.Add("CLIENT_RemoveRecordReceiveName");
	ArrBlueFunc.Add("OnMailSendSuccess");
	Supper::InitBlueCB();
}

void URoleMailInterface::onLeaveWorld()
{
	MailMap.Empty();
	for (auto It = MailTimerDict.CreateIterator(); It; ++It)
	{
		if (It.Value().IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(It.Value());
		}
	}
	MailTimerDict.Empty();
	RecordReceiceNames.Empty();
	Supper::onLeaveWorld();
}

