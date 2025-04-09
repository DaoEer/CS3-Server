#include "Alias.h"
#include "Util/ConvertUtil.h"
#include "Manager/TimeManager.h"
#include "JsonReader.h"
#include "JsonObject.h"
#include "JsonSerializer.h"


FString AliasRoleInfo::ToString()
{
	return FString::Printf(TEXT("dbid: %u, playerName: %s, level:%d, LoginLevel:%s"), DBid, *PlayerName, Level, *LoginLevel);
}

void AliasRoleInfo::ToFVariantMap(KBEngine::FVariantMap &out)
{
	out.Add(TEXT("dbid"), FVariant(DBid));
	out.Add(TEXT("playerName"), FVariant(PlayerName));
	out.Add(TEXT("level"), FVariant(Level));
	out.Add(TEXT("profession"), FVariant(Profession));
	out.Add(TEXT("camp"), FVariant(Camp));
	out.Add(TEXT("modelNumber"), FVariant(ModelNumber));
	out.Add(TEXT("bodyModel"), FVariant(AModelInfo.BodyModel));
	out.Add(TEXT("headModel"), FVariant(AModelInfo.HeadModel));
	out.Add(TEXT("suitsModel"), FVariant(AModelInfo.SuitsModel));
	out.Add(TEXT("hairModel"), FVariant(AModelInfo.HairModel));
	out.Add(TEXT("adornModel"), FVariant(AModelInfo.AdornModel));
	out.Add(TEXT("headAdornModel"), FVariant(AModelInfo.HeadAdornModel));
	out.Add(TEXT("faceAdornModel"), FVariant(AModelInfo.FaceAdornModel));
	out.Add(TEXT("backAdornModel"), FVariant(AModelInfo.BackAdornModel));
	out.Add(TEXT("waistAdornModel"), FVariant(AModelInfo.WaistAdornModel));
	out.Add(TEXT("hatModel"), FVariant(AModelInfo.HatModel));
	out.Add(TEXT("coatModel"), FVariant(AModelInfo.CoatModel));
	out.Add(TEXT("pantsModel"), FVariant(AModelInfo.PantsModel));
	out.Add(TEXT("shoesModel"), FVariant(AModelInfo.ShoesModel));
	out.Add(TEXT("cloakModel"), FVariant(AModelInfo.CloakModel));
	out.Add(TEXT("wristModel"), FVariant(AModelInfo.WristModel));
	out.Add(TEXT("handModel"), FVariant(AModelInfo.GlovesModel));
	out.Add(TEXT("waistModel"), FVariant(AModelInfo.WaistModel));
	out.Add(TEXT("necklaceModel"), FVariant(AModelInfo.NecklaceModel));
	out.Add(TEXT("lringModel"), FVariant(AModelInfo.LringModel));
	out.Add(TEXT("rringModel"), FVariant(AModelInfo.RringModel));
	out.Add(TEXT("weaponModel"), FVariant(AModelInfo.WeaponModel));
	out.Add(TEXT("offlineTime"), FVariant(OfflineTime));
	KBEngine::FVariantMap facemodel;
	KBEngine::FVariantMap facestyle;
	faceModel.ToFVariantMap(facemodel);
	faceStyle.ToFVariantMap(facestyle);
	out.Add(TEXT("faceModel"), FVariant(facemodel));
	out.Add(TEXT("faceStyle"), FVariant(facestyle));
}

void AliasRoleInfo::CreateFromVariant(const FVariant& val, AliasRoleInfo& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.DBid = m[TEXT("dbid")].GetValue<uint64>();
	out.PlayerName = m[TEXT("playerName")].GetValue<FString>();
	out.Level = m[TEXT("level")].GetValue<int32>();
	out.Profession = m[TEXT("profession")].GetValue<int32>();
	out.Camp = m[TEXT("camp")].GetValue<int32>();
	out.Gender = m[TEXT("gender")].GetValue<int32>();
	out.ModelNumber = m[TEXT("modelNumber")].GetValue<FString>();
	out.AModelInfo.BodyModel = m[TEXT("bodyModel")].GetValue<FString>();
	out.AModelInfo.HeadModel = m[TEXT("headModel")].GetValue<FString>();
	out.AModelInfo.SuitsModel = m[TEXT("suitsModel")].GetValue<FString>();
	out.AModelInfo.HairModel = m[TEXT("hairModel")].GetValue<FString>();
	out.AModelInfo.AdornModel = m[TEXT("adornModel")].GetValue<FString>();
	out.AModelInfo.CoatModel = m[TEXT("coatModel")].GetValue<FString>();
	out.AModelInfo.PantsModel = m[TEXT("pantsModel")].GetValue<FString>();
	out.AModelInfo.ShoesModel = m[TEXT("shoesModel")].GetValue<FString>();
	out.AModelInfo.CloakModel = m[TEXT("cloakModel")].GetValue<FString>();
	out.AModelInfo.HeadAdornModel = m[TEXT("headAdornModel")].GetValue<FString>();
	out.AModelInfo.FaceAdornModel = m[TEXT("faceAdornModel")].GetValue<FString>();
	out.AModelInfo.BackAdornModel = m[TEXT("backAdornModel")].GetValue<FString>();
	out.AModelInfo.WaistAdornModel = m[TEXT("waistAdornModel")].GetValue<FString>();
	out.AModelInfo.HatModel = m[TEXT("hatModel")].GetValue<FString>();
	out.AModelInfo.WristModel = m[TEXT("wristModel")].GetValue<FString>();
	out.AModelInfo.GlovesModel = m[TEXT("handModel")].GetValue<FString>();
	out.AModelInfo.WaistModel = m[TEXT("waistModel")].GetValue<FString>();
	out.AModelInfo.NecklaceModel = m[TEXT("necklaceModel")].GetValue<FString>();
	out.AModelInfo.LringModel = m[TEXT("lringModel")].GetValue<FString>();
	out.AModelInfo.RringModel = m[TEXT("rringModel")].GetValue<FString>();
	out.AModelInfo.WeaponModel = m[TEXT("weaponModel")].GetValue<FString>();
	out.OfflineTime = m[TEXT("offlineTime")].GetValue<uint64>();
	FaceInfoList::CreateFromVariant(m[TEXT("faceModel")],out.faceModel);
	FaceStyle::CreateFromVariant(m[TEXT("faceStyle")],out.faceStyle);
}

FString AliasRoleInfoTmap::ToString()
{
	FString InfoStr;
	TArray<FStringFormatArg> Arg;
	uint32 i = 0;
	for (auto& info : infos)
	{
		InfoStr += FString::Printf(TEXT("{%u}, "), i++);
		Arg.Add(info.ToString());
	}

	InfoStr = FString::Format(*InfoStr, Arg);
	return FString::Printf(TEXT("infos:[%s]"), *InfoStr);
}

void AliasRoleInfoTmap::CreateFromVariant(const FVariant& val, AliasRoleInfoTmap& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	auto fs = m[TEXT("infos")].GetValue<KBEngine::FVariantArray>();
	for (auto& itor : fs)
	{
		AliasRoleInfo item;
		AliasRoleInfo::CreateFromVariant(itor.GetValue<KBEngine::FVariantMap>(),item);
		out.infos.Add(item);
	}
}


void FaceInfo::ToFVariantMap(KBEngine::FVariantMap &out)
{
	out.Add(TEXT("boneName"), FVariant(boneName));
	out.Add(TEXT("boneData"), FVariant(boneData));
}

void FaceInfo::CreateFromVariant(const FVariant& val, FaceInfo& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.boneName = m[TEXT("boneName")].GetValue<FString>();
	out.boneData = m[TEXT("boneData")].GetValue<FString>();
}

void FaceInfoList::ToFVariantMap(KBEngine::FVariantMap &out)
{	
	
	KBEngine::FVariantArray faceInfoList;
	for (FaceInfo& info : infolist)
	{
		KBEngine::FVariantMap faceInfo;
		faceInfo.Add(TEXT("boneName"),FVariant(info.boneName));
		faceInfo.Add(TEXT("boneData"),FVariant(info.boneData));
		faceInfoList.Add(FVariant(faceInfo));
	}
	out.Add(TEXT("infos"), faceInfoList);
	
}

void FaceInfoList::CreateFromVariant(const FVariant& val, FaceInfoList& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	auto fs=m[TEXT("infos")].GetValue<KBEngine::FVariantArray>();
	for (auto& itor : fs)
	{	
		FaceInfo faceInfo;
		FaceInfo::CreateFromVariant(itor.GetValue<KBEngine::FVariantMap>(), faceInfo);
		out.infolist.Add(faceInfo);
	}

}

void FaceStyle::ToFVariantMap(KBEngine::FVariantMap &out) 
{
	out.Add(TEXT("ChunzhuangIndex"), FVariant(ChunzhuangIndex));
	out.Add(TEXT("ChunzhuangShape"), FVariant(ChunzhuangShape));
	out.Add(TEXT("HuXuIndex"), FVariant(HuXuIndex));
	out.Add(TEXT("LianWenIndex"), FVariant(LianWenIndex));
	out.Add(TEXT("MeiMaoIndex"), FVariant(MeiMaoIndex));
	out.Add(TEXT("MeiMaoShape"), FVariant(MeiMaoShape));
	out.Add(TEXT("YanXianIndex"), FVariant(YanXianIndex));
	out.Add(TEXT("SaiHongIndex"), FVariant(SaiHongIndex));
	out.Add(TEXT("SaiHongShape"), FVariant(SaiHongShape));
	out.Add(TEXT("YanYingIndex"), FVariant(YanYingIndex));
	out.Add(TEXT("YanYingShape"), FVariant(YanYingShape));
	out.Add(TEXT("Brightness"), FVariant(Brightness));
	out.Add(TEXT("ColorDepth"), FVariant(ColorDepth));
	out.Add(TEXT("EyeIndex"), FVariant(EyeIndex));
	out.Add(TEXT("EyeScale"), FVariant(EyeScale));
	
}

void Model::ToFVariantMap(KBEngine::FVariantMap &out)
{
	out.Add(TEXT("modelName"), FVariant(modelName));
	out.Add(TEXT("modelNumber"), FVariant(modelNumber));
}
 
void Model::CreateFromVariant(const FVariant& val, Model& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.modelName = m[TEXT("modelName")].GetValue<FString>();
	out.modelNumber = m[TEXT("modelNumber")].GetValue<FString>();
}

void ModelList::ToFVariantMap(KBEngine::FVariantMap &out)
{
	KBEngine::FVariantArray ModelList;
	for (Model& model : modelList)
	{
		KBEngine::FVariantMap Model;
		Model.Add(TEXT("modelName"), FVariant(model.modelName));
		Model.Add(TEXT("modelNumber"), FVariant(model.modelNumber));
		ModelList.Add(FVariant(Model));
	}
	out.Add(TEXT("modelList"), ModelList);
}

void ModelList::CreateFromVariant(const FVariant& val, ModelList& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	auto ml = m[TEXT("modelList")].GetValue<KBEngine::FVariantArray>();
	for (auto& itor : ml)
	{
		Model model;
		Model::CreateFromVariant(itor.GetValue<KBEngine::FVariantMap>(), model);
		out.modelList.Add(model);
	}
}

void FaceStyle::CreateFromVariant(const FVariant& val, FaceStyle& out) 
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.ChunzhuangIndex = m[TEXT("ChunzhuangIndex")].GetValue<int32>();
	out.ChunzhuangShape = m[TEXT("ChunzhuangShape")].GetValue<FString>();
	out.HuXuIndex = m[TEXT("HuXuIndex")].GetValue<int32>();
	out.LianWenIndex = m[TEXT("LianWenIndex")].GetValue<int32>();
	out.MeiMaoIndex = m[TEXT("MeiMaoIndex")].GetValue<int32>();
	out.MeiMaoShape = m[TEXT("MeiMaoShape")].GetValue<FString>();
	out.YanXianIndex = m[TEXT("YanXianIndex")].GetValue<int32>();
	out.SaiHongIndex = m[TEXT("SaiHongIndex")].GetValue<int32>();
	out.SaiHongShape = m[TEXT("SaiHongShape")].GetValue<FString>();
	out.YanYingIndex = m[TEXT("YanYingIndex")].GetValue<int32>();
	out.YanYingShape = m[TEXT("YanYingShape")].GetValue<FString>();
	out.Brightness = m[TEXT("Brightness")].GetValue<FString>();
	out.ColorDepth = m[TEXT("ColorDepth")].GetValue<FString>();
	out.EyeIndex = m[TEXT("EyeIndex")].GetValue<int32>();
	out.EyeScale = m[TEXT("EyeScale")].GetValue<FString>();
}

void AliasChatData::CreateFromVariant(const FVariant& val, FChatData& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.playerDBID = m[TEXT("playerDBID")].GetValue<uint64>();
	out.name = m[TEXT("name")].GetValue<FString>();
	switch (m[TEXT("type")].GetValue<int8>())
	{
	case 0:		out.type = ChatType::Nearby; break;
	case 1:		out.type = ChatType::Space; break;
	case 2:		out.type = ChatType::World; break;
	case 3:		out.type = ChatType::Whisper; break;
	case 4:		out.type = ChatType::Group; break;
	case 5:		out.type = ChatType::Team; break;
	case 6:		out.type = ChatType::Collective; break;
	case 7:		out.type = ChatType::Gang; break;
	case 8:		out.type = ChatType::Aliance; break;
	case 9:		out.type = ChatType::School; break;
	case 10:	out.type = ChatType::Camp; break;
	case 11:	out.type = ChatType::Battlespace; break;
	case 12:	out.type = ChatType::Tianyin; break;
	case 13:	out.type = ChatType::Xianyin; break;
	case 14:	out.type = ChatType::System; break;
	case 15:	out.type = ChatType::Friend; break;
	default:break;
	}
	out.entityType = m[TEXT("entityType")].GetValue<int8>();
	out.message = m[TEXT("message")].GetValue<FString>();
	out.time = UUECS3GameInstance::Instance->TimeManager->GetClientTime();
	auto rich = m[TEXT("richText")].GetValue<KBEngine::FVariantArray>();
	for (auto& itor : rich)
	{
		out.richText.Add(itor);
	}
}

void AliasChatData::CreateFromString(const FString& val, FChatData& out)
{
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(val);
	TSharedPtr<FJsonObject> jsonParsed;

	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);
	if (BFlag)
	{
		out.playerDBID = jsonParsed->GetIntegerField("playerDBID");
		out.name = jsonParsed->GetStringField("name");
		switch (jsonParsed->GetIntegerField("type"))
		{
		case 0: out.type = ChatType::Nearby; break;
		case 1: out.type = ChatType::Space; break;
		case 2: out.type = ChatType::World; break;
		case 3: out.type = ChatType::Whisper; break;
		case 4: out.type = ChatType::Group; break;
		case 5: out.type = ChatType::Team; break;
		case 6: out.type = ChatType::Collective; break;
		case 7: out.type = ChatType::Gang; break;
		case 8: out.type = ChatType::Aliance; break;
		case 9: out.type = ChatType::School; break;
		case 10: out.type = ChatType::Camp; break;
		case 11: out.type = ChatType::Battlespace; break;
		case 12: out.type = ChatType::Tianyin; break;
		case 13: out.type = ChatType::Xianyin; break;
		case 14: out.type = ChatType::System; break;
		case 15: out.type = ChatType::Friend; break;
		default:break;
		}
		out.entityType = jsonParsed->GetIntegerField("entityType");
		out.message = jsonParsed->GetStringField("message");
		out.time = UUECS3GameInstance::Instance->TimeManager->GetClientTime();
		TArray<TSharedPtr<FJsonValue>> curr = jsonParsed->GetArrayField("richText");
		for (auto& itor : curr)
		{
			out.richText.Add(itor->AsString());
		}
	}
}

void AliasChatData::CreateFromVariantToPage(const FVariant& variant, TArray<FChatPageData>& out)
{

	FCHAT_PAGESETTINGS_DATAS pageDatas = FCHAT_PAGESETTINGS_DATAS(variant);
	FChatPageData inst;
	ChatType currType;
	for (auto& pageData : pageDatas.datas )
	{
		switch ( pageData.pageType )
		{
			case 0: inst.pageType = ChatPageType::Synthesis; break;
			case 1: inst.pageType = ChatPageType::Common; break;
			case 2: inst.pageType = ChatPageType::Other; break;
			case 3: inst.pageType = ChatPageType::Private; break;
			case 4: inst.pageType = ChatPageType::Fight; break;
			case 5: inst.pageType = ChatPageType::Custom1; break;
			case 6: inst.pageType = ChatPageType::Custom2; break;
			default:break;
			}

			inst.isDeletable = pageData.isDeletable;
			inst.isDraggable = pageData.isDraggable;
			inst.pageName = pageData.pageName;
			inst.channelList.Reset();

			for (auto& ou : pageData.channelList)
			{
				switch ( ou )
				{
				case 0: currType = ChatType::Nearby; break;
				case 1: currType = ChatType::Space; break;
				case 2: currType = ChatType::World; break;
				case 3: currType = ChatType::Whisper; break;
				case 4: currType = ChatType::Group; break;
				case 5: currType = ChatType::Team; break;
				case 6: currType = ChatType::Collective; break;
				case 7: currType = ChatType::Gang; break;
				case 8: currType = ChatType::Aliance; break;
				case 9: currType = ChatType::School; break;
				case 10: currType = ChatType::Camp; break;
				case 11: currType = ChatType::Battlespace; break;
				case 12: currType = ChatType::Tianyin; break;
				case 13: currType = ChatType::Xianyin; break;
				case 14: currType = ChatType::System; break;
				default:break;
				}
				inst.channelList.Add(currType);
			}
			out.Add(inst);
		}
}

void AliasChatData::CreateFromVariantToPageData(const FVariant& variant, FChatPageData& out)
{
	FCHAT_PAGESETTINGS pageData = FCHAT_PAGESETTINGS(variant);
	switch (pageData.pageType)
	{
		case 0: out.pageType = ChatPageType::Synthesis; break;
		case 1: out.pageType = ChatPageType::Common; break;
		case 2: out.pageType = ChatPageType::Other; break;
		case 3: out.pageType = ChatPageType::Private; break;
		case 4: out.pageType = ChatPageType::Fight; break;
		case 5: out.pageType = ChatPageType::Custom1; break;
		case 6: out.pageType = ChatPageType::Custom2; break;
	default:break;
	}
		out.isDeletable = pageData.isDeletable;
		out.isDraggable = pageData.isDraggable;
		out.pageName = pageData.pageName;

		ChatType currType;
		for (auto& ou : pageData.channelList)
		{
			switch ( ou )
			{
			case 0: currType = ChatType::Nearby; break;
			case 1: currType = ChatType::Space; break;
			case 2: currType = ChatType::World; break;
			case 3: currType = ChatType::Whisper; break;
			case 4: currType = ChatType::Group; break;
			case 5: currType = ChatType::Team; break;
			case 6: currType = ChatType::Collective; break;
			case 7: currType = ChatType::Gang; break;
			case 8: currType = ChatType::Aliance; break;
			case 9: currType = ChatType::School; break;
			case 10: currType = ChatType::Camp; break;
			case 11: currType = ChatType::Battlespace; break;
			case 12: currType = ChatType::Tianyin; break;
			case 13: currType = ChatType::Xianyin; break;
			case 14: currType = ChatType::System; break;
			default:break;
			}
			out.channelList.Add(currType);
		}
	
}

void AliasChatData::CreateFromStringToChannel(const FString& channelDatas, TArray<FChatChannelData>& out)
{
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(channelDatas);
	TSharedPtr<FJsonValue> jsonParsed;
	
	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);
	if (BFlag)
	{
		TSharedPtr<FJsonObject> jsonObject;
		FChatChannelData inst;

		for (auto& jsonValue : jsonParsed->AsArray())
		{
			jsonObject = jsonValue->AsObject();
			switch (jsonObject->GetIntegerField("channelType"))
			{
			case 0: inst.channelType = ChatType::Nearby; break;
			case 1: inst.channelType = ChatType::Space; break;
			case 2: inst.channelType = ChatType::World; break;
			case 3: inst.channelType = ChatType::Whisper; break;
			case 4: inst.channelType = ChatType::Group; break;
			case 5: inst.channelType = ChatType::Team; break;
			case 6: inst.channelType = ChatType::Collective; break;
			case 7: inst.channelType = ChatType::Gang; break;
			case 8: inst.channelType = ChatType::Aliance; break;
			case 9: inst.channelType = ChatType::School; break;
			case 10: inst.channelType = ChatType::Camp; break;
			case 11: inst.channelType = ChatType::Battlespace; break;
			case 12: inst.channelType = ChatType::Tianyin; break;
			case 13: inst.channelType = ChatType::Xianyin; break;
			case 14: inst.channelType = ChatType::System; break;
			default:break;
			}

			inst.isCanModify = jsonObject->GetIntegerField("isCanModify");
			inst.shortcutKey = jsonObject->GetStringField("shortcutKey");
			out.Add(inst);
		}
	}
}

USEConditionBase* AliasSpaceEventConditions::CreateConFromString(const FString& SpaceScriptID, const INT32 EventType, const INT32 EventID, const FString& SrcStr)
{
	FString ScriptName;
	FString Param1;
	FString Param2;
	FString Param3;
	FString Param4;

	TArray<FString> ConArray;
	SrcStr.ParseIntoArray(ConArray, TEXT(", "), true);
	for (auto& ConParam : ConArray)
	{
		FString sKey;
		FString sValue(ConParam);
		sValue.Split(": ", &sKey, &sValue);
		sKey.RemoveFromStart("\"");
		sKey.RemoveFromEnd("\"");
		sValue.RemoveFromStart("\"");
		sValue.RemoveFromEnd("\"");

		if (sKey == "param1") { Param1 = sValue; }
		else if (sKey == "param2") { Param2 = sValue; }
		else if (sKey == "param3") { Param3 = sValue; }
		else if (sKey == "param4") { Param4 = sValue; }
		else if (sKey == "scriptName") { ScriptName = sValue; }
	}

	USEConditionBase* ConIns = USEConditionFactory::CreateConditionByClass(ScriptName);
	ConIns->InitParams(SpaceScriptID, EventType, EventID, Param1, Param2, Param3, Param4);
	return ConIns;

}

AliasSpaceEventConditions::~AliasSpaceEventConditions()
{

}

void AliasSpaceEventConditions::CreateFromString(const FString& SpaceScriptID, const INT32 EventType, const INT32 EventID, const FString & ConInfoStr, AliasSpaceEventConditions& out)
{
	TArray<FString> ConInfoArray;
	FString sLeft;
	FString sRight(ConInfoStr);
	sRight.Split("[{", &sLeft, &sRight);
	sRight.Split("}]}", &sLeft, &sRight);
	sLeft.ParseIntoArray(ConInfoArray, TEXT("}, {"), true);

	for (auto& ConInfo : ConInfoArray)
	{
		USEConditionBase* ConIns = CreateConFromString(SpaceScriptID, EventType, EventID, ConInfo);
		ConIns->AddToRoot();
		out.Infos.Add(ConIns);
	}
}

void AliasNpcShopItemList::CreateFromString(const FString& val, TMap<FString, TMap<FString, float>>& out)
{
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(val);
	TSharedPtr<FJsonObject> jsonParsed;

	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);

	if (BFlag)
	{	
		TMap<FString, float> value;
		for (auto dict : jsonParsed->Values)
		{
			auto data = dict.Value->AsObject();
			value.Add("itemID", data->GetNumberField("itemID"));
			value.Add("amount", data->GetNumberField("amount"));
			value.Add("startTime", data->GetNumberField("startTime"));
			out.Add(dict.Key, value);
		}
	}
}

void BuffDataType::CreateFromVariant(const FVariant& val, BuffDataType& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.index = m[TEXT("index")].GetValue<int32>();
	out.buffID = m[TEXT("buffID")].GetValue<int32>();
	out.holdTime = m[TEXT("holdTime")].GetValue<float>();
	out.endTime = m[TEXT("endTime")].GetValue<uint64>();
	out.timerID = m[TEXT("timerID")].GetValue<int32>();
	out.casterID = m[TEXT("casterID")].GetValue<int32>();
	out.casterIsSelf = m[TEXT("casterIsSelf")].GetValue<uint8>();
	out.layer = m[TEXT("layer")].GetValue<int32>();
	out.className = m[TEXT("className")].GetValue<FString>();
}

TESTITEM::~TESTITEM()
{
	flag.Empty();
}

void TESTITEM::ToFVariantMap(KBEngine::FVariantMap& out)
{
	out.Add(TEXT("uid"), FVariant((uint64)uid));
	out.Add(TEXT("id"), FVariant(id));
	out.Add(TEXT("amount"), FVariant(amount));
	
	KBEngine::FVariantArray arr;
	for (auto v : flag)
	{
		arr.Add(FVariant(v));
	}

	out.Add(TEXT("flag"), FVariant(arr));

	out.Add(TEXT("misc"), FVariant(misc));
}

TESTITEMS::~TESTITEMS()
{
	itemList.Empty();
}

void TESTITEMS::ToFVariantMap(KBEngine::FVariantMap& out)
{
	out.Add(TEXT("id"), FVariant(id));
	KBEngine::FVariantArray arr;
	for (auto v : itemList)
	{
		KBEngine::FVariantMap testitem;
		v.ToFVariantMap(testitem);
		arr.Add(FVariant(testitem));
	}
	out.Add("itemList", FVariant(arr));
}

STALLITEMS::~STALLITEMS()
{
	stallItemList.Empty();
}

void STALLITEMS::ToFVariantMap(KBEngine::FVariantArray& out)
{
	for (auto item:stallItemList)
	{
		KBEngine::FVariantMap stallItem;
		stallItem.Add(TEXT("id"), FVariant(item.Id));
		stallItem.Add(TEXT("itemID"), FVariant(item.ItemID));
		stallItem.Add(TEXT("amount"), FVariant(item.Amount));
		stallItem.Add(TEXT("price"), FVariant(item.Price));
		out.Add(FVariant(stallItem));
	}
}

void AliasShopMallItemList::CreateFromString(const FString& val, TMap<FString, TMap<FString, int32>>& out)
{
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(val);
	TSharedPtr<FJsonObject> jsonParsed;

	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);

	if (BFlag)
	{
		TMap<FString, int32> value;
		for (auto dict : jsonParsed->Values)
		{
			auto data = dict.Value->AsObject();
			value.Add("itemID", FSTRING_TO_INT(data->GetStringField("itemID")));
			value.Add("amount", data->GetIntegerField("amount"));
			out.Add(dict.Key, value);
		}
	}
}

void BuyShopMallItems::ToFVariantMap(KBEngine::FVariantArray& out)
{
	for (auto item:buyShopMallItemList)
	{
		KBEngine::FVariantMap buyItem;
		buyItem.Add(TEXT("shopMallType"), FVariant(item.ShopMallType));
		buyItem.Add(TEXT("slot"), FVariant(item.Slot));
		buyItem.Add(TEXT("itemID"), FVariant(item.ItemID));
		buyItem.Add(TEXT("amount"), FVariant(item.Amount));
		buyItem.Add(TEXT("moneyType"), FVariant(item.MoneyType));
		buyItem.Add(TEXT("itemType"), FVariant(item.ItemType));
		out.Add(FVariant(buyItem));
	}
}

FLEVEL_RANK::FLEVEL_RANK()
{

}

FLEVEL_RANK::FLEVEL_RANK(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	playerDBID1 = variantMap[TEXT("playerDBID")].GetValue<uint64>();
	playerName2 = variantMap[TEXT("playerName")].GetValue<FString>();
	camp3 = variantMap[TEXT("camp")].GetValue<uint8>();
	profession4 = variantMap[TEXT("profession")].GetValue<int32>();
	combatPower5 = variantMap[TEXT("combatPower")].GetValue<int32>();
	level6 = variantMap[TEXT("level")].GetValue<int32>();
	ascend7 = variantMap[TEXT("ascend")].GetValue<int32>();

}

FVariant FLEVEL_RANK::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("playerDBID"), playerDBID1);
	variantMap.Add(TEXT("playerName"), playerName2);
	variantMap.Add(TEXT("camp"), camp3);
	variantMap.Add(TEXT("profession"), profession4);
	variantMap.Add(TEXT("combatPower"), combatPower5);
	variantMap.Add(TEXT("level"), level6);
	variantMap.Add(TEXT("ascend"), ascend7);

	return FVariant(variantMap);
}

FLEVEL_RANK_DICT::FLEVEL_RANK_DICT()
{

}

FLEVEL_RANK_DICT::FLEVEL_RANK_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_datas1 = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_datas1)
	{
		FLEVEL_RANK element1 = FLEVEL_RANK(elementVariant0);
		datas1.Add(element1);
	}

}

FVariant FLEVEL_RANK_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_datas1.Add(element1);
	}
	variantMap.Add(TEXT("datas"), variantArray_datas1);

	return FVariant(variantMap);
}

FCOMBAT_RANK_DICT::FCOMBAT_RANK_DICT()
{

}

FCOMBAT_RANK_DICT::FCOMBAT_RANK_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_datas1 = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_datas1)
	{
		FLEVEL_RANK element1 = FLEVEL_RANK(elementVariant0);
		datas1.Add(element1);
	}

}

FVariant FCOMBAT_RANK_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_datas1.Add(element1);
	}
	variantMap.Add(TEXT("datas"), variantArray_datas1);

	return FVariant(variantMap);
}

FMONEY_RANK::FMONEY_RANK()
{

}

FMONEY_RANK::FMONEY_RANK(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	playerDBID1 = variantMap[TEXT("playerDBID")].GetValue<uint64>();
	playerName2 = variantMap[TEXT("playerName")].GetValue<FString>();
	camp3 = variantMap[TEXT("camp")].GetValue<uint8>();
	profession4 = variantMap[TEXT("profession")].GetValue<int32>();
	money5 = variantMap[TEXT("money")].GetValue<int64>();
	level6 = variantMap[TEXT("level")].GetValue<int32>();
	ascend7 = variantMap[TEXT("ascend")].GetValue<int32>();

}

FVariant FMONEY_RANK::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("playerDBID"), playerDBID1);
	variantMap.Add(TEXT("playerName"), playerName2);
	variantMap.Add(TEXT("camp"), camp3);
	variantMap.Add(TEXT("profession"), profession4);
	variantMap.Add(TEXT("money"), money5);
	variantMap.Add(TEXT("level"), level6);
	variantMap.Add(TEXT("ascend"), ascend7);

	return FVariant(variantMap);
}

FMONEY_RANK_DICT::FMONEY_RANK_DICT()
{

}

FMONEY_RANK_DICT::FMONEY_RANK_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_datas1 = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_datas1)
	{
		FMONEY_RANK element1 = FMONEY_RANK(elementVariant0);
		datas1.Add(element1);
	}

}

FVariant FMONEY_RANK_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_datas1.Add(element1);
	}
	variantMap.Add(TEXT("datas"), variantArray_datas1);

	return FVariant(variantMap);
}

FWEAPON_COMBAT_RANK::FWEAPON_COMBAT_RANK()
{

}

FWEAPON_COMBAT_RANK::FWEAPON_COMBAT_RANK(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	playerDBID1 = variantMap[TEXT("playerDBID")].GetValue<uint64>();
	playerName2 = variantMap[TEXT("playerName")].GetValue<FString>();
	camp3 = variantMap[TEXT("camp")].GetValue<uint8>();
	weaponUID4 = variantMap[TEXT("weaponUID")].GetValue<uint64>();
	weaponID5 = variantMap[TEXT("weaponID")].GetValue<int32>();
	quality6 = variantMap[TEXT("quality")].GetValue<int32>();
	combatPower7 = variantMap[TEXT("combatPower")].GetValue<int32>();
	attackProperties8 = variantMap[TEXT("attackProperties")].GetValue<FString>();
	attachProperties9 = variantMap[TEXT("attachProperties")].GetValue<FString>();
	intensifyProperties10 = variantMap[TEXT("intensifyProperties")].GetValue<FString>();
	ascend11 = variantMap[TEXT("ascend")].GetValue<int32>();

}

FVariant FWEAPON_COMBAT_RANK::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("playerDBID"), playerDBID1);
	variantMap.Add(TEXT("playerName"), playerName2);
	variantMap.Add(TEXT("camp"), camp3);
	variantMap.Add(TEXT("weaponUID"), weaponUID4);
	variantMap.Add(TEXT("weaponID"), weaponID5);
	variantMap.Add(TEXT("quality"), quality6);
	variantMap.Add(TEXT("combatPower"), combatPower7);
	variantMap.Add(TEXT("attackProperties"), attackProperties8);
	variantMap.Add(TEXT("attachProperties"), attachProperties9);
	variantMap.Add(TEXT("intensifyProperties"), intensifyProperties10);
	variantMap.Add(TEXT("ascend"), ascend11);

	return FVariant(variantMap);
}

FWEAPON_COMBAT_DICT::FWEAPON_COMBAT_DICT()
{

}

FWEAPON_COMBAT_DICT::FWEAPON_COMBAT_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_datas1 = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_datas1)
	{
		FWEAPON_COMBAT_RANK element1 = FWEAPON_COMBAT_RANK(elementVariant0);
		datas1.Add(element1);
	}

}

FVariant FWEAPON_COMBAT_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_datas1.Add(element1);
	}
	variantMap.Add(TEXT("datas"), variantArray_datas1);

	return FVariant(variantMap);
}

FGUARD_SOUL_DATA::FGUARD_SOUL_DATA()
{

}

FGUARD_SOUL_DATA::FGUARD_SOUL_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	scriptID1 = variantMap[TEXT("scriptID")].GetValue<FString>();
	level2 = variantMap[TEXT("level")].GetValue<int32>();
	buyTime3 = variantMap[TEXT("buyTime")].GetValue<uint8>();

}

FVariant FGUARD_SOUL_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("scriptID"), scriptID1);
	variantMap.Add(TEXT("level"), level2);
	variantMap.Add(TEXT("buyTime"), buyTime3);

	return FVariant(variantMap);
}

FPAGODA_SOUL_DATA::FPAGODA_SOUL_DATA()
{

}

FPAGODA_SOUL_DATA::FPAGODA_SOUL_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_allPagoda1 = variantMap[TEXT("allPagoda")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_allPagoda1)
	{
		FString element1 = elementVariant0.GetValue<FString>();
		allPagoda1.Add(element1);
	}
	KBEngine::FVariantArray variantArray_deadPagoda2 = variantMap[TEXT("deadPagoda")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_deadPagoda2)
	{
		FString element1 = elementVariant0.GetValue<FString>();
		deadPagoda2.Add(element1);
	}
	wayType3 = variantMap[TEXT("wayType")].GetValue<int32>();

}

FVariant FPAGODA_SOUL_DATA::ToVariant()
{
	FVariant outVariant = FVariant();
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_allPagoda1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : allPagoda1)
	{
		FString element1 = elementVariant0;
		variantArray_allPagoda1.Add(element1);
	}
	variantMap.Add(TEXT("allPagoda"), variantArray_allPagoda1);
	KBEngine::FVariantArray variantArray_deadPagoda2 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : deadPagoda2)
	{
		FString element1 = elementVariant0;
		variantArray_deadPagoda2.Add(element1);
	}
	variantMap.Add(TEXT("deadPagoda"), variantArray_deadPagoda2);
	variantMap.Add(TEXT("wayType"), wayType3);

	outVariant = FVariant(variantMap);
	return outVariant;

}

FBIGMAP_SHOW_INFO::FBIGMAP_SHOW_INFO()
{

}

FBIGMAP_SHOW_INFO::FBIGMAP_SHOW_INFO(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	objectID1 = variantMap[TEXT("objectID")].GetValue<int32>();
	position2 = variantMap[TEXT("position")].GetValue<FVector>();
	name3 = variantMap[TEXT("name")].GetValue<FString>();

}

FVariant FBIGMAP_SHOW_INFO::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("objectID"), objectID1);
	variantMap.Add(TEXT("position"), position2);
	variantMap.Add(TEXT("name"), name3);

	return FVariant(variantMap);
}

FBIGMAP_SHOW_INFOS::FBIGMAP_SHOW_INFOS()
{

}

FBIGMAP_SHOW_INFOS::FBIGMAP_SHOW_INFOS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_infos1 = variantMap[TEXT("infos")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_infos1)
	{
		FBIGMAP_SHOW_INFO element1 = FBIGMAP_SHOW_INFO(elementVariant0);
		infos1.Add(element1);
	}

}

FVariant FBIGMAP_SHOW_INFOS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_infos1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : infos1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_infos1.Add(element1);
	}
	variantMap.Add(TEXT("infos"), variantArray_infos1);

	return FVariant(variantMap);
}

FEQUIP_INFO::FEQUIP_INFO()
{

}

FEQUIP_INFO::FEQUIP_INFO(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	itemID1 = variantMap[TEXT("itemID")].GetValue<uint32>();
	combatPower2 = variantMap[TEXT("combatPower")].GetValue<uint32>();
	hardiness3 = variantMap[TEXT("hardiness")].GetValue<int32>();
	attackPropertiesStr4 = variantMap[TEXT("attackPropertiesStr")].GetValue<FString>();
	attachPropertiesStr5 = variantMap[TEXT("attachPropertiesStr")].GetValue<FString>();
	intensifyDataStr6 = variantMap[TEXT("intensifyDataStr")].GetValue<FString>();

}

FVariant FEQUIP_INFO::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("itemID"), itemID1);
	variantMap.Add(TEXT("combatPower"), combatPower2);
	variantMap.Add(TEXT("hardiness"), hardiness3);
	variantMap.Add(TEXT("attackPropertiesStr"), attackPropertiesStr4);
	variantMap.Add(TEXT("attachPropertiesStr"), attachPropertiesStr5);
	variantMap.Add(TEXT("intensifyDataStr"), intensifyDataStr6);

	return FVariant(variantMap);
}

FEQUIP_INFO_DICT::FEQUIP_INFO_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("Datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FEQUIP_INFO element1 = FEQUIP_INFO(elementVariant0);
		Datas1.Add(element1);
	}

}

FVariant FEQUIP_INFO_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : Datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("Datas"), variantArray_Datas1);

	return FVariant(variantMap);
}

FROLE_PROPERTY_INFO::FROLE_PROPERTY_INFO()
{

}

FROLE_PROPERTY_INFO::FROLE_PROPERTY_INFO(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	name = variantMap[TEXT("name")].GetValue<FString>();
	camp1 = variantMap[TEXT("camp")].GetValue<int8>();
	gender2 = variantMap[TEXT("gender")].GetValue<int8>();
	profession3 = variantMap[TEXT("profession")].GetValue<uint8>();
	level4 = variantMap[TEXT("level")].GetValue<uint8>();
	xiuwei5 = variantMap[TEXT("xiuwei")].GetValue<uint32>();
	jingjieLevel6 = variantMap[TEXT("jingjieLevel")].GetValue<uint8>();
	killingValue7 = variantMap[TEXT("killingValue")].GetValue<uint16>();
	potential8 = variantMap[TEXT("potential")].GetValue<uint32>();
	combatPower9 = variantMap[TEXT("combatPower")].GetValue<uint16>();
	strength10 = variantMap[TEXT("strength")].GetValue<uint32>();
	dexterity11 = variantMap[TEXT("dexterity")].GetValue<uint32>();
	intellect12 = variantMap[TEXT("intellect")].GetValue<uint32>();
	corporeity13 = variantMap[TEXT("corporeity")].GetValue<uint32>();
	discern14 = variantMap[TEXT("discern")].GetValue<uint32>();
	speed15 = variantMap[TEXT("speed")].GetValue<uint16>();
	HP16 = variantMap[TEXT("HP")].GetValue<uint32>();
	HP_Max17 = variantMap[TEXT("HP_Max")].GetValue<uint32>();
	MP18 = variantMap[TEXT("MP")].GetValue<uint32>();
	MP_Max19 = variantMap[TEXT("MP_Max")].GetValue<uint32>();
	gangQiValue20 = variantMap[TEXT("gangQiValue")].GetValue<uint32>();
	gangQiValue_Max21 = variantMap[TEXT("gangQiValue_Max")].GetValue<uint32>();
	damage22 = variantMap[TEXT("damage")].GetValue<uint32>();
	magic_damage23 = variantMap[TEXT("magic_damage")].GetValue<uint32>();
	armor24 = variantMap[TEXT("armor")].GetValue<uint32>();
	magic_armor25 = variantMap[TEXT("magic_armor")].GetValue<uint32>();
	gangQi_damagePoint26 = variantMap[TEXT("gangQi_damagePoint")].GetValue<uint32>();
	gangQi_armorPoint27 = variantMap[TEXT("gangQi_armorPoint")].GetValue<uint32>();
	criticalstrike28 = variantMap[TEXT("criticalstrike")].GetValue<uint16>();
	parry29 = variantMap[TEXT("parry")].GetValue<uint16>();
	hitrate30 = variantMap[TEXT("hitrate")].GetValue<uint16>();
	dodgerate31 = variantMap[TEXT("dodgerate")].GetValue<uint16>();
	healingrate32 = variantMap[TEXT("healingrate")].GetValue<uint16>();
	cure33 = variantMap[TEXT("cure")].GetValue<uint32>();
	ice_damage34 = variantMap[TEXT("ice_damage")].GetValue<uint32>();
	fire_damage35 = variantMap[TEXT("fire_damage")].GetValue<uint32>();
	thunder_damage36 = variantMap[TEXT("thunder_damage")].GetValue<uint32>();
	xuan_damage37 = variantMap[TEXT("xuan_damage")].GetValue<uint32>();
	ice_armor38 = variantMap[TEXT("ice_armor")].GetValue<uint32>();
	fire_armor39 = variantMap[TEXT("fire_armor")].GetValue<uint32>();
	thunder_armor40 = variantMap[TEXT("thunder_armor")].GetValue<uint32>();
	xuan_armor41 = variantMap[TEXT("xuan_armor")].GetValue<uint32>();
	damage_ignore42 = variantMap[TEXT("damage_ignore")].GetValue<uint32>();
	magic_damage_ignore43 = variantMap[TEXT("magic_damage_ignore")].GetValue<uint32>();
	armor_ignore44 = variantMap[TEXT("armor_ignore")].GetValue<uint32>();
	magic_armor_ignore45 = variantMap[TEXT("magic_armor_ignore")].GetValue<uint32>();
	criticalstrike_ignore46 = variantMap[TEXT("criticalstrike_ignore")].GetValue<uint32>();
	parry_ignore47 = variantMap[TEXT("parry_ignore")].GetValue<uint32>();
	hitrate_ignore48 = variantMap[TEXT("hitrate_ignore")].GetValue<uint32>();
	dodgerate_ignore49 = variantMap[TEXT("dodgerate_ignore")].GetValue<uint32>();
	ice_damage_ignore50 = variantMap[TEXT("ice_damage_ignore")].GetValue<uint32>();
	fire_damage_ignore51 = variantMap[TEXT("fire_damage_ignore")].GetValue<uint32>();
	thunder_damage_ignore52 = variantMap[TEXT("thunder_damage_ignore")].GetValue<uint32>();
	xuan_damage_ignore53 = variantMap[TEXT("xuan_damage_ignore")].GetValue<uint32>();
	ice_armor_ignore54 = variantMap[TEXT("ice_armor_ignore")].GetValue<uint32>();
	fire_armor_ignore55 = variantMap[TEXT("fire_armor_ignore")].GetValue<uint32>();
	thunder_armor_ignore56 = variantMap[TEXT("thunder_armor_ignore")].GetValue<uint32>();
	xuan_armor_ignore57 = variantMap[TEXT("xuan_armor_ignore")].GetValue<uint32>();
	depress_resist58 = variantMap[TEXT("depress_resist")].GetValue<uint32>();
	hitback_resist59 = variantMap[TEXT("hitback_resist")].GetValue<uint32>();
	control_resist60 = variantMap[TEXT("control_resist")].GetValue<uint32>();
	insane_resist61 = variantMap[TEXT("insane_resist")].GetValue<uint32>();
	feats62 = variantMap[TEXT("feats")].GetValue<uint32>();
}

FVariant FROLE_PROPERTY_INFO::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("name"), name);
	variantMap.Add(TEXT("camp"), camp1);
	variantMap.Add(TEXT("gender"), gender2);
	variantMap.Add(TEXT("profession"), profession3);
	variantMap.Add(TEXT("level"), level4);
	variantMap.Add(TEXT("xiuwei"), xiuwei5);
	variantMap.Add(TEXT("jingjieLevel"), jingjieLevel6);
	variantMap.Add(TEXT("killingValue"), killingValue7);
	variantMap.Add(TEXT("potential"), potential8);
	variantMap.Add(TEXT("combatPower"), combatPower9);
	variantMap.Add(TEXT("strength"), strength10);
	variantMap.Add(TEXT("dexterity"), dexterity11);
	variantMap.Add(TEXT("intellect"), intellect12);
	variantMap.Add(TEXT("corporeity"), corporeity13);
	variantMap.Add(TEXT("discern"), discern14);
	variantMap.Add(TEXT("speed"), speed15);
	variantMap.Add(TEXT("HP"), HP16);
	variantMap.Add(TEXT("HP_Max"), HP_Max17);
	variantMap.Add(TEXT("MP"), MP18);
	variantMap.Add(TEXT("MP_Max"), MP_Max19);
	variantMap.Add(TEXT("gangQiValue"), gangQiValue20);
	variantMap.Add(TEXT("gangQiValue_Max"), gangQiValue_Max21);
	variantMap.Add(TEXT("damage"), damage22);
	variantMap.Add(TEXT("magic_damage"), magic_damage23);
	variantMap.Add(TEXT("armor"), armor24);
	variantMap.Add(TEXT("magic_armor"), magic_armor25);
	variantMap.Add(TEXT("gangQi_damagePoint"), gangQi_damagePoint26);
	variantMap.Add(TEXT("gangQi_armorPoint"), gangQi_armorPoint27);
	variantMap.Add(TEXT("criticalstrike"), criticalstrike28);
	variantMap.Add(TEXT("parry"), parry29);
	variantMap.Add(TEXT("hitrate"), hitrate30);
	variantMap.Add(TEXT("dodgerate"), dodgerate31);
	variantMap.Add(TEXT("healingrate"), healingrate32);
	variantMap.Add(TEXT("cure"), cure33);
	variantMap.Add(TEXT("ice_damage"), ice_damage34);
	variantMap.Add(TEXT("fire_damage"), fire_damage35);
	variantMap.Add(TEXT("thunder_damage"), thunder_damage36);
	variantMap.Add(TEXT("xuan_damage"), xuan_damage37);
	variantMap.Add(TEXT("ice_armor"), ice_armor38);
	variantMap.Add(TEXT("fire_armor"), fire_armor39);
	variantMap.Add(TEXT("thunder_armor"), thunder_armor40);
	variantMap.Add(TEXT("xuan_armor"), xuan_armor41);
	variantMap.Add(TEXT("damage_ignore"), damage_ignore42);
	variantMap.Add(TEXT("magic_damage_ignore"), magic_damage_ignore43);
	variantMap.Add(TEXT("armor_ignore"), armor_ignore44);
	variantMap.Add(TEXT("magic_armor_ignore"), magic_armor_ignore45);
	variantMap.Add(TEXT("criticalstrike_ignore"), criticalstrike_ignore46);
	variantMap.Add(TEXT("parry_ignore"), parry_ignore47);
	variantMap.Add(TEXT("hitrate_ignore"), hitrate_ignore48);
	variantMap.Add(TEXT("dodgerate_ignore"), dodgerate_ignore49);
	variantMap.Add(TEXT("ice_damage_ignore"), ice_damage_ignore50);
	variantMap.Add(TEXT("fire_damage_ignore"), fire_damage_ignore51);
	variantMap.Add(TEXT("thunder_damage_ignore"), thunder_damage_ignore52);
	variantMap.Add(TEXT("xuan_damage_ignore"), xuan_damage_ignore53);
	variantMap.Add(TEXT("ice_armor_ignore"), ice_armor_ignore54);
	variantMap.Add(TEXT("fire_armor_ignore"), fire_armor_ignore55);
	variantMap.Add(TEXT("thunder_armor_ignore"), thunder_armor_ignore56);
	variantMap.Add(TEXT("xuan_armor_ignore"), xuan_armor_ignore57);
	variantMap.Add(TEXT("feats"), feats62);

	return FVariant(variantMap);
}

FEQUIP_INTENSIFY_SAVE::FEQUIP_INTENSIFY_SAVE()
{

}

FEQUIP_INTENSIFY_SAVE::FEQUIP_INTENSIFY_SAVE(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	index1 = variantMap[TEXT("index")].GetValue<int32>();
	EquipUID2 = variantMap[TEXT("EquipUID")].GetValue<uint64>();
	EquipID3 = variantMap[TEXT("EquipID")].GetValue<int32>();
	intensifyDataStr4 = variantMap[TEXT("intensifyDataStr")].GetValue<FString>();

}

FVariant FEQUIP_INTENSIFY_SAVE::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("index"), index1);
	variantMap.Add(TEXT("EquipUID"), EquipUID2);
	variantMap.Add(TEXT("EquipID"), EquipID3);
	variantMap.Add(TEXT("intensifyDataStr"), intensifyDataStr4);

	return FVariant(variantMap);
}

FEQUIP_INTENSIFY_SAVES::FEQUIP_INTENSIFY_SAVES()
{

}

FEQUIP_INTENSIFY_SAVES::FEQUIP_INTENSIFY_SAVES(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_datas1 = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_datas1)
	{
		FEQUIP_INTENSIFY_SAVE element1 = FEQUIP_INTENSIFY_SAVE(elementVariant0);
		datas1.Add(element1);
	}

}

FVariant FEQUIP_INTENSIFY_SAVES::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_datas1.Add(element1);
	}
	variantMap.Add(TEXT("datas"), variantArray_datas1);

	return FVariant(variantMap);
}

FNPCSHOP_ITEM::FNPCSHOP_ITEM()
{

}

FNPCSHOP_ITEM::FNPCSHOP_ITEM(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id1 = variantMap[TEXT("id")].GetValue<FString>();
	amount2 = variantMap[TEXT("amount")].GetValue<int32>();
	startTime3 = variantMap[TEXT("startTime")].GetValue<double>();

}

FVariant FNPCSHOP_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id1);
	variantMap.Add(TEXT("amount"), amount2);
	variantMap.Add(TEXT("startTime"), startTime3);

	return FVariant(variantMap);
}

FNPCSHOP_ITEM_LIST::FNPCSHOP_ITEM_LIST()
{

}

FNPCSHOP_ITEM_LIST::FNPCSHOP_ITEM_LIST(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_items1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_items1)
	{
		FNPCSHOP_ITEM element1 = FNPCSHOP_ITEM(elementVariant0);
		items1.Add(element1);
	}

}

FVariant FNPCSHOP_ITEM_LIST::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_items1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : items1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_items1.Add(element1);
	}
	variantMap.Add(TEXT("items"), variantArray_items1);

	return FVariant(variantMap);
}
FDRUP_SOUL_DATA::FDRUP_SOUL_DATA()
{

}

FDRUP_SOUL_DATA::FDRUP_SOUL_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id1 = variantMap[TEXT("id")].GetValue<int32>();
	sellPrice2 = variantMap[TEXT("sellPrice")].GetValue<int32>();
	buyPrice3 = variantMap[TEXT("buyPrice")].GetValue<int32>();

}

FVariant FDRUP_SOUL_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id1);
	variantMap.Add(TEXT("sellPrice"), sellPrice2);
	variantMap.Add(TEXT("buyPrice"), buyPrice3);

	return FVariant(variantMap);
}

FSTOREGOODS::FSTOREGOODS()
{

}

FSTOREGOODS::FSTOREGOODS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	ID1 = variantMap[TEXT("ID")].GetValue<int32>();
	GoodsType2 = variantMap[TEXT("GoodsType")].GetValue<int32>();
	GoodsState3 = variantMap[TEXT("GoodsState")].GetValue<int32>();
	ItemType4 = variantMap[TEXT("ItemType")].GetValue<int32>();
	ItemID5 = variantMap[TEXT("ItemID")].GetValue<int32>();
	Price6 = variantMap[TEXT("Price")].GetValue<int32>();
	LimitTime7 = variantMap[TEXT("LimitTime")].GetValue<FString>();
	LimitAmount8 = variantMap[TEXT("LimitAmount")].GetValue<int32>();
	ServeLimitAmount9 = variantMap[TEXT("ServeLimitAmount")].GetValue<int32>();
	DiscountTime10 = variantMap[TEXT("DiscountTime")].GetValue<FString>();
	DiscountPrice11 = variantMap[TEXT("DiscountPrice")].GetValue<int32>();
	RefreshType12 = variantMap[TEXT("RefreshType")].GetValue<int32>();
	Description13 = variantMap[TEXT("Description")].GetValue<FString>();
	ThirdLable14 = variantMap[TEXT("ThirdLable")].GetValue<int32>();
	RebateRate15 = variantMap[TEXT("RebateRate")].GetValue<float>();

}

FVariant FSTOREGOODS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("ID"), ID1);
	variantMap.Add(TEXT("GoodsType"), GoodsType2);
	variantMap.Add(TEXT("GoodsState"), GoodsState3);
	variantMap.Add(TEXT("ItemType"), ItemType4);
	variantMap.Add(TEXT("ItemID"), ItemID5);
	variantMap.Add(TEXT("Price"), Price6);
	variantMap.Add(TEXT("LimitTime"), LimitTime7);
	variantMap.Add(TEXT("LimitAmount"), LimitAmount8);
	variantMap.Add(TEXT("ServeLimitAmount"), ServeLimitAmount9);
	variantMap.Add(TEXT("DiscountTime"), DiscountTime10);
	variantMap.Add(TEXT("DiscountPrice"), DiscountPrice11);
	variantMap.Add(TEXT("RefreshType"), RefreshType12);
	variantMap.Add(TEXT("Description"), Description13);
	variantMap.Add(TEXT("ThirdLable"), ThirdLable14);
	variantMap.Add(TEXT("RebateRate"), RebateRate15);

	return FVariant(variantMap);
}

FSTOREGOODS_DICT::FSTOREGOODS_DICT()
{

}

FSTOREGOODS_DICT::FSTOREGOODS_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("Datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FSTOREGOODS element1 = FSTOREGOODS(elementVariant0);
		Datas1.Add(element1);
	}

}

FVariant FSTOREGOODS_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : Datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("Datas"), variantArray_Datas1);

	return FVariant(variantMap);
}

FLIMIT_GOODS::FLIMIT_GOODS()
{

}

FLIMIT_GOODS::FLIMIT_GOODS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id1 = variantMap[TEXT("id")].GetValue<int32>();
	amount2 = variantMap[TEXT("amount")].GetValue<int32>();
	startTime3 = variantMap[TEXT("startTime")].GetValue<double>();

}

FVariant FLIMIT_GOODS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id1);
	variantMap.Add(TEXT("amount"), amount2);
	variantMap.Add(TEXT("startTime"), startTime3);

	return FVariant(variantMap);
}

FSERVERLIMIT_GOODS_LIST::FSERVERLIMIT_GOODS_LIST()
{

}

FSERVERLIMIT_GOODS_LIST::FSERVERLIMIT_GOODS_LIST(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_items1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_items1)
	{
		FLIMIT_GOODS element1 = FLIMIT_GOODS(elementVariant0);
		items1.Add(element1);
	}

}

FVariant FSERVERLIMIT_GOODS_LIST::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_items1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : items1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_items1.Add(element1);
	}
	variantMap.Add(TEXT("items"), variantArray_items1);

	return FVariant(variantMap);
}

FPLAYERLIMIT_GOODS::FPLAYERLIMIT_GOODS()
{

}

FPLAYERLIMIT_GOODS::FPLAYERLIMIT_GOODS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	playerDbid1 = variantMap[TEXT("playerDbid")].GetValue<uint64>();
	KBEngine::FVariantArray variantArray_limitGoods2 = variantMap[TEXT("limitGoods")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_limitGoods2)
	{
		FLIMIT_GOODS element1 = FLIMIT_GOODS(elementVariant0);
		limitGoods2.Add(element1);
	}

}

FVariant FPLAYERLIMIT_GOODS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("playerDbid"), playerDbid1);
	KBEngine::FVariantArray variantArray_limitGoods2 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : limitGoods2)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_limitGoods2.Add(element1);
	}
	variantMap.Add(TEXT("limitGoods"), variantArray_limitGoods2);

	return FVariant(variantMap);
}

FPLAYERLIMIT_GOODS_LIST::FPLAYERLIMIT_GOODS_LIST()
{

}

FPLAYERLIMIT_GOODS_LIST::FPLAYERLIMIT_GOODS_LIST(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_items1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_items1)
	{
		FPLAYERLIMIT_GOODS element1 = FPLAYERLIMIT_GOODS(elementVariant0);
		items1.Add(element1);
	}

}

FVariant FPLAYERLIMIT_GOODS_LIST::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_items1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : items1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_items1.Add(element1);
	}
	variantMap.Add(TEXT("items"), variantArray_items1);

	return FVariant(variantMap);
}

FSTORE_BUY_RECORD::FSTORE_BUY_RECORD()
{

}

FSTORE_BUY_RECORD::FSTORE_BUY_RECORD(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	goodsID1 = variantMap[TEXT("goodsID")].GetValue<int32>();
	amount2 = variantMap[TEXT("amount")].GetValue<int32>();
	buyTime3 = variantMap[TEXT("buyTime")].GetValue<FString>();
	uid4 = variantMap[TEXT("uid")].GetValue<FString>();
	price5 = variantMap[TEXT("price")].GetValue<int32>();
	goodsType6 = variantMap[TEXT("goodsType")].GetValue<int32>();
	itemID7 = variantMap[TEXT("itemID")].GetValue<int32>();

}

FVariant FSTORE_BUY_RECORD::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("goodsID"), goodsID1);
	variantMap.Add(TEXT("amount"), amount2);
	variantMap.Add(TEXT("buyTime"), buyTime3);
	variantMap.Add(TEXT("uid"), uid4);
	variantMap.Add(TEXT("price"), price5);
	variantMap.Add(TEXT("goodsType"), goodsType6);
	variantMap.Add(TEXT("itemID"), itemID7);

	return FVariant(variantMap);
}

FSTORE_BUY_RECORD_DICT::FSTORE_BUY_RECORD_DICT()
{

}

FSTORE_BUY_RECORD_DICT::FSTORE_BUY_RECORD_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("Datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FSTORE_BUY_RECORD element1 = FSTORE_BUY_RECORD(elementVariant0);
		Datas1.Add(element1);
	}

}

FVariant FSTORE_BUY_RECORD_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : Datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("Datas"), variantArray_Datas1);

	return FVariant(variantMap);
}

FSTORE_PRESENT_RECORD::FSTORE_PRESENT_RECORD()
{

}

FSTORE_PRESENT_RECORD::FSTORE_PRESENT_RECORD(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	goodsID1 = variantMap[TEXT("goodsID")].GetValue<int32>();
	amount2 = variantMap[TEXT("amount")].GetValue<int32>();
	buyTime3 = variantMap[TEXT("buyTime")].GetValue<FString>();
	sender4 = variantMap[TEXT("sender")].GetValue<FString>();
	receiver5 = variantMap[TEXT("receiver")].GetValue<FString>();
	uid6 = variantMap[TEXT("uid")].GetValue<FString>();
	price7 = variantMap[TEXT("price")].GetValue<int32>();
	receiverDBID8 = variantMap[TEXT("receiverDBID")].GetValue<FString>();
	senderDBID9 = variantMap[TEXT("senderDBID")].GetValue<FString>();
	itemID10 = variantMap[TEXT("itemID")].GetValue<int32>();

}

FVariant FSTORE_PRESENT_RECORD::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("goodsID"), goodsID1);
	variantMap.Add(TEXT("amount"), amount2);
	variantMap.Add(TEXT("buyTime"), buyTime3);
	variantMap.Add(TEXT("sender"), sender4);
	variantMap.Add(TEXT("receiver"), receiver5);
	variantMap.Add(TEXT("uid"), uid6);
	variantMap.Add(TEXT("price"), price7);
	variantMap.Add(TEXT("receiverDBID"), receiverDBID8);
	variantMap.Add(TEXT("senderDBID"), senderDBID9);
	variantMap.Add(TEXT("itemID"), itemID10);

	return FVariant(variantMap);
}

FSTORE_PRESENT_RECORD_DICT::FSTORE_PRESENT_RECORD_DICT()
{

}

FSTORE_PRESENT_RECORD_DICT::FSTORE_PRESENT_RECORD_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("Datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FSTORE_PRESENT_RECORD element1 = FSTORE_PRESENT_RECORD(elementVariant0);
		Datas1.Add(element1);
	}

}

FVariant FSTORE_PRESENT_RECORD_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : Datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("Datas"), variantArray_Datas1);

	return FVariant(variantMap);
}

FSTORE_GIFT_BOX_DATA::FSTORE_GIFT_BOX_DATA()
{

}

FSTORE_GIFT_BOX_DATA::FSTORE_GIFT_BOX_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	goodsID1 = variantMap[TEXT("goodsID")].GetValue<int32>();
	amount2 = variantMap[TEXT("amount")].GetValue<int32>();
	receiverName3 = variantMap[TEXT("receiverName")].GetValue<FString>();
	receiverDBID4 = variantMap[TEXT("receiverDBID")].GetValue<FString>();
	senderName5 = variantMap[TEXT("senderName")].GetValue<FString>();
	senderDBID6 = variantMap[TEXT("senderDBID")].GetValue<FString>();
	endTime7 = variantMap[TEXT("endTime")].GetValue<FString>();
	giftState8 = variantMap[TEXT("giftState")].GetValue<int32>();
	message9 = variantMap[TEXT("message")].GetValue<FString>();
	uid10 = variantMap[TEXT("uid")].GetValue<FString>();
	overtime11 = variantMap[TEXT("overtime")].GetValue<FString>();
	price12 = variantMap[TEXT("price")].GetValue<int32>();
	itemID13 = variantMap[TEXT("itemID")].GetValue<int32>();

}

FVariant FSTORE_GIFT_BOX_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("goodsID"), goodsID1);
	variantMap.Add(TEXT("amount"), amount2);
	variantMap.Add(TEXT("receiverName"), receiverName3);
	variantMap.Add(TEXT("receiverDBID"), receiverDBID4);
	variantMap.Add(TEXT("senderName"), senderName5);
	variantMap.Add(TEXT("senderDBID"), senderDBID6);
	variantMap.Add(TEXT("endTime"), endTime7);
	variantMap.Add(TEXT("giftState"), giftState8);
	variantMap.Add(TEXT("message"), message9);
	variantMap.Add(TEXT("uid"), uid10);
	variantMap.Add(TEXT("overtime"), overtime11);
	variantMap.Add(TEXT("price"), price12);
	variantMap.Add(TEXT("itemID"), itemID13);

	return FVariant(variantMap);
}

FSTORE_GIFT_BOX_DATA_DICT::FSTORE_GIFT_BOX_DATA_DICT()
{

}

FSTORE_GIFT_BOX_DATA_DICT::FSTORE_GIFT_BOX_DATA_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("Datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FSTORE_GIFT_BOX_DATA element1 = FSTORE_GIFT_BOX_DATA(elementVariant0);
		Datas1.Add(element1);
	}

}

FVariant FSTORE_GIFT_BOX_DATA_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : Datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("Datas"), variantArray_Datas1);

	return FVariant(variantMap);
}

FSTORE_CART_DATA::FSTORE_CART_DATA()
{

}

FSTORE_CART_DATA::FSTORE_CART_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	goodsType1 = variantMap[TEXT("goodsType")].GetValue<int32>();
	goodsID2 = variantMap[TEXT("goodsID")].GetValue<int32>();
	amount3 = variantMap[TEXT("amount")].GetValue<int32>();

}

FVariant FSTORE_CART_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("goodsType"), goodsType1);
	variantMap.Add(TEXT("goodsID"), goodsID2);
	variantMap.Add(TEXT("amount"), amount3);

	return FVariant(variantMap);
}

FSTORE_CART_DATA_DICT::FSTORE_CART_DATA_DICT()
{

}

FSTORE_CART_DATA_DICT::FSTORE_CART_DATA_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("Datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FSTORE_CART_DATA element1 = FSTORE_CART_DATA(elementVariant0);
		Datas1.Add(element1);
	}

}

FVariant FSTORE_CART_DATA_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : Datas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("Datas"), variantArray_Datas1);

	return FVariant(variantMap);
}

FPASSIVE_SKILL_BAR_DATA::FPASSIVE_SKILL_BAR_DATA()
{
}

FPASSIVE_SKILL_BAR_DATA::FPASSIVE_SKILL_BAR_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	skillID = variantMap[TEXT("skillID")].GetValue<int32>();
	isLock = variantMap[TEXT("isLock")].GetValue<uint8>();
}

FVariant FPASSIVE_SKILL_BAR_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id);
	variantMap.Add(TEXT("skillID"), skillID);
	variantMap.Add(TEXT("isLock"), isLock);

	return FVariant(variantMap);
}


FPASSIVE_SKILL_BAR_DATAS::FPASSIVE_SKILL_BAR_DATAS()
{
}

FPASSIVE_SKILL_BAR_DATAS::FPASSIVE_SKILL_BAR_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FPASSIVE_SKILL_BAR_DATA element1 = FPASSIVE_SKILL_BAR_DATA(elementVariant0);
		datas.Add(element1);
	}
}

FVariant FPASSIVE_SKILL_BAR_DATAS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("items"), variantArray_Datas1);

	return FVariant(variantMap);
}

REMIND_CROND_DATA::REMIND_CROND_DATA()
{
}

REMIND_CROND_DATA::REMIND_CROND_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	scriptID = variantMap[TEXT("scriptID")].GetValue<FString>();
	remindType = variantMap[TEXT("remindType")].GetValue<uint8>();
}

REMIND_CROND_DATAS::REMIND_CROND_DATAS()
{
}

REMIND_CROND_DATAS::REMIND_CROND_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		REMIND_CROND_DATA element1 = REMIND_CROND_DATA(elementVariant0);
		datas.Add(element1);
	}
}
TEMP_ITEM_DATA::TEMP_ITEM_DATA()
{

}
TEMP_ITEM_DATA::TEMP_ITEM_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<FString>();
	itemID = variantMap[TEXT("itemID")].GetValue<int32>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	price = variantMap[TEXT("price")].GetValue<int32>();
}
void TEMP_ITEM_DATA::CreateFromVariant(const FVariant& val, TEMP_ITEM_DATA& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.id = m[TEXT("id")].GetValue<FString>();
	out.amount = m[TEXT("amount")].GetValue<int32>();
	out.itemID = m[TEXT("itemID")].GetValue<int32>();
	out.price = m[TEXT("price")].GetValue<int32>();
}

void BUY_ITEM_RECORD_DATA::CreateFromVariant(const FVariant& val, BUY_ITEM_RECORD_DATA& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.stallName = m[TEXT("stallName")].GetValue<FString>();
	out.itemName = m[TEXT("itemName")].GetValue<FString>();
	out.amount = m[TEXT("amount")].GetValue<int32>();
	out.totalPrice = m[TEXT("totalPrice")].GetValue<int32>();
}

void TEMP_SELL_RECORD_DATA::CreateFromVariant(const FVariant& val, TEMP_SELL_RECORD_DATA& out)
{
	auto m = val.GetValue<KBEngine::FVariantMap>();
	out.itemName = m[TEXT("itemName")].GetValue<FString>();
	out.playerName = m[TEXT("playerName")].GetValue<FString>();
	out.amount = m[TEXT("amount")].GetValue<int32>();
	out.tax = m[TEXT("tax")].GetValue<int32>();
	out.totalPrice = m[TEXT("totalPrice")].GetValue<int32>();
	out.time = m[TEXT("time")].GetValue<FString>();
}
SELL_ITEM_DATA::SELL_ITEM_DATA()
{

}
SELL_ITEM_DATA::SELL_ITEM_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	itemID = variantMap[TEXT("itemID")].GetValue<int32>();
	id = variantMap[TEXT("id")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	price = variantMap[TEXT("price")].GetValue<int32>();
	combatPower = variantMap[TEXT("combatPower")].GetValue<int32>();
	attackPropertiesStr = variantMap[TEXT("attackPropertiesStr")].GetValue<FString>();
	attachPropertiesStr = variantMap[TEXT("attachPropertiesStr")].GetValue<FString>();
	intensifyDataStr = variantMap[TEXT("intensifyDataStr")].GetValue<FString>();
	hardiness = variantMap[TEXT("hardiness")].GetValue<int32>();
}

BUY_AND_SELL_DATAS::BUY_AND_SELL_DATAS()
{

}
BUY_AND_SELL_DATAS::BUY_AND_SELL_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("stallCollectionItemList")].GetValue<KBEngine::FVariantArray>();
	KBEngine::FVariantArray variantArray_Datas2 = variantMap[TEXT("stallSellItemList")].GetValue<KBEngine::FVariantArray>();

	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		TEMP_ITEM_DATA element1 = TEMP_ITEM_DATA(elementVariant0);
		stallCollectionItemList.Add(element1);
	}
	for (FVariant& elementVariant1 : variantArray_Datas2)
	{
		SELL_ITEM_DATA element1 = SELL_ITEM_DATA(elementVariant1);
		stallSellItemList.Add(element1);
	}
}
ON_REQUEST_STALL_ITEMS_DATAS::ON_REQUEST_STALL_ITEMS_DATAS()
{

}
ON_REQUEST_STALL_ITEMS_DATAS::ON_REQUEST_STALL_ITEMS_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("stallCollectionItemList")].GetValue<KBEngine::FVariantArray>();
	KBEngine::FVariantArray variantArray_Datas2 = variantMap[TEXT("stallSellItemList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		TEMP_ITEM_DATA element1 = TEMP_ITEM_DATA(elementVariant0);
		stallCollectionItemList.Add(element1);
	}
	for (FVariant& elementVariant1 : variantArray_Datas2)
	{
		TEMP_ITEM_DATA element1 = TEMP_ITEM_DATA(elementVariant1);
		stallSellItemList.Add(element1);
	}
}

PET_PERSISTENT_DATA::PET_PERSISTENT_DATA()
{

}
PET_PERSISTENT_DATA::PET_PERSISTENT_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<uint64>();
	scriptID = variantMap[TEXT("scriptID")].GetValue<FString>();
	name = variantMap[TEXT("name")].GetValue<FString>();
	uname = variantMap[TEXT("uname")].GetValue<FString>();
	camp = variantMap[TEXT("camp")].GetValue<uint16>();
	level = variantMap[TEXT("level")].GetValue<uint16>();
	takeLevel = variantMap[TEXT("takeLevel")].GetValue<uint16>();
	ability = variantMap[TEXT("ability")].GetValue<uint16>();
	ability_Max = variantMap[TEXT("ability_Max")].GetValue<uint16>();
	step = variantMap[TEXT("step")].GetValue<uint8>();
	exp = variantMap[TEXT("exp")].GetValue<int32>();
	quality = variantMap[TEXT("quality")].GetValue<uint8>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("attrSkillBox")].GetValue<KBEngine::FVariantArray>();
	KBEngine::FVariantArray variantArray_Datas2 = variantMap[TEXT("passiveSkillBox")].GetValue<KBEngine::FVariantArray>();
	KBEngine::FVariantArray variantArray_Datas3 = variantMap[TEXT("noLearnedSkillBox")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		int32 element1 = int32(elementVariant0);
		attrSkillBox.Add(element1);
	}
	for (FVariant& elementVariant0 : variantArray_Datas2)
	{
		int32 element1 = int32(elementVariant0);
		passiveSkillBox.Add(element1);
	}
	for (FVariant& elementVariant0 : variantArray_Datas3)
	{
		int32 element1 = int32(elementVariant0);
		noLearnedSkillBox.Add(element1);
	}
	sleepTime = variantMap[TEXT("sleepTime")].GetValue<uint64>();
	corporeity = variantMap[TEXT("corporeity")].GetValue<uint32>();
	strength = variantMap[TEXT("strength")].GetValue<uint32>();
	intellect = variantMap[TEXT("intellect")].GetValue<uint32>();
	discern = variantMap[TEXT("discern")].GetValue<uint32>();
	dexterity = variantMap[TEXT("dexterity")].GetValue<uint32>();
	HP = variantMap[TEXT("HP")].GetValue<uint32>();
	MP = variantMap[TEXT("MP")].GetValue<uint32>();
	HP_Max = variantMap[TEXT("HP_Max")].GetValue<uint32>();
	MP_Max = variantMap[TEXT("MP_Max")].GetValue<uint32>();
	damage = variantMap[TEXT("damage")].GetValue<uint32>();
	magic_damage = variantMap[TEXT("magic_damage")].GetValue<uint32>();
	magic_armor = variantMap[TEXT("magic_armor")].GetValue<uint32>();
	criticalstrike = variantMap[TEXT("criticalstrike")].GetValue<uint32>();
	parry = variantMap[TEXT("parry")].GetValue<uint32>();
	speed = variantMap[TEXT("speed")].GetValue<uint32>();
	hitrate = variantMap[TEXT("hitrate")].GetValue<uint32>();
	dodgerate = variantMap[TEXT("dodgerate")].GetValue<uint32>();
	gangQiValue = variantMap[TEXT("gangQiValue")].GetValue<uint32>();
	gangQiValue_Max = variantMap[TEXT("gangQiValue_Max")].GetValue<uint32>();
	gangQiState = variantMap[TEXT("gangQiState")].GetValue<uint32>();
	gangQi_damagePoint = variantMap[TEXT("gangQi_damagePoint")].GetValue<uint32>();
	gangQi_armorPoint = variantMap[TEXT("gangQi_armorPoint")].GetValue<uint32>();
	gangQi_qiJieRevive = variantMap[TEXT("gangQi_qiJieRevive")].GetValue<uint32>();
	gangQi_qiYingRevive = variantMap[TEXT("gangQi_qiYingRevive")].GetValue<uint32>();
	combatPower = variantMap[TEXT("combatPower")].GetValue<uint32>();
	cure = variantMap[TEXT("cure")].GetValue<int32>();

	ice_damage = variantMap[TEXT("ice_damage")].GetValue<uint32>();
	fire_damage = variantMap[TEXT("fire_damage")].GetValue<uint32>();
	thunder_damage = variantMap[TEXT("thunder_damage")].GetValue<uint32>();
	xuan_damage = variantMap[TEXT("xuan_damage")].GetValue<uint32>();
	ice_armor = variantMap[TEXT("ice_armor")].GetValue<uint32>();
	fire_armor = variantMap[TEXT("fire_armor")].GetValue<uint32>();
	thunder_armor = variantMap[TEXT("thunder_armor")].GetValue<uint32>();
	xuan_armor = variantMap[TEXT("xuan_armor")].GetValue<uint32>();

	damage_ignore = variantMap[TEXT("damage_ignore")].GetValue<uint32>();
	magic_damage_ignore = variantMap[TEXT("magic_damage_ignore")].GetValue<uint32>();
	armor_ignore = variantMap[TEXT("armor_ignore")].GetValue<uint32>();
	magic_armor_ignore = variantMap[TEXT("magic_armor_ignore")].GetValue<uint32>();
	criticalstrike_ignore = variantMap[TEXT("criticalstrike_ignore")].GetValue<uint32>();
	parry_ignore = variantMap[TEXT("parry_ignore")].GetValue<uint32>();
	hitrate_ignore = variantMap[TEXT("hitrate_ignore")].GetValue<uint32>();
	dodgerate_ignore = variantMap[TEXT("dodgerate_ignore")].GetValue<uint32>();

	ice_damage_ignore = variantMap[TEXT("ice_damage_ignore")].GetValue<uint32>();
	fire_damage_ignore = variantMap[TEXT("fire_damage_ignore")].GetValue<uint32>();
	thunder_damage_ignore = variantMap[TEXT("thunder_damage_ignore")].GetValue<uint32>();
	xuan_damage_ignore = variantMap[TEXT("xuan_damage_ignore")].GetValue<uint32>();
	ice_armor_ignore = variantMap[TEXT("ice_armor_ignore")].GetValue<uint32>();
	fire_armor_ignore = variantMap[TEXT("fire_armor_ignore")].GetValue<uint32>();
	thunder_armor_ignore = variantMap[TEXT("thunder_armor_ignore")].GetValue<uint32>();
	xuan_armor_ignore = variantMap[TEXT("xuan_armor_ignore")].GetValue<uint32>();

	depress_resist = variantMap[TEXT("depress_resist")].GetValue<uint32>();
	hitback_resist = variantMap[TEXT("hitback_resist")].GetValue<uint32>();
	control_resist = variantMap[TEXT("control_resist")].GetValue<uint32>();
	insane_resist = variantMap[TEXT("insane_resist")].GetValue<uint32>();
	KBEngine::FVariantArray variantArray_petShenTongSKill = variantMap[TEXT("petShenTongSKill")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_petShenTongSKill)
	{
		FDICT_INT_INT_ITEM element1 = FDICT_INT_INT_ITEM(elementVariant0);
		petShenTongSKill.Add(element1);
	}
}

BUY_BACK_ITEM_DATA::BUY_BACK_ITEM_DATA()
{

}
BUY_BACK_ITEM_DATA::BUY_BACK_ITEM_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	bindType = variantMap[TEXT("bindType")].GetValue<int32>();
	combatPower = variantMap[TEXT("combatPower")].GetValue<int32>();
	attackPropertiesStr = variantMap[TEXT("attackPropertiesStr")].GetValue<FString>();
	attachPropertiesStr = variantMap[TEXT("attachPropertiesStr")].GetValue<FString>();
	intensifyDataStr = variantMap[TEXT("intensifyDataStr")].GetValue<FString>();
	hardiness = variantMap[TEXT("hardiness")].GetValue<int32>();
}

BUY_BACK_ITEM_DATAS::BUY_BACK_ITEM_DATAS()
{

}
BUY_BACK_ITEM_DATAS::BUY_BACK_ITEM_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("buyBackItemDataList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		BUY_BACK_ITEM_DATA element1 = BUY_BACK_ITEM_DATA(elementVariant0);
		buyBackItemDataList.Add(element1);
	}

}

SIMPLE_ITEM_DICT::SIMPLE_ITEM_DICT()
{

}
SIMPLE_ITEM_DICT::SIMPLE_ITEM_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	uid = variantMap[TEXT("uid")].GetValue<uint64>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	bindType = variantMap[TEXT("bindType")].GetValue<int32>();
	dynamicData = variantMap[TEXT("dynamicData")].GetValue<FString>();

}


CATALOG_DATA::CATALOG_DATA()
{

}
CATALOG_DATA::CATALOG_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	relationIndex = variantMap[TEXT("relationIndex")].GetValue<int32>();
	catalogName = variantMap[TEXT("catalogName")].GetValue<FString>();
	KBEngine::FVariantArray variantArray_catalogList1 = variantMap[TEXT("catalogList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_catalogList1)
	{
		uint64 element1 = elementVariant0.GetValue<uint64>();
		catalogList.Add(element1);
	}
}

RELATION_CATALOG_DATA::RELATION_CATALOG_DATA()
{

}
RELATION_CATALOG_DATA::RELATION_CATALOG_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("RelationCatalogDatas")].GetValue<KBEngine::FVariantArray>();

	for (FVariant& elementVariant0 : variantArray_Data)
	{
		CATALOG_DATA element1 = CATALOG_DATA(elementVariant0);
		RelationCatalogDatas.Add(element1);
	}
}

FSIGN_DATA::FSIGN_DATA()
{

}
FSIGN_DATA::FSIGN_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("dayList")].GetValue<KBEngine::FVariantArray>();
	yearMonth = variantMap[TEXT("yearMonth")].GetValue<int32>();
	for (FVariant& elementVariant0 : variantArray_Data)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		dayList.Add(element1);
	}
}

FSIGN_DATAS::FSIGN_DATAS()
{

}
FSIGN_DATAS::FSIGN_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("signDatas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Data)
	{
		FSIGN_DATA element1 = FSIGN_DATA(elementVariant0);
		signDatas.Add(element1);
	}
}

FPICK_UP_ITEM_DATA::FPICK_UP_ITEM_DATA()
{

}
FPICK_UP_ITEM_DATA::FPICK_UP_ITEM_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	bindType = variantMap[TEXT("bindType")].GetValue<int32>();
	quality = variantMap[TEXT("quality")].GetValue<int32>();
	dynamicData = variantMap[TEXT("dynamicData")].GetValue<FString>();
}

FPICK_UP_ITEM_DATAS::FPICK_UP_ITEM_DATAS()
{

}
FPICK_UP_ITEM_DATAS::FPICK_UP_ITEM_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("pickUpItemList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Data)
	{
		FPICK_UP_ITEM_DATA element1 = FPICK_UP_ITEM_DATA(elementVariant0);
		pickUpItemList.Add(element1);
	}
}

MAIL_DATA::MAIL_DATA()
{

}
MAIL_DATA::MAIL_DATA(const FVariant& variant )
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<uint64>();
	title = variantMap[TEXT("title")].GetValue<FString>();
	content = variantMap[TEXT("content")].GetValue<FString>();
	money = variantMap[TEXT("money")].GetValue<int64>();
	senderName = variantMap[TEXT("senderName")].GetValue<FString>();
	receiverName = variantMap[TEXT("receiverName")].GetValue<FString>();
	senderType = variantMap[TEXT("senderType")].GetValue<int32>();
	receiveTime = variantMap[TEXT("receiveTime")].GetValue<uint64>();
	remainTime = variantMap[TEXT("remainTime")].GetValue<int32>();
	isTaken = variantMap[TEXT("isTaken")].GetValue<int32>();
	isRead = variantMap[TEXT("isRead")].GetValue<int32>();
	isUpper = variantMap[TEXT("isUpper")].GetValue<int32>();
	lingshi = variantMap[TEXT("lingshi")].GetValue<int32>();
	xianshi = variantMap[TEXT("xianshi")].GetValue<int32>();
	bindMoney = variantMap[TEXT("bindMoney")].GetValue<int64>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("itemList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Data)
	{
		SIMPLE_ITEM_DICT element1 = SIMPLE_ITEM_DICT(elementVariant0);
		itemList.Add(element1);
	}
}
FCHAT_PAGESETTINGS::FCHAT_PAGESETTINGS()
{

}
FCHAT_PAGESETTINGS::FCHAT_PAGESETTINGS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	pageType = variantMap[TEXT("pageType")].GetValue<int8>();
	isDeletable = variantMap[TEXT("isDeletable")].GetValue<int8>();
	isDraggable = variantMap[TEXT("isDraggable")].GetValue<int8>();
	pageName = variantMap[TEXT("pageName")].GetValue<FString>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("channelList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Data)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		channelList.Add(element1);
	}
}

FCHAT_PAGESETTINGS_DATAS::FCHAT_PAGESETTINGS_DATAS()
{

}

FCHAT_PAGESETTINGS_DATAS::FCHAT_PAGESETTINGS_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Data)
	{
		FCHAT_PAGESETTINGS element1 = FCHAT_PAGESETTINGS(elementVariant0 );
		datas.Add(element1);
	}
}
FCHAT_PARMS_DATA::FCHAT_PARMS_DATA()
{

}
FCHAT_PARMS_DATA::FCHAT_PARMS_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key = variantMap[TEXT("key")].GetValue<FString>();
	value = variantMap[TEXT("value")].GetValue<int32>();
}
FCHAT_DATA::FCHAT_DATA()
{

}
FCHAT_DATA::FCHAT_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	playerDBID = variantMap[TEXT("playerDBID")].GetValue<uint64>();
	name = variantMap[TEXT("name")].GetValue<FString>();
	type = variantMap[TEXT("type")].GetValue<int8>();
	entityType = variantMap[TEXT("entityType")].GetValue<int8>();
	message = variantMap[TEXT("message")].GetValue<FString>();
	KBEngine::FVariantArray variantArray_richText = variantMap[TEXT("richText")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_richText)
	{
		FString element1 = elementVariant0.GetValue<FString>();
		richText.Add(element1);
	}
	KBEngine::FVariantArray variantArray_parms = variantMap[TEXT("parms")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_richText)
	{
		FCHAT_PARMS_DATA element1 = FCHAT_PARMS_DATA(elementVariant0);
		parms.Add(element1);
	}
}

FCOUPON_ITEM::FCOUPON_ITEM()
{

}

FCOUPON_ITEM::FCOUPON_ITEM(const FVariant& variant )
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	couponId = variantMap[TEXT("couponId")].GetValue<FString>();
	uid = variantMap[TEXT("uid")].GetValue<uint64>();
	createTime = variantMap[TEXT("createTime")].GetValue<double>();
}

FCOUPON_ITEM_LIST::FCOUPON_ITEM_LIST()
{

}
FCOUPON_ITEM_LIST::FCOUPON_ITEM_LIST(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_richText = variantMap[TEXT("couponItems")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_richText)
	{
		FCOUPON_ITEM element1 = FCOUPON_ITEM(elementVariant0);
		couponItems.Add(element1);
	}
}

FGIFT_GOODS_DATA::FGIFT_GOODS_DATA()
{

}
FGIFT_GOODS_DATA::FGIFT_GOODS_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();
	itemID = variantMap[TEXT("itemID")].GetValue<int32>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	itemName = variantMap[TEXT("itemName")].GetValue<FString>();
	playerName = variantMap[TEXT("playerName")].GetValue<FString>();
	state = variantMap[TEXT("state")].GetValue<int32>();
	time = variantMap[TEXT("time")].GetValue<FString>();
}

RECALL_GIFT_DATA::RECALL_GIFT_DATA()
{

}

RECALL_GIFT_DATA::RECALL_GIFT_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();;
	state = variantMap[TEXT("state")].GetValue<int32>();
	changeTime = variantMap[TEXT("changeTime")].GetValue<FString>();
}

RECALL_GIFT_DATAS::RECALL_GIFT_DATAS()
{

}

RECALL_GIFT_DATAS::RECALL_GIFT_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_richText = variantMap[TEXT("dealGivingGoodsData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_richText)
	{
		RECALL_GIFT_DATA element1 = RECALL_GIFT_DATA(elementVariant0);
		dealGivingGoodsData.Add(element1);
	}
}

FCLINE_RESEARCH_SKILL::FCLINE_RESEARCH_SKILL()
{

}
FCLINE_RESEARCH_SKILL::FCLINE_RESEARCH_SKILL(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	skillID = variantMap[TEXT("skillID")].GetValue<int32>();
	progress = variantMap[TEXT("progress")].GetValue<int32>();
}

FTONG_SKILL_DATA::FTONG_SKILL_DATA()
{

}
FTONG_SKILL_DATA::FTONG_SKILL_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantMap RSVariant = variantMap[TEXT("ResearchSkill")].GetValue<KBEngine::FVariantMap>();
	ResearchSkill = FCLINE_RESEARCH_SKILL(RSVariant);
	KBEngine::FVariantArray variantArray_Pause = variantMap[TEXT("PauseSkill")].GetValue<KBEngine::FVariantArray>();

	for (FVariant& elementVariant0 : variantArray_Pause)
	{
		FCLINE_RESEARCH_SKILL element1 = FCLINE_RESEARCH_SKILL(elementVariant0);
		PauseSkill.Add(element1);
	}
	KBEngine::FVariantArray variantArray_SkillList = variantMap[TEXT("SkillList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_SkillList)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		SkillList.Add(element1);
	}
	KBEngine::FVariantArray variantArray_SkillLevelList = variantMap[TEXT("SkillLevelList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_SkillLevelList)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		SkillList.Add(element1);
	}
}

FCLINE_TONG_DATAS::FCLINE_TONG_DATAS()
{

}

FCLINE_TONG_DATAS::FCLINE_TONG_DATAS(const FVariant& variant )
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	TongDBID = variantMap[TEXT("TongDBID")].GetValue<FString>();
	TongLeader = variantMap[TEXT("TongLeader")].GetValue<FString>();
	TongName = variantMap[TEXT("TongName")].GetValue<FString>();
	level = variantMap[TEXT("level")].GetValue<int32>();
	TongMoney = variantMap[TEXT("TongMoney")].GetValue<FString>();
	TongAffiche = variantMap[TEXT("TongAffiche")].GetValue<FString>();
	TongActivity = variantMap[TEXT("TongActivity")].GetValue<int32>();
	TongGrow = variantMap[TEXT("TongGrow")].GetValue<int32>();
	TotalNum = variantMap[TEXT("TotalNum")].GetValue<int32>();
	League = variantMap[TEXT("League")].GetValue<FString>();
	City = variantMap[TEXT("City")].GetValue<FString>();
	ShenShou = variantMap[TEXT("ShenShou")].GetValue<int32>();
	Sign = variantMap[TEXT("Sign")].GetValue<int32>();
	signTime = variantMap[TEXT("signTime")].GetValue<int32>();
	donateMoney = variantMap[TEXT("donateMoney")].GetValue<int32>();
	Salary = variantMap[TEXT("Salary")].GetValue<int32>();
	UpGradeActivity = variantMap[TEXT("UpGradeActivity")].GetValue<int32>();
	MinActivity = variantMap[TEXT("minActivity")].GetValue<int32>();
	TongRecruitAffiche = variantMap[TEXT("recruitAffiche")].GetValue<FString>();
	Allocation = variantMap[TEXT("Allocation")].GetValue<uint8>();
	BHLDAllocation = variantMap[TEXT("BHLDAllocation")].GetValue<uint8>();

	KBEngine::FVariantArray variantArray_TitleNames = variantMap[TEXT("TitleNames")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_TitleNames)
	{
		FString element1 = elementVariant0.GetValue<FString>();
		TitleNames.Add(element1);
	}

	KBEngine::FVariantArray variantArray_TongGrades = variantMap[TEXT("TongGrades")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_TongGrades)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		TongGrades.Add(element1);
	}

	KBEngine::FVariantArray variantArray_TongBuild = variantMap[TEXT("TongBuild")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_TongBuild)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		TongBuild.Add(element1);
	}

	KBEngine::FVariantMap TSVariant = variantMap[TEXT("TongSkill")].GetValue<KBEngine::FVariantMap>();
	TongSkill = FTONG_SKILL_DATA(TSVariant);
}

JOIN_TONG_DATA::JOIN_TONG_DATA()
{

}
JOIN_TONG_DATA::JOIN_TONG_DATA(const FVariant& variant )
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	TongDBID = variantMap[TEXT("TongDBID")].GetValue<FString>();
	Name = variantMap[TEXT("Name")].GetValue<FString>();
	Level = variantMap[TEXT("Level")].GetValue<int32>();
	Activity = variantMap[TEXT("Activity")].GetValue<int32>();
	TongNum = variantMap[TEXT("TongNum")].GetValue<int32>();
	TotalNum = variantMap[TEXT("TotalNum")].GetValue<int32>();
	LeaderName = variantMap[TEXT("LeaderName")].GetValue<FString>();
	Money = variantMap[TEXT("Money")].GetValue<FString>();
	Recruit = variantMap[TEXT("Recruit")].GetValue<FString>();
	League = variantMap[TEXT("League")].GetValue<FString>();
	City = variantMap[TEXT("City")].GetValue<FString>();
	ShenShou = variantMap[TEXT("ShenShou")].GetValue<int32>();
	PersonTitle = variantMap[TEXT("PersonTitle")].GetValue<FString>();
}

JOIN_TONG_DATAS::JOIN_TONG_DATAS()
{

}
JOIN_TONG_DATAS::JOIN_TONG_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_tongDatas = variantMap[TEXT("tongDatas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_tongDatas)
	{
		JOIN_TONG_DATA element1 = JOIN_TONG_DATA(elementVariant0);
		tongDatas.Add(element1);
	}
}

CLENT_TONG_MEMBER_DATA::CLENT_TONG_MEMBER_DATA()
{

}
CLENT_TONG_MEMBER_DATA::CLENT_TONG_MEMBER_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	exp = variantMap[TEXT("exp")].GetValue<int32>();
	name = variantMap[TEXT("name")].GetValue<FString>();
	DBID = variantMap[TEXT("DBID")].GetValue<FString>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	level = variantMap[TEXT("level")].GetValue<int32>();
	profession = variantMap[TEXT("profession")].GetValue<int32>();
	title = variantMap[TEXT("title")].GetValue<int32>();
	weekContribution = variantMap[TEXT("weekContribution")].GetValue<int32>();
	contribution = variantMap[TEXT("contribution")].GetValue<int32>();
	totalContribution = variantMap[TEXT("totalContribution")].GetValue<int32>();
	localSpace = variantMap[TEXT("localSpace")].GetValue<FString>();
	offLineTime = variantMap[TEXT("offLineTime")].GetValue<FString>();
	isGag = variantMap[TEXT("isGag")].GetValue<int32>();
	soldierAmount = variantMap[TEXT("soldierAmount")].GetValue<int32>();
	militaryRank = variantMap[TEXT("militaryRank")].GetValue<int32>();
	KBEngine::FVariantArray variantArray_param = variantMap[TEXT("tongBlocklist")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant : variantArray_param)
	{
		FString element = elementVariant.GetValue<FString>();
		tongBlocklist.Add(element);
	}
}

TONG_EVENT_DATA::TONG_EVENT_DATA()
{

}
TONG_EVENT_DATA::TONG_EVENT_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	time = variantMap[TEXT("time")].GetValue<FString>();
	type = variantMap[TEXT("type")].GetValue<int32>();
	KBEngine::FVariantArray variantArray_param = variantMap[TEXT("param")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_param)
	{
		FString element1 = elementVariant0.GetValue<FString>();
		param.Add(element1);
	}
	
}

TONG_EVENT_DATAS::TONG_EVENT_DATAS()
{

}
TONG_EVENT_DATAS::TONG_EVENT_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_eventDatas = variantMap[TEXT("eventDatas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_eventDatas)
	{
		TONG_EVENT_DATA element1 = TONG_EVENT_DATA(elementVariant0);
		eventDatas.Add(element1);
	}
}

FORDER_DATA::FORDER_DATA()
{

}
FORDER_DATA::FORDER_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	price = variantMap[TEXT("price")].GetValue<int32>();
	remainTime = variantMap[TEXT("remainTime")].GetValue<FString>();
	tradeType = variantMap[TEXT("tradeType")].GetValue<int32>();
	earnMoney = variantMap[TEXT("earnMoney")].GetValue<int32>();
}

FORDER_DATAS::FORDER_DATAS()
{

}
FORDER_DATAS::FORDER_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_orderData = variantMap[TEXT("orderData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_orderData)
	{
		FORDER_DATA element1 = FORDER_DATA(elementVariant0);
		orderData.Add(element1);
	}
}

FALL_ORDER_DATAS::FALL_ORDER_DATAS()
{

}
FALL_ORDER_DATAS::FALL_ORDER_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_TradeOrder = variantMap[TEXT("lingShiTradeOrder")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_TradeOrder)
	{
		FORDER_DATA element1 = FORDER_DATA(elementVariant0);
		lingShiTradeOrder.Add(element1);
	}
	KBEngine::FVariantArray variantArray_SellOrder = variantMap[TEXT("allLingShiTradeSellOrder")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_SellOrder)
	{
		FORDER_DATA element1 = FORDER_DATA(elementVariant0);
		allLingShiTradeSellOrder.Add(element1);
	}
	KBEngine::FVariantArray variantArray_CollectOrder = variantMap[TEXT("allLingShiTradeCollectOrder")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_CollectOrder)
	{
		FORDER_DATA element1 = FORDER_DATA(elementVariant0);
		allLingShiTradeCollectOrder.Add(element1);
	}
	tax = variantMap[TEXT("tax")].GetValue<int32>();
}

FALL_TRADE_DATA::FALL_TRADE_DATA()
{

 }
FALL_TRADE_DATA::FALL_TRADE_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	remainTime = variantMap[TEXT("remainTime")].GetValue<FString>();
	tradeType = variantMap[TEXT("tradeType")].GetValue<int32>();
}

FLINGSHITRADE_SUCCESS_DATA::FLINGSHITRADE_SUCCESS_DATA()
{

}
FLINGSHITRADE_SUCCESS_DATA::FLINGSHITRADE_SUCCESS_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	price = variantMap[TEXT("price")].GetValue<int32>();
	isSend = variantMap[TEXT("isSend")].GetValue<int32>();
	tradeType = variantMap[TEXT("tradeType")].GetValue<int32>();
}

FUPDATA_ORDER_DATA::FUPDATA_ORDER_DATA()
{

}
FUPDATA_ORDER_DATA::FUPDATA_ORDER_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantMap TRVariant = variantMap[TEXT("allTradeData")].GetValue<KBEngine::FVariantMap>();
	allTradeData = FALL_TRADE_DATA(TRVariant);
	KBEngine::FVariantMap TSVariant = variantMap[TEXT("allTradeSuccess")].GetValue<KBEngine::FVariantMap>();
	allTradeSuccess = FLINGSHITRADE_SUCCESS_DATA(TSVariant);
}

TONG_QUEST_TREE_DATA::TONG_QUEST_TREE_DATA()
{

}
TONG_QUEST_TREE_DATA::TONG_QUEST_TREE_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	questTitle = variantMap[TEXT("questTitle")].GetValue<FString>();
	questID = variantMap[TEXT("questID")].GetValue<int32>();
	layer = variantMap[TEXT("layer")].GetValue<int32>();
	genre = variantMap[TEXT("genre")].GetValue<int32>();
	KBEngine::FVariantArray variantArray_route = variantMap[TEXT("route")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_route)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		route.Add(element1);
	}
}

TONG_QUEST_TREE_DATAS::TONG_QUEST_TREE_DATAS()
{

}
TONG_QUEST_TREE_DATAS::TONG_QUEST_TREE_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_route = variantMap[TEXT("data")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_route)
	{
		TONG_QUEST_TREE_DATA element1 = TONG_QUEST_TREE_DATA(elementVariant0);
		data.Add(element1);
	}
}

FSOLDIER_SPECIAL_SKILL_DATA::FSOLDIER_SPECIAL_SKILL_DATA()
{

}

FSOLDIER_SPECIAL_SKILL_DATA::FSOLDIER_SPECIAL_SKILL_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	skillID = variantMap[TEXT("skillID")].GetValue<int32>();
	exp = variantMap[TEXT("exp")].GetValue<int32>();
	maxExp = variantMap[TEXT("maxExp")].GetValue<int32>();
}

FBARRACKSSOLDIERDATA::FBARRACKSSOLDIERDATA()
{

}
FBARRACKSSOLDIERDATA::FBARRACKSSOLDIERDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	scriptID = variantMap[TEXT("scriptID")].GetValue<FString>();
	soldierType = variantMap[TEXT("soldierType")].GetValue<int32>();
	level = variantMap[TEXT("level")].GetValue<int32>();
	exp = variantMap[TEXT("exp")].GetValue<int32>();
	isInArmy = variantMap[TEXT("isInArmy")].GetValue<int32>();
	maxExp = variantMap[TEXT("maxExp")].GetValue<int32>();
	KBEngine::FVariantArray variantArray = variantMap[TEXT("skillIDDatas")].GetValue<KBEngine::FVariantArray > ();
	for (FVariant& elementVariant0 :variantArray)
	{
		skillIDDatas.Add(FSOLDIER_SPECIAL_SKILL_DATA(elementVariant0));
	}
	isActive = bool(variantMap[TEXT("isActive")].GetValue<int32>());
}

FARMYDATA::FARMYDATA()
{

}
FARMYDATA::FARMYDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	controlArmyID = variantMap[TEXT("controlArmyID")].GetValue<int32>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	firstGuardScriptID = variantMap[TEXT("firstGuardScriptID")].GetValue<FString>();
	secondGuardScriptID = variantMap[TEXT("secondGuardScriptID")].GetValue<FString>();
	soldierScriptID = variantMap[TEXT("soldierScriptID")].GetValue<FString>();
	KBEngine::FVariantArray variantArray = variantMap[TEXT("soldierIDs")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		soldierIDs.Add(element1);
	}
}

void FARMYDATA::ToFVariantMap(KBEngine::FVariantMap& out)
{
	out.Add(TEXT("id"), FVariant(id));
	out.Add(TEXT("controlArmyID"), FVariant(controlArmyID));
	out.Add(TEXT("firstGuardScriptID"), FVariant(firstGuardScriptID));
	out.Add(TEXT("secondGuardScriptID"), FVariant(secondGuardScriptID));
	out.Add(TEXT("soldierScriptID"), FVariant(soldierScriptID));
	KBEngine::FVariantArray arr;
	for (auto v : soldierIDs)
	{
		arr.Add(FVariant(v));
	}
	out.Add(TEXT("soldierIDs"), FVariant(arr));
}


FORIGIN_PET_DATA::FORIGIN_PET_DATA()
{

}

FORIGIN_PET_DATA::FORIGIN_PET_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid1 = variantMap[TEXT("uid")].GetValue<uint64>();
	scriptID2 = variantMap[TEXT("scriptID")].GetValue<FString>();
	name3 = variantMap[TEXT("name")].GetValue<FString>();
	uname4 = variantMap[TEXT("uname")].GetValue<FString>();
	camp5 = variantMap[TEXT("camp")].GetValue<uint16>();
	exp6 = variantMap[TEXT("exp")].GetValue<int32>();
	bEvolution = variantMap[TEXT("bEvolution")].GetValue<uint8>();
	level7 = variantMap[TEXT("level")].GetValue<uint16>();
	takeLevel8 = variantMap[TEXT("takeLevel")].GetValue<uint16>();
	ability9 = variantMap[TEXT("ability")].GetValue<uint16>();
	ability_Max10 = variantMap[TEXT("ability_Max")].GetValue<uint16>();
	step11 = variantMap[TEXT("step")].GetValue<uint8>();
	quality12 = variantMap[TEXT("quality")].GetValue<uint8>();
	KBEngine::FVariantArray variantArray_attrSkillBox13 = variantMap[TEXT("attrSkillBox")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_attrSkillBox13)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		attrSkillBox13.Add(element1);
	}
	KBEngine::FVariantArray variantArray_passiveSkillBox14 = variantMap[TEXT("passiveSkillBox")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_passiveSkillBox14)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		passiveSkillBox14.Add(element1);
	}
	KBEngine::FVariantArray variantArray_noLearnedSkillBox15 = variantMap[TEXT("noLearnedSkillBox")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_noLearnedSkillBox15)
	{
		int32 element1 = elementVariant0.GetValue<int32>();
		noLearnedSkillBox15.Add(element1);
	}
	sleepTime16 = variantMap[TEXT("sleepTime")].GetValue<uint64>();
	wildness17 = variantMap[TEXT("wildness")].GetValue<uint8>();
	corporeity22 = variantMap[TEXT("corporeity")].GetValue<uint32>();
	strength23 = variantMap[TEXT("strength")].GetValue<uint32>();
	intellect24 = variantMap[TEXT("intellect")].GetValue<uint32>();
	discern25 = variantMap[TEXT("discern")].GetValue<uint32>();
	dexterity26 = variantMap[TEXT("dexterity")].GetValue<uint32>();
	HP27 = variantMap[TEXT("HP")].GetValue<uint32>();
	MP28 = variantMap[TEXT("MP")].GetValue<uint32>();
	HP_Max29 = variantMap[TEXT("HP_Max")].GetValue<uint32>();
	MP_Max30 = variantMap[TEXT("MP_Max")].GetValue<uint32>();
	damage31 = variantMap[TEXT("damage")].GetValue<uint32>();
	magic_damage32 = variantMap[TEXT("magic_damage")].GetValue<uint32>();
	armor33 = variantMap[TEXT("armor")].GetValue<uint32>();
	magic_armor34 = variantMap[TEXT("magic_armor")].GetValue<uint32>();
	criticalstrike35 = variantMap[TEXT("criticalstrike")].GetValue<uint32>();
	parry36 = variantMap[TEXT("parry")].GetValue<uint32>();
	speed37 = variantMap[TEXT("speed")].GetValue<uint32>();
	hitrate38 = variantMap[TEXT("hitrate")].GetValue<uint32>();
	dodgerate39 = variantMap[TEXT("dodgerate")].GetValue<uint32>();
	gangQiValue40 = variantMap[TEXT("gangQiValue")].GetValue<uint32>();
	gangQiValue_Max41 = variantMap[TEXT("gangQiValue_Max")].GetValue<uint32>();
	gangQiState42 = variantMap[TEXT("gangQiState")].GetValue<uint32>();
	gangQi_damagePoint43 = variantMap[TEXT("gangQi_damagePoint")].GetValue<uint32>();
	gangQi_armorPoint44 = variantMap[TEXT("gangQi_armorPoint")].GetValue<uint32>();
	gangQi_qiJieRevive45 = variantMap[TEXT("gangQi_qiJieRevive")].GetValue<uint32>();
	gangQi_qiYingRevive46 = variantMap[TEXT("gangQi_qiYingRevive")].GetValue<uint32>();
	combatPower47 = variantMap[TEXT("combatPower")].GetValue<uint32>();
	cure48 = variantMap[TEXT("cure")].GetValue<int32>();

	ice_damage = variantMap[TEXT("ice_damage")].GetValue<uint32>();
	fire_damage = variantMap[TEXT("fire_damage")].GetValue<uint32>();
	thunder_damage = variantMap[TEXT("thunder_damage")].GetValue<uint32>();
	xuan_damage = variantMap[TEXT("xuan_damage")].GetValue<uint32>();
	ice_armor = variantMap[TEXT("ice_armor")].GetValue<uint32>();
	fire_armor = variantMap[TEXT("fire_armor")].GetValue<uint32>();
	thunder_armor = variantMap[TEXT("thunder_armor")].GetValue<uint32>();
	xuan_armor = variantMap[TEXT("xuan_armor")].GetValue<uint32>();

	damage_ignore = variantMap[TEXT("damage_ignore")].GetValue<uint32>();
	magic_damage_ignore = variantMap[TEXT("magic_damage_ignore")].GetValue<uint32>();
	armor_ignore = variantMap[TEXT("armor_ignore")].GetValue<uint32>();
	magic_armor_ignore = variantMap[TEXT("magic_armor_ignore")].GetValue<uint32>();
	criticalstrike_ignore = variantMap[TEXT("criticalstrike_ignore")].GetValue<uint32>();
	parry_ignore = variantMap[TEXT("parry_ignore")].GetValue<uint32>();
	hitrate_ignore = variantMap[TEXT("hitrate_ignore")].GetValue<uint32>();
	dodgerate_ignore = variantMap[TEXT("dodgerate_ignore")].GetValue<uint32>();

	ice_damage_ignore = variantMap[TEXT("ice_damage_ignore")].GetValue<uint32>();
	fire_damage_ignore = variantMap[TEXT("fire_damage_ignore")].GetValue<uint32>();
	thunder_damage_ignore = variantMap[TEXT("thunder_damage_ignore")].GetValue<uint32>();
	xuan_damage_ignore = variantMap[TEXT("xuan_damage_ignore")].GetValue<uint32>();
	ice_armor_ignore = variantMap[TEXT("ice_armor_ignore")].GetValue<uint32>();
	fire_armor_ignore = variantMap[TEXT("fire_armor_ignore")].GetValue<uint32>();
	thunder_armor_ignore = variantMap[TEXT("thunder_armor_ignore")].GetValue<uint32>();
	xuan_armor_ignore = variantMap[TEXT("xuan_armor_ignore")].GetValue<uint32>();

	depress_resist = variantMap[TEXT("depress_resist")].GetValue<uint32>();
	hitback_resist = variantMap[TEXT("hitback_resist")].GetValue<uint32>();
	control_resist = variantMap[TEXT("control_resist")].GetValue<uint32>();
	insane_resist = variantMap[TEXT("insane_resist")].GetValue<uint32>();
}

FVariant FORIGIN_PET_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("uid"), uid1);
	variantMap.Add(TEXT("scriptID"), scriptID2);
	variantMap.Add(TEXT("name"), name3);
	variantMap.Add(TEXT("uname"), uname4);
	variantMap.Add(TEXT("camp"), camp5);
	variantMap.Add(TEXT("exp"), exp6);
	variantMap.Add(TEXT("bEvolution"), bEvolution);
	variantMap.Add(TEXT("level"), level7);
	variantMap.Add(TEXT("takeLevel"), takeLevel8);
	variantMap.Add(TEXT("ability"), ability9);
	variantMap.Add(TEXT("ability_Max"), ability_Max10);
	variantMap.Add(TEXT("step"), step11);
	variantMap.Add(TEXT("quality"), quality12);
	KBEngine::FVariantArray variantArray_attrSkillBox13 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : attrSkillBox13)
	{
		int32 element1 = elementVariant0;
		variantArray_attrSkillBox13.Add(element1);
	}
	variantMap.Add(TEXT("attrSkillBox"), variantArray_attrSkillBox13);
	KBEngine::FVariantArray variantArray_passiveSkillBox14 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : passiveSkillBox14)
	{
		int32 element1 = elementVariant0;
		variantArray_passiveSkillBox14.Add(element1);
	}
	variantMap.Add(TEXT("passiveSkillBox"), variantArray_passiveSkillBox14);
	KBEngine::FVariantArray variantArray_noLearnedSkillBox15 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : noLearnedSkillBox15)
	{
		int32 element1 = elementVariant0;
		variantArray_noLearnedSkillBox15.Add(element1);
	}
	variantMap.Add(TEXT("noLearnedSkillBox"), variantArray_noLearnedSkillBox15);
	variantMap.Add(TEXT("sleepTime"), sleepTime16);
	variantMap.Add(TEXT("wildness17"), wildness17);
	variantMap.Add(TEXT("corporeity"), corporeity22);
	variantMap.Add(TEXT("strength"), strength23);
	variantMap.Add(TEXT("intellect"), intellect24);
	variantMap.Add(TEXT("discern"), discern25);
	variantMap.Add(TEXT("dexterity"), dexterity26);
	variantMap.Add(TEXT("HP"), HP27);
	variantMap.Add(TEXT("MP"), MP28);
	variantMap.Add(TEXT("HP_Max"), HP_Max29);
	variantMap.Add(TEXT("MP_Max"), MP_Max30);
	variantMap.Add(TEXT("damage"), damage31);
	variantMap.Add(TEXT("magic_damage"), magic_damage32);
	variantMap.Add(TEXT("armor"), armor33);
	variantMap.Add(TEXT("magic_armor"), magic_armor34);
	variantMap.Add(TEXT("criticalstrike"), criticalstrike35);
	variantMap.Add(TEXT("parry"), parry36);
	variantMap.Add(TEXT("speed"), speed37);
	variantMap.Add(TEXT("hitrate"), hitrate38);
	variantMap.Add(TEXT("dodgerate"), dodgerate39);
	variantMap.Add(TEXT("gangQiValue"), gangQiValue40);
	variantMap.Add(TEXT("gangQiValue_Max"), gangQiValue_Max41);
	variantMap.Add(TEXT("gangQiState"), gangQiState42);
	variantMap.Add(TEXT("gangQi_damagePoint"), gangQi_damagePoint43);
	variantMap.Add(TEXT("gangQi_armorPoint"), gangQi_armorPoint44);
	variantMap.Add(TEXT("gangQi_qiJieRevive"), gangQi_qiJieRevive45);
	variantMap.Add(TEXT("gangQi_qiYingRevive"), gangQi_qiYingRevive46);
	variantMap.Add(TEXT("combatPower"), combatPower47);
	variantMap.Add(TEXT("cure"), cure48);

	variantMap.Add(TEXT("ice_damage"), ice_damage);
	variantMap.Add(TEXT("fire_damage"), fire_damage);
	variantMap.Add(TEXT("thunder_damage"), thunder_damage);
	variantMap.Add(TEXT("xuan_damage"), xuan_damage);
	variantMap.Add(TEXT("ice_armor"), ice_armor);
	variantMap.Add(TEXT("fire_armor"), fire_armor);
	variantMap.Add(TEXT("thunder_armor"), thunder_armor);
	variantMap.Add(TEXT("xuan_armor"), xuan_armor);

	variantMap.Add(TEXT("damage_ignore"), damage_ignore);
	variantMap.Add(TEXT("magic_damage_ignore"), magic_damage_ignore);
	variantMap.Add(TEXT("armor_ignore"), armor_ignore);
	variantMap.Add(TEXT("magic_armor_ignore"), magic_armor_ignore);
	variantMap.Add(TEXT("criticalstrike_ignore"), criticalstrike_ignore);
	variantMap.Add(TEXT("parry_ignore"), parry_ignore);
	variantMap.Add(TEXT("hitrate_ignore"), hitrate_ignore);
	variantMap.Add(TEXT("dodgerate_ignore"), dodgerate_ignore);

	variantMap.Add(TEXT("ice_damage_ignore"), ice_damage_ignore);
	variantMap.Add(TEXT("fire_damage_ignore"), fire_damage_ignore);
	variantMap.Add(TEXT("thunder_damage_ignore"), thunder_damage_ignore);
	variantMap.Add(TEXT("xuan_damage_ignore"), xuan_damage_ignore);
	variantMap.Add(TEXT("ice_armor_ignore"), ice_armor_ignore);
	variantMap.Add(TEXT("fire_armor_ignore"), fire_armor_ignore);
	variantMap.Add(TEXT("thunder_armor_ignore"), thunder_armor_ignore);
	variantMap.Add(TEXT("xuan_armor_ignore"), xuan_armor_ignore);

	variantMap.Add(TEXT("depress_resist"), depress_resist);
	variantMap.Add(TEXT("hitback_resist"), hitback_resist);
	variantMap.Add(TEXT("control_resist"), control_resist);
	variantMap.Add(TEXT("insane_resist"), insane_resist);
	return FVariant(variantMap);
}

FPET_FENCE_DATAS::FPET_FENCE_DATAS()
{

}

FPET_FENCE_DATAS::FPET_FENCE_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_pets1 = variantMap[TEXT("pets")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_pets1)
	{
		FORIGIN_PET_DATA element1 = FORIGIN_PET_DATA(elementVariant0);
		pets1.Add(element1);
	}

}

FVariant FPET_FENCE_DATAS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_pets1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : pets1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_pets1.Add(element1);
	}
	variantMap.Add(TEXT("pets"), variantArray_pets1);

	return FVariant(variantMap);
}

FSGMZ_BOSS_DATA::FSGMZ_BOSS_DATA()
{

}
FSGMZ_BOSS_DATA::FSGMZ_BOSS_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	name = variantMap[TEXT("name")].GetValue<FString>();
	scriptID = variantMap[TEXT("scriptID")].GetValue<FString>();
	time = variantMap[TEXT("time")].GetValue<int32>();
	exp = variantMap[TEXT("exp")].GetValue<int32>();
	PerHP = variantMap[TEXT("PerHP")].GetValue<float>();
	level = variantMap[TEXT("level")].GetValue<int32>();
	stage = variantMap[TEXT("stage")].GetValue<int32>();
}

SGMZ_TEAM_DATA::SGMZ_TEAM_DATA()
{

}
SGMZ_TEAM_DATA::SGMZ_TEAM_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	teamCamp = variantMap[TEXT("camp")].GetValue<int32>();
	isKillBoss = variantMap[TEXT("isKillBoss")].GetValue<int32>();
	isWin = variantMap[TEXT("isWin")].GetValue<int32>();
	extraExp = variantMap[TEXT("extraExp")].GetValue<int32>();
	score = variantMap[TEXT("score")].GetValue<int32>();
	feats = variantMap[TEXT("feats")].GetValue<int32>();
	BossKiller = variantMap[TEXT("bossKiller")].GetValue<FString>();
	KBEngine::FVariantArray variantArray = variantMap[TEXT("bossDatas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray)
	{
		FSGMZ_BOSS_DATA element1 = FSGMZ_BOSS_DATA(elementVariant0);
		bossDatas.Add(element1);
	}
}

SGMZ_TEAM_DATAS::SGMZ_TEAM_DATAS()
{

}
SGMZ_TEAM_DATAS::SGMZ_TEAM_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray)
	{
		SGMZ_TEAM_DATA element1 = SGMZ_TEAM_DATA(elementVariant0);
		datas.Add(element1);
	}
}

FSHOPMALL_ITEM::FSHOPMALL_ITEM()
{
}

FSHOPMALL_ITEM::FSHOPMALL_ITEM(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<FString>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
	itemID = variantMap[TEXT("itemID")].GetValue<int32>();

}

FVariant FSHOPMALL_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id);
	variantMap.Add(TEXT("amount"), amount);
	variantMap.Add(TEXT("itemID"), itemID);

	return FVariant(variantMap);
}

FSHOPMALL_ITEM_LIST::FSHOPMALL_ITEM_LIST()
{
}

FSHOPMALL_ITEM_LIST::FSHOPMALL_ITEM_LIST(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_items1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_items1)
	{
		FSHOPMALL_ITEM element1 = FSHOPMALL_ITEM(elementVariant0);
		items.Add(element1);
	}

}

FVariant FSHOPMALL_ITEM_LIST::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_items1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : items)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_items1.Add(element1);
	}
	variantMap.Add(TEXT("items"), variantArray_items1);

	return FVariant(variantMap);
}



FDICT_INT_INT_ITEM::FDICT_INT_INT_ITEM()
{

}

FDICT_INT_INT_ITEM::FDICT_INT_INT_ITEM(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key1 = variantMap[TEXT("key")].GetValue<int32>();
	value2 = variantMap[TEXT("value")].GetValue<int32>();

}

FVariant FDICT_INT_INT_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("key"), key1);
	variantMap.Add(TEXT("value"), value2);

	return FVariant(variantMap);
}

FDICT_INT_INT::FDICT_INT_INT()
{

}

FDICT_INT_INT::FDICT_INT_INT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_dictData1 = variantMap[TEXT("dictData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_dictData1)
	{
		FDICT_INT_INT_ITEM element1 = FDICT_INT_INT_ITEM(elementVariant0);
		dictData1.Add(element1.key1, element1.value2);
	}

}

FVariant FDICT_INT_INT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_dictData1 = KBEngine::FVariantArray();
	for (auto it = dictData1.CreateConstIterator(); it; ++it)
	{
		KBEngine::FVariantMap variantMapSub = KBEngine::FVariantMap();
		variantMapSub.Add(TEXT("key"), it.Key());
		variantMapSub.Add(TEXT("value"), it.Value());
		variantArray_dictData1.Add(variantMapSub);
	}
	variantMap.Add(TEXT("dictData"), variantArray_dictData1);

	return FVariant(variantMap);
}

FDICT_INT_INT32_LIST_ITEM::FDICT_INT_INT32_LIST_ITEM()
{
}

FDICT_INT_INT32_LIST_ITEM::FDICT_INT_INT32_LIST_ITEM(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key1 = variantMap[TEXT("key")].GetValue<int32>();
	KBEngine::FVariantArray variantArray_dictData1 = variantMap[TEXT("value")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_dictData1)
	{
		value2.Add(elementVariant0.GetValue<int32>());
	}
	
}

FVariant FDICT_INT_INT32_LIST_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("key"), key1);
	KBEngine::FVariantArray arr;
	for (auto v : value2)
	{
		arr.Add(FVariant(v));
	}
	variantMap.Add(TEXT("value"), FVariant(arr));

	return FVariant(variantMap);
}

FDICT_INT_INT32_LIST::FDICT_INT_INT32_LIST()
{
}

FDICT_INT_INT32_LIST::FDICT_INT_INT32_LIST(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_dictData1 = variantMap[TEXT("dictData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_dictData1)
	{
		FDICT_INT_INT32_LIST_ITEM element1 = FDICT_INT_INT32_LIST_ITEM(elementVariant0);
		dictData1.Add(element1.key1, element1.value2);
	}
}

FVariant FDICT_INT_INT32_LIST::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_dictData1 = KBEngine::FVariantArray();
	for (auto it = dictData1.CreateConstIterator(); it; ++it)
	{
		KBEngine::FVariantMap variantMapSub = KBEngine::FVariantMap();
		variantMapSub.Add(TEXT("key"), it.Key());
		KBEngine::FVariantArray arr;
		for (auto v : it.Value())
		{
			arr.Add(FVariant(v));
		}
		variantMapSub.Add(TEXT("value"), FVariant(arr));
		variantArray_dictData1.Add(variantMapSub);
	}
	variantMap.Add(TEXT("dictData"), variantArray_dictData1);

	return FVariant(variantMap);
}

FDICT_INT_INTDICT_ITEM::FDICT_INT_INTDICT_ITEM()
{

}

FDICT_INT_INTDICT_ITEM::FDICT_INT_INTDICT_ITEM(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key1 = variantMap[TEXT("key")].GetValue<int32>();
	value2 = FDICT_INT_INT(variantMap[TEXT("value")]);
}

FVariant FDICT_INT_INTDICT_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("key"), key1);
	variantMap.Add(TEXT("value"), value2.ToVariant());

	return FVariant(variantMap);
}

FDICT_INT_INTDICT::FDICT_INT_INTDICT()
{

}

FDICT_INT_INTDICT::FDICT_INT_INTDICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_dictData1 = variantMap[TEXT("dictData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_dictData1)
	{
		FDICT_INT_INTDICT_ITEM element1(elementVariant0);
		dictData1.Add(element1.key1, element1.value2);
	}
}

FVariant FDICT_INT_INTDICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_dictData1 = KBEngine::FVariantArray();
	for (auto it = dictData1.CreateConstIterator(); it; ++it)
	{
		KBEngine::FVariantMap variantMapSub = KBEngine::FVariantMap();
		variantMapSub.Add(TEXT("key"), it.Key());

		KBEngine::FVariantArray variantArray_dictData2 = KBEngine::FVariantArray();
		KBEngine::FVariantMap variantMapSub2 = KBEngine::FVariantMap();
		for (auto itsub = it.Value().dictData1.CreateConstIterator(); itsub; ++itsub)
		{
			KBEngine::FVariantMap variantMapSub3 = KBEngine::FVariantMap();
			variantMapSub3.Add(TEXT("key"), itsub.Key());
			variantMapSub3.Add(TEXT("value"), itsub.Value());
			variantArray_dictData2.Add(variantMapSub3);
		}
		variantMapSub2.Add(TEXT("dictData"), variantArray_dictData2);

		variantMapSub.Add(TEXT("value"), variantMapSub2);
		variantArray_dictData1.Add(variantMapSub);
	}
	variantMap.Add(TEXT("dictData"), variantArray_dictData1);

	return FVariant(variantMap);
}


FBHZB_SIGN_MEMBER_DATA::FBHZB_SIGN_MEMBER_DATA()
{

}
FBHZB_SIGN_MEMBER_DATA::FBHZB_SIGN_MEMBER_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	signID = variantMap[TEXT("signID")].GetValue<int32>();
	groupID = variantMap[TEXT("groupID")].GetValue<int32>();
	captainDBID = variantMap[TEXT("captainDBID")].GetValue<FString>();
	KBEngine::FVariantArray variantArray = variantMap[TEXT("memberDBIDs")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray)
	{
		FString element1 = elementVariant0.GetValue<FString>();
		memberDBIDs.Add(element1);
	}
	isActive = variantMap[TEXT("isActive")].GetValue<uint8>();
	pointIndex = variantMap[TEXT("pointIndex")].GetValue<int32>();
}

void FBHZB_SIGN_MEMBER_DATA::ToFVariantMap(KBEngine::FVariantMap& out)
{
	out.Add(TEXT("signID"), FVariant(signID));
	out.Add(TEXT("groupID"), FVariant(groupID));
	out.Add(TEXT("captainDBID"), FVariant(captainDBID));
	out.Add(TEXT("isActive"), FVariant(isActive));
	out.Add(TEXT("pointIndex"), FVariant(pointIndex));
	KBEngine::FVariantArray arr;
	for (auto v : memberDBIDs)
	{
		arr.Add(FVariant(v));
	}
	out.Add(TEXT("memberDBIDs"), FVariant(arr));
}


FDICT_STR_INT_ITEM::FDICT_STR_INT_ITEM()
{

}

FDICT_STR_INT_ITEM::FDICT_STR_INT_ITEM(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key = variantMap[TEXT("key")].GetValue<FString>();
	value = variantMap[TEXT("value")].GetValue<int32>();
}

FVariant FDICT_STR_INT_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantMap dictData = KBEngine::FVariantMap();
	dictData.Add(TEXT("key"), key);
	dictData.Add(TEXT("value"), value);
	variantMap.Add(TEXT("dictData"), dictData);

	return FVariant(variantMap);
}



FDICT_STR_INT::FDICT_STR_INT()
{
}

FDICT_STR_INT::FDICT_STR_INT(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray _dictDataList = variantMap[TEXT("dictData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& _dictData : _dictDataList)
	{
		FDICT_STR_INT_ITEM dictData = FDICT_STR_INT_ITEM(_dictData);
		dictDataList.Add(dictData.key, dictData.value);
	}
}

FVariant FDICT_STR_INT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray _dictDataList = KBEngine::FVariantArray();
	for (auto it = dictDataList.CreateConstIterator(); it; ++it)
	{
		KBEngine::FVariantMap dictData = KBEngine::FVariantMap();
		dictData.Add(TEXT("key"), it.Key());
		dictData.Add(TEXT("value"), it.Value());
		_dictDataList.Add(dictData);
	}
	variantMap.Add(TEXT("dictData"), _dictDataList);
	return FVariant();
}



FTRAIN_SOLDIER_QUEST_DICT::FTRAIN_SOLDIER_QUEST_DICT()
{

}

FTRAIN_SOLDIER_QUEST_DICT::FTRAIN_SOLDIER_QUEST_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	title1 = variantMap[TEXT("title")].GetValue<FString>();
	questID2 = variantMap[TEXT("questID")].GetValue<int32>();
	taskTitle3 = variantMap[TEXT("taskTitle")].GetValue<FString>();
	reward4 = variantMap[TEXT("reward")].GetValue<uint16>();
	soldierScriptID5 = variantMap[TEXT("soldierScriptID")].GetValue<FString>();
}

FVariant FTRAIN_SOLDIER_QUEST_DICT::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("title"), title1);
	variantMap.Add(TEXT("questID"), questID2);
	variantMap.Add(TEXT("taskTitle"), taskTitle3);
	variantMap.Add(TEXT("reward"), reward4);
	variantMap.Add(TEXT("soldierScriptID"), soldierScriptID5);

	return FVariant(variantMap);
}


FITEM_FOR_CLIENT::FITEM_FOR_CLIENT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue< KBEngine::FVariantMap >();
	id = variantMap[TEXT("id")].GetValue< int32 >();
	uid = FString::Printf(TEXT("%llu"), variantMap[TEXT("uid")].GetValue< uint64 >() );
	amount = variantMap[TEXT("amount")].GetValue< int32 >();
	bindType = variantMap[TEXT("bindType")].GetValue< int32 >();
	itemOrder = variantMap[TEXT("itemOrder")].GetValue< int32 >();
	itemEndTime = variantMap[TEXT("itemEndTime")].GetValue< FString >();
	dynamicData = variantMap[TEXT("dynamicData")].GetValue< FString >();
}

FCROND_DATA_DICT::FCROND_DATA_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue< KBEngine::FVariantMap >();
	status = variantMap[TEXT("status")].GetValue< uint8 >();
	timeTxt = variantMap[TEXT("timeTxt")].GetValue< FString >();
	nextStartTime = FSTRING_TO_INT(variantMap[TEXT("nextStartTime")].GetValue< FString >());
}

FACTIVITY_DATA_DICT::FACTIVITY_DATA_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue< KBEngine::FVariantMap >();
	scriptID = variantMap[TEXT("scriptID")].GetValue< FString >();
	KBEngine::FVariantArray variantArray_crondList = variantMap[TEXT("crondList")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_crondList)
	{
		FCROND_DATA_DICT element1 = FCROND_DATA_DICT(elementVariant0);
		crondList.Add(element1);
	}
}

FACTIVITIES_DATA_DICT::FACTIVITIES_DATA_DICT(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue< KBEngine::FVariantMap >();
	month = variantMap[TEXT("month")].GetValue< FString >();
	day = variantMap[TEXT("day")].GetValue< FString >();
	wday = variantMap[TEXT("wday")].GetValue< FString >();
	KBEngine::FVariantArray variantArray_table = variantMap[TEXT("table")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_table)
	{
		FACTIVITY_DATA_DICT element1 = FACTIVITY_DATA_DICT(elementVariant0);
		table.Add(element1);
	}
}

FBHZB_TONG_INTEGRALDATA::FBHZB_TONG_INTEGRALDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	tongDBID = variantMap[TEXT("tongDBID")].GetValue<uint64>();
	tongName = variantMap[TEXT("tongName")].GetValue<FString>();
	tongLevel = variantMap[TEXT("tongLevel")].GetValue<int32>();
	occupyPointAmount = variantMap[TEXT("occupyPointAmount")].GetValue<int32>();
	integral = variantMap[TEXT("integral")].GetValue<int32>();
	camp = variantMap[TEXT("camp")].GetValue<int32>();
}

LINGTIAN_DATA::LINGTIAN_DATA(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	scriptID = variantMap[TEXT("scriptID")].GetValue<FString>();
	seedNum = variantMap[TEXT("seedNum")].GetValue<int32>();
	growthStage = variantMap[TEXT("growthStage")].GetValue<int8>();
	growTime = variantMap[TEXT("growTime")].GetValue<uint32>();
}

LINGTIAN_DATA::LINGTIAN_DATA()
{

}

LINGTIAN_DATA_ARR::LINGTIAN_DATA_ARR()
{
}

LINGTIAN_DATA_ARR::LINGTIAN_DATA_ARR(const FVariant & variant)
{
	KBEngine::FVariantArray _dictDataList = variant.GetValue<KBEngine::FVariantArray>();
	for (FVariant& _dictData : _dictDataList)
	{
		datas.Add(LINGTIAN_DATA(_dictData));
	}
}

CLIENT_DONGFUDATA::CLIENT_DONGFUDATA()
{

}

CLIENT_DONGFUDATA::CLIENT_DONGFUDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	dongFuType = variantMap[TEXT("dongFuType")].GetValue<int8>();
	group = variantMap[TEXT("group")].GetValue<int16>();
	batteleID = variantMap[TEXT("batteleID")].GetValue<int32>();
	level = variantMap[TEXT("level")].GetValue<INT8>();
	playerName = variantMap[TEXT("playerName")].GetValue<FString>();
	challengeState = variantMap[TEXT("challengeState")].GetValue<int8>();
}

CLIENT_DONGFUDATA_ARR::CLIENT_DONGFUDATA_ARR()
{

}

CLIENT_DONGFUDATA_ARR::CLIENT_DONGFUDATA_ARR(const FVariant& variant)
{
	KBEngine::FVariantArray _dictDataList = variant.GetValue<KBEngine::FVariantArray>();
	for (FVariant& _dictData : _dictDataList)
	{
		datas.Add(CLIENT_DONGFUDATA(_dictData));
	}
}

BHZB_TONG_SIGNUP_RANK_DATA::BHZB_TONG_SIGNUP_RANK_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	tongDBID = variantMap[TEXT("tongDBID")].GetValue<uint64>();
	tongName = variantMap[TEXT("tongName")].GetValue<FString>();
	tongLevel = variantMap[TEXT("tongLevel")].GetValue<int32>();
	activity = variantMap[TEXT("activity")].GetValue<uint32>();
	tongMemNum = variantMap[TEXT("tongMemNum")].GetValue<int32>();
	camp = variantMap[TEXT("camp")].GetValue<int32>();
}

BHZB_POINT_DATA::BHZB_POINT_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	index = variantMap[TEXT("index")].GetValue<int32>();
	occupyPlayerDBID = variantMap[TEXT("occupyPlayerDBID")].GetValue<uint64>();
	occupyPlayerName = variantMap[TEXT("occupyPlayerName")].GetValue<FString>();
	occupyTongDBID = variantMap[TEXT("occupyTongDBID")].GetValue<uint64>();
	occupyTongName = variantMap[TEXT("occupyTongName")].GetValue<FString>();
	pointType = variantMap[TEXT("pointType")].GetValue<uint8>();
	declareWarState = variantMap[TEXT("declareWarState")].GetValue<uint8>();
	fightEndTime = variantMap[TEXT("fightEndTime")].GetValue<FString>();
	restEndTime = variantMap[TEXT("restEndTime")].GetValue<FString>();
	readyEndTime = variantMap[TEXT("readyEndTime")].GetValue<FString>();
	attackGroupTeamID = variantMap[TEXT("attackGroupTeamID")].GetValue<int32>();
	joinProtectGroupTeamID = variantMap[TEXT("joinProtectGroupTeamID")].GetValue<int32>();
	declareTongDBID = variantMap[TEXT("declareTongDBID")].GetValue<uint64>();
	KBEngine::FVariantArray variantArray = variantMap[TEXT("joinAttackPlayerDBIDs")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray)
	{
		joinAttackPlayerDBIDs.Add(elementVariant0.GetValue<uint64>());
	}
	KBEngine::FVariantArray variantArray1 = variantMap[TEXT("joinProtectPlayerDBIDs")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray1)
	{
		joinProtectPlayerDBIDs.Add(elementVariant0.GetValue<uint64>());
	}
}

FDICT_STRING_POS_ITEM::FDICT_STRING_POS_ITEM()
{

}

FDICT_STRING_POS_ITEM::FDICT_STRING_POS_ITEM(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key1 = variantMap[TEXT("key")].GetValue<FString>();
	value2 = variantMap[TEXT("value")].GetValue<FVector>();

}

FVariant FDICT_STRING_POS_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("key"), key1);
	variantMap.Add(TEXT("value"), value2);

	return FVariant(variantMap);
}

FBATTACK_DATA::FBATTACK_DATA()
{

}

FBATTACK_DATA::FBATTACK_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	belongSide1 = variantMap[TEXT("belongSide")].GetValue<int8>();
	KBEngine::FVariantArray variantArray_datas2 = variantMap[TEXT("datas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_datas2)
	{
		FDICT_STRING_POS_ITEM element1 = FDICT_STRING_POS_ITEM(elementVariant0);
		datas2.Add(element1);
	}

}

FVariant FBATTACK_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("belongSide"), belongSide1);
	KBEngine::FVariantArray variantArray_datas2 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas2)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_datas2.Add(element1);
	}
	variantMap.Add(TEXT("datas"), variantArray_datas2);

	return FVariant(variantMap);
}

FBATTACK_MAP::FBATTACK_MAP()
{

}

FBATTACK_MAP::FBATTACK_MAP(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_dictDatas1 = variantMap[TEXT("dictDatas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_dictDatas1)
	{
		FBATTACK_DATA element1 = FBATTACK_DATA(elementVariant0);
		dictDatas1.Add(element1);
	}

}

FVariant FBATTACK_MAP::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_dictDatas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : dictDatas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_dictDatas1.Add(element1);
	}
	variantMap.Add(TEXT("dictDatas"), variantArray_dictDatas1);

	return FVariant(variantMap);
}

FBATTERY_INFOS::FBATTERY_INFOS()
{

}

FBATTERY_INFOS::FBATTERY_INFOS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	entityID1 = variantMap[TEXT("entityID")].GetValue<int32>();
	scriptID1 = variantMap[TEXT("scriptID")].GetValue<FString>();
	state2 = variantMap[TEXT("state")].GetValue<int8>();
	pos3 = variantMap[TEXT("pos")].GetValue<FVector>();
}

FVariant FBATTERY_INFOS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("entityID"), entityID1);
	variantMap.Add(TEXT("scriptID"), scriptID1);
	variantMap.Add(TEXT("state"), state2);
	variantMap.Add(TEXT("pos"), pos3);

	return FVariant(variantMap);
}

FBATTERY_MAP::FBATTERY_MAP()
{

}

FBATTERY_MAP::FBATTERY_MAP(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_dictDatas1 = variantMap[TEXT("dictDatas")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_dictDatas1)
	{
		FBATTERY_INFOS element1 = FBATTERY_INFOS(elementVariant0);
		dictDatas1.Add(element1);
	}

}

FVariant FBATTERY_MAP::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_dictDatas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : dictDatas1)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_dictDatas1.Add(element1);
	}
	variantMap.Add(TEXT("dictDatas"), variantArray_dictDatas1);

	return FVariant(variantMap);
}

void AliasAccountInfo::CreateFromVariant(const FVariant& val, AliasAccountInfo& out)
{
	auto VariantData = val.GetValue<KBEngine::FVariantMap>();
	out.GameTimeBalance = VariantData[TEXT("gameTimeBalance")].GetValue<int32>();
	out.LastLoginTime = VariantData[TEXT("lastLoginTime")].GetValue<FString>();
	out.LoginTime = VariantData[TEXT("loginTime")].GetValue<FString>();
}

BHZB_MAP_HOMEBARRACKSDATA::BHZB_MAP_HOMEBARRACKSDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	index = variantMap[TEXT("index")].GetValue<int32>();
	position = variantMap[TEXT("position")].GetValue<FVector>();
	belongTongDBID = variantMap[TEXT("belongTongDBID")].GetValue<uint64>();
	name = variantMap[TEXT("name")].GetValue<FString>();
}

BHZB_MAP_MEMBERPOSDATA::BHZB_MAP_MEMBERPOSDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	groupID = variantMap[TEXT("groupID")].GetValue<int32>();
	position = variantMap[TEXT("position")].GetValue<FVector>();
}

FMYSTERIOUSSHOPDATA_MAP::FMYSTERIOUSSHOPDATA_MAP(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	slotID = variantMap[TEXT("slotID")].GetValue<int32>();
	amount = variantMap[TEXT("amount")].GetValue<int32>();
}

ORIGIN_PET_CLIENT_SIMPLE_DATA::ORIGIN_PET_CLIENT_SIMPLE_DATA()
{
}

ORIGIN_PET_CLIENT_SIMPLE_DATA::ORIGIN_PET_CLIENT_SIMPLE_DATA(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("uid")].GetValue<uint64>();
	index = variantMap[TEXT("index")].GetValue<int8>();
	scriptID = variantMap[TEXT("scriptID")].GetValue<FString>();
	bEvolution = variantMap[TEXT("bEvolution")].GetValue<uint8>();
}

FVariant ORIGIN_PET_CLIENT_SIMPLE_DATA::ToVariant()
{
	return FVariant();
}

ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST::ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST()
{
}

ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST::ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST(const FVariant & variant)
{
	KBEngine::FVariantArray datas = variant.GetValue<KBEngine::FVariantArray>();
	for (auto it : datas)
	{
		dictDatas1.Add(ORIGIN_PET_CLIENT_SIMPLE_DATA(it));
	}
}

FVariant ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST::ToVariant()
{
	return FVariant();
}

FCHUANCHENG_SKILL_BAR_DATA::FCHUANCHENG_SKILL_BAR_DATA()
{
}

FCHUANCHENG_SKILL_BAR_DATA::FCHUANCHENG_SKILL_BAR_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<int32>();
	skillID = variantMap[TEXT("skillID")].GetValue<int32>();
	isLock = variantMap[TEXT("isLock")].GetValue<uint8>();
}

FVariant FCHUANCHENG_SKILL_BAR_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id);
	variantMap.Add(TEXT("skillID"), skillID);
	variantMap.Add(TEXT("isLock"), isLock);

	return FVariant(variantMap);
}


FCHUANCHENG_SKILL_BAR_DATAS::FCHUANCHENG_SKILL_BAR_DATAS()
{
}

FCHUANCHENG_SKILL_BAR_DATAS::FCHUANCHENG_SKILL_BAR_DATAS(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Datas1 = variantMap[TEXT("items")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& elementVariant0 : variantArray_Datas1)
	{
		FCHUANCHENG_SKILL_BAR_DATA element1 = FCHUANCHENG_SKILL_BAR_DATA(elementVariant0);
		datas.Add(element1);
	}
}

FVariant FCHUANCHENG_SKILL_BAR_DATAS::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray variantArray_Datas1 = KBEngine::FVariantArray();
	for (auto& elementVariant0 : datas)
	{
		FVariant element1 = elementVariant0.ToVariant();
		variantArray_Datas1.Add(element1);
	}
	variantMap.Add(TEXT("items"), variantArray_Datas1);

	return FVariant(variantMap);
}

FCITY_MEMBER_DATA::FCITY_MEMBER_DATA(const FVariant& variant)
{

	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();

	ID = variantMap[TEXT("id")].GetValue<uint64>();
	Name = variantMap[TEXT("roleName")].GetValue<FString>();
	BelongSide = variantMap[TEXT("belongSide")].GetValue<int32>();
	KillEnemy = variantMap[TEXT("killEnemy")].GetValue<int32>();
	Dead = variantMap[TEXT("dead")].GetValue<int32>();
	Assists = variantMap[TEXT("assists")].GetValue<int32>();
	KillSoldier = variantMap[TEXT("killSoldier")].GetValue<int32>();
	TotalExploit = variantMap[TEXT("totalGetExploit")].GetValue<int32>();
	OwnerSoldierDeadNum = variantMap[TEXT("ownerSoldierDeadNum")].GetValue<int32>();
}

FATT_CITY_MEMBER_DATA::FATT_CITY_MEMBER_DATA(const FVariant& variant)
{

	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	AttackName = variantMap[TEXT("attackName")].GetValue<FString>();
	ProtectName = variantMap[TEXT("protectName")].GetValue<FString>();

	KBEngine::FVariantArray TempArray = variantMap[TEXT("members")].GetValue<KBEngine::FVariantArray>();
	for (auto & VariantStr : TempArray)
	{
		Members.Add(FCITY_MEMBER_DATA(VariantStr));
	}
}

BHZB_TONG_WAR_DETAIL::BHZB_TONG_WAR_DETAIL(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	tongDBID = variantMap[TEXT("tongDBID")].GetValue<uint64>();
	integral = variantMap[TEXT("integral")].GetValue<int32>();
	rank = variantMap[TEXT("rank")].GetValue<int32>();
	occupyPointAmount = variantMap[TEXT("occupyPointAmount")].GetValue<int32>();
	KBEngine::FVariantArray tempTeamArray = variantMap[TEXT("teamDatas")].GetValue<KBEngine::FVariantArray>();
	for (auto tempTeam: tempTeamArray)
	{
		teamDatas.Add(BHZB_TONG_TEAM_DATA(tempTeam));
	}
	KBEngine::FVariantArray tempOccupyPointDataArray = variantMap[TEXT("occupyPointDatas")].GetValue<KBEngine::FVariantArray>();
	for (auto tempOccupyPointData : tempOccupyPointDataArray)
	{
		occupyPointDatas.Add(BHZB_TONG_OCCUPY_POINT_DATA(tempOccupyPointData));
	}
	KBEngine::FVariantArray tempWarMsgDataArray = variantMap[TEXT("warMsgDatas")].GetValue<KBEngine::FVariantArray>();
	for (auto tempWarMsgData : tempWarMsgDataArray)
	{
		warMsgDatas.Add(BHZB_TONG_MSG_DATA(tempWarMsgData));
	}
}

BHZB_TONG_TEAM_DATA::BHZB_TONG_TEAM_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	teamNumber = variantMap[TEXT("teamNumber")].GetValue<int32>();
	pointNumber = variantMap[TEXT("pointNumber")].GetValue<int32>();
	pointState = variantMap[TEXT("pointState")].GetValue<int32>();
	pointName = variantMap[TEXT("pointName")].GetValue<FString>();
}

BHZB_TONG_OCCUPY_POINT_DATA::BHZB_TONG_OCCUPY_POINT_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	pointNumber = variantMap[TEXT("pointNumber")].GetValue<int32>();
	pointState = variantMap[TEXT("pointState")].GetValue<int32>();
	pointName = variantMap[TEXT("pointName")].GetValue<FString>();
}

BHZB_TONG_MSG_DATA::BHZB_TONG_MSG_DATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	statusID = variantMap[TEXT("statusID")].GetValue<int32>();
	statusArgs = variantMap[TEXT("statusArgs")].GetValue<FString>();
}

FDICT_STR_STR_ITEM::FDICT_STR_STR_ITEM()
{

}

FDICT_STR_STR_ITEM::FDICT_STR_STR_ITEM(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	key = variantMap[TEXT("key")].GetValue<FString>();
	value = variantMap[TEXT("value")].GetValue<FString>();
}

FVariant FDICT_STR_STR_ITEM::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantMap dictData = KBEngine::FVariantMap();
	dictData.Add(TEXT("key"), key);
	dictData.Add(TEXT("value"), value);
	variantMap.Add(TEXT("dictData"), dictData);

	return FVariant(variantMap);
}

FDICT_STR_STR::FDICT_STR_STR()
{
}

FDICT_STR_STR::FDICT_STR_STR(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray _dictDataList = variantMap[TEXT("dictData")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& _dictData : _dictDataList)
	{
		FDICT_STR_STR_ITEM dictData = FDICT_STR_STR_ITEM(_dictData);
		dictDataList.Add(dictData.key, dictData.value);
	}
}

FVariant FDICT_STR_STR::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	KBEngine::FVariantArray _dictDataList = KBEngine::FVariantArray();
	for (auto it = dictDataList.CreateConstIterator(); it; ++it)
	{
		KBEngine::FVariantMap dictData = KBEngine::FVariantMap();
		dictData.Add(TEXT("key"), it.Key());
		dictData.Add(TEXT("value"), it.Value());
		_dictDataList.Add(dictData);
	}
	variantMap.Add(TEXT("dictData"), _dictDataList);
	return FVariant();
}

FROLLDOM_DATA::FROLLDOM_DATA()
{
}

FROLLDOM_DATA::FROLLDOM_DATA(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("UID")].GetValue<FString>();
	ownerDBID = variantMap[TEXT("ownerDBID")].GetValue<FString>();
	isPickUp = variantMap[TEXT("isPickUp")].GetValue<uint8>();
	maxRollDBID = variantMap[TEXT("maxRollDBID")].GetValue<FString>();
	maxRoll = variantMap[TEXT("maxRoll")].GetValue<int8>();
	selfRoll = variantMap[TEXT("selfRoll")].GetValue<int8>();
}

FVariant FROLLDOM_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("UID"), uid);
	variantMap.Add(TEXT("ownerDBID"), ownerDBID);
	variantMap.Add(TEXT("isPickUp"), isPickUp);
	variantMap.Add(TEXT("maxRollDBID"), maxRollDBID);
	variantMap.Add(TEXT("maxRoll"), maxRoll);
	variantMap.Add(TEXT("selfRoll"), selfRoll);
	return FVariant();
}

FAUCTION_DATA::FAUCTION_DATA()
{
}

FAUCTION_DATA::FAUCTION_DATA(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	uid = variantMap[TEXT("UID")].GetValue<FString>();
	ownerDBID = variantMap[TEXT("ownerDBID")].GetValue<FString>();
	isPickUp = variantMap[TEXT("isPickUp")].GetValue<uint8>();
	maxAuctionDBID = variantMap[TEXT("maxAuctionDBID")].GetValue<FString>();
	selfMoney = variantMap[TEXT("selfMoney")].GetValue<int32>();
	round = variantMap[TEXT("round")].GetValue<uint8>();
	lastAuctionDBID = variantMap[TEXT("lastAuctionDBID")].GetValue<FString>();
	curAuctionRoleAmount = variantMap[TEXT("curAuctionRoleAmount")].GetValue<uint8>();
	maxAuctionMoney = variantMap[TEXT("maxAuctionMoney")].GetValue<int32>();
}

FVariant FAUCTION_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("UID"), uid);
	variantMap.Add(TEXT("ownerDBID"), ownerDBID);
	variantMap.Add(TEXT("isPickUp"), isPickUp);
	variantMap.Add(TEXT("maxAuctionDBID"), maxAuctionDBID);
	variantMap.Add(TEXT("selfMoney"), selfMoney);
	variantMap.Add(TEXT("round"), round);
	variantMap.Add(TEXT("lastAuctionDBID"), lastAuctionDBID);
	variantMap.Add(TEXT("curAuctionRoleAmount"), curAuctionRoleAmount);
	variantMap.Add(TEXT("maxAuctionMoney"), maxAuctionMoney);
	return FVariant();
}

FAUCTION_HISTORY_DATA::FAUCTION_HISTORY_DATA()
{
}

FAUCTION_HISTORY_DATA::FAUCTION_HISTORY_DATA(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	id = variantMap[TEXT("id")].GetValue<FString>();
	roleName = variantMap[TEXT("roleName")].GetValue<FString>();
	result = variantMap[TEXT("result")].GetValue<int8>();
	money = variantMap[TEXT("money")].GetValue<int32>();
}

FVariant FAUCTION_HISTORY_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("id"), id);
	variantMap.Add(TEXT("roleName"), roleName);
	variantMap.Add(TEXT("result"), result);
	variantMap.Add(TEXT("money"), money);
	return FVariant();
}

FALLBHZB_TONG_INTEGRALDATA::FALLBHZB_TONG_INTEGRALDATA(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	tongDBID = variantMap[TEXT("tongDBID")].GetValue<uint64>();
	tongName = variantMap[TEXT("tongName")].GetValue<FString>();
	tongLevel = variantMap[TEXT("tongLevel")].GetValue<int32>();
	totalIntegral = variantMap[TEXT("totalIntegral")].GetValue<int32>();
	integral = variantMap[TEXT("integral")].GetValue<int32>();
	camp = variantMap[TEXT("camp")].GetValue<int32>();
	startTime = variantMap[TEXT("startTimes")].GetValue<FString>();
}

FZYJJ_REWARD_DATA::FZYJJ_REWARD_DATA()
{
}

FZYJJ_REWARD_DATA::FZYJJ_REWARD_DATA(const FVariant & variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	exp = variantMap[TEXT("exp")].GetValue<uint32>();
	feats = variantMap[TEXT("feats")].GetValue<uint32>();
	exploit = variantMap[TEXT("exploit")].GetValue<uint32>();
	contribution = variantMap[TEXT("contribution")].GetValue<uint32>();
}

FVariant FZYJJ_REWARD_DATA::ToVariant()
{
	KBEngine::FVariantMap variantMap = KBEngine::FVariantMap();
	variantMap.Add(TEXT("exp"), exp);
	variantMap.Add(TEXT("feats"), feats);
	variantMap.Add(TEXT("exploit"), exploit);
	variantMap.Add(TEXT("contribution"), contribution);
	return FVariant();
}