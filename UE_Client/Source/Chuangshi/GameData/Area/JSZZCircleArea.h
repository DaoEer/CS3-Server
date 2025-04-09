#pragma once
#include "GameData/Area/BaseArea.h"
#include "JSZZCircleArea.generated.h"


/**
* 文件名称：JSZZCircleArea.h
* 功能说明：金树种子检测圆形区域
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-04-19
*/

UCLASS(BlueprintType)
class  CHUANGSHI_API UJSZZCircleArea : public UBaseArea
{
	GENERATED_BODY()
public:
	UJSZZCircleArea();
	~UJSZZCircleArea();
	void InitParams(const FString SpaceScriptID, const FVector position, const float range);
	bool IsPlayerIn() override;

	void OnEnter(const FString SpaceScriptID) override;
	void OnLeave(const FString SpaceScriptID) override;

protected:
	FVector Point;///<中心点
	float Range;	///< 半径

};

