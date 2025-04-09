// Fill out your copyright notice in the Description page of Project Settings.
#pragma once

#include "PinchFaceAnimInstance.h"


TArray<FBoneLimit>& UPinchFaceAnimInstance::GetLimitArrayByType(EBodyPartType type)
{
	if (type == EBodyPartType::Part_Face)
	{
		return FaceBoneLimitArray;
	}
	else
	{
		return BodyBoneLimitArray;
	}
}



void UPinchFaceAnimInstance::ResetAllBones(EBodyPartType faceOrBody)
{
	TArray<FBoneStruct>& boneArray = GetArrayByType(faceOrBody);

	switch (faceOrBody)
	{
	case EBodyPartType::Part_Face:
		for (auto& bone : boneArray)
		{
			FTransform s;
			bone.transform = s;
		}
		break;

	case EBodyPartType::Part_Body:
		for (auto& bone : boneArray)
		{
			FTransform s;
			s.SetRotation(bone.transform.GetRotation());
			bone.transform = s;
		}
		break;
	default:
		break;
	}
}

void UPinchFaceAnimInstance::ResetBone(FName boneName, EBodyPartType faceOrBody)
{
	TArray<FBoneStruct>& boneArray = GetArrayByType(faceOrBody);
	FBoneStruct* pBone = boneArray.FindByPredicate([boneName](const FBoneStruct& bone){ return bone.boneName == boneName; });
	if (pBone)
	{
		switch (faceOrBody)
		{
		case EBodyPartType::Part_Face:
		{
			pBone->transform = FTransform();
			break;
		}


		case EBodyPartType::Part_Body:
		{
			FTransform s;
			s.SetRotation((pBone->transform.GetRotation()));
			pBone->transform = s;
			break;
		}

		case EBodyPartType::Part_Pose:
		{
			FTransform s = pBone->transform;
			s.SetRotation(FQuat().Identity);
			pBone->transform = s;
			break;
		}
		}
	}
}



FTransform UPinchFaceAnimInstance::GetSynBoneTrans(FTransform inTrans, EBodyPartType faceOrBody)
{
	FTransform out = inTrans;

	FVector loc = inTrans.GetLocation();
	loc.X = -loc.X;
	out.SetTranslation(loc);

	FRotator rot = inTrans.Rotator();
	rot.Yaw = -rot.Yaw;
	out.SetRotation(FQuat(rot));

	return out;
}

void UPinchFaceAnimInstance::SetLimitBoneArray(TArray<FBoneLimit> limitArray, EBodyPartType faceOrBody)
{
	TArray<FBoneLimit>& limitArr = GetLimitArrayByType(faceOrBody);
	limitArr.Empty();
	for (auto& limit : limitArray)
	{
		limitArr.Add(limit);
	}
}


void UPinchFaceAnimInstance::InitBoneArray(TArray<FBoneStruct> boneArray, EBodyPartType faceOrBody)
{
	//父类直接设置的骨骼的变换，子类需验证骨骼是否有效
	TArray<FBoneStruct>& RegBoneArray = GetArrayByType(faceOrBody);
	for (const FBoneStruct& bone : boneArray)
	{
		FBoneStruct* searchBone = RegBoneArray.FindByPredicate([&bone](const FBoneStruct& iterBone) { return iterBone.boneName == bone.boneName; });
		if (nullptr != searchBone)//骨骼有注册
		{
			searchBone->transform = bone.transform;
			searchBone->alpha = bone.alpha;
		}
	}
}

void UPinchFaceAnimInstance::AddModifyBone(FName boneName, EBodyPartType faceOrBody)
{
	TArray<FBoneStruct>& boneArray = GetArrayByType(faceOrBody);
	FBoneStruct* findBone = boneArray.FindByPredicate([&boneName](FBoneStruct& a) {return a.boneName == boneName; });
	if (!findBone)
	{
		FBoneStruct f;
		f.boneName = boneName;
		f.boneIndex = GetSkelMeshComponent()->GetBoneIndex(boneName);
		if (f.boneIndex > 0)
		{
			boneArray.Add(f);
		}
	}
}


void UPinchFaceAnimInstance::SetBoneTransform(FTransform trans, FName boneName, EBodyPartType faceOrBody)
{
	TArray<FBoneStruct>& boneArray = GetArrayByType(faceOrBody);
	FBoneStruct* bone = boneArray.FindByPredicate([&boneName](FBoneStruct& a) {return a.boneName == boneName; });
	if(bone)
	{
		bone->transform.SetLocation(bone->transform.GetLocation() + trans.GetLocation());
		bone->transform.SetRotation(FQuat(bone->transform.Rotator() + trans.Rotator()));
		bone->transform.SetScale3D(bone->transform.GetScale3D() * trans.GetScale3D());
		LimitBone(*bone, faceOrBody);
		
	}
}

void UPinchFaceAnimInstance::SetBonePresentValue(FName boneName, EBodyPartType faceOrBody, EBoneTransType transType, float value)
{
	TArray<FBoneStruct>& boneArray = GetArrayByType(faceOrBody);
	FBoneStruct* bone = boneArray.FindByPredicate([&boneName](FBoneStruct& a) {return a.boneName == boneName; });
	if (bone)
	{
		TArray<FBoneLimit>& boneLimitArray = GetLimitArrayByType(faceOrBody);

		FBoneLimit* limit = boneLimitArray.FindByPredicate([&boneName](FBoneLimit& a) {return a.boneName == boneName; });

		bool doLocal = true;
		bool doRot = true;
		bool doScalc = true;
		FVector minLocaltion;
		FVector maxLocaltion;
		FRotator minRotation;
		FRotator maxRotation;
		FVector minScalction;
		FVector maxScalction;
		if (limit)
		{
			doLocal = limit->doTranslation;
			doRot = limit->doRotation;
			doScalc = limit->doScaling;
			minLocaltion = limit->MinTransform.GetLocation();
			maxLocaltion = limit->MaxTransform.GetLocation();
			minRotation = limit->MinTransform.Rotator();
			maxRotation = limit->MaxTransform.Rotator();
			minScalction = limit->MinTransform.GetScale3D();
			maxScalction = limit->MaxTransform.GetScale3D();
		}
		else
		{
			minLocaltion = FVector(minLoc, minLoc, minLoc);
			maxLocaltion = FVector(maxLoc, maxLoc, maxLoc);
			minRotation = FRotator(minRot, minRot, minRot);
			maxRotation = FRotator(maxRot, maxRot, maxRot);
			minScalction = FVector(minScl, minScl, minScl);
			maxScalction = FVector(maxScl, maxScl, maxScl);
		}

		switch (transType)
		{
		case EBoneTransType::POS_X:
		{
			if (doLocal)
			{
				auto location = bone->transform.GetLocation();
				location.X = FMath::Lerp(minLocaltion.X, maxLocaltion.X, value);
				bone->transform.SetLocation(location);
			}
			
		}
		break;
		case EBoneTransType::POS_Y:
		{
			if (doLocal)
			{
				auto location = bone->transform.GetLocation();
				location.Y = FMath::Lerp(minLocaltion.Y, maxLocaltion.Y, value);
				bone->transform.SetLocation(location);
			}
		}
		break;
		case EBoneTransType::POS_Z:
		{
			if (doLocal)
			{
				auto location = bone->transform.GetLocation();
				location.Z = FMath::Lerp(minLocaltion.Z, maxLocaltion.Z, value);
				bone->transform.SetLocation(location);
			}
		}
		break;
		case EBoneTransType::ROT_X:
		{
			if (doRot)
			{
				auto rotator = bone->transform.Rotator();
				rotator.Yaw = FMath::Lerp(minRotation.Yaw, maxRotation.Yaw, value);
				bone->transform.SetRotation(FQuat(rotator));
			}
		}
		break;
		case EBoneTransType::ROT_Y:
		{
			if (doRot)
			{
				auto rotator = bone->transform.Rotator();
				rotator.Pitch = FMath::Lerp(minRotation.Pitch, maxRotation.Pitch, value);
				bone->transform.SetRotation(FQuat(rotator));
			}
		}
		break;
		case EBoneTransType::ROT_Z:
		{
			if (doRot)
			{
				auto rotator = bone->transform.Rotator();
				rotator.Roll = FMath::Lerp(minRotation.Roll, maxRotation.Roll, value);
				bone->transform.SetRotation(FQuat(rotator));
			}
		}
		break;
		case EBoneTransType::SCALC_X:
		{
			if (doScalc)
			{
				auto scalc = bone->transform.GetScale3D();
				scalc.X = FMath::Lerp(minScalction.X, maxScalction.X, value);
				bone->transform.SetScale3D(scalc);
			}
		}
		break;
		case EBoneTransType::SCALC_Y:
		{
			if (doScalc)
			{
				auto scalc = bone->transform.GetScale3D();
				scalc.Y = FMath::Lerp(minScalction.Y, maxScalction.Y, value);
				bone->transform.SetScale3D(scalc);
			}
		}
		break;
		case EBoneTransType::SCALC_Z:
		{
			if (doScalc)
			{
				auto scalc = bone->transform.GetScale3D();
				scalc.Z = FMath::Lerp(minScalction.Z, maxScalction.Z, value);
				bone->transform.SetScale3D(scalc);
			}
		}
		break;
		default:
			break;
		}
	}
}



void UPinchFaceAnimInstance::GetBoneTransformInfo(EBodyPartType faceOrBody, FName boneName, bool& doLocal, FBoneOffsetStruct3& Local, bool& doRot, FBoneOffsetStruct3& Rot, bool& doScalc, FBoneOffsetStruct3& Scalc)
{
	TArray<FBoneStruct>& boneArray = GetArrayByType(faceOrBody);
	FBoneStruct* resultBone = boneArray.FindByPredicate([&boneName](const FBoneStruct& bone) { return bone.boneName == boneName; });
	if (resultBone)
	{
		FVector CurPos = resultBone->transform.GetLocation();
		FRotator CurRot = resultBone->transform.Rotator();
		FVector CurScl = resultBone->transform.GetScale3D();

		TArray<FBoneLimit>& boneLimitArray = GetLimitArrayByType(faceOrBody);
		FBoneLimit* limit = boneLimitArray.FindByPredicate([&boneName](FBoneLimit& a) {return a.boneName == boneName; });

		FVector minLocaltion;
		FVector maxLocaltion;
		FRotator minRotation;
		FRotator maxRotation;
		FVector minScalction;
		FVector maxScalction;
		if (limit)
		{
			doLocal = limit->doTranslation;
			doRot = limit->doRotation;
			doScalc = limit->doScaling;
			//从limit取出上下限
			minLocaltion = limit->MinTransform.GetLocation();
			maxLocaltion = limit->MaxTransform.GetLocation();
			minRotation = limit->MinTransform.Rotator();
			maxRotation = limit->MaxTransform.Rotator();
			minScalction = limit->MinTransform.GetScale3D();
			maxScalction = limit->MaxTransform.GetScale3D();
		}
		else
		{
			doLocal = true;
			doRot = true;
			doScalc = true;
			//使用默认上下限
			minLocaltion = FVector(minLoc, minLoc, minLoc);
			maxLocaltion = FVector(maxLoc, maxLoc, maxLoc);
			minRotation = FRotator(minRot, minRot, minRot);
			maxRotation = FRotator(maxRot, maxRot, maxRot);
			minScalction = FVector(minScl, minScl, minScl);
			maxScalction = FVector(maxScl, maxScl, maxScl);
		}
		//localtion
		if (doLocal)
		{
			Local.X.MinValue = minLocaltion.X;
			Local.X.MaxValue = maxLocaltion.X;
			Local.X.CurValue = CurPos.X;

			Local.Y.MinValue = minLocaltion.Y;
			Local.Y.MaxValue = maxLocaltion.Y;
			Local.Y.CurValue = CurPos.Y;

			Local.Z.MinValue = minLocaltion.Z;
			Local.Z.MaxValue = maxLocaltion.Z;
			Local.Z.CurValue = CurPos.Z;
		}
		//rotation

		//从limit取出上下限
		if (doRot)
		{
			Rot.X.MinValue = minRotation.Yaw;
			Rot.X.MaxValue = maxRotation.Yaw;
			Rot.X.CurValue = CurRot.Yaw;

			Rot.Y.MinValue = minRotation.Pitch;
			Rot.Y.MaxValue = maxRotation.Pitch;
			Rot.Y.CurValue = CurRot.Pitch;

			Rot.Z.MinValue = minRotation.Roll;
			Rot.Z.MaxValue = maxRotation.Roll;
			Rot.Z.CurValue = CurRot.Roll;
		}
		//scalc

		//从limit取出上下限
		if (doScalc)
		{
			Scalc.X.MinValue = minScalction.X;
			Scalc.X.MaxValue = maxScalction.X;
			Scalc.X.CurValue = CurScl.X;

			Scalc.Y.MinValue = minScalction.Y;
			Scalc.Y.MaxValue = maxScalction.Y;
			Scalc.Y.CurValue = CurScl.Y;

			Scalc.Z.MinValue = minScalction.Z;
			Scalc.Z.MaxValue = maxScalction.Z;
			Scalc.Z.CurValue = CurScl.Z;
		}
	}
}


void UPinchFaceAnimInstance::LimitBone(FBoneStruct& bone, EBodyPartType type)
{
	TArray<FBoneLimit>& limitArray = GetLimitArrayByType(type);
	FBoneLimit* limit = limitArray.FindByPredicate([&bone](const FBoneLimit& limit) { return bone.boneName == limit.boneName;  });

	FVector loc = bone.transform.GetLocation();
	FRotator rot = bone.transform.Rotator();
	FVector scl = bone.transform.GetScale3D();

	bool doLocal = true;
	bool doRot = true;
	bool doScalc = true;
	FVector minLocaltion;
	FVector maxLocaltion;
	FRotator minRotation;
	FRotator maxRotation;
	FVector minScalction;
	FVector maxScalction;

	if (limit)
	{
		doLocal = limit->doTranslation;
		doRot = limit->doRotation;
		doScalc = limit->doScaling;
		minLocaltion = limit->MinTransform.GetLocation();
		maxLocaltion = limit->MaxTransform.GetLocation();
		minRotation = limit->MinTransform.Rotator();
		maxRotation = limit->MaxTransform.Rotator();
		minScalction = limit->MinTransform.GetScale3D();
		maxScalction = limit->MaxTransform.GetScale3D();
	}
	else
	{
		//没有设置限制，使用默认限制
		minLocaltion = FVector(minLoc, minLoc, minLoc);
		maxLocaltion = FVector(maxLoc, maxLoc, maxLoc);
		minRotation = FRotator(minRot, minRot, minRot);
		maxRotation = FRotator(maxRot, maxRot, maxRot);
		minScalction = FVector(minScl, minScl, minScl);
		maxScalction = FVector(maxScl, maxScl, maxScl);
	}

	//应用限制 
	if (doLocal)
	{
		loc.X = FMath::Clamp(loc.X, minLocaltion.X, maxLocaltion.X);
		loc.Y = FMath::Clamp(loc.Y, minLocaltion.Y, maxLocaltion.Y);
		loc.Z = FMath::Clamp(loc.Z, minLocaltion.Z, maxLocaltion.Z);
	}
	else
	{
		loc = FVector::ZeroVector;
	}

	//限制旋转角度范围在 -30 到 +30
	if (doRot)
	{
		rot.Yaw = FMath::Clamp(rot.Yaw, minRotation.Yaw, maxRotation.Yaw);
		rot.Pitch = FMath::Clamp(rot.Pitch, minRotation.Pitch, maxRotation.Pitch);
		rot.Roll = FMath::Clamp(rot.Roll, minRotation.Roll, maxRotation.Roll);
	}
	else
	{
		rot = FRotator::ZeroRotator;
	}

	//限制缩放范围
	if (doScalc)
	{
		scl.X = FMath::Clamp(scl.X, minScalction.X, maxScalction.X);
		scl.Y = FMath::Clamp(scl.Y, minScalction.Y, maxScalction.Y);
		scl.Z = FMath::Clamp(scl.Z, minScalction.Z, maxScalction.Z);
	}
	else
	{
		scl = FVector(1,1,1);
	}
	

	//应用修正后的数据
	bone.transform.SetLocation(loc);
	bone.transform.SetRotation(FQuat(rot));
	bone.transform.SetScale3D(scl);
}



void UPinchFaceAnimInstance::SavePinchFaceData()
{

}


