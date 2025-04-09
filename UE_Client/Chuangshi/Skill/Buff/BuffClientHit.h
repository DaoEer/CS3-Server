#pragma once
#pragma once
#include "CoreMinimal.h"
#include "Skill/Buff/BuffClientHold.h"
#include "BuffClientHit.generated.h"


/*
* 文件名称：BuffClientHold.h
* 功能说明：客户端打击buff
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-26
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffClientHit :public UBuffClientHold
{
	GENERATED_BODY()
public:
	UBuffClientHit();
	~UBuffClientHit();

public:
	/*初始化buff数据*/
	virtual void init(FString BuffID, const FBUFF_TABLE_DATA* dictDat);

	/*获得打击*/
	virtual UBuffHitDefine* getHit(FString attrName, int32 index);

	/*开始打击*/
	virtual	void doBeginHit(CS3Entity* receiver, UBuffDataType* buffData);

	/*结束打击*/
	virtual	void doEndHit(CS3Entity* receiver, UBuffDataType* buffData);
protected:
	UPROPERTY()
	UBuffHitData* _beginHitList;
	UPROPERTY()
	UBuffHitData* _endHitList;
};

