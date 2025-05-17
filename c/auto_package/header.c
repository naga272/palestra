#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <locale.h>
#include <errno.h>
#include <time.h>
#include "./header.h"


#if __unix__
    // i comandi di questa funzione non sono consentiti su windows
    void do__linux__(const char *name_package_ptr){
        static const char *path_base = NULL;
        path_base = name_package_ptr;

        checker(mkdir(path_base, 0777));

        // CREAZIONE README
        char *readme_ptr = (char*) calloc(40, sizeof(char));
        checker(readme_ptr == NULL);
        strcat(readme_ptr, path_base);
        create_readme(strcat(readme_ptr, "README.md"));
        free(readme_ptr);

        // CREAZIONE CHANGELOG
        char *changelog_ptr = (char*) calloc(40, sizeof(char));
        checker(changelog_ptr == NULL);
        strcat(changelog_ptr, path_base);
        create_changelog(strcat(changelog_ptr, "CHANGELOG.txt"));
        free(changelog_ptr);

        // CREAZIONE /BIN/
        char *bin_ptr = (char*) calloc(40, sizeof(char));
        checker(bin_ptr == NULL);
        strcat(bin_ptr, path_base);
        checker(mkdir(strcat(bin_ptr, "bin/"), 0777));
        
        create_pythonfile(strcat(bin_ptr, "file.py"));
        free(bin_ptr);


        // CREAZIONE /FLUSSI/
        char *flussi_ptr = (char*) calloc(40, sizeof(char));
        checker(flussi_ptr == NULL);
        strcat(flussi_ptr, path_base);
        checker(mkdir(strcat(flussi_ptr, "flussi/"), 0777));
        free(flussi_ptr);

        // CREAZIONE /LOG/
        char *log_ptr = (char*) calloc(40, sizeof(char));
        checker(log_ptr == NULL);
        strcat(log_ptr, path_base);
        checker(mkdir(strcat(log_ptr, "log/"), 0777));
        free(log_ptr);


        // CREAZIONE /DB/
        char *db_ptr = (char*) calloc(40, sizeof(char));
        checker(db_ptr == NULL);
        strcat(db_ptr, path_base);
        checker(mkdir(strcat(db_ptr, "db/"), 0777));
        free(db_ptr);

        return ;
    }


#else
    // i comandi di questa funzione non sono consentiti su linux
    void do__windows__(void){
        printf("incomplite yet... )=");
        return ;
    }

#endif


void create_readme(const char* readme){
    FILE *README = fopen(readme, "w");
    checker(README == NULL);
    const char *text_readme = "# TITLE\n\n![Language](https://img.shields.io/badge/Spellcheck-Pass-green?style=flat)  ![Platform](https://img.shields.io/badge/OS%20platform%20supported-Linux-green?style=flat) ![Language](https://img.shields.io/badge/Language-Python-yellowgreen?style=flat) ![Testing](https://img.shields.io/badge/PEP8%20CheckOnline-Passing-green)  ![Testing](https://img.shields.io/badge/Test-Pass-green)\n\n## Descrizione\nsome_text\n\n## Requisiti\nsome_text\n\n## Esecuzione\nsome_text\n## Tags\n\nsome_text\n\n## Author\nsome_text\n";

    fprintf(README, "%s", text_readme);
    fclose(README);
    return;
}


void create_changelog(const char* changelog){
    FILE *CHANGELOG = fopen(changelog, "w");
    checker(CHANGELOG == NULL);
    time_t tempo = time(NULL);

    // # changelog\n\n## version [1.0.1] - %s
    char *changelog_text = "\n\n### added\n\t- ./CHANGELOG.txt\n\t- ./README.md\n\t- /db/\n\t- /log/\n\t- /flussi/\n\t- /bin/\n\t- /bin/python.py\n";

    fprintf(CHANGELOG, "# changelog\n\n## version [1.0.1] - %s", ctime(&tempo));
    fprintf(CHANGELOG, changelog_text);

    fclose(CHANGELOG);
    return;
}


void create_pythonfile(const char* file_py){
    FILE *PYTHON = fopen(file_py, "w");
    checker(PYTHON == NULL);

    const char *library = "\n#import standard library\nfrom datetime import datetime\nimport platform\nimport time\nimport sys\nimport os\nimport re\n";
    const char *def_log = "\n\n\ndef log():\n    return 0\n\n\n";

    const char *def_main = "def main(argc:int, argv:list):\n    #argc rappresenta il numero di argomenti passati\n    #argv e' la lista con gli argomenti\n    return 0\n\n\n";
    const char *name_main = "if __name__ == \"__main__\":\n    main(len(sys.argv), sys.argv)";

    fprintf(PYTHON, "%s", library);
    fprintf(PYTHON, "%s", def_log);
    fprintf(PYTHON, "%s", def_main);
    fprintf(PYTHON, "%s", name_main);

    fclose(PYTHON);
    return ;
}