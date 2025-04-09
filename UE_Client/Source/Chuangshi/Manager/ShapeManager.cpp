// Fill out your copyright notice in the Description page of Project Settings.

#include "ShapeManager.h"
// 数据类型
#include "GameData/Shape/BaseShape.h"
#include "GameData/Shape/Box.h"
#include "GameData/Shape/Capsule.h"
#include "GameData/Shape/Sphere.h"
#include "GameData/Shape/Sector.h"
#include "GameData/Shape/Cylinder.h"
// CS3类型
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include"Chuangshi.h"


UShapeManager::UShapeManager()
{
	// 初始化表
	TypeMapping.Add(SHAPE_TYPE::CYLINDER, UShapeCylinder::StaticClass());
	TypeMapping.Add(SHAPE_TYPE::BOX, UShapeBox::StaticClass());
	TypeMapping.Add(SHAPE_TYPE::SHPERE, UShapeSphere::StaticClass());
	TypeMapping.Add(SHAPE_TYPE::SECTOR, UShapeSector::StaticClass());
	TypeMapping.Add(SHAPE_TYPE::CAPSULE, UShpaeCapsule::StaticClass());
}

UShapeManager* UShapeManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UShapeManager>();
}

UBaseShape* UShapeManager::CreateShapeBindEvent(AActor* OwnerActor, SHAPE_TYPE Type, FVector Bounds, FShapeDynamicDelegate BeginOverlap, FShapeDynamicDelegate  EndOverlap)
{
	return InternalCreateShape(OwnerActor, Type, Bounds, BeginOverlap, EndOverlap);
}

UBaseShape* UShapeManager::CreateShapeBindFunction(AActor* OwnerActor, UObject* Object, SHAPE_TYPE Type, FVector Bounds, FString BeginOverlapName, FString EndOverlapName)
{
	FName const BeginName(*BeginOverlapName);
	FShapeDynamicDelegate BeginOverlapDelegate;
	BeginOverlapDelegate.BindUFunction(Object, BeginName);


	FName const EndName(*EndOverlapName);
	FShapeDynamicDelegate EndOverlapDelegate;
	EndOverlapDelegate.BindUFunction(Object, EndName);
		
	return InternalCreateShape(OwnerActor, Type, Bounds, BeginOverlapDelegate, EndOverlapDelegate);
}

UBaseShape* UShapeManager::InternalCreateShape(AActor* OwnerActor, SHAPE_TYPE Type, FVector Bounds, FShapeDynamicDelegate BeginOverlapDelegate, FShapeDynamicDelegate EndOverlapDelegate)
{
	if (TypeMapping.Contains(Type))
	{
		UBaseShape* BaseShape = Cast<UBaseShape>(StaticConstructObject_Internal(TypeMapping[Type]));

		BaseShape->BeginOverlap.Add(BeginOverlapDelegate);
		BaseShape->EndOverlap.Add(EndOverlapDelegate);

		BaseShape->Owner = OwnerActor;
		BaseShape->UpdateBounds(Bounds);
		BaseShape->EnableTick();

		ShapeList.Add(BaseShape);
		return BaseShape;
	}
	// 传入的类型错误，返回值为空，请检查传入的类型
	ensureMsgf(false, TEXT("Create failed, please check TypeMapping has Contains : %d"), (int32)Type);
	return nullptr;
}

UBaseShape* UShapeManager::InternalCreateShapeByDelegate(AActor* OwnerActor, SHAPE_TYPE Type, FVector Bounds, FShapeDelegate BeginOverlapDelegate, FShapeDelegate EndOverlapDelegate)
{
	if (TypeMapping.Contains(Type))
	{
		UBaseShape* BaseShape = Cast<UBaseShape>(StaticConstructObject_Internal(TypeMapping[Type]));

		BaseShape->BeginOverlapSingle = BeginOverlapDelegate;
		BaseShape->EndOverlapSingle = EndOverlapDelegate;

		BaseShape->Owner = OwnerActor;
		BaseShape->UpdateBounds(Bounds);
		BaseShape->EnableTick();

		ShapeList.Add(BaseShape);
		return BaseShape;
	}
	// 传入的类型错误，返回值为空，请检查传入的类型
	ensureMsgf(false, TEXT("Create failed, please check TypeMapping has Contains : %d"), (int32)Type);
	return nullptr;
}

