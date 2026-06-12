/* game/psx/textsys.cpp -- RECONSTRUCTED (NFS4 PSX text/word system; C++ TU)
 *   8 fns: TextSys_LoadWordsGeneric/LoadInGame/LoadWords, Word/WordFlags/WordX/WordY, UnloadWords.
 *   GTE-free. Full SYM-locals applied.
 */
#include "../../nfs4_types.h"
#include "textsys_externs.h"

/* ---- intra-TU forward declarations (auto-emitted, signature-exact) ---- */
void TextSys_LoadWordsGeneric(int language,char *path);
void TextSys_LoadInGame(int language);
void TextSys_LoadWords(int language);
char * TextSys_Word(int wordnum);
int TextSys_WordFlags(int wordnum);
int TextSys_WordX(int wordnum);
int TextSys_WordY(int wordnum);
void TextSys_UnloadWords(void);


/* ---- TextSys_LoadWordsGeneric__FiPc  [TEXTSYS.CPP:41-52] SLD-VERIFIED ---- */
void TextSys_LoadWordsGeneric(int language,char *path)

{
  char *pcVar1;
  char string [250];
  
  if (language < 7) {
    if (wordFile != (char *)0x0) {
      purgememadr(wordFile);
    }
    pcVar1 = (char *)sprintf(string,"%s%s",path,langFileName[language]);
    loadfileadr(string,0);
    wordFile = pcVar1;
  }
  return;
}

/* ---- TextSys_LoadInGame__Fi  [TEXTSYS.CPP:55-58] SLD-VERIFIED ---- */
void TextSys_LoadInGame(int language)

{
  char fullpath [80];
  
  sprintf(fullpath,"%s%s",Paths_Paths[0x1a],"p");
  TextSys_LoadWordsGeneric(language,fullpath);
  return;
}

/* ---- TextSys_LoadWords__Fi  [TEXTSYS.CPP:62-63] SLD-VERIFIED ---- */
void TextSys_LoadWords(int language)

{
  TextSys_LoadWordsGeneric(language,Paths_Paths[0x22]);
  return;
}

/* ---- TextSys_Word__Fi  [TEXTSYS.CPP:69-75] SLD-VERIFIED ---- */
char * TextSys_Word(int wordnum)

{
  return wordFile + *(int *)(wordFile + wordnum * 0xc + 8);
}

/* ---- TextSys_WordFlags__Fi  [TEXTSYS.CPP:120-126] SLD-VERIFIED ---- */
int TextSys_WordFlags(int wordnum)

{
  return (u_int)(u_char)wordFile[wordnum * 0xc + 3];
}

/* ---- TextSys_WordX__Fi  [TEXTSYS.CPP:132-141] SLD-VERIFIED ---- */
int TextSys_WordX(int wordnum)

{
  return (int)*(short *)(wordFile + wordnum * 0xc + 4);
}

/* ---- TextSys_WordY__Fi  [TEXTSYS.CPP:147-156] SLD-VERIFIED ---- */
int TextSys_WordY(int wordnum)

{
  return (int)*(short *)(wordFile + wordnum * 0xc + 6);
}

/* ---- TextSys_UnloadWords__Fv  [TEXTSYS.CPP:162-165] SLD-VERIFIED ---- */
void TextSys_UnloadWords(void)

{
  char fullpath [80];
  
  if (wordFile != (char *)0x0) {
    purgememadr(wordFile);
  }
  wordFile = (char *)0x0;
  return;
}

/* end of textsys.cpp */
