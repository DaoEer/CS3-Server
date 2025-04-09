#pragma once

/*
* 文件名称：EffectStateBase.h
* 功能说明：entity效果状态基类
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-06-16
*/

class AActor;

class EffectStateBase
{
public:
	EffectStateBase();
	virtual ~EffectStateBase();

	virtual void Add(AActor* _Actor);///< 添加某效果
	virtual void Del(AActor* _Actor);///< 失去某效果
};

