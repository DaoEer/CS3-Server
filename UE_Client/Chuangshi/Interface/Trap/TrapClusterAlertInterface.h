// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "TrapInterface.h"
#include "TrapClusterAlertInterface.generated.h"

/*
* 文件名称：TrapClusterAlertInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTrapClusterAlertInterface : public UTrapInterface
{
	GENERATED_BODY()
	typedef UTrapInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UTrapClusterAlertInterface();
	~UTrapClusterAlertInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TrapClusterAlertInterface'"); } //获取蓝图对象路径
protected:
	void StartCheckRoleTimer(float interval);
	void StopCheckRoleTimer();
	bool HasCheckRoleTimer();
	void CheckRole();

public:
	virtual void OnEnterScenes() override;
	virtual void onLeaveWorld() override;     ///< 当Entity离开世界时，此方法被调用

private:
	FTimerHandle CheckRoleTimerHandle_;	     ///< 检测玩家timer
};