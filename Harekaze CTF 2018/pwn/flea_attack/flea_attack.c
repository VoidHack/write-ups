int del_name() {
  int result; // eax@1
  __int64 v1; // rsi@1
  void *addr; // [sp+10h] [bp-10h]@1
  __int64 canary; // [sp+18h] [bp-8h]@1

  canary = *MK_FP(__FS__, 40LL);
  addr = 0LL;
  printf("Addr: ");
  __isoc99_scanf("%llx", &addr);
  free(addr);
  result = puts("Done!");
  v1 = *MK_FP(__FS__, 40LL);
  return result;
}



int add_name() {
  int size; // ST2C_4@1
  void *buf; // ST20_8@1

  printf("Size: ");
  size = gets_int();
  buf = malloc(size);                           // fastbin top to flag address
  printf("Name: ");
  read(0, buf, size);
  puts("Done!");
  printf("Name: %s\n", buf);                    // here is have to be the flag address
  return printf("Addr: %llx\n", buf);
}



int gets_int() {
  int num; // eax@1
  char input; // [sp+1Ch] [bp-14h]@1
  __int64 canary; // [sp+28h] [bp-8h]@1

  canary = *MK_FP(__FS__, 40LL);
  fgets(&input, 11, stdin);
  num = atoi(&input);
  *MK_FP(__FS__, 40LL);
  return num;
}



int show_menu() {
  puts("1. Add name");
  puts("2. Delete name");
  return puts("3. Exit");
}



__int64 __fastcall original_fgets(__int64 ptr, __int64 size) {
  __int64 result; // rax@2
  unsigned __int64 i; // [sp+18h] [bp-18h]@1

  for ( i = 0LL; ; ++i ) {
    result = i;
    if ( i >= size - 1 )
      break;
    read(0, (void *)(i + ptr), 1uLL);
    if ( !*(_BYTE *)(ptr + i) ) {
      *(_BYTE *)(ptr + i) = '\n';
LABEL_7:
      result = ptr;
      *(_BYTE *)(ptr + i + 1) = 0;
      return result;
    }
    if ( *(_BYTE *)(ptr + i) == '\n' )
      goto LABEL_7;
  }
  return result;
}



__int64 gets_comment() {
  return original_fgets((__int64)&comment, 96LL);
}



char *open_flag() {
  FILE *stream; // [sp+18h] [bp-8h]@1

  stream = fopen("/home/flea_attack/flag", "r");
  if ( !stream ) {
    puts("ERROR: Open Error");
    exit(1);
  }
  return fgets((char *)&flag, 48, stream);
}



int __cdecl __noreturn main(int argc, const char **argv, const char **envp) {
  int choice; // [sp+20h] [bp-20h]@2

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  open_flag();
  printf("Some comment this note:", 0LL);
  gets_comment();
  while ( 1 ) {
    while ( 1 ) {
      show_menu();
      printf("> ");
      choice = gets_int();
      if ( choice != 1 )
        break;
      add_name();
    }
    if ( choice == 2 ) {
      del_name();
    }
    else {
      if ( choice == 3 ) {
        puts("Bye.");
        exit(0);
      }
      puts("Invalid");
    }
  }
}