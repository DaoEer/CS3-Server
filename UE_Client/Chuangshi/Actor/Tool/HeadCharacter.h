#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "HeadCharacter.generated.h"

/*
* 文件名称：HeadCharacter.h
* 功能说明：用于动态半身像配置工具，因为工具不进游戏，需要自建一个玩家
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-08-12
*/


UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AHeadCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	AHeadCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void OnCreateModelOver() override;
	virtual void OnCreateApperanceOver() override;

public:
	///通过HeadID更换模型
	UFUNCTION(BlueprintCallable, Category = "HeadCharacter")
		void ChangeModel(FString ModelID);
	
	UFUNCTION(BlueprintCallable, Category = "HeadCharacter")
		void PlayAction_BP(FName ActionID);

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	
private:
	
};
