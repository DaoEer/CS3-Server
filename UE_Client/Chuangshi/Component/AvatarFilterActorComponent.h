// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include <queue>

#include "FilterActorComponent.h"
#include "KBEngine.h"
#include "AvatarFilterActorComponent.generated.h"

/*
* 文件名称：AvatarFilterActorComponent.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

class UAvatarFilterActorComponent;

class SmoothFilter
{
public:
	static const uint32 NUM_STORED_INPUTS = 8;
	/// 重置时假设每个数据的接收时间相隔0.1秒，
	/// 与服务器每秒发送10次位置数据相匹配
	const float NONZERO_TIME_DIFFERENCE = 0.1f;


	SmoothFilter();
	SmoothFilter(const SmoothFilter& filter);
	virtual ~SmoothFilter();

	void owner(UAvatarFilterActorComponent* o) { owner_ = o; }
	UAvatarFilterActorComponent* owner() { return owner_; }

	bool isActive() { return true; }

	void reset(double time) { reset_ = true; }

	virtual void input(double time, int32 spaceID, int32 vehicleID, const FVector& pos, const FVector& posError, const FVector& dir);

	void output(double time);

	bool getLastInput(double& time, int32& spaceID, int32& vehicleID, FVector& pos, FVector& posError, FVector& direction);

	/**
	*	This is an internal structure used to encapsulate a single set of
	*	received input values for use by the AvatarFilter. Currently the
	*	avatar filter ignores 'roll' and that is continued here.
	*/
	struct StoredInput
	{
		double		time_;
		int32		spaceID_;
		int32		vehicleID_;
		FVector		position_;
		FVector		positionError_;
		FVector		direction_;
		bool		onGround_;
	};

protected:

	/**
	*	This structure stores a location in time and space for the filter
	*	output to move too or from.
	*/
	struct Waypoint
	{
		double			time_;
		int32			spaceID_;
		int32			vehicleID_;
		FVector			position_;
		FVector			direction_;

		StoredInput		storedInput_;

		void changeCoordinateSystem(int32 spaceID, int32 vehicleID);
	};


protected:
	void resetStoredInputs(double time, int32 spaceID, int32 vehicleID, const FVector& position, const FVector& positionError, const FVector& direction);
	void extract(double time, int32& outputSpaceID, int32& outputVehicleID, FVector& outputPosition, FVector& outputVelocity, FVector& outputDirection);
	void chooseNextWaypoint(double time);

public:
	StoredInput& getStoredInput(uint32 index);

protected:
	const StoredInput& getStoredInput(uint32 index) const;


	/// Doxygen comments for all members can be found in the .cpp
	StoredInput		storedInputs_[NUM_STORED_INPUTS];
	uint32			currentInputIndex_;

	Waypoint		nextWaypoint_;
	Waypoint		previousWaypoint_;

	float			latency_;
	float			idealLatency_;
	double			timeOfLastOutput_;
	bool			gotNewInput_;
	bool			reset_;
	
	/// 记录下最后一次的输入时间，用于重置输入，
	/// 以避免因太长时间没有输入而对延迟算法产生负面影响
	double			timeOfLastInput_;
	

	UAvatarFilterActorComponent* owner_;

public:
	static float s_latencyVelocity_; //延迟的速度（速度越快，从pos0-pos1所花的时间就越小）
	static float s_latencyMinimum_;
	float s_latencyFrames_ = 2.0f; //延迟的帧率（值越快，越接近服务器直接传过来的pos，平滑效果就要差些）
	static float s_latencyCurvePower_;
};

/**
 * 一个听从服务器指挥，在一定的时间忠实的插值移动到服务器指定的位置，常用于服务器更新其它玩家、怪物的坐标及朝向
 */
UCLASS( )
class CHUANGSHI_API UAvatarFilterActorComponent : public UFilterActorComponent
{	
	GENERATED_BODY()

	typedef UFilterActorComponent Supper;

public:
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void SimulateMovement(float DeltaTime) override;
	virtual void Pos(const int32 vehicleID, const FVector& position, const FVector& direction, const FVector& velocity);
	virtual void OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void SetPosition(const FVector& position, int32 parentID) override;
	virtual void SetDirection(const FVector& direction, int32 parentID) override;
	virtual void OnGotParentEntity(KBEngine::Entity* parentEnt) override;
	virtual void OnLoseParentEntity() override;
	virtual void InitFilter(bool IsActiveTickEnabled = true) override;
	void SetSmoothFilterLatencyFrames(float LatencyFrame);
	void ResetComponent();
	bool IsMoving();

protected:
	virtual void SetPosBySerPos(const int32 vehicleID, const FVector& position, const FVector& direction);
	virtual void SpeedChangedNotify(float speed) override;
	void UpdateMoveSpeed(const FVector& position, const FVector& direction, const FVector& velocity);

protected:
	SmoothFilter mFilter;
	FVector vLastPos = FVector::ZeroVector;
	FVector mVelocity = FVector::ZeroVector;
	FVector mLastDir = FVector::ZeroVector;
	float mLastYaw = 0.0;
	float mLastSpeed = 0.0;
	bool bCanFilterTick = false;
};
