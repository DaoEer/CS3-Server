#pragma once

#include "Actor/GameCharacter.h"
#include "FlyCharacter.generated.h"

/*
* 文件名称：AFlyCharacter.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2018-07-11
*/

DECLARE_DELEGATE(FFlyCharacterOnCreateModelOverDelegate);//模型加载结束通知

/**
* 飞行基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API AFlyCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	AFlyCharacter();
	virtual void BeginPlay()override;

	virtual void SetInitAction() override;///<重写SetInitAction

	virtual void OnCreateModelOver() override;
public:
	FFlyCharacterOnCreateModelOverDelegate FlyCharacterOnCreateModelOver;
protected:
	virtual void InitBaseComponent() override;
};
