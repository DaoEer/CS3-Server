#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "QTEDate.generated.h"


/**
* 文件名称：QTEDate.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-08-21
*/

UENUM(BlueprintType)
enum class QTE_TYPE : uint8
{
	///Default（默认）
	///	Param1~3：无
	///支持：
	///	开始、结束、提前结束、中断（以描述“计时”、“跳转”等表现行为）（@CST-3781）
	///		默认模式，只支持基本的流程事件
	///触发：
	///	Result1~4：无
	DEFAULT_Mode		UMETA(DisplayName = "DEFAULT_Mode"),
	///MobileMouse（鼠标左右晃动）
	///	Param1~3：无
	///支持：
	///	开始、结束、提前结束、中断
	///	利用鼠标进行滑动到达一个值时，执行相对应的方法（@CST-4407）
	///		目前成功/失败时，会默认中断QTE（后续可以考虑优化）
	///触发：
	///	Result1：攒槽成功（鼠标左右晃动攒槽，槽满了，触发结果1）
	///	Result2：攒槽失败（QTE持续时间结束时，槽还没满，触发结果2）
	///	Result3~4：无
	///注意：
	///	目前界面显示由BuffQTE驱动，而不是QTE类型，显示上有缺陷（后续可以考虑优化）
	MOBILE_MOUSE		UMETA(DisplayName = "MOBILE_MOUSE"),
	///KeyboardKeys（指定按键）
	///	Param1：目标按键1|目标按键2|目标按键3……（格式“A|B|C”，不支持缺省）
	///	Param2~3：无
	///支持：
	///	开始、结束、提前结束、中断
	///	按下键盘时响应，按键与“目标按键”相符，则返回相应结果；按键错误或时间结束，则失败（@CST-3781）
	///触发：
	///	Result1：“目标按键1”成功（按键与目标按键1相符，触发结果1）
	///	Result2：“目标按键2”成功（按键与目标按键2相符，触发结果2）
	///	Result3：“目标按键3”成功（按键与目标按键3相符，触发结果3）
	///	Result4：按键失败（按键不相符，或，QTE持续时间结束时，触发结果4）
	///		目前“结果1~4”时，都会默认中断QTE，触发成功后不再有效果（后续可以考虑优化）
	///注意：
	///	“按键名称”的填写规则，由UE4定义，请谨慎配置
	///		（详见，UE4编辑器-工具栏-设置-项目设置-输入-Bindings-Action Mappings-选择键值）
	///		键盘按键大致如下：
	///			“常规键位”直观大写，如：“A”、“B”、“C”、“1”、“=”、“F1”……
	///			“小键盘”加前缀，如：“Num 0”、“Num 1”、“Num /”……
	///			“功能键”填中文（很不讲道理的，请注意区分），如：
	///				“回车键”（Enter）、“空格键”（Space）、“回格键”（BackSpace）、“Escape”（Esc）……
	///				“左Ctrl”、“左Shift”、“左Alt”、“左Cmd”、“Tab键”、“ ”（空格）……
	///				“向上”、“向下键”、“向左键”、“向右键”（吐槽：“向上”还真是不一样，UE4的翻译简直有毒）
	///		鼠标按键也可以触发：
	///			都是中文，如：“鼠标左键”、“鼠标右键”、“鼠标滚轮轴”、“鼠标滚轮上滚”……
	KEYBOARD_KEYS		UMETA(DisplayName = "KEYBOARD_KEYS"),
	///ContinuityKeyboard（连续按键）
	/// Param1：指定字符集合，缺省则为A~Z（26个英文字母）；
	///	Param2：规则类型（程序自定，缺省1）
	///		0：顺序固定，按键数量不限，要求连续按对，点错重来（@CST-7529）
	///		1：顺序随机，上限按Param3，要求全部按完，按错规则按Param3（@CST-6196）（@CST-12007）
	///	Param3：(Param2=1才有效) 随机个数下限 | 随机个数上限 | 按错规则
	///		按错规则（缺省默认1）:
	///		1：按错全部键重来，QTE不结束，恢复前面按对的字符状态，重新从第一个开始;（@CST-12007）
	///		2：按错不重来，QTE结束;（@CST-12007）
	///		3：按错重新生成随机字符串，QTE不结束;（@CST-12007）
	///		4：按错当前键重来，QTE不结束，字符不刷新，进度不变;（@CST-13424）
	///支持：
	///	开始、结束、提前结束、中断
	///	按界面要求，连续按下相应按键（@CST-6196/CST-7529）
	///触发：
	///	Result1：单个按键成功（按键与当前目标按键相符，触发结果1）
	///	Result2：单个按键失败（按键与当前目标按键不符，触发结果2）
	///	Result3：整体成功（全部按键正确，触发结果3）
	///	Result4：整体失败（QTE持续时间结束时，按键没有全部正确，触发结果4）
	///注意：
	///	“按键名称”的填写规则，由UE4定义，请谨慎配置
	///		（详见，UE4编辑器-工具栏-设置-项目设置-输入-Bindings-Action Mappings-选择键值）
	///		键盘按键大致如下：
	///			“常规键位”直观大写，如：“A”、“B”、“C”、“1”、“=”、“F1”……
	///			“小键盘”加前缀，如：“Num 0”、“Num 1”、“Num /”……
	///			“功能键”填中文（很不讲道理的，请注意区分），如：
	///				“回车键”（Enter）、“空格键”（Space）、“回格键”（BackSpace）、“Escape”（Esc）……
	///				“左Ctrl”、“左Shift”、“左Alt”、“左Cmd”、“Tab键”、“ ”（空格）……
	///				“向上”、“向下键”、“向左键”、“向右键”（吐槽：“向上”还真是不一样，UE4的翻译简直有毒）
	///		鼠标按键也可以触发：
	///			都是中文，如：“鼠标左键”、“鼠标右键”、“鼠标滚轮轴”、“鼠标滚轮上滚”……
	CONTINUITY_KEYBOARD	UMETA(DisplayName = "CONTINUITY_KEYBOARD"),
};

UENUM(BlueprintType)
enum class QTE_EVENT_TYPE : uint8
{
	///OnCellCall（回调服务器消息）
	///	Param1：联动BuffQTE触发技能申请
	///		1：申请QTE成功技能（对应BuffQTE的参数2）
	///		0：申请QTE失败技能（对应BuffQTE的参数3）
	///	Param2~3：无
	///支持：
	///	回调服务器成功/失败消息，调用BuffTable中成功/失败技能（@CST-7529）
	CELLCALL_EVENT		UMETA(DisplayName = "CELLCALL_EVENT"),
	///Camera（播放剧情动画）
	///	Param1：剧情动画ID（@DT_StoryCfg）
	///	Param2：播放次数（缺省1次）
	///	Param3：无
	///支持：
	///	播放剧情动画表现（@CST-3781）
	CAMERA_EVENT		UMETA(DisplayName = "CAMERA_EVENT"),
	///PlayEffect（播放光效）
	///	Param1：光效ID（@DT_EffectCfg）
	///	Param2~3：无
	///支持：
	///	播放光效表现（@CST-3781）
	///注意：
	///	光效的施法者、目标，都是PC自身
	PLAYEFFECT_EVENT	UMETA(DisplayName = "PLAYEFFECT_EVENT"),
	///PlaySound（播放音效）
	///	Param1：音效ID（@DT_AudioCfg）
	///	Param2~3：无
	///支持：
	///	播放音效表现（@CST-6196）
	PLAYSOUND_EVENT		UMETA(DisplayName = "PLAYSOUND_EVENT"),
	///RETREAT（提前结束）
	///	Param1~3：无
	///支持：
	///	无需等待生存时间，直接提前结束本QTE（@CST-3781）
	///		提前结束时，可以触发本QTE的结束事件
	RETREAT_EVENT		UMETA(DisplayName = "RETREAT_EVENT"),
	///INTERRUPT（中断QTE）
	///	Param1~3：无
	///支持：
	///	中断QTE（@CST-3781）
	///注意：
	///	【未完成】暂未实现，留下接口等待实现中
	INTERRUPT_EVENT		UMETA(DisplayName = "INTERRUPT_EVENT"),
	///InternalJump（内部跳转）
	///	Param1：跳转元素编号（从0开始的列表元素编号，缺省代表“没有跳转”）
	///	Param2~3：无
	///支持：
	///	跳转到本行QTE配置中的，指定元素内容（@CST-3781）
	///注意：
	///	跳转时，不触发本QTE的结束事件，触发目标QTE的开始事件
	INTERNALJUMP_EVENT	UMETA(DisplayName = "INTERNALJUMP_EVENT"),
	///ExternalJump（外部跳转）
	///	Param1：跳转QTE编号（QTE配置表的行号，缺省代表“没有跳转”）
	///	Param2：跳转元素编号（从0开始的列表元素编号，缺省0）
	///	Param3：无
	///支持：
	///	跳转到其他QTE配置中的，指定元素内容（@CST-3781）
	///注意：
	///	【未完成】暂未实现，留下接口等待实现中
	EXTERNAL_JUMP		UMETA(DisplayName = "EXTERNAL_JUMP"),
	///BossDemo（BossDemo专用事件）
	///	Param1：是否成功
	///		1：是
	///		0：否
	///	Param2：下一个QTE也是鼠标移动类型时，需要填写与间隔时间相同的时间
	///	Param3：无
	///支持：
	///	BossDemo专用，抓取挣脱事件（@CST-3781）
	///注意：
	///	参数说明待定
	BOSSDEMO_EVENT		UMETA(DisplayName = "BOSSDEMO_EVENT"),
	///BossDemoUI（BossDemoUI专用事件）
	///	Param1：是否显示
	///		1：是
	///		0：否
	///	Param2：显示boss站ui界面
	///	Param3：无
	///支持：
	///	BossDemo专用事件（）
	///注意：
	///	参数说明待定
	BOSSDEMO_PROGRESS	UMETA(DisplayName = "BOSSDEMO_PROGRESS"),
	///Lenskey（镜头按键专用事件）
	///	Param1：剧情动画ID（@DT_StoryCfg，留空代表“没有剧情动画”）
	///	Param2：播放帧率（从那一秒开始播放）PlayRate
	///	Param3：是否循环（缺省0）
	///		1：循环
	///		0：不循环
	///支持：
	///	镜头按键专用事件（@CST-6196）
	///注意：
	///	参数说明待定
	LENSKEY_EVENT		UMETA(DisplayName = "LENSKEY_EVENT"),
	///LenskeyRate（设置剧情播放的速率）
	///	Param1：目标播放速率（如1代表100%）
	///	Param2：无
	///	Param3：无
	///支持：
	///	设置剧情播放的速率（@CST-7529）
	LENSKEYRATE_EVENT	UMETA(DisplayName = "LENSKEYRATE_EVENT"),
	///HaoLingGuUI（浩灵谷UI事件）
	///	Param1：开启/关闭，浩灵谷UI显示
	///		1：开启
	///		0：关闭
	///	Param2~3：无
	///支持：
	///	浩灵谷专用事件（@CST-6196）
	HAOLINGGUUI_EVENT	UMETA(DisplayName = "HAOLINGGUUI_EVENT"),
	///HaoLingGuKey（浩灵谷KEY回调事件）
	///	Param1~3：无
	///支持：
	///	浩灵谷专用事件（@CST-6196）
	HAOLINGGUKEY_EVENT	UMETA(DisplayName = "HAOLINGGUKEY_EVENT"),
	///ServerCall（调用服务器方法）
	///	Param1：需要调用的服务器方法
	///		1：RPC_onCompleteQTENotyfy
	///			对应Param2：（0：失败；1：成功）
	///			对应Param3：无
	///	Param2~3：由参数1定义
	///支持：
	///	副本浩灵谷程序功能需求（@CST-6196）
	///注意：
	///	此方法需要填入的参数需要写入参数2和参数3中 具体看备注详解
	SERVERCALL_EVENT	UMETA(DisplayName = "SERVERCALL_EVENT"),
	///Custom（自定义事件）
	///	Param1~3：无
	///注意：
	///	【未完成】当前仅供测试使用（@CST-3781）
	CUSTOM_EVENT		UMETA(DisplayName = "CUSTOM_EVENT"),
};

UENUM(BlueprintType)
enum class QTE_COMPLETE_TYPE : uint8
{
	///QTE事件响应：开始
	START_EVENT			UMETA(DisplayName = "START_EVENT"),
	///QTE事件响应：结束
	END_EVENT			UMETA(DisplayName = "END_EVENT"),
	///QTE事件响应：结果1
	Result1_EVENT		UMETA(DisplayName = "Result1_EVENT"),
	///QTE事件响应：结果2
	Result2_EVENT		UMETA(DisplayName = "Result2_EVENT"),
	///QTE事件响应：结果3
	Result3_EVENT		UMETA(DisplayName = "Result3_EVENT"),
	///QTE事件响应：结果4
	Result4_EVENT		UMETA(DisplayName = "Result4_EVENT"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FQTE_EVENT_DATA
{
	GENERATED_BODY()
public:
	///QTE事件响应类型（发生何事件时响应）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		QTE_COMPLETE_TYPE QTEComplete;
	///QTE事件行为类型（响应时的操作）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		QTE_EVENT_TYPE QTEEventType;
	///QTE事件行为参数1：字符串
	///	功能由QTE事件行为定义（详见具体脚本说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		FString Param1;
	///QTE事件行为参数2：字符串
	///	功能由QTE事件行为定义（详见具体脚本说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		FString Param2;
	///QTE事件行为参数3：字符串
	///	功能由QTE事件行为定义（详见具体脚本说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		FString Param3;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FQTE_TYPE_DATA
{
	GENERATED_BODY()
public:
	///QTE类型（如：晃动鼠标、按下键盘按键）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		QTE_TYPE QTEType ;
	///QTE类型参数1：字符串
	///	功能由QTE类型定义（详见具体脚本说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		FString Param1;
	///QTE类型参数2：字符串
	///	功能由QTE类型定义（详见具体脚本说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		FString Param2;
	///QTE类型参数3：字符串
	///	功能由QTE类型定义（详见具体脚本说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		FString Param3;
	///QTE生存时间（秒，“0秒”代表“开始后立刻结束”，“-1秒”代表“不会结束”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		float QTESurvivalTime = 0.0f;
	///QTE事件列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		TArray<FQTE_EVENT_DATA> QTEEventData;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FQTE_DATE : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QTE")
		TArray<FQTE_TYPE_DATA> QTEData;

public:
	void WriteLog(FString Log, bool bHasError, RowCheckResultInfo& ResultInfo)
	{
		ResultInfo.Result = Error;
		if (bHasError)
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("; %s"), *Log);
		}
		else
		{
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: %s"), *Log);
		}

	}

	void CheckQTEEventData(RowCheckResultInfo& ResultInfo, TArray<FQTE_EVENT_DATA> QTEEventData, int QTEDataIndex, bool& bHasError)
	{
		for (int i = 0; i < QTEEventData.Num(); i++)
		{
			auto& EventData = QTEEventData[i];
			if (EventData.QTEEventType == QTE_EVENT_TYPE::CELLCALL_EVENT || EventData.QTEEventType == QTE_EVENT_TYPE::BOSSDEMO_PROGRESS)
			{
				FString TempParam1 = EventData.Param1.TrimStartAndEnd();
				if (TempParam1 != "0" && TempParam1 != "1")
				{
					WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param1\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
					bHasError = true;
				}
			}
			else if (EventData.QTEEventType == QTE_EVENT_TYPE::CAMERA_EVENT)
			{
				FString TempParam2 = EventData.Param2.TrimStartAndEnd();
				if (!TempParam2.IsEmpty() && TempParam2 != "0")
				{
					int IntParam2 = FSTRING_TO_INT(TempParam2);
					if (IntParam2 == 0 || IntParam2 < 0)
					{
						WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param2\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
						bHasError = true;
					}
				}
			}
			else if (EventData.QTEEventType == QTE_EVENT_TYPE::INTERNALJUMP_EVENT)
			{
				FString TempParam1 = EventData.Param1.TrimStartAndEnd();
				if (!TempParam1.IsEmpty() && TempParam1 != "0")
				{
					int IntParam1 = FSTRING_TO_INT(TempParam1);
					if (IntParam1 == 0 || IntParam1 < 0)
					{
						WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param1\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
						bHasError = true;
					}
				}
			}
			else if (EventData.QTEEventType == QTE_EVENT_TYPE::EXTERNAL_JUMP)
			{
				FString TempParam1 = EventData.Param1.TrimStartAndEnd();
				FString TempParam2 = EventData.Param2.TrimStartAndEnd();
				if ((!TempParam1.IsEmpty() && TempParam1 != "0") || (!TempParam2.IsEmpty() && TempParam2 != "0"))
				{
					int IntParam1 = FSTRING_TO_INT(TempParam1);
					int IntParam2 = FSTRING_TO_INT(TempParam2);
					if (IntParam1 == 0 || IntParam1 < 0 || IntParam2 == 0 || IntParam2 < 0)
					{
						WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param1\" or \"Param2\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
						bHasError = true;
					}
				}
			}
			else if (EventData.QTEEventType == QTE_EVENT_TYPE::BOSSDEMO_EVENT)
			{
				FString TempParam1 = EventData.Param1.TrimStartAndEnd();
				FString TempParam2 = EventData.Param2.TrimStartAndEnd();
				if ((!TempParam1.IsEmpty() && TempParam1 != "0") || (!TempParam2.IsEmpty() && TempParam2 != "0" && 
					(FSTRING_TO_INT(TempParam2) == 0 || FSTRING_TO_INT(TempParam2) < 0)))
				{
					WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param1\" or \"Param2\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
					bHasError = true;
				}
			}
			else if (EventData.QTEEventType == QTE_EVENT_TYPE::LENSKEY_EVENT)
			{
				FString TempParam2 = EventData.Param2.TrimStartAndEnd();
				FString TempParam3 = EventData.Param3.TrimStartAndEnd();
				if ((!TempParam2.IsEmpty() && TempParam2 != "0" && FSTRING_TO_FLOAT(TempParam2) == 0) || 
					(!TempParam3.IsEmpty() && TempParam3 != "0" && TempParam3 != "1"))
				{
					WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param2\" or \"Param3\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
					bHasError = true;
				}
			}
			else if (EventData.QTEEventType == QTE_EVENT_TYPE::LENSKEYRATE_EVENT)
			{
				FString TempParam1 = EventData.Param1.TrimStartAndEnd();
				if (TempParam1 != "0")
				{
					int IntParam1 = FSTRING_TO_FLOAT(TempParam1);
					if (IntParam1 == 0 || IntParam1 < 0)
					{
						WriteLog(FString::Printf(TEXT("QTEData Index(%d), QEVENTData Index(%d), \"Param1\" config error"), QTEDataIndex, i), bHasError, ResultInfo);
						bHasError = true;
					}
				}
			}
		}
	}

	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;

		for (int i = 0; i < QTEData.Num(); i++)
		{
			auto& Data = QTEData[i];
			if (Data.QTEType == QTE_TYPE::CONTINUITY_KEYBOARD)
			{
				FString TempParam2 = Data.Param2.TrimStartAndEnd();
				if (!TempParam2.IsEmpty() && TempParam2 != "0")
				{
					if (FSTRING_TO_INT(TempParam2) == 0)
					{
						ResultInfo.Result = Error;
						if (bHasError)
						{
							ResultInfo.CheckLog += FString::Printf(TEXT("; QTEData Index(%d), \"Param2\" Not of type int"), i);
						}
						else
						{
							ResultInfo.CheckLog = FString::Printf(TEXT("Error: QTEData Index(%d), \"Param2\" Not of type int"), i);
						}

						bHasError = true;
					}
				}
			}
			CheckQTEEventData(ResultInfo, Data.QTEEventData, i, bHasError);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
