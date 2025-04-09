// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "ShapeManager.generated.h"

/*
* 文件名称：ShapeManager.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

class UBaseShape;

DECLARE_DELEGATE(FShapeDelegate);
DECLARE_DYNAMIC_DELEGATE(FShapeDynamicDelegate);


UENUM(BlueprintType)
enum class SHAPE_TYPE: uint8
{
	CYLINDER = 1		UMETA(DisplayName = "CYLINDER"),	///<圆柱		XY的最小值为半径，Z为高度
	BOX = 2				UMETA(DisplayName = "BOX"),			///<盒子		XYZ为长宽高
	SHPERE = 3			UMETA(DisplayName = "SHPERE"),		///<球			XYZ的最小值为半径
	SECTOR = 4			UMETA(DisplayName = "SECTOR"),		///<扇形		X为半径，Y为角度，Z为高度
	CAPSULE = 5			UMETA(DisplayName = "CAPSULE"),		///<胶囊体		XY的最小值为半径，Z为半高
};


UCLASS(BlueprintType)
class CHUANGSHI_API UShapeManager : public UCS3Object
{
	GENERATED_BODY()

public:
	
	UShapeManager();

	/**
	 * 创建Shape
	 *
	 * @param OwnerActor	 拥有体积的Actor	
	 * @param Type			 体积类型
	 * @param Bounds		 体积边界
	 * @param BeginOverlap	 开始重叠事件
	 * @param EndOverlap	 结束重叠事件
	 *
	 *@return 返回体积对象
	 */
	UFUNCTION(BlueprintCallable)
	UBaseShape* CreateShapeBindEvent(AActor* OwnerActor, SHAPE_TYPE Type, FVector Bounds, FShapeDynamicDelegate BeginOverlap, FShapeDynamicDelegate EndOverlap);


	/**
	 * 创建Shape
	 *
	 * @param OwnerActor		 拥有体积的Actor
	 * @param Object			 this
	 * @param Type				 体积类型
	 * @param Bounds			 体积边界
	 * @param BeginOverlapName	 开始重叠函数名称
	 * @param EndOverlapName	 结束重叠函数名称
	 *
	 *@return 返回体积对象
	 */
	UFUNCTION(BlueprintCallable)
	UBaseShape* CreateShapeBindFunction(AActor* OwnerActor, UObject* Object, SHAPE_TYPE Type, FVector Bounds, FString BeginOverlapName, FString EndOverlapName);

	/**
	 * 创建Shape
	 *
	 * @param OwnerActor		 拥有体积的Actor
	 * @param Object			 this
	 * @param Type				 体积类型
	 * @param Bounds			 体积边界
	 * @param BeginOverlap		 开始重叠函数
	 * @param EndOverlap		 结束重叠函数
	 *
	 *@return 返回体积对象
	 */
	template<class UserClass>
	UBaseShape* CreateShape(AActor* OwnerActor, UserClass* Object, SHAPE_TYPE Type, FVector Bounds, typename FShapeDelegate::TUObjectMethodDelegate<UserClass>::FMethodPtr BeginOverlap, typename FShapeDelegate::TUObjectMethodDelegate<UserClass>::FMethodPtr EndOverlap)
	{
		return InternalCreateShapeByDelegate(OwnerActor, Type, Bounds, FShapeDelegate::CreateUObject(Object, BeginOverlap), FShapeDelegate::CreateUObject(Object, EndOverlap));
	}
	
	///获取实例
	static UShapeManager* GetInstance();

private:
	///创建Shape,内部调用
	UBaseShape* InternalCreateShape(AActor* OwnerActor, SHAPE_TYPE Type, FVector Bounds, FShapeDynamicDelegate BeginOverlapDelegate, FShapeDynamicDelegate EndOverlapDelegate);
	UBaseShape* InternalCreateShapeByDelegate(AActor* OwnerActor, SHAPE_TYPE Type, FVector Bounds, FShapeDelegate BeginOverlapDelegate, FShapeDelegate EndOverlapDelegate);
public:
	///引用所有的Shape，防止被GC
	UPROPERTY()
	TArray<UBaseShape*> ShapeList;

private:
	///所有形状的map
	TMap<SHAPE_TYPE, UClass*> TypeMapping;

};
