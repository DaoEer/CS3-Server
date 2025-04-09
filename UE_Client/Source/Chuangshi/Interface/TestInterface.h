// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "TestInterface.generated.h"

/*
* 文件名称：TestInterface.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-05
*/

/**
 * Test接口类，示例接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UTestInterface : public UCS3EntityInterface
{
	typedef UCS3EntityInterface Supper;
	GENERATED_BODY()
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("TestInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_TestInterface.BP_TestInterface_C'"); } //获取蓝图对象路径
		
	//******************************cell call client method******************************
	//******************************common***********************************************
	UPROPERTY(BlueprintReadOnly, Category = "TestInterface")
		TArray<int32> myintlist;
	UPROPERTY(BlueprintReadOnly, Category = "TestInterface")
		TArray<FString> mystrlist;

	/**
	*BlueprintCallable,cell call client method
	*
	*@param a int32参数a
	*@param b float参数b
	*@param c FString参数c
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server | Common")
		void testCellCpp1(int32 a, float b, const FString& c);

	/**
	*BlueprintCallable,cell call client method
	*
	*@param strinlist FString数组
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server | Common")
		void testCellCpp2(const TArray<int32>& strinlist);

	/**
	*BlueprintNativeEvent,cell call client method，如果蓝图覆盖了此方法，将会调用BP_TestInterface蓝图的此同名方法
	*
	*@param strinlist FString数组
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void testCellCpp3(const TArray<FString>& strinlist);

	/**
	*BlueprintImplementableEvent,cell call client method，c++没有实现，调用蓝图的方法
	*
	*@param strinlist FString数组
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Server | Common")
		void testCellCpp4(const TArray<FString>& strinlist);

	//******************************json***************************************************

	/**
	*BlueprintCallable,cell call client method
	*
	*@param jsonstr 参数为Json 如：jsonstr = "{"ROOT":[{"aa":1, "bb":2.0, "cc":"fdsafdsfasdf"}, {"aa":2, "bb":3.0, "cc":"rewrttwq"}]}"
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server | Common")
		void testJsonCpp1(const FString& jsonstr);

	/**
	*BlueprintCallable,cell call client method
	*
	*@param jsonstr 参数为Json 如：jsonstr = "{"Root":{"aa":1, "bb":2.0, "cc":"fdsafdsf", "dd":["1111", "22222"]}}"
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server | Common")
		void testJsonCpp2(const FString& jsonstr);


	//******************************client call cell method**********************************
	//******************************common***************************************************
	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testIntList();///<BlueprintCallable,client call cell method,参数为int数组

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testFloatList();///<BlueprintCallable,client call cell method,参数为float数组，建议不使用，存在精度丢失，建议使用testStringList

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testDoubleList();///<BlueprintCallable,client call cell method,参数为float数组，建议不使用

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testStringList();///<BlueprintCallable,client call cell method,参数为String数组

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testClientCall1();///<BlueprintCallable,client call cell method,参数为int32，float，FString，KBEngine::FVariantArray

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testComplex();///<BlueprintCallable,client call cell method,参数为int32，float，FString，KBEngine::FVariantMap

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testComplex1();///<BlueprintCallable,client call cell method,参数为int32，float，FString， KBEngine::FVariantMap

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testIntAndFStringList();///<测试BaseInterface中的CallCellWithIntList和CallCellWithFStringList

	UFUNCTION(BlueprintCallable, Category = "Client | Common")
		void testGolbalIntAndFStringList();///<测试UGolbalBPFunctionLibrary中的CallCellWithIntList和CallCellWithFStringList

	UFUNCTION(BlueprintCallable, Category = "Golbal")
		void testGetValue();///<测试UGolbalBPFunctionLibrary中关于获取entity的属性值的方法

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_testCommonBP(const FString& STRING_1, const FString& STRING_2, const FString& STRING_3);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_testIntList(const TArray<int32>& ARRAY_INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_testStringList(const TArray<FString>& ARRAY_STRING_1);

	virtual void InitBlueCB() override;
};
