#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "TutorialData.generated.h"

/**
* 文件名称：TutorialData.h
* 功能说明：指引提示
* 文件作者：lizhenghui
* 目前维护：zhangdan
* 创建时间：2017-11-1
*/

///指引类型
enum class ETUTORIAL_TYPE : uint8
{
	///无类型
	TUTORIAL_NULL = 0,	
	///箭头指引
	TUTORIAL_ARROW = 1,	
	///图片提示（如角色移动操作提示）
	TUTORIAL_IMG_PROMPT = 2,	
	///消息提示（如装备更高战斗力提示）
	TUTORIAL_MESSAGE_PROMPT = 3,
	///物品或技能放入快捷栏指引
	TUTORIAL_DRAG_ITEM = 4,			
};

///箭头指引类型
UENUM(BlueprintType)
enum class EARROWTYPE : uint8
{
	/// 左箭头指引
	LEFT_ARROW_TUTORIAL = 1,
	/// 右箭头指引
	RIGHT_ARROW_TUTORIAL = 2,
	/// 上箭头指引
	UP_ARROW_TUTORIAL = 3,
	/// 下箭头指引
	DOWN_ARROW_TUTORIAL = 4,
};

///触发类型
UENUM(BlueprintType)
enum class ETUTORIALTRIGGERTYPE : uint8
{
	///触发类型
	/// 任务触发
	QuestTrigger,
	/// 等级触发
	LevelTrigger,
	/// 按钮触发
	ButtonTrigger,
	/// 点击目标
	ActorClickTrigger,
	/// 获取物品触发
	AddItemTrigger,
	/// 首次学习技能触发
	FirstLearnSkillTrigger,
	/// 装备战力触发
	EquipScoreTrigger,
	/// 物品数量不足触发
	LackItemTrigger,
	/// 背包满时触发
	BagFullTrigger,
	/// 死亡触发
	DeathTrigger,
	/// 进入场景触发
	EnterMapTrigger,
	/// 陷阱触发
	TrapTrigger,
	/// 镜头触发
	StoryTrigger,
	/// 打开界面触发
	OpenWindowTrigger,
	/// 提示技能升级触发
	UpgradeSkillTrigger,
	/// 获得buff触发
	AddBuffTrigger,
};

///触发条件基类
UCLASS(BlueprintType)
class CHUANGSHI_API UCS3TriggerCNDBase : public UCS3Object
{
	GENERATED_BODY()
};

///关闭条件基类
UCLASS(BlueprintType)
class CHUANGSHI_API UCS3CloseCNDBase : public UCS3Object
{
	GENERATED_BODY()
};

///表现基类
UCLASS(BlueprintType)
class CHUANGSHI_API UCS3TriggerActionBase : public UCS3Object
{
	GENERATED_BODY()
};

///触发条件参数
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTCNDPARAM
{
	GENERATED_USTRUCT_BODY()
public:
	///程序自动赋值，仅程序用
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName KeyIndex;
	///用来指定使用那个UClass类来处理此参数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSubclassOf<UCS3TriggerCNDBase> ScriptID;
	///参数一
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数二
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数三
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
};

///关闭条件参数
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCLOSECNDPARAM
{
	GENERATED_USTRUCT_BODY()
public:
	///程序自动赋值，仅程序用
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName KeyIndex;
	///用来指定使用那个UClass类来处理此参数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSubclassOf<UCS3CloseCNDBase> ScriptID;
	///参数一
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数二
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数三
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
};

///表现参数
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTUTORIALPARAM
{
	GENERATED_USTRUCT_BODY()
public:
	///程序自动赋值，仅程序用
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName KeyIndex;
	///表现类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ActionType = 0;
	///是否等待面板打开
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isWaitPanelOpen;
	///是否需要功能完成才能进行下一步
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isWaitFinish;
	///指引的按钮UI的类型，1 有面板路径UI 2 动态取UI(面板+子节点名字)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 UIType = 0;
	///指引的按钮UI的路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString UILinkTarget;
	///是否锁屏
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsLockScreen;
	///语音ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString AudioID;
	///语音播完是否自动下一步
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsAutoNextStep;
	///用来指定使用那个UClass类来处理此参数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSubclassOf<UCS3TriggerActionBase> ScriptID;
	///参数一
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数二
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数三
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
	///参数四
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param4;
	///参数五
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param5;
	///参数六
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param6;
	///参数七
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param7;
	///参数八
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param8;
};

#pragma region	/** 指引触发条件相关 */
///触发条件
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerBaseCND : public UCS3TriggerCNDBase
{
	GENERATED_BODY()
public:
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) { return false; }
};

///阵营，Param1配置 阵营：1（仙），2（魔）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerCampCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///等级，Param1配置 等级
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerLevelCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///等级区间，Param1配置 最小等级， Param2配置 最大等级
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerLvRangeCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///职业，Param1配置 职业：1（战士），2（剑客），3（链刃)，4（法师）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerProfessionCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///性别，Param1配置 性别：1（男），2（女）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerGenderCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///装备位置，Param1装备的配置（20帽子,21衣服,22护腕,23手套,24腰带,25裤子,26鞋子,27项链,28戒指,31双手武器,32左手武器,33右手武器,34披风,35法宝）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerEquipPartCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///任务，Param1配置 任务ID, Param2配置 任务状态：1（未接），2(已完成)，3（未完成），4（已提交）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerQuestCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///子任务，Param1配置 任务ID, Param2配置 子任务ID，Param3配置 子任务状态：2（子任务目标已经完成），3（任务目标未完成）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerQuestTaskCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///获得物品，Param1配置 物品ID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerAddItemCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是物品ID，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///物品已入包，Param1配置 物品ID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerItemInKitbagCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///获得技能，Param1配置 技能ID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerAddSkillCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是技能ID，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///拥有技能，Param1配置 技能ID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerHasSkillCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///快捷栏是否有某个技能，Param1配置 技能ID或药品ID， Param2配置 是否拥有：0（没有），1（有），不配默认是有
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerHasQuickSkillCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///获得Buff，Param1配置 BuffID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerAddBuffCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是BuffID，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///拥有Buff，Param1配置 BuffID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerHasBuffCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///镜头状态，Param1配置 镜头ID，Param2配置 镜头状态：1（开始），2（结束）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerStoryCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是镜头ID，Param2是镜头状态（1表示开始，2表示结束）
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///快捷栏空位，Param1配置 是否固定快捷栏位置：0（不固定），1（固定），Param2配置 固定的快捷栏相对位置（即当前页的0-9号位）
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerQuickBarSlotCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///打开界面，Param1配置 WindowID
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerOpenWindowCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是WindowID，Param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};

///显示n个引导，Param1配置1-n数字，每个数字配一行。
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerMatchIndexCND : public UTriggerBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1配置1-n数字，每个数字配一行，param2无
	*/
	virtual bool CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2) override;
};
#pragma endregion

#pragma region	/** 指引表现相关 */
///触发行为
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerBaseACT : public UCS3TriggerActionBase
{
	GENERATED_BODY()
public:
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) {  }
};

/**箭头文本表现
*isWaitPanelOpen配置 是否等待面板打开：true（等待），false（不等待）【目前只有箭头表现有支持】
*isWaitFinish配置 是否等待功能完成：true（等待），false（不等待），配置为等待时，如果功能没完成的话点击指引位置不会完成指引【目前只有箭头表现有支持】
*UIType配置 指引的UI的类型：1（固定的UI路径），2（动态UI路径，比如配置物品ID、技能ID、任务ID等，通过数据计算目标控件路径）
*UILinkTarget配置 指引的UI的路径
*bIsLockScreen配置 是否锁屏：true（锁屏），false（不锁屏）【目前只有箭头表现有支持】
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 是否显示锁定框：0（不显示），1（显示锁定框），2（显示跑马灯）
*Param2配置 箭头方向：1（箭头向左），2（箭头向右），3（箭头向上），4（箭头向下）
*Param3配置 标题
*Param4配置 内容
*Param5配置 锁定框或跑马灯的UI路径：UIType|UILinkTarget ，1（固定的UI路径），2（动态UI路径），UILinkTarget（UI路径）
*Param6配置 是否显示关闭按钮
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerArrowACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无, Param2无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**物品拖动到快捷栏表现
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 物品ID
*Param2配置 否需要显示闪烁效果，0（不显示），1（显示）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerDragItemACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1是物品ID, Param2是物品UID
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**首次学习技能或首次获得药品表现
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 技能或物品的ID|X|Y|Z 
*X：1（技能），3（药品）；
*Y：1（固定快捷栏位置），0（不固定，就会去找第一个空位，没有空位就不触发，有空位就放那个空位）；
*Z：当Y为1时，ICON固定进入快捷栏的位置，若Y为0则不填
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerFirstLearnSkillACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无, Param2是无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**消息提示表现
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 物品ID
*Param2配置 消息类型：1（装备替换），2（背包已满），3（物品不足），4（打开礼包），5（复活界面），6（技能升级）
*Param3配置 是否显示物品图标：1（显示），0（不显示）
*Param4配置 是否显示提示箭头：1（显示），0（不显示）
*Param5配置 标题
*Param6配置 内容
*Param7配置 确定按钮文字
*Param8配置 取消按钮文字
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerMessageACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1是物品ID, Param2是物品UID
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**图片提示表现
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 图片资源路径
*Param2配置 是否显示“下一步”按钮，1（显示），0（不显示）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerImageACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无, Param2是无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**添加操作模式指引
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerOperationACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**添加按键指引
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 标题
*Param2配置 内容
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerKeyACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**添加购买指引
*UIType配置 指引的UI的类型：1（固定的UI路径），2（动态UI路径，比如配置物品ID、技能ID、任务ID等，通过数据计算目标控件路径）
*UILinkTarget配置 指引的UI的路径
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 标题
*Param2配置 内容
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerBuyTipsACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1是商品ID，Param2是空
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**添加移动指引
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerMoveTipsACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无，Param2无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**镜头触发表现
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*Param1配置 镜头ID
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerStoryACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1无, Param2无
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

/**添加拖拽手势指引
*UIType配置 指引的UI的类型：1（固定的UI路径），2（动态UI路径，比如配置物品ID、技能ID、任务ID等，通过数据计算目标控件路径）
*UILinkTarget配置 指引的UI的路径
*AudioID配置 指引时播放语音ID，不配则不播放
*bIsAutoNextStep配置 语音播完是否自动下一步：true（自动），false（不自动）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTriggerDragGestureACT : public UTriggerBaseACT
{
	GENERATED_BODY()
public:
	/**
	*Param1是空, Param2是空
	*/
	virtual void DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2) override;
};

#pragma endregion

#pragma region	/** 关闭条件相关 */

///关闭条件
UCLASS(BlueprintType)
class CHUANGSHI_API UCloseBaseCND : public UCS3CloseCNDBase
{
	GENERATED_BODY()
public:
	virtual bool CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck = false) { return false; }
};

///等级，Param1配置 等级
UCLASS(BlueprintType)
class CHUANGSHI_API UCloseMaxLevelCND : public UCloseBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1无
	*/
	virtual bool CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck = false) override;
};

///任务，Param1配置 任务ID，Param2配置 任务状态：1（未接）,2(已完成)，3（未完成），4（已提交）
UCLASS(BlueprintType)
class CHUANGSHI_API UCloseQuestCND : public UCloseBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是任务ID
	*/
	virtual bool CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck = false) override;
};

///播放技能，Param1配置 技能ID
UCLASS(BlueprintType)
class CHUANGSHI_API UClosePlaySkillCND : public UCloseBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是技能ID
	*/
	virtual bool CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck = false) override;
};

///快捷栏是否有某个技能，Param1配置 技能ID或药品ID， Param2配置 是否拥有：0（没有），1（有），不配默认是有
UCLASS(BlueprintType)
class CHUANGSHI_API UCloseSkillInQuickBarCND : public UCloseBaseCND
{
	GENERATED_BODY()
public:
	/**
	*Param1是技能ID
	*/
	virtual bool CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck = false) override;
};

#pragma endregion

///触发条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTriggerCondition
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTCNDPARAM CndParams;
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UTriggerBaseCND* CndObj;

	virtual ~FTriggerCondition() {}

	virtual bool CheckCondition(const FString& Param1, const FString& Param2);
};

///关闭条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCloseCondition
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FCLOSECNDPARAM CndParams;
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UCloseBaseCND* CndObj;

	virtual ~FCloseCondition() {}

	virtual bool CheckCloseCondition(const FString& Param1, const bool& IsOpenCheck = false);
};

///触发行为
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTriggerTutorialAction
{
	GENERATED_USTRUCT_BODY()
public:
	///行为自带条件配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTriggerCondition> TriggerCnds;
	///行为参数配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTUTORIALPARAM ActParams;
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UTriggerBaseACT* ActObj;
	///执行行为，返回值：行为条件是否符合
	bool DoAction(const FString& Param1, const FString& Param2);
	///执行行为前检测
	bool CheckCondition(const FString& Param1, const FString& Param2)
	{
		if (TriggerCnds.Num() <= 0)
		{
			return true;
		}
		else
		{
			for (FTriggerCondition TriggerCnd : TriggerCnds)
			{
				if (!TriggerCnd.CheckCondition(Param1, Param2))
				{
					return false;
				}
			}
			return true;
		}
	}
};

///@struct FTUTORIALDATA 配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTUTORIALDATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///触发索引
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName KeyIndex;
	///是否仅触发一次
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsTriggerOnce;
	///延迟触发
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float DelayTime;
	///指引触发类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ETUTORIALTRIGGERTYPE TriggerType;
	///指引类型（1箭头指引 2图片指引 3消息指引）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TutorialType = 0;
	///触发条件配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTriggerCondition> TriggerCnds;
	///关闭条件配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCloseCondition> CloseCnds;
	///触发行为配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTriggerTutorialAction> TriggerActs;
	///备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Comment;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool KeyIndexResult = !KeyIndex.IsNone() && FNAME_TO_FSTRING(KeyIndex).TrimStartAndEnd().IsNumeric();
		bool TriggerTypeResult = TutorialType == 1 || TutorialType == 2 || TutorialType == 3;
		if (!KeyIndexResult) ResultInfo.CheckLog += FString::Printf(TEXT("KeyIndex is not int!  "));
		if (!TriggerTypeResult) ResultInfo.CheckLog += FString::Printf(TEXT("TutorialType is config error!  "));
		bool TriggerCndsResult = true;
		if (TriggerCnds.Num() == 0)
		{
			TriggerCndsResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("TriggerCnds is empty! "));
		}
		else
		{
			int index = 0;
			for (auto cnd : TriggerCnds) 
			{
				if (cnd.CndParams.ScriptID == NULL || cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.TrimStartAndEnd().IsNumeric()
					|| (!cnd.CndParams.Param2.IsEmpty() && !cnd.CndParams.Param2.TrimStartAndEnd().IsNumeric())
					|| (!cnd.CndParams.Param3.IsEmpty() && !cnd.CndParams.Param3.TrimStartAndEnd().IsNumeric()))
				{
					TriggerCndsResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("TriggerCnds: Index(%d) "), index);
					if (cnd.CndParams.ScriptID == NULL) ResultInfo.CheckLog += FString::Printf(TEXT("Script is None!  "));
					if (cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param1: \"%s\" is config error!  "), *cnd.CndParams.Param1);
					if (!cnd.CndParams.Param2.IsEmpty() && !cnd.CndParams.Param2.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param2 \"%s\" is not int!  "), *cnd.CndParams.Param2);
					if (!cnd.CndParams.Param3.IsEmpty() && !cnd.CndParams.Param3.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param3 \"%s\" is not int!  "), *cnd.CndParams.Param3);
				}
				index++;
			}
		}

		bool CloseCndsResult = true;
		if (CloseCnds.Num() == 0)
		{
			CloseCndsResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("CloseCnds is empty! "));
		}
		else
		{
			int index = 0;
			for (auto cnd : CloseCnds)
			{
				if (cnd.CndParams.ScriptID == NULL || cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.TrimStartAndEnd().IsNumeric()
					|| (!cnd.CndParams.Param2.IsEmpty() && !cnd.CndParams.Param2.TrimStartAndEnd().IsNumeric())
					|| (!cnd.CndParams.Param3.IsEmpty() && !cnd.CndParams.Param3.TrimStartAndEnd().IsNumeric()))
				{
					CloseCndsResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("CloseCnds: Index(%d) "), index);
					if (cnd.CndParams.ScriptID == NULL) ResultInfo.CheckLog += FString::Printf(TEXT("Script is None!  "));
					if (cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param1: \"%s\" is config error!  "), *cnd.CndParams.Param1);
					if (!cnd.CndParams.Param2.IsEmpty() && !cnd.CndParams.Param2.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param2 \"%s\" is not int!  "), *cnd.CndParams.Param2);
					if (!cnd.CndParams.Param3.IsEmpty() && !cnd.CndParams.Param3.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param3 \"%s\" is not int!  "), *cnd.CndParams.Param3);
				}
				index++;
			}
		}

		bool TriggerActsResult = true;
		if (TriggerActs.Num() == 0)
		{
			TriggerActsResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("TriggerActs is empty! "));
		}
		else
		{
			int index = 0;
			for (auto act : TriggerActs)
			{
				if (act.TriggerCnds.Num() > 0)
				{
					int cndIndex = 0;
					for (auto cnd : act.TriggerCnds)
					{
						if (cnd.CndParams.ScriptID == NULL || cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.TrimStartAndEnd().IsNumeric())
						{
							TriggerCndsResult = false;
							ResultInfo.CheckLog += FString::Printf(TEXT("TriggerActs: Index(%d), TriggerCnds: index(%d): "), index, cndIndex);
							if (cnd.CndParams.ScriptID == NULL) ResultInfo.CheckLog += FString::Printf(TEXT("Script is None!  "));
							if (cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.TrimStartAndEnd().IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param1: \"%s\" is config error!  "), *cnd.CndParams.Param1);
						}
						cndIndex++;
					}
				}
				bool Param1Result = true;
				for (auto datas : UGolbalBPFunctionLibrary::SplitString(act.ActParams.Param1, false, TEXT(",")))
				{
					for (auto data : UGolbalBPFunctionLibrary::SplitString(datas, false, TEXT("|")))
					{
						if (!data.TrimStartAndEnd().IsNumeric())
						{
							Param1Result = false;
							break;
						}
					}
				}
				if (act.ActParams.ScriptID == NULL || !Param1Result)
				{
					TriggerCndsResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("TriggerActs Index(%d): "), index);
					if (act.ActParams.ScriptID == NULL) ResultInfo.CheckLog += FString::Printf(TEXT("ScriptID is None!  "));
					if (!Param1Result) ResultInfo.CheckLog += FString::Printf(TEXT("Param1: \"%s\" is config error!  "), *act.ActParams.Param1);
				}
				index++;
			}
		}
		bool result = KeyIndexResult && TriggerTypeResult && TriggerCndsResult && CloseCndsResult && TriggerActsResult;
		if (result)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};

	FORCEINLINE bool operator==(const FTUTORIALDATA& Other) const
	{
		if (this->KeyIndex == Other.KeyIndex)
		{
			return true;
		}
		else
		{
			return false;
		}
	}

	//完成此操作指引，通知服务器记录已经触发过的指引
	void SaveTriggerIndex();

	///指引表现
	void DoAction(const FString& Param1, const FString& Param2);
	///执行行为前检测
	bool CheckCondition(const FString& Param1, const FString& Param2)
	{
		if (TriggerCnds.Num() <= 0)
		{
			return true;
		}
		else
		{
			for (FTriggerCondition& TriggerCnd : TriggerCnds)
			{
				if (!TriggerCnd.CheckCondition(Param1, Param2))
				{
					return false;
				}
			}
			return true;
		}
	}
	///刚登录时、条件变化时检测是否关闭
	bool CheckCloseCondition(const FString& Param1, const bool& IsOpenCheck = false, UClass* CloseCndClass = nullptr)
	{
		if (CloseCnds.Num() <= 0)
		{
			return false;
		}
		else
		{
			for (FCloseCondition& CloseCnd : CloseCnds)
			{
				//只检测一个类型
				if (CloseCndClass != nullptr)
				{
					if ((CloseCnd.CndParams.ScriptID)->IsChildOf(CloseCndClass))
					{
						if (CloseCnd.CheckCloseCondition(Param1, IsOpenCheck))
						{
							return true;
						}
					}
				}
				else
				{
					//有一个条件符合就关闭
					if (CloseCnd.CheckCloseCondition(Param1, IsOpenCheck))
					{
						return true;
					}
				}
			}
			return false;
		}
	}
};

///指引数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTutorialListData
{
	GENERATED_USTRUCT_BODY()
public:
	///指引数据
	UPROPERTY(BlueprintReadOnly)
		FTUTORIALDATA TutorialData;
	///参数一
	UPROPERTY(BlueprintReadOnly)
		FString Param1;
	///参数二
	UPROPERTY(BlueprintReadOnly)
		FString Param2;
	///是否已完成
	UPROPERTY(BlueprintReadOnly)
		bool IsFinished;

	FORCEINLINE bool operator==(const FTutorialListData& Other) const
	{
		if (this->TutorialData == Other.TutorialData && this->Param1 == Other.Param1 \
			&& this->Param2 == Other.Param2 && this->IsFinished == Other.IsFinished)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};