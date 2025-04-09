#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/GameDeFine.h"
#include "VisibleManager.generated.h"

/*
* 文件名称：VisibleManager.h
* 功能说明：可见性管理器
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-04-18
*/ 

DECLARE_STATS_GROUP(TEXT("UVisibleManager"), STATGROUP_VisibleManager, STATCAT_Advanced);

/**
*可见性管理类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UVisibleManager : public UCS3Object
{
	GENERATED_BODY()
public:
	UVisibleManager();///<构造函数
	~UVisibleManager();///<析构函数

	static UVisibleManager* GetInstance();

	/**
	*更新Actor模型显示
	*
	*@param Actor* Actor
	*
	*return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "VisibleManager")
	void UpdateModelVisible(AActor* Actor);

	/**
	*获取Actor当前显示样式
	*
	*@param Actor* Actor
	*
	*return VISIBLE_STYLE
	*/
	UFUNCTION(BlueprintPure, Category = "VisibleManager")
	VISIBLE_STYLE GetModelVisibleStyle(AActor* Actor);

	/**
	*根据显示样式设置Actor显示
	*
	*@param AActor* Actor
	*@param VISIBLE_STYLE 显示样式
	*
	*return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "VisibleManager")
	void SetModelVisible(AActor* Actor, VISIBLE_STYLE VisibleStyle);


	class USkillInterface* GetActorSkillinterface(AActor* Actor);
private:
	/**

	*玩家未决状态显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByRoleState(AActor* Actor);

	/**

	*怪物未决状态显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByMonsterState(AActor* Actor);

	/**

	*幻兽未决状态显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByVehiclePetState(AActor* Actor);

	/**
	*标志位显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByFlag(AActor* Actor);

	/**
	*玩家标志位显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByRoleFlag(AActor* Actor);

	/**
	*剧情模式显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByStory(AActor* Actor);
	/**
	*飞行模式显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByFly(AActor* Actor);
	/**
	*死亡效果显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByDeadEffect(AActor* Actor);

	/**
	*Spellbox死亡隐藏
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByBoxDie(AActor* Actor);

	/**
	*buff隐藏规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByBUFF(AActor* Actor);

	/**
	*DropBox显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByDropBox(AActor* Actor);

	/**
	*任务可见或隐藏显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByQuest(AActor* Actor);

	/**
	*隐身效果的显示规则 (特殊 详情见JIRA CST-9111)
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByEffectHide(AActor* Actor);

	/**
	* Actor 半透明
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByBuffTransparency(AActor* Actor);

	/**
	*跳伞模式显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleBySkyDiving(AActor* Actor);

	/**

	*模型显示筛选规则
	*
	*@param TArray<VISIBLE_TYPE> 显示类型列表
	*
	*return VISIBLE_STYLE
	*/
	VISIBLE_STYLE ChoseVisibleStyleByTypes(TArray<VISIBLE_TYPE> VisibleTypes);


	/**
	* 陷阱符玉显示规则
	*
	*@param AActor* Actor
	*
	*return VISIBLE_TYPE
	*/
	VISIBLE_TYPE QueryVisibleByTrapSymbol(AActor* Actor);
	
	//static UVisibleManager* Instance;
};
