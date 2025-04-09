#pragma once
#include "AvatarFilterActorComponent.h"
#include "RoleFilterActorComponent.generated.h"

/*
* 文件名称：RoleFilterActorComponent.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：huting
* 创建时间：2017-07-20
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleFilterActorComponent : public UAvatarFilterActorComponent
{
	GENERATED_BODY()
		typedef UAvatarFilterActorComponent Supper;
public:
	//virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void Pos(const int32 vehicleID, const FVector& position, const FVector& direction, const FVector& velocity) override;
};

