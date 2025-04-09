// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterCopyRoleModelInterface.h"
#include "MonsterExtFenShenInterface.generated.h"

/*
* 文件名称：MonsterExtFenShenInterface.h
* 功能说明：
* 文件作者：QRN
* 目前维护：QRN
* 创建时间：2020-09-07
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtFenShenInterface : public UMonsterCopyRoleModelInterface
{
	GENERATED_BODY()
	typedef UMonsterCopyRoleModelInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtFenShenInterface();
	~UMonsterExtFenShenInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtFenShenInterface'"); } //获取蓝图对象路径

	

	void BeginPosSyncServer();
	void EndPosSyncServer();
	
	// 发生动作位移同步位置到服务器，不用UMonsterPosSyncComponent；
	// 因为内部作了优化禁止移动，不向服务器同步位置。
	void UpdateVolatileDataToServer();


private:
	FTimerHandle UpdateVolHandle;
};
