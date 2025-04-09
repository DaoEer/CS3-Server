#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtJiuZiZhenYanInterface.generated.h"

/*
* 文件名称：MonsterExtJiuZiZhenYanInterface.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-03-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtJiuZiZhenYanInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtJiuZiZhenYanInterface();
	~UMonsterExtJiuZiZhenYanInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtJiuZiZhenYanInterface'"); } //获取蓝图对象路径

	/**
	*服务器通知自身这一组开始腐化
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJiuZiZhenYanInterface")
		void onStartOccupy();

	/**
	*服务器通知自身这一组结束抢夺
	*
	@param isPlayerOccupy:是否是玩家占领(boss占领)
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJiuZiZhenYanInterface")
		void onEndOccupy(const uint8& isPlayerOccupy);

	/**
	*真言从墙壁上拉扯而出向玩家砸动
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UMonsterExtJiuZiZhenYanInterface")
		void onPoundPlayer();

	virtual void InitBlueCB() override;

	void Set_zhenyanType(const int32& newVal, const int32& oldVal);///<1：临:2：兵:3：斗，4：者:5：皆:6：阵:7：列:8：前:9：行
	void Set_curCorrupt(const int32& newVal, const int32& oldVal);///<当前腐化值
	void Set_maxCorrupt(const int32& newVal, const int32& oldVal);///<最大腐化值

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UMonsterExtJiuZiZhenYanInterface")
		int32 zhenyanType = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UMonsterExtJiuZiZhenYanInterface")
		int32 curCorrupt = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UMonsterExtJiuZiZhenYanInterface")
		int32 maxCorrupt = 0;
private:
	bool mIsStartOccupy = false;
	int8 mOccupyStatus = 0;		//0:未被占领  1：玩家占领  2：boss占领
};
