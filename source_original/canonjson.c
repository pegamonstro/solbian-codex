#include "canon_json.h"
#include <stdio.h>
#include <string.h>

static void usage(const char *argv0){
  fprintf(stderr,"Usage: %s --in <path|-] --out <path|-]\n", argv0);
}

int main(int argc, char **argv){
  const char *in="-", *out="-";
  for (int i=1;i<argc;i++){
    if (!strcmp(argv[i],"--in") && i+1<argc){ in=argv[++i]; continue; }
    if (!strcmp(argv[i],"--out")&& i+1<argc){ out=argv[++i]; continue; }
    if (!strcmp(argv[i],"--help")){ usage(argv[0]); return 0; }
  }
  canon_json_set_locale_c();
  if (canon_json_path(in,out)!=0){
    fprintf(stderr,"canonjson: failed\n");
    return 1;
  }
  return 0;
}