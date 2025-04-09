// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/CharacterData.h"
#include "BaseOperation.generated.h"

/*
* 文件名称：BaseOperation.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：huting
* 创建时间：2018-01-09
*/

class UItemBase;
 
DECLARE_STATS_GROUP(TEXT("UBaseOperation"), STATGROUP_UBaseOperation, STATCAT_Advanced);

#pragma region	操作基类
UCLASS(Abstract)
class CHUANGSHI_API UBaseOperation : public UCS3Object
{
	GENERATED_BODY()

public:
	/**
	*初始化
	*
	*@param FString OperName 操作名字
	*
	*@return void
	*/
	void Init(FString OperName);

	/**
	*初始化
	*
	*
	*@return FString 名字
	*/
	FString& GetName() { return m_OperName; }

	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);

	/**
	*BlueprintImplementableEvent,蓝图执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	UFUNCTION(BlueprintImplementableEvent)
		void BP_ExecuteOperation(const FString& InputKey, const float& InputScale,const TArray<FString>& OtherValue);

protected:
	/// 是否能执行
	UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();

	/// 是否能执行蓝图重载
	UFUNCTION(BlueprintNativeEvent)
	bool BP_IsCanExecuteOperation();

private:
	/// 操作名字
	FString m_OperName;

};
#pragma endregion

#pragma region	移动操作基类
UCLASS(Abstract)
class CHUANGSHI_API UBaseMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);

protected:
	virtual bool GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector,FVector& KeepVector);

	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	前后方向移动操作(X)
UCLASS()
class CHUANGSHI_API UMoveForwardOperation : public UBaseMoveOperation
{
	GENERATED_BODY()
protected:
	virtual bool GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector) override;
};
#pragma endregion

#pragma region	左右方向移动操作(X)
UCLASS()
class CHUANGSHI_API UMoveRightOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

protected:
	virtual bool GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector) override;
};
#pragma endregion

#pragma region	前后方向移动操作(Y)
UCLASS()
class CHUANGSHI_API UActionMoveForwardOperation : public UBaseMoveOperation
{
	GENERATED_BODY()
protected:
	virtual bool GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector) override;
};
#pragma endregion

#pragma region	左右方向移动操作(Y)
UCLASS()
class CHUANGSHI_API UActionMoveRightOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

protected:
	virtual bool GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector) override;
};
#pragma endregion

#pragma region	载具前后移动
UCLASS()
class CHUANGSHI_API UVehicleMoveForwardOperation : public UBaseMoveOperation
{
	GENERATED_BODY()
protected:
	virtual bool GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector) override;
};
#pragma endregion

#pragma region	飞行上升移动操作
UCLASS()
class CHUANGSHI_API UFlyUpOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	玩家控制器控制的Pawn移动操作基类
UCLASS(Abstract)
class CHUANGSHI_API UBaseActorMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	virtual bool GetMoveWorldDirection(FVector& MoveVector);
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	玩家控制器控制的Pawn前后方向移动操作(比如：鬼瞳之眼探查功能)
UCLASS()
class CHUANGSHI_API UActorMoveForwardOperation : public UBaseActorMoveOperation
{
	GENERATED_BODY()
protected:
	virtual bool GetMoveWorldDirection(FVector& MoveVector) override;
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	玩家控制器控制的Pawn左右方向移动操作(比如：鬼瞳之眼探查功能)
UCLASS()
class CHUANGSHI_API UActorMoveRightOperation : public UBaseActorMoveOperation
{
	GENERATED_BODY()

protected:
	virtual bool GetMoveWorldDirection(FVector& MoveVector) override;
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	玩家控制器控制的Pawn前后方向移动操作(多人载具)
UCLASS()
class CHUANGSHI_API UActorMoveForwardOperation_Vehicle : public UActorMoveForwardOperation
{
	GENERATED_BODY()
protected:
	virtual bool GetMoveWorldDirection(FVector& MoveVector) override;
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	玩家控制器控制的Pawn左右方向移动操作(多人载具)
UCLASS()
class CHUANGSHI_API UActorMoveRightOperation_Vehicle : public UActorMoveRightOperation
{
	GENERATED_BODY()

protected:
	virtual bool GetMoveWorldDirection(FVector& MoveVector) override;
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion


#pragma region	匀速上升+左右移动操作
UCLASS()
class CHUANGSHI_API UYunSuUpOperation : public UActionMoveRightOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)override;

private:
	FVector BeforLocation;
};
#pragma endregion

#pragma region	固定移动朝向操作
UCLASS()
class CHUANGSHI_API UKeepDirectionOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	取消固定移动朝向操作
UCLASS()
class CHUANGSHI_API UUnKeepDirectionOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	记录当前玩家前和右操作
UCLASS()
class CHUANGSHI_API URecordPlayerVectorOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	显示鼠标操作
UCLASS()
class CHUANGSHI_API UShowMouseOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	隐藏鼠标操作
UCLASS()
class CHUANGSHI_API UHideMouseOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	摄像机旋转基类
UCLASS()
class CHUANGSHI_API UBaseCameraTurn : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
protected:
	/// 旋转操作
	virtual void RotateOperation(float InputScale){}
};
#pragma endregion

#pragma region	摄像机左右旋转(Y)
UCLASS()
class CHUANGSHI_API UCameraTurnYOperation : public UBaseCameraTurn
{
	GENERATED_BODY()
protected:
	/// 旋转操作
	virtual void RotateOperation(float InputScale);
};
#pragma endregion

#pragma region	摄像机上下旋转(Y)
UCLASS()
class CHUANGSHI_API UCameraLookUpYOperation : public UBaseCameraTurn
{
	GENERATED_BODY()
protected:
	/// 旋转操作
	virtual void RotateOperation(float InputScale);
};
#pragma endregion

#pragma region	摄像机左右旋转(X)
UCLASS()
class CHUANGSHI_API UCameraTurnOperation : public UCameraTurnYOperation
{
	GENERATED_BODY()
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();

};
#pragma endregion

#pragma region	摄像机上下旋转(X)
UCLASS()
class CHUANGSHI_API UCameraLookUpOperation : public UCameraLookUpYOperation
{
	GENERATED_BODY()
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	练兵模式摄像机上下旋转(偏移最小值有做限制)
UCLASS()
class CHUANGSHI_API UCameraLookUpTrainSoldierOperation : public UCameraLookUpOperation
{
	GENERATED_BODY()
protected:
	/// 旋转操作
	virtual void RotateOperation(float InputScale);
private:
	void LimitViewPitch(FRotator& ViewRotation, float InViewPitchMin, float InViewPitchMax);
};
#pragma endregion


#pragma region	清除施法辅助操作
UCLASS()
class CHUANGSHI_API UClearSkillAssisOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	点击地面移动操作
UCLASS()
class CHUANGSHI_API UMoveByClickOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);

protected:
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	通知玩家左击事件操作
UCLASS()
class CHUANGSHI_API UCallLeftClickEventOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	通知玩家右击事件操作
UCLASS()
class CHUANGSHI_API UCallRightClickEventOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	通知玩家Esc按键事件操作
UCLASS()
class CHUANGSHI_API UCallEscClickEventOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	摄像机被操作操作
UCLASS()
class CHUANGSHI_API UCameraBeOperationOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	取消摄像机被操作操作
UCLASS()
class CHUANGSHI_API UUnCameraBeOperationOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	玩家旋转基类操作
UCLASS(Abstract)
class CHUANGSHI_API UBaseTurnOperation : public UBaseOperation
{
	GENERATED_BODY()

protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	玩家旋转(类似ACT旋转，但是当IsCanExecuteOperation=false时玩家可以旋转，如鼠标点击地面玩家可以转向移动目标)
UCLASS()
class CHUANGSHI_API USACTBaseTurnOperation : public UBaseTurnOperation
{
	GENERATED_BODY()
public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	玩家旋转操作
UCLASS()
class CHUANGSHI_API UTurnOperation : public UBaseTurnOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);

protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	玩家Action旋转操作
UCLASS()
class CHUANGSHI_API UActionTurnOperation : public UBaseTurnOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	玩家旋转(ALT)
UCLASS()
class CHUANGSHI_API UALTTurnOperation : public USACTBaseTurnOperation
{
	GENERATED_BODY()
public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();

};
#pragma endregion

#pragma region	玩家旋转(飞行轨道模式)
UCLASS()
class CHUANGSHI_API UFlyTurnOperation : public UActionTurnOperation
{
	GENERATED_BODY()
public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();

};

#pragma region	玩家旋转(滑翔模式)
UCLASS()
class CHUANGSHI_API UGlidingTurnOperation : public USACTBaseTurnOperation
{
	GENERATED_BODY()	
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	玩家旋转(降落模式)
UCLASS()
class CHUANGSHI_API UFallTurnOperation : public USACTBaseTurnOperation
{
	GENERATED_BODY()
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	玩家控制器控制的Pawn旋转操作(比如：鬼瞳之眼探查功能)
UCLASS()
class CHUANGSHI_API UActorTurnOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region	玩家是否能旋转
UCLASS()
class CHUANGSHI_API UActorCanTurnOperation : public UBaseOperation
{
	GENERATED_BODY()
public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
private:
	float OldInputScale = 0.0f;
};
#pragma endregion

#pragma region 开启自动移动
UCLASS()
class CHUANGSHI_API UOpenAutoMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 关闭自动移动
UCLASS()
class CHUANGSHI_API UCloseAutoMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 闪避基类
UCLASS(Abstract)
class CHUANGSHI_API UBaseDodgeOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	virtual bool IsCanExecuteOperation();
protected:
	//获取闪避技能ID
	virtual int32 GetFrontDodgeSkillID() { return 900002001; }
	virtual int32 GetDodgeSkillID() { return 0; }
	//获取禁止转向时旋转角度
	virtual FRotator GetRoleNewRotation();
	//获取开始转向时旋转角度
	virtual bool GetRoleStartRotation();
private:
	UFUNCTION()
		void DeferredUseSkill();
};
#pragma endregion

#pragma region 前闪避
UCLASS()
class CHUANGSHI_API UDodgeFrontOperation : public UBaseDodgeOperation
{
	GENERATED_BODY()

protected:
	//获取闪避技能ID
	virtual int32 GetDodgeSkillID() { return 900002001; }
	//获取禁止转向时旋转角度
	virtual FRotator GetRoleNewRotation();

};
#pragma endregion

#pragma region 后闪避
UCLASS()
class CHUANGSHI_API UDodgeBackOperation : public UBaseDodgeOperation
{
	GENERATED_BODY()

protected:
	//获取闪避技能ID
	virtual int32 GetDodgeSkillID() { return 900002002; }
	//获取禁止转向时旋转角度
	virtual FRotator GetRoleNewRotation();

};
#pragma endregion

#pragma region 左闪避
UCLASS()
class CHUANGSHI_API UDodgeLeftOperation : public UBaseDodgeOperation
{
	GENERATED_BODY()

protected:
	//获取闪避技能ID
	virtual int32 GetDodgeSkillID() { return 900002003; }
	//获取禁止转向时旋转角度
	virtual FRotator GetRoleNewRotation();

};
#pragma endregion

#pragma region 右闪避
UCLASS()
class CHUANGSHI_API UDodgeRightOperation : public UBaseDodgeOperation
{
	GENERATED_BODY()

protected:
	//获取闪避技能ID
	virtual int32 GetDodgeSkillID() { return 900002004; }
	//获取禁止转向时旋转角度
	virtual FRotator GetRoleNewRotation();

};
#pragma endregion

#pragma region 玩家镜头缩放基类
UCLASS(Abstract)
class CHUANGSHI_API UBaseFlexHandleOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);

protected:
	virtual float GetSpeed() { return 0.0f; }
};
#pragma endregion

#pragma region 镜头扩大
UCLASS()
class CHUANGSHI_API UAddFlexHandleOperation : public UBaseFlexHandleOperation
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return -50.0f; }
};
#pragma endregion

#pragma region 镜头缩小
UCLASS()
class CHUANGSHI_API UDelFlexHandleOperation : public UBaseFlexHandleOperation
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return 50.0f; }
};
#pragma endregion

#pragma region 模型旋转基类
UCLASS(Abstract)
class CHUANGSHI_API UBaseFlexHandleOperation_ModelTurn : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	virtual float GetSpeed() { return 0.0f; }
};
#pragma endregion

#pragma region 模型右旋转
UCLASS()
class CHUANGSHI_API UBaseFlexHandleOperation_ModelTurnRight : public UBaseFlexHandleOperation_ModelTurn
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return 10.0f; }
};
#pragma endregion

#pragma region 模型左旋转
UCLASS()
class CHUANGSHI_API UBaseFlexHandleOperation_ModelTurnLeft : public UBaseFlexHandleOperation_ModelTurn
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return -10.0f; }
};
#pragma endregion

#pragma region 怪物镜头缩放基类(鬼瞳之眼探查功能)
UCLASS(Abstract)
class CHUANGSHI_API UBaseFlexHandleOperation_Monster : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	virtual float GetSpeed() { return 0.0f; }
};
#pragma endregion

#pragma region 镜头扩大
UCLASS()
class CHUANGSHI_API UAddFlexHandleOperation_Monster : public UBaseFlexHandleOperation_Monster
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return -50.0f; }
};
#pragma endregion

#pragma region 镜头缩小
UCLASS()
class CHUANGSHI_API UDelFlexHandleOperation_Monster : public UBaseFlexHandleOperation_Monster
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return 50.0f; }
};
#pragma endregion

#pragma region 镜头缩放基类(多人载具)
UCLASS(Abstract)
class CHUANGSHI_API UBaseFlexHandleOperation_Vehicle : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	virtual float GetSpeed() { return 0.0f; }
};
#pragma endregion

#pragma region 镜头扩大
UCLASS()
class CHUANGSHI_API UAddFlexHandleOperation_Vehicle : public UBaseFlexHandleOperation_Vehicle
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return -50.0f; }
};
#pragma endregion

#pragma region 镜头缩小
UCLASS()
class CHUANGSHI_API UDelFlexHandleOperation_Vehicle : public UBaseFlexHandleOperation_Vehicle
{
	GENERATED_BODY()

protected:
	virtual float GetSpeed() { return 50.0f; }
};
#pragma endregion

#pragma region 恢复到背景模式
UCLASS()
class CHUANGSHI_API URecoveryModeOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 切换到Alt模式
UCLASS()
class CHUANGSHI_API USwitchToAltOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);

protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region 重置已按下键操作
UCLASS()
class CHUANGSHI_API UFlushPressedKeysOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion


#pragma region 切换到YControl模式
UCLASS()
class CHUANGSHI_API USwitchToYControlOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 跳跃操作
UCLASS()
class CHUANGSHI_API UJumpPressedOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 停止跳跃操作
UCLASS()
class CHUANGSHI_API UJumpReleasedOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 跳跃操作（控制器控制的Pawn）
UCLASS()
class CHUANGSHI_API UPawnJumpPressedOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	virtual bool IsCanExecuteOperation() override;
};

UCLASS()
class CHUANGSHI_API UPawnJumpReleasedOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region 切换快捷栏按键到Dafault
UCLASS()
class CHUANGSHI_API USwitchToDafaultQuickOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 切换快捷栏按键到Action
UCLASS()
class CHUANGSHI_API USwitchToActionQuickOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 设置玩家可以Actor旋转
UCLASS()
class CHUANGSHI_API UActorCanRotateOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale,TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 调整摄像机视角
UCLASS()
class CHUANGSHI_API UAdjustViewTargetWithBlendOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 取消调整摄像机视角
UCLASS()
class CHUANGSHI_API UUnAdjustViewTargetWithBlendOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 使用技能
UCLASS()
class CHUANGSHI_API UUseSkillOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region 使用物品基类
UCLASS(Abstract)
class CHUANGSHI_API UUseItemBaseOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	virtual UItemBase* GetItem(TArray<FString>& OtherValue) { return nullptr; }
};
#pragma endregion

#pragma region 在快捷栏使用物品
UCLASS()
class CHUANGSHI_API UUseItemInQuickOperation : public UUseItemBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	virtual bool IsCanExecuteOperation() override;

protected:
	virtual UItemBase* GetItem(TArray<FString>& OtherValue);
};
#pragma endregion

#pragma region 在背包使用物品
UCLASS()
class CHUANGSHI_API UUseItemInBagOperation : public UUseItemBaseOperation
{
	GENERATED_BODY()
public:
		virtual bool IsCanExecuteOperation() override;
protected:
	virtual UItemBase* GetItem(TArray<FString>& OtherValue);
};
#pragma endregion

#pragma region 检测是否进入Y操作
UCLASS()
class CHUANGSHI_API UCheckChangeToYOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	荷花移动操作基类
UCLASS(Abstract)
class CHUANGSHI_API UHeHuaBaseMoveOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:	
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();

	void OnCallServerMethod(const FString& DirectionName);	
};

#pragma region	荷花向前移动操作基类
UCLASS()
class CHUANGSHI_API UHeHuaForwardMoveOperation : public UHeHuaBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion


#pragma region	荷花向后移动操作基类
UCLASS()
class CHUANGSHI_API UHeHuaBackwardsMoveOperation : public UHeHuaBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region	荷花向右移动操作基类
UCLASS()
class CHUANGSHI_API UHeHuaRightsMoveOperation : public UHeHuaBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region	荷花向左移动操作基类
UCLASS()
class CHUANGSHI_API UHeHuaLeftMoveOperation : public UHeHuaBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region	下荷花操作
UCLASS()
class CHUANGSHI_API UDismountHeHuaOperation : public UBaseMoveOperation
{
	GENERATED_BODY()
public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};

#pragma endregion


#pragma region	随机动作行为
UCLASS()
class CHUANGSHI_API URandomActionOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
private:
	int32 StandTime; //静止站立的时间
};
#pragma endregion

#pragma region 使用射击技能
UCLASS()
class CHUANGSHI_API UUseSkillOfBaseShoot : public UUseSkillOperation
{
	GENERATED_BODY()
public:
	/**
		*获取技能ID
		*
		*@param FString  当前模式中对应不同状态的名字
		*@param float InputScale 输入的轴变量
		*
		*@return FString
		*/
	virtual FString GetSkillIDByState(int32 Index);
};
#pragma endregion

#pragma region 使用射击技能（仅灵域狩魂可用）
UCLASS()
class CHUANGSHI_API UUseSkillOfShoot : public UUseSkillOfBaseShoot
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

private:
	//关闭自动射击
	void CloseAutoShoot();
	void UsePositionSkill();
private:
	//自动战斗句柄
	FTimerHandle AutoShootHandle;
};
#pragma endregion

#pragma region 关闭射击技能（仅灵域狩魂可用）
UCLASS()
class CHUANGSHI_API UCloseAutoShoot : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 右键瞄准状态（远程吃鸡）
UCLASS()
class CHUANGSHI_API UUseAimState : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 使用射击连线技能（仅灵域狩魂可用）
UCLASS()
class CHUANGSHI_API UUseSkillOfLineShoot : public UUseSkillOfBaseShoot
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
protected:
	/// 是否能执行
	//UFUNCTION(BlueprintCallable)
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region 打断射击连线技能（仅灵域狩魂可用）
UCLASS()
class CHUANGSHI_API UBreakSkillOfLineShoot : public UUseSkillOfBaseShoot
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 进入自动寻路
UCLASS()
class CHUANGSHI_API UActivateNavigateMoveMode : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
protected:
	/// 是否能执行
	virtual bool IsCanExecuteOperation();
};
#pragma endregion

#pragma region 退出自动寻路
UCLASS()
class CHUANGSHI_API UUnActivateNavigateMoveMode : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 开始跨地图寻路
UCLASS()
class CHUANGSHI_API UStartCrossMapNavigate : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 开始摆摊
UCLASS()
class CHUANGSHI_API UOnStartStallOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	八卦阵向前移动操作基类
UCLASS()
class CHUANGSHI_API UBaGuaZhenForwardMoveOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
protected:
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	八卦阵向右移动操作基类
UCLASS()
class CHUANGSHI_API UBaGuaZhenRightMoveOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
protected:
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	新版秘境移动操作
UCLASS()
class CHUANGSHI_API UMiJingForwardOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion

#pragma region	玩家辅助跳跃操作
UCLASS()
class CHUANGSHI_API UPlayerLedgesJumpOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

private:
	/**
	*获取辅助跳参数
	*
	*@param FString  辅助下跳检测长度
	*
	*/
	void GetParameter(int32& LedgesJumpDownStep);
};
#pragma endregion

#pragma region 云梯上下攀爬
UCLASS()
class CHUANGSHI_API ULadderForwardMoveOperation : public UBaseMoveOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};

#pragma region 使用0-9快捷键
UCLASS()
class CHUANGSHI_API UUseQuickKeyOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 勇闯绝命岛射击模式使用0-9快捷键
UCLASS()
class CHUANGSHI_API UShootYCJMDUseQuickKeyOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	帮会掠夺战器械建造模式左击事件操作
UCLASS()
class CHUANGSHI_API UEquipBuildLeftClickOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region	帮会掠夺战器械建造模式右键或者按ESC按钮取消建造
UCLASS()
class CHUANGSHI_API UEquipBuildCancelOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 空中飞行载具大鸟左右移动(新版吃鸡)
UCLASS()
class CHUANGSHI_API UYCJMDSkyCarrierRightMoveOperation : public UMoveRightOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region 按F键离开空中飞行载具大鸟(新版吃鸡)
UCLASS()
class CHUANGSHI_API ULeaveYCJMDSkyCarrierOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
};
#pragma endregion

#pragma region 按F键开始打开降落伞(新版吃鸡)
UCLASS()
class CHUANGSHI_API UYCJMDFKeyOpenParachuteOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region 跳伞过程中(未开伞)向前后移动(新版吃鸡)
UCLASS()
class CHUANGSHI_API UYCJMDSkyDivingForwardMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region 跳伞过程中(未开伞)向左右移动(新版吃鸡)
UCLASS()
class CHUANGSHI_API UYCJMDSkyDivingRightMoveOperation : public UMoveRightOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region 跳伞过程中(已开伞)向前后移动(新版吃鸡)
UCLASS()
class CHUANGSHI_API UYCJMDOpenParachuteForwardMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);
private:
	
};
#pragma endregion

#pragma region 跳伞过程中(已开伞)向左右移动(新版吃鸡)
UCLASS()
class CHUANGSHI_API UYCJMDOpenParachuteRightMoveOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

};
#pragma endregion

#pragma region	上下载具
UCLASS()
class CHUANGSHI_API UVehicleOperation : public UBaseOperation
{
	GENERATED_BODY()

public:
	/**
	*执行操作
	*
	*@param FKey InputKey 输入的KEY值
	*@param float InputScale 输入的轴变量
	*
	*@return FString 名字
	*/
	virtual void ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue);

protected:
	virtual bool IsCanExecuteOperation() override;
};
#pragma endregion