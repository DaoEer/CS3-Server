// Fill out your copyright notice in the Description page of Project Settings.


#include "TestInterface.h"
#include "Util/CS3Debug.h"
#include "JsonFieldData.h"
#include "GameData/Test/TestStructA.h"
#include "GameData/Test/TestStructAArray.h"
#include "GameData/Test/TestStructC.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Entity/Alias.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/CS3Entity.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTestInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTestInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	

void UTestInterface::testCellCpp1(int32 a, float b, const FString& c)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("inta = %d, floatb = %f, stringc = %s"), a, b, *c);
}

void UTestInterface::testCellCpp2(const TArray<int32>& strinlist)
{
	for (auto str : strinlist)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("each FString = %d"), str);
	}
}

void UTestInterface::testCellCpp3_Implementation(const TArray<FString>& strinlist)
{
	for (auto str : strinlist)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("each FString = %s"), *str);
	}
}

void UTestInterface::testJsonCpp1(const FString& jsonstr)
{
	/*
	jsonstr = "{"ROOT":[{"aa":1, "bb":2.0, "cc":"fdsafdsfasdf"}, {"aa":2, "bb":3.0, "cc":"rewrttwq"}]}"
	*/
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("jsonstr = %s"), *jsonstr);
	FTestStructAArray tempStructArray;
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(jsonstr);
	auto temparray = returnvalue->GetObjectArray(this, TEXT("ROOT"));
	for (auto item : temparray)
	{
		FTestStructA tempStructA;
		tempStructA.aa = _tstoi(*item->GetString(TEXT("aa")));
		tempStructA.bb = _tstof(*item->GetString(TEXT("bb")));
		//tempStructA.aa = FCString::Atoi(*(item->GetString(TEXT("aa"))));
		//tempStructA.bb = FCString::Atof(*(item->GetString(TEXT("bb"))));
		tempStructA.cc = item->GetString(TEXT("cc"));
		tempStructArray.StructAArray.Add(tempStructA);
	}
}

void UTestInterface::testJsonCpp2(const FString& jsonstr)
{
	/*
	jsonstr = "{"Root":{"aa":1, "bb":2.0, "cc":"fdsafdsf", "dd":["1111", "22222"]}}"
	*/
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("jsonstr = %s"), *jsonstr);
	FTestStructC tempStructC;
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(jsonstr);
	auto value = returnvalue->GetObject(TEXT("ROOT"));
	tempStructC.aa = _tstoi(*value->GetString(TEXT("aa")));
	tempStructC.bb = _tstof(*value->GetString(TEXT("bb")));
	//tempStructC.aa = FCString::Atoi(*(value->GetString(TEXT("aa"))));
	//tempStructC.bb = FCString::Atof(*(value->GetString(TEXT("bb"))));
	tempStructC.cc = value->GetString(TEXT("cc"));
	for (auto item : value->GetStringArray(TEXT("dd")))
	{
		tempStructC.dd.Add(item);
	}

}

void UTestInterface::testIntList()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testIntList"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testIntList : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testIntList : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}

	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	arr.Add(FVariant(10000));
	arr.Add(FVariant(20000));
	arr.Add(FVariant(30000));
	args.Add(FVariant(arr));
	player->CellCall(TEXT("testIntList"), args);
}

void UTestInterface::testFloatList()
{
	//不建议使用，下面的float转换存在精度丢失的问题
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testFloatList"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testFloatList : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testFloatList : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	arr.Add(FVariant((float)145446.1));
	arr.Add(FVariant((float)24213.2));
	arr.Add(FVariant((float)300000.3));
	args.Add(FVariant(arr));
	player->CellCall(TEXT("testFloatList"), args);
}

void UTestInterface::testDoubleList()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testDoubleList"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testDoubleList : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testDoubleList : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	arr.Add(FVariant((double)2145446.1));
	arr.Add(FVariant((double)224213.2));
	arr.Add(FVariant((double)310000.3));
	args.Add(FVariant(arr));
	player->CellCall(TEXT("testDoubleList"), args);
}

void UTestInterface::testStringList()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testStringList"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testStringList : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testStringList : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	arr.Add(FVariant(TEXT("aaaaa")));
	arr.Add(FVariant(TEXT("bbbbb")));
	arr.Add(FVariant(TEXT("ccccc")));
	args.Add(FVariant(arr));
	player->CellCall(TEXT("testStringList"), args);
}

void UTestInterface::testClientCall1()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testClientCall1"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testClientCall1 : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testClientCall1 : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	int32 a = 1;
	float b = 2.0;
	FString c = TEXT("fdsfasdfsa"); 
	KBEngine::FVariantArray d;
	d.Add(FVariant(TEXT("AAA")));
	d.Add(FVariant(TEXT("BBB")));
	args.Add((int32)a);
	args.Add((double)b);
	args.Add(c);
	args.Add(FVariant(d));
	player->CellCall(TEXT("testClientCall1"), args);
}

void UTestInterface::testComplex()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testComplex"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testComplex : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testComplex : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	int32 a = 1;
	float b = 2.0;
	FString c = TEXT("fdsfasdfsa");
	//testitem
	TESTITEM testitem;
	testitem.id = 1000;
	testitem.uid = 10000;
	testitem.amount = 10;
	testitem.misc = TEXT("ITEM测试");
	testitem.flag.Add(TEXT("AAA"));
	testitem.flag.Add(TEXT("BBB"));
	KBEngine::FVariantMap d;
	testitem.ToFVariantMap(d);

	args.Add(a);
	args.Add(b);
	args.Add(c);
	args.Add(FVariant(d));
	player->CellCall(TEXT("testComplex"), args);
}

void UTestInterface::testComplex1()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("testComplex1"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testComplex1 : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::testComplex1 : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;

	TESTITEMS testitems;
	testitems.id = 1000;

	//testitem
	TESTITEM testitem;
	testitem.id = 1000;
	testitem.uid = 10000;
	testitem.amount = 10;
	testitem.misc = TEXT("ITEM测试");
	testitem.flag.Add(TEXT("AAA"));
	testitem.flag.Add(TEXT("BBB"));
	//testitem1
	TESTITEM testitem1;
	testitem1.id = 1001;
	testitem1.uid = 10001;
	testitem1.amount = 11;
	testitem1.misc = TEXT("ITEM测试2");
	testitem1.flag.Add(TEXT("CCC"));
	testitem1.flag.Add(TEXT("DDD"));

	testitems.itemList.Add(testitem);
	testitems.itemList.Add(testitem1);

	KBEngine::FVariantMap d;
	testitems.ToFVariantMap(d);

	args.Add(FVariant(1));
	args.Add(FVariant(d));
	player->CellCall(TEXT("testComplex1"), args);
}

void UTestInterface::testIntAndFStringList()
{
	TArray<int32> intlist;
	intlist.Add(1000);
	intlist.Add(2000);
	intlist.Add(3000);
	TArray<FString> stringlist;
	stringlist.Add(TEXT("AAAA"));
	stringlist.Add(TEXT("BBBB"));
	stringlist.Add(TEXT("CCCC"));
	CellCallWithIntList(TEXT("testIntList"), intlist);
	CellCallWithFStringList(TEXT("testStringList"), stringlist);
}

void UTestInterface::testGolbalIntAndFStringList()
{
	TArray<int32> intlist;
	intlist.Add(1000);
	intlist.Add(2000);
	intlist.Add(3000);
	TArray<FString> stringlist;
	stringlist.Add(TEXT("AAAA"));
	stringlist.Add(TEXT("BBBB"));
	stringlist.Add(TEXT("CCCC"));
	UGolbalBPFunctionLibrary::CellCallWithIntList(EntityID, TEXT("testIntList"), intlist);
	UGolbalBPFunctionLibrary::CellCallWithFStringList(EntityID, TEXT("testStringList"), stringlist);
}

void UTestInterface::testGetValue()
{
	int32 playerid = UGolbalBPFunctionLibrary::GetPlayerID();
	int32 testint8 = UGolbalBPFunctionLibrary::GetIntPropertyValue(playerid, TEXT("testint8"));
	int32 testint16 = UGolbalBPFunctionLibrary::GetIntPropertyValue(playerid, TEXT("testint16"));
	int32 testint32 = UGolbalBPFunctionLibrary::GetIntPropertyValue(playerid, TEXT("testint32"));
	int32 testuint8 = UGolbalBPFunctionLibrary::GetIntPropertyValue(playerid, TEXT("testuint8"));
	int32 testuint16 = UGolbalBPFunctionLibrary::GetIntPropertyValue(playerid, TEXT("testuint16"));
	float testfloat = UGolbalBPFunctionLibrary::GetFloatPropertyValue(playerid, TEXT("testfloat"));
	double testdouble = UGolbalBPFunctionLibrary::GetDoublePropertyValue(playerid, TEXT("testdouble"));
	FString teststring = UGolbalBPFunctionLibrary::GetFStringPropertyValue(playerid, TEXT("teststring"));
	FString testunicode = UGolbalBPFunctionLibrary::GetFStringPropertyValue(playerid, TEXT("testunicode"));
	int32 testuint32 = UGolbalBPFunctionLibrary::GetIntPropertyValue(playerid, TEXT("testuint32"));
}

void UTestInterface::RPC_CELL_testCommonBP(const FString& STRING_1, const FString& STRING_2, const FString& STRING_3)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::RPC_CELL_testCommonBP : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);
	args.Add(STRING_3);

	entity->CellCall(TEXT("testCommonBP"), args);
}

void UTestInterface::RPC_CELL_testIntList(const TArray<int32>& ARRAY_INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::RPC_CELL_testIntList : entity!"));
		return;
	}
	KBEngine::FVariantArray ARRAY_INT32_1_ = KBEngine::FVariantArray();
	for (auto& elementVariant0 : ARRAY_INT32_1)
	{
		FVariant element1 = FVariant(elementVariant0);
		ARRAY_INT32_1_.Add(element1);
	}

	KBEngine::FVariantArray args;
	args.Add(ARRAY_INT32_1_);

	entity->CellCall(TEXT("testIntList"), args);
}

void UTestInterface::RPC_CELL_testStringList(const TArray<FString>& ARRAY_STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTestInterface::RPC_CELL_testStringList : entity!"));
		return;
	}
	KBEngine::FVariantArray ARRAY_STRING_1_ = KBEngine::FVariantArray();
	for (auto& elementVariant0 : ARRAY_STRING_1)
	{
		FVariant element1 = FVariant(elementVariant0);
		ARRAY_STRING_1_.Add(element1);
	}

	KBEngine::FVariantArray args;
	args.Add(ARRAY_STRING_1_);

	entity->CellCall(TEXT("testStringList"), args);
}

void UTestInterface::InitBlueCB()
{
	ArrBlueFunc.Add("TestCellCommon1");
	ArrBlueFunc.Add("TestCellCommon2");
	ArrBlueFunc.Add("TestCellCommon3");
	ArrBlueFunc.Add("TestCellCommon4");
	ArrBlueFunc.Add("testJson1");
	ArrBlueFunc.Add("testJson2");
	ArrBlueFunc.Add("testCellCpp1");
	ArrBlueFunc.Add("testCellCpp2");
	ArrBlueFunc.Add("testCellCpp3");
	ArrBlueFunc.Add("testCellCpp4");
	ArrBlueFunc.Add("testCellCpp5");
	ArrBlueFunc.Add("testJsonCpp1");
	ArrBlueFunc.Add("testJsonCpp2");
}
