// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Area/WholeArea.h"
#include "SpaceCopyStoryArea.generated.h"

/**
* 文件名称：SpaceCopyStoryArea.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-10-26
*/

/**
 * 剧情副本类型(任务用)
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceCopyStoryArea : public UWholeArea
{
	GENERATED_BODY()
	
	virtual SPACE_AREA_TYPE GetType() override { return SPACE_AREA_TYPE::SPACE_AREA_TYPE_SC_STORY; }
	
	
};
