// Fill out your copyright notice in the Description page of Project Settings.


#include "Classes/Engine/CanvasRenderTarget2D.h"
#include "CanvasRenderSeparateTriangles.generated.h"

/*
* 文件名称：CanvasRenderSeparateTriangles.h
* 功能说明：
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2017-07-07
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPolygonData
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(BlueprintReadOnly, Category = FPolygonData)
		FString MapScriptID;
	
	UPROPERTY(BlueprintReadOnly, Category = FPolygonData)
		TArray<FVector2D> Vertex;

	void clear()
	{
		MapScriptID = "";
		Vertex.Empty();
	}
};

/**
 * 
 */
UCLASS(BlueprintType)
class UCanvasRenderSeparateTriangles : public UCanvasRenderTarget2D
{
	GENERATED_UCLASS_BODY()


	UFUNCTION(BlueprintCallable, Category = CanvasRenderSeparateTriangles)
	TArray<FCanvasUVTri> TableDataToSeparateTriangles(FVector2D LevelSize, FVector2D LevelOrign, FVector2D MiniMapSize, const TArray<FVector2D>& VertexData, FLinearColor Color);

	UFUNCTION(BlueprintCallable, Category = CanvasRenderSeparateTriangles)
	FPolygonData ReadTableDataTest(const FString& RowName);
};