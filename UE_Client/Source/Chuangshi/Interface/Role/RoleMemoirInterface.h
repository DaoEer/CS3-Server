// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "RoleMemoirInterface.generated.h"

/*
* 文件名称：RoleMemoirInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：yikun
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleMemoirInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleMemoirInterface();
	~URoleMemoirInterface();
	static FString GetName() { return TEXT("RoleMemoirInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleMemoirInterface.BP_RoleMemoirInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	*接收所有仙魔录ID  服务器回调函数
	*
	*@param memoirIDs 仙魔录ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMemoirInterface")
	void CLIENT_ReceiveMemoirIDList(const TArray<FString>& memoirIDs);

	/**
	*接收所有仙魔录ID  服务器回调函数(通知界面初始化数据)
	*
	*@param memoirIDs 仙魔录ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleMemoirInterface")
	void ReceiveMemoirIDListCB(const TArray<FString>& memoirIDs);

	/**
	*Define method
	*增加一个仙魔录ID
	*
	*@param memoirID 仙魔录ID
	*@param nextMemoirID 下一个仙魔录ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMemoirInterface")
	void CLIENT_AddMemoirStory(const FString& memoirID, const FString& nextMemoirID);

	/**
	*显示一个仙魔录
	*
	*@param memoirID 仙魔录ID
	*@param nextMemoirID 下一个仙魔录ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleMemoirInterface")
		void ShowMemoirStory(const FString& memoirID, const FString& nextMemoirID);

	/**
	*Define method
	*服务回调函数，通知播放仙魔录CG动画
	*
	*@param memoirCGID 仙魔录动画ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleMemoirInterface")
		void CLIENT_PlayMemoirCG(const FString& memoirCGID, const FString& memoirID);
	/**
	*触发仙魔录
	*
	*@param IsTrigger:True(触发), False(没有触发) 是否触发仙魔录
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleMemoirInterface")
	void TriggerMemoirState(bool IsTrigger);
	
	UFUNCTION(BlueprintCallable, Category = "RoleMemoirInterface")
		void CELL_endPlayMemoirCG();

	virtual void InitBlueCB() override;
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> MemoirIDList;///< 玩家仙魔录ID
};