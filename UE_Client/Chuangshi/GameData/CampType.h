#pragma once
#include "CoreMinimal.h"
#include "CampType.generated.h"

/**
* 文件名称：CampType.h
* 功能说明：
* 文件作者：chenweilian
* 目前维护：wuxiaoou
* 创建时间：2017-04-17
*/

UENUM(BlueprintType)
enum class CAMP_TYPE_ENUM : uint8
{
	CAMP_TAOISM = 1				UMETA(DisplayName = "CAMP_TAOISM"),
	CAMP_DEMON = 2				UMETA(DisplayName = "CAMP_DEMON"),
	CAMP_NEUTRAL_ENEMY = 3		UMETA(DisplayName = "CAMP_NEUTRAL_ENEMY"),
	CAMP_NEUTRAL_NORMAL = 4		UMETA(DisplayName = "CAMP_NEUTRAL_NORMAL"),
};