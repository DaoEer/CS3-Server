// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Level/CS3LevelScriptActor.h"
#include "GameData/CharacterData.h"
#include "GameData/RoleInfo.h"
#include "NewCreateRoleLevel.generated.h"

/**
 * 
 */
class ALoginCharacter;

UCLASS()
class CHUANGSHI_API ANewCreateRoleLevel : public ACS3LevelScriptActor
{
	GENERATED_BODY()
public:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void CreateDynamicRes() override;
	virtual void OnCreateModelFinished() override;
	//virtual void OnLoadLevelFinished() override;
	void ChangeCreateRole(ROLE_PROFESSION_ENUM Job, ROLE_GENDER_ENUM Gender);

	void CloseLoadingWidget();///关闭加载进度条
	ALoginCharacter* SPawnBPAccount(FROLEINFO RoleInfo);

private:

	UFUNCTION()
		void LoadBlockStreamLevelCreateRoleFinished();

	void OpenSelectRole();

	//获取选中的索引FRoleCreateUIData的rowName[通过职业+性别+阵营转换过来]
	int32 GetSelectIndex();

public:
	//四个职业角色模型列表
	UPROPERTY(BlueprintReadOnly, Category = "ANewCreateRoleLevel")
		TArray<AActor*> ProfessionActors;

	//选中的职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ANewCreateRoleLevel")
		ROLE_PROFESSION_ENUM SelectRoleProfessionID = ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_ZHAN_SHI;

	//选中的性别
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ANewCreateRoleLevel")
		ROLE_GENDER_ENUM SelectGender = ROLE_GENDER_ENUM::ROLE_GENDER_TYPE_MALE;

private:
	int32 LoadLevelIndex = 0;//加载四个关卡完成记录
	int32 CreateFinishCount = 0;//加载四个职业完成记录
	
	UPROPERTY()
		TMap<int32, AActor *> CreateRoleCameras;//key 阵营+职业

};
