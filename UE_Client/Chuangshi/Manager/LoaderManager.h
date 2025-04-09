#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameData/CS3Object.h"
#include "CS3Base/GameObject.h"
#include "LoaderManager.generated.h"

/*
* 文件名称：LoaderManager.h
* 功能说明：加载管理器
* 文件作者：shenbing
* 目前维护：huting
* 创建时间：2017/03/27
*/

/**
*加载回调
*/
DECLARE_DYNAMIC_DELEGATE(FEndLoadCallBack);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FBB);
DECLARE_DELEGATE_OneParam(FSLoadCallBack, float);
DECLARE_DELEGATE_OneParam(FTLoadCallBack, float);
DECLARE_MULTICAST_DELEGATE_OneParam(FLoadDelegate,FSLoadCallBack);

#pragma region 检测类及其扩展 : UBaseLoader
/**
*加载基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBaseDetect : public UCS3Object, public FTickableGameObject
{
	GENERATED_BODY()

public:
	UBaseDetect();	///<构造函数
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void StartDetect(FSLoadCallBack SCallBack);
	virtual void OnDetect(FSLoadCallBack SCallBack);	///<检测加载进度
	virtual void FinishDetect();	///<取消当前加载
	virtual void Tick(float DeltaTime) override {}
	virtual bool IsTickable() const override { return (!GWorld->HasBegunPlay() && GIsEditor) ? false : true; }
	virtual TStatId GetStatId() const override { RETURN_QUICK_DECLARE_CYCLE_STAT(UBaseDetect, STATGROUP_Tickables); }

	virtual void BeginDestroy()override;
public:
	FTimerHandle TimeoutTimer;					///<超时Timer
	FTimerHandle DetectTimer;					///<检测Timer
	float CProgress = 0.0f;
	float TimeoutTime = 0.0f;					///<超时时间
};

/**
*镜头、媒体等多个资源检测基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAssetDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void StartDetect(FSLoadCallBack SCallBack) override;
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度
	virtual void FinishDetect() override;	///<取消当前加载	
	virtual void LoadAssetFinished();						///<单个资源加载完成
	virtual void ResetData();
public:
	int32 Count = 0;						///<资源加载数量
	int32 CurCount = 0;					///<已加载的资源数量
	float SDProgress = 0.0f;					///<单个资源加载进度
	bool bIsLoadAssetFinished = false;		///<资源是否加载完成
};


/**
*镜头资源检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UStoryDetect : public UAssetDetect
{
	GENERATED_BODY()

public:

	virtual void StartDetect(FSLoadCallBack SCallBack) override;
	
};

/**
*媒体资源检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMediaDetect : public UAssetDetect
{
	GENERATED_BODY()

public:
	virtual void StartDetect(FSLoadCallBack SCallBack) override;
};

/**
*角色选择进入到游戏场景检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UWorldSceneDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void StartDetect(FSLoadCallBack SCallBack) override;
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度
	virtual void FinishDetect() override;	///<取消当前加载	
};

/**
*如登录，角色选择，创建阵营，创建角色等关卡资源加载检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API ULoginSceneDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度	
};

/**
*角色加载检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UPlayerCharacterDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void StartDetect(FSLoadCallBack SCallBack) override;
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度
	virtual void FinishDetect() override;	///<取消当前加载
};

/**
*界面资源加载检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UGuisDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度	
};

/**
*配置资源加载检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConfigDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度	
};

/**
*配置资源加载检测
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UParticleDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度	
};

/**
*视频是否已播放最小时间检测 CST-12205
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UPlayMediaDetect : public UBaseDetect
{
	GENERATED_BODY()

public:
	virtual void OnDetect(FSLoadCallBack SCallBack) override;	///<检测加载进度	
	virtual void FinishDetect() override;	///<取消当前加载	
};
#pragma endregion


#pragma region 加载类及其扩展 : UBaseLoader
/**
*加载基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBaseLoader : public UCS3Object, public FTickableGameObject
{
	GENERATED_BODY()

public:
	UBaseLoader();	///<构造函数
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack);
	virtual void Detect();	///<检测加载进度
	virtual void Cancel();	///<取消当前加载
	virtual void BeginDestroy()override;
	virtual void Tick(float DeltaTime) override {}
	//virtual bool IsTickableWhenPaused() const override { return true; }
	virtual bool IsTickable() const override { return (!GWorld->HasBegunPlay() && GIsEditor) ? false : true; }
	virtual TStatId GetStatId() const override { RETURN_QUICK_DECLARE_CYCLE_STAT(UBaseLoader, STATGROUP_Tickables); }

public:
	float CProgress = 0.0f;						///<当前加载进度
	float TotalProgress;						///<加载总进度
	FTimerHandle LoadTimer;						///<循环侦测Timer
	FTLoadCallBack TLoadCallBack;				///<加载回调
	FLoadDelegate CurrLoadDetector;				///<当前加载任务
	TArray<float> LoadProgressList;				///<加载进度列表
	TArray<FLoadDelegate> LoadDetectorList;		///<加载任务列表
};

/**
*进入账号登录加载类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API ULoginLoader : public UBaseLoader
{
	GENERATED_BODY()

public:
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack) override;
	virtual void Detect() override;	///<检测加载进度
	virtual void Cancel() override;	///<取消当前加载

protected:
	/**
	*场景加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void SceneDetect(FSLoadCallBack SCallBack);
public:
	UPROPERTY()
		ULoginSceneDetect* LoginSceneDetector;
};

/**
*进入阵营选择加载类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCampLoader : public UBaseLoader
{
	GENERATED_BODY()

public:
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack) override;
	virtual void Detect() override;	///<检测加载进度
	virtual void Cancel() override;	///<取消当前加载

protected:
	/**
	*场景加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void SceneDetect(FSLoadCallBack SCallBack);
public:
	UPROPERTY()
		ULoginSceneDetect* LoginSceneDetector;
};

/**
*进入角色创建加载类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCreatorLoader : public UBaseLoader
{
	GENERATED_BODY()

public:
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack) override;
	virtual void Detect() override;	///<检测加载进度
	virtual void Cancel() override;	///<取消当前加载

protected:
	/**
	*场景加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void SceneDetect(FSLoadCallBack SCallBack);
public:
	UPROPERTY()
		ULoginSceneDetect* LoginSceneDetector;
};

/**
*进入角色选择加载类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USelectorLoader : public UBaseLoader
{
	GENERATED_BODY()

public:
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack) override;
	virtual void Detect() override;	///<检测加载进度
	virtual void Cancel() override;	///<取消当前加载

protected:
	/**
	*场景加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void SceneDetect(FSLoadCallBack SCallBack);
public:
	UPROPERTY()
		ULoginSceneDetect* LoginSceneDetector;
};

/**
*进入游戏世界加载类,从角色选择进入到游戏
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UWorldLoader : public UBaseLoader
{
	GENERATED_BODY()

public:
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack) override;
	virtual void Detect() override;	///<检测加载进度
	virtual void Cancel() override;	///<取消当前加载
protected:
	/**
	*配置加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void ConfigDetect(FSLoadCallBack SCallBack);
	/**
	*UI加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void GuisDetect(FSLoadCallBack SCallBack);
	/**
	*场景加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void SceneDetect(FSLoadCallBack SCallBack);
	/**
	*镜头加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void StoryDetect(FSLoadCallBack SCallBack);
	/**
	*媒体加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void MediaDetect(FSLoadCallBack SCallBack);
	
	/**
	*玩家加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void PlayerCharacterDetect(FSLoadCallBack SCallBack);
public:
	UPROPERTY()
	UWorldSceneDetect* SceneDetector;				///<场景资源加载
	UPROPERTY()
	UStoryDetect* StoryDetector;					///<镜头资源检测器	
	UPROPERTY()
	UPlayerCharacterDetect*  PlayerCharacterDetector;///<角色资源检测器
	UPROPERTY()
	UMediaDetect* MediaDetector;					///<媒体资源检测器
};

/**
*进入地图传送加载类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTeleportLoader : public UBaseLoader
{
	GENERATED_BODY()

public:
	/**
	*正式进入加载
	*
	*@param TCallBack 加载回调
	*
	*@return 无
	*/
	virtual void Run(FTLoadCallBack TCallBack) override;
	virtual void Detect() override;	///<检测加载进度
	virtual void Cancel() override;	///<取消当前加载

protected:
	/**
	*场景加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void SceneDetect(FSLoadCallBack SCallBack);
	/**
	*镜头加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void StoryDetect(FSLoadCallBack SCallBack);
	/**
	*媒体加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void MediaDetect(FSLoadCallBack SCallBack);
	/**
	*玩家加载检测
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void PlayerCharacterDetect(FSLoadCallBack SCallBack);
	/**
	*媒体播放检测器
	*
	*@param SCallBack 加载回调
	*
	*@return 无
	*/
	void PlayMediaDetect(FSLoadCallBack SCallBack);
public:
	UPROPERTY()
		UWorldSceneDetect* SceneDetector;				///<场景资源检测器
	UPROPERTY()
		UStoryDetect* StoryDetector;					///<镜头资源检测器
	UPROPERTY()
		UPlayerCharacterDetect*  PlayerCharacterDetector;///<角色资源检测器
	UPROPERTY()
		UMediaDetect* MediaDetector;					///<媒体资源检测器
	UPROPERTY()
		UPlayMediaDetect* PlayMediaDetector;			///<媒体播放检测器
	
};

#pragma endregion


#pragma region 加载管理类 : UGLoaderManager

UCLASS(Blueprintable)
class CHUANGSHI_API UGLoaderManager : public UCS3Object
{
	GENERATED_BODY()

public:
	UGLoaderManager();	///<构造函数
	~UGLoaderManager();	///<析沟函数

	static UGLoaderManager *GetInstance();
	void PostInitProperties() override;

	/**
	*BlueprintImplementableEvent,进度改变回调
	*
	*@param Progress 加载进度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "LoaderManager")
		void OnProgressNotify(float Progress);


	void LoadLoginSpace(FEndLoadCallBack EndCallBack);		///<进入账号登录


	void LoadCampSpace(FEndLoadCallBack EndCallBack);		///<进入阵营选择


	void LoadCreatorSpace(FEndLoadCallBack EndCallBack);	///<进入角色创建


	void LoadSelectorSpace(FEndLoadCallBack EndCallBack);	///<进入角色选择


	void LoadWorldSpace(FEndLoadCallBack EndCallBack);		///<进入游戏世界


	void LoadTeleportSpace(FEndLoadCallBack EndCallBack);	///<进入传送地图


	bool IsLoading() { return IsValid(CurrLoader); };
private:

	UPROPERTY()
		UBaseLoader* LoginLoader;		///<账号登录加载器
	UPROPERTY()
		UBaseLoader* CampLoader;		///<阵营选择加载器
	UPROPERTY()
		UBaseLoader* CreatorLoader;	///<角色创建加载器
	UPROPERTY()
		UBaseLoader* SelectorLoader;	///<角色选择加载器
	UPROPERTY()
		UBaseLoader* WorldLoader;		///<游戏世界加载器
	UPROPERTY()
		UBaseLoader* TeleportLoader;	///<传送地图加载器

	UPROPERTY()
		UBaseLoader* CurrLoader;		///<当前活动的加载器
/*
private:
	static UGLoaderManager* Instance;*/
};


#pragma endregion