/* link_trampolines.cpp -- AUTO-GENERATED flat->member bridges (LINK phase). */
#include "nfs4_types.h"

void Display(tDialogBase* a0) {
  a0->Display();
}
void Hide(tDialogBase* a0) {
  a0->Hide();
}
short Run(tDialogInteractive* a0) {
  return (short)(a0->Run());
}
void Redraw(tFEApplication* a0) {
  a0->Redraw();
}
void UpdateMusic(tFEApplication* a0) {
  a0->UpdateMusic();
}
void SaveTournament(tTournamentManager* a0, tSaveTournament* a1) {
  a0->SaveTournament(a1);
}
void LoadTournament(tTournamentManager* a0, tSaveTournament* a1) {
  a0->LoadTournament(a1);
}
void SaveTracks(tTrackManager* a0, tSaveTrackInfo* a1) {
  a0->SaveTracks(*a1);
}
void LoadTracks(tTrackManager* a0, tSaveTrackInfo* a1) {
  a0->LoadTracks(*a1);
}
void SaveCars(tCarManager* a0, tSaveCarInfo* a1) {
  a0->SaveCars(*a1);
}
void LoadCars(tCarManager* a0, tSaveCarInfo* a1, short a2) {
  a0->LoadCars(*a1, a2);
}
void LoadPinkSlipsCars(tCarManager* a0, tSaveCarInfo* a1, short a2) {
  a0->LoadPinkSlipsCars(*a1, a2);
}
int GetHelpText(tScreenControllerConfig* a0) {
  return (int)(a0->GetHelpText());
}
void DisplayHelp(tFEApplication * a0, int a1) {
  a0->DisplayHelp(a1);
}
void GetGarageCar(tCarManager* a0, unsigned a1, tCarInfo* a2, int a3) {
  a0->GetGarageCar(a1, *a2, a3);
}
void * GetCarFromID(tCarManager* a0, int a1) {
  return (void *)(a0->GetCarFromID(a1));
}
void * TransitionIsFinished(tOptionsMenu * a0) {
  return (void *)(a0->TransitionIsFinished());
}
int Percentage(tMenuItemLeftRightAudioSlider * a0) {
  return (int)(a0->Percentage());
}
void DrawBackgroundImage(tScreen* a0, int a1, int a2, tTexture_ShapeInfo* a3, int a4) {
  a0->DrawBackgroundImage(a1, a2, a3, a4);
}
void * IsShapeFileLoaded(tScreen* a0, tShapeInformation* a1) {
  return (void *)(a0->IsShapeFileLoaded(*a1));
}
void FreeShapes(tScreen* a0, tShapeInformation* a1) {
  a0->FreeShapes(*a1);
}
void InitializeShapes(tScreen* a0, tShapeInformation* a1, int a2) {
  a0->InitializeShapes(*a1, a2);
}
void AsyncLoadSwapShapeFile(tScreen* a0, char* a1) {
  a0->AsyncLoadSwapShapeFile(a1);
}
void AsyncLoadShapeFile(tScreen* a0, char* a1, tShapeInformation* a2) {
  a0->AsyncLoadShapeFile(a1, *a2);
}
void TurnOn(tVideoWall* a0) {
  a0->TurnOn();
}
void TurnOff(tVideoWall* a0) {
  a0->TurnOff();
}
void TurnOffInstant(tVideoWall* a0) {
  a0->TurnOffInstant();
}
void UpdateImages(tVideoWall* a0) {
  a0->UpdateImages();
}
void UpdateTransition(tVideoWall* a0) {
  a0->UpdateTransition();
}
void Draw(tVideoWall* a0) {
  a0->Draw();
}
void SetAvailable(tVideoWall* a0, unsigned a1) {
  a0->SetAvailable(a1);
}
void SetAvailableText(tVideoWall* a0, short a1, short a2, short a3) {
  a0->SetAvailableText(a1, a2, a3);
}
void GetTrack(tTrackManager* a0, unsigned a1, void* a2) {
  a0->GetTrack(a1, *(tTrackInformation*)a2);
}
tTrackInformation * GetTrackByID(tTrackManager* a0, short a1) {
  return (tTrackInformation *)(a0->GetTrackByID(a1));
}
void PreLoad(tScreen* a0) {
  a0->PreLoad();
}
tCarInfo * GetCarFromID(tCarManager * a0, short a1) {
  return (tCarInfo *)(a0->GetCarFromID(a1));
}
void GetGarageCar(tCarManager * a0, short a1, tCarInfo * a2, short a3) {
  a0->GetGarageCar(a1, *a2, a3);
}
void GetPinkSlipsCar(tCarManager * a0, short a1, tCarInfo * a2, short a3) {
  a0->GetPinkSlipsCar(a1, *a2, a3);
}
void GetAwardInformation(tTournamentManager * a0, tAwardInformation * a1) {
  a0->GetAwardInformation(a1);
}
short PlayerRanking(tTournamentManager * a0, short a1) {
  return (short)(a0->PlayerRanking(a1));
}
void UploadSwapShapes(tScreen * a0, int a1) {
  a0->UploadSwapShapes(a1);
}
void UploadShapes(tScreen* a0, tShapeInformation* a1, short a2, short a3, int a4, int a5) {
  a0->UploadShapes(*a1, a2, a3, a4, a5);
}
void InitializeShapes(tScreen* a0, tShapeInformation* a1, unsigned a2) {
  a0->InitializeShapes(*a1, a2);
}
void Init(tCreditManager* a0, u_long a1) {
  a0->Init(a1);
}
void DeInit(tCreditManager* a0) {
  a0->DeInit();
}
void Draw(tCreditManager* a0, int a1) {
  a0->Draw(a1);
}
short TextValue(tListIteratorTournament * a0, tPlayer a1) {
  return (short)(a0->TextValue(a1));
}
short * GetTrackList(tTournamentManager * a0, short a1, short a2) {
  return (short *)(a0->GetTrackList(a1, a2));
}
void GetTrackToRace(tTournamentManager * a0, tTrackInfo * a1) {
  a0->GetTrackToRace(a1);
}
short TextValue(tListIteratorTrack * a0, tPlayer a1) {
  return (short)(a0->TextValue(a1));
}
void Decrement(tListIteratorTrack * a0, tPlayer a1) {
  a0->Decrement(a1);
}
void Increment(tListIteratorTrack * a0, tPlayer a1) {
  a0->Increment(a1);
}
void GetTrack(tTrackManager * a0, u_short a1, tTrackInformation * a2) {
  a0->GetTrack(a1, *a2);
}
void SetAvailable(tVideoWall * a0, u_short a1) {
  a0->SetAvailable(a1);
}
void ProcessInput(tScreen * a0, tPlayer a1, tInputKeyType & a2, tMenuCommand & a3) {
  a0->ProcessInput(a1, a2, a3);
}
tCarInfo * GetCarFromSimID(tCarManager * a0, short a1) {
  return (tCarInfo *)(a0->GetCarFromSimID(a1));
}
