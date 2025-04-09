// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interfaces/IHttpRequest.h"
#include "CS3Object.h"
#include "CS3HttpRequest.generated.h"


DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FCS3RequestDelegate, FString, ContentString);
/**
*
*/
UCLASS()
class CHUANGSHI_API UCS3HttpRequest : public UCS3Object
{
	GENERATED_UCLASS_BODY()
	
public:
	/* Posts a request with the supplied post data to the specified page */
	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Post Http Request"), Category = "CS3HttpRequest")
		static UCS3HttpRequest* PostHttpRequest(const FString& URL, const FString& ContentString);

	/* Requests a page from the internet with a JSON response */
	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Get Http Request"), Category = "CS3HttpRequest")
		static UCS3HttpRequest* GetHttpRequest(const FString& URL);

	UFUNCTION(BlueprintPure, meta = (DisplayName = "Get Json String Field"), Category = "CS3HttpRequest")
		static FString GetJsonStringField(const FString& JsonString, const FString& Key);

public:
	UPROPERTY(BlueprintAssignable, Category = "CS3HttpRequest")
		FCS3RequestDelegate OnSuccess;

	UPROPERTY(BlueprintAssignable, Category = "CS3HttpRequest")
		FCS3RequestDelegate OnFail;

private:
	/** Handles requests coming from the web */
	void HandleRequest(FHttpRequestPtr HttpRequest, FHttpResponsePtr HttpResponse, bool bSucceeded);
};
