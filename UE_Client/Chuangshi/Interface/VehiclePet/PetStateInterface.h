// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/StateInterface.h"
#include "PetStateInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UPetStateInterface : public UStateInterface
{
	GENERATED_BODY()

		typedef UStateInterface Supper;
	
public:

	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.PetStateInterface'"); } //获取蓝图对象路径
																																			   
																																					   /**
	*virtual,角色状态改变
	*
	*@param NewState 新的状态值
	*@param OldState 旧的状态值
	*
	*@return 无
	*/
	virtual void OnStateChanged(const int32& NewState, const int32& OldState)override;
};
