#pragma once
#include "CoreMinimal.h"
#include "Skill/Buff/BuffClientHit.h"
#include "BuffClientLoop.generated.h"


/*
* 文件名称：BuffClientLoop.h
* 功能说明：客户端周期buff
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-26
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffClientLoop :public UBuffClientHit
{
	GENERATED_BODY()
public:
	UBuffClientLoop();
	~UBuffClientLoop();

public:
	/*初始化buff数据*/
	virtual void init(FString BuffID, const FBUFF_TABLE_DATA* dictDat);

	/*效果开始*/
	virtual void doBegin(CS3Entity* receiver, UBuffDataType* buffData);

	/*上线重新加载buff*/
	virtual void doReload(CS3Entity* receiver, UBuffDataType* buffData);

	/*效果结束*/
	virtual void doEnd(CS3Entity* receiver, UBuffDataType* buffData, BUFF_END_RESON reason);

	/*周期打击*/
	virtual	void doLoopHit(CS3Entity* receiver, UBuffDataType* buffData);

	/*获得打击*/
	virtual UBuffHitDefine* getHit(FString attrName, int32 index);

	/*添加loop Timer*/
	void addBuffLoopTimer(CS3Entity* receiver, UBuffDataType* buffData);

protected:
	UPROPERTY()
	UBuffHitData* _loopHitList;
};



