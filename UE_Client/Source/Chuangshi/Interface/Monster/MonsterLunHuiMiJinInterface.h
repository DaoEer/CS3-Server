// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterLunHuiMiJinInterface.generated.h"

/*
* 文件名称：MonsterLunHuiMiJinInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-12-24
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterLunHuiMiJinInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	UMonsterLunHuiMiJinInterface();
	~UMonsterLunHuiMiJinInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterLunHuiMiJinInterface'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;
};
