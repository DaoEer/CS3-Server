// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Area/WholeArea.h"
#include "SpaceCopyNormalArea.generated.h"

/**
* 文件名称：SpaceCopyNormalArea.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2016-10-26
*/

/**
 *  通用副本类型
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceCopyNormalArea : public UWholeArea
{
	GENERATED_BODY()
	
	virtual SPACE_AREA_TYPE GetType() override { return SPACE_AREA_TYPE::SPACE_AREA_TYPE_SC_NORMAL; }
	
};