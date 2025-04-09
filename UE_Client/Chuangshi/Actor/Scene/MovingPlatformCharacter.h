#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "MovingPlatformCharacter.generated.h"

/*
* 文件名称：MovingPlatformCharacter.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-05-15
*/

/*
* MovingPlatform类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AMovingPlatformCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()

#pragma region	Avatar功能相关
public:

	virtual void InitFilterActorComponent() override;

#pragma endregion
public:
	AMovingPlatformCharacter();///<构造函数
	virtual void BeginPlay()override;

	virtual void GossipWith() override;///<重写GossipWith
	virtual void SetInitAction() override;///<重写SetInitAction
	virtual void PlayDeadEffect() override;

	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void OnReadyToMoveBack();

	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void OnReadyToMove();

	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void starShade(const FString& EndTime);


	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void starDisPlay(const FString& EndTime);

	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void OnPlayerEnterMovingPlatform();

	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void OnPlayerLeaveMovingPlatform();

	UFUNCTION(BlueprintImplementableEvent, Category = "MovingPlatform")
	void OnNotifyClientStartRotat(FVector angle, float moveSpeed, int isContinuousMove);

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual FString GetEntityUName() override;///<重写GetEntityUName
	virtual bool IsEntityBoss() override;///<重写IsEntityBoss
	
};