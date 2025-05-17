#include <stdio.h>
#include <string.h>

int main(void){
	char 
		str1[20] = "hello",
		str2[20] = "hello";
	
	int ret;
	
	ret = strncmp(str1, str2, 3);
	
	if(ret < 0){
		printf("str2 maggiore");
	}else if(ret == 0){
		printf("sono uguali");
	}
	else{
		printf("str1 maggiore");
	}
	printf("%d", ret);
	return 0;
}
