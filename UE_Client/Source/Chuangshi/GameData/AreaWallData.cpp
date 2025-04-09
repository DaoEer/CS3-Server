
#include "AreaWallData.h"
#include "CoreMinimal.h"
#include "GameDefine.h"
#include "BossArea.h"
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"
#include "Manager/MapManager.h"
#include "AreaMap.h"
#include"Chuangshi.h"


UAreaWallData* UAreaWallData::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UAreaWallData>();
}

bool UAreaWallData::SetAreaWallData(const FString RowNumber, AREA_LIGHT_WALL_TYPE_ENUM CurrentWallType)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FLIGHT_WALL_DATA* LightWallData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LIGHT_WALL_DATA)->GetRow<FLIGHT_WALL_DATA>(RowNumber);

	switch (CurrentWallType)
	{
	case AREA_LIGHT_WALL_TYPE_ENUM::AreaLightWall:
		{
			//获得位面光墙数据
			TArray<FVector2D> Polygon = UUECS3GameInstance::Instance->MapManager->GetPlanePolygon();
			if (Polygon.Num())
			{
				this->WorldLocation = UGolbalBPFunctionLibrary::ConvertFVector2DToFVector(Polygon);
				this->IsValidPosZ = false;
			}
			else
			{
				this->WorldLocation.Empty();
				return false;
			}
		}
			break;
	case AREA_LIGHT_WALL_TYPE_ENUM::BossLightWall:
	case AREA_LIGHT_WALL_TYPE_ENUM::NormalAreaWall:
		{
			//获得Boss光墙数据
			const FBOSS_AREA_DATA* BossAreaData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BOSS_AREA)->GetRow<FBOSS_AREA_DATA>(RowNumber);
			if (BossAreaData)
			{
				this->WorldLocation = BossAreaData->Polygon;
				this->IsValidPosZ = true;
			}
			else
			{
				this->WorldLocation.Empty();
				return false;
			}
		}
		break;
	case AREA_LIGHT_WALL_TYPE_ENUM::TerrainLightWall:
		{
			//获取阻挡光墙数据
			const FAREA_TERRAINCLASSIFICATION_DATA* TerrainData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FAREA_TERRAINCLASSIFICATION_DATA)->GetRow<FAREA_TERRAINCLASSIFICATION_DATA>(RowNumber);
			if (TerrainData)
			{
				this->WorldLocation = TerrainData->Position;
				this->IsValidPosZ = true;
			}
			else
			{
				this->WorldLocation.Empty();
				return false;
			}
		}
		break;
	}

	this->WallType = CurrentWallType;
	
	if (LightWallData)
	{
		this->ValidHeight = LightWallData->ValidHeight;
		this->EqualLength = LightWallData->EqualLength;
		this->Object = LightWallData->Object;
		this->UpLength = LightWallData->UpLength;
		this->DownLength = LightWallData->DownLength;
		this->HeightCorrection = LightWallData->HeightCorrection;
		this->bIsClose = LightWallData->bIsClose;
	}
	else
	{
		LightWallData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LIGHT_WALL_DATA)->GetRow<FLIGHT_WALL_DATA>(INT_TO_FSTRING((int)this->WallType));
		if (!LightWallData)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UAreaWallData::SetAreaWallData : LightWallData!"));
			return false;
		}
		this->ValidHeight = LightWallData->ValidHeight;
		this->EqualLength = LightWallData->EqualLength;
		this->Object = LightWallData->Object;
		this->UpLength = LightWallData->UpLength;
		this->DownLength = LightWallData->DownLength;
		this->HeightCorrection = LightWallData->HeightCorrection;
		this->bIsClose = LightWallData->bIsClose;
	}
	return true;
}