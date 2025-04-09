// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3Base/CS3EntityInterface.h"
#include "CS3Base/InterfaceDef.h"
#include "GMTestInterface.generated.h"


/**
 * 
 */
UCLASS()
class CHUANGSHI_API UGMTestInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	CS3_DECLARE_INTERFACE_MAP()
	typedef UCS3EntityInterface Supper;
public:
	UGMTestInterface();
	~UGMTestInterface();
	static FString GetName() { return TEXT("GMInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.GMTestInterface'"); } //获取蓝图对象路径


	void GMTestOpenEffect(const FString& effectType, const uint8& isOpen);


};
