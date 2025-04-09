#pragma once

#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "Flock.generated.h"

/*
* 文件名称：Flock.h
* 功能说明：鸟群等活动类场景物件
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2017-05-18
*/

class UArrowComponent;

UCLASS(BlueprintType)
class CHUANGSHI_API AFlock : public AActor
{
	GENERATED_BODY()
	 
public:	
	/// Sets default values for this actor's properties
	AFlock();

	/// Called when the game starts or when spawned
	virtual void BeginPlay() override;
	
	/// Called every frame
	virtual void Tick( float DeltaSeconds ) override;

	virtual void Destroyed() override;

	virtual bool ShouldTickIfViewportsOnly() const override;///< 在world不启动的时候也可以每帧Tick
	
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	UAnimSequence* AnimFly;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	UAnimSequence* AnimLand;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	UAnimSequence* AnimRandom;	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	USkeletalMesh* SKMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	FVector MaxCubeRange;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
		float FlySpeed;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
		float UpSpeed;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	int Index;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	float DistanceInterval;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
	FVector Offset;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
		int32 InitialPos;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (ExposeOnSpawn = true))
		float DistanceToHide= 2000.0f;
	
	FVector CenterPosition;
	USceneComponent* DefaultSceneRoot;
	UArrowComponent* FlockBase;
	USkeletalMeshComponent* Mesh;
	
	FVector2D LandTimeRange = FVector2D(8, 15);

	// 玩家摄像机
	APlayerCameraManager* CurrentPlayerCamera;

	// 每帧的间隔
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock")
	float FlockTickInterval;

protected:
	// 求椭圆上一点
	FVector2D GetEllipseLocation(float Angle, float A, float B);
	// 求某一点的斜率，返回角度作为飞行方向
	float GetEllipsePointSlope(float x, float y, float A, float B, float Theta);
	// 控制角度范围-180~180
	void MakeAngleInRange(float& Angle);
	// 求圆外一点P与椭圆切线的交点
	void GetEllipseTangentPoint(float x, float y, float A, float B);

	void MoveEvent();

	void Fly();
	void Land();
	void LandRandom();
	void RestToFly();

	// 获取当前玩家的摄像机的位置
	void GetCharCamera();
	// 设置每帧的间隔
	void UpdateTickInterval();



private:

	float EllipseA;		//椭圆顶点
	float EllipseB;
	float CurrPlaneAngle;//椭圆上一点和中心点连线的与X轴的角度
	float CurrZAngle;	// 用于计算Z轴方向上的偏移坐标
	float Speed;
	float LandTime;

	bool IsFly;
	bool IsRandom;
	bool bIsMove;

	// 鱼群和玩家的距离
	UPROPERTY(EditAnywhere, Category = "Flock")
	FVector FlockToCharacter;

};
