


quote_t *__fastcall scribe_recall(uint32_t num) {
  quote_t *result; // rax@2
  quote_t *quote; // [sp+18h] [bp-8h]@3

  if ( num < templeWisdom ) {
    quote = temple[(unsigned __int64)num];
    if ( !quote )
      puts("You have already studied this knowledge.");
    result = quote;
  }
  else {
    puts("You will find no knowledge of this here.");
    result = 0LL;
  }
  return result;
}


void __fastcall free_wisdom(quote_t *quote) {
  int i; // [sp+1Ch] [bp-4h]@3

  if ( !strcmp(quote->character, "Neonate\n") )
    mm_free(quote->text);
  mm_free(quote);
  for ( i = 0; i < templeWisdom; ++i ) {
    if ( quote == temple[i] ) {
      temple[i] = 0LL;
      return;
    }
  }
}


void __fastcall print_wisdom(quote_t *quote) {
  write(1, quote->text, quote->text_size);
  write(1, "\t - ", 4uLL);
  write(1, quote->character, quote->character_size);
}


__int64 __fastcall readbytes(char *buf, uint32_t bufsize) {
  fgets(buf, bufsize + 1, stdin);
  return bufsize + 1;
}


__int64 __cdecl readint() {
  __int64 result; // rax@3
  __int64 v1; // rcx@6
  int i; // [sp+Ch] [bp-114h]@2
  char buf[256]; // [sp+10h] [bp-110h]@1
  __int64 v4; // [sp+118h] [bp-8h]@1

  v4 = *MK_FP(__FS__, 40LL);
  if ( fgets(buf, 256, stdin) ) {
    i = atoi(buf);
    if ( i >= 0 )
      result = (unsigned int)i;
    else
      result = 0LL;
  }
  else {
    result = 0LL;
  }
  v1 = *MK_FP(__FS__, 40LL) ^ v4;
  return result;
}


void __cdecl modify_wisdom() {
  unsigned int num; // [sp+4h] [bp-Ch]@1
  quote_t *quote; // [sp+8h] [bp-8h]@3

  printf("What wisdom do you wish to rethink?: ");
  num = readint();
  if ( num > 7 ) {
    quote = scribe_recall(num);
    if ( quote ) {
      printf("(%lu) How do you see this differently?: ", quote->text_size);
      readbytes(quote->text, quote->text_size);
    }
  }
  else {
    puts("That's not your wisdom!");
  }
}


void __cdecl give_wisdom() {
  quote_t *newQuote; // ST10_8@3
  char *v1; // rax@3
  char *newWisdom; // ST18_8@3
  unsigned int v3; // eax@3
  uint32_t size; // [sp+8h] [bp-18h]@1

  printf("How much wisdom do you hold?: ");
  size = readint();
  if ( size ) {
    printf("What is your wisdom?: ");
    newQuote = (quote_t *)mm_malloc(32uLL);
    v1 = (char *)mm_malloc(size);
    newWisdom = v1;
    v3 = readbytes(v1, size);
    newQuote->text = newWisdom;
    newQuote->text_size = v3;
    newQuote->character = "Neonate\n";
    newQuote->character_size = strlen(newQuote->character);
    scribe_store(newQuote);
  }
  else {
    puts("Your wisdom is not wanted here.");
  }
}


void __cdecl take_wisdom() {
  uint32_t input; // ST04_4@1
  quote_t *quote; // [sp+8h] [bp-8h]@1

  printf("What wisdom do you seek?: ");
  input = readint();
  quote = scribe_recall(input);
  if ( quote ) {
    print_wisdom(quote);
    free_wisdom(quote);
  }
}


void __cdecl seek_divinity() {
  int32_t input; // [sp+Ch] [bp-4h]@1

  puts("\nChild, what do you seek?");
  puts("[1] Take wisdom");
  puts("[2] Give wisdom");
  puts("[3] Rethink wisdom");
  printf("Your choice: ");
  input = readint();
  switch ( input ) {
    case 1:
      take_wisdom();
      break;
    case 2:
      give_wisdom();
      break;
    case 3:
      modify_wisdom();
      break;
    default:
      puts("What you ask for cannot be found here.");
      break;
  }
}


void __fastcall scribe_store(quote_t *quote) {
  if ( templeWisdom > 255 ) {
    puts("We have nothing else to offer you. Seek another temple.");
    exit(0);
  }
  temple[(unsigned __int64)templeWisdom++] = quote;
}


quote_t *__cdecl make_wisdom() {
  quote_t *quote; // ST08_8@1
  int v1; // eax@1
  char *chosenProphet; // ST18_8@1
  const char *v3; // rdx@1

  quote = (quote_t *)mm_malloc(32uLL);
  v1 = rand();
  chosenProphet = prophets[(signed int)(v1
                                      - 6
                                      * ((unsigned __int64)(0x0AAAAAAAAAAAAAAABLL
                                                          * (unsigned __int128)(unsigned __int64)v1 >> 64) >> 2))];
  v3 = wisdom[(unsigned __int64)templeWisdom];
  quote->text = (char *)v3;
  quote->text_size = strlen(v3);
  quote->character = chosenProphet;
  quote->character_size = strlen(chosenProphet);
  scribe_store(quote);
  return quote;
}


int main(int argc, const char **argv, const char **envp) {
  unsigned int v3; // eax@1
  int i; // [sp+2Ch] [bp-4h]@1

  setvbuf(stdout, 0LL, 2, 0LL);
  v3 = time(0LL);
  srand(v3);
  horizon();
  for ( i = 0; i <= 7; ++i )
    make_wisdom();
  while ( 1 )
    seek_divinity();
}