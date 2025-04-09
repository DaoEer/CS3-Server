#pragma once
#include "CoreMinimal.h"
#include "Skill/Buff/BuffClientLoop.h"
#include "BuffClientStackable.generated.h"


/*
* 文件名称：BuffClientStackable.h
* 功能说明：可叠加的持有buff
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-26
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffClientStackable :public UBuffClientLoop
{
	GENERATED_BODY()
public:
	UBuffClientStackable();
	~UBuffClientStackable();

public:
	/*初始化buff数据*/
	virtual void init(FString BuffID, const FBUFF_TABLE_DATA* dictDat);

	/*通过了免疫、替换等等等的拦截，真正要加buff*/
	virtual bool receiveSuccess(CS3Entity* caster, CS3Entity* receiver);

	/*加载持有效果*/
	virtual void addHoldEffect(CS3Entity* receiver, UBuffDataType* buffData, bool isReloadBuff = false);

	/*加载持有效果*/
	virtual void removeHoldEffect(CS3Entity* receiver, UBuffDataType* buffData);

	/*叠加*/
	virtual	void doStack(CS3Entity* receiver, UBuffDataType* buffData);

protected:
	int32 maxStackLayer = 1;
};

