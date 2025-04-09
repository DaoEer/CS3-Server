// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleTitleInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/GameObject.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTitleInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTitleInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleTitleInterface::URoleTitleInterface()
{
}


URoleTitleInterface::~URoleTitleInterface()
{
}

void URoleTitleInterface::onLeaveWorld()
{
	TitleData.Empty();
	AvailableTitleData.Empty();
	Supper::onLeaveWorld();
}


void URoleTitleInterface::SelectTitle(int32 TitleID)
{
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	if (SelfEntity != nullptr)
	{
		KBEngine::FVariantArray Args;
		Args.Add(TitleID);
		SelfEntity->CellCall(TEXT("CELL_selectTitle"), Args);
	}
}


void URoleTitleInterface::CLIENT_OnTitleAdded(int32 TitleID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnTitleAdded==============TitleID=%d"), TitleID);

	OnTitleAddedCB(TitleID);
}


void URoleTitleInterface::CLIENT_OnTitleRemoved(int32 TitleID)
{
	for (auto data: TitleData)
	{
		if (data.TitleID == TitleID)
		{
			TitleData.Remove(data);
			break;
		}
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnTitleRemoved==============TitleID=%d"), TitleID);
	OnTitleRemovedCB(TitleID);
}


void URoleTitleInterface::CLIENT_OnSetTitleData(int32 TitleID, FString AttackPropertiesStr, float LimitTime)
{
	FTITLE_DATA Data;
	Data.TitleID = TitleID;
	Data.AttackProperties = ParseAttackPropertiesStr(AttackPropertiesStr);
	Data.LimitTime = LimitTime;
	TitleData.Add(Data);
	
	TitleData.Sort([](const FTITLE_DATA& data1, const FTITLE_DATA& data2){ return data1.TitleID < data2.TitleID; });//按ID大小排序
	OnStartOwnTime();//通知蓝图倒计时
}

void URoleTitleInterface::CLIENT_OnSetAvailableTitleData(int32 TitleID, FString AttackPropertiesStr, float LimitTime)
{
	FTITLE_DATA Data;
	Data.TitleID = TitleID;
	Data.AttackProperties = ParseAttackPropertiesStr(AttackPropertiesStr);
	Data.LimitTime = LimitTime;
	AvailableTitleData.Add(Data);

	AvailableTitleData.Sort([](const FTITLE_DATA& data1, const FTITLE_DATA& data2) { return data1.TitleID < data2.TitleID; });//按ID大小排序

}

FTITLE_DATA  URoleTitleInterface::GetTitleDataByID(int32 TitleID)
{
	for (auto data: TitleData)
	{
		if (data.TitleID == TitleID)
		{
			return data;
		}
	}
	FTITLE_DATA tempData;
	return tempData;
}

FTITLE_DATA URoleTitleInterface::GetAvailableTitleDataByID(int32 TitleID)
{
	for (auto data : AvailableTitleData)
	{
		if (data.TitleID == TitleID)
		{
			return data;
		}
	}
	FTITLE_DATA tempData;
	return tempData;
}

bool URoleTitleInterface::IsOwnTitle(int32 TitleID)
{
	for (auto data : TitleData)
	{
		if (data.TitleID == TitleID)
		{
			return true;
		}
	}
	return false;
}

FString URoleTitleInterface::ParseAttackPropertiesStr(FString AttackPropertiesStr)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ParseAttackPropertiesStr==============AttackPropertiesStr=%s"),*ParsePropertiesStr(AttackPropertiesStr, TEXT("FFFFFFFF")));
	return ParsePropertiesStr(AttackPropertiesStr, TEXT("47A69EFF")); 
}


void URoleTitleInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnTitleAdded");
	ArrBlueFunc.Add("CLIENT_OnTitleRemoved");
	ArrBlueFunc.Add("CLIENT_OnSetTitleData");
	ArrBlueFunc.Add("CLIENT_OnSetAvailableTitleData");
	Supper::InitBlueCB();
}



FString URoleTitleInterface::ParsePropertiesStr(const FString& propstr, const FString& propcolor)
{
	return ParsePropertiesStr_v(propstr, propcolor);
}


FString URoleTitleInterface::ParsePropertiesStr_v(const FString& propstr, const FString& propcolor)
{
	FString describe = TEXT("");
	if (propstr != TEXT(""))
	{
		TArray<FString> propids;
		TArray<FString> propvalues;
		TArray<FString> idandvalues;
		propstr.ParseIntoArray(idandvalues, TEXT("|"), true);
		for (auto item : idandvalues)
		{
			FString left;
			FString right;
			item.Split(TEXT("#"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
			propids.Add(left);
			propvalues.Add(right);
		}
		if (propids.Num() > 0)
		{
			for (int i = 0; i < propids.Num(); i++)
			{
				describe += GetPropertyStr(propids[i], propvalues[i], propcolor);
			}
		}
	}
	return describe;
}

FString URoleTitleInterface::GetPropertyStr(const FString& propid, const FString& propvalue, const FString& propcolor)
{
	return GetPropertyStr_v(propid, propvalue, propcolor);
}

FString URoleTitleInterface::GetPropertyStr_v(const FString& propid, const FString& propvalue, const FString& propcolor)
{
	int32 propertyid = FSTRING_TO_INT(propid);
	FString describe = UGolbalBPFunctionLibrary::GetChinese(propid);
	switch (propertyid)
	{
	case 30001:
	case 30002:
	case 30003:
	case 30004:
	case 30005:
	case 30006:
	case 30007:
	case 30008:
	case 30009:
	case 30010:
	case 30011:
	case 30012:
	case 30013:
	{
		describe += propvalue;
		break;
	}
	case 30014:
	{
		describe = *FString::Printf(TEXT("%s%.2f"), *describe, (FSTRING_TO_FLOAT(propvalue)) / 100.0);
		break;
	}
	case 30015:
	case 30016:
	case 30017:
	{
		describe = *FString::Printf(TEXT("%s%.2f%%"), *describe, (FSTRING_TO_FLOAT(propvalue)) / 100.0);
		break;
	}
	default:
		check(false);
		break;
	}
	FString showdowcolor = propcolor;
	return StrToColorStr(describe, propcolor, showdowcolor, TEXT("[0,0]"));
}

FString URoleTitleInterface::StrToColorStr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset)
{
	if (inputstr == TEXT(""))
	{
		return inputstr;
	}
	return FString::Printf(TEXT("<text color=\"#%s\" shadowColor=\"#%s\" shadowOffset=\"#%s\">%s</text><br/>"), *colorstr, *shadowcolor, *shadowoffset, *inputstr);
}