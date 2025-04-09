// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "CS3Base/InterfaceDef.h"
#include "RoleExpData.generated.h"


USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleExpData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleExpData")
		int32 level = 0;
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleExpData")
		int32 maxExp = 0;

};