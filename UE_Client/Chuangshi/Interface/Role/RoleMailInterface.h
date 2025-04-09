// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/MailData.h"
#include "RoleMailInterface.generated.h"

/*
* 文件名称：RoleMailInterface.h
* 功能说明：玩家邮件
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-07-24
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleMailInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleMailInterface();
	~URoleMailInterface();
	static FString GetName() { return TEXT("RoleMailInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleMailInterface.BP_RoleMailInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	*接收所有邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void ReceiveAllMailBP();
	void ReceiveAllMail(const FVariantArray& recordNames,const FVariantArray& AllMailData);

	/**
	*Define method
	*接收一封邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void ReceiveMailBP(const FString& mailId);

	void ReceiveMail(const FVariant& MailData);

	/**
	*Define method
	*删除邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void OnMailDeletedBP(const TArray<FString>& MailIDList);

	void OnMailDeleted(const FVariantArray&  mailids);
	/**
	*Define method
	*提取一封邮件成功
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void CLIENT_ExtractMailSuccess(const FString& MailID);

	/**
	*Define method
	*打开邮箱界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void CLIENT_OpenMailWindow();

	FMailData AddOneMailData(const FVariant& MailData);

	void AddMailByJsonData(const FString& jsonData);

	void BASE_TimeToDelMail(const FString& MailID);

	/**
	*请求删除邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		void BASE_RequestDeleteMail(TArray<FString> MailIDList);

	/**
	*请求发送邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		void BASE_RequestSendMail(FString receiverName, FString title, FString content);

	/**
	*Define method
	*发送邮件成功回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void OnMailSendSuccess();

	/**
	*请求提取邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		void CELL_RequestExtractMail(TArray<FString> MailIDList);

	/**
	*发送已读邮件到服务器
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		void BASE_ReadedMailNotifyToSever(FString MailID);

	/**
	*获得某个发送类型的邮件列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		TArray<FMailData> GetMailDataByMailSendType(MAIL_SEND_TYPE mailSendType);

	/**
	*通过邮件ID获得邮件
	*
	*param mailID 邮件ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		FMailData GetMailDataByMailID(FString mailID);

	/**
	*判断某个发送类型的邮件列表是否有未读邮件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		bool IsMailDataNotRead(MAIL_SEND_TYPE mailSendType);


	/**
	*Define method
	*增加收信人的记录
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void CLIENT_AddRecordReceiveName( const FString& receiveName );

	/**
	*Define method
	*删除收信人的记录
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMailInterface")
		void CLIENT_RemoveRecordReceiveName(const FString& receiveName);

	/**
	*获得收信人的记录
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMailInterface")
		TArray<FString> GetRecordReceiveNames();

	virtual void InitBlueCB() override;

	virtual void onLeaveWorld() override;
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<FString,FMailData> MailMap;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> RecordReceiceNames;

private:
	TMap< FString, FTimerHandle > MailTimerDict;
};