#pragma once
#include "CS3Base/CS3EntityInterface.h"
#include "RoleQTEInterface.generated.h"

/*
* 文件名称：RoleQTEInterface.h
* 功能说明：QTE
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-08-13
*/


UCLASS(BlueprintType)
class URoleQTEInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleQTEInterface();
	virtual ~URoleQTEInterface();
	
	static FString GetName() { return TEXT("RoleQTEInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleQTEInterface.BP_RoleQTEInterface_C'"); } //获取蓝图对象路径


public:
	virtual void InitBlueCB() override;
	/**
	*Define method
	*BlueprintNativeEvent，开始BuffQTE
	*
	*@param qteTypeList QTE类型列表
	*@param qteTimeList 时间列表
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQTEInterface")
		void OnStartBuffQTE(const FString& TableRowName);
	/**
	*Define method
	*BlueprintNativeEvent，结束QTE
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQTEInterface")
		void OnEndBuffQTE();

	/**
	*Define method
	*BlueprintNativeEvent，开始镜头QTE
	*@param Type  QTE类型
	*@param KeypressList 按键组合列表
	*@param qteTimeList  时间列表
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQTEInterface")
		void OnStartStoryQTE(const FString& TableRowName);

	void onCompleteQTEBuffEvent(bool bIsSuccess);

	void onCompleteBuffQTE( );
};

