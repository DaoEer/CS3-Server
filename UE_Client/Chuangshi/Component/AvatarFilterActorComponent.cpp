// Fill out your copyright notice in the Description page of Project Settings.
#include "AvatarFilterActorComponent.h"
#include "CS3Base/GameObject.h"
#include "Interface/CombatInterface.h"
#include "Interface/StateInterface.h"
#include "GameData/GameDeFine.h"
#include "Actor/ServerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/KismetMathLibrary.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Entity.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("SimulateMovement(AvatarFilter)"), STAT_AvatarFilterSimulateMovement, STATGROUP_CS3EntityActorSynchLocation);
DECLARE_CYCLE_STAT(TEXT("Pos(AvatarFilter)"), STAT_AvatarFilterPos, STATGROUP_CS3EntityActorSynchLocation);
DECLARE_CYCLE_STAT(TEXT("UpdateMoveSpeed(AvatarFilter)"), STAT_AvatarFilterUpdateMoveSpeed, STATGROUP_CS3EntityActorSynchLocation);

DECLARE_CYCLE_STAT(TEXT("SmoothFilter::output"), STAT_SmoothFilter_output, STATGROUP_CS3EntityActorSynchLocation);
DECLARE_CYCLE_STAT(TEXT("SmoothFilter::extract"), STAT_SmoothFilter_extract, STATGROUP_CS3EntityActorSynchLocation);
DECLARE_CYCLE_STAT(TEXT("SmoothFilter::chooseNextWaypoint"), STAT_SmoothFilter_chooseNextWaypoint, STATGROUP_CS3EntityActorSynchLocation);

namespace FilterUtilityFunctions
{
	/**
	*	This function decodes the 'on ground' condition by sampling
	*	the terrain height.
	*/
	bool resolveOnGroundPosition(FVector& position, bool& onGround)
	{
		//onGround = false;

		//if (position.y < -12000.0f)
		//{
		//	float terrainHeight = Terrain::BaseTerrainBlock::getHeight(position[0],
		//		position[2]);
		//	if (terrainHeight == Terrain::BaseTerrainBlock::NO_TERRAIN)
		//		return false;


		//	position.y = terrainHeight;
		//	onGround = true;
		//}

		return true;
	}

	/**
	*	This function transforms the given position and direction into
	*	common/world space.
	*
	*	@param	spaceID	The server space in which the give position and direction
	*				are defined.
	*	@param	vehicleID	The vehicle who's coordinate system the given position and
	*				direction are defined.
	*	@param	pos	The local space position to be translated into common space.
	*	@param	dir	The local space direction to be translated into common space.
	*/
	void transformIntoCommon(int32 spaceID, int32 vehicleID, FVector& pos, FVector& dir)
	{
		if (vehicleID <= 0)
			return;

		if (UUECS3GameInstance::pKBEApp == nullptr)
		{
			return;
		}

		KBEngine::Entity* parentEnt = UUECS3GameInstance::pKBEApp->FindEntity(vehicleID);
		if (!parentEnt)
		{
			CS3_Warning(TEXT("-->Null Pointer error:transformIntoCommon : parentEnt!"));
			return;
		}

		pos = parentEnt->PositionLocalToWorld(pos);
		dir = parentEnt->DirectionLocalToWorld(dir);
	}

	/**
	*	This function transforms the given position to its local representation.
	*
	*	@param	spaceID	The server space into which the give position and direction
	*				will be placed.
	*	@param	vehicleID	The vehicle in who's coordinate system the given position
	*				and direction will now exist.
	*	@param	pos	The common space position to be translated into local space.
	*	@param	dir	The common space direction to be translated into local space.
	*/
	void transformFromCommon(int32 spaceID, int32 vehicleID, FVector& pos, FVector& dir)
	{
		if (vehicleID <= 0)
			return;

		if (UUECS3GameInstance::pKBEApp == nullptr)
		{
			return;
		}
		KBEngine::Entity* parentEnt = UUECS3GameInstance::pKBEApp->FindEntity(vehicleID);
		if (!parentEnt)
		{
			CS3_Warning(TEXT("-->Null Pointer error:transformFromCommon : parentEnt!"));
			return;
		}

		pos = parentEnt->PositionWorldToLocal(pos);
		dir = parentEnt->DirectionWorldToLocal(dir);
	}

	FVector clamp(const FVector& alpha, const FVector& lower, const FVector& upper)
	{
		return FVector(
			FMath::Clamp<float>(alpha.X, lower.X, upper.X),
			FMath::Clamp<float>(alpha.Y, lower.Y, upper.Y),
			FMath::Clamp<float>(alpha.Z, lower.Z, upper.Z) );
	}

	bool almostEqual(const FVector& v1, const FVector& v2, const float epsilon = 0.0004f)
	{
		return	FMath::IsNearlyEqual(v1.X, v2.X, epsilon) &&
				FMath::IsNearlyEqual(v1.Y, v2.Y, epsilon) &&
				FMath::IsNearlyEqual(v1.Z, v2.Z, epsilon);
	}

	/**
	*	This method tests if the bounding box contains the given point
	*/
	bool intersects(const FBox& b, const FVector& v)
	{
		return (v[0] >= b.Min[0]) && (v[1] >= b.Min[1]) && (v[2] >= b.Min[2]) &&
			(v[0] < b.Max[0]) && (v[1] < b.Max[1]) && (v[2] < b.Max[2]);
	}

	/**
	* 把两个不同符号的角度換成相同符号的角度
	*/
	float sameSignDegree(float degree, float closer)
	{
		if (closer > degree + 180.0)
			return closer - 2.0 * 180.0;
		else if (closer < degree - 180.0)
			return closer + 2.0 * 180.0;
		else
			return closer;
	}

	FVector sameSignDegree(const FVector& degree, const FVector& closer)
	{
		FVector v;
		v.X = sameSignDegree(degree.X, closer.X);
		v.Y = sameSignDegree(degree.Y, closer.Y);
		v.Z = sameSignDegree(degree.Z, closer.Z);
		return v;
	}
}









float SmoothFilter::s_latencyVelocity_ = 1.00f;
float SmoothFilter::s_latencyMinimum_ = 0.10f;
float SmoothFilter::s_latencyCurvePower_ = 2.0f;


SmoothFilter::SmoothFilter() :
	latency_(0),
	idealLatency_(0),
	timeOfLastOutput_(0),
	gotNewInput_(false),
	reset_(true),
	timeOfLastInput_(0),
	owner_(nullptr)
{
	s_latencyFrames_ = 2.0f;
	this->resetStoredInputs(-2000, 0, 0, FVector::ZeroVector, FVector::ZeroVector, FVector::ZeroVector);
	this->reset(0);
}

SmoothFilter::SmoothFilter(const SmoothFilter& filter) :
	//nextWaypoint_(filter.nextWaypoint_),
	//previousWaypoint_(filter.previousWaypoint_),
	currentInputIndex_(filter.currentInputIndex_),
	latency_(filter.latency_),
	idealLatency_(filter.idealLatency_),
	timeOfLastOutput_(filter.timeOfLastOutput_),
	//timeOfLastInput_(filter.timeOfLastInput_),
	gotNewInput_(filter.gotNewInput_),
	reset_(filter.reset_)
{
	nextWaypoint_ = filter.nextWaypoint_;
	previousWaypoint_ = filter.previousWaypoint_;
	timeOfLastInput_ = filter.timeOfLastInput_;

	for (uint32 i = 0; i<NUM_STORED_INPUTS; i++)
	{
		storedInputs_[i] = filter.storedInputs_[i];
	}
}

SmoothFilter::~SmoothFilter()
{
}

void SmoothFilter::input(double time, int32 spaceID, int32 vehicleID, const FVector & position, const FVector& positionError, const FVector& direction)
{
	// 长时间没有新数据输入就认为是重新开始，需要重置时间
	if (!reset_ && time - timeOfLastInput_ > 1.0f)
	{
		const StoredInput& topInput = getStoredInput(0);
		for (uint32 i = 0; i < NUM_STORED_INPUTS; i++)
		{
			StoredInput& storedInput = getStoredInput(i);
			storedInput.time_ = time - (i * NONZERO_TIME_DIFFERENCE);
			storedInput.position_ = topInput.position_;
			storedInput.direction_ = topInput.direction_;
			storedInput.vehicleID_ = topInput.vehicleID_;
			storedInput.spaceID_ = topInput.spaceID_;
			storedInput.onGround_ = topInput.onGround_;
		}
	}

	if (reset_)
	{
		this->resetStoredInputs(time, spaceID, vehicleID, position, positionError, direction);
		reset_ = false;
	}
	else
	{
		if (time > this->getStoredInput(0).time_)
		{
			currentInputIndex_ = (currentInputIndex_ + NUM_STORED_INPUTS - 1) % NUM_STORED_INPUTS;
		}

		StoredInput & storedInput = this->getStoredInput(0);

		storedInput.time_ = time;
		storedInput.spaceID_ = spaceID;
		storedInput.vehicleID_ = vehicleID;
		storedInput.position_ = position;
		storedInput.positionError_ = positionError;
		storedInput.direction_ = direction;

		FilterUtilityFunctions::resolveOnGroundPosition(storedInput.position_, storedInput.onGround_);

		gotNewInput_ = true;
	}

	timeOfLastInput_ = time;
}

void SmoothFilter::output(double time)
{
	SCOPE_CYCLE_COUNTER(STAT_SmoothFilter_output);
	
	// adjust ideal latency if we got something new
	if (gotNewInput_)
	{
		gotNewInput_ = false;

		const double newestTime = this->getStoredInput(0).time_;
		const double olderTime = this->getStoredInput(NUM_STORED_INPUTS - 1).time_;
		
		s_latencyFrames_ = FMath::Clamp<float>(s_latencyFrames_, 0.0f, NUM_STORED_INPUTS - 1);

		double ratio = ((NUM_STORED_INPUTS - 1) - s_latencyFrames_) / (NUM_STORED_INPUTS - 1);
		
		idealLatency_ = float(time - FMath::Lerp(olderTime, newestTime, ratio));

		idealLatency_ = std::max(idealLatency_, s_latencyMinimum_);
	}

	// move latency towards the ideal...
	float dTime = float(time - timeOfLastOutput_);
	if (idealLatency_ > latency_)
	{
		latency_ += (s_latencyVelocity_ * dTime) * std::min(1.0f, powf(fabsf(idealLatency_ - latency_), SmoothFilter::s_latencyCurvePower_));
		latency_ = std::min(latency_, idealLatency_);
	}
	else
	{
		latency_ -= (s_latencyVelocity_ * dTime) * std::min(1.0f, powf(fabsf(idealLatency_ - latency_), SmoothFilter::s_latencyCurvePower_));
		latency_ = std::max(latency_, idealLatency_);
	}


	// record this so we can move latency at a velocity independent
	//  of the number of times we're called.
	timeOfLastOutput_ = time;

	// find the position at 'time - latency'
	double outputTime = time - latency_;

	int32		resultSpaceID;
	int32		resultVehicleID;
	FVector		resultPosition;
	FVector		resultVelocity;
	FVector		resultDirection;

	this->extract(outputTime, resultSpaceID, resultVehicleID, resultPosition, resultVelocity, resultDirection);

	// make sure it's in the right coordinate system
	//FilterUtilityFunctions::coordinateSystemCheck(owner_, resultSpaceID, resultVehicleID);

	owner_->Pos(resultVehicleID, resultPosition, resultDirection, resultVelocity);
}

/**
*	This method changes the coordinate system of the waypoint by first
*	transforming into common coordinates and then into the new coordinates.
*	spaceID_ and vehicleID_ are also set to that of the new coordinate system.
*/
void SmoothFilter::Waypoint::changeCoordinateSystem(int32 spaceID, int32 vehicleID)
{
	if (spaceID_ == spaceID && vehicleID_ == vehicleID)
		return;

	FilterUtilityFunctions::transformIntoCommon(spaceID_,
		vehicleID_,
		position_,
		direction_);

	spaceID_ = spaceID;
	vehicleID_ = vehicleID;

	FilterUtilityFunctions::transformFromCommon(spaceID_,
		vehicleID_,
		position_,
		direction_);
}

void SmoothFilter::resetStoredInputs(double time, int32 spaceID, int32 vehicleID, const FVector& position, const FVector& positionError, const FVector& direction)
{
	currentInputIndex_ = 0;
	gotNewInput_ = true;

	for (uint32 i = 0; i< NUM_STORED_INPUTS; i++)
	{
		StoredInput & storedInput = this->getStoredInput(i);

		// set times of older inputs as to avoid zero time differences
		storedInput.time_ = time - (i * NONZERO_TIME_DIFFERENCE);

		storedInput.spaceID_ = spaceID;
		storedInput.vehicleID_ = vehicleID;
		storedInput.position_ = position;
		storedInput.positionError_ = positionError;
		storedInput.direction_ = direction;

		FilterUtilityFunctions::resolveOnGroundPosition(storedInput.position_, storedInput.onGround_);
	}

	this->latency_ = s_latencyFrames_ * NONZERO_TIME_DIFFERENCE;

	nextWaypoint_.time_ = time - NONZERO_TIME_DIFFERENCE;
	nextWaypoint_.spaceID_ = spaceID;
	nextWaypoint_.vehicleID_ = vehicleID;
	nextWaypoint_.position_ = position;
	nextWaypoint_.direction_ = direction;

	previousWaypoint_ = nextWaypoint_;
	previousWaypoint_.time_ -= NONZERO_TIME_DIFFERENCE;
}

/**
*	This method 'extracts' a set of filtered values from the input history,
*	clamping at the extremes of the time period stored. In the case that
*	requested time falls between two inputs a weighed blend is performed
*	taking into account vehicle transitions.
*	A small amount of speculative movement supported when the most recent
*	value in the history is older than the time requested.
*
*	@param	time		The client time stamp of the values required.
*	@param	iSID		The resultant space ID
*	@param	iVID		The resultant vehicle ID
*	@param	iPos		The estimated position in the space of iVID
*	@param	iVelocity	The estimated velocity of the entity at the time
*						specified.
*	@param	iDir		The estimated yaw and pitch of the entity.
*/
void SmoothFilter::extract(double time, int32& outputSpaceID, int32& outputVehicleID, FVector& outputPosition, FVector& outputVelocity, FVector& outputDirection)
{
	SCOPE_CYCLE_COUNTER(STAT_SmoothFilter_extract);
	if (!isActive())
	{
		const StoredInput & mostRecentInput = this->getStoredInput(0);

		outputSpaceID = mostRecentInput.spaceID_;
		outputVehicleID = mostRecentInput.vehicleID_;
		outputPosition = mostRecentInput.position_;
		outputDirection = mostRecentInput.direction_;
		outputVelocity = FVector::ZeroVector;
		
		return;
	}
	else
	{
		if (time > nextWaypoint_.time_)
		{
			this->chooseNextWaypoint(time);
		}

		float proportionateDifferenceInTime = float((time - previousWaypoint_.time_) /
			(nextWaypoint_.time_ - previousWaypoint_.time_));

		outputSpaceID = nextWaypoint_.spaceID_;
		outputVehicleID = nextWaypoint_.vehicleID_;
		
		outputPosition = FMath::Lerp(previousWaypoint_.position_, nextWaypoint_.position_, proportionateDifferenceInTime);

		outputVelocity = (nextWaypoint_.position_ - previousWaypoint_.position_) /
			float(nextWaypoint_.time_ - previousWaypoint_.time_);

		outputDirection = FMath::Lerp(FilterUtilityFunctions::sameSignDegree(nextWaypoint_.direction_, previousWaypoint_.direction_), nextWaypoint_.direction_, proportionateDifferenceInTime);
	}


}

/**
*	This internal method choses a new set of waypoints to traverse based on the
*	history of stored input and the requested time. A few approaches are used
*	depending on the number of received inputs ahead of the requested time.
*
*	Two inputs ahead of time
*	A vector is made from head of the previous waypoints to the centre of the
*	input two ahead. The point on this vector that exists one input ahead in
*	time is then found and its position clamped to the box of error tolerance
*	of that same input. This point forms the new head waypoint and the previous
*	becomes the new tail.
*
*	Only one input ahead of time
*	The current pair of waypoints are projected into the future to the time of
*	the next input ahead. The resultant position is then clamped to the box of
*	error tolerance of that input.
*
*	No inputs ahead of time
*	In the event no inputs exist ahead of the time both waypoints are set to
*	the same position. The entity will stand still until an input is received
*	that is ahead of game time minus latency.
*
*	Note: Both waypoints are always in the same coordinate system; that of the
*	next input ahead.
*
*	@param time	The time which the new waypoints should enclose
*/
void SmoothFilter::chooseNextWaypoint(double time)
{
	SCOPE_CYCLE_COUNTER(STAT_SmoothFilter_chooseNextWaypoint);

	Waypoint & previousWaypoint = previousWaypoint_;
	Waypoint & currentWaypoint = nextWaypoint_;

	Waypoint newWaypoint;

	if (this->getStoredInput(0).time_ > time)
	{
		for (int i = NUM_STORED_INPUTS - 1; i >= 0; i--)
		{
			if (this->getStoredInput(i).time_ > time)
			{
				const StoredInput & lookAheadInput = this->getStoredInput(0);
				const StoredInput & nextInput = this->getStoredInput(i);

				newWaypoint.time_ = nextInput.time_;
				newWaypoint.spaceID_ = nextInput.spaceID_;
				newWaypoint.vehicleID_ = nextInput.vehicleID_;
				newWaypoint.direction_ = nextInput.direction_;

				newWaypoint.storedInput_ = nextInput;

				previousWaypoint.changeCoordinateSystem(newWaypoint.spaceID_,
					newWaypoint.vehicleID_);

				currentWaypoint.changeCoordinateSystem(newWaypoint.spaceID_,
					newWaypoint.vehicleID_);

				float lookAheadRelativeDifferenceInTime = float((lookAheadInput.time_ - previousWaypoint.time_) /
					(currentWaypoint.time_ - previousWaypoint.time_));

				FVector lookAheadPosition = FMath::Lerp(previousWaypoint.position_, currentWaypoint.position_, lookAheadRelativeDifferenceInTime);

				FVector direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformIntoCommon(newWaypoint.spaceID_,    newWaypoint.vehicleID_,    lookAheadPosition, direction);
				direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformFromCommon(lookAheadInput.spaceID_, lookAheadInput.vehicleID_, lookAheadPosition, direction);

				lookAheadPosition = FilterUtilityFunctions::clamp(lookAheadPosition, 
							lookAheadInput.position_ - lookAheadInput.positionError_,
							lookAheadInput.position_ + lookAheadInput.positionError_);

				direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformIntoCommon(lookAheadInput.spaceID_, lookAheadInput.vehicleID_, lookAheadPosition, direction);
				direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformFromCommon(newWaypoint.spaceID_,    newWaypoint.vehicleID_,    lookAheadPosition, direction);

				// Handel overlapping error rectangles
				{
					FBox newWaypointBB(newWaypoint.storedInput_.position_ - newWaypoint.storedInput_.positionError_,
						newWaypoint.storedInput_.position_ + newWaypoint.storedInput_.positionError_);
					FBox currentWaypointBB(currentWaypoint.storedInput_.position_ - currentWaypoint.storedInput_.positionError_,
						currentWaypoint.storedInput_.position_ + currentWaypoint.storedInput_.positionError_);

					if (newWaypoint.spaceID_ == currentWaypoint.storedInput_.spaceID_ &&
						newWaypoint.vehicleID_ == currentWaypoint.storedInput_.vehicleID_ &&
						!FilterUtilityFunctions::almostEqual(newWaypoint.storedInput_.positionError_, currentWaypoint.storedInput_.positionError_) &&
						newWaypointBB.Intersect(currentWaypointBB))
					{
						// Remain still if the previous move was only to adjust
						// for changes in position error (ie overlapping error regions).
						newWaypoint.position_ = currentWaypoint.position_;
					}
					else
					{
						float proportionateDifferenceInTime = float((nextInput.time_ - currentWaypoint.time_) /
							(lookAheadInput.time_ - currentWaypoint.time_));

						newWaypoint.position_ = FMath::Lerp(currentWaypoint.position_, lookAheadPosition, proportionateDifferenceInTime);
					}
				}

				// Constrain waypoint position to its input error rectangle
				{
					FBox nextInputBB(nextInput.position_ - nextInput.positionError_,
						nextInput.position_ + nextInput.positionError_);

					if (!FilterUtilityFunctions::intersects(nextInputBB, newWaypoint.position_))
					{
						FVector clampedPosition = FilterUtilityFunctions::clamp(newWaypoint.position_,
							nextInput.position_ - nextInput.positionError_,
							nextInput.position_ + nextInput.positionError_);

						FVector lookAheadVector = newWaypoint.position_ - currentWaypoint.position_;
						FVector clampedVector = clampedPosition - currentWaypoint.position_;

						if (lookAheadVector.SizeSquared() > 0.0f)
							newWaypoint.position_ = currentWaypoint.position_ + clampedVector.ProjectOnTo(lookAheadVector);
						else
							newWaypoint.position_ = currentWaypoint.position_;

						newWaypoint.position_ = FilterUtilityFunctions::clamp(newWaypoint.position_,
							nextInput.position_ - nextInput.positionError_,
							nextInput.position_ + nextInput.positionError_);
					}
				}

				break;
			}
		}
	}
	else
	{
		// In the event there is no more input data, stand still for one frame.
		//newWaypoint = nextWaypoint_;
		//newWaypoint.time_ = time;

		// 总是使用当前帧的数据，以避免在同一个tick下收到多个相同数据包时导致坐标与服务器的不一致的问题
		// 因为KBE在移动结束后不会继续发送数据包过来
		const StoredInput & topInput = this->getStoredInput(0);
		newWaypoint.spaceID_ = topInput.spaceID_;
		newWaypoint.vehicleID_ = topInput.vehicleID_;
		newWaypoint.position_ = topInput.position_;
		newWaypoint.direction_ = topInput.direction_;
		newWaypoint.storedInput_ = topInput;
		newWaypoint.time_ = time;

	}

	previousWaypoint_ = currentWaypoint;
	nextWaypoint_ = newWaypoint;
}

SmoothFilter::StoredInput & SmoothFilter::getStoredInput(uint32 index)
{
	KBE_ASSERT(index < NUM_STORED_INPUTS);

	return storedInputs_[(currentInputIndex_ + index) % NUM_STORED_INPUTS];
}

const SmoothFilter::StoredInput & SmoothFilter::getStoredInput(uint32 index) const
{
	return const_cast<SmoothFilter*>(this)->getStoredInput(index);
}

bool SmoothFilter::getLastInput(double & time, int32& spaceID, int32& vehicleID, FVector& pos, FVector& posError, FVector& direction)
{
	if (!reset_)
	{
		const StoredInput & storedInput = this->getStoredInput(0);
		time = storedInput.time_;
		spaceID = storedInput.spaceID_;
		vehicleID = storedInput.vehicleID_;
		pos = storedInput.position_;
		direction = storedInput.direction_;
		return true;
	}
	return false;
}




void UAvatarFilterActorComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);

	SpeedChangedNotify(0);
}

void UAvatarFilterActorComponent::ResetComponent()
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());

	if (IsValid(ServerActor))
	{
		vLastPos = ServerActor->GetActorLocation();
		mLastYaw = ServerActor->GetActorRotation().Yaw;
		FVector dir = ServerActor->GetActorRotation().Euler();
		FVector pos = ServerActor->GetActorLocation();
		KBEngine::Entity* parentEntity = nullptr;
		KBEngine::Entity* entity = ServerActor->GetSelfEntity();

		if (entity)
		{
			parentEntity = entity->Parent();

			if (parentEntity)
			{
				//pos = parentEntity->PositionWorldToLocal(pos);
				//dir = parentEntity->DirectionWorldToLocal(dir);
				pos = entity->LocalPosition();
				dir = entity->LocalDirection();
			}

			mFilter.reset(GetWorld()->GetTimeSeconds());
			int32 vehicleID = entity ? entity->ParentID() : 0;
			mFilter.input(GetWorld()->GetTimeSeconds() - 0.1, 0, vehicleID, pos, FVector::ZeroVector, dir);
		}
	}
}

bool UAvatarFilterActorComponent::IsMoving()
{
	return mLastSpeed > 0.01;
}

void UAvatarFilterActorComponent::InitFilter(bool IsActiveTickEnabled /*= true*/)
{
	mFilter.owner(this);
	Super::InitFilter(IsActiveTickEnabled);
	ResetComponent();//初始化重置组件写入数据，避免在移动平台克隆怪物的时候，会设置父亲，那时候Actor和组件都没有创建，没有写入数据，移动平台移动通知孩子，孩子没数据表现就不对
}

void UAvatarFilterActorComponent::SimulateMovement(float DeltaTime)
{
	SCOPE_CYCLE_COUNTER(STAT_AvatarFilterSimulateMovement);
	if (!bCanFilterTick)
	{
		return;
	}

	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());

	if (IsValid(ServerActor))
	{
		auto *pEntity = ServerActor->GetSelfEntity();

		if (nullptr == pEntity || !((GameObject*)pEntity)->IsSyncServerPos())
		{
			CS3_Warning(TEXT("-->Null Pointer error:UAvatarFilterActorComponent::TickComponent: pEntity|| ((GameObject*)pEntity)->IsSyncServerPos()!"));
			return;
		}
		float time = GetWorld()->GetTimeSeconds();
		mFilter.output(time);
	}
}

void UAvatarFilterActorComponent::OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID)
{
	int sceneID = 0;
	int vehicleID = parentID;

	float time = GetWorld()->GetTimeSeconds();
	bCanFilterTick = true;
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());
	if (!IsValid(ServerActor)) return;
	KBEngine::Entity *entity = ServerActor->GetSelfEntity();
	if (entity == nullptr) return;
	FVector newPos = position;
	if (entity->IsOnGround())//navigate移动是在地面上，不会发高度值，Z值用Actor的高度,怪物Filter是写入数据在下一帧执行位移
	{
		FVector LocalPosition;
		if (entity->ParentID() > 0 && entity->Parent() != nullptr && entity->Parent()->Actor())
		{
			LocalPosition = entity->Parent()->PositionWorldToLocal(ServerActor->GetActorLocation());
		}
		else
		{
			LocalPosition = ServerActor->GetActorLocation();
		}
		newPos.Z = LocalPosition.Z;
	}
	mFilter.input(time, sceneID, vehicleID, newPos, FVector::ZeroVector, direction);
}

void UAvatarFilterActorComponent::SetPosition(const FVector& position, int32 parentID)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAvatarFilterActorComponent::SetPosition(), %d - %d, position (%f, %f, %f)"),
	//	GameObjComponent()->entity()->ID(), parentID,
	//	position.X, position.Y, position.Z);
	double time = GetWorld()->GetTimeSeconds();
	int32 topSID;
	int32 topVID;
	FVector topPos = position;
	FVector topDir = GetOwner()->GetActorRotation().Euler();
	FVector topErr = FVector::ZeroVector;

	mFilter.getLastInput(time, topSID, topVID, topPos, topErr, topDir);
	mFilter.reset(GetWorld()->GetTimeSeconds());
	bCanFilterTick = true;
	mFilter.input(GetWorld()->GetTimeSeconds(), topSID, topVID, position, topErr, topDir);
}

void UAvatarFilterActorComponent::SetDirection(const FVector& direction, int32 parentID)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAvatarFilterActorComponent::SetDirection(), %d - %d, direction (%f, %f, %f)"),
	//	GameObjComponent()->entity()->ID(), parentID,
	//	direction.X, direction.Y, direction.Z);
	
	double time = GetWorld()->GetTimeSeconds();
	int32 topSID;
	int32 topVID;
	FVector topPos = GetOwner()->GetActorLocation();
	FVector topDir = direction;
	FVector topErr = FVector::ZeroVector;

	mFilter.getLastInput(time, topSID, topVID, topPos, topErr, topDir);
	mFilter.reset(GetWorld()->GetTimeSeconds());
	bCanFilterTick = true;
	mFilter.input(GetWorld()->GetTimeSeconds(), topSID, topVID, topPos, topErr, direction);
}

void UAvatarFilterActorComponent::SpeedChangedNotify(float speed)
{
	Super::SpeedChangedNotify(speed);

	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());

	if (IsValid(ServerActor))
	{
		ServerActor->OnFilterSpeedChanged(speed);
	}
}

void UAvatarFilterActorComponent::UpdateMoveSpeed(const FVector& position, const FVector& direction, const FVector& velocity)
{
	SCOPE_CYCLE_COUNTER(STAT_AvatarFilterUpdateMoveSpeed);

	mVelocity = velocity;
	float newSpeed = mVelocity.Size();
	if (newSpeed > 0.01)
	{
		SpeedChangedNotify(newSpeed);
	}
	else if (mLastSpeed <= 0.01 && newSpeed <= 0.01)
	{
		SpeedChangedNotify(0);
	}

	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());
	if (!IsValid(ServerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAvatarFilterActorComponent::Pos : ServerActor!"));
		return;
	}
	KBEngine::Entity *entity = ServerActor->GetSelfEntity();
	if (!entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAvatarFilterActorComponent::Pos : entity!"));
		return;
	}

	float YawChangedValue = abs(mLastYaw - ServerActor->GetActorRotation().Yaw);

	bool isNotDirChange = (YawChangedValue < 2.0 );	//表示转动是否大于 2度

	bool isNotPosChange = (abs(UKismetMathLibrary::Vector_Distance(ServerActor->GetActorLocation(),vLastPos)) < 10.0);		//10 厘米

	if (isNotDirChange && isNotPosChange && mLastSpeed <= 0.01 && newSpeed <= 0.01)
	{
		bCanFilterTick = false;
		return;
	}

	entity->SyncAndNotifyVolatileDataToChildren(false);
	vLastPos = position;
	mLastYaw = ServerActor->GetActorRotation().Yaw;
	mLastSpeed = newSpeed;
}

void UAvatarFilterActorComponent::Pos(const int32 vehicleID, const FVector& position, const FVector& direction, const FVector& velocity)
{
	SCOPE_CYCLE_COUNTER(STAT_AvatarFilterPos);
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetOwner());
	if (!IsValid(ServerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAvatarFilterActorComponent::Pos : ServerActor!"));
		return;
	}
	KBEngine::Entity *entity = ServerActor->GetSelfEntity();
	if (!entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAvatarFilterActorComponent::Pos : entity!"));
		return;
	}
	
	FVector newPos;
	FVector newDir;
	bool IsValidData = GetPositionAndDirection(position, direction, vehicleID, newPos, newDir);
	if (!IsValidData) return;
	
	//一种客户端actor需要始终面向目标的功能（在客户端模拟）
	UCombatInterface* CombatIns = ServerActor->GetEntityInterface_Cache().CombatInterface;
	UStateInterface* StateIns = ServerActor->GetEntityInterface_Cache().StateInterface;
	if (IsValid(CombatIns))
	{
		int32 tid;
		tid = CombatIns->GetWalkAroundTargetID();
		if (tid != 0 && StateIns->CurrentState == int(ENTITY_STATE::EntityStateFight) )
		{
			if (UUECS3GameInstance::pKBEApp == nullptr)
			{
				return;
			}
			KBEngine::Entity* en = UUECS3GameInstance::pKBEApp->FindEntity(tid);
			if (en != nullptr)
			{
				GameObject* TargetEntity = (GameObject*)(en);
				if (TargetEntity != nullptr)
				{
					AActor* TargetActor = TargetEntity->Actor();
					if (IsValid(TargetActor))
					{
						FVector tpos = TargetActor->GetActorLocation();
						FVector dir = tpos - newPos;
						float yaw = 0.0f;
						yaw = FMath::Atan2(dir.Y, dir.X);
						newDir = FVector(0.0, 0.0, FMath::RadiansToDegrees(yaw));
					}
				}
			}
		}
	}

	//设置位置
	SafeMove(newPos, newDir, true);
	//更新移动速度
	UpdateMoveSpeed(newPos, newDir, velocity);
}

void UAvatarFilterActorComponent::SetPosBySerPos(const int32 vehicleID, const FVector& position, const FVector& direction)
{
	Pos(vehicleID, position, direction,FVector::ZeroVector);
}

void UAvatarFilterActorComponent::SetSmoothFilterLatencyFrames(float LatencyFrame)
{
	mFilter.s_latencyFrames_ = LatencyFrame;
}

void UAvatarFilterActorComponent::OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID)
{
	if (IsActive())
	{
		float time = GetWorld()->GetTimeSeconds();
		mFilter.output(time);
	}
}

void UAvatarFilterActorComponent::OnGotParentEntity(KBEngine::Entity* parentEnt)
{
// 	if (parentEnt != nullptr)
// 	{
// 		GameObject* GameEntity = (GameObject *)(parentEnt);
// 		if (GameEntity != nullptr)
// 		{
// 			AServerCharacter* ParentCharacter = (AServerCharacter *)GameEntity->Actor();
// 			if (IsValid(ParentCharacter))
// 			{
// 				UFilterActorComponent* ParentFilterCom = ParentCharacter->GetFilterComponent();
// 				if (IsValid(ParentFilterCom))
// 				{
// 					PrimaryComponentTick.AddPrerequisite(ParentFilterCom, ParentFilterCom->PrimaryComponentTick);
// 
// 				}
// 				ResetComponent();
// 			}
// 		}
// 	}

	ResetComponent();
}

void UAvatarFilterActorComponent::OnLoseParentEntity()
{
	ResetComponent();
}

CONTROL_COMPILE_OPTIMIZE_END
