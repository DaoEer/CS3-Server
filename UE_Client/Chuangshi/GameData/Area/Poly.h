// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "RectArea.h"

/**
* 文件名称：Polygon.h
* 功能说明：多边形
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2016-11-25
*/

/**
* 多边形类
*/
class CHUANGSHI_API Poly
{
public:
	Poly();
	~Poly();

	/**
	*更新多边形数据
	*
	*@param Points 多边形数据
	*
	*@return 无
	*/
	void UpdatePoints(TArray<FVector2D>& Points);

	/**
	*判断参数位置是否在区域范围内
	*
	*@param Position 位置
	*
	*@return bool 参数位置在区域范围内返回true，否则为false
	*/
	bool IsPointIn(FVector& Position);

	/**
	*判断参数位置与多边形之间距离是否小于一定距离
	*
	*@param Position 位置
	*@param Distance 距离
	*
	*@return bool 参数位置与区域在范围内返回true，否则为false
	*/
	bool IsCloseTo(FVector& Position, float Distance);

private:
	TSharedPtr<RectArea> RectPtr;///<外接矩形
	TArray<FVector2D> PolyPoints;///<多边形坐标点
};