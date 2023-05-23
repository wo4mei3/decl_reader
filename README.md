# decl_reader

# Usage
```
$ python3 main.py

> char *const ptr [4] ;

ptr array [ 4 ] of const pointer of char

> char (*const ptr)[4];

ptr const pointer of array [ 4 ] of char

> bool (*(*p)[10])(int a, int b);

p pointer of array [ 10 ] of pointer of function ( a int , b int ) returning bool

> void (*signal(int sig, void(*func)(int a)))(int b);

signal function ( sig int , func pointer of function ( a int ) returning void ) returning pointer of function ( b int ) returning void

```