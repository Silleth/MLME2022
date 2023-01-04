// Fill out your copyright notice in the Description page of Project Settings.


#include "SC_DialogueM.h"
#include "UObject/ConstructorHelpers.h"
#include "ML_ProjectCharacter.h"
#include "Engine/DataTable.h"

// Sets default values for this component's properties
USC_DialogueM::USC_DialogueM()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


void USC_DialogueM::InitiateDialogue(bool ShouldSpeak, bool ReferenceBool)
{
	// Assign value and set correct tick enable state
	SpeakEnable = ShouldSpeak;
	//MoveEnable = false;
	

	if (ChatToken > 0 && ShouldSpeak && RefBool)
	{
		//SetComponentTickEnabled(MoveEnable);
		USC_DialogueM::StartDialogue();
		//USC_DialogueM::AddDialogueInstance();
		
		//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("You initiate dialogue"));
		if (!RefBool)
		{
			ChatToken = 0;
			//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("You lost your token"));
		}
	}
	
}

void USC_DialogueM::EnableCheck(bool CheckTalk)
{
	CheckSpeakEnable = CheckTalk;
	if (CheckTalk)
	{
		ChatToken += 1;
		
	}

	if (ChatToken > 0)
	{
		bool BufferBool = false;
		RefBool = CheckTalk;
		USC_DialogueM::InitiateDialogue(BufferBool, RefBool);
	}
}

// Called when the game starts
void USC_DialogueM::BeginPlay()
{
	Super::BeginPlay();
	// ...
	

}


// Called every frame
void USC_DialogueM::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	// ...

}

void USC_DialogueM::Reset()
{
	UsedRow.Reset();
}

// Called when the game starts
void USC_DialogueM::StartDialogue()
{
	//USC_DialogueM::AddDialogueInstance();

	// Source - calling data table
	static const FString ContextString(TEXT("LabelString"));
	//int32 RowNumber = PlayerDialogueNum;
	FString RowString = FString::FromInt(PlayerDialogueNum);
	FName RowName = FName(*RowString);


	FPlayerDialogue* Dialogue = PlayerDialogueData->FindRow<FPlayerDialogue>(RowName, ContextString, true);
	if (Dialogue)
	{

		/** Initialize data for input dialogue **/
		TArray<float> CorrVals = Dialogue->LabelCorrs;
		int32 AttitudeVals = Dialogue->Attitude;
		int32 AttitudeRange = 3;
		FString DialogueTypes = Dialogue->Type;

		/** Debug confirmation that data is found **/
		//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("We found a row in PlayerDialogueDataframe"));
		FString Name = RowName.ToString();

		/** Retrieve DataTable information **/
		FString DataPrint = PlayerDialogueData->GetTableAsString(EDataTableExportFlags::None);
		TArray<FName> DataPrintRow = PlayerDialogueData->GetRowNames();
		//TArray<FString> DataPrintColumn = PlayerDialogueData->GetColumnTitles();

		//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, SpecifiedColumn);

		/** Table Sampling **/
		int32 CountRow = DataPrintRow.Num();
		//int32 CountColumn = DataPrintColumn.Num();
		// ...
		FName Rows = DataPrintRow[1];
		FString LabelString = Dialogue->LabelString;

		/** FString convertions **/
		FString RowsStr = Rows.ToString();
		FString CountRowStr = FString::FromInt(CountRow);

		
		//TArray<int32> UsedRow;
		RelevantRow.Reset();

		/** Goes through each collumn possible **/
		for (int32 i = 0; i < CountRow; i++)
		{
			float MinCorr = 0.0f;
			float MaxCorr = 0.0f;
			FString num = FString::FromInt(i);
			FName RowNames(num);
			static const FString ContextStrings(TEXT("Label Corr3"));
			FPlayerDialogue* Dialogues = PlayerDialogueData->FindRow<FPlayerDialogue>(RowNames, ContextStrings, true);
			FString LabelCorrelationNum = FString::SanitizeFloat(CorrVals[i]);
			int32 AttitudeValsOut = Dialogues->Attitude;
			FString AttitudeValsStr = FString::SanitizeFloat(AttitudeValsOut);
			FString DialogueTypesOut = Dialogues->Type;


			/** When the attitude and type of sentence is different (Desired (Now highly desired due to dynamic attitude swap))**/
			if (AttitudeValsOut != AttitudeVals && DialogueTypes != DialogueTypesOut)
			{
				MinCorr += .40f;
				MaxCorr += .70f;
			}
			/** When the attitude is different, and the type of sentence is the same (Not desired at all) **/
			if (AttitudeValsOut != AttitudeVals && DialogueTypes == DialogueTypesOut)
			{
				MinCorr += .49f;
				MaxCorr += .50f;
			}
			/** When the attitude is the same, and the type of sentence is different (Highly desired) **/
			if (AttitudeValsOut == AttitudeVals && DialogueTypes != DialogueTypesOut)
			{
				MinCorr += .40f;
				MaxCorr += .70f;
			}
			/** When the attitude and type of sentence is the same (Not as desired) **/
			if (AttitudeValsOut == AttitudeVals && DialogueTypes == DialogueTypesOut)
			{
				MinCorr += .40f;
				MaxCorr += .55f;
			}

			/** if output attitude subtracted or added with input attitude is higher or lower than threshold **/
			int32 AttitudeValAbsSub = abs(AttitudeVals - AttitudeValsOut);
			int32 AttitudeValAbsAdd = abs(AttitudeVals + AttitudeValsOut);
			if (AttitudeValAbsSub >= AttitudeRange || AttitudeValAbsAdd >= AttitudeRange)
			{
				MinCorr = .50f;
				MaxCorr = .502f;
			}

			/** Add only qualified lines into new array to be sampled from **/
			float CorrVal = CorrVals[i];
			if (CorrVal < MaxCorr && CorrVal > MinCorr && !UsedRow.FindByKey(i))
			{
				RelevantRow.Add(i);
			}


		}
		std::srand(std::time(nullptr));
		int32 Count = RelevantRow.Num();
		FString ChosenRowStr = FString(TEXT("This value is zero"));
		if (Count != 0)
		{
			/** Sample array by random and remember not to be repeated **/
			int32 ChosenRowPass = RelevantRow[rand() % Count + 1 - 1];
			UsedRow.Add(ChosenRowPass);
			FString ChosenRowStrPass = FString::FromInt(ChosenRowPass);
			FName ChosenRowName = FName(*ChosenRowStrPass);
			FPlayerDialogue* DialoguesPass = PlayerDialogueData->FindRow<FPlayerDialogue>(ChosenRowName, ContextString, true);

			//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Green, RelevantRow);
			//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Green, ChosenRowStrPass);
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Green, DialoguesPass->LabelString);
			OutputDialogue = DialoguesPass->LabelString;
		}
		else
		{
			FString ChosenRowStrFail = FString(TEXT("This value is zero and failed"));
			FString Debugger = FString::FromInt(Count);
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, Debugger);
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("No answers are left pending. Try pick another topic."));
			OutputDialogue = TEXT("I think we are done talking.");
		}
	}
}

