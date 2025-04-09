#pragma once

#include "GameData/ServerListData.h"
#include "CS3Base/CS3EntityInterface.h"
#include "RoleCrossServiceInterface.generated.h"


/*
* 文件名称：RoleCrossServiceInterface.h
* 功能说明：玩家跨服相关接口
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2020-04-13
*/


UCLASS(BlueprintType)
class CHUANGSHI_API URoleCrossServiceInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleCrossServiceInterface();
	~URoleCrossServiceInterface();
	static FString GetName() { return TEXT("RoleCrossServiceInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleCrossServiceInterface.BP_RoleCrossServiceInterface_C'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;

private:
	bool Check(FSERVER_DATA CurrServerData, FSERVER_DATA TargetServerData);
	void BeforeCrossService();
	void BeforeReturnServer();

public:

	/**
	*BlueprintCallable,请求跨服
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void RPC_RequestCrossService(FString TargetServerName);
	/**
	*Define Method
	*BlueprintNativeEvent,跨服请求结果
	*
	*@return 无
	*/
	void CLIENT_OnRequestCrossServiceResult(const FString& Result);
	/**
	*BlueprintCallable,请求返回原服
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void RPC_RequestReturnServer();
	/**
	*Define Method
	*BlueprintNativeEvent,返回原服请求结果
	*
	*@return 无
	*/
	void CLIENT_OnRequestReturnServerResult(const FString& Result);

	/**
	*Define method
	*BlueprintNativeEvent 跨服完成返回原地图
	*
	*@return 无
	*/
	void OnRoleReEnterWorld();

private:
};

