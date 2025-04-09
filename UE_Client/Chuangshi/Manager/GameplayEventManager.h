#pragma once

#include "GameData/CS3Object.h"
#include "GameplayEventManager.generated.h"

/*
* 文件名称：GameplayEventManager.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2018-11-12
*/

UCLASS(Blueprintable)
class CHUANGSHI_API UGameplayEventManager : public UCS3Object
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	UGameplayEventManager();
	~UGameplayEventManager();

	static UGameplayEventManager* GetInstance();

};