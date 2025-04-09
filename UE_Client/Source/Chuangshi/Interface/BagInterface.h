#pragma once
#include "BagInterface.generated.h"

/**
* 文件名称：BagInterface.h
* 功能说明：背包/装备/仓库界面接口
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-14
*/

UINTERFACE()
class CHUANGSHI_API UBagInterface : public UInterface
{
	GENERATED_BODY()
};

class CHUANGSHI_API IBagInterface
{
	GENERATED_BODY()
public:
	/**
	*BlueprintImplementableEvent，BlueprintCallable，更新装备
	*
	*@param Uid 物品UID
	*@param Absorder 物品位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = "BagInterface")
		void UpdateGrid(const FString& Uid, int32 Absorder);

	/**
	*BlueprintImplementableEvent，BlueprintCallable，更新物品使用CD
	*
	*@param uid 物品UID
	*@param absorder 物品位置
	*@param RemainningTime 物品CD时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = "BagInterface")
		void UpdateGridUsingCD(const FString& uid, const int32& absorder, const float& RemainningTime, const float& PersistTime);
};
