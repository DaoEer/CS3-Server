// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SkillTableData.h"
#include "GameData/CsvTableRowBase.h"
#include "BuffTableData.generated.h"

/**
* 文件名称：BuffTableData.h
* 功能说明：BUFF的基本数据
* 文件作者：WangZhen
* 目前维护：all
* 创建时间：2016-12-26
*/


UENUM(BlueprintType)
enum class ENUM_BUFF_CLASS_TYPE : uint8
{
	///BuffHold（持有Buff）
	///	Param1~5：无
	///设计原意：
	///	将最基本的Buff行为逐步剥离出来
	///支持：
	///	替换/额外、添加/移除、条件/中断、保存、添加表现、持有（@CST-678）
	BuffHold = 0 UMETA(DisplayName = "BuffHold"),
	///BuffHit（打击Buff）
	///	Param1~5：无
	///设计原意：
	///	将最基本的Buff行为逐步剥离出来
	///支持：
	///	继承：BuffHold
	///	开始打击、结束打击（@CST-678/@CST-1024）
	BuffHit = 1 UMETA(DisplayName = "BuffHit"),
	///BuffHitBack（击退Buff）
	///	Param1：击退动作ID:起始帧时间（秒）
	///	Param2：起身动作ID:起始帧时间（秒）
	///	Param3：击退时间（秒）|起身时间（秒，参数2有效时生效）
	///	Param4：击退距离下限（缺省0米）|上限（缺省＝下限）
	///		服务器位移速度有≤50米/秒的限制，实际上为了同步表现正确，建议速度表现≤25米/秒
	///	Param5：改变朝向类型|击退方向类型（不得缺省）
	///	　改变朝向类型（先【转向】，后击退）
	///		0：同“施法者当前朝向”（表现为“和施法者看相同的方向”）
	///		1：逆“施法者当前朝向”（表现为“和施法者看相反的方向”）
	///		2：施法者→受术者方向（表现为“背对施法者”，若位置重叠则修正为“施法者当前朝向”）
	///		3：受术者→施法者方向（表现为“围观施法者”，若位置重叠则修正为“受术者当前朝向”）
	///		4：同“受术者当前朝向”（表现为“受术者刷新朝向”）
	///		5：逆“受术者当前朝向”（表现为“受术者向后转”）
	///	　击退方向类型（先转向，后【击退】）
	///		0：同“施法者当前朝向”（表现为“整齐地，推走”）
	///		1：逆“施法者当前朝向”（表现为“整齐地，拉回”）
	///		2：施法者→受术者方向（表现为“分散地，推走”，若位置重叠则修正为“施法者当前朝向”）
	///		3：受术者→施法者方向（表现为“分散地，拉回”，若位置重叠则修正为“受术者当前朝向”）
	///		4：同“受术者当前朝向”（表现为“受术者向前扑街”）
	///		5：逆“受术者当前朝向”（表现为“受术者向后摔跤”）
	///		示例：“5|5”，代表“目标先【向后转】，然后再【往（新的）后方摔倒】”
	///设计原意：
	///	描述单位“被击退”的表现
	///支持：
	///	继承：BuffHit
	///	情景免疫：被罡气格挡（@CST-2229）
	///	受击状态、击退表现：击退动作→转向→位移→位移停止→起身动作→结束（@CST-1325）
	///	效果状态持有：受击状态（/queryAttr effectCounter，#3，第4个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止施法、禁止改变朝向、禁止主动移动、禁止跳跃、禁止交互
	///注意：
	///	击退类特效，同类顶替：BuffHitBack、BuffPull、BuffRise
	///	已知风险：无法保障重新添加时的表现，请谨慎配置“下线保存”
	///	已知风险：若击退时间≤Buff持续时间，则后续表现无效，请谨慎配置“击退时间”
	BuffHitBack = 2 UMETA(DisplayName = "BuffHitBack"),
	///BuffLoop（周期Buff）
	///	Param1~5：无
	///设计原意：
	///	描述“广义的周期Buff行为”的表现
	///支持：
	///	继承：BuffHit
	///	周期打击：施法者是Buff施法者，打击目标是Buff持有者（@CST-678/@CST-1024）
	///		（如，若“A给B套个离子烫，B去烫C”，则伤害是A给C的，B只是个搬运工，甚至B被顺便打到也不奇怪）
	BuffLoop = 3 UMETA(DisplayName = "BuffLoop"),
	///BuffStackable（可叠加Buff）
	///	Param1：叠加层数上限（缺省1层，≤0修正为“上限1层”）
	///	Param2~5：无
	///设计原意：
	///	描述“Buff可以叠加几层”的表现
	///支持：
	///	继承：BuffLoop
	///	叠加表现：多次注册持有效果，刷新Buff持续时间（@CST-888/@CST-2576）
	///		Buff图标右下角显示当前层数（若叠加层数上限≤1，则修正为“不显示层数”）
	///反思：
	///	为了避免伤害来源混淆，此处放弃了“叠加时触发多次周期打击”
	BuffStackable = 4 UMETA(DisplayName = "BuffStackable"),
	///BuffChangeBody（变身Buff）
	///	Param1：变身模型ID（@DT_ModelCfg）
	///	Param2：变身模型缩放比率（如0.5代表“50%大小”，不得缺省）
	///	Param3：变身初始动作ID（只维持三秒，若期间从AOI外恢复，则可重播变身初始动作）
	///	Param4~5：无
	///设计原意：
	///	描述“变身”、“变羊”…等表现
	///支持：
	///	继承：BuffHold
	///	替换模型表现：直接换个模型（@CST-888）
	///	开关状态持有：禁止更换装备（以避免模型更新）
	///	变身完成后，播放初始动作（@CST-2292）
	///注意：
	///	模型类特效，同类顶替：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountTalisman、BuffMountCarrier
	///	模型类特效，中断骑乘：若受术者为PC，则中断骑乘
	///	已知风险：若模型ID错误，则表现为默认异常模型（SK_#404），请谨慎配置“模型ID”
	///	已知风险：若动画蓝图资源与单位类型不匹配，则可能产生报错，请谨慎配置（来源待定）
	///		建议选择匹配单位类型的模型ID，以保障表现正确（如怪物应选择“带_Mon后缀”的模型ID）
	BuffChangeBody = 5 UMETA(DisplayName = "BuffChangeBody"),
	///BuffXinMoCtrl（心魔控制Buff）
	///	Param1：允许使用的技能开关类型列表（|竖号分隔，留空代表“只允许ForbidNone的技能”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“1”，代表“只允许使用ForbidSpell的技能”
	///	Param2：禁止使用的技能ID（@DT_SkillCfg，|竖号分隔，留空代表“没有排除”）
	///		示例：“900002001|900002002|900002003|900002004”，代表“不允许使用紧急回避技能”
	///	Param3~5：无
	///设计原意：
	///	“心智类”的异常状态，描述“失心疯，情不自禁地攻击队友”的表现
	///支持：
	///	继承：BuffHold
	///	心魔控制表现：不受玩家控制、强制攻击队友（@CST-888）
	///		选定敌人：指定“30米内的（距离最近的、可见的）敌对单位”作为当前目标
	///		选定技能：指定“已学习列表内的（不是被动技能的、开关允许的、不被排除的、不在冷却中的）可用的技能”作为当前技能
	///注意：
	///	受术者单位类型：PC限定
	///	一般地，“心智异常”表现不视为“控制行为”，不受“无敌”、“霸体”…等状态制约
	///	已知风险：由于“已学习技能列表”的顺序不固定，不同PC在心魔控制时的具体表现可能不同，暂定无需处理（@CST-888）
	BuffXinMoCtrl = 6 UMETA(DisplayName = "BuffXinMoCtrl"),
	///BuffReplaceSkillBar（替换快捷栏Buff）
	///	Param1：快捷栏类型1:对应配置1|快捷栏类型2:对应配置2…（:冒号和|竖号分隔，支持最多9个格子）
	///	　快捷栏类型：（缺省0）
	///		0：空格子（@csdefine.QB_ITEM_NONE）
	///		1：玩家技能
	///		3：背包道具
	///	　对应配置格式：
	///		对应“0：空格子”　：无
	///		对应“1：玩家技能”：技能ID（@DT_SkillCfg，不得缺省）
	///		对应“3：背包道具”：道具ID（@DT_ItemDataCfg，不得缺省）
	///	　示例：“0|1:911001001|3:202010001”，代表“第1格是空格子，第2格是技能，第3格是道具”
	///	Param2：是替换技能栏还是叠加到技能栏。（0或缺省：替换全部技能栏，1：叠加技能栏）
	///	Param3~5：无
	///设计原意：
	///	不让PC使用原有技能的状态，实现上变成了PC强制使用指定快捷栏技能
	///支持：
	///	继承：BuffHold
	///	替换快捷栏：替换快捷栏的图标，顺序显示（@CST-1719/@CST-1303/@CST-4141）
	///注意：
	///	受术者单位类型：PC限定
	///	界面类特效，同类顶替：BuffReplaceSkillBar、BuffReSkillBarAndLoginTeleport
	///	已知风险：若技能ID错误，则服务器初始化时警告，请谨慎配置“技能ID”
	BuffReplaceSkillBar = 7 UMETA(DisplayName = "BuffReplaceSkillBar"),
	///BuffStone（石化表现Buff）
	///	Param1：石化表现淡入时间（秒，0代表“立即”）
	///	Param2：石化表现淡出时间（同上）
	///	Param3：材质覆盖表现配置ID（@DT_BuffClientEffectCfg.EffectType，缺省0）
	///		0：石头材质表现（仅供参考，具体表现可自定义）
	///		1：冰冻材质表现
	///		999001001：测试表现
	///	Param4~5：无
	///设计原意：
	///	描述“目标变成了石头材质”的表现（只是外观改变，依然可以随意移动）
	///支持：
	///	继承：BuffHold
	///	材质渐变表现：“原表现”→渐变→“目标材质表现”→渐变→“原表现”（@CST-1719/@CST-1357）
	///	石化表现恢复：模型重新加载后，恢复显示成100%的石化表现（@CST-3814）
	///	支持自定义材质表现（@CST-6804）
	///注意：
	///	模型类特效，同类顶替：BuffStone
	BuffStone = 8 UMETA(DisplayName = "BuffStone"),
	///BuffHitSlow（动作定帧表现Buff）
	///	Param1：动作迟缓速率（如0.5代表“减速50%伤害”，不得缺省）
	///	Param2：动作迟缓持续时间（秒，不得缺省）
	///	Param3~5：无
	///设计原意：
	///	尝试达到单机游戏打击感的尝试，似乎是失败了呵呵
	///支持：
	///	继承：BuffHit
	///	定帧表现：临时方案，动作渐变减速，最后停止（@CST-1616）
	///注意：
	///	动作类特效，同类顶替：BuffHitSlow
	///	已知风险：若动作迟缓持续时间≤Buff持续时间，则后续表现无效，请谨慎配置
	BuffHitSlow = 9 UMETA(DisplayName = "BuffHitSlow"),
	///BuffStoryBind（剧情动画Buff，未验收完成）
	///	Param1：剧情动画ID（@DT_StoryCfg）
	///	Param2~5：无
	///设计原意：
	///	希望整合“播放剧情动画”的表现（扩展可被中断、可持有效果状态…等）
	///支持：
	///	继承：BuffHold
	///	剧情动画表现：播放动画→播放完毕中断Buff（@CST-1813/@CST-7538）
	///		剧情动画过程中，玩家不受伤害（@CST-7538）
	///	效果状态持有：表演状态（/queryAttr effectCounter，#12，第13个）
	///注意：
	///	受术者单位类型：PC限定
	///	剧情动画特效，同类顶替：BuffStoryBind
	BuffStoryBind = 10 UMETA(DisplayName = "BuffStoryBind"),
	///BuffPull（拉扯Buff）
	///	Param1：击退动作ID:起始帧时间（秒）
	///	Param2：起身动作ID:起始帧时间（秒）
	///	Param3：拉扯速度（米/秒）|起身时间（秒，起身动作ID有效时才生效）
	///		服务器位移速度有≤50米/秒的限制，实际上为了同步表现正确，建议速度表现≤25米/秒
	///		若实际拉扯位移时间＞起身时间，则位移结束时才起身
	///	Param4：拉扯截止距离，表现为“拉到距离X米就停下”（＜0修正为“0米”）
	///		若“初始距离≤截止距离”，则修正为“立即抵达，不位移”
	///	Param5：无
	///设计原意：
	///	做个方向不同的，击退，把人拉到我面前来就停下，而不要穿到我后面去
	///支持：
	///	继承：BuffHit
	///	情景免疫：被罡气格挡（@CST-2229）
	///	拉扯表现：击退动作→位移停止→起身动作→结束（@CST-886）
	///	效果状态持有：受击状态（/queryAttr effectCounter，#3，第4个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止施法、禁止改变朝向、禁止主动移动、禁止跳跃、禁止交互
	///注意：
	///	击退类特效，同类顶替：BuffHitBack、BuffPull、BuffRise
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	///	已知风险：无法保障重新添加时的表现，请谨慎配置“下线保存”
	BuffPull = 11 UMETA(DisplayName = "BuffPull"),
	///BuffChangeModelScale（模型缩放表现Buff）
	///	Param1：模型缩放大小修正（支持多种缺省格式，＜0表现为“镜像”，请慎用）
	///		①XYZ全部留空，视为“1|1|1”，代表“没有缩放”
	///		②X有配置，YZ留空，视为“X|X|X”，代表“整体缩放X倍”
	///		③XY有配置，Z留空，视为“X|Y|1”，代表“水平缩放，高度不缩放”
	///		④XYZ全部有配置，视为“X|Y|Z”，代表“全部自定义缩放”
	///	Param2：缩放淡入时间（秒，0代表“立即”）
	///	Param3：缩放淡出时间（同上）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold
	///	模型缩放表现：XYZ可以独立缩放、表现恢复“直接表现为目标大小”（@CST-886/@CST-5197）
	///	缩放结算：目标大小＝原大小×修正
	///注意：
	///	模型类特效，同类顶替：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountTalisman、BuffMountCarrier
	///	模型类特效，中断骑乘：若受术者为PC，则中断骑乘
	///	已知风险：若【变大过快】，可能因碰撞顶出方向判断规则，导致穿模（如“卡入地面”），请谨慎配置
	BuffChangeModelScale = 12 UMETA(DisplayName = "BuffChangeModelScale"),
	///BuffSlipInto（强制友好Buff）
	///	Param1~5：无
	///设计原意：
	///	（开挂的）强制让单位变成，和其他人互相友好
	///支持：
	///	继承：BuffHold
	///	强制友好表现：看谁/被谁看都是友好的（@CST-1947）
	///注意：
	///	关系类特效，同类顶替：BuffSlipInto
	BuffSlipInto = 13 UMETA(DisplayName = "BuffSlipInto"),
	///BuffChangePosture（模型替换姿态表现Buff）
	///	Param1：替换姿态模型ID（@DT_ModelCfg）|入场动作ID|离场动作ID
	///	Param2~5：无
	///设计原意：
	///	PC单位不需要更换衣服，但是换了一套动作（如重伤、发狂…等）
	///支持：
	///	继承：BuffHold
	///	替换姿态表现：不替换模型/部件/光效，只换动作表（@CST-1568）
	///	替换姿态“进/离场动作”表现：替换姿态前/后，主动播放一个动作（@CST-3427）
	///注意：
	///	受术者单位类型：PC限定
	///	模型类特效，同类顶替：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountTalisman、BuffMountCarrier
	///	模型类特效，中断骑乘：若受术者为PC，则中断骑乘
	///	已知风险：若模型ID错误，则表现为默认异常模型（SK_#404），请谨慎配置“模型ID”
	///	已知风险：若动画资源与单位骨骼不匹配，则可能产生报错，请谨慎配置“模型ID”（来源待定）
	BuffChangePosture = 14 UMETA(DisplayName = "BuffChangePosture"),
	///BuffBullet（子弹Buff）
	///	Param1：子弹列表（格式“子弹光效ID1:发射偏角1|子弹光效ID2:发射偏角2…”）
	///		子弹光效ID：带碰撞的光效配置（@DT_EffectCfg，留空代表“没有子弹”）
	///		发射偏角：带路径的子弹光效，可以自定义路径的偏转角度（缺省0度，右手螺旋法则）
	///	Param2：子弹碰撞时触发的技能ID（@DT_SkillCfg，留空代表“没有触发”）
	///	Param3：有效触发次数上限（次，≤0代表“次数不限”）
	///	Param4：子弹抵达时触发的技能ID（@DT_SkillCfg，留空代表“没有触发”）
	///	Param5：子弹撞墙时触发的技能ID（@DT_SkillCfg，留空代表“没有触发”）
	///设计原意：
	///	在施放之前不确定，需要由客户端模拟后才知道是否打中了的飞行子弹表现（作为技能和打击之间的桥梁）
	///支持：
	///	继承：BuffHold
	///	裁判机制（@CST-2110/@CST-4356）
	///	子弹表现：产生光效，光效碰撞/抵达/撞墙时，反馈给Buff，触发相应子弹技能（@CST-2110/@CST-2368/@CST-4203/@CST-9523）
	///	子弹方向偏移：可以调整光效的偏向，而无需重新定义光效（@CST-2354）
	///	防弹表现：拥有怪物标志位#25的单位是“防弹的”，若与子弹Buff施法者敌对，则中断子弹（@CST-4356）
	///注意：
	///	关于碰撞时：
	///		“碰撞”指“光效的静态网格物体组件碰到目标单位时”
	///			依赖“光效StaticMesh组件”相关配置支持（建议使用Standard系列标准碰撞资源）
	///			依赖“光效CollisionResponse组件”相关配置支持（默认配置即可支持子弹表现）
	///		“有效触发次数”依赖“碰撞触发”
	///			“防弹”、“抵达”、“撞墙”均不视为“碰撞”，不计有效触发次数
	///			“有效触发计数”的条件，由碰撞子技能的具体配置决定，触发的技能施展成功时，才视为有效触发，计数1次（@CST-4060）
	///			参数1中多个光效的触发次数由Buff统一计算，不作区分
	///		可以碰到“开启了真实碰撞标志位#24”的单位的静态部件（@CST-4238）
	///	关于抵达时：
	///		“抵达”指“飞行光效到达目标位置时”、“飞行路径完成指定次数后”
	///			依赖“光效脚本BP_FlyEffect”或“光效路径组件Spline”相关配置支持
	///	关于撞墙时：
	///		“撞墙”指“飞行光效检测到前方有墙壁时”（@CST-9523）
	///			依赖“光效CollisionResponse组件”相关配置支持（需要手动配置，默认配置不支持撞墙）
	///		“撞墙”时，将默认地移除光效
	///	已知风险：无法保障重新添加时的表现，请谨慎配置“下线保存”
	///	已知风险：若子弹所触发的子技能是“引导的”，则可能因施法者正在引导而施展失败，请谨慎配置“触发技能”（@CST-2110）
	///		建议子弹所触发的子技能使用“瞬发的、主动技能”，以保障表现正确
	BuffBullet = 15 UMETA(DisplayName = "BuffBullet"),
	///BuffFlyPatrolBind（御剑飞行Buff，未完成）
	///	Param1：飞行路径ID（@DT_FlyPatrolCfg）
	///	Param2：载具表现配置ID（@DT_CarrierCfg，留空代表“改为使用参数3”）
	///	Param3：御剑飞行骑乘表现配置ID（@DT_FlyCarrierCfg，若配置了参数2，则参数3无效）
	///	Param4~5：无
	///设计原意：
	///	希望整合“御剑飞行”的表现（扩展可被中断、可持有效果状态…等）
	///支持：
	///	继承：BuffHold
	///	御剑飞行表现：飞行→动作→路线→传送（@CST-572/@CST-1813）
	///注意：
	///	受术者单位类型：PC限定
	///	任务表现特效，同类免疫：BuffFlyPatrolBind
	BuffFlyPatrolBind = 16 UMETA(DisplayName = "BuffFlyPatrolBind"),
	///BuffPromptOper（界面引导使用道具表现Buff）
	///	Param1：地图ID（@DT_HashMapCfg，留空代表“立即给提示”）
	///		当前地图ID可以通过（/queryAttr spaceScriptID）查询
	///	Param2：目标位置坐标（虚幻坐标系，格式“X Y Z”，留空代表“使用施法者当前位置”）
	///	Param3：目标位置半径（靠近目标这个距离，触发表现）
	///	Param4：先判断是否技能ID（@DT_SkillCfg），再判断是否道具ID（@DT_ItemDataCfg）
	///	Param5：文字提示（留空代表“没有文字提示”）;界面偏移左|右（留空代表“居中显示”）
	///		示例：“提示;-10|10”，代表“界面偏左10%，偏下10%，写着提示”
	///支持：
	///	继承：BuffLoop
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	“道具使用引导”界面表现（@CST-2234）
	///		在Buff周期时（LoopTime），检测“是否满足提示显示要求”
	///注意：
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffPromptOper = 17 UMETA(DisplayName = "BuffPromptOper"),
	///BuffRise（垂直击飞Buff）
	///	Param1：动作ID1:起始帧时间1|动作ID2:起始帧时间2（秒）…（:冒号和|竖号分隔）
	///		示例：“Attack_01|Attack_02:0.5”，代表“顺序播放：从头开始的Attack_01、从0.5秒开始的Attack_02”
	///	Param2：击飞上升速度（米/秒）
	///	Param3：上升持续时间（秒，要求＞0，不得缺省）
	///		上升结束后，目标开始自由落体表现，但Buff持续时间内依然无法移动
	///	Param4~5：无
	///支持：
	///	继承：BuffHit
	///	情景免疫：被罡气格挡（@CST-2229）
	///	击飞表现：匀速上升→自由落体→结束（@CST-2478）
	///	支持动作起始帧时间设定（@CST-1192）
	///	支持播放连续动作：任一动作中断则中断连续动作；技能中断则中断对应的连续动作（@CST-3036）
	///	效果状态持有：受击状态（/queryAttr effectCounter，#3，第4个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止施法、禁止改变朝向、禁止主动移动、禁止跳跃、禁止交互
	///注意：
	///	受术者单位类型：PC限定
	///	击退类特效，同类顶替：BuffHitBack、BuffPull、BuffRise
	///	已知风险：无法保障重新添加时的表现，请谨慎配置“下线保存”
	///	已知风险：若上升持续时间≤Buff持续时间，则后续表现无效，请谨慎配置“上升持续时间”
	///	已知风险：若击飞动作的动作优先级低于JumpAir，则相关表现无效，表现为JumpAir，请谨慎配置“击飞动作”
	///		建议使用“优先级≥JumpAir”的击飞动作，以保障表现正确
	///	已知风险：【建议逐步弃用】建议替换为“给个眩晕Buff，和一个被动跳跃”，详见EffectForcedJump
	///反思：
	///	当时未有受迫跳跃支持，用来描述“类似击退的，被怼到天上”的表现
	///	现在继续使用已经不合适了，因为与击退、重力、吹风…等表现冲突
	BuffRise = 19 UMETA(DisplayName = "BuffRise"),
	///BuffLink（连线Buff，对应BuffBeLink）
	///	Param1：连线光效ID（@DT_EffectCfg，需要配合BP_BeamEffect使用）
	///	Param2：连线距离上限，距离超过上限时将中断连线（米）
	///	Param3~5：无
	///设计原意：
	///	从双方的方向进入AOI都可以准确恢复的连线光效表现
	///支持：
	///	继承：BuffLoop
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	连线Buff联动添加、移除（@CST-2568）
	///		需要配合BuffBeLink使用
	///		使用时【只添加BuffBeLink】，系统将会自动添加对应的BuffLink
	///		在Buff周期时（LoopTime），检测对应Buff是否存在，若不存在则中断自身（自尽）
	///	可重播连线表现（@CST-2568）
	///注意：
	///	使用方法：“通过对应BuffBeLink添加”限定
	///		直接添加BuffLink无效，应当添加对应的BuffBeLink
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffLink = 22 UMETA(DisplayName = "BuffLink"),
	///BuffBeLink（被连线Buff，对应BuffLink）
	///	Param1：对应“BuffLink”的BuffID（@DT_BuffCfg，不得缺省）
	///	Param2~5：无
	///设计原意：
	///	从双方的方向进入AOI都可以准确恢复的连线光效表现
	///支持：
	///	继承：BuffLoop
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	连线Buff联动添加、移除（@CST-2568）
	///		需要配合BuffLink使用
	///		使用时【只添加BuffBeLink】，系统将会自动添加对应的BuffLink
	///		在Buff周期时（LoopTime），检测对应Buff是否存在，若不存在则中断自身（自尽）
	///	可重播连线表现（@CST-2568）
	///注意：
	///	需要配合BuffLink使用
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffBeLink = 23 UMETA(DisplayName = "BuffBeLink"),
	///BuffMountTalisman（野外竞速专用，法宝骑乘Buff）
	///	Param1：延迟前进时间，配合上车动作表现用（秒）
	///	Param2：载具表现配置ID（@DT_CarrierCfg）
	///	Param3：转弯速度（待定）
	///	Param4：前进速度（米/秒）
	///	Param5：无
	///设计原意：
	///	野外竞速专用表现与模式
	///支持：
	///	继承：BuffHold
	///	竞速表现：坐上法宝，以指定速度自动前进，只能控制左右转弯（@CST-2139）
	///注意：
	///	受术者单位类型：PC限定
	///	模型类特效，同类顶替：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountTalisman、BuffMountCarrier
	///	已知风险：若延迟前进时间≥Buff持续时间，则后续表现无效，请谨慎配置“延迟前进时间”
	BuffMountTalisman = 24 UMETA(DisplayName = "BuffMountTalisman"),
	///BuffChangeTempCamp（改变临时阵营Buff）
	///	Param1：阵营类型（不得缺省）
	///		1：仙道（@csdefine.CAMP_TAOSIM）
	///		2：魔道
	///		3：中立敌对
	///		4：中立友好
	///		查询：可以通过【/queryAttr tempCamp】，查询【临时阵营】属性
	///	Param2~5：无
	///设计原意：
	///	（开挂的）临时改变敌对关系表现
	///支持：
	///	继承：BuffHold
	///	临时改变阵营：以改变敌对关系（@CST-2129）
	///		优先级：势力关系＞阵营关系（有势力关系时忽略阵营关系）
	///注意：
	///	关系类特效，同类顶替：BuffChangeTempCamp
	///	已知风险：【切忌】与AIAction#127、#128一同使用，将会使AI表现错乱，请谨慎使用
	///反思：
	///	此处参数1【不得缺省】的有效性检测方法，是特别的，不符合当前的参数规范
	///		利用已有概念CAMP_LIST，未导致概念变得更复杂
	///		只在初始化时有消耗，在运行时无消耗
	///		这是很好的特性，在将来的其他项目中可以考虑推广
	BuffChangeTempCamp = 25 UMETA(DisplayName = "BuffChangeTempCamp"),
	///BuffChangeTempFaction（改变临时势力Buff）
	///	Param1：势力类型（@DT_FactionRelationCfg.行号，不得缺省）
	///		查询：可以通过【/queryAttr tempFaction】，查询【临时势力】属性
	///	Param2~5：无
	///设计原意：
	///	（开挂的）临时改变敌对关系表现
	///支持：
	///	继承：BuffHold
	///	临时改变势力：以改变敌对关系（@CST-2129）
	///		优先级：势力关系＞阵营关系（有势力关系时忽略阵营关系）
	///注意：
	///	受术者单位类型：Monster、NPC限定（因为PC没有势力属性，另PC有阵营属性）
	///	关系类特效，同类顶替：BuffChangeTempFaction
	///	已知风险：若势力类型错误，则直到效果使用完毕都没有任何报错，配置错误相当难以发现，请谨慎配置“势力类型”
	///	已知风险：【切忌】与AIAction#127、#128一同使用，将会使AI表现错乱，请谨慎使用
	BuffChangeTempFaction = 26 UMETA(DisplayName = "BuffChangeTempFaction"),
	///BuffDistortScene（摄像机波浪扭曲表现Buff）
	///	Param1：淡入时间（秒，0代表“立即”）
	///	Param2：淡出时间（同上）
	///	Param3：扭曲强度（0代表“完全不动”，美术建议0.005 ~ 0.1）
	///	Param4：亮度滤镜修正 R|G|B（缺省“1|1|1”，代表“整体正常亮度”）
	///		R：画面红色亮度修正（如“1|0|0”，表现为“只剩下红色”）
	///		G：画面绿色亮度修正（如“0|0|0”，表现为“关灯了全都黑了”）
	///		B：画面蓝色亮度修正（如“2|2|1”，表现为“就像被额外的1|1|0的黄灯光照射”）
	///	Param5：色调蒙版修正 R|G|B|A（缺省“1|1|1|0”，代表“没有蒙版遮挡”）
	///		R：蒙版红色值（如“1|0|0|1”，代表“不透明的红色蒙版”）
	///		G：蒙版绿色值（如“1|0|0|0.5”，代表“半透明的红色蒙版”）
	///		B：蒙版蓝色值（如“0|0|0|0”，代表“全透明的黑色蒙版”）
	///		A：蒙版透明度（如“1|1|0|0.1”，代表“不透明度10%的黄色”，表现为“就像戴着淡淡的黄色太阳眼镜”）
	///设计原意：
	///	描述“类似喝醉了”的表现
	///支持：
	///	继承：BuffHold
	///	屏幕扭曲效果：画面扭曲、滤镜修正、蒙版修正（@CST-2377）
	///		滤镜修正可以理解为“原画面信息乘法修正”，不同颜色之间的差距一般会放大（对比度上升）
	///		蒙版修正可以理解为“原画面信息加法修正”，不同颜色之间的差距一般会缩小（对比度下降）
	///注意：
	///	摄像机类特效，同类顶替：BuffDistortScene
	BuffDistortScene = 27 UMETA(DisplayName = "BuffDistortScene"),
	///BuffShield（护盾Buff）
	///	Param1：允许响应的伤害类型列表（|竖号分隔，不得缺省）
	///		1：物理（外功）
	///		2：法术（内功）
	///		3：冰元素
	///		4：火元素
	///		5：雷元素
	///		6：玄元素
	///	Param2：护盾值百分比（缺省0.0） | 护盾值固定值（缺省0） | 护盾值上限倍率（缺省1.0倍，支持单独缺省）
	///		护盾值百分比（缺省0.0，如0.5代表"50%生命值上限"）
	///		护盾值固定值（缺省0点，护盾值＜0代表“护盾值不限”，护盾值＝0代表“轻轻一碰就破”）
	///		护盾值上限倍率（缺省1.0倍，＜1视为“1.0倍”，以简化配置逻辑）
	///	Param3：伤害吸收百分比（如0.5代表“吸收50%伤害”）|固定值（整型）
	///	Param4：抵挡次数（缺省-1次）|抵挡次数上限（缺省＝抵挡次数）
	///		抵挡次数（缺省-1次，＜0代表“次数不限”，＝0代表“轻轻一碰就破”）
	///		抵挡次数上限（缺省＝抵挡次数，＜0代表“抵挡次数的充能没有上限”）
	///	Param5：破盾反击技能ID（@DT_SkillCfg，需要配合“锁定目标的、瞬发的、主动技能”配置使用）
	///		技能申请者　【单位】＝护盾Buff持有者【单位】
	///		技能申请目标【单位】＝伤害效果施法者【单位】
	///支持：
	///	继承：BuffHold
	///	护盾结算：依据伤害量和当前护盾值，吸收伤害（@CST-2923/@CST-9952）
	///		伤害吸收量＝伤害量×伤害吸收百分比＋固定值
	///			有效范围：伤害吸收量≥0，伤害吸收量≤伤害量，伤害吸收量≤护盾当前值
	///		伤害量＝伤害量－伤害吸收量
	///		护盾当前值＝护盾当前值－伤害吸收量
	///	护盾量计算：现在可以与生命值上限相关了（@CST-12406）
	///		护盾值＝生命值上限×护盾值百分比＋护盾值固定值
	///		护盾值上限＝护盾值×护盾值上限倍率
	///	护盾充能：重复获得同ID的护盾Buff，可以补充护盾值和次数，刷新Buff持续时间（@CST-8457）
	///		充能不是叠加（不继承BuffStackable，不会使持有效果重复），只是表现有点像
	///	破盾触发：破盾触发反击技能申请（@CST-2923）
	///		破盾技能的触发时机在“Buff移除”之后，不享受持有效果
	///注意：
	///	已知风险：多个护盾，依据注册顺序先后触发；若伤害被前面的护盾吸收完了，后面的护盾可能不触发
	///	已知风险：护盾目前只影响EffectNormalDamage，不影响EffectDamage、EffectAbsorbHP（可参考农药里“真实伤害”与“护盾”的关系）
	///示例：
	///	①“当身技”表现
	///		Param1：1|2（代表“物理法术都可以”）
	///		Param2：0|-1（代表“护盾值不限”）
	///		Param3：0.9（代表“吸收90%”）
	///		Param4：1（代表“抵挡1次就破坏，触发破盾技能”）
	///		Param5：999001001（触发啥都行，此略）
	BuffShield = 28 UMETA(DisplayName = "BuffShield"),
	///BuffReSkillBarAndLoginTeleport（替换快捷栏Buff，登录时根据技能获取位置信息进行传送）
	///	Param1：传送判断技能ID（@DT_SkillCfg，不得缺省）
	///		需要配合EffectUseSkillByQuestID使用，以获取传送任务、位置信息
	///	Param2：传送技能ID（@DT_SkillCfg，若配置了参数2，则参数1无效）
	///		需要配合EffectTeleportSpace使用，以获取传送位置信息
	///	Param3~5：无
	///支持：
	///	继承：BuffHold
	///	替换快捷栏：直接替换快捷栏的图标（@CST-1719/@CST-1303）
	///	登录时根据技能获取位置信息进行传送（@CST-3039）
	///注意：
	///	受术者单位类型：PC限定
	///	界面类特效，同类顶替：BuffReplaceSkillBar、BuffReSkillBarAndLoginTeleport
	///反思：
	///	此处的参数设定互相冲突，理应合并，避免冗余
	///		应理解成“只有唯一的技能，优先级关系：传送技能＞传送判断技能”
	BuffReSkillBarAndLoginTeleport = 29 UMETA(DisplayName = "BuffReSkillBarAndLoginTeleport"),
	///BuffAim（进入瞄准状态，未完成验收）
	///	Param1~5：无
	///支持：
	///	未完成验收（@CST-3574）
	///	继承：BuffHold
	///	功能待定：灵岛危机副本玩法（@CST-3574）
	BuffAim = 30 UMETA(DisplayName = "BuffAim"),
	///BuffHoldJinDan（玩家怀抱金丹表现）
	///	Param1：替换姿态模型ID（@DT_ModelCfg）|入场动作ID|离场动作ID
	///	Param2：被抱金丹表现ID（@MeshBindTable）
	///	Param3：金丹爆炸技能ID，Buff结束时施放此技能，作爆炸表现（@DT_SkillCfg，不得缺省）
	///	Param4~5：无
	///支持：
	///	继承：BuffChangePosture
	///	功能待定：灵岛危机副本玩法（@CST-2936）
	BuffHoldJinDan = 31 UMETA(DisplayName = "BuffHoldJinDan"),
	///BuffHoldThroughCanyon（穿越峡谷专用，飞行滑翔Buff）
	///	Param1：载具表现配置ID（@DT_CarrierCfg，留空代表“改为使用参数3”）
	///	Param2：向前滑翔速度（厘米/秒）
	///	Param3：向下滑翔速度（同上）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold
	///	功能待定：穿越峡谷玩法，坐上飞行道具，并自动向前下方滑行（@CST-2146）
	///	速度叠加：支持与SkillCanyonCharge、多个EffectAddSpeed同时作用，速度表现为“矢量和”
	///注意：
	///	受术者单位类型：PC限定
	///	使用方法：“需要配合SkillCanyonCharge、EffectAddSpeed、陷阱行为TrapNormalSetTemp使用”限定
	BuffHoldThroughCanyon = 32 UMETA(DisplayName = "BuffHoldThroughCanyon"),
	///BuffReplace（可顶替Buff）
	///	Param1：Buff顶替ID（整型，要求＞0，不得缺省）
	///		Buff顶替ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：Buff顶替优先级（缺省0级）
	///		高级免疫低级：若有优先级更高的Buff，则添加失败
	///		平级互相顶替：若有优先级相同或更低的Buff，则顶替它们
	///	Param3~5：无
	///设计原意：
	///	实现“自定义的”Buff冲突关系
	///支持：
	///	继承：BuffLoop
	///	互相顶替：依据顶替类型和优先级，自定义同顶替类型的Buff之间的冲突关系（@CST-3600）
	BuffReplace = 33 UMETA(DisplayName = "BuffReplace"),
	///BuffGetMovingPlatFormControl（控制台子，改变视角）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	控制台子，改变视角（@CST-3250）
	BuffGetMovingPlatFormControl = 34 UMETA(DisplayName = "BuffGetMovingPlatFormControl"),
	///BuffUsurp（灵魂之誓专用，摄像机附身表现Buff）
	///	Param1：摄像机绑定的光效ID列表（@DT_EffectCfg，|竖号分隔）
	///	Param2：摄像机移动时间（秒，不得缺省）
	///	Param3：怪物销毁光效ID（@DT_EffectCfg，功能待定）
	///	Param4：特效延迟时间（秒，不得缺省）
	///	Param5：无
	///支持：
	///	继承：BuffHold
	///	灵魂之誓专用，摄像机附身表现：功能待定（@CST-3704）
	///注意：
	///	受术者单位类型：PC限定
	///	摄像机类特效，同类顶替：BuffUsurp
	BuffUsurp = 35 UMETA(DisplayName = "BuffUsurp"),
	///BuffLXDistortScene（屏幕旋涡扭曲Buff）
	///	Param1：旋转角度（功能待定）
	///	Param2：遮罩大小（功能待定）
	///	Param3：淡入时间（秒，0代表“立即”）
	///	Param4：淡出时间（同上）
	///	Param5：无
	///支持：
	///	继承：BuffHold
	///	屏幕旋涡扭曲（@CST-3030）
	///注意：
	///	摄像机类特效，同类顶替：BuffLXDistortScene
	///	已知风险：若淡入时间+淡出时间≤Buff持续时间，则后续表现无效，请谨慎配置“淡入/淡出时间”
	BuffLXDistortScene = 36 UMETA(DisplayName = "BuffLXDistortScene"),
	///BuffTaunt（嘲讽Buff）
	///	Param1：嘲讽距离要求（缺省10米，＜0视为“没有距离要求，不会因为距离太远而中断”）
	///		若施受双方之间，距离超过要求，则：①添加失败②中断
	///	Param2~5：无
	///支持：
	///	继承：BuffLoop
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	情景免疫（@CST-3740）
	///		自身免疫（不允许，嘲讽自己）
	///		不可战斗时免疫（不允许，嘲讽不可互相战斗的目标，如状态、敌对关系…等）
	///		距离太远时免疫（不允许，嘲讽不满足距离要求的目标）
	///	嘲讽距离要求：若施受双方之间，距离超过要求，则中断嘲讽Buff（@CST-3740）
	///		添加时，若距离超过要求，则添加失败
	///		在Buff周期时，检测距离是否超过要求，若超过要求则中断
	///	怪物被嘲讽表现：对于怪物，使施法者作为目标AI的“优先攻击目标”（@CST-3740）
	///		只影响“明确的通用战斗AIAction”（暂定：AIAction#4、#42、#66、#67、#71、#98），其他行为不受嘲讽影响
	///		目标不在附近时，依据原AI需求选取单位
	///	PC被嘲讽表现：切换操作模式，从已学习技能列表中挑选技能攻击目标（@CST-4560）
	///		目标不在附近时，待机不动
	///注意：
	///	操作类特效，同类顶替：BuffTaunt
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffTaunt = 37 UMETA(DisplayName = "BuffTaunt"),
	///BuffAddExtraSkillBar（额外快捷栏Buff）
	///	Param1：额外快捷栏的技能ID列表（@DT_SkillCfg，|竖号分隔，顺序显示，数量上限待定）
	///	Param2~5：无
	///支持：
	///	继承：BuffHold
	///	额外快捷栏：在界面上额外显示一个快捷栏，显示指定技能（@CST-3542）
	///注意：
	///	受术者单位类型：PC限定
	///	界面类特效，同类顶替：BuffAddExtraSkillBar
	///	已知风险：若技能ID错误，则服务器初始化时警告，请谨慎配置“技能ID”
	BuffAddExtraSkillBar = 38 UMETA(DisplayName = "BuffAddExtraSkillBar"),
	///BuffTPS（灵域狩魂专用，TPS射击模式Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	灵域狩魂专用，射击模式：功能待定（@CST-3232）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffTPS、BuffTPSParam
	///反思：
	///	此类操作模式，与机遇键鼠的操作界面有冲突，原则上都需要补充“智能切换Alt模式”等相关支持
	///	调试方法：目前可用【Shift+F1】临时呼出鼠标（方便UE4编辑器内的操作）
	BuffTPS = 39 UMETA(DisplayName = "BuffTPS"),
	///BuffRandomMultipleBullet（仙隐画院专用，多个方向随机发射子弹Buff）
	///	Param1：子弹光效ID1:数量1|光效ID2:数量2…（@DT_EffectCfg，:冒号和|竖号分隔，不得留空，不得部分缺省）
	///	Param2：子弹光效ID1:副本消息1|光效ID2:副本消息2…（@DT_EffectCfg，:冒号和|竖号分隔，不得留空，不得部分缺省）
	///	Param3：子弹碰到目标后，让目标播放的光效ID（@DT_EffectCfg）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold（注意，不是BuffBullet）
	///	仙隐画院专用子弹表现：莲花机关向多个随机的方向发射莲花，莲花碰撞到玩家后将对应的消息发送给副本，用于统计收集莲花个数（@CST-2962）
	///注意：
	///	已知风险：无法保障重新添加时的表现，请谨慎配置“下线保存”
	BuffRandomMultipleBullet = 40 UMETA(DisplayName = "BuffRandomMultipleBullet"),
	///BuffHost（主Buff，对应BuffGuest）
	///	Param1~5：无
	///设计原意：
	///	描述两个单位间“互相作用”的状态
	///支持：
	///	继承：BuffHold
	///	主从Buff联动添加、移除（@CST-3677）
	///		需要配合BuffGest使用
	///		使用时【只添加BuffGuest】，系统将会自动添加对应的BuffHost
	///		BuffGuest添加时，将会协助检测BuffHost的添加条件，以保障同时有效
	///注意：
	///	需要配合BuffGuest使用
	///	使用方法：“通过对应BuffGuest添加”限定
	///		直接添加BuffHost无效，应当添加对应的BuffGuest
	BuffHost = 41 UMETA(DisplayName = "BuffHost"),
	///BuffGuest（从Buff，对应BuffHost）
	///	Param1：对应的BuffHost的BuffID（@DT_BuffCfg，不得缺省）
	///	Param2~5：无
	///设计原意：
	///	描述两个单位间“互相作用”的状态
	///支持：
	///	继承：BuffHold
	///	主从Buff联动添加、移除（@CST-3677）
	///		需要配合BuffHost使用
	///		使用时【只添加BuffGuest】，系统将会自动添加对应的BuffHost
	///		BuffGuest添加时，将会协助检测BuffHost的添加条件，以保障同时有效
	///注意：
	///	需要配合BuffHost使用
	BuffGuest = 42 UMETA(DisplayName = "BuffGuest"),
	///BuffBeCapture（被抓取Buff，对应BuffCapture）
	///	Param1：对应的BuffCapture的BuffID（@DT_BuffCfg，不得缺省）
	///	Param2：抓取者插槽名称（被抓者的“胶囊中点”将绑定到抓取者身上的指定“抓取者插槽”中）
	///	Param3：插槽偏移位置（格式“X|Y|Z”，留空修正为“0|0|0”，不得部分缺省）
	///	Param4：插槽偏移方向（格式“X|Y|Z”，留空修正为“0|0|0”，不得部分缺省）
	///	Param5：无
	///设计原意：
	///	描述两个单位间“抓住丢来丢去”的表现
	///支持：
	///	继承：BuffGuest
	///	主从Buff联动添加、移除（@CST-3677）
	///		需要配合BuffCapture使用
	///		使用时【只添加BuffBeCapture】，系统将会自动添加对应的BuffCapture
	///		BuffBeCapture添加时，将会协助检测BuffCapture的添加条件，以保障同时有效
	///	情景免疫：简化抓取关系，规避互相抓取带来的表现混乱（@CST-3677）
	///		“抓取者”免疫“被抓”（不允许抓取链，不允许抓取自身）
	///		“被抓取者”免疫“抓人”和“被抓”（不允许抓取链）
	///	抓取表现：被抓取者以抓取者为位置基准，绑定在其指定骨骼点处（@CST-3677）
	///	效果状态持有：受击状态（/queryAttr effectCounter，#3，第4个）
	///	开关状态持有：禁止被击退（@CST-4800/@CST-3677）
	///		简化抓取表现，规避“被抓取者随意移动”所带来的表现混乱
	///注意：
	///	需要配合BuffCapture使用
	BuffBeCapture = 43 UMETA(DisplayName = "BuffBeCapture"),
	///BuffCapture（抓取Buff，对应BuffBeCapture）
	///	Param1~5：无
	///设计原意：
	///	描述两个单位间“抓住丢来丢去”的表现
	///支持：
	///	继承：BuffHost
	///	主从Buff联动添加、移除（@CST-3677）
	///		需要配合BuffBeCapture使用
	///		使用时【只添加BuffBeCapture】，系统将会自动添加对应的BuffCapture
	///		BuffBeCapture添加时，将会协助检测BuffCapture的添加条件，以保障同时有效
	///	情景免疫：简化抓取关系，规避互相抓取带来的表现混乱（@CST-3677）
	///		“抓取者”免疫“被抓”（不允许抓取链，不允许抓取自身）
	///		“被抓取者”免疫“抓人”和“被抓”（不允许抓取链）
	///	抓取表现：被抓取者以抓取者为位置基准，绑定在其指定骨骼点处（@CST-3677）
	///	开关状态持有：禁止被击退（@CST-3677）
	///		简化抓取表现，规避“被抓取者随意移动”所带来的表现混乱
	///注意：
	///	需要配合BuffBeCapture使用
	///	使用方法：“通过对应BuffBeCapture添加”限定
	///		直接添加BuffCapture无效，应当添加对应的BuffBeCapture
	BuffCapture = 44 UMETA(DisplayName = "BuffCapture"),
	///BuffAutoMoveForward（自动前进模式Buff）
	///	Param1：旋转角度
	///	Param2~5：无
	///支持：
	///	继承：BuffHold
	///	幻阵迷宫奇遇专用，玩家自动前进：功能待定（@CST-4020）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffAutoMoveForward
	BuffAutoMoveForward = 45 UMETA(DisplayName = "BuffAutoMoveForward"),
	///BuffQTE（QTE表现Buff）
	///	Param1：QTE配置ID（@DT_QteCfg）
	///	Param2：QTE成功技能ID（@DT_SkillCfg，留空代表“没有技能触发”）
	///	Param3：QTE失败技能ID（同上）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold
	///	通用的QTE表现（@CST-4407）
	///注意：
	///	受术者单位类型：PC限定
	///	界面类特效，同类顶替：BuffQTE
	BuffQTE = 46 UMETA(DisplayName = "BuffQTE"),
	///BuffEmissiveColor（模型自发光表现Buff）
	///	Param1：自发光颜色（格式“R|G|B”，建议范围0~1）
	///	Param2：自发光亮度（越大越亮，不得缺省）
	///		示例：“0”，代表“没有发光”
	///		示例：“1.0”，代表“看起来就是这个颜色”
	///	Param3~5：无
	///设计原意：
	///	描述“单位的颜色变了”
	///支持：
	///	继承：BuffHold
	///	单位材质自发光表现（@CST-4350）
	///注意：
	///	模型类特效，同类顶替：BuffEmissiveColor
	BuffEmissiveColor = 47 UMETA(DisplayName = "BuffEmissiveColor"),
	///BuffMountCarrier（骑乘载具Buff）
	///	Param1：载具表现配置ID（@DT_CarrierCfg）
	///	Param2：移除时创建单位ID（@DT_MonsterCfg，留空代表“不创建”）
	///	Param3：延迟创建单位时间（秒）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold
	///	通用的载具骑乘支持：骑乘及生蛋（@CST-4514）
	///注意：
	///	受术者单位类型：PC限定
	///	模型类特效，同类顶替：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountCarrier
	BuffMountCarrier = 48 UMETA(DisplayName = "BuffMountCarrier"),
	///BuffLingMai（灵脉Buff）
	///	Param1：离开领地多少距离，开始减少/增加灵能（米，不得缺省）
	///	Param2：增加的灵能点数（点，不得缺省）
	///	Param3~5：无
	///支持：
	///	继承：BuffLoop
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///		在Buff周期时（LoopTime），更新距离状态信息
	///	表现待定（@CST-4054）
	///注意：
	///	受术者单位类型：PC限定
	BuffLingMai = 49 UMETA(DisplayName = "BuffLingMai"),
	///BuffTransparency（模型渐变透明表现Buff）
	///	Param1：目标透明度（建议0.3、0.7两档，不得缺省）|起始透明度（缺省1）
	///		示例：“0.5”，代表“初始透明度是1.0，目标透明度是0.5”
	///		示例：“0.7|0.3”，代表“初始透明度是0.3，目标透明度是0.7”
	///	Param2：透明淡入时间（秒，＝0代表“立即”）
	///	Param3：透明淡出时间（同上）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold
	///	强调“逐渐改变”的半透明表现（@CST-4841）
	///注意：
	///	摄像机类特效，同类顶替：BuffTransparency
	///	已知风险：此渲染透明方案表现上有局限，请谨慎使用
	///		①同屏渲染透明表现，建议不多于3人（@CST-4650）
	///		②单位透明度，建议优先选择0.3、0.7、1.0，三个预设档次（@CST-4650）
	///		③渲染透明表现与“阴影”、“贴花”、“单位头顶UI”…等表现有冲突，建议主动规避（@CST-4841）
	///		④渲染透明表现之间互相冲突，优先级有：HoldEffectHide＞BuffTransparency（@CST-9111）
	BuffTransparency = 50 UMETA(DisplayName = "BuffTransparency"),
	///BuffAimShoot（天之幻境专用，射击模式Buff）
	///	Param1：Buff顶替ID（整型，要求＞0，不得缺省）
	///		Buff顶替ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：Buff顶替优先级（缺省0级）
	///		高级免疫低级：若有优先级更高的Buff，则添加失败
	///		平级互相顶替：若有优先级相同或更低的Buff，则顶替它们
	///	Param3：手持武器姿态的模型ID（@DT_ModelCfg）
	///	Param4：射击次数（-1代表“射击次数不限”）
	///	Param5：发射技能ID，检测使用次数用（@DT_SkillCfg）
	///支持：
	///	继承：BuffReplace
	///	天之幻境专用，射击模式表现：功能待定（@CST-4369、@CST-5288）
	///注意：
	///	受术者单位类型：PC限定
	BuffAimShoot = 51 UMETA(DisplayName = "BuffAimShoot"),
	///BuffAttackEnemy（周期性攻击敌人）
	///	Param1：Buff顶替ID（整型，要求＞0，不得缺省）
	///		Buff顶替ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：Buff顶替优先级（缺省0级）
	///		高级免疫低级：若有优先级更高的Buff，则添加失败
	///		平级互相顶替：若有优先级相同或更低的Buff，则顶替它们
	///	Param3：周期攻击使用的技能ID（@DT_SkillCfg，若是引导技能，则玩家无法施放自己的技能）
	///	Param4~5：无
	///支持：
	///	继承：BuffReplace
	///	周期性对“敌对列表中的第一个敌人”使用技能（@CST-4369、@CST-5288）
	BuffAttackEnemy = 52 UMETA(DisplayName = "BuffAttackEnemy"),
	///BuffAircraft（飞行器Buff）
	///	Param1：Buff顶替ID（整型，要求＞0，不得缺省）
	///		Buff顶替ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：Buff顶替优先级（缺省0级）
	///		高级免疫低级：若有优先级更高的Buff，则添加失败
	///		平级互相顶替：若有优先级相同或更低的Buff，则顶替它们
	///	Param3：飞行模型配置ID（@DT_FlyBindActorCfg）
	///	Param4：怪物ID列表（@DT_MonsterCfg，|竖号分隔，功能待定）
	///	Param5：范围|单位类型|高度（功能待定）
	///支持：
	///	继承：BuffReplace
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///		在Buff周期时（LoopTime），下达攻击指令或表现
	///	天之幻境专用，青光剑表现：使用后，青光剑会飞到头顶，当半径15米内出现敌方目标便会自动飞过去攻击目标，对目标造成连击技能的控制及伤害。（@CST-4369）
	///	主动攻击：攻击Buff持有者的敌人列表首位，若敌人列表为空，则修正为“主动攻击周围的指定怪物”
	///注意：
	///	受术者单位类型：PC限定
	BuffAircraft = 53 UMETA(DisplayName = "BuffAircraft"),
	///BuffThrowJinDan（十方城专用，扔金丹Buff）
	///	Param1：替换姿态模型ID（@DT_ModelCfg）|入场动作ID|离场动作ID
	///	Param2：金丹表现用，模型挂件配置ID（@DT_MeshBindCfg）
	///	Param3：金丹爆炸技能ID，Buff结束时施放此技能，作爆炸表现（@DT_SkillCfg，不得缺省）
	///	Param4：显示金丹头顶显示倒计时的BuffID、配合扔金丹的Tips用（@DT_BuffCfg）
	///	Param5：无
	///支持：
	///	继承：BuffChangePosture
	///	十方城专用，扔金丹表现：功能待定（@CST-5457）
	BuffThrowJinDan = 54 UMETA(DisplayName = "BuffThrowJinDan"),
	///BuffHook（钩取Buff，对应BuffBeHook）
	///	Param1：连线光效ID（@DT_EffectCfg，需要配合BP_BeamEffect使用）
	///	Param2：连线中断距离，超过上限将中断连线（米）
	///	Param3：抓取截止距离，超过下限将中断连线，并触发技能（米）
	///	Param4：抓取截止触发的技能ID（@DT_SkillCfg，留空代表“没有触发”）
	///	Param5：无
	///支持：
	///	继承：BuffLink
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	连线Buff联动添加、移除（@CST-5559）
	///		需要配合BuffBeHook使用
	///		使用时【只添加BuffBeHook】，系统将会自动添加对应的BuffHook
	///		在Buff周期时（LoopTime），检测对应Buff是否存在，若不存在则中断自身（自尽）
	///	钩取表现：功能待定（@CST-5559）
	///注意：
	///	使用方法：“通过对应BuffBeHook添加”限定
	///		直接添加BuffHook无效，应当添加对应的BuffBeHook
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffHook = 55 UMETA(DisplayName = "BuffHook"),
	///BuffBeHook（被钩取Buff，对应BuffHook）
	///	Param1：对应“BuffHook”的BuffID（@DT_BuffCfg，不得缺省）
	///	Param2：钩取速度（缺省0米/秒，≤0代表“不会钩取移动”）
	///	Param3~5：无
	///支持：
	///	继承：BuffBeLink
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	连线Buff联动添加、移除（@CST-5559）
	///		需要配合BuffHook使用
	///		使用时【只添加BuffBeHook】，系统将会自动添加对应的BuffHook
	///		在Buff周期时（LoopTime），检测对应Buff是否存在，若不存在则中断自身（自尽）
	///	钩取表现：待定（@CST-5559）
	///	效果状态持有：表演状态（/queryAttr effectCounter，#12，第13个）
	///注意：
	///	受术者单位类型：非PC限定（因为依赖服务器相关移动方法）
	///	需要配合BuffHook使用
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffBeHook = 56 UMETA(DisplayName = "BuffBeHook"),
	///BuffShenfengMiJing（神风秘径专用，玩家骑老鹰模式Buff）
	///	Param1：（已废弃）老鹰单位ID（@DT_MonsterCfg）
	///	Param2：（已废弃）老鹰刷新点位置“X Y Z”
	///	Param3：（已废弃）老鹰刷新点朝向“X Y Z”
	///	Param4：飞行路线（@DT_FXLXCfg）
	///	Param5：无
	///支持：
	///	继承：BuffLoop
	///	神风秘径专用，玩家骑上啸风鹰表现：功能待定（@CST-5559）
	BuffShenfengMiJing = 57 UMETA(DisplayName = "BuffShenfengMiJing"),
	///BuffTPSParam（自定义参数射击模式Buff）
	///	Param1：摄像机的俯仰视角，下限|上限（角度）
	///		示例：如“-15|45”，代表“往下可以看15度，往上可以看45度”
	///	Param2：摄像机的臂长|距离（待定）
	///	Param3~5：无
	///支持：
	///	继承：BuffHold
	///	射击模式：功能待定（@CST-5969）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffTPS、BuffTPSParam
	///	参数表现受限于游戏过程标准模式下的参数范围
	///		摄像机的俯仰角度，有效范围约[-60°,60°]
	///		摄像机的臂长，有效范围待定
	///反思：
	///	此类操作模式，与机遇键鼠的操作界面有冲突，原则上都需要补充“智能切换Alt模式”等相关支持
	///	调试方法：目前可用【Shift+F1】临时呼出鼠标（方便UE4编辑器内的操作）
	BuffTPSParam = 58 UMETA(DisplayName = "BuffTPSParam"),
	///BuffPromptOperShowArea（金树种子专用，道具使用引导界面Buff）
	///	Param1：地图ID（@DT_HashMapCfg，留空代表“立即给提示”）
	///		当前地图ID可以通过（/queryAttr spaceScriptID）查询
	///	Param2：目标位置坐标（虚幻坐标系，格式“X Y Z”，留空代表“使用施法者当前位置”）
	///	Param3：目标位置半径（靠近目标这个距离，触发表现）
	///	Param4：先判断是否技能ID（@DT_SkillCfg），再判断是否道具ID（@DT_ItemDataCfg）
	///	Param5：文字提示（留空代表“没有文字提示”）;界面偏移左|右（留空代表“居中显示”）
	///		示例：“提示;-10|10”，代表“界面偏左10%，偏下10%，写着提示”
	///支持：
	///	继承：BuffPromptOper
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	金树种子专用，会在大地图显示目标区域（@CST-2234）
	///注意：
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffPromptOperShowArea = 59 UMETA(DisplayName = "BuffPromptOperShowArea"),
	///BuffItemGrey（物品置灰Buff）
	///	Param1：需要置灰的物品ID（@DT_ItemDataCfg）
	///	Param2~5：无
	///支持：
	///	继承：BuffHold
	///	依据物品ID将道具置灰，不允许使用（@CST-5772）
	BuffItemGrey = 60 UMETA(DisplayName = "BuffItemGrey"),
	///BuffIncludePet（阵营相关支持，联动幻兽Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	阵营相关支持：功能待定（@CST-5967，未完成验收）
	BuffIncludePet = 61 UMETA(DisplayName = "BuffIncludePet"),
	///BuffAimingThrowMode（晶石洞窟专用，瞄准模式Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	晶石洞窟专用，瞄准模式：功能待定（@CST-6101，未完成验收）
	BuffAimingThrowMode = 62 UMETA(DisplayName = "BuffAimingThrowMode"),
	///BuffConstantFall（缓慢下落Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	缓慢下落表现：缓慢下落，避免摔死（@CST-5903）
	///注意：
	///	受术者单位类型：PC限定
	BuffConstantFall = 63 UMETA(DisplayName = "BuffConstantFall"),
	///BuffFog（迷雾Buff）
	///	Param1：迷雾表现类型（不得缺省）
	///		1：迷雾逐渐靠近摄像机
	///		2：迷雾原地渐变生成
	///	Param2：开始迷雾浓度|可视距离|过渡系数（不得留空）
	///	Param3：结束迷雾浓度|可视距离|过渡系数（同上）
	///	Param4：淡入时间|淡出时间（秒）
	///	Param5：无
	///支持：
	///	继承：BuffHold
	///	功能待定（@CST-6390）
	///注意：
	///	受术者单位类型：PC限定
	BuffFog = 64 UMETA(DisplayName = "BuffFog"),
	///BuffPLMJCarrierUI（蟠龙秘境专用，UI表现Buff）
	///	Param1：法宝骑乘模式BuffID，作龙鳞载具表现用（@DT_BuffCfg）
	///	Param2：免伤BuffID（@DT_BuffCfg，功能待定）
	///	Param3~5：无
	///支持：
	///	继承：BuffHold
	///	蟠龙秘境专用的UI表现：持续显示一个“开始按钮”，按一下获得两个Buff，再按一下去掉两个Buff（@CST-6262）
	///注意：
	///	受术者单位类型：PC限定
	BuffPLMJCarrierUI = 65 UMETA(DisplayName = "BuffPLMJCarrierUI"),
	///BuffAutoRise（冥域缉凶专用，自动上升模式Buff）
	///	Param1：上升速度（米/秒）
	///	Param2：左右移动速度（米/秒）
	///	Param3：摄像机与玩家距离（米）
	///	Param4~5：无
	///支持：
	///	继承：BuffHold
	///	冥域缉凶专用，自动上升表现：功能待定（@CST-6526）
	///	开关状态持有：禁止施法
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffAutoRise
	BuffAutoRise = 66 UMETA(DisplayName = "BuffAutoRise"),
	///BuffMountSlide（冰霜山脉专用，骑乘滑板模式Buff）
	///	Param1：延迟移动时间（秒）
	///	Param2：初始速度|最大速度（米/秒）
	///	Param3：加速度（缺省5米/秒²，用于描述“在斜坡往下滑，下坡加速”的表现）
	///	Param4：载具表现配置ID（@DT_CarrierCfg，决定骑乘表现，留空代表“没有骑乘表现，自己用脚跑”）
	///	Param5：摄像机左右转动倍率（缺省5倍）
	///支持：
	///	继承：BuffHold
	///	冰霜山脉专用，骑乘滑板表现：坐上雪橇，逐渐加速前进，只能控制左右转弯（@CST-8358）
	///注意：
	///	受术者单位类型：PC限定
	///	操作模式特效，同类顶替：BuffHSBZModelTPS
	///	模型类特效，中断骑乘：若受术者为PC，则中断骑乘
	///	开关状态持有：禁止主动移动
	///反思：
	///	此类操作模式，与机遇键鼠的操作界面有冲突，原则上都需要补充“智能切换Alt模式”等相关支持
	///	调试方法：目前可用【Shift+F1】临时呼出鼠标（方便UE4编辑器内的操作）
	BuffMountSlide = 67 UMETA(DisplayName = "BuffMountSlide"),
	///BuffControlXianzhou（仙舟渡劫专用，控制仙舟Buff）
	/// Param1：仙舟的scriptID
	///	Param2~5：无
	///支持：
	///	继承：BuffHold
	///	仙舟渡劫专用，控制仙舟：功能待定（@CST-8730，未验收）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffControlXianzhou
	BuffControlXianzhou = 68 UMETA(DisplayName = "BuffControlXianzhou"),
	///BuffOverLookScene（摄像机俯瞰Buff）
	///	Param1：指定摄像机世界位置（格式“X|Y|Z”，留空代表“0|0|0”）
	///	Param2：指定摄像机世界旋转（格式“X|Y|Z”，留空代表“0|0|0”）
	///	Param3：表现淡入时间（秒，≤0代表“立刻”）
	///	Param4：表现持续时间（秒，≤0代表“永久”）
	///	Param5：表现淡出时间（秒，≤0代表“立刻”）
	///支持：
	///	继承：BuffHold
	///	摄像机俯瞰表现：将PC的摄像机平滑移动到目标位置，再回到原位（@CST-8051）
	///注意：
	///	受术者单位类型：PC限定
	///	摄像机类特效，同类顶替：BuffOverLookScene
	BuffOverLookScene = 69 UMETA(DisplayName = "BuffOverLookScene"),
	///BuffRespond（事件响应Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	事件响应打击表现：Buff持有者触发指定事件时，Buff施法者向Buff持有者申请“事件触发打击”（@CST-8362）
	///		打击施法者＝（Buff的）施法者
	///		打击目标　＝（Buff的）持有者
	///注意：
	///	触发时机在“响应事件中断”之前，可享受持有效果
	///示例：
	///	①只触发一次打击，然后移除Buff（同时配置“响应中断”和“响应打击”，即可）
	BuffRespond = 71 UMETA(DisplayName = "BuffRespond"),
	///BuffYCJMDTPS（勇闯绝命岛专用，射击模式Buff）
	///	Param1：左键点击使用的技能ID|对应高亮的技能ID|鼠标右键模式的buffID（@DT_SkillCfg）
	///	Param2：显示图标用，武器物品ID（@DT_ItemDataCfg，0代表“没有图标”）
	///	Param3：替换姿态模型ID（@DT_ModelCfg）|入场动作ID|离场动作ID
	///	Param4：替换武器类型|插槽名称|武器部件ID（@DT_ModelPartCfg）
	///	　替换武器类型：（由代码写死，详细情况可联系@冉渊）
	///		0：无武器
	///		1：手弩
	///		2：十字弩
	///		示例：“3|Socket_Weapon_R_nujian|SM_ZW0352”，代表“武器装备对应单手弩，插槽和部件如配置所示”
	///	Param5：快捷栏类型1:对应配置1|快捷栏类型2:对应配置2…（:冒号和|竖号分隔，支持最多9个格子）
	///	　快捷栏类型：（缺省0）
	///		0：空格子（@csdefine.QB_ITEM_NONE）
	///		1：玩家技能
	///		3：背包道具
	///	　对应配置格式：
	///		对应“0：空格子”　：无
	///		对应“1：玩家技能”：技能ID（@DT_SkillCfg，不得缺省）
	///		对应“3：背包道具”：道具ID（@DT_ItemDataCfg，不得缺省）
	///	　示例：“0|1:911001001|3:202010001”，代表“第1格是空格子，第2格是技能，第3格是道具
	///支持：
	///	继承：BuffHold
	///	勇闯绝命岛专用，射击模式Buff：还配套支持了，替换快捷栏、替换姿态、替换武器等（@CST-8973）
	///		可按Alt键呼出鼠标
	///	远程射击相关表现支持：替换武器（@CST-10405）
	///	同ID免疫：重复获得同ID的此Buff时，将免疫新Buff的添加（@CST-10405）
	///注意：
	///	受术者单位类型：PC限定
	///	语境类特效，互相顶替：BuffYCJMDTPS
	///		免疫、顶替，模型类特效：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountCarrier
	///	已知风险：目前还有诸多表现问题未处理完毕，请谨慎使用（@CST-10405）
	BuffYCJMDTPS = 72 UMETA(DisplayName = "BuffYCJMDTPS"),
	///BuffDark（漆黑山洞表现Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffHold
	///	漆黑山洞表现：玩家处于一片漆黑中（@CST-7524）
	///注意：
	///	受术者单位类型：PC限定
	///	场景类特效，同类顶替：BuffDark
	BuffDark = 73 UMETA(DisplayName = "BuffDark"),
	///BuffLight（能照明玩家一定范围）
	///	Param1：照明范围（米）
	///	Param2~5：无
	///支持：
	///	继承：BuffHold
	///	漆黑山洞表现：在漆黑的山洞里，照亮周围（@CST-7524）
	///注意：
	///	受术者单位类型：PC限定
	///	场景类特效，同类顶替：BuffLight
	BuffLight = 74 UMETA(DisplayName = "BuffLight"),
	///BuffClientHold（持有客户端Buff）
	///	Param1~5：无
	///支持：
	///	客户端版本的BuffHold（@CST-9038）
	BuffClientHold = 75 UMETA(DisplayName = "BuffClientHold"),
	///BuffClientHit（客户端打击Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffClientHold
	///	客户端版本的BuffHit（@CST-9038）
	BuffClientHit = 76 UMETA(DisplayName = "BuffClientHit"),
	///BuffClientLoop（客户端周期Buff）
	///	Param1~5：无
	///支持：
	///	继承：BuffClientHit
	///	客户端版本的BuffLoop（@CST-9038）
		BuffClientLoop = 77 UMETA(DisplayName = "BuffClientLoop"),
	///BuffClientStackable（客户端可叠加Buff）
	///	Param1：叠加层数上限（缺省1层，≤0修正为“上限1层”）
	///	Param2~5：无
	///支持：
	///	继承：BuffClientLoop
	///	客户端版本的BuffStackable（@CST-9038）
	BuffClientStackable = 78 UMETA(DisplayName = "BuffClientStackable"),
	///BuffClientHitBack（客户端击退Buff）
	///	Param1：击退动作ID:起始帧时间（秒）
	///	Param2：起身动作ID:起始帧时间（秒）
	///	Param3：击退时间（秒）|起身时间（秒，起身动作ID有效时生效）
	///	Param4：击退距离下限（缺省0米）|上限（缺省＝下限）
	///		服务器位移速度有≤50米/秒的限制，实际上为了同步表现正确，建议速度表现≤25米/秒
	///	Param5：改变朝向类型|击退方向类型（不得缺省）
	///	　改变朝向类型（先【转向】，后击退）
	///		0：同“施法者当前朝向”（表现为“和施法者看相同的方向”）
	///		1：逆“施法者当前朝向”（表现为“和施法者看相反的方向”）
	///		2：施法者→受术者方向（表现为“背对施法者”，若位置重叠则修正为“施法者当前朝向”）
	///		3：受术者→施法者方向（表现为“围观施法者”，若位置重叠则修正为“受术者当前朝向”）
	///		4：同“受术者当前朝向”（表现为“受术者刷新朝向”）
	///		5：逆“受术者当前朝向”（表现为“受术者向后转”）
	///	　击退方向类型（先转向，后【击退】）
	///		0：同“施法者当前朝向”（表现为“整齐地，推走”）
	///		1：逆“施法者当前朝向”（表现为“整齐地，拉回”）
	///		2：施法者→受术者方向（表现为“分散地，推走”，若位置重叠则修正为“施法者当前朝向”）
	///		3：受术者→施法者方向（表现为“分散地，拉回”，若位置重叠则修正为“受术者当前朝向”）
	///		4：同“受术者当前朝向”（表现为“受术者向前扑街”）
	///		5：逆“受术者当前朝向”（表现为“受术者向后摔跤”）
	///		示例：“5|5”，代表“目标先【向后转】，然后再【往（新的）后方摔倒】”
	///支持：
	///	继承：BuffClientHit
	///	客户端版本的BuffHitBack（@CST-9038）
	///	受击状态、击退表现：击退动作→转向→位移→位移停止→起身动作→结束（@CST-1325）
	///	效果状态持有：受击状态（/queryAttr effectCounter，#3，第4个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止施法、禁止改变朝向、禁止主动移动、禁止跳跃、禁止交互
	///注意：
	///	击退类特效，同类顶替：BuffClientHitBack
	///	已知风险：无法保障重新添加时的表现，请谨慎配置“下线保存”
	///	已知风险：若击退时间≤Buff持续时间，则后续表现无效，请谨慎配置“击退时间”
	BuffClientHitBack = 79 UMETA(DisplayName = "BuffClientHitBack"),
	///BuffHSBZModelTPS（轮回秘境专用，幻兽捕捉射击模式Buff）
	///	Param1：对应施放的技能ID（@DT_SkillCfg）
	///	Param2：对应使用的物品ID（@DT_ItemDataCfg）
	///	Param3~5：无
	///支持：
	///	继承：BuffHold
	///	轮回秘境专用，幻兽捕捉射击模式表现：功能待定（@CST-9310）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffHSBZModelTPS
	///反思：
	///	此类操作模式，与机遇键鼠的操作界面有冲突，原则上都需要补充“智能切换Alt模式”等相关支持
	///	调试方法：目前可用【Shift+F1】临时呼出鼠标（方便UE4编辑器内的操作）
	BuffHSBZModelTPS = 80 UMETA(DisplayName = "BuffHSBZModelTPS"),
	///BuffParachuteLand（勇闯绝命岛专用，跳伞降落模式Buff）
	///	Param1：男战士|男剑客|男链刃|男法师的跳伞表现模型ID（@DT_ModelCfg，不得留空）
	///	Param2：女战士|女剑客|女链刃|女法师的跳伞表现模型ID（同上）
	///	Param3~5：无
	///支持：
	///	继承：BuffHold
	///	勇闯绝命岛专用，跳伞降落表现：功能待定（@CST-9960）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效，同类顶替：BuffParachuteLand
	BuffParachuteLand = 81 UMETA(DisplayName = "BuffParachuteLand"),
	///BuffRuDao（九字真言专用，入道Buff）
	///	Param1-5：无
	///支持：
	///	继承：BuffStackable
	///	九字真言专用，入道Buff：功能待定（@CST-4246）
	///注意：
	///	受术者单位类型：PC限定
	///	操作类特效：功能待定
	BuffRuDao = 82 UMETA(DisplayName = "BuffRuDao"),
	///BuffJZZYMieDeng（九字真言专用，入道Buff）
	///	Param1：灭灯数量（待定）
	///	Param2-5：无
	///支持：
	///	继承：BuffHold
	///	九字真言专用，灭灯：功能待定（@CST-4246）
	///注意：
	///	受术者单位类型：Monster限定
	///	操作类特效：功能待定
	BuffJZZYMieDeng = 83 UMETA(DisplayName = "BuffJZZYMieDeng"),
	///BuffAddPrefixName（自定义名称前缀Buff）
	///	Param1：名称前缀（文本，建议＜10字）
	///		名称前缀可以通过（/queryAttr prefixName）查询
	///		名称前缀可以通过（/setAttr prefixName "前缀名"）设置调试
	///	Param2-5：无
	///支持：
	///	继承：BuffHold
	///	自定义名称前缀表现：名称前显示前缀，形如【<前缀>名称】（@CST-10643）
	///注意：
	///	已知风险：目前所有单位都支持此属性，但是NPC不支持Buff，所以不支持，请谨慎使用（@CST-10643）
	///	已知风险：目前GM指令输入文本值的正确方法还不明确，双引号本身的输入方法待定，请谨慎使用（@CST-10643）
	BuffAddPrefixName = 84 UMETA(DisplayName = "BuffAddPrefixName"),
	///BuffGhostEye（勇闯绝命岛专用，鬼瞳Buff）
	///	Param1：鬼曈脚本ID（待定）
	///	Param2：最大可探距离（不得超过200米，当距离大于AOI距离时，取AOI距离）
	///	Param3：向前偏移|向左偏移
	///	Param4-5：无
	///支持：
	///	继承：BuffLoop
	///		默认值脚本修正：LoopTime＝0时，将自动校正为1秒，以规范配置与表现（@CST-9200）
	///	鬼瞳表现：待定（@CST-10390）
	///注意：
	///	已知风险：LoopTime≤0时，BuffLoop将跳过周期触发，周期距离检测将失效，请谨慎使用
	BuffGhostEye = 85 UMETA(DisplayName = "BuffGhostEye"),
	///BuffMountSlideExt（冰霜山脉专用，骑乘滑板模式Buff BuffMountSlide的另一个版本的表现）
	///	Param1：延迟移动时间（秒）
	///	Param2：初始速度|最大速度（米/秒）
	///	Param3：加速度（缺省5米/秒²，用于描述“在斜坡往下滑，下坡加速”的表现）
	///	Param4：载具表现配置ID（@DT_CarrierCfg，决定骑乘表现，留空代表“没有骑乘表现，自己用脚跑”）
	///	Param5：摄像机左右转动倍率（缺省5倍）
	///支持：
	///	继承：BuffHold
	///	冰霜山脉专用，骑乘滑板表现：坐上雪橇，逐渐加速前进，只能控制左右转弯（@CST-8358、@CST-9039）
	///注意：
	///	受术者单位类型：PC限定
	///	操作模式特效，同类顶替：BuffHSBZModelTPS
	///	模型类特效，中断骑乘：若受术者为PC，则中断骑乘
	///	开关状态持有：禁止主动移动
	///反思：
	///	此类操作模式，与机遇键鼠的操作界面有冲突，原则上都需要补充“智能切换Alt模式”等相关支持
	///	调试方法：目前可用【Shift+F1】临时呼出鼠标（方便UE4编辑器内的操作）
		BuffMountSlideExt = 86 UMETA(DisplayName = "BuffMountSlideExt"),		
		///BuffEnergyLevel（能量等级Buff）
		///	Param1：能量初值|能量上限（都是整数，能量下限0无需设置）
		///	Param2：能量下界1;持有效果:持有效果:持有效果…|能量下界2;持有效果:持有效果:持有效果…|……
		///			（能量值决定唯一的当前能级，能量值＜第一个下界时，没有持有效果）
		///	Param3：原能量值要求类型;数量指;新能量值要求类型;数量指标;触发技能|…… 
		///			（申请者＝Buff持有者，申请目标＝充能施法者，技能＝主动瞬发技能）
		///			要求类型（不得缺省）
		///			0：＝等于
		///			1：＞大于
		///			2：＜小于
		///			3：≥大于等于
		///			4：≤小于等于
		///			5：≠不等于
		///	Param4：触发中断能量要求求列表（新能量值要求类型|数量指标）
		///	Param5：标记列表
		///		  标记：IsLocal，是施法者独占交互（包括添加Buff是否成功、充能/消耗效果是否成功）  
		///支持：
		///	继承：BuffLoop
		BuffEnergyLevel = 87 UMETA(DisplayName = "BuffEnergyLevel"),
		///BuffPLMJMountCarrier（野外竞速专用，法宝骑乘Buff）
		///	Param1：延迟前进时间，配合上车动作表现用（秒）
		///	Param2：载具表现配置ID（@DT_CarrierCfg）
		///	Param3：转弯速度（待定）
		///	Param4：前进速度（米/秒）
		///	Param5：无
		///设计原意：
		///	野外竞速专用表现与模式
		///支持：
		///	继承：BuffMountTalisman，只在buff结束时，通知界面显示按钮可点击CST-13639
		///	竞速表现：坐上法宝，以指定速度自动前进，只能控制左右转弯（@CST-2139）
		///注意：
		///	受术者单位类型：PC限定
		///	模型类特效，同类顶替：BuffChangeBody、BuffChangePosture、BuffChangeModelScale、BuffMountTalisman、BuffMountCarrier
		///	已知风险：若延迟前进时间≥Buff持续时间，则后续表现无效，请谨慎配置“延迟前进时间”
		BuffPLMJMountCarrier = 88 UMETA(DisplayName = "BuffPLMJMountCarrier"),
};

UENUM(BlueprintType)
enum class ENUM_BUFF_SAVE_TYPE : uint8
{
	///NotSave（不保存）
	NotSave = 0 UMETA(DisplayName = "NotSave"),
	///ContinueTime（下线保存，继续计时）
	///注意：
	///	重新上线时，可能因为“已经过期”，而重新添加失败
	ContinueTime = 1 UMETA(DisplayName = "ContinueTime"),
	///NotContinueTime（下线保存，冻结计时）
	NotContinueTime = 2 UMETA(DisplayName = "NotContinueTime"),
	///AgainTime（下线保存，重新计时）
	AgainTime = 3 UMETA(DisplayName = "AgainTime"),
};

///Buff打击
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBUFF_HIT
{
	GENERATED_BODY()
	///打击作用范围
	///支持：
	///	选择受术者的初始方法
	UPROPERTY(EditAnywhere)
		FSKILL_HIT_AREA HitArea;
	///受术者条件列表
	///支持：
	///	判断“施法者→受术者”的条件是否满足，把不满足条件的受术者排除（如“对HP≤10%的目标造成斩杀”）
	///注意：
	///	若因受术者无效而导致执行失败（如“缺少属性”），则视为“失败”（@CST-2113）
	UPROPERTY(EditAnywhere)
		TArray<FSKILL_USE_CONDITION> ReceiverCondition;
	///受术者排序列表
	///支持：
	///	使受术者按需排序，并选择前几个受术者（如“攻击血量最少的3个目标”）
	///注意：
	///	若因受术者无效而导致执行失败（如“缺少属性”），则视为“移至队末”（@CST-2113）
	UPROPERTY(EditAnywhere)
		TArray<FRECEIVER_FLITER_CONDITION> FilterCondition;
	///打击命中类型
	///支持：
	///	应当理解为“对受术者列表依据命中判定进行筛选”，是让一部分受术者免受打击的方法
	///注意：
	///	流程上应当在“条件筛选”之后、“排序筛选”之前
	///	若因受术者无效而导致执行失败（如“缺少属性”），则视为“未命中”（@CST-2113）
	UPROPERTY(EditAnywhere)
		ENUM_HIT_TYPE HitType = ENUM_HIT_TYPE::HitDodge;
	///打击效果列表
	///支持：
	///	“施法者→受术者”添加技能效果（如“伤害”、“表现”…等）
	///注意：
	///	若因受术者无效而导致执行失败（如“缺少属性”），则视为“免疫该效果”（@CST-2113）
	///	若因受术者无效而导致触发失败（如“不支持触发”），则跳过触发流程（@CST-2113）
	UPROPERTY(EditAnywhere)
		TArray<FHIT_EFFECT> EffectList;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBUFF_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///Buff名称
	///支持：
	///	界面显示、技能反馈显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffName")
		FString BuffName;
	///Buff图标
	///支持：
	///	界面显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffIcon")
		TSoftObjectPtr<UTexture2D> BuffIcon;
	///Buff品质
	///	0：没有自定义品质，没有外框显示
	///	1：白色（白色边框）
	///	2：蓝色（蓝色边框）
	///	3：金色（金色边框）
	///	4：粉色（粉色边框）
	///	5：地阶（绿色边框）
	///	6：天阶（绿色边框）
	///	7：圣阶（绿色边框＋流光）
	///	8：神阶（绿色边框＋闪电）
	///支持：
	///	界面显示（@CST-11464）
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Quality")
		int32 Quality = 0;
	///Buff等级（级）
	///支持：
	///	界面显示（@CST-12843）
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffLevel")
		uint8 BuffLevel;
	///自定义“状态性质”显示（文本）
	///支持：
	///	界面显示：自定义Buff信息界面上的“状态性质”（@CST-12843）
	///		当此处有值时，优先显示此处的自定义值；当此处留空时，再按默认规则显示状态信息
	///		默认规则为：依据Buff的持有者开关条件配置，显示“状态性质”信息（@DT_BuffTargetActForbidUICfg）
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "TargetActForbidDescribe")
		FString TargetActForbidDescribe;
	///Buff描述
	///支持：
	///	界面显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Description")
		FString Description;
	///是否显示Buff图标
	///支持：
	///	界面显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "IsShowIcon")
		bool IsShowIcon = true;
	///Buff脚本类型
	///支持：
	///	决定Buff行为、参数的具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffType")
		ENUM_BUFF_CLASS_TYPE BuffType;
	///Buff持有者开关条件
	///支持：
	///	添加条件判定、注册中断响应（@CST-1209）
	///	界面显示：默认的Buff信息界面上的“状态性质”（@CST-12843）
	///		当自定义信息有值时，优先显示自定义值；当自定义信息留空时，再按默认规则显示状态信息
	///		默认规则为：依据“Buff持有者开关条件”配置，显示“状态性质”信息（@DT_BuffTargetActForbidUICfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "TargetActForbid")
		ACTION_FLAG TargetActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Param1")
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Param2")
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Param3")
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Param4")
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "Param5")
		FString Param5;
	///替换条件列表
	///设计原意：
	///	以灵活的方式，实现类似创二中的“叠加”、“替换”
	///支持：
	///	替换流程（Buff添加前，若满足“替换条件”，则本Buff添加失败，改为添加“替换效果”）
	///示例：
	///	①目标霸体时，击退Buff替换为播放指定受击光效（若完全被免疫，则缺少必要反馈）
	///		条件：若目标有霸体状态
	///		替换：则播放光效表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "ReplaceCondition")
		TArray<FSKILL_USE_CONDITION> ReplaceCondition;
	///替换效果列表
	///设计原意：
	///	以灵活的方式，实现类似创二中的“叠加”、“替换”
	///支持：
	///	替换流程（Buff添加前，若满足“替换条件”，则本Buff添加失败，改为添加“替换效果”）
	///示例：
	///	①目标霸体时，击退Buff替换为播放指定受击光效（若完全被免疫，则缺少必要反馈）
	///		条件：若目标有霸体状态
	///		替换：则播放光效表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "ReplaceEffectList")
		TArray<FHIT_EFFECT> ReplaceEffectList;
	///额外条件列表
	///设计原意：
	///	以灵活的方式，实现类似创二中的“叠加”、“替换”
	///支持：
	///	额外流程（Buff添加后注册前，若满足“额外条件”，则额外添加“额外效果”）
	///示例：
	///	①同时只能有1个变身Buff（可以避免中断行为影响本Buff）
	///		条件：无条件，必然通过
	///		额外：中断其他变身类Buff
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "ExtraCondition")
		TArray<FSKILL_USE_CONDITION> ExtraCondition;
	///额外效果列表
	///设计原意：
	///	以灵活的方式，实现类似创二中的“叠加”、“替换”
	///支持：
	///	额外流程（Buff添加后注册前，若满足“额外条件”，则额外添加“额外效果”）
	///示例：
	///	①同时只能有1个变身Buff（可以避免中断行为影响本Buff）
	///		条件：无条件，必然通过
	///		额外：中断其他变身类Buff
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "ExtraEffectList")
		TArray<FHIT_EFFECT> ExtraEffectList;
	///Buff添加动作ID列表
	///	配置格式：动作ID1:起始帧时间1|动作ID2:起始帧时间2（秒）…（:冒号和|竖号分隔）
	///		示例：“Attack_01|Attack_02:0.5”，代表“顺序播放：从头开始的Attack_01、从0.5秒开始的Attack_02”
	///支持：
	///	Buff添加表现（Buff添加时连续播放，中断/结束/移除时不中止）
	///	支持动作起始帧时间设定（@CST-1192）
	///	支持播放连续动作：任一动作中断则中断连续动作；技能中断则中断对应的连续动作（@CST-3036）
	///注意：
	///	不支持表现重播（@CST-2568）
	///	已知风险：傀儡的表现同步有延迟，请谨慎使用（@CST-2187）
	///		使用“广播机制”进行同步的效果（如EffectAction、Buff的添加光效），在“傀儡受术者”创建时立即添加无效，建议延迟添加
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffAction")
		FString BuffAction;
	///Buff添加光效ID列表
	///	配置格式：光效ID1|光效ID2…（@DT_EffectCfg，|竖号分隔）
	///		示例：“10003|10004”，代表“同时播放两个光效”
	///支持：
	///	Buff添加表现（Buff添加时同时播放，中断/结束/移除时不中止）
	///		光效表现施法者＝（Buff的）施法者
	///		光效表现目标　＝（Buff的）持有者
	///注意：
	///	不支持表现重播（@CST-2568）
	///	已知风险：傀儡的表现同步有延迟，请谨慎使用（@CST-2187）
	///		使用“广播机制”进行同步的效果（如EffectAction、Buff的添加光效），在“傀儡受术者”创建时立即添加无效，建议延迟添加
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffEffect")
		FString BuffEffect;
	///Buff添加音效ID列表
	///	配置格式：音效ID1|音效ID2…（@DT_AudioCfg，|竖号分隔）
	///		示例：“A010001|A0100012”，代表“同时播放两个音效”
	///支持：
	///	Buff添加表现（Buff添加时同时播放，中断/结束/移除时不中止）
	///		音效表现施法者＝（Buff的）施法者
	///		音效表现目标　＝（Buff的）持有者
	///注意：
	///	不支持表现重播（@CST-2568）
	///	已知风险：傀儡的表现同步有延迟，请谨慎使用（@CST-2187）
	///		使用“广播机制”进行同步的效果（如EffectAction、Buff的添加光效），在“傀儡受术者”创建时立即添加无效，建议延迟添加
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BuffSound")
		FString BuffSound;
	///Buff持续时间（默认-1秒）
	///	＜0代表“永久”（下线保存永久的Buff有风险，请谨慎使用）
	///	＝0代表“添加之后立即移除”（@CST-3411）
	///支持：
	///	Buff持续计时（向上取整，精确到0.1秒）
	///	下线保存恢复计时（如重新计时、继续计时…等）
	///	刷新持续时间（@CST-2576）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "HoldTime")
		float HoldTime = -1;
	///持有效果列表
	///注意：
	///	已知风险：允许重复配置，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "HoldEffectList")
		TArray<FHOLD_EFFECT> HoldEffectList;
	///响应Buff施法者事件中断列表
	///支持：
	///	响应Buff施法者身上发生的事件，触发此Buff中断
	///注意：
	///	已知风险：允许重复配置，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "CasterInterruptBuffEvent")
		TArray<FSKILL_EVENT> CasterInterruptBuffEvent;
	///响应Buff持有者事件中断列表
	///支持：
	///	响应Buff持有者身上发生的事件，触发此Buff中断
	///	即使留空，也会注册一些默认的事件响应，如“Buff持有者开关条件”
	///注意：
	///	已知风险：允许重复配置，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "TargetInterruptBuffEvent")
		TArray<FSKILL_EVENT> TargetInterruptBuffEvent;
	///下线保存类型
	///支持：
	///	PC重新上线时，可重新加载已保存的Buff
	///注意：
	///	已知风险：【不支持表现重播】的表现，在重新上线后将【不会恢复】，请谨慎使用
	///		如：Buff添加动作/光效/音效、子弹Buff的子弹光效、击退Buff的动作/位移
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "SaveType")
		ENUM_BUFF_SAVE_TYPE SaveType;
	///开始打击列表
	///支持：
	///	Buff开始后，执行一次“开始打击”
	///		打击施法者＝（Buff的）施法者
	///		打击目标　＝（Buff的）持有者
	///注意：
	///	脚本类型：BuffHit限定
	///	触发时机在“注册”之后，可享受持有效果
	///	Buff重新加载/叠加时，不执行“开始打击”（如“重新加载sven飞锤，不会再次AOE晕”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "BeginHitList")
		TArray<FBUFF_HIT> BeginHitList;
	///Buff周期时间（默认0秒，≤0秒代表“不会触发周期打击”）
	///支持：
	///	精确到0.1秒，向下取整
	///	以下脚本支持【默认值修正】，一般无需手动配置：当LoopTime＝缺省0时，将被视为1秒（@CST-9200）
	///		BuffLink、BuffBeLink、BuffHook、BuffBeHook（@CST-9200）
	///		BuffPromptOper、BuffPromptOperShowArea（@CST-9200）
	///		BuffTaunt、BuffGhostEye（@CST-9200）
	///		BuffAircraft、BuffLingMai（@CST-9200）
	///注意：
	///	脚本类型：BuffLoop限定
	///	已知风险：由于以下原因，周期打击的具体次数不可靠，请谨慎使用，尽量避免设计“对周期次数要求严格”的玩法
	///		①重新加载时，将重置周期计时（离线前后加起来，总次数可能比预期多）
	///		②Buff叠加时，不更新周期计时（刷新持续时间后，总次数可以增加）
	///		③周期计时精度不足（如“持续1秒，周期0.1秒”，表现为“有时打9下，有时打10下”），建议避免设计过短的周期
	///		④打击内容太多时，将推迟周期触发（@CST-6210），建议避免设计过多的同时内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "LoopTime")
		float LoopTime;
	///周期打击列表
	///支持：
	///	Buff周期时间触发时，执行一次“周期打击”
	///		打击施法者＝（Buff的）施法者
	///		打击目标　＝（Buff的）持有者
	///注意：
	///	脚本类型：BuffLoop限定
	///	已知风险：由于以下原因，周期打击的具体次数不可靠，请谨慎使用，尽量避免设计“对周期次数要求严格”的玩法
	///		①重新加载时，将重置周期计时（离线前后加起来，总次数可能比预期多）
	///		②Buff叠加时，不更新周期计时（刷新持续时间后，总次数可以增加）
	///		③周期计时精度不足（如“持续1秒，周期0.1秒”，表现为“有时打9下，有时打10下”），建议避免设计过短的周期
	///		④打击内容太多时，将推迟周期触发（@CST-6210），建议避免设计过多的同时内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "LoopHitList")
		TArray<FBUFF_HIT> LoopHitList;
	///响应Buff持有者事件触发打击列表
	///支持：
	///	响应Buff持有者身上发生的事件，触发打击
	///注意：
	///	脚本类型：BuffRespond限定
	///	触发时机在“响应事件中断”之前，可享受持有效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "TriggerBuffEvent")
		TArray<FSKILL_EVENT> TriggerBuffEvent;
	///触发打击列表
	///支持：
	///	响应Buff持有者事件时，执行一次“触发打击”
	///		打击施法者＝（Buff的）施法者
	///		打击目标　＝（Buff的）持有者
	///注意：
	///	脚本类型：BuffRespond限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "TriggerHitList")
		TArray<FBUFF_HIT> TriggerHitList;
	///结束打击列表
	///支持：
	///	Buff结束前，执行一次“结束打击”
	///		打击施法者＝（Buff的）施法者
	///		打击目标　＝（Buff的）持有者
	///注意：
	///	脚本类型：BuffHit限定
	///	触发时机在“注销”之前，可享受持有效果
	///	Buff中断/移除时，不执行“结束打击”（如“定时炸弹被驱散时，不会爆炸”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "EndHitList")
		TArray<FBUFF_HIT> EndHitList;
	///备注信息
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuffData", DisplayName = "备注")
		FString Remarks;

public:
	///不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (BuffIcon.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(BuffIcon.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"BuffIcon\" resource does not exist"));
			}
		}
	}

	///会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBUFF_CLIENT_EFFECT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///Buff客户端表现类型（整型，应当与“行号”保持一致）
	///支持：
	///	①对应BuffStone的参数3“Buff客户端材质表现类型ID”
	///注意：
	///	目前功能无区别，表现可自定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 EffectType;
	///效果材质细节法线贴图
	///	影响表面光照强弱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> StoneDetailNormal;
	///效果材质法线强度（越大越明显）
	///	与法线贴图（StoneDetailNormal）共同作用，可加强对材质的光照影响
	///	类似透明度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float StoneNormalIntensity;
	///效果材质混合度（越大越明显）
	///	类似透明度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float StonePetrifiedAlpha;
	///效果材质粗糙度B（越大越粗糙）
	///	影响材质的光滑度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float StoneRoughnessB;
	///效果材质粗糙度H（越大越粗糙）
	///	影响材质的光滑度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float StoneRoughnessH;
	///效果材质高光（越大越反光）
	///	影响材质对光的反射程度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float StoneSpecular;
	///效果材质颜色贴图
	///	影响材质的基本颜色表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> StoneTexture_D;
	///效果法线贴图
	///	与法线贴图（StoneDetailNormal）共同作用，影响材质表面的光照强弱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> StoneTexture_N;
	///效果描述（字符串）
	///	无功能，仅供备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;

public:
	///不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;

		if (StoneDetailNormal.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(StoneDetailNormal.ToString()))
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("; \"StoneDetailNormal\" resource does not exist"));
			}
		}
		else
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("; \"StoneDetailNormal\" config is None"));
		}

		if (StoneTexture_D.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(StoneTexture_D.ToString()))
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"StoneTexture_D\" resource does not exist"));
			}
		}
		else
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"StoneTexture_D\" config is None"));
		}

		if (StoneTexture_N.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(StoneTexture_N.ToString()))
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"StoneTexture_N\" resource does not exist"));
			}
		}
		else
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"StoneTexture_N\" config is None"));
		}
		if (bHasError)
		{
			ResultInfo.CheckLog = ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	///会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/*
	Buff开关条件显示配置
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBUFF_TARGETACTFORBID_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///Buff持有者开关条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ACTION_FLAG TargetActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///文字描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ChineseDesc;
};