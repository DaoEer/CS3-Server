#pragma once
#include "CoreMinimal.h"
#include "Skill/Buff/BuffClientHit.h"
#include "BuffClientHitBack.generated.h"


/*
* 文件名称：BuffClientHitBack.h
* 功能说明：受击击退buff（受击动作、光效、音效,击退位移）
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-26
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffClientHitBack :public UBuffClientHit
{
	GENERATED_BODY()
public:
	UBuffClientHitBack();
	~UBuffClientHitBack();
public:
	/*初始化buff数据*/
	virtual void init(FString BuffID, const FBUFF_TABLE_DATA* dictDat);

	/*用于给目标施加一个buff，所有的buff的接收都必须通过此接口，
		此接口必须判断接收者是否为realEntity*/
	virtual bool receive(CS3Entity* caster, CS3Entity* receiver);

	/*通过了免疫、替换等等等的拦截，真正要加buff*/
	virtual bool receiveSuccess(CS3Entity* caster, CS3Entity* receiver);

	/*添加检测*/
	virtual bool addBuffCheck(CS3Entity* caster, CS3Entity* receiver);

	/*效果开始*/
	virtual void doBegin(CS3Entity* receiver, UBuffDataType* buffData);

	/*效果结束*/
	virtual void doEnd(CS3Entity* receiver, UBuffDataType* buffData, BUFF_END_RESON reason);

	/*击退*/
	void doHitBack(CS3Entity* receiver, UBuffDataType* buffData);

	/*击退*/
	void endHitBack(CS3Entity* receiver, UBuffDataType* buffData);
private:
	FString _actionID = "";
	float _moveTime = 0.0f;
	float _distMin = 0.0f;
	float _distMax = 0.0f;
	float _actionBeginTime = 0.0f;
	FString _endActionID = "";
	TArray<FString> _getUpActionID;
	TArray<FString> _getUpActionBeginTime;
	float _getUpActionDelayTime = 0.0f;
	BUFF_HIT_DIRECTION _directionType = BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_CASTER_DIRECTION;
	BUFF_HIT_TYPE _hitBackType = BUFF_HIT_TYPE::BUFF_HIT_TYPE_CASTER_FORWARD;

};




