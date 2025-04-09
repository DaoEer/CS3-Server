// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

/**
* 文件名称：Rect.h
* 功能说明：矩形
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2016/11/25
*/

/**
* 矩形类
*/
class CHUANGSHI_API RectArea
{
public:
	RectArea();
	~RectArea();

	/**
	*更新矩形最小坐标和最大坐标
	*
	*@param MinPoint 最小点坐标
	*@param MaxPoint 最大点坐标
	*
	*@return 无
	*/
	void UpdatePoint(FVector2D& MinPoint, FVector2D& MaxPoint);

	/**
	*判断参数位置是否在矩形范围内
	*
	*@param Position 位置
	*
	*@return bool 参数位置在矩形范围内返回true，否则为false
	*/
	bool IsPointIn(FVector& Position);

private:
	FVector2D MinPos;///<最小点坐标
	FVector2D MaxPos;///<最大点坐标
};
