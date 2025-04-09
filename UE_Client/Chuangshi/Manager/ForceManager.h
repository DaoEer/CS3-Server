// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "Component/Role/ForceComponent.h"
#include "ForceManager.generated.h"

/*
* 文件名称：ForceManager.h
* 功能说明：力管理器，对角色添加额外的速度的管理器
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2017-10-09
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UForceManager : public UCS3Object
{
	GENERATED_BODY()
public:
	UForceManager();

	static UForceManager* GetInstance();
	//void ClearInstanceData();

public:

	/**
	* @brief 添加力
	*@param AddForceCharacter 	需要添加力的角色
	* @param _ForceSpeed 	力大小（速度）
	* @param _ForceDirection 力的方向
	*
	* @return 这个力的ID
	*/
	int32 AddForce(ACharacter* AddForceCharacter, float _ForceSpeed, FVector _ForceDirection);

	/**
	* @brief 添加力
	*@param AddForceCharacter 	需要添加力的角色
	* @param _ForceSpeed 	力大小（速度）
	* @param ForceDire 力的方向
	*
	* @return 这个力的ID
	*/
	int32 AddForce(ACharacter* AddForceCharacter, float _ForceSpeed, ELOCAL_FORCE_DIRE ForceDire);

	/**
	* @brief 添加力
	*@param AddForceCharacter 	需要添加力的角色
	* @param _ForceSpeed 	力大小（速度）
	* @param ForceDire 力的方向
	*
	* @return 这个力的ID
	*/
	UFUNCTION(BlueprintCallable, Category = "ForceManager")
	int32 AddForceUseOtherLocDire(ACharacter* AddForceCharacter, ACharacter* OtherCharacter, float _ForceSpeed, ELOCAL_FORCE_DIRE ForceDire);

	/**
	* @brief 开始某个力
	*
	* @param ForceID 	力ID
	* @param _ForceSpeed 	力大小（速度）(不填则为添加时的风速)
	* @param _ForceDirection 力的方向(不填则为添加时的方向)
	*
	* @return 是否成功开启
	*/
	bool BeginForce(int32 ForceID, float _ForceSpeed = -1.0f, FVector _ForceDirection = FVector::ZeroVector);

	/**
	* @brief 开始某个力
	*
	* @param ForceID 	力ID
	* @param _ForceSpeed 	力大小（速度）(不填则为添加时的风速)
	* @param _ForceDirection 力的方向(不填则为添加时的方向)
	*
	* @return 是否成功开启
	*/
	bool BeginForce(int32 ForceID, ELOCAL_FORCE_DIRE ForceDire, float _ForceSpeed = -1.0f);

	/**
	* @brief 暂停某个力
	* @param ForceID 这个力的ID
	*
	* @return 是否成功暂停
	*/
	UFUNCTION(BlueprintCallable, Category = "ForceManager")
	bool PauseForce(int32 ForceID);

	/**
	* @brief 停止所有力
	*
	*@param DetachForceCharacter 	需要解除力的角色
	*@param ForceArr 	力的ID数组
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "ForceManager")
	void StopForces(ACharacter* DetachForceCharacter, int32 ForceID);

	/**
	* @brief 停止所有力
	*
	*@param DetachForceCharacter 	需要解除力的角色
	*@param ForceArr 	力的ID数组
	*
	* @return 无
	*/
	void StopAllForces(ACharacter* DetachForceCharacter,TArray<int32>& ForceArr);

	UFUNCTION(BlueprintCallable, Category = "ForceManager")
	UForceComponent* GetForceById(int32 Id)
	{
		if (ForceDictionarie.Contains(Id))
		{
			return ForceDictionarie[Id];
		}

		return nullptr;
	}

	/**
	* @brief 设置某一角色额外的力百分比
	*
	*@param Character 	角色
	*@param Percentage 	百分比，力的大小表现为 Speed + Speed * Percentage
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "ForceManager")
		void SetCharacterForcePercentage(ACharacter* Character, float Percentage);

protected:
	//设置角色力的百分比
	void SetForcePercentageByCharacter(ACharacter* Character);

private:
	UPROPERTY()
	TMap<int32, UForceComponent*> ForceDictionarie;//力的字典容器
	int32 ForceCount;

	TMap<ACharacter*, float> ForcePercentageMap;///<角色身上力的百分比
	//static UForceManager* Instance;
};
