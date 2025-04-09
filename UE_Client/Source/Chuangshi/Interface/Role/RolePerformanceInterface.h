#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/CrossMapConfigData.h"
#include "GameData/SpaceHunTingData.h"
#include "GameData/SpaceYeZhanFengQiData.h"
#include "GameData/VoiceData.h"
#include "GameData/SGMZMatchData.h"
#include "RolePerformanceInterface.generated.h"

/*
* 文件名称：RolePerformanceInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：all
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URolePerformanceInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URolePerformanceInterface();
	~URolePerformanceInterface();
	
	static FString GetName() { return TEXT("RolePerformanceInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RolePerformanceInterface.BP_RolePerformanceInterface_C'"); } //获取蓝图对象路径

	virtual void OnEnterScenes() override;
	UPROPERTY(BlueprintReadWrite)
		AActor* TalkingTarget = nullptr;
	TArray<FVOICE_PLAY_DATA> VoicePlayDataList;

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> SGMZFinishedStage; //上古密阵进度信息

	int32 PrompetItemID = 0, PrompetskillID = 0;//屏幕中央技能、物品


	/** Id:	服务器发送编号(或链表),首字母:A:AI, Q:任务,对应VoiceData->Id J:镜头 */

	/**
	*Define method
	*BlueprintCallable，调用客户端显示界面内容并播放语音
	*
	*@param Ids ，语音ID（const FString&）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void ShowMessagePlaySound(const FString& Ids);

	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void PlayNext();
	void PlaySoundsAndStorys();

	/**
	*Define method
	*BlueprintImplementableEvent，玩家显示副本剩余时间
	*
	*@param EndTime ，结束时间（FString）
	*@param isMoveDown,是否将结束时间往下移
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowSpaceLife(const FString& EndTime,const int32& isMoveDown,const FString& CurTime );

	/**
	*Define method
	*BlueprintImplementableEvent，停止显示副本剩余时间
	*
	*@param RemainTime ，剩余时间（int32）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowStopSpaceLife(int32 RemainTime);

	/**
	*Define method
	*BlueprintImplementableEvent，隐藏副本剩余时间
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void HideSpaceLife();

	/**
	*Define method
	*BlueprintCallable，开始变身
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnChangeBodyStart();

	/**
	*Define method
	*BlueprintCallable，结束变身
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnChangeBodyEnd();

	/**
	*Define method
	*BlueprintCallable，心魔附身开始
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void onXinMoCtrlStart(const TArray<int32>& ExcludeSkillList, const TArray<int32>& ActForbidList);

	/**
	*Define method
	*BlueprintCallable，心魔附身结束
	*
	*
	*@return 无
	*/

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void onXinMoCtrlEnd();

	/**
	*Define method
	*BlueprintCallable,开始陷阱持有效果:吸力
	*
	*@param SuckPos(FVector)
	*@param SuckSpeed(float)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnBeginTrapSuck(const FVector& SuckPos, const float SuckSpeed);

	/**
	*Define method
	*BlueprintCallable,结束陷阱持有效果:吸力
	*
	*@param SuckPos
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnEndTrapSuck();

	/**
	*Define method
	*BlueprintImplementableEvent，打开宝箱的提示信息
	*
	*@param type  类型 （获得物品，获得经验等）
	*@param value 值，(经验值，物品id等)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowSpellBoxResultMessage(const int32& type, const int32& vlue);

	/**
	*Define method
	*BlueprintCallable，使用物品/技能提示
	*
	*@param PromptID  物品ID（或技能ID）
	*@param PromptTip 使用提示
	*@param OffsetPos 界面偏移量（ -10|10，表示界面居中向左偏移10%向下偏移10%。如果不配，在原位置）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowPrompetOper(const int32& PromptID, const FString& PromptTip, const FString& OffsetPos);

	/**
	*BlueprintImplementableEvent，使用物品/技能提示，通知蓝图
	*
	*@param type  类型（0 物品，1 技能）
	*@param PromptID id（物品id，技能id）
	*@param PromptTip 文字提示
	*@param OffsetPos 界面偏移量（ -10|10，表示界面居中向左偏移10%向下偏移10%。如果不配，在原位置）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RolePerformanceInterface")
		void OnShowPrompetOper(const int32& type, const int32& PromptID, const FString& PromptTip, const FString& OffsetPos);

	/**
	*Define method
	*BlueprintCallable，提示结束
	*
	*@return 无
	*/

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void HidePrompetOper();

	/**
	*BlueprintImplementableEvent，使用物品/技能提示结束，通知蓝图
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RolePerformanceInterface")
		void OnHidePrompetOper();

	/**
	*Define method
	*BlueprintCallable，开始猜大小游戏
	*
	*@param progress ，猜对次数
	*@param initMsg ，语音ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void StartGuessGame(const int32& progress, const FString& initMsg);

	/**
	*Define method
	*BlueprintCallable，游戏结果：猜对
	*
	*@param roll ，骰子roll的点数
	*@param winMsg ，语音ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void RightGuess( const FString& winMsg);

	/**
	*Define method
	*BlueprintCallable，游戏结果：猜错
	*
	*@param roll ，骰子roll的点数
	*@param lostMsg ，语音ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void WrongGuess(const FString& lostMsg);

	/**
	*Define method
	*BlueprintCallable，完成猜大小游戏
	*
	*@param roll ，骰子roll的点数
	*@param finishMsg ，语音ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void FinishGuess(const FString& finishMsg);

	/**
	*BlueprintCallable,副本通关结束，客户端请求服务器开宝箱
	*
	*@param BoxIndex 宝箱索引（0-5）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void RequestOpenSpaceSettlementRewdBox(const int32 BoxIndex);

	/**
	*Define method
	*BlueprintCallable,显示某装备耐久度的特殊界面 见JIRA CST-2149
	*
	*@param itemUid 物品uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowEquipHardiness(const FString& itemUid);

	/**
	*BlueprintCallable,通知界面显示某装备耐久度的特殊界面 见JIRA CST-2149
	*
	*@param Hardiness 装备耐久度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RolePerformanceInterface")
		void OnShowEquipHardiness(int32 Hardiness);
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void StartHLDRound();

	/**
	*Define method
	*BlueprintCallable，抱起幻兽
	*
	*@param roll ，骰子roll的点数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void HoldPet(const FString& AttachMeshID);

	/**
	*Define method
	*BlueprintCallable，放下幻兽
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void DownPet(const FString& AttachMeshID);

	/**
	*Define method
	*BlueprintNativeEvent，进入瞄准状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void EnterAimStatus();

	/**
	*Define method
	*BlueprintNativeEvent，退出瞄准状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void LeaveAimStatus();

	/**
	*Define method
	*BlueprintNativeEvent，进入瞄准状态(CST-4369:天之幻境副本)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void EnterShootModel();

	/**
	*Define method
	*BlueprintNativeEvent，退出瞄准状态(CST-4369:天之幻境副本)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void LeaveShootModel();

	/**
	*Define method
	*BlueprintNativeEvent，进入飞行状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void EnterFlyModel();

	/**
	*Define method
	*BlueprintNativeEvent，退出飞行状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void LeaveFlyModel();

	/**
	*Define method
	*BlueprintNativeEvent，抱起组件
	*
	*@param HoldModelId ，金丹模型ID
	@param buffRemainTime ，buff持续时间
	*@param TimerInterval 倒计时回调时间间隔
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void HoldJinDan(const FString& AttachMeshID, float buffRemainTime, float TimerInterval);

	/**
	*Define method
	*BlueprintNativeEvent，放下组件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void DownJinDan(const FString& AttachMeshID);

	/**
	*Define method
	*BlueprintNativeEvent，显示“放下金丹”按钮
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowPutDownJinDanBtn();

	/**
	*Define method
	*BlueprintNativeEvent，隐藏“放下金丹”按钮
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void HidePutDownJinDanBtn();

	/**
	*Define Method
	*BlueprintNativeEvent,在指定Actor播放光效
	*
	*@param entityID
	*@param effectID 光效ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void PlayBindEffect(const int32& targetID, const FString& effectID);

	/**
	*Define Method
	*BlueprintNativeEvent,停止播放光效
	*
	*@param entityID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void EndPlayBindEffect(const int32& targetID);

	/**
	*Define Method
	*BlueprintNativeEvent,开始混乱表现
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void onBeginConfusion();

	/**
	*Define Method
	*BlueprintNativeEvent,结束混乱表现
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void onEndConfusion();
	
	/**
	*
	*BlueprintCallable，开始穿越峡谷
	*
	*@param ForwardForceSpeed 前进的速度
	*@param DownForceSpeed 下落的速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void OnStartThroughCanyon(const FString& MountModelId, const float& ForwardForceSpeed, const float& DownForceSpeed);

	/**
	*
	*BlueprintCallable，离开穿越峡谷
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void OnEndThroughCanyon();

	/**
	* BlueprintCallable,添加冲刺力(冲刺技能支持)
	*
	*@param Dire	力的方向
	*@param ForceSpeed 力的速度
	*@param ForceTime 力持续的时间
	*
	* @return 这个力的ID
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
	int32 AddFlyForce(int Dire, float ForceSpeed, float ForceTime);

	//同地图传送事件回调
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RolePerformanceInterface")
	void OnGoToSameLevel();

	/**
	*OnStoryPlayEnd
	* @brief 预加载剧情播放结束回调
	* @return void
	*/
	void OnStoryPlayEnd();

	/**
	*OnLoadSpaceCompleted
	* @brief space加载完成回调
	* @param bool IsFirst
	* @return void
	*/
	void OnLoadSpaceCompleted(bool IsFirst);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RolePerformanceInterface")
	void OnLoadSpaceCompletedBP();

	void SetCrossMapTargetInfo(TArray<FCROSS_MAP_TARGET_INFO>& CrossMapInfos);
	TArray<FCROSS_MAP_TARGET_INFO> GetCrossMapTargetInfo();

	FCROSS_MAP_QUEST_TARGET_INFO GetCurrentMapTargetInfo();

	void SetCurrentMapTargetInfo(FCROSS_MAP_TARGET_INFO& MapTargetInfo, bool IsCompletedQuest, FString QuestTaskClass, int AutoQuestID = 0, int32 GossipWithType = 0);

	void ClearTargetInfo();

	/**
	*StartPerformCrossMapNavigate
	* @brief 开始表现跨地图寻路
	* @param TArray<FCROSS_MAP_TARGET_INFO>& CrossMapInfos 跨地图寻路信息
	* @param FString DstSpaceName	目标地图，可以为空，为空表示当前地图
	* @param bool IsCompletedQuest	是否是交任务行为，如果不是，那就是任务目标寻路
	* @param FString QuestTaskClass	任务目标的Class
	* @param FString NPCScriptID	NPC的ScriptID，如果是直接给位置，这个地方直接给一个""
	* @param const FVector& FinalPosition	直接给的任务寻路位置
	* @param float NearbyRange		靠近距离
	* @param int AutoQuestID		任务的ID
	* @return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void StartPerformCrossMapNavigate(TArray<FCROSS_MAP_TARGET_INFO>& CrossMapInfos, FString DstSpaceName, bool IsCompletedQuest, FString QuestTaskClass = "", FString NPCScriptID = "", FVector FinalPosition = FVector::ZeroVector, float NearbyRange = 2.0f, int AutoQuestID = 0, int32 GossipWithType = 0);

	void CrossMapNavigateHandle();

	void HandleCrossMapNavigate();

	//玩家寻路到目的地回调
	void OnNavigateArriveFinalSpace();

	//玩家停止寻路回调，一般是玩家主动停止寻路
	void OnNavigateStop();

	void SetNavigateActionType(ENUM_NAVIGATE_ACTION_TYPE Type);
	ENUM_NAVIGATE_ACTION_TYPE GetNavigateActionType() { return NavigateActionType; };

	virtual void InitBlueCB() override;


	/**
	*Define Method
	*BlueprintNativeEvent,进入MoveTrapByTrigger陷阱
	*@param trapID: Trap的entityID
	*@param speed Trap的行走速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void onStartMoveByMoveTrap(const int32& trapID, const float& speed);

	/**
	*Define Method
	*BlueprintNativeEvent,离开MoveTrapByTrigger陷阱，或者MoveTrapByTrigger陷阱停止移动
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void onStopMoveByMoveTrap();

	/**
	*Define Method
	*BlueprintNativeEvent,进入MoveTrapByTrigger陷阱
	*@param trapID: Trap的entityID
	*@param speed Trap的行走速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_AddTrapVortex(const int32 trapID, const float speed);

	/**
	*Define Method
	*BlueprintNativeEvent,离开MoveTrapByTrigger陷阱，或者MoveTrapByTrigger陷阱停止移动
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_RemoveTrapVortex(const int32 trapID);

	/**
	*Define Method
	*BlueprintNativeEvent,玩家变化视角，控制石板移动
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void GetMovingPlatFormControl();

	/**
	*Define Method
	*BlueprintNativeEvent,玩家结束变化视角，控制石板移动
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void LoseMovingPlatFormControl();

	/**
	*Define Method
	*BlueprintNativeEvent,附身功能中的镜头移动
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void RoleCameraMoveToEntity(int32 targetEntityID,const FString& effectID, float MoveTime, float DelayTime);

	/**
	*Define Method
	*BlueprintNativeEvent,镜头结束后摄像机回归玩家
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void RoleCameraMoveToEntityCB(const FString& effectID);

	/**
	*Define Method
	*BlueprintNativeEvent,灵魂出窍
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ExpelTheSoul(const int32& targetID,const FString& effectID, float delayDestroyTime);

	/**
	*Define Method
	*BlueprintNativeEvent,吸魂
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void AbsorbTheSoul(const int32& targetID);


	/**
	*Define Method
	*BlueprintNativeEvent,进入射击模式
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void EnterModelTPS();

	/**
	*Define Method
	*BlueprintNativeEvent,离开射击模式
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void LeaveModelTPS();
	/**
*Define Method
*BlueprintNativeEvent,进入射击模式
*
*@return 无
*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_EnterModelTPSParam(const FString& Param);

	/**
	*Define Method
	*BlueprintNativeEvent,离开射击模式
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_LeaveModelTPSParam();

	/**
	*Define Method
	*BlueprintNativeEvent,玩家头顶冒字
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ShowMessageUpPlayerHead(const int32& msgID);

	/**
	*Define Method
	*BlueprintNativeEvent,灵魂狩猎副本积分
	*isOpen 0:关闭界面 2：打开/更新界面
	*score :显示的分数
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void UpdateScoreForLHSL(int32 isOpen, int32 score);

	/**
	*Define Method
	*BlueprintNativeEvent,开启阻挡
	*
	*@param:number  编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OpenAreaWall(const FString& number);

	/**
	*Define Method
	*BlueprintNativeEvent,关闭阻挡
	*
	*@param:number  编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CloseAreaWall(const FString& number);

	//设置CurVoiceIds值
	void SetCurVoiceIds(FString VoiceIds) { CurVoiceIds = VoiceIds; };

	/**
	*Define Method
	*BlueprintNativeEvent,显示狂牛冲撞生存时间
	*
	*@param:totalSurverTime  总生存时间
	*@param:gradeList  生存时间奖励阶段
	*@param:expList  每个阶段对应的经验奖励
	*@param:moneyList  每个阶段对应的金钱奖励（可能为0，则不显示）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_showSurvivalTime(const int32& totalSurverTime, const TArray<int32>& gradeList , const TArray<int32>& expList, const TArray<int32>& moneyList);

	/**
	*Define Method
	*BlueprintNativeEvent,开始计时狂牛冲撞生存时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_startSurvivalTime();

	/**
	*Define Method
	*BlueprintNativeEvent,结束计时狂牛冲撞生存时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_endSurvivalTime(const int32& surverTime);

	/**
	*Define Method
	*BlueprintNativeEvent,夜袭凤栖镇镜头注视效果
	* targetID:目标ID
	*CameraTime：flaot（飞行时间），float（镜头停留时间） ，float（镜头飞回时间）
	.CameraTargetLotation：镜头目标位置偏移量（FVector 0|0|0）
	*CameraTargetRotator：镜头目标旋转偏移量（FVector 0|0|0）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CameraLookAtTarget(const int32& targetID, const FString& CameraTime, const FString& CameraTargetLotation, const FString& CameraTargetRotator);
protected:
#pragma region 飞行力相关

	/**
	* @brief 添加自动飞行力
	*
	* @return 这个力的ID
	*/

	void AddAutoFlyForce(float ForwardForceSpeed, float DownForceSpeed);

	/**
	* @brief 停止飞行力
	*
	* @return
	*/

	void StopFlyForce();

#pragma endregion
private:
	FString CurVoiceIds = TEXT("");
	//TArray<AEffectEmitter*> UnbindEffectArr;

	TArray<int32> UnbindEffectUID;

	//TMap<int32, AEffectEmitter*> BindEffectArr;

	TMap<int32, int32> BindEffectUID;

	TArray<int32> MoveTrapForceIDs;//移动触发力ID容器
	TMap<int32, int32> ClientTriggerTrapVortex;//旋涡脚本类型陷阱触发力ID容器

	TArray<FCROSS_MAP_TARGET_INFO> CrossMapTargetInfo;//跨地图寻路目标信息

	FCROSS_MAP_QUEST_TARGET_INFO CurrentMapQuestTargetInfo;//跨地图寻路当前地图目标信息

	FTimerHandle NavigateDataDoneHandle;

	FTimerHandle GlidingHandle;

	ENUM_NAVIGATE_ACTION_TYPE NavigateActionType;

	float PlayerCameraArmLength;

#pragma region 法宝相关
public:
	/**
	*Define Method
	*BlueprintNativeEvent,法宝播放动作，特效
	*
	*@param:targetID  目标ID
	*@param:playerID  玩家ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void FabaoPlayEffect( int32 targetID, int32 playerID, const FString& actionID,const FString& effectID, const FString& playTime);

	/**
	*Define Method
	*BlueprintNativeEvent,法宝播放动作，特效结束
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface") 
		void FabaoPlayEffectEnd();

	/**
	*Define Method
	*BlueprintNativeEvent,灵魂之誓 创建法宝
	*
	*@param:targetID  目标ID
	*@param:FaBaoID   法宝ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CreateFaBao(int32 playerID,const FString& FaoBaoID);

	/**
	*Define Method
	*BlueprintNativeEvent,灵魂之誓 删除法宝
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void RemoveFaBao();

	/**
	*Define Method
	*BlueprintNativeEvent,增加飞行绑定mesh
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_CreateAircraft(const FString&  FlybindmeshID,int32 TargetID);

	/**
	*Define Method
	*BlueprintNativeEvent,删除飞行绑定mesh
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_RemoveAircraft(int32 TargetID);

	/**
	*Define Method
	*BlueprintNativeEvent,使用飞行绑定mesh
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void AircraftUseSkill(int32 TargetID);

	/**
	*Define Method
	*BlueprintNativeEvent,青光剑飞向目标后，停留2s返回玩家
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_AircraftUseSkill(int32 CasterID, int32 TargetID);

	/**
	*Define Method
	*BlueprintNativeEvent,玩家震屏
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void RoleCameraShake(float intensity, float rate, float time ,int32 priority);

	/**
	*Define Method
	*BlueprintNativeEvent,嘲讽开始
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnTauntBegin();

	/**
	*Define Method
	*BlueprintNativeEvent,嘲讽结束
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnTauntEnd();

	/**
	*Define Method
	*BlueprintNativeEvent 镜头转向
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnSetViewTarget(int32 TargetID, const FString& DurationTimeStr /*= 0 0 0*/, float Range /*= 0.0f*/, const FString& StartViewRotatorStr /*= 0 0 0*/, const FString& TargetViewRotatorStr /*= 0 0 0*/, uint8 bIsResetPlayerCamera /*= true*/);

#pragma endregion
	/**
	*Define method
	*BlueprintNativeEvent，抱起组件
	*
	*@param HoldModelId ，金丹模型ID
	@param buffRemainTime ，buff持续时间
	*@param TimerInterval 倒计时回调时间间隔
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_ThrowJinDan(const FString& AttachMeshID, float buffRemainTime, float TimerInterval);

	/**
	*Define method
	*BlueprintNativeEvent，放下组件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_OnThrowJinDan(const FString& AttachMeshID);
	/**
	*Define Method
	*BlueprintNativeEvent,重置跳跃次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void CLIENT_ResetJump();
	/**
	*Define Method
	*BlueprintNativeEvent,添加透视对象（CST-7692）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_AddPerspectiveTarget(int32 targetID, float maxDist, float minDist, float maxHeigth);
	/**
	*Define Method
	*BlueprintNativeEvent,移除透视对象（CST-7692）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_RemovePerspectiveTarget(int32 targetID, float maxDist, float minDist, float maxHeigth);

	/**
	*Define Method
	*BlueprintNativeEvent,显示副本通关结算界面
	*@Param spaceType 副本类型
	*@Param rewardValue 奖励值
	*@Param spacetime 副本通关时间
	*@Param dieNumber 死亡总次数
	*@Param level 完成等级 1：入道 2：出尘 3：问鼎 4：超凡
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_ShowSpaceSettlementWin(const int32& spaceType,const int32& rewardValue,const int32& spacetime, const int32& dieNumber,const int32& level);

#pragma region 上古密阵
	/**
	*Define Method
	*BlueprintNativeEvent,显示副本结束对战信息
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
	void SGMZOnWinGame(const FVariant& SGMZTeamData);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
	void SGMZOnWinGameShow(const TArray<FSGMZTEAM0DATA>& SGMZTeamData);

	/**
	*Define Method
	*BlueprintNativeEvent，某个队伍领先
	*@Param camp 队伍阵营
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void SGMZLeadTeamChange(const int32& camp);
	/**
	*Define Method
	*BlueprintNativeEvent，更新上古密阵boss的血量信息
	*@Param perHp 血量百分比
	*@Param stage 阶段
	*@Param camp 队伍camp
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void SGMZSendMonsterHp(const int32& camp, const int32& stage, const int32& perHp);

	/**
	*Define Method
	*BlueprintNativeEvent，更新上古密阵的总比分
	*@Param score 积分、比分
	*@Param stage 阶段
	*@Param camp 队伍camp
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void SGMZSendScore(const int32& camp, const int32& stage, const int32& score);

	/**
	*Define Method
	*BlueprintNativeEvent，上古密阵击杀玩家时的比分变化
	*@Param killerCamp 击杀者的camp
	*@Param value 积分变化值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void SGMZSendScoreChange(const int32& killerCamp, const int32& value);

	/**
	*Define Method
	*BlueprintNativeEvent，上古密阵普通boss死亡
	*@Param stage 阶段
	*@Param camp 队伍camp
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_SGMZBossKilled(const int32& camp, const int32& stage);

#pragma endregion

	/**
	*Define Method
	*BlueprintNativeEvent,设置当前NPC对话任务目标的NPCScriptID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void OnDialogWithNPCTaskScriptID(const FString& NPCScriptID);


	/**
	*Define Method
	*BlueprintNativeEvent,开启血条显示（CST-7682 程序需求——根据战斗关系显示血条和关闭）
	*targetID 目标的id
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_ShowHPPercentAboveQuestBar(int32 targetID);

	/**
	*Define Method
	*BlueprintNativeEvent,关闭血条显示（CST-7682 程序需求——根据战斗关系显示血条和关闭）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_CloseHPPercentAboveQuestBar();

	/**
	*Define Method
	*BlueprintNativeEvent,设置小地图可视范围的默认缩放倍数
	*@param	DefaultScale 默认倍数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_SetMiniMapViewDefaultScale(float DefaultScale);

	/**
	*Define Method
	*BlueprintNativeEvent,进入勇闯绝命岛射击模式
	*@param	skillID 射击释放技能
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void EnterYCJMDModelTPS( const int32& skillID, const int32& weaponItemID);

	/**
	*Define Method
	*BlueprintNativeEvent,离开勇闯绝命岛射击模式
	*@param	skillID 射击释放技能
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void LeaveYCJMDModelTPS();

	/**
	*Define Method
	*BlueprintNativeEvent,改变勇闯绝命岛技能ID
	*@param	skillID 射击释放技能
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void ChangeYCJMDModelTPSSkillID(const int32& skillID);

	/**
	*Define Method 显示勇闯绝命岛快捷栏高亮
	*@param	skillID 高亮技能ID
	*
	*@return 无
	*/
	void ShowSkillBarsHighLigh(const int32& highLighID);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RolePerformanceInterface")
		void ShowSkillBarsHighLighBP(const int32& highLighID);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_guessGameSize(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_guessGameRoll(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_endGuessGame();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_ldwj_putDownJinDan();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onSwordCollisionBegin(const FString& STRING_1, const int32& INT32_1, const FVector& POSITION_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onObtainCountAddList(const FString& STRING_1, const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onBaGuaJigsawCompleted();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onRoleCameraMoveToEntity();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_createMonsterExtLightWall(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestRandomDice();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_TriggerQuestDialogWithNPC(const FString& STRING_1);
	
	void RPC_StopPlaySound(FString soundID);

public:
	//追击者分配位置 <半径， 角度>
	TMap<float, TMap<float, int>> ChasePosInfo;

	/**
	*Define Method
	*BlueprintNativeEvent,清空追击者位置信息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RolePerformanceInterface")
		void CLIENT_ClearChasePosInfo ();

	// 回收怪物
	UFUNCTION(BlueprintCallable, Category = "cs3|RolePerformanceInterface")
		void SelectMonsterMenu(const int32& MonsterID, const int32& Index);

};

