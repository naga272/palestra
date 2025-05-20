
#include "./gc.h"


int main()
{
    init_gc();

    void *ptr = gcmalloc(sizeof(int) * 4);

    free_gc();
    return EXIT_SUCCESS;
}
