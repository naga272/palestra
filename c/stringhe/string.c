#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>


#define checker(x, msg)                             \
if (x) {                                            \
    printf("error %d: %s", errno, msg);             \
    exit(EXIT_FAILURE);                             \
}


typedef struct stringa{
    char* s;
    size_t len_s;
    void (*append)(struct stringa*, char*);
    void (*del)(struct stringa*);
} string;


string* String(char* s);
void __append(string *self, char *s_to_copy);
void __del__(struct stringa*);
size_t get_len_char_ptr(char* s);


size_t get_len_char_ptr(char* s) 
{
    size_t index = 0;
    while (s[index] != '\0') {
        index++;
    }
    return index;
}


string* String(char* s)
{
    string *str = (string*) malloc(sizeof(string));
    checker(str == NULL, "errore, impossibile inizializzare un'stanza string! puntatore str == NULL")

    str->s = (char*) calloc(get_len_char_ptr(s) + 1, sizeof(char));
    checker(s == NULL, "errore, impossibile inizializzare un'stanza string! puntatore str->s == NULL")

    size_t index = 0;
    while (s[index] != '\0') {
        str->s[index] = s[index];
        index++;
    }

    str->len_s = index;

    str->append = __append;
    str->del = __del__;
    return str;
}


void __append(string *self, char *s_to_copy)
{
    size_t index = get_len_char_ptr(s_to_copy);

    self->s = (char*) realloc(self->s, self->len_s + index + 1);
    checker(self->s == NULL, "errore, impossibile inizializzare un'stanza string! puntatore str->s == NULL");

    index = 0;
    while (s_to_copy[index]) {
        self->s[self->len_s + index] = s_to_copy[index]; 
        index++;
    }

    self->s[self->len_s + index] = '\0';
    self->len_s += index;
}


void __del__(string *self)
{
    if (self != NULL)
        free(self);
}


int main() 
{
    string *s = String("Hello World");
    printf("%s\n", s->s);

    s->append(s, "hello world");
    printf("%s\n", s->s);

    s->del(s);
    return EXIT_SUCCESS;
}
