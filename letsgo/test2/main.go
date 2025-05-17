package main


import (
        "fmt";
        "strings";
        "unicode/utf8";
)


func reverse(s string) string {
        /*
        *       Scrivi una funzione reverse(s string) string che inverte una stringa. 
        *       (Hint: ricordati che le stringhe in Go sono immutabili e codificate in UTF-8…)
        */       
        
        b := []rune(s);

        for start, end := 0, utf8.RuneCountInString(s) - 1; start < end; start, end = start + 1, end - 1 {
                b[start], b[end] = b[end], b[start];
        }  
        
        return string(b);
}


func vocal_counter(s string) int {
        /*
        *       Conta le vocali
        */
        s = strings.ToLower(s);
        a := 0;
        
        for i := 0; i < utf8.RuneCountInString(s); i++ {
                if s[i] == 'a' || s[i] == 'e' || s[i] == 'i' || s[i] == 'o' || s[i] == 'u' {
                        a += 1;
                }
        }
        return a;
}



func occorrenze(s string) map[string]int {
        /* Conta quante volte i caratteri appaiono all'interno della stringa */
        maps_char := map[string]int{};
        
        for _, char := range(s) {
                maps_char[string(char)]++;
        }

        return maps_char;
} 


func palindromo(s string) bool {
        
        len_s := utf8.RuneCountInString(s);
        for i := 0; i < len_s % 2; i++ {
                if (s[i] != s[len_s - 1 - i]) {
                        return false;
                }
        } 
        
        return true;
}


func main() {
        s := "Hello World";      
        fmt.Println(reverse(s));
        fmt.Println(vocal_counter(s));
        fmt.Println(occorrenze(s));

        fmt.Println(palindromo(s));

        fmt.Println(palindromo("anna"));
        
        fmt.Println(palindromo("hello world hello"));
}

