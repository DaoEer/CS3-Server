#pragma once

#include "GameData/CS3Object.h"
#include "GameData/SpaceEntityRelation/SpaceEntityRelation.h"
#include "GameData/SpaceEntityRelation/SpaceEntityRelationTableData.h"
#include "GameData/FactionRelationData.h"
#include "GameData/GameDeFine.h"
#include "SpaceEntityRelationMgr.generated.h"

/*
* 文件名称：SpaceEntityRelationMgr.h
* 功能说明：地图中entity关系查询管理类
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-06-23
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USpaceEntityRelationMgr : public UCS3Object 
{
	GENERATED_BODY()

public:
	USpaceEntityRelationMgr();
	~USpaceEntityRelationMgr();

	static USpaceEntityRelationMgr* GetInstance();

	///生成通用关系模式的关系判断实例
	void InitDefaultEntityRelationIns();

	///生成当前地图关系模式下的关系判断实例
	void InitEntityRelationIns(FString RelationMode);

	/**
	*BlueprintPure 根据阵营获取关系类型
	*
	*@param CampA	阵营A(int32)
	*@param CampB	阵营B(int32)
	*
	*@return COMBAT_RELATION 关系类型
	*/
	COMBAT_RELATION GetCampRelation(int32 CampA, int32 CampB);

	/**
	*BlueprintPure 根据势力获取关系类型
	*
	*@param CampA	势力A(int32)
	*@param CampB	势力B(int32)
	*
	*@return COMBAT_RELATION 关系类型
	*/
	COMBAT_RELATION GetFactionRelation(int32 FactionA, int32 FactionB);

	///根据entity脚本获取关系判断实例
	URelationBase* GetRelationIns(ENTITY_TYPE_EXT EntityFlagExt);

	///根据类名获取关系判断实例
	URelationBase* GetRelationInsByCls(FString RelClsStr);

public:
	UPROPERTY()
	TMap<ENTITY_TYPE_EXT, URelationBase*> DefaultModeRelationMap;

	UPROPERTY()
	TMap<ENTITY_TYPE_EXT, URelationBase*> CurrModeRelationMap;

	UPROPERTY()
	TMap<FString, URelationBase*> RelationClsMap;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString OldRelationMode = "";
/*
private:
	static USpaceEntityRelationMgr* Instance;*/

};