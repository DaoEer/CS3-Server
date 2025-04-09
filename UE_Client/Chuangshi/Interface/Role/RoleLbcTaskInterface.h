// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "CS3Base/CS3EntityInterface.h"
#include "GameData/LBCTaskDatas.h"
#include "RoleLbcTaskInterface.generated.h"


/*
* 文件名称：RoleLbcTaskInterface.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-07-06
*/

/**
 * 玩家练兵场练兵任务
 */

UCLASS(BlueprintType)
class CHUANGSHI_API URoleLbcTaskInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleLbcTaskInterface() {};

	static FString GetName() { return TEXT("RoleLbcTaskInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleLbcTaskInterface.BP_RoleLbcTaskInterface_C'"); } //获取蓝图对象路径
	//打开任务面板
	UFUNCTION(BlueprintCallable, Category = "RoleLbcTaskInterface")
	void OpenLbcTaskUI(int32 type);
	//接受任务
	UFUNCTION(BlueprintCallable, Category = "RoleLbcTaskInterface")
	void AcceptLbcTask();
	//显示开始练兵界面
	void ShowLbcStartTrainWnd();
	//副本内 开始练兵
	UFUNCTION(BlueprintCallable, Category = "RoleLbcTaskInterface")
	void LbcTaskStartPlay();
	//玩家移动到指定位置
	void RoleMoveToLocation(const  KBEngine::FVariantArray& posList, const float& moveSpeed, const float& dis);
	//进入练兵场练兵操作
	void StartRoleLbcTaskOperation(const float& armLength, const FVector& cameraRotation);
	//退出练兵场练兵操作模式
	void EndRoleLbcTaskOperation();
	//创建尸体
	void LbcTaskCreateBody(const FString& model, const int32& amount, const float& radius, const FVector& centerPos);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleLbcTaskInterface")
	void LbcTaskCreateBodyBP(const FString& model, const int32& amount, const float& radius, const FVector& centerPos);
	//显示结算界面
	void ShowLbcTaskResult(const int32& result, const FString& fistGuardScriptID, const int32& exp, const int32& addExp, const int32& lossNum, const FString& cmdrerScriptID);

	void RPC_RoleMoveToLocationOver();

	virtual void InitBlueCB() override;
	virtual void onLeaveWorld() override;
private:
	void LoadLBCTaskDatas();
	void RoleMoveToPoint(bool firstOne,bool IsNext = true);
	
private:
	float CurPlayerCameraArmLength;
	FVector CurSocketOffset;
	float CurPlayerMoveSpeed;
	TArray<FLBCTASKDATA*> LBCTaskDatas;
	int32 posIndex = 0;
	TArray<FVector> pointList;
	float rolemoveSpeed;
	FTimerHandle DelayMoveEventHandle;///<检测QTE事件定时器
	float NewarmLength;
	FVector NewcameraRotation;
	float RoleDistance;
};