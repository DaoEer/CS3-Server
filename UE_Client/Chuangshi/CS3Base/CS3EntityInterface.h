// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"

#include "KBEngine.h"
#include "Engine/DataAsset.h"
#include "Engine/EngineTypes.h"

#include "CS3InterfaceDeclare.h"

#include "GameData/CS3Object.h"
#include "CS3EntityInterface.generated.h"


/**
 * 
 */
class CS3Entity;

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UCS3EntityInterface : public UCS3Object
{
	GENERATED_BODY()

public:
	UCS3EntityInterface();
	virtual ~UCS3EntityInterface();

	//entity初始化完成的回调
	virtual void __init__() {};

	/**
	* Called after the C++ constructor and after the properties have been initialized, including those loaded from config.
	* mainly this is to emulate some behavior of when the constructor was called after the properties were initialized.
	*/
	virtual void PostInitProperties() override;

	/**
	*获取Actor
	*
	*@return AActor * OwnerActor
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		AActor *GetActor();

	/**
	*设置OwnerActor
	*
	*@param Actor 参数Actor
	*
	*@return bool 设置OwnerActor返回TRUE
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		bool SetActor(const AActor *Actor);

	/**
	*调用cell方法
	*
	*@param methodname 方法名
	*@param arguments 方法参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		void CellCallWithBp(const FString &methodname, const TArray<FString> &arguments);
	void CellCall(const FString& name, const KBEngine::FVariantArray& args=KBEngine::FVariantArray());
	void BaseCall(const FString& name, const KBEngine::FVariantArray& args = KBEngine::FVariantArray());

	/**
	*调用cell方法，参数为Int数组
	*
	*@param methodname 方法名
	*@param arguments 方法参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		void CellCallWithIntList(const FString &methodname, const TArray<int32> &arguments);

	/**
	*调用cell方法，参数为String数组
	*
	*@param methodname 方法名
	*@param arguments 方法参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		void CellCallWithFStringList(const FString &methodname, const TArray<FString> &arguments);

	/**
	*调用Base方法
	*
	*@param methodname 方法名
	*@param arguments 方法参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		void BaseCallWithBp(const FString &methodname, const TArray<FString> &arguments);
	void BaseCall(const FString& name, KBEngine::FVariantArray& args);

	/**
	*调用Base方法，参数为Int数组
	*
	*@param methodname 方法名
	*@param arguments 方法参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		void BaseCallWithIntList(const FString &methodname, const TArray<int32> &arguments);

	/**
	*调用Base方法，参数为String数组
	*
	*@param methodname 方法名
	*@param arguments 方法参数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		void BaseCallWithFStringList(const FString &methodname, const TArray<FString> &arguments);


	/**
	*获取接口
	*
	*@param FString 接口名
	*
	*@return CS3EntityInterface* 接口对象
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3EntityInterface")
		UCS3EntityInterface* GetInterfaceByName(FString interfacname);


	virtual void onEnterWorld();///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld(); ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void OnEnterScenes() {};///<开始场景
	virtual void OnLeaveScenes() {};///<离开场景

	UFUNCTION(BlueprintImplementableEvent, Category = "CS3EntityInterface")
		void BP_onEnterWorld();///<BlueprintImplementableEvent， 当Entity进入世界时，此方法被调用
	UFUNCTION(BlueprintImplementableEvent, Category = "CS3EntityInterface")
		void BP_onLeaveWorld();///< BlueprintImplementableEvent，当Entity离开世界（被销毁时）时，此方法被调用

	/**
	*获取Entity
	*
	*@return KBEngine::Entity*  Entity
	*/
	KBEngine::Entity *GetEntity();

	CS3Entity *GetMyEntity();
	
	//template< typename TT >




	/**
	*设置Entity
	*
	*@param ent Entity
	*
	*@return bool 设置Entity为ent返回TRUE
	*/
	bool SetEntityID(int32 entID);

	/**
	*加载接口
	*
	*@param KBEEntities 所有继承CS3EntityInterface的接口
	*@param name 接口名
	*@param type 接口类型
	*@param ent 接口Entity
	*@param entid 接口EntityID
	*
	*@return 无
	*/

public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CS3EntityInterface")
		int32 EntityID;///<EntityID

private:
	UPROPERTY()
		AActor *OwnerActor;///<OwnerActor

		//KBEngine::Entity *Entity;///<Entity


//方法、属性回调到篮图方法
protected:
	TArray<FString> ArrBlueFunc;
	TArray<FString> ArrBluePropertyCB;

public:
	virtual void InitBlueCB();

//处理远程接口调用
public:
	//引擎回调方法
	virtual void OnUpdateProperty(const FString &name, const FVariant &newVal, const FVariant &oldVal);
	virtual void OnRemoteMethodCall(const FString &name, const TArray<FVariant> &args);

public:
	static CS3_INTERFACE_METHOD_MAP _thisMethodMap;
	static CS3_INTERFACE_PROPERTY_MAP _thisPropertyMap;
	static void InitMethodMap() { _thisMethodMap.Add(TEXT(""), nullptr); }
	static void InitPropertyMap() { _thisPropertyMap.Add(TEXT(""), nullptr); }
protected:
	virtual void CallDefineMethod(const FString &name, const TArray<FVariant> &args) {};
	virtual void NotifyDefineProperty(const FString &name, const FVariant &newVal, const FVariant &oldVal) {};

public:
	static FString GetName() { return TEXT(""); } 
	static FString GetBlueprintClassPath() { return TEXT(""); } 
};
