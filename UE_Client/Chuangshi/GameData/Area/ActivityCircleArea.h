
#pragma once

#include "GameData/Area/BaseArea.h"
#include "UObject/NoExportTypes.h"
#include "ActivityCircleArea.generated.h"


/**
* 文件名称：ActivityCircleArea.h
* 功能说明：大地图活动玩法时，检测圆形区域
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-12-11
*/

UCLASS(BlueprintType)
class  CHUANGSHI_API UActivityCircleArea : public UBaseArea
{
	GENERATED_BODY()
public:
	UActivityCircleArea();
	~UActivityCircleArea();
	void InitParams(const FString SpaceScriptID, const FVector position, const float range, const int32 Index);
	bool IsPlayerIn() override;

	void OnEnter(const FString SpaceScriptID) override;
	void OnLeave(const FString SpaceScriptID) override;


public:
	int32 AreaIndex;///<用于标识是哪个区域

protected:
	FVector Point;///<中心点
	float Range;	///< 半径
	
};