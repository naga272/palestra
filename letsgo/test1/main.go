package main


import "fmt" // ciao


func main(){
        s := "Hello world";
        r := []byte(s)
        r[0] = 'C'
        s = string(r)
        fmt.Println(s);
}

