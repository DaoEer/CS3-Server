// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/ModifyFaceData.h"
#include "CfgManager.h"
#include "Actor/PinchFace/ModifyFaceCharacter.h"
#include "ModifyFaceManager.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UModifyFaceManager : public UCS3Object
{

	GENERATED_BODY()
	
public:

	UModifyFaceManager();

	static UModifyFaceManager* GetInstance();

	// 设置骨骼数组
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void SetBoneRef(AGameCharacter* Actor);

	// 修改骨骼的 Transform 
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void SetBoneTrans(AGameCharacter* GameActor, FName BoneName, bool bIsSymBone, FTransform BoneTrans, bool IsMouse = true);

	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void SetTouchBone(int32 Index, int32 ModifyType = 0/*EModifyType Type = EModifyType::Part_Face*/);

	// 限制骨骼的可调节范围
	void LimitBoneTrans(FMODIFY_FACE_DATA* Bones, int32 ModifyType);

	// 获取镜像骨骼 Transform
	UFUNCTION(BlueprintPure, Category = "ModifyFace|Fucntion")
	FTransform SymBoneTrans(FTransform BoneTrans);

	//获取当前选中根骨骼名字
	UFUNCTION(BlueprintPure, Category = "ModifyFace|Fucntion")
		FName GetCurrentBoneName() const;

	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void SetCurrentBone();

	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void SetModifyData();

	UFUNCTION(BlueprintPure, Category = "ModifyFace|Function")
		TArray<FMODIFY_FACE_DATA>& GetBoneReference(int32 ModifyType = 0/*EModifyType Type = EModifyType::Part_Face*/);

	///获取当前触摸骨骼名
	UFUNCTION(BlueprintPure, Category = "ModifyFace|Fucntion")
		FName GetTouchBoneName() const;
	
	//保存捏脸数据
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFaceActor")
		FString SaveFileData(FString name);
	//导入捏脸数据
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFaceActor")
		FString LoadFileData();
	//当前状态
	UFUNCTION(BlueprintPure, Category = "ModifyFace|Function")
		bool GetFinishState();
	//重置面部数据
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void ResetFileData(AGameCharacter* GameActor);

	//获取脸部数据文件名
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		TArray<FString> GetFaceFileName();

	//获取脸部数据文件名
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		AModifyFaceCharacter* GetModifyFaceActor();

	//设置模型的脸部类型
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|Function")
		void SetModelFaceStyle(AGameCharacter* Target , FFACE_STYLE_DATA faceStyleData);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace|ModifyFaceCharacter")
		UConfigTable* BoneDataTable;//面部骨骼数据表

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace|ModifyFaceCharacter")
		UConfigTable* BoneLimitTable;//面部骨骼信息表

	void SetActorFaceData(AGameCharacter* Target, TArray<FMODIFY_FACE_DATA> ModifyFaceDatas, FFACE_STYLE_DATA FaceStyleDatas);

	bool SerialzeData(FString DataPath);

	bool DeserialzeData(FString DataPath);

private:
	TArray<FMODIFY_FACE_DATA> FaceBoneRef;
	TArray<FMODIFY_FACE_DATA> BodyBoneRef;//身体数据暂未启用
	TArray<FBONE_FACE_LIMIT> BoneLimitRef;

	bool bIsGetBone = false;
	FMODIFY_FACE_DATA* TouchBone;
	FMODIFY_FACE_DATA* CurrentBone;
	FMODIFY_FACE_DATA* SymBone;
	
};
