// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "MessageID.generated.h"

/**
* 文件名称：MessageID.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-02-06
*/

/**
 * 全局性MessageID类
 */
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UMessageID : public UCS3Object
{
	GENERATED_BODY()
public:
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEM_USE_GO_ON_MSG = 592;///<物品能正常使用
	
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEM_NOT_EXIST_MSG = 593;///<物品不存在
	
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEM_USE_LV_LESS_MSG = 596;///<你的等级太低，不能使用此物品
	
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEM_USE_CLASS_NOTMATCH = 603;///<你的职业不适合使用此物品
	
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEMBAG_LOCKED = 604;///<背包锁了，暂不能卸载装备
	
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEM_LIMITDESTORY = 606;///<此物品不允许销毁
	
	UPROPERTY(BlueprintReadOnly, Category = "Item")
		int32 ITEM_INCD = 607;///<此物品在CD中，请稍候
	
};
