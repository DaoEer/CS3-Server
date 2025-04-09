// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "GameData/GameDeFine.h"
#include "CS3Base/CS3EntityInterface.h"
#include "StatusMessageInterface.generated.h"

/*
* 文件名称：StatusMessageInterface.h
* 功能说明：消息提示类
* 文件作者：liulinghao
* 目前维护：hejingke
* 创建时间：2016-11-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UStatusMessageInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UStatusMessageInterface();
	~UStatusMessageInterface();
	static FString GetName() { return TEXT("StatusMessageInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_StatusMessageInterface.BP_StatusMessageInterface_C'"); } //获取蓝图对象路径
	/**
	*Define method
	*BlueprintCallable,通知消息
	*
	*@param statusID 消息类型
	*@param args 参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
	void statusMessage(const int32& statusID, const FString& args);


	/**
	*Define method
	*BlueprintCallable,通知消息
	*
	*@param statusID 消息类型
	*@param args 参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void HideStatusMessage(const int32& statusID);


	/**
	*Define method
	*BlueprintCallable,服务器与客户端交互，点击按钮自动回应服务器
	*
	*@param statusID 消息类型
	*@param args 参数
	*@param key 服务器自动生成的值
	*@param Compotent 是cell 还是 base 发过来的
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
	void inquireMessage(const int32& statusID, const FString& args, const int32 key, const FString& Compotent);

	/**
	*字符串替换
	*
	*@param replaceMessage 原字符串
	*@param args 替换参数
	*@param SplitChar 可选分隔符，默认“|”
	*
	*@return FString 替换后字符串
	*/
	static FString GetReplaceMessage(const FString& replaceMessage, const FString args = TEXT(""), FString SplitChar = TEXT("|"));

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_Cell_replyMessage(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_Base_replyMessage(const FString& STRING_1, const FString& STRING_2);

	virtual void InitBlueCB() override;
};
